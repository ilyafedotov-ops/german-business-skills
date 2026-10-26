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
        self.assertEqual(snapshot["next_action"], "choose_task")
        self.assertEqual(snapshot["capabilities"]["elster_submission"], "not_implemented")

    def test_another_month_document_does_not_make_workspace_empty(self):
        self.receive()
        overview.generate(self.root, "2026-11", "2026-11-02", "en")
        snapshot = ws._load(ws._inside(self.root, "00_admin/overview.json"))
        self.assertEqual(snapshot["documents"], [])
        self.assertEqual(snapshot["next_action"], "choose_accounting")


class LifecycleOverviewTests(CaseFixture):
    configure = lifecycle.AccountingTests.configure
    entry = lifecycle.AccountingTests.entry
    filing = lifecycle.AccountingTests.filing
    action = lifecycle.AccountingTests.action
    view = OverviewTests.view

    def setUp(self):
        super().setUp()
        self.proof = self.evidence()

    def task(self, identifier, title, status="pending", **fields):
        record = {"schema_version": 1, "id": identifier, "title": title,
                  "owner": "owner", "status": status, **fields}
        saved = ws.save_entry(self.root, "tasks", {**record, "status": "pending"})
        if status != "pending":
            return ws.save_entry(self.root, "tasks", record, saved["sha256"])
        return saved

    def test_undated_lifecycle_task_is_visible_without_selecting_accounting(self):
        self.task("launch", "Prepare registration <script>unsafe</script>", note="Read the existing launch plan")
        paths = ["00_admin/tasks.json", "00_admin/questions.json", "01_profile/business.json", ws.EVENTS]
        before = {p: ws._inside(self.root, p).read_bytes() for p in paths}
        for language in ("en", "ru"):
            snapshot, html = self.view(language)
            self.assertEqual(snapshot["next_action"], "continue_task")
            self.assertEqual(snapshot["next_task_id"], "launch")
            self.assertEqual(snapshot["active_tasks"][0]["readiness"], "ready")
            self.assertEqual(snapshot["accounting"]["accounting_system"], "undecided")
            self.assertIn('id="active-tasks"', html)
            self.assertIn("Prepare registration &lt;script&gt;unsafe&lt;/script&gt;", html)
            self.assertNotIn("<script>", html)
            md=ws._inside(self.root,"00_admin/overview.md").read_text()
            self.assertIn("Prepare registration",md)
            self.assertNotIn("reconciliation_not_supplied", {row["code"] for row in snapshot["open_items"]})
        self.assertEqual(before,{p: ws._inside(self.root,p).read_bytes() for p in paths})
        later = overview.generate(self.root,"2026-11","2026-11-02","en")
        self.assertEqual(ws._load(ws._inside(self.root,"00_admin/overview.json"))["next_task_id"],"launch")

    def test_cancelled_and_incomplete_dependencies_do_not_become_ready(self):
        self.task("cancelled", "Cancelled request", "cancelled")
        self.task("waiting", "Wait for existing reply", depends_on=["cancelled"])
        self.task("blocked", "Explicitly blocked", "blocked")
        snapshot, _=self.view()
        self.assertEqual(snapshot["next_action"],"review_tasks")
        self.assertIsNone(snapshot["next_task_id"])
        self.assertEqual({row["id"] for row in snapshot["active_tasks"]},{"waiting","blocked"})
        waiting=next(row for row in snapshot["active_tasks"] if row["id"]=="waiting")
        self.assertEqual(waiting["pending_dependencies"],["cancelled"])
        self.assertEqual(waiting["readiness"],"blocked")

    def test_changed_completion_evidence_blocks_transitive_dependency(self):
        first=ws._inside(self.root,"08_correspondence/first.txt");first.write_text("Synthetic first proof")
        second=ws._inside(self.root,"08_correspondence/second.txt");second.write_text("Synthetic second proof")
        self.task("first","Gather facts","completed",evidence_file="08_correspondence/first.txt")
        self.task("second","Prepare plan","completed",depends_on=["first"],evidence_file="08_correspondence/second.txt")
        self.task("submit","Review application",depends_on=["second"])
        snapshot,_=self.view()
        self.assertEqual(snapshot["next_task_id"],"submit")
        first.write_text("Changed proof")
        snapshot,_=self.view()
        self.assertIsNone(snapshot["next_task_id"])
        self.assertEqual(snapshot["active_tasks"][0]["pending_dependencies"],["first"])
        self.assertEqual(snapshot["active_tasks"][0]["readiness"],"needs_review")

    def test_changed_task_evidence_does_not_hide_independent_work(self):
        self.task("stale","Revise a letter",evidence_file=self.proof)
        self.task("other","Prepare service questions")
        ws._inside(self.root,self.proof).write_text("Changed evidence")
        snapshot,_=self.view()
        self.assertEqual(snapshot["next_task_id"],"other")
        stale=next(row for row in snapshot["active_tasks"] if row["id"]=="stale")
        self.assertEqual(stale["evidence_status"],"needs_review")
        self.assertEqual(stale["readiness"],"needs_review")

    def test_lifecycle_task_cannot_hide_uncertain_submission_or_corruption(self):
        self.configure("external")
        self.filing(period="2026-09")
        for action in ("review","authorize","begin"):self.action("return-1",action)
        self.task("launch","Plan next activity")
        snapshot,_=self.view()
        self.assertEqual(snapshot["next_action"],"resolve_submission")
        ws._inside(self.root,"00_admin/tasks.json").write_text('{broken')
        snapshot,html=self.view()
        self.assertEqual(snapshot["next_action"],"repair")
        self.assertEqual(snapshot["active_tasks"],[])
        self.assertIsNone(snapshot["next_task_id"])
        self.assertNotIn("Plan next activity",html)
