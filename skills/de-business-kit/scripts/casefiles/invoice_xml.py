"""Bounded UTF-8 UBL/CII candidate extraction, never schema/profile validation."""
import re
import sys
import uuid
import xml.etree.ElementTree as ET

import workspace as ws
from . import documents as docs
from . import storage as st

NS = {"ubl": "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
      "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
      "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
      "rsm": "urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100",
      "ram": "urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100",
      "udt": "urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100"}
SETTLEMENT = "rsm:SupplyChainTradeTransaction/ram:ApplicableHeaderTradeSettlement/"
TOTAL = SETTLEMENT + "ram:SpecifiedTradeSettlementHeaderMonetarySummation/"
AGREEMENT = "rsm:SupplyChainTradeTransaction/ram:ApplicableHeaderTradeAgreement/"
PATHS = {
    "ubl_invoice": {"invoice_number": "cbc:ID", "invoice_date": "cbc:IssueDate", "due_date": "cbc:DueDate",
                    "currency": "cbc:DocumentCurrencyCode", "supplier_reference": "cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName",
                    "customer_reference": "cac:AccountingCustomerParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName",
                    "net": "cac:LegalMonetaryTotal/cbc:TaxExclusiveAmount", "tax": "cac:TaxTotal/cbc:TaxAmount",
                    "gross": "cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount", "amount_due": "cac:LegalMonetaryTotal/cbc:PayableAmount"},
    "cii": {"invoice_number": "rsm:ExchangedDocument/ram:ID", "invoice_date": "rsm:ExchangedDocument/ram:IssueDateTime/udt:DateTimeString",
            "due_date": SETTLEMENT + "ram:SpecifiedTradePaymentTerms/ram:DueDateDateTime/udt:DateTimeString",
            "currency": SETTLEMENT + "ram:InvoiceCurrencyCode", "supplier_reference": AGREEMENT + "ram:SellerTradeParty/ram:Name",
            "customer_reference": AGREEMENT + "ram:BuyerTradeParty/ram:Name", "net": TOTAL + "ram:TaxBasisTotalAmount",
            "tax": TOTAL + "ram:TaxTotalAmount", "gross": TOTAL + "ram:GrandTotalAmount", "amount_due": TOTAL + "ram:DuePayableAmount"}}


def parse(data):
    if len(data) > 5 * 1024 * 1024:
        raise ws.WorkspaceError("XML inspection supports at most 5 MiB; the original remains preserved.")
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ws.WorkspaceError("This inspector supports UTF-8 XML only; preserve other encodings for separate tooling.") from exc
    encoding = re.search(r'<\?xml\b[^>]*encoding\s*=\s*[\'"]([^\'"]+)', text, re.I)
    if "\x00" in text or encoding and encoding.group(1).lower() not in {"utf-8", "utf8", "us-ascii"}:
        raise ws.WorkspaceError("Unsupported XML encoding.")
    if re.search(r"<!\s*(DOCTYPE|ENTITY)\b", text, re.I):
        raise ws.WorkspaceError("DTD/entity declarations are forbidden; no expansion or external lookup performed.")
    parser = ET.XMLPullParser(events=("start", "end"))
    first, depth, nodes = None, 0, 0
    try:
        for start in range(0, len(text), 4096):
            parser.feed(text[start:start + 4096])
            for event, element in parser.read_events():
                if event == "start":
                    if first is None:
                        first = element
                    depth += 1
                    nodes += 1
                    if depth > 128 or nodes > 50000:
                        raise ws.WorkspaceError("XML exceeds inspection depth/node limits.")
                else:
                    depth -= 1
                    if len(element.text or "") > 200000:
                        raise ws.WorkspaceError("XML text node exceeds inspection limit.")
        parser.close()
    except ET.ParseError as exc:
        raise ws.WorkspaceError("XML is not well formed: " + str(exc)) from exc
    return first


