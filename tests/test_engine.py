from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
import unittest

from invoice_contract.engine import audit,decimal,digest,prepare
from invoice_contract.ubl import parse_invoice

ROOT=Path(__file__).resolve().parent.parent


def example():return json.loads((ROOT/"invoice_contract/examples/partial-receipt.json").read_text())


class AcceptanceTests(unittest.TestCase):
    def test_partial_receipt_and_previous_billing_are_both_accounted(self):
        report=audit(example())
        self.assertEqual(report["status"],"blocked")
        self.assertEqual(report["lines"][0]["permitted_quantity"],"1")
        self.assertEqual({f["code"] for f in report["findings"]},{"quantity_exceeds_contract","price_mismatch"})

    def test_repair_draft_reaudits_cleanly_without_mutating_source(self):
        case=example();before=deepcopy(case);proposal=prepare(case)
        self.assertEqual(case,before)
        self.assertEqual(proposal["status"],"draft_ready_for_review")
        self.assertEqual(proposal["after_line_subtotal"],"12.50")
        self.assertEqual(len(proposal["changes"]),2)
        self.assertFalse(proposal["approval_or_execution_performed"])
        self.assertFalse(proposal["audit"]["payment_authorized"])
        self.assertEqual(proposal["external_actions"],[])

    def test_missing_receipt_is_unknown_not_invented_delivery(self):
        case=example();case["receipts"]=[]
        report=audit(case)
        self.assertIsNone(report["lines"][0]["permitted_quantity"])
        self.assertIn("missing_receipt_evidence",{f["code"] for f in report["findings"]})
        self.assertEqual(prepare(case)["status"],"needs_evidence_or_human_edit")

    def test_ordered_billing_basis_allows_delivery_independent_contract(self):
        case=example();case["receipts"]=[];case["order"]["lines"][0]["billing_basis"]="ordered"
        proposal=prepare(case)
        self.assertEqual(proposal["draft"]["invoice"]["lines"][0]["quantity"],"4")
        self.assertEqual(proposal["after_line_subtotal"],"50.00")

    def test_identical_receipt_retry_does_not_double_capacity(self):
        case=example();case["receipts"].append(deepcopy(case["receipts"][0]))
        self.assertEqual(audit(case)["lines"][0]["permitted_quantity"],"1")

    def test_conflicting_receipt_id_blocks_draft(self):
        case=example();copy=deepcopy(case["receipts"][0]);copy["quantity"]="100";case["receipts"].append(copy)
        self.assertIsNone(prepare(case)["draft"])

    def test_currency_and_identifier_scheme_cannot_be_silently_converted(self):
        for field,value in (("currency","USD"),("buyer",{"scheme":"different","value":"buyer-01"})):
            case=example();case["invoice"][field]=value
            self.assertIsNone(prepare(case)["draft"])

    def test_duplicate_invoice_scope_includes_seller(self):
        case=example();case["seen_invoices"]=[{"id":case["invoice"]["id"],"seller":{"scheme":"demo","value":"other"}}]
        self.assertNotIn("invoice_seen_before",{f["code"] for f in audit(case)["findings"]})
        case["seen_invoices"][0]["seller"]=case["invoice"]["seller"]
        self.assertIsNone(prepare(case)["draft"])

    def test_split_lines_cannot_each_consume_full_remaining_capacity(self):
        case=prepare(example())["draft"];line=deepcopy(case["invoice"]["lines"][0]);line["id"]="2";case["invoice"]["lines"].append(line);case["invoice"]["line_subtotal"]="25.00"
        report=audit(case)
        self.assertIn("quantity_exceeds_contract",{f["code"] for f in report["findings"]})
        self.assertEqual(prepare(case)["status"],"needs_evidence_or_human_edit")

    def test_unresolved_reference_stays_in_review_without_sku_guess(self):
        case=example();case["invoice"]["lines"][0]["order_line_id"]=None
        report=audit(case)
        self.assertEqual(report["status"],"review")
        self.assertEqual(report["findings"][0]["expected"],["10"])
        self.assertIsNone(report["lines"][0]["permitted_quantity"])

    def test_source_digest_changes_after_new_receipt(self):
        case=example();before=prepare(case)["snapshot_sha256"];case["receipts"][0]["quantity"]="4"
        self.assertNotEqual(before,digest(case))

    def test_exact_decimal_rounding(self):
        from invoice_contract.engine import money
        self.assertEqual(money(Decimal("0.335")),"0.34")
        self.assertEqual(money(Decimal("12.50")*Decimal("0.1")),"1.25")
        for value in (1.2,"NaN","1e9","-1","1.0000001"):
            with self.assertRaises(ValueError):decimal(value)

    def test_real_ubl_namespace_import_matches_json_invoice(self):
        xml=(ROOT/"invoice_contract/examples/invoice.xml").read_bytes()
        self.assertEqual(parse_invoice(xml),example()["invoice"])

    def test_xml_entities_and_unsupported_pricing_are_rejected(self):
        with self.assertRaises(ValueError):parse_invoice(b'<!DOCTYPE x [<!ENTITY x "bad">]><x/>')
        xml=(ROOT/"invoice_contract/examples/invoice.xml").read_bytes().replace(b'>1</cbc:BaseQuantity>',b'>2</cbc:BaseQuantity>')
        with self.assertRaisesRegex(ValueError,"unsupported_base_quantity"):parse_invoice(xml)


if __name__=="__main__":unittest.main()
