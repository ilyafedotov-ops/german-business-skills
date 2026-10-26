"""Real private-file accounting routing, cash journal and filing evidence journeys."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace as ws
from casefiles import accounting as ac


class AccountingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "private"
        ws.init_workspace(self.root, 2026, "en")
        self.proof = "08_correspondence/review.md"
        (self.root / self.proof).write_text("Synthetic user choice and reviewed evidence", encoding="utf-8")

    def configure(self, system="local", **changes):
        value = ac.template("configuration")
        value.update(system=system, product="Example accounting / web" if system == "external" else None,
                     account_reference="business-one", method="EÜR", reviewer="owner", evidence_file=self.proof)
        value.update(changes)
        return ac.configure(self.root, value)

    def entry(self, identifier="sale", amount="100.00", kind="income", **changes):
        value = ac.template("entry")
        value.update(entry_id=identifier, date="2026-10-20", account="psp", transaction_id=identifier,
                     amount=amount, currency="EUR", reviewer="owner", evidence_file=self.proof,
                     note="Synthetic reviewed cash movement")
        value["lines"] = [{"kind": kind, "amount": amount, "category": kind, "activity_id": "activity-1", "proposal_id": None,
                           "vat": {"status": "none_stated", "net": None, "tax": None, "rate": None}}]
        value.update(changes)
        return value

    def filing(self, identifier="return-1", **changes):
        payload = self.root / "05_tax/2026/draft.json"
        if not payload.exists():
            payload.write_text('{"synthetic":true,"amount":"100.00"}', encoding="utf-8")
        value = ac.template("filing")
        value.update(filing_id=identifier, form="ustva", form_version="2026", period="2026-10",
                     recipient="synthetic-finanzamt", payload_file="05_tax/2026/draft.json",
                     source_files=[self.proof], unresolved_items=[], supersedes=None)
        value.update(changes)
        return ac.create_filing(self.root, value)

    def action(self, identifier, action, **changes):
        current = ac.get_filing(self.root, identifier)
        value = ac.template("filing-action")
        value.update(filing_id=identifier, action=action, actor="owner", evidence_file=self.proof,
                     note="Synthetic explicit review of recipient, period and exact report")
        value.update(changes)
        return ac.filing_action(self.root, value, current["sha256"])

    def test_welcome_has_no_accounting_default_and_resume_preserves_choice(self):
        self.assertEqual(ac.status(self.root)["accounting_system"], "undecided")
        self.assertFalse((self.root / ac.STATE).exists())
        self.configure("external")
        ws.start_workspace(self.root, year=2027, language="ru")
        self.assertEqual(ac.status(self.root)["accounting_system"], "external")
        with self.assertRaises(ws.WorkspaceError):
            ac.post(self.root, self.entry())
        self.assertEqual(ac.status(self.root)["entry_count"], 0)

    def test_existing_profile_method_is_not_replaced_or_assumed(self):
        before = (self.root / ws.PROFILE).read_bytes()
        self.configure(method="unresolved")
        with self.assertRaises(ws.WorkspaceError):
            ac.post(self.root, self.entry())
        self.assertEqual((self.root / ws.PROFILE).read_bytes(), before)

    def test_cash_movements_separate_sales_fees_transfers_and_currencies(self):
        self.configure()
        for record in (self.entry(), self.entry("fee", "-3.00", "expense"),
                       self.entry("payout", "-97.00", "transfer"),
                       self.entry("bank-credit", "97.00", "transfer", account="bank"),
                       self.entry("usd-sale", "20.00", currency="USD")):
            ac.post(self.root, record)
        report = ac.period_report(self.root, "2026-10")
        self.assertEqual(report["totals"]["EUR"], {"income": "100.00", "expense": "-3.00", "transfer": "0.00", "unresolved": "0", "operating_cash_net": "97.00"})
        self.assertEqual(report["totals"]["USD"]["income"], "20.00")
        self.assertEqual(report["tax_return_status"], "not_calculated")
        self.assertIn("coverage_not_confirmed", report["open_items"])

    def test_split_totals_and_duplicate_account_transaction_are_checked(self):
        self.configure()
        record = self.entry(amount="97.00")
        record["lines"] = [dict(record["lines"][0], amount="100.00"),
                           dict(record["lines"][0], kind="expense", category="fee", amount="-3.00")]
        ac.post(self.root, record)
        with self.assertRaises(ws.WorkspaceError):
            ac.post(self.root, self.entry("another-id", transaction_id="sale"))
        with self.assertRaises(ws.WorkspaceError):
            ac.post(self.root, self.entry("unbalanced", lines=record["lines"]))

    def test_corrections_preserve_original_and_do_not_double_reverse(self):
        self.configure()
        ac.post(self.root, self.entry())
        result = ac.reverse(self.root, "sale", "sale-reversal", self.proof, "owner", "Wrong amount")
        self.assertEqual(result["reverses"], "sale")
        with self.assertRaises(ws.WorkspaceError):
            ac.reverse(self.root, "sale", "again", self.proof, "owner", "Again")
        replacement = self.entry("corrected", "90.00", transaction_id="sale", replaces="sale")
        ac.post(self.root, replacement)
        self.assertEqual(ac.period_report(self.root, "2026-10")["totals"]["EUR"]["income"], "90.00")
        self.assertEqual(ac.status(self.root)["entry_count"], 3)

    def test_system_change_after_posting_requires_migration_not_configuration(self):
        self.configure()
        ac.post(self.root, self.entry())
        with self.assertRaises(ws.WorkspaceError):
            self.configure("external")
        self.assertEqual(ac.status(self.root)["accounting_system"], "local")

    def test_changed_entry_evidence_is_not_a_clean_report(self):
        self.configure()
        ac.post(self.root, self.entry())
        (self.root / self.proof).write_text("Changed evidence", encoding="utf-8")
        with self.assertRaises(ws.WorkspaceError):
            ac.period_report(self.root, "2026-10")

    def test_empty_and_unresolved_records_never_claim_complete_accounts(self):
        self.configure()
        self.assertIn("no_entries", ac.period_report(self.root, "2026-10")["open_items"])
        ac.post(self.root, self.entry(kind="unresolved"))
        result = ac.period_report(self.root, "2026")
        self.assertIn("unclassified_movements", result["open_items"])
        self.assertEqual(result["readiness"], "needs_review")

    def test_external_route_prepares_filing_without_creating_shadow_ledger(self):
        self.configure("external")
        self.filing()
        self.assertEqual(ac.get_filing(self.root, "return-1")["record"]["state"], "draft")
        self.assertEqual(ac.status(self.root)["entry_count"], 0)
        self.assertEqual(ac.status(self.root)["transmission"], "not_implemented")

    def test_review_and_authorization_do_not_mean_submission(self):
        self.configure()
        self.filing()
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "authorize")
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        record = ac.get_filing(self.root, "return-1")["record"]
        self.assertEqual(record["state"], "authorized")
        self.assertEqual(record["responses"], [])
        self.assertIsNone(record["receipt"])

    def test_changed_payload_blocks_attempt_and_new_draft_needs_new_approval(self):
        self.configure()
        self.filing()
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        (self.root / "05_tax/2026/draft.json").write_text('{"changed":true}', encoding="utf-8")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "begin")
        self.action("return-1", "cancel")
        self.filing("return-2", supersedes="return-1")
        self.assertEqual(ac.get_filing(self.root, "return-2")["record"]["state"], "draft")

    def test_ambiguous_submission_blocks_retry_and_duplicate_filing(self):
        self.configure()
        self.filing()
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        self.action("return-1", "begin")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "begin")
        with self.assertRaises(ws.WorkspaceError):
            self.filing("duplicate")
        with self.assertRaises(ws.WorkspaceError):
            self.filing("correction", supersedes="return-1")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "cancel")
        self.action("return-1", "not-submitted")
        self.assertEqual(ac.get_filing(self.root, "return-1")["record"]["state"], "reviewed")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "begin")

    def test_receipt_and_responses_preserve_exact_snapshot_after_source_changes(self):
        self.configure("external")
        self.filing()
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        self.action("return-1", "begin")
        (self.root / "05_tax/2026/draft.json").write_text("Next version", encoding="utf-8")
        self.action("return-1", "receipt", external_id="synthetic-ticket-1")
        self.action("return-1", "response", response_kind="request_for_information", due_date="2026-11-15")
        record = ac.get_filing(self.root, "return-1")["record"]
        self.assertEqual(record["state"], "submitted")
        self.assertEqual(record["responses"][0]["due_date"], "2026-11-15")
        self.assertIn('"amount":"100.00"', (self.root / record["payload"]["path"]).read_text())
        self.assertNotIn("accepted", record)

    def test_stale_updates_missing_receipts_and_mutable_evidence_are_rejected(self):
        self.configure()
        created = self.filing()
        self.action("return-1", "review")
        action = ac.template("filing-action")
        action.update(filing_id="return-1", action="authorize", actor="owner", evidence_file=self.proof, note="Approved")
        with self.assertRaises(ws.WorkspaceError):
            ac.filing_action(self.root, action, created["sha256"])
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "receipt", external_id="ticket")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "authorize", evidence_file=ac.STATE)

    def test_unresolved_filing_and_invalid_deadline_cannot_pass_review(self):
        self.configure()
        self.filing(unresolved_items=["Unverified total"])
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "review")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "response", due_date="2026-02-30")

    def test_configuration_change_requires_current_hash_and_evidence(self):
        original = self.configure()
        changed = ac.template("configuration")
        changed.update(system="external", product="Example", account_reference="company", method="EÜR", reviewer="owner", evidence_file=self.proof)
        with self.assertRaises(ws.WorkspaceError):
            ac.configure(self.root, changed)
        ac.configure(self.root, changed, original["sha256"])
        self.assertEqual(ac.status(self.root)["accounting_system"], "external")

    def test_cli_templates_and_status_work_in_existing_desk(self):
        for args in (["accounting-template", "--kind", "configuration"],
                     ["accounting-status", "--root", str(self.root)]):
            result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "desk.py"), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIsInstance(json.loads(result.stdout), dict)

    def test_report_export_reconciles_real_csv_and_renders_both_languages(self):
        self.configure()
        ac.post(self.root, self.entry(account="bank"))
        bank_path = "03_banking/synthetic.csv"
        (self.root / bank_path).write_text("transaction_id,booking_date,amount,currency\nsale,2026-10-20,100.00,EUR\n", encoding="utf-8")
        for language, expected in (("en", "Cash movement report"), ("ru", "Отчёт о движении денег")):
            ws.configure_workspace(self.root, language=language)
            exported = ac.export_report(self.root, "2026-10")
            self.assertIn(expected, (self.root / exported["markdown_path"]).read_text(encoding="utf-8"))
            reconciled = ws.reconciliation_report(self.root, bank_path, exported["ledger_files"]["bank"], "2026-10")
            self.assertEqual(len(reconciled["matches"]), 1)
            self.assertEqual(reconciled["differences"], [])

    def test_amounts_keep_small_differences_beside_large_values(self):
        self.configure()
        ac.post(self.root, self.entry(amount="1000000000000000000000000000000.00001"))
        ac.post(self.root, self.entry("tiny", "-0.00002", "expense"))
        self.assertEqual(ac.period_report(self.root, "2026-Q4")["totals"]["EUR"]["operating_cash_net"], "999999999999999999999999999999.99999")

    def test_missing_or_rolled_back_register_cannot_erase_uncertain_submission(self):
        self.configure()
        old = (self.root / ac.STATE).read_bytes()
        self.filing()
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        self.action("return-1", "begin")
        (self.root / ac.STATE).unlink()
        with self.assertRaises(ws.WorkspaceError):
            ac.status(self.root)
        with self.assertRaises(ws.WorkspaceError):
            self.configure()
        (self.root / ac.STATE).write_bytes(old)
        with self.assertRaises(ws.WorkspaceError):
            ac.status(self.root)

    def test_local_ledger_change_invalidates_source_report_before_attempt(self):
        self.configure()
        ac.post(self.root, self.entry())
        report = ac.export_report(self.root, "2026-10")
        self.filing(source_files=[report["path"]])
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        ac.post(self.root, self.entry("late-receipt", "7.00"))
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "begin")

    def test_account_alias_case_does_not_split_reconciliation_export(self):
        self.configure()
        ac.post(self.root, self.entry(account="Bank"))
        ac.post(self.root, self.entry("sale-2", account="bank"))
        report = ac.export_report(self.root, "2026-10")
        self.assertEqual(list(report["ledger_files"]), ["bank"])
        self.assertEqual(len((self.root / report["ledger_files"]["bank"]).read_text().splitlines()), 3)

    def test_cash_summary_cannot_be_approved_as_a_completed_tax_return(self):
        self.configure()
        ac.post(self.root, self.entry())
        report = ac.export_report(self.root, "2026-10")
        self.filing(payload_file=report["path"])
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "review")

    def test_filing_check_is_read_only_and_exposes_each_required_step(self):
        self.configure("external")
        self.filing()
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        check = ac.check_filing(self.root, "return-1")
        self.assertEqual(check["next_step"], "review")
        self.assertEqual(check["allowed_preflight_actions"], ["review"])
        self.assertEqual(check["issues"], [])
        self.assertEqual(check["tax_correctness"], "not_assessed")
        self.assertEqual(check["transmission"], "not_implemented")
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.action("return-1", "review")
        self.assertEqual(ac.check_filing(self.root, "return-1")["allowed_preflight_actions"], ["authorize"])
        self.action("return-1", "authorize")
        self.assertEqual(ac.check_filing(self.root, "return-1")["allowed_preflight_actions"], ["begin"])
        self.action("return-1", "begin")
        check = ac.check_filing(self.root, "return-1")
        self.assertEqual(check["next_step"], "resolve_submission_outcome")
        self.assertEqual(check["allowed_preflight_actions"], [])

    def test_filing_check_reports_multiple_issues_without_changing_draft(self):
        self.configure()
        self.filing(unresolved_items=["Unverified VAT timing"])
        (self.root / self.proof).unlink()
        (self.root / "05_tax/2026/draft.json").write_text("Changed draft")
        check = ac.check_filing(self.root, "return-1")
        codes = {item["code"] for item in check["issues"]}
        self.assertTrue({"configuration_evidence", "source_changed", "unresolved_item"} <= codes)
        self.assertEqual(check["allowed_preflight_actions"], [])
        self.assertEqual(check["next_step"], "resolve_issues")
        self.assertEqual(check["state"], "draft")
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "review")

    def test_filing_check_detects_missing_frozen_evidence_and_never_calls_it_ready(self):
        self.configure()
        self.filing()
        saved = ac.get_filing(self.root, "return-1")["record"]
        (self.root / saved["payload"]["path"]).unlink()
        check = ac.check_filing(self.root, "return-1")
        self.assertIn("snapshot_changed", [item["code"] for item in check["issues"]])
        self.assertEqual(check["allowed_preflight_actions"], [])

    def test_filing_check_reports_stale_cash_sources_and_actions_recheck(self):
        self.configure()
        ac.post(self.root, self.entry())
        report = ac.export_report(self.root, "2026-10")
        self.filing(source_files=[report["path"]])
        self.action("return-1", "review")
        self.action("return-1", "authorize")
        self.assertEqual(ac.check_filing(self.root, "return-1")["allowed_preflight_actions"], ["begin"])
        ac.post(self.root, self.entry("later", "7.00"))
        check = ac.check_filing(self.root, "return-1")
        self.assertIn("local_report_invalid", [item["code"] for item in check["issues"]])
        with self.assertRaises(ws.WorkspaceError):
            self.action("return-1", "begin")
        self.assertEqual(ac.get_filing(self.root, "return-1")["record"]["state"], "authorized")

    def test_check_historical_attempt_uses_frozen_evidence_and_does_not_allow_retry(self):
        self.configure()
        self.filing()
        for action in ("review", "authorize", "begin"):
            self.action("return-1", action)
        (self.root / self.proof).write_text("New current records")
        (self.root / "05_tax/2026/draft.json").unlink()
        check = ac.check_filing(self.root, "return-1")
        self.assertEqual(check["issues"], [])
        self.assertEqual(check["source_scope"], "frozen_evidence_only")
        self.assertEqual(check["allowed_preflight_actions"], [])
        self.action("return-1", "receipt", external_id="actual-reference-for-synthetic-test")
        self.assertEqual(ac.check_filing(self.root, "return-1")["next_step"], "follow_up")

    def test_filing_check_cli_and_unknown_record(self):
        self.configure()
        self.filing()
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "desk.py"),
                                 "filing-check", "--root", str(self.root), "--id", "return-1"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["next_step"], "review")
        with self.assertRaises(ws.WorkspaceError):
            ac.check_filing(self.root, "missing")

    def test_filing_check_keeps_independent_report_blockers_when_one_snapshot_is_missing(self):
        self.configure()
        ac.post(self.root, self.entry())
        month = ac.export_report(self.root, "2026-10")
        year = ac.export_report(self.root, "2026")
        self.filing(source_files=[month["path"], year["path"]])
        ac.post(self.root, self.entry("late", "7.00"))
        check = ac.check_filing(self.root, "return-1")
        invalid = {item["path"] for item in check["issues"] if item["code"] == "local_report_invalid"}
        self.assertEqual(invalid, {month["path"], year["path"]})
        record = ac.get_filing(self.root, "return-1")["record"]
        (self.root / record["sources"][0]["path"]).unlink()
        check = ac.check_filing(self.root, "return-1")
        self.assertIn("snapshot_changed", [item["code"] for item in check["issues"]])
        self.assertIn(year["path"], [item["path"] for item in check["issues"] if item["code"] == "local_report_invalid"])

    def test_filing_check_lists_independent_changed_cash_entry_evidence(self):
        self.configure()
        paths = ["08_correspondence/one.md", "08_correspondence/two.md"]
        for i, path in enumerate(paths):
            (self.root / path).write_text("Synthetic cash entry evidence")
            ac.post(self.root, self.entry("sale-" + str(i), evidence_file=path))
        report = ac.export_report(self.root, "2026-10")
        self.filing(source_files=[report["path"]])
        for path in paths:
            (self.root / path).unlink()
        check = ac.check_filing(self.root, "return-1")
        self.assertEqual({item["path"] for item in check["issues"] if item["code"] == "local_entry_evidence"}, set(paths))


if __name__ == "__main__":
    unittest.main()
