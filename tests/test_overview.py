"""The real overview must expose work without granting accounting/filing approval."""
import json
import test_accounting_lifecycle as lifecycle
from test_casework import CaseFixture
from casefiles import accounting as ac, overview
import workspace as ws


class OverviewTests(CaseFixture):
    configure = lifecycle.AccountingTests.configure
    entry = lifecycle.AccountingTests.entry
    filing = lifecycle.AccountingTests.filing
    action = lifecycle.AccountingTests.action

    def setUp(self):
        super().setUp()
        self.proof = self.evidence()

    def view(self, language="en"):
        result = overview.generate(self.root, "2026-10", "2026-10-26", language)
        snapshot = ws._load(ws._inside(self.root, "00_admin/overview.json"))
        return snapshot, (self.root / result["html_path"]).read_text(encoding="utf-8")

    def test_actual_journal_filing_blocker_and_question_are_visible_and_read_only(self):
        self.configure()
        ac.post(self.root, self.entry())
        self.filing(unresolved_items=["Check VAT evidence <script>unsafe</script>"])
        ws.save_entry(self.root, "questions", {"schema_version": 1, "id": "vat-question",
                      "title": "Clarify the invoice country", "owner": "owner", "status": "open"})
        before = (self.root / ac.STATE).read_bytes()
        for language in ("en", "ru"):
            snapshot, html = self.view(language)
            self.assertEqual(snapshot["accounting"]["accounting_system"], "local")
            self.assertEqual(snapshot["accounting"]["period_entry_count"], 1)
            self.assertEqual(snapshot["capabilities"]["local_cash_journal"], "available")
            self.assertEqual(snapshot["capabilities"]["accounting_ledger"], "limited_cash_journal")
            self.assertEqual(snapshot["next_action"], "resolve_filing")
            self.assertEqual(snapshot["filings"][0]["issues"][0]["code"], "unresolved_item")
            self.assertIn("Clarify the invoice country", html)
            self.assertIn("return-1", html)
            self.assertIn("&lt;script&gt;unsafe&lt;/script&gt;", html)
            self.assertNotIn("<script>", html)
            self.assertIn("Clarify the invoice country", (self.root / "00_admin/overview.md").read_text())
        self.assertEqual((self.root / ac.STATE).read_bytes(), before)

    def test_unconfirmed_previous_period_is_never_hidden_by_month_filter(self):
        self.configure("external")
        self.filing(period="2026-09")
        for action in ("review", "authorize", "begin"):
            self.action("return-1", action)
        snapshot, html = self.view()
        self.assertEqual(snapshot["next_action"], "resolve_submission")
        self.assertEqual(snapshot["filings"][0]["state"], "submission_unconfirmed")
        self.assertIn("2026-09", html)
        self.assertIsNone(snapshot["accounting"]["period_entry_count"])

    def test_annual_and_quarterly_filings_are_included_without_other_month_drafts(self):
        self.configure("external")
        self.filing("annual", period="2026")
        self.filing("quarter", period="2026-Q4")
        self.filing("september", period="2026-09")
        snapshot, _ = self.view()
        self.assertEqual({row["filing_id"] for row in snapshot["filings"]}, {"annual", "quarter"})
        self.assertEqual(snapshot["accounting"]["product"], "Example accounting / web")

    def test_missing_or_changed_accounting_state_cannot_look_healthy(self):
        self.configure()
        self.filing()
        (self.root / ac.STATE).unlink()
        snapshot, _ = self.view()
        self.assertEqual(snapshot["health"], "needs_review")
        self.assertEqual(snapshot["next_action"], "repair")
        self.assertIsNone(snapshot["counts"]["documents"])

    def test_changed_filing_source_keeps_actual_preflight_blocker_in_view(self):
        self.configure("external")
        self.filing()
        (self.root / "05_tax/2026/draft.json").write_text("changed")
        snapshot, _ = self.view()
        self.assertIn("source_changed", {row["code"] for row in snapshot["filings"][0]["issues"]})
        self.assertEqual(snapshot["next_action"], "resolve_filing")

    def test_unconfigured_workspace_has_no_assumed_accounting_method(self):
        snapshot, _ = self.view()
        self.assertEqual(snapshot["accounting"]["accounting_system"], "undecided")
        self.assertEqual(snapshot["next_action"], "choose_accounting")
        self.assertEqual(snapshot["capabilities"]["elster_submission"], "not_implemented")
