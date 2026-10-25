import json
import unittest
from test_casework import CaseFixture
import workspace as ws
from casefiles import invoice_xml

UBL = 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2'
CBC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'
CAC = 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2'


class InvoiceXMLTests(CaseFixture):
    def xml(self, extra=""):
        return f'''<Invoice xmlns="{UBL}" xmlns:b="{CBC}" xmlns:a="{CAC}">
<b:ID>SYN-1</b:ID><b:IssueDate>2026-10-01</b:IssueDate><b:DueDate>2026-10-31</b:DueDate>
<b:DocumentCurrencyCode>EUR</b:DocumentCurrencyCode><b:InvoiceTypeCode>380</b:InvoiceTypeCode>
<a:TaxTotal><b:TaxAmount currencyID="EUR">19.00</b:TaxAmount></a:TaxTotal>
<a:LegalMonetaryTotal><b:TaxExclusiveAmount currencyID="EUR">100.00</b:TaxExclusiveAmount>
<b:TaxInclusiveAmount currencyID="EUR">119.00</b:TaxInclusiveAmount><b:PayableAmount currencyID="EUR">69.00</b:PayableAmount></a:LegalMonetaryTotal>{extra}</Invoice>'''.encode()

    def test_ubl_exact_paths_preserve_gross_due_dates_and_validation_boundaries(self):
        received = self.receive("invoice.xml", self.xml())
        result = invoice_xml.inspect(self.root, received["document_id"])
        report = json.loads((self.root / result["path"]).read_text())
        self.assertEqual(report["fields"]["gross"]["value"], "119.00")
        self.assertEqual(report["fields"]["amount_due"]["value"], "69.00")
        self.assertEqual(report["fields"]["due_date"]["value"], "2026-10-31")
        self.assertEqual(report["schema_validation"], "not_performed")
        self.assertEqual(report["business_rule_validation"], "not_performed")
        self.assertEqual(report["fields"]["net"]["status"], "extracted")

    def test_duplicate_header_candidates_and_unnamespaced_lookalikes_remain_unresolved(self):
        received = self.receive("duplicate.xml", self.xml('<b:ID>SYN-2</b:ID>'))
        report = invoice_xml.inspect(self.root, received["document_id"])
        parsed = json.loads((self.root / report["path"]).read_text())
        self.assertIsNone(parsed["fields"]["invoice_number"]["value"])
        self.assertIn("multiple_candidates:invoice_number", parsed["issues"])
        lookalike = self.receive("plain.xml", b"<Invoice><ID>FAKE</ID></Invoice>")
        result = invoice_xml.inspect(self.root, lookalike["document_id"])
        self.assertEqual(result["syntax"], "unsupported")

    def test_dtd_entities_and_utf16_are_rejected_without_network_or_expansion(self):
        for data in (b'<!DOCTYPE Invoice [<!ENTITY x SYSTEM "file:///private/secret">]><Invoice>&x;</Invoice>',
                     '<Invoice/>'.encode('utf-16')):
            received = self.receive("unsafe.xml", data)
            with self.assertRaises(ws.WorkspaceError):
                invoice_xml.inspect(self.root, received["document_id"])

    def test_pdf_does_not_claim_absence_of_embedded_xml(self):
        received = self.receive("hybrid.pdf", b"%PDF synthetic placeholder only")
        result = invoice_xml.inspect(self.root, received["document_id"])
        self.assertEqual(result["syntax"], "requires_pdf_extractor")

    def test_cii_tax_currency_and_date_are_not_inferred_from_other_totals(self):
        xml = b'''<r:CrossIndustryInvoice xmlns:r="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" xmlns:a="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100" xmlns:u="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">
<r:ExchangedDocument><a:ID>SYN-CII</a:ID><a:IssueDateTime><u:DateTimeString format="102">20261001</u:DateTimeString></a:IssueDateTime></r:ExchangedDocument>
<r:SupplyChainTradeTransaction><a:ApplicableHeaderTradeSettlement><a:InvoiceCurrencyCode>EUR</a:InvoiceCurrencyCode>
<a:SpecifiedTradeSettlementHeaderMonetarySummation><a:TaxBasisTotalAmount>100.00</a:TaxBasisTotalAmount><a:TaxTotalAmount currencyID="EUR">19.00</a:TaxTotalAmount><a:TaxTotalAmount currencyID="USD">21.00</a:TaxTotalAmount><a:GrandTotalAmount>119.00</a:GrandTotalAmount><a:DuePayableAmount>119.00</a:DuePayableAmount></a:SpecifiedTradeSettlementHeaderMonetarySummation>
</a:ApplicableHeaderTradeSettlement></r:SupplyChainTradeTransaction></r:CrossIndustryInvoice>'''
        received = self.receive("cii.xml", xml)
        result = invoice_xml.inspect(self.root, received["document_id"])
        report = json.loads((self.root / result["path"]).read_text())
        self.assertEqual(report["fields"]["tax"]["value"], "19.00")
        self.assertEqual(report["fields"]["invoice_date"]["value"], "2026-10-01")


if __name__ == "__main__":
    unittest.main()
