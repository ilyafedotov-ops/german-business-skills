"""Explicit receipt comparison, not a payment allocation or collection action."""
import json
from unittest.mock import patch
import test_invoicing as fixtures
from test_casework import CaseFixture
from casefiles import invoicing as inv
from casefiles import invoice_payments as pay
import workspace as ws


class InvoicePaymentTests(CaseFixture):
    write = fixtures.InvoicingTests.write
    create = fixtures.InvoicingTests.create
    action = fixtures.InvoicingTests.action
    begin_issue = fixtures.InvoicingTests.begin_issue
    issued = fixtures.InvoicingTests.issued

    def setUp(self):
        super().setUp()
        self.draft_file = self.write("draft.md", "Synthetic invoice preview")
        self.final_file = self.write("issued.xml", "<SyntheticInvoice>119 EUR</SyntheticInvoice>")
        self.proof = self.write("review.md", "Synthetic reviewed statement allocation and original amount due")
        self.issued()
        self.bank = self.write("bank.csv", "transaction_id,booking_date,amount,currency\npre,2026-09-01,30,EUR\np1,2026-10-01,60,EUR\np2,2026-11-01,29,EUR\nrefund,2026-11-02,-10,EUR\nfx,2026-11-03,29,USD\n")
        self.request = pay.template()
        self.request.update(invoice_id="invoice-1", as_of="2026-11-30", amount_due="89.00",
                            bank_account="synthetic-bank", bank_file=self.bank, review_file=self.proof,
                            coverage_confirmed=True, reviewer="synthetic reviewer")

    def item(self, transaction, amount, treatment="later_receipt"):
        return dict(transaction_id=transaction, amount=amount, treatment=treatment, evidence_file=self.proof)

    def prepare(self, language="en"):
        request = self.write("payment-input.json", json.dumps(self.request))
        return pay.prepare(self.root, request, inv.show(self.root, "invoice-1")["sha256"], language)

    def test_prepaid_not_subtracted_twice_and_cross_period_partial_refund(self):
        self.request["payments"] = [self.item("pre", "30", "included_prepaid"), self.item("p1", "60")]
        first = self.prepare()
        self.assertEqual(first["comparison_remaining"], "29.00")
        self.request["payments"] += [self.item("p2", "29"), self.item("refund", "-10", "later_refund")]
        second = self.prepare()
        self.assertEqual(second["comparison_remaining"], "10.00")
        self.assertNotEqual(first["path"], second["path"])
        self.assertEqual(pay.check(self.root, first["path"])["current"], False)
        self.assertEqual(inv.show(self.root, "invoice-1")["record"]["delivery"]["state"], "not_prepared")

    def test_zero_and_equal_amount_do_not_mark_invoice_paid(self):
        before = inv.show(self.root, "invoice-1")["sha256"]
        self.request["amount_due"] = "0.00"
        report = self.prepare()
        self.assertEqual(report["status"], "zero_difference")
        self.assertEqual(report["comparison_remaining"], "0.00")
        self.assertEqual(inv.show(self.root, "invoice-1")["sha256"], before)
        text = ws._inside(self.root, report["markdown_path"]).read_text()
        self.assertIn("No payment allocation", text)

    def test_ambiguous_currency_future_and_incomplete_coverage_remain_open(self):
        for item in [self.item("fx", "29"), self.item("p1", "60", "uncertain"), self.item("p2", "29")]:
            with self.subTest(item=item):
                self.request["as_of"] = "2026-10-31"
                self.request["payments"] = [item]
                report = self.prepare()
                self.assertEqual(report["status"], "needs_review")
                self.assertIsNone(report["comparison_remaining"])
        self.request["payments"] = []
        self.request["coverage_confirmed"] = False
        self.assertIsNone(self.prepare()["comparison_remaining"])

    def test_reject_duplicate_unknown_oversized_and_wrong_sign_allocations(self):
        for rows in [[self.item("p1", "60")]*2, [self.item("missing", "1")],
                     [self.item("p1", "61")], [self.item("refund", "10")],
                     [self.item("p1", "-10", "later_refund")]]:
            with self.subTest(rows=rows), self.assertRaises(ws.WorkspaceError):
                self.request["payments"] = rows
                self.prepare()

    def test_correction_invalidates_prior_report_and_blocks_new_balance(self):
        first = self.prepare()
        self.assertTrue(pay.check(self.root, first["path"])["current"])
        self.create("correction", business_reference="corr", corrects="invoice-1", correction_kind="amount_credit")
        self.assertFalse(pay.check(self.root, first["path"])["current"])
        second = self.prepare()
        self.assertIsNone(second["comparison_remaining"])
        self.assertIn("correction_review_required", second["issues"])

    def test_frozen_evidence_corruption_and_stale_hash_fail_closed(self):
        path = self.write("payment-input.json", json.dumps(self.request))
        with self.assertRaises(ws.WorkspaceError):
            pay.prepare(self.root, path, "0"*64)
        report = self.prepare()
        saved = json.loads(ws._inside(self.root, report["path"]).read_text())
        ws._inside(self.root, saved["sources"][0]["path"]).write_text("tampered")
        with self.assertRaises(ws.WorkspaceError):
            pay.check(self.root, report["path"])

    def test_both_reports_are_readable_and_tampering_is_rejected(self):
        for language, phrase in [("en", "Payment comparison"), ("ru", "Сверка оплаты")]:
            report = self.prepare(language)
            self.assertIn(phrase, ws._inside(self.root, report["markdown_path"]).read_text())
            self.assertTrue(pay.check(self.root, report["path"])["current"])
        p = ws._inside(self.root, report["path"])
        data = json.loads(p.read_text()); data["comparison_remaining"] = "0"
        p.write_text(json.dumps(data))
        with self.assertRaises(ws.WorkspaceError):
            pay.check(self.root, report["path"])

    def test_cli_prepares_checks_and_preserves_original_invoice(self):
        from synthetic_journey import command
        self.assertEqual(command("desk.py", "invoice-payment-template")["payments"], [])
        self.request["payments"] = [self.item("p1", "60"), self.item("p2", "29")]
        path = self.write("payment-input.json", json.dumps(self.request))
        before = inv.show(self.root, "invoice-1")["sha256"]
        result = command("desk.py", "invoice-payment-prepare", "--root", self.root,
                         "--input", path, "--expected-sha256", before, "--language", "ru")
        self.assertEqual(result["status"], "zero_difference")
        checked = command("desk.py", "invoice-payment-check", "--root", self.root, "--report", result["path"])
        self.assertTrue(checked["current"])
        self.assertEqual(inv.show(self.root, "invoice-1")["sha256"], before)

    def test_partial_bank_amount_overpayment_and_unsafe_sources(self):
        self.request["amount_due"] = "19"
        self.request["payments"] = [self.item("p1", "20")]
        self.assertEqual(self.prepare()["comparison_remaining"], "-1")
        for path in ["../outside.csv", inv.STATE]:
            self.request["bank_file"] = path
            with self.assertRaises(ws.WorkspaceError):
                self.prepare()

    def test_malformed_rows_and_treatments_fail_with_domain_error(self):
        self.request["payments"] = [self.item("p1", "60", [])]
        with self.assertRaises(ws.WorkspaceError):
            self.prepare()
        self.request["payments"] = []
        ws._inside(self.root, self.bank).write_text("transaction_id,booking_date,amount,currency\nx\n")
        with self.assertRaises(ws.WorkspaceError):
            self.prepare()

    def test_repeated_source_capture_cannot_replace_parsed_bank_fingerprint(self):
        self.request["payments"] = [self.item("p1", "60")]
        self.request["payments"][0]["evidence_file"] = self.bank
        original = pay.st.evidence
        seen = 0
        def changing_capture(root, path):
            nonlocal seen
            if path == self.bank:
                seen += 1
                if seen == 2:
                    bank = ws._inside(self.root, self.bank)
                    bank.write_text(bank.read_text().replace(",60,EUR", ",6,EUR"))
            return original(root, path)
        with patch.object(pay.st, "evidence", side_effect=changing_capture), self.assertRaises(ws.WorkspaceError):
            self.prepare()

    def test_as_of_before_issue_has_no_balance_and_localized_explanation(self):
        self.request["as_of"] = "2026-01-01"
        report = self.prepare("ru")
        self.assertIsNone(report["comparison_remaining"])
        self.assertIn("before_issue", report["issues"])
        text = ws._inside(self.root, report["markdown_path"]).read_text()
        self.assertIn("раньше", text)
        self.assertNotIn("before_issue", text)
