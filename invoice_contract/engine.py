from copy import deepcopy
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import json
import re


def decimal(value, positive=False):
    if not isinstance(value,str) or not re.fullmatch(r"\d{1,9}(?:\.\d{1,6})?",value):
        raise ValueError("invalid_decimal")
    number=Decimal(value)
    if positive and number<=0:raise ValueError("invalid_positive_decimal")
    return number


def money(value):return format(value.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP),".2f")


def identity(value):
    return isinstance(value,dict) and set(value)=={"scheme","value"} and all(isinstance(v,str) and bool(v) for v in value.values())


def validate(case):
    if not isinstance(case,dict) or not isinstance(case.get("order"),dict) or not isinstance(case.get("invoice"),dict):raise ValueError("invalid_case")
    for kind in ("order","invoice"):
        document=case[kind]
        if not isinstance(document.get("id"),str) or not document["id"] or not re.fullmatch("[A-Z]{3}",document.get("currency","")) or not identity(document.get("buyer")) or not identity(document.get("seller")):raise ValueError("invalid_document")
        lines=document.get("lines")
        if not isinstance(lines,list) or not 1<=len(lines)<=100 or any(not isinstance(l,dict) for l in lines):raise ValueError("invalid_lines")
        ids=[l.get("id") for l in lines]
        if any(not isinstance(k,str) or not k for k in ids) or len(set(ids))!=len(ids):raise ValueError("invalid_line_ids")
        for line in lines:
            if not isinstance(line.get("sku"),str) or not line["sku"] or not isinstance(line.get("unit"),str) or not line["unit"]:raise ValueError("invalid_item")
            decimal(line.get("quantity"),True);decimal(line.get("unit_price"))
            if kind=="order":
                if line.get("billing_basis") not in ("received","ordered"):raise ValueError("invalid_billing_basis")
                decimal(line.get("previous_billed_quantity"))
            else:
                decimal(line.get("line_total"))
                if line.get("order_line_id") is not None and not isinstance(line["order_line_id"],str):raise ValueError("invalid_order_line_reference")
    decimal(case["invoice"].get("line_subtotal"))
    if not isinstance(case["invoice"].get("order_ref"),str):raise ValueError("invalid_order_reference")
    receipts=case.get("receipts",[])
    if not isinstance(receipts,list) or len(receipts)>200:raise ValueError("invalid_receipts")
    for receipt in receipts:
        if not isinstance(receipt,dict) or any(not isinstance(receipt.get(k),str) or not receipt[k] for k in ("id","order_line_id","unit")) or receipt.get("status") not in ("accepted","rejected"):raise ValueError("invalid_receipt")
        decimal(receipt.get("quantity"))
    seen=case.get("seen_invoices",[])
    if not isinstance(seen,list) or len(seen)>1000 or any(not isinstance(s,dict) or not isinstance(s.get("id"),str) or not identity(s.get("seller")) for s in seen):raise ValueError("invalid_history")


