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

    def credit_note(self, references="", totals="119.00"):
        return f'''<CreditNote xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2" xmlns:b="{CBC}" xmlns:a="{CAC}">
<b:ID>CN-1</b:ID><b:IssueDate>2026-10-21</b:IssueDate><b:CreditNoteTypeCode>381</b:CreditNoteTypeCode>
<b:DocumentCurrencyCode>EUR</b:DocumentCurrencyCode>
<a:PaymentMeans><b:PaymentDueDate>2026-11-01</b:PaymentDueDate></a:PaymentMeans>
<a:TaxTotal><b:TaxAmount currencyID="EUR">19.00</b:TaxAmount></a:TaxTotal>
<a:LegalMonetaryTotal><b:TaxExclusiveAmount currencyID="EUR">100.00</b:TaxExclusiveAmount>
<b:TaxInclusiveAmount currencyID="EUR">{totals}</b:TaxInclusiveAmount><b:PayableAmount currencyID="EUR">69.00</b:PayableAmount></a:LegalMonetaryTotal>{references}</CreditNote>'''.encode()

    def inspect_report(self, name, payload):
        received = self.receive(name, payload)
        result = invoice_xml.inspect(self.root, received["document_id"])
        return received, json.loads((self.root / result["path"]).read_text())

    def test_credit_note_reads_header_and_preceding_invoice_without_mutating_catalog(self):
        refs = '<a:BillingReference><a:InvoiceDocumentReference><b:ID>SYN-1</b:ID><b:IssueDate>2026-10-01</b:IssueDate></a:InvoiceDocumentReference></a:BillingReference>'
        received, report = self.inspect_report("credit.xml", self.credit_note(refs))
        self.assertEqual(report["syntax"], "ubl_credit_note")
        self.assertEqual(report["document_type_candidates"], ["381"])
        self.assertEqual(report["fields"]["gross"]["value"], "119.00")
        self.assertEqual(report["fields"]["amount_due"]["value"], "69.00")
        self.assertEqual(report["fields"]["due_date"]["value"], "2026-11-01")
        reference = report["preceding_invoices"][0]
        self.assertEqual(reference["invoice_number"]["value"], "SYN-1")
        self.assertEqual(reference["issue_date"]["value"], "2026-10-01")
        self.assertIn("BillingReference[1]", reference["invoice_number"]["location"])
        self.assertEqual(reference["invoice_number"]["status"], "extracted")
        from casefiles import documents
        catalog = documents.get(self.root, received["document_id"])
        self.assertEqual(catalog["type"], "invoice")  # Supplied intake type is not reclassified.
        self.assertEqual(catalog["relations"], [])
        self.assertIsNone(catalog["dates"]["paid"])
        self.assertEqual(report["tax_review"], "not_performed")
        self.assertEqual(report["schema_validation"], "not_performed")

    def test_credit_note_preserves_negative_sign_and_rejects_wrong_currency(self):
        _, report = self.inspect_report("negative.xml", self.credit_note(totals="-119.00"))
        self.assertEqual(report["fields"]["gross"]["value"], "-119.00")
        payload = self.credit_note().replace(b'<b:TaxInclusiveAmount currencyID="EUR">', b'<b:TaxInclusiveAmount currencyID="USD">')
        _, report = self.inspect_report("currency.xml", payload)
        self.assertIsNone(report["fields"]["gross"]["value"])
        self.assertIn("invalid_or_unsupported:gross", report["issues"])

    def test_credit_note_does_not_borrow_invoice_root_due_date_or_choose_ambiguous_payment_date(self):
        raw = self.credit_note().replace(b'<a:PaymentMeans><b:PaymentDueDate>2026-11-01</b:PaymentDueDate></a:PaymentMeans>', b'<b:DueDate>2026-12-01</b:DueDate>')
        _, report = self.inspect_report("wrong-date-path.xml", raw)
        self.assertIsNone(report["fields"]["due_date"]["value"])
        raw = self.credit_note().replace(b'</CreditNote>', b'<a:PaymentMeans><b:PaymentDueDate>2026-11-02</b:PaymentDueDate></a:PaymentMeans></CreditNote>')
        _, report = self.inspect_report("ambiguous-due.xml", raw)
        self.assertIsNone(report["fields"]["due_date"]["value"])
        self.assertIn("multiple_candidates:due_date", report["issues"])

    def test_invoice_references_keep_groups_optional_dates_and_ambiguity(self):
        refs = '''<a:BillingReference><a:InvoiceDocumentReference><b:ID>OLD-1</b:ID></a:InvoiceDocumentReference></a:BillingReference>
<a:BillingReference><a:InvoiceDocumentReference><b:ID>OLD-2</b:ID><b:ID>OTHER</b:ID><b:IssueDate>2026-02-30</b:IssueDate></a:InvoiceDocumentReference></a:BillingReference>
<a:BillingReference><a:InvoiceDocumentReference><b:ID><b:Note>nested</b:Note></b:ID></a:InvoiceDocumentReference></a:BillingReference>
<a:BillingReference><a:CreditNoteDocumentReference><b:ID>NOT-AN-INVOICE-REFERENCE</b:ID></a:CreditNoteDocumentReference></a:BillingReference>
<a:InvoiceLine><a:BillingReference><a:InvoiceDocumentReference><b:ID>LINE-ONLY</b:ID></a:InvoiceDocumentReference></a:BillingReference></a:InvoiceLine>'''
        _, report = self.inspect_report("references.xml", self.xml(refs))
        groups = report["preceding_invoices"]
        self.assertEqual(len(groups), 4)
        self.assertEqual(groups[0]["invoice_number"]["value"], "OLD-1")
        self.assertIsNone(groups[0]["issue_date"]["value"])
        self.assertEqual(groups[0]["issue_date"]["note"], "optional_missing")
        self.assertIsNone(groups[1]["invoice_number"]["value"])
        self.assertIsNone(groups[1]["issue_date"]["value"])
        self.assertIsNone(groups[2]["invoice_number"]["value"])
        self.assertIsNone(groups[3]["invoice_number"]["value"])
        self.assertTrue(any("preceding_invoices[2].invoice_number" in issue for issue in report["issues"]))

    def test_malformed_reference_children_cannot_combine_unrelated_id_and_date(self):
        refs = '<a:BillingReference><a:InvoiceDocumentReference><b:ID>OLD-A</b:ID></a:InvoiceDocumentReference><a:InvoiceDocumentReference><b:IssueDate>2026-09-01</b:IssueDate></a:InvoiceDocumentReference></a:BillingReference>'
        _, report = self.inspect_report("split-reference.xml", self.xml(refs))
        reference = report["preceding_invoices"][0]
        self.assertIsNone(reference["invoice_number"]["value"])
        self.assertIsNone(reference["issue_date"]["value"])
        self.assertIn("multiple_candidates:preceding_invoices[1].invoice_number", report["issues"])
        self.assertIn("multiple_candidates:preceding_invoices[1].issue_date", report["issues"])

    def test_cii_preceding_invoices_use_header_issuer_id_and_formatted_date(self):
        payload = b'''<r:CrossIndustryInvoice xmlns:r="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" xmlns:a="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100" xmlns:q="urn:un:unece:uncefact:data:standard:QualifiedDataType:100" xmlns:u="urn:un:unece:uncefact:data:standard:UnqualifiedDataType:100">
<r:SupplyChainTradeTransaction><a:ApplicableHeaderTradeSettlement>
<a:InvoiceReferencedDocument><a:IssuerAssignedID>OLD-CII</a:IssuerAssignedID><a:FormattedIssueDateTime><q:DateTimeString format="102">20260915</q:DateTimeString></a:FormattedIssueDateTime></a:InvoiceReferencedDocument>
<a:InvoiceReferencedDocument><a:IssuerAssignedID>OLD-CII-2</a:IssuerAssignedID><a:FormattedIssueDateTime><q:DateTimeString format="203">202609151200</q:DateTimeString></a:FormattedIssueDateTime></a:InvoiceReferencedDocument>
<a:InvoiceReferencedDocument><a:IssuerAssignedID>WRONG-DATE-NAMESPACE</a:IssuerAssignedID><a:FormattedIssueDateTime><u:DateTimeString format="102">20260915</u:DateTimeString></a:FormattedIssueDateTime></a:InvoiceReferencedDocument>
</a:ApplicableHeaderTradeSettlement></r:SupplyChainTradeTransaction></r:CrossIndustryInvoice>'''
        _, report = self.inspect_report("cii-reference.xml", payload)
        self.assertEqual(report["preceding_invoices"][0]["invoice_number"]["value"], "OLD-CII")
        self.assertEqual(report["preceding_invoices"][0]["issue_date"]["value"], "2026-09-15")
        self.assertIsNone(report["preceding_invoices"][1]["issue_date"]["value"])

        self.assertIn("multiple_preceding_invoices_outside_inspected_cii_subset", report["issues"])
        self.assertIsNone(report["preceding_invoices"][2]["issue_date"]["value"])
        self.assertIn("invalid_or_unsupported:preceding_invoices[3].issue_date", report["issues"])

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

    def test_ubl_prepayment_and_rounding_are_source_values_not_new_payments(self):
        from casefiles import documents
        for name, raw in (("invoice", self.xml()), ("credit", self.credit_note())):
            with self.subTest(syntax=name):
                payload = raw.replace(b'</a:LegalMonetaryTotal>', b'<b:PrepaidAmount currencyID="EUR">50.00</b:PrepaidAmount><b:PayableRoundingAmount currencyID="EUR">-0.01</b:PayableRoundingAmount></a:LegalMonetaryTotal>')
                received, report = self.inspect_report(name + "-prepaid.xml", payload)
                self.assertEqual(report["fields"]["prepaid_amount"]["value"], "50.00")
                self.assertEqual(report["fields"]["rounding_amount"]["raw"], "-0.01")
                self.assertEqual(report["fields"]["rounding_amount"]["value"], "-0.01")
                self.assertEqual(report["fields"]["amount_due"]["value"], "69.00")
                self.assertEqual(report["business_rule_validation"], "not_performed")
                self.assertIsNone(documents.get(self.root, received["document_id"])["dates"]["paid"])

    def test_optional_payment_totals_distinguish_absence_zero_and_wrong_location(self):
        _, report = self.inspect_report("missing-totals.xml", self.xml('<b:PrepaidAmount currencyID="EUR">99.00</b:PrepaidAmount><a:InvoiceLine><a:LegalMonetaryTotal><b:PayableRoundingAmount currencyID="EUR">9.00</b:PayableRoundingAmount></a:LegalMonetaryTotal></a:InvoiceLine>'))
        for name in ("prepaid_amount", "rounding_amount"):
            self.assertIsNone(report["fields"][name]["value"])
            self.assertEqual(report["fields"][name]["note"], "optional_missing")
            self.assertNotIn("missing:" + name, report["issues"])
        payload = self.xml().replace(b'</a:LegalMonetaryTotal>', b'<b:PrepaidAmount currencyID="EUR">0.00</b:PrepaidAmount></a:LegalMonetaryTotal>')
        _, report = self.inspect_report("zero-prepaid.xml", payload)
        self.assertEqual(report["fields"]["prepaid_amount"]["value"], "0.00")

    def test_ubl_ambiguous_or_invalid_payment_totals_remain_unresolved(self):
        variants = [
            '<b:PrepaidAmount currencyID="EUR">50.00</b:PrepaidAmount>' * 2,
            '<b:PrepaidAmount currencyID="USD">50.00</b:PrepaidAmount>',
            '<b:PrepaidAmount>50.00</b:PrepaidAmount>',
            '<b:PrepaidAmount currencyID="EUR">1e2</b:PrepaidAmount>',
            '<b:PrepaidAmount currencyID="EUR"></b:PrepaidAmount>',
            '<b:PrepaidAmount currencyID="EUR"><b:Note>50.00</b:Note></b:PrepaidAmount>',
        ]
        for index, fragment in enumerate(variants):
            with self.subTest(fragment=fragment):
                payload = self.xml().replace(b'</a:LegalMonetaryTotal>', fragment.encode() + b'</a:LegalMonetaryTotal>')
                _, report = self.inspect_report(f"invalid-prepaid-{index}.xml", payload)
                self.assertIsNone(report["fields"]["prepaid_amount"]["value"])
                self.assertTrue(any(issue.endswith(":prepaid_amount") for issue in report["issues"]))

    def cii_payment_totals(self, currency="EUR", fragment=""):
        return f'''<r:CrossIndustryInvoice xmlns:r="urn:un:unece:uncefact:data:standard:CrossIndustryInvoice:100" xmlns:a="urn:un:unece:uncefact:data:standard:ReusableAggregateBusinessInformationEntity:100">
<r:SupplyChainTradeTransaction><a:ApplicableHeaderTradeSettlement><a:InvoiceCurrencyCode>{currency}</a:InvoiceCurrencyCode>
<a:SpecifiedTradeSettlementHeaderMonetarySummation>{fragment}</a:SpecifiedTradeSettlementHeaderMonetarySummation>
</a:ApplicableHeaderTradeSettlement></r:SupplyChainTradeTransaction></r:CrossIndustryInvoice>'''.encode()

    def test_cii_payment_totals_preserve_signs_and_optional_currency(self):
        _, report = self.inspect_report("cii-payment.xml", self.cii_payment_totals(fragment='<a:TotalPrepaidAmount>-50.00</a:TotalPrepaidAmount><a:RoundingAmount currencyID="EUR">0.01</a:RoundingAmount>'))
        self.assertEqual(report["fields"]["prepaid_amount"]["value"], "-50.00")
        self.assertEqual(report["fields"]["rounding_amount"]["value"], "0.01")
        self.assertIn("SpecifiedTradeSettlementHeaderMonetarySummation", report["fields"]["prepaid_amount"]["location"])

    def test_cii_payment_totals_require_unambiguous_valid_document_currency(self):
        for index, (currency, fragment) in enumerate([
            ("EUR", '<a:TotalPrepaidAmount currencyID="USD">50.00</a:TotalPrepaidAmount>'),
            ("", '<a:TotalPrepaidAmount>50.00</a:TotalPrepaidAmount>'),
            ("invalid", '<a:TotalPrepaidAmount>50.00</a:TotalPrepaidAmount>'),
            ("EUR</a:InvoiceCurrencyCode><a:InvoiceCurrencyCode>EUR", '<a:TotalPrepaidAmount>50.00</a:TotalPrepaidAmount>'),
            ("EUR", '<a:TotalPrepaidAmount>50.00</a:TotalPrepaidAmount>' * 2),
        ]):
            with self.subTest(currency=currency, fragment=fragment):
                _, report = self.inspect_report(f"cii-invalid-payment-{index}.xml", self.cii_payment_totals(currency, fragment))
                self.assertIsNone(report["fields"]["prepaid_amount"]["value"])
                self.assertTrue(any(issue.endswith(":prepaid_amount") for issue in report["issues"]))

    def test_inspected_payment_totals_survive_draft_proposal_without_payment_inference(self):
        from casefiles import documents, reviews, storage
        payload = self.xml().replace(b'</a:LegalMonetaryTotal>', b'<b:PrepaidAmount currencyID="EUR">50.00</b:PrepaidAmount></a:LegalMonetaryTotal>')
        received, report = self.inspect_report("proposal-prepaid.xml", payload)
        draft = reviews.proposal_template()
        draft.update(proposal_id="payment-review", document_id=received["document_id"], period="2026-10", activity_id="consulting", fields=report["fields"])
        reviews.save_proposal(self.root, draft)
        saved = storage.load(self.root)["proposals"]["payment-review"]
        self.assertEqual(saved["fields"]["prepaid_amount"], report["fields"]["prepaid_amount"])
        self.assertIsNone(saved["fields"]["rounding_amount"]["value"])
        self.assertEqual(saved["review"]["status"], "draft")
        self.assertIsNone(documents.get(self.root, received["document_id"])["dates"]["paid"])


if __name__ == "__main__":
    unittest.main()
