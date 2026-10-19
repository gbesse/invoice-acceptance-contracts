"""Deliberately narrow UBL line import, not schema or Peppol conformance validation."""
import xml.etree.ElementTree as ET

from .engine import decimal

NS={"cac":"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    "cbc":"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"}


def parse_invoice(data):
    if not isinstance(data,bytes) or len(data)>100000 or b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():raise ValueError("invalid_xml")
    try:root=ET.fromstring(data)
    except ET.ParseError:raise ValueError("invalid_xml") from None
    if root.tag!="{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice":raise ValueError("invalid_ubl_invoice")
    if root.findall(".//cac:AllowanceCharge",NS):raise ValueError("invalid_unsupported_allowance_charge")
    def text(element,path,required=True):
        found=element.find(path,NS)
        value=found.text.strip() if found is not None and found.text else None
        if required and not value:raise ValueError("invalid_missing_ubl_field")
        return value
    def party(path):
        found=root.find(path+"/cac:Party/cac:PartyIdentification/cbc:ID",NS)
        if found is None or not found.text or not found.attrib.get("schemeID"):raise ValueError("invalid_missing_ubl_identifier")
        return {"scheme":found.attrib["schemeID"],"value":found.text.strip()}
    currency=text(root,"cbc:DocumentCurrencyCode")
    for monetary in root.findall(".//cbc:LineExtensionAmount",NS)+root.findall(".//cbc:PriceAmount",NS):
        if monetary.attrib.get("currencyID")!=currency:raise ValueError("invalid_mixed_ubl_currency")
    lines=[]
    for line in root.findall("cac:InvoiceLine",NS):
        quantity=line.find("cbc:InvoicedQuantity",NS)
        if quantity is None or not quantity.attrib.get("unitCode"):raise ValueError("invalid_missing_unit")
        base=text(line,"cac:Price/cbc:BaseQuantity",False)
        if base is not None and decimal(base)!=1:raise ValueError("invalid_unsupported_base_quantity")
        base_node=line.find("cac:Price/cbc:BaseQuantity",NS)
        if base_node is not None and base_node.attrib.get("unitCode")!=quantity.attrib["unitCode"]:raise ValueError("invalid_base_unit")
        for monetary in line.findall("cbc:LineExtensionAmount",NS)+line.findall("cac:Price/cbc:PriceAmount",NS):
            if monetary.attrib.get("currencyID")!=currency:raise ValueError("invalid_mixed_ubl_currency")
        lines.append({"id":text(line,"cbc:ID"),"order_line_id":text(line,"cac:OrderLineReference/cbc:LineID",False),
                      "sku":text(line,"cac:Item/cac:SellersItemIdentification/cbc:ID"),"unit":quantity.attrib["unitCode"],
                      "quantity":text(line,"cbc:InvoicedQuantity"),"unit_price":text(line,"cac:Price/cbc:PriceAmount"),
                      "line_total":text(line,"cbc:LineExtensionAmount")})
    if not 1<=len(lines)<=100:raise ValueError("invalid_ubl_line_count")
    return {"id":text(root,"cbc:ID"),"order_ref":text(root,"cac:OrderReference/cbc:ID"),"currency":currency,
            "buyer":party("cac:AccountingCustomerParty"),"seller":party("cac:AccountingSupplierParty"),
            "lines":lines,"line_subtotal":text(root,"cac:LegalMonetaryTotal/cbc:LineExtensionAmount")}