def digest(case):return hashlib.sha256(json.dumps(case,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()


def audit(case):
    validate(case)
    order,invoice=case["order"],case["invoice"]
    findings=[]
    def add(code,line=None,expected=None,actual=None,sources=None,severity="block"):
        findings.append({"code":code,"line":line,"expected":expected,"actual":actual,"sources":sources or [order["id"],invoice["id"]],"severity":severity})
    for key in ("buyer","seller","currency"):
        if order[key]!=invoice[key]:add(key+"_mismatch",expected=order[key],actual=invoice[key])
    if invoice["order_ref"]!=order["id"]:add("order_reference_mismatch",expected=order["id"],actual=invoice["order_ref"])
    if any(s["id"]==invoice["id"] and s["seller"]==invoice["seller"] for s in case.get("seen_invoices",[])):add("invoice_seen_before")
    receipts={}
    for receipt in case.get("receipts",[]):
        if receipt["id"] in receipts:
            if receipts[receipt["id"]]!=receipt:add("conflicting_receipt_evidence",sources=[receipt["id"]])
        else:receipts[receipt["id"]]=receipt
    order_lines={l["id"]:l for l in order["lines"]}
    for receipt in receipts.values():
        if receipt["order_line_id"] not in order_lines:add("unmapped_receipt",sources=[receipt["id"]])
    grouped={}
    details=[]
    for line in invoice["lines"]:
        source=[invoice["id"]+":"+line["id"]]
        ordered=order_lines.get(line.get("order_line_id"))
        if ordered is None:
            candidates=[l["id"] for l in order["lines"] if l["sku"]==line["sku"]]
            add("order_line_unresolved",line["id"],expected=candidates,actual=line.get("order_line_id"),sources=source,severity="review")
            details.append({"line":line["id"],"permitted_quantity":None,"repairable":False})
            continue
        source.append(order["id"]+":"+ordered["id"])
        if line["sku"]!=ordered["sku"]:add("item_mismatch",line["id"],ordered["sku"],line["sku"],source)
        if line["unit"]!=ordered["unit"]:add("unit_mismatch",line["id"],ordered["unit"],line["unit"],source)
        quantity=decimal(line["quantity"])
        grouped.setdefault(ordered["id"],[]).append(line)
        if decimal(line["unit_price"])!=decimal(ordered["unit_price"]):add("price_mismatch",line["id"],ordered["unit_price"],line["unit_price"],source)
        expected_total=money(quantity*decimal(line["unit_price"]))
        if decimal(line["line_total"])!=Decimal(expected_total):add("line_total_mismatch",line["id"],expected_total,line["line_total"],source)
        relevant=[r for r in receipts.values() if r["order_line_id"]==ordered["id"] and r["status"]=="accepted"]
        prior=decimal(ordered["previous_billed_quantity"])
        available=decimal(ordered["quantity"])-prior
        unknown=False
        if available<0:add("prior_billing_exceeds_order",line["id"],ordered["quantity"],ordered["previous_billed_quantity"],source)
        if ordered["billing_basis"]=="received":
            if not relevant:
                add("missing_receipt_evidence",line["id"],sources=source,severity="review");unknown=True
            elif any(r["unit"]!=ordered["unit"] for r in relevant):
                add("receipt_unit_mismatch",line["id"],sources=source+[r["id"] for r in relevant]);unknown=True
            else:
                available=min(available,sum((decimal(r["quantity"]) for r in relevant),Decimal(0))-prior)
                source += [r["id"] for r in relevant]
        details.append({"line":line["id"],"order_line":ordered["id"],"permitted_quantity":None if unknown else str(max(Decimal(0),available)),
                        "agreed_unit_price":ordered["unit_price"],"sources":source,
                        "repairable":not unknown and line["sku"]==ordered["sku"] and line["unit"]==ordered["unit"]})
    for key,lines in grouped.items():
        detail=next(d for d in details if d.get("order_line")==key)
        permitted=detail["permitted_quantity"]
        billed=sum((decimal(l["quantity"]) for l in lines),Decimal(0))
        if permitted is not None and billed>Decimal(permitted):
            add("quantity_exceeds_contract",lines[0]["id"],permitted,str(billed),detail["sources"])
        if len(lines)>1:add("split_order_line_requires_review",lines[0]["id"],sources=detail["sources"],severity="review")
    expected_subtotal=money(sum((decimal(l["line_total"]) for l in invoice["lines"]),Decimal(0)))
    if decimal(invoice["line_subtotal"])!=Decimal(expected_subtotal):add("subtotal_mismatch",expected=expected_subtotal,actual=invoice["line_subtotal"])
    state="blocked" if any(f["severity"]=="block" for f in findings) else "review" if findings else "ready_for_review"
    return {"status":state,"snapshot_sha256":digest(case),"findings":findings,"lines":details,
            "rounding":"line_level_decimal_HALF_UP_2_places","scope":"buyer_supplied_acceptance_contract_only",
            "official_status_changed":False,"payment_authorized":False}


def prepare(case):
    initial=audit(case)
    draft=deepcopy(case)
    changes=[]
    codes={f["code"] for f in initial["findings"]}
    global_blocks={"buyer_mismatch","seller_mismatch","currency_mismatch","order_reference_mismatch","invoice_seen_before","conflicting_receipt_evidence","unmapped_receipt"}
    if codes&global_blocks:
        return {"status":"needs_context_review","snapshot_sha256":initial["snapshot_sha256"],"changes":[],"draft":None,"audit":initial,"external_actions":[]}
    for line in draft["invoice"]["lines"]:
        detail=next(d for d in initial["lines"] if d["line"]==line["id"])
        if not detail["repairable"] or "split_order_line_requires_review" in {f["code"] for f in initial["findings"] if f["line"]==line["id"]}:
            continue
        permitted=Decimal(detail["permitted_quantity"])
        if permitted<=0:continue
        for field,value in (("quantity",str(min(decimal(line["quantity"]),permitted))),("unit_price",detail["agreed_unit_price"])):
            if decimal(line[field])!=decimal(value):
                changes.append({"line":line["id"],"field":field,"before":line[field],"after":value,"sources":detail["sources"]})
                line[field]=value
        line["line_total"]=money(decimal(line["quantity"])*decimal(line["unit_price"]))
    draft["invoice"]["line_subtotal"]=money(sum((decimal(l["line_total"]) for l in draft["invoice"]["lines"]),Decimal(0)))
    after=audit(draft)
    return {"status":"draft_ready_for_review" if after["status"]=="ready_for_review" else "needs_evidence_or_human_edit",
            "snapshot_sha256":initial["snapshot_sha256"],"changes":changes,"draft":draft,
            "before_line_subtotal":case["invoice"]["line_subtotal"],"after_line_subtotal":draft["invoice"]["line_subtotal"],
            "audit":after,"external_actions":[],"approval_or_execution_performed":False}