def inspect(root, document_id):
    root = ws._workspace(root)
    original = docs.original(root, document_id)
    suffix = ws._inside(root, original["path"]).suffix
    report = {"schema_version": 1, "document_id": document_id,
              "source": {"path": original["path"], "sha256": original["sha256"]},
              "schema_validation": "not_performed", "business_rule_validation": "not_performed",
              "tax_review": "not_performed", "line_and_tax_breakdown": "not_extracted", "status": "needs_review",
              "parser": "Python ElementTree / " + sys.version.split()[0], "namespaces": NS, "fields": {}, "issues": []}
    if suffix != ".xml":
        report["syntax"] = "requires_pdf_extractor" if suffix == ".pdf" else "unsupported"
        report["issues"].append("embedded_xml_not_inspected_no_absence_claim")
    else:
        tree = parse(ws._read_regular(ws._inside(root, original["path"])))
        syntax = {"{" + NS["ubl"] + "}Invoice": "ubl_invoice", "{" + NS["rsm"] + "}CrossIndustryInvoice": "cii"}.get(tree.tag, "unsupported")
        report.update(syntax=syntax, xml_well_formed=True)
        if syntax == "unsupported":
            report["issues"].append("unsupported_namespace_or_root")
        else:
            paths = PATHS[syntax]
            currency_nodes = tree.findall(paths["currency"], NS)
            currency = currency_nodes[0].text.strip() if len(currency_nodes) == 1 and currency_nodes[0].text else None
            for name, path in paths.items():
                nodes = tree.findall(path, NS)
                if name == "tax":
                    nodes = [node for node in nodes if currency and node.get("currencyID") == currency]
                field = {"raw": None, "value": None, "location": path, "status": "unavailable", "reviewer": None, "note": "missing"}
                if len(nodes) != 1:
                    issue = ("multiple_candidates:" if nodes else "missing:") + name
                    report["issues"].append(issue)
                    field["note"] = issue
                else:
                    node = nodes[0]
                    raw = node.text or ""
                    value = raw.strip()
                    field["raw"] = raw or None
                    try:
                        if list(node) or not value or len(value) > 20000:
                            raise ws.WorkspaceError("Unsupported empty, nested or oversized field.")
                        if name in {"net", "tax", "gross", "amount_due"}:
                            ws._amount(value)
                            if node.get("currencyID") not in {None, currency} or syntax == "ubl_invoice" and not node.get("currencyID"):
                                raise ws.WorkspaceError("Amount currency is unresolved.")
                        elif name in {"invoice_date", "due_date"}:
                            if syntax == "cii":
                                if node.get("format") != "102" or not re.fullmatch(r"\d{8}", value):
                                    raise ws.WorkspaceError("Unsupported CII date format.")
                                value = value[:4] + "-" + value[4:6] + "-" + value[6:]
                            ws._day(value)
                        elif name == "currency":
                            ws._currency(value)
                        field.update(value=value, status="extracted", note=None)
                    except ws.WorkspaceError as exc:
                        field["note"] = str(exc)
                        report["issues"].append("invalid_or_unsupported:" + name)
                report["fields"][name] = field
            type_path = "cbc:InvoiceTypeCode" if syntax == "ubl_invoice" else "rsm:ExchangedDocument/ram:TypeCode"
            report["document_type_candidates"] = [node.text for node in tree.findall(type_path, NS)]
    identifier = "inspection-" + uuid.uuid4().hex
    relative = f"06_bookkeeping/{original['period'][:4]}/{original['period'][5:]}/derived/{identifier}.json"
    with st.edit(root, "invoice_xml_inspected", {"document_id": document_id, "inspection_id": identifier}) as state:
        st.check_evidence(root, report["source"])
        ws._mkdir(ws._inside(root, relative).parent)
        ws._atomic_json(ws._inside(root, relative), report)
        state["inspections"][identifier] = {"inspection_id": identifier, "document_id": document_id,
            "syntax": report["syntax"], "report": st.evidence(root, relative), "source": report["source"]}
    return {"inspection_id": identifier, "path": relative, "syntax": report["syntax"], "status": "needs_review"}
