"""Customer-safe drafts stay separate from private reconciliation evidence."""
import json
from test_casework import CaseFixture
import test_invoice_payments as fixtures
from casefiles import invoice_payments as pay, payment_followup as follow
import workspace as ws


class FollowupTests(CaseFixture):
    write = fixtures.InvoicePaymentTests.write
    create = fixtures.InvoicePaymentTests.create
    action = fixtures.InvoicePaymentTests.action
    begin_issue = fixtures.InvoicePaymentTests.begin_issue
    issued = fixtures.InvoicePaymentTests.issued
    item = fixtures.InvoicePaymentTests.item

    def setUp(self):
        super().setUp()
        self.draft_file = self.write("draft.md", "Synthetic draft")
        self.final_file = self.write("invoice.md", "Synthetic INV-1: EUR 89 due after prepayment")
        self.proof = self.write("private-review.md", "PRIVATE-SOURCE-MARKER: reviewed facts and exact customer email")
        self.issued()
        self.bank = self.write("bank.csv", "transaction_id,booking_date,amount,currency\nr1,2026-10-28,60,EUR\n")
        self.payment = pay.template()
        self.payment.update(invoice_id="invoice-1", as_of="2026-10-29", amount_due="89.00",
                            bank_account="PRIVATE-BANK-ACCOUNT", bank_file=self.bank, review_file=self.proof,
                            reviewer="Synthetic reviewer", coverage_confirmed=True,
                            payments=[self.item("r1", "60")])
        self.compare()
        self.request = follow.template()
        self.request.update(comparison_file=self.comparison["path"], mode="balance_query",
                            recipient={"channel":"email", "address":"buyer@example.invalid"},
                            customer_name="Example Customer", sender_name="Example Seller",
                            recipient_language="de", prepared_on="2026-10-30", review_file=self.proof)

    def compare(self):
        path = self.write("comparison-input.json", json.dumps(self.payment))
        self.comparison = pay.prepare(self.root, path, pay.inv.show(self.root, "invoice-1")["sha256"])

    def prepare(self, language="en", expected=None):
        path = self.write("followup-input.json", json.dumps(self.request))
        return follow.prepare(self.root, path, expected or pay.check(self.root, self.comparison["path"])["report_sha256"], language)

    def test_positive_difference_creates_customer_draft_and_separate_private_review(self):
        before = pay.inv.show(self.root, "invoice-1")["sha256"]
        result = self.prepare("ru")
        text = ws._inside(self.root, result["recipient_path"]).read_text()
        self.assertIn("29,00 EUR", text)
        self.assertIn("NUMBER-invoice-1", text)
        for secret in ["PRIVATE-SOURCE-MARKER", "PRIVATE-BANK-ACCOUNT", self.proof, "SHA-256", "invoice-evidence"]:
            self.assertNotIn(secret, text)
        self.assertIn("Не отправлено", ws._inside(self.root, result["review_path"]).read_text())
        self.assertEqual(pay.inv.show(self.root, "invoice-1")["sha256"], before)
        self.assertTrue(follow.check(self.root, result["path"])["current"])

    def test_unresolved_balance_allows_only_amount_free_clarification(self):
        self.payment["coverage_confirmed"] = False
        self.compare(); self.request["comparison_file"] = self.comparison["path"]
        with self.assertRaises(ws.WorkspaceError):
            self.prepare()
        self.request["mode"] = "clarification"
        result = self.prepare()
        text = ws._inside(self.root, result["recipient_path"]).read_text()
        self.assertNotIn("EUR", text)
        self.assertNotIn("29", text)
        self.assertIn("coverage_unconfirmed", follow.check(self.root, result["path"])["comparison_issues"])

    def test_zero_and_negative_comparisons_do_not_generate_payment_query(self):
        for due in ["60", "59"]:
            self.payment["amount_due"] = due; self.compare()
            self.request["comparison_file"] = self.comparison["path"]
            with self.assertRaises(ws.WorkspaceError):
                self.prepare()

    def test_source_change_and_new_correction_stale_prepared_message(self):
        result = self.prepare()
        self.create("corr", business_reference="corr", corrects="invoice-1", correction_kind="amount_credit")
        self.assertFalse(follow.check(self.root, result["path"])["current"])
        with self.assertRaises(ws.WorkspaceError):
            self.prepare()

    def test_changed_recipient_artifact_fails_integrity_and_revisions_preserve_old(self):
        first = self.prepare(); self.request["recipient"]["address"] = "other@example.invalid"
        second = self.prepare()
        self.assertNotEqual(first["path"], second["path"])
        self.assertFalse(follow.check(self.root, first["path"])["current"])
        ws._inside(self.root, second["recipient_path"]).write_text("Edited demand")
        with self.assertRaises(ws.WorkspaceError):
            follow.check(self.root, second["path"])

    def test_stale_expected_hash_and_invalid_recipient_fields_are_rejected(self):
        with self.assertRaises(ws.WorkspaceError):
            self.prepare(expected="0"*64)
        for key,value in [("sender_name","Seller\nBcc: outsider@example.invalid"),
                          ("recipient",{"channel":"email","address":"buyer@example.invalid\nBcc:x"}),
                          ("prepared_on","2026-01-01")]:
            old=self.request[key]; self.request[key]=value
            with self.assertRaises(ws.WorkspaceError):
                self.prepare()
            self.request[key]=old

    def test_recipient_languages_and_cli(self):
        from synthetic_journey import command
        self.assertEqual(command("desk.py", "payment-followup-template")["mode"], None)
        for language, phrase in [("de","Betreff:"),("en","Subject:"),("ru","Тема:")]:
            self.request["recipient_language"] = language
            path = self.write("followup-input.json", json.dumps(self.request))
            result = command("desk.py", "payment-followup-prepare", "--root", self.root,
                             "--input", path, "--expected-sha256", pay.check(self.root, self.comparison["path"])["report_sha256"])
            self.assertIn(phrase, ws._inside(self.root, result["recipient_path"]).read_text())
            checked = command("desk.py", "payment-followup-check", "--root", self.root, "--report", result["path"])
            self.assertEqual(checked["delivery_state"], "not_sent")

    def test_working_evidence_drift_blocks_reuse_without_destroying_draft(self):
        result = self.prepare()
        draft = ws._inside(self.root, result["recipient_path"]).read_bytes()
        ws._inside(self.root, self.proof).write_text("Revised private review")
        self.assertFalse(follow.check(self.root, result["path"])["current"])
        with self.assertRaises(ws.WorkspaceError):
            self.prepare()
        self.assertEqual(ws._inside(self.root, result["recipient_path"]).read_bytes(), draft)

    def test_manifest_or_frozen_review_corruption_fails_closed(self):
        first = self.prepare()
        path = ws._inside(self.root, first["path"])
        manifest = json.loads(path.read_text()); manifest["delivery_state"] = "sent"
        path.write_text(json.dumps(manifest))
        with self.assertRaises(ws.WorkspaceError):
            follow.check(self.root, first["path"])
        second = self.prepare()
        manifest = json.loads(ws._inside(self.root, second["path"]).read_text())
        ws._inside(self.root, manifest["sources"][1]["path"]).write_text("Corrupted review")
        with self.assertRaises(ws.WorkspaceError):
            follow.check(self.root, second["path"])
