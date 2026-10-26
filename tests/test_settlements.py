"""Recorded payment allocation is distinct from authoritative invoice settlement."""
import json
from test_cash_vat import ProposalLinkTests, ac, ws


class SettlementTests(ProposalLinkTests):
    def settlement(self, period="2026-10", identifier="proposal-1"):
        return next(row for row in ac.period_report(self.root, period)["settlements"]
                    if row["proposal_id"] == identifier)

    def test_partial_payments_across_periods_and_refund(self):
        self.proposal("proposal-1")
        first = self.entry("first", "60", self.line("60", status="none_stated", proposal="proposal-1"))
        ac.post(self.root, first)
        self.assertEqual(self.settlement()["remaining"], "59.00")
        self.assertEqual(self.settlement()["status"], "partial")
        ac.post(self.root, self.entry("second", "59", self.line("59", status="none_stated", proposal="proposal-1"), date="2026-11-02"))
        self.assertEqual(self.settlement()["remaining"], "59.00")
        self.assertEqual(self.settlement("2026-11")["status"], "balanced")
        ac.post(self.root, self.entry("refund", "-19", self.line("-19", status="none_stated", proposal="proposal-1"), date="2026-11-03"))
        self.assertEqual(self.settlement("2026-11")["remaining"], "19.00")

    def test_overpayment_is_preserved_and_flagged(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        ac.post(self.root, self.paid("second"))
        row = self.settlement()
        self.assertEqual((row["allocated"], row["remaining"], row["status"]), ("238.00", "-119.00", "overpaid"))
        self.assertIn("settlement_overpaid", ac.period_report(self.root, "2026-10")["open_items"])

    def test_currency_difference_has_no_invented_conversion(self):
        self.proposal("proposal-1")
        value = self.paid()
        value["currency"] = "USD"
        ac.post(self.root, value)
        row = self.settlement()
        self.assertEqual(row["status"], "needs_review")
        self.assertIsNone(row["remaining"])
        self.assertIn("currency_mismatch", row["issues"])
        self.assertEqual(row["payments"][0]["currency"], "USD")

    def test_expense_and_refund_keep_direction_and_reversal_clears_allocation(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.entry("purchase", "-119", self.line("-119", "expense", status="none_stated", proposal="proposal-1")))
        self.assertEqual(self.settlement()["status"], "balanced")
        ac.reverse(self.root, "purchase", "reversal", self.proof, "owner", "Synthetic reversal")
        self.assertEqual(self.settlement()["allocated"], "0")
        self.assertEqual(self.settlement()["status"], "unpaid")
        ac.post(self.root, self.entry("corrected", "-100", self.line("-100", "expense", status="none_stated", proposal="proposal-1"), replaces="purchase", transaction_id="purchase"))
        self.assertEqual(self.settlement()["remaining"], "19.00")

    def test_transfer_cannot_satisfy_invoice_and_supersession_does_not_reallocate(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.entry("transfer", "119", self.line("119", "transfer", status="none_stated", proposal="proposal-1")))
        self.assertIn("movement_unresolved", self.settlement()["issues"])
        self.proposal("proposal-2", supersedes="proposal-1")
        self.assertIn("proposal_superseded", self.settlement()["issues"])
        self.assertEqual(self.settlement(identifier="proposal-2")["allocated"], "0")

    def test_prior_period_change_invalidates_report_used_by_filing(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        report = ac.export_report(self.root, "2026-11")
        payload = self.root / "05_tax/2026/synthetic.txt"
        payload.write_text("Synthetic external output", encoding="utf-8")
        filing = ac.template("filing")
        filing.update(filing_id="filing", form="ustva", form_version="2026", period="2026-11", recipient="synthetic",
                      payload_file="05_tax/2026/synthetic.txt", source_files=[report["path"]])
        ac.create_filing(self.root, filing)
        self.assertFalse(ac.check_filing(self.root, "filing")["issues"])
        ac.post(self.root, self.paid("late-recorded-october-payment"))
        self.assertTrue(ac.check_filing(self.root, "filing")["issues"])

    def test_corrected_allocation_clears_superseded_proposal_warning(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        self.proposal("proposal-2", supersedes="proposal-1")
        ac.reverse(self.root, "paid", "reversal", self.proof, "owner", "Reallocate to reviewed correction")
        replacement = self.paid("corrected", proposal="proposal-2")
        replacement.update(replaces="paid", transaction_id="paid")
        ac.post(self.root, replacement)
        report = ac.period_report(self.root, "2026-11")
        self.assertEqual([(row["proposal_id"], row["status"]) for row in report["settlements"]], [("proposal-2", "balanced")])
        self.assertNotIn("settlement_needs_review", report["open_items"])

    def test_changed_prior_period_evidence_blocks_settlement(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        (self.root / self.proof).write_text("Changed payment proof", encoding="utf-8")
        with self.assertRaises(ws.WorkspaceError):
            ac.period_report(self.root, "2026-11")

    def test_export_readable_balances_in_both_languages(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        for language, title in (("en", "Invoice payment allocation"), ("ru", "Распределение платежей по счетам")):
            ws.configure_workspace(self.root, language=language)
            output = ac.export_report(self.root, "2026-10")
            text = (self.root / output["markdown_path"]).read_text()
            self.assertIn(title, text)
            self.assertIn("SYN-1", text)
            self.assertIn("119.00", text)
            self.assertEqual(json.loads((self.root / output["path"]).read_text())["settlements"][0]["status"], "balanced")

    def test_currency_warning_is_readable_in_export(self):
        self.proposal("proposal-1")
        entry = self.paid()
        entry["currency"] = "USD"
        ac.post(self.root, entry)
        output = ac.export_report(self.root, "2026-10")
        self.assertIn("Payment and invoice currencies differ", (self.root / output["markdown_path"]).read_text())
