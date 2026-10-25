"""Synthetic first-run, readiness, and profile contract regressions."""
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts/workspace.py"
SPEC = importlib.util.spec_from_file_location("onboarding_workspace", SCRIPT)
workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workspace)


class OnboardingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "Business Демо files"
        workspace.init_workspace(self.root, 2026, "en")

    def read(self, name):
        return json.loads((self.root / name).read_text(encoding="utf-8"))

    def fact(self, field, value):
        return {"field": field, "value": value, "status": "declared",
                "source": {"kind": "user_statement", "ref": "synthetic-intake"}}

    def runtime(self):
        record = self.read("00_admin/runtime.json")
        record.update(assistant_product="Synthetic host", app_version="test",
                      session_execution="local", model_provider="Synthetic provider",
                      authentication_type="account", contract_plan="Synthetic plan",
                      training_policy_checked_at="2026-10-25", dpa_status="reviewed",
                      retention_policy_reference="Synthetic terms", residency_scope="reviewed scope",
                      client_data_mode="review_recorded",
                      review={"reviewed_by": "Synthetic owner", "reviewed_at": "2026-10-25",
                              "scope": "Synthetic bookkeeping workflow", "evidence_file": "00_admin/review.md"})
        (self.root / "00_admin/review.md").write_text("Synthetic assessment, not a legal certification.", encoding="utf-8")
        return record

    def test_fresh_workspace_is_usable_for_demo_but_setup_incomplete(self):
        result = workspace.workspace_status(self.root)
        self.assertEqual(result["status"], "setup_incomplete")
        self.assertEqual(result["workspace_health"], "ok")
        self.assertEqual(result["data_processing_review"], "not_recorded")
        self.assertIn("assistant_product", result["setup_missing"])
        self.assertTrue(result["synthetic_work_available"])

    def test_missing_and_corrupt_runtime_are_actionable_without_profile_leak(self):
        workspace.record_fact(self.root, self.fact("owner_name", "Private Synthetic Owner"))
        path = self.root / "00_admin/runtime.json"
        for payload in (None, b"{broken", b"[]"):
            with self.subTest(payload=payload):
                if payload is None:
                    path.unlink(missing_ok=True)
                else:
                    path.write_bytes(payload)
                result = workspace.workspace_status(self.root)
                self.assertEqual(result["status"], "needs_attention")
                self.assertIn("runtime_invalid", result["issues"])
                self.assertNotIn("Private Synthetic Owner", json.dumps(result))

    def test_runtime_review_requires_evidence_and_records_history(self):
        record = self.runtime()
        before = (self.root / "00_admin/runtime.json").read_bytes()
        invalid = dict(record, review={**record["review"], "evidence_file": "00_admin/missing.md"})
        with self.assertRaises(workspace.WorkspaceError):
            workspace.configure_runtime(self.root, invalid)
        self.assertEqual((self.root / "00_admin/runtime.json").read_bytes(), before)
        result = workspace.configure_runtime(self.root, record)
        self.assertTrue((self.root / f"09_audit/history/{result['history_id']}.json").is_file())
        status = workspace.workspace_status(self.root)
        self.assertEqual(status["data_processing_review"], "recorded")
        self.assertEqual(status["status"], "configured")
        self.assertNotIn("compliant", status)

    def test_review_evidence_change_invalidates_recorded_review(self):
        workspace.configure_runtime(self.root, self.runtime())
        (self.root / "00_admin/review.md").write_text("Replaced assessment", encoding="utf-8")
        status = workspace.workspace_status(self.root)
        self.assertEqual(status["status"], "needs_attention")
        self.assertIn("runtime_invalid", status["issues"])

    def test_invalid_fact_values_do_not_mutate_profile_or_audit(self):
        before = [(self.root / p).read_bytes() for p in (workspace.PROFILE, workspace.EVENTS)]
        invalid = [("vat_current_regime", {"invalid": ["anything"]}),
                   ("vat_current_regime", "automatically exempt"), ("employees", "yes"),
                   ("business_start_date", "2026-02-30"), ("vat_prior_year", True),
                   ("client_countries", "Germany"),
                   ("vat_prior_year_turnover_all_activities", 123.45),
                   ("activities", [{"description": "No stable ID"}])]
        for field, value in invalid:
            with self.subTest(field=field, value=value):
                with self.assertRaises(workspace.WorkspaceError):
                    workspace.record_fact(self.root, self.fact(field, value))
        self.assertEqual([(self.root / p).read_bytes() for p in (workspace.PROFILE, workspace.EVENTS)], before)

    def test_valid_typed_facts_and_unknown_remain_supported(self):
        records = [("vat_current_regime", "Regelbesteuerung"), ("employees", False),
                   ("business_start_date", "2026-10-01"), ("client_countries", ["DE", "FR"]),
                   ("vat_prior_year_turnover_all_activities", {"amount": "1234.56", "currency": "EUR", "period": "2025"}),
                   ("activities", [{"activity_id": "activity-1", "description": "Synthetic services", "classification": "unresolved", "commenced_at": None}])]
        for field, value in records:
            workspace.record_fact(self.root, self.fact(field, value))
        self.assertEqual(self.read(workspace.PROFILE)["facts"]["employees"]["value"], False)
        workspace.record_fact(self.root, {"field": "employees", "value": None, "status": "unknown"})

    def test_legacy_malformed_fact_is_flagged_without_rewriting_it(self):
        path = self.root / workspace.PROFILE
        profile = self.read(workspace.PROFILE)
        profile["facts"]["vat_current_regime"].update(value={"old": "unsupported"}, status="declared")
        path.write_text(json.dumps(profile), encoding="utf-8")
        before = path.read_bytes()
        result = workspace.workspace_status(self.root)
        self.assertEqual(result["status"], "needs_attention")
        self.assertIn("vat_current_regime", result["invalid_profile_fields"])
        self.assertEqual(path.read_bytes(), before)

    def test_start_resumes_existing_workspace_without_resetting_preferences(self):
        workspace.configure_workspace(self.root, language="ru", mode="tax-consultant")
        before = {p: (self.root / p).read_bytes() for p in (workspace.PROFILE, workspace.MARKER, workspace.EVENTS)}
        result = workspace.start_workspace(self.root, year=2027, language="en", mode="general")
        self.assertEqual(result["action"], "resumed")
        self.assertEqual(result["language"], "ru")
        self.assertEqual(result["mode"], "tax-consultant")
        self.assertEqual({p: (self.root / p).read_bytes() for p in before}, before)

    def test_start_creates_only_empty_private_workspace(self):
        target = self.base / "New business"
        result = workspace.start_workspace(target, year=2026, language="en", mode="general")
        self.assertEqual(result["action"], "created")
        self.assertEqual(result["status"], "setup_incomplete")
        occupied = self.base / "Occupied"
        occupied.mkdir()
        (occupied / "keep.txt").write_text("keep", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.start_workspace(occupied, year=2026)
        self.assertEqual((occupied / "keep.txt").read_text(), "keep")

    def test_demo_has_real_verifiable_synthetic_results_and_refuses_overwrite(self):
        target = self.base / "Demo only"
        result = workspace.create_demo(target, year=2026, language="ru")
        self.assertEqual(result["reconciliation"]["matched_groups"], 3)
        self.assertEqual(result["reconciliation"]["unmatched_bank"], 1)
        self.assertEqual(result["reconciliation"]["status"], "needs_review")
        self.assertEqual(workspace.verify_workspace(target)["status"], "ok")
        self.assertEqual(workspace.workspace_status(target)["documents"], 2)
        report = target / result["guide"]
        self.assertIn("12", report.read_text(encoding="utf-8"))
        before = report.read_bytes()
        with self.assertRaises(workspace.WorkspaceError):
            workspace.create_demo(target, year=2026)
        self.assertEqual(report.read_bytes(), before)

    def test_doctor_checks_local_health_without_inventing_host_capabilities(self):
        (self.root / workspace.LOCK).write_text("active writer", encoding="utf-8")
        result = workspace.diagnose_workspace(self.root)
        self.assertEqual(result["status"], "needs_attention")
        self.assertIn("workspace_locked", result["issues"])
        self.assertEqual(result["host_capabilities"], "not_probed")
        self.assertEqual((self.root / workspace.LOCK).read_text(), "active writer")

    def test_start_cli_outputs_machine_readable_next_action(self):
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(workspace.main(["start", "--root", str(self.root)]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["action"], "resumed")
        self.assertTrue(result["next_action"])

    def test_corrupt_audit_is_diagnosed_before_claiming_usable_workspace(self):
        (self.root / workspace.EVENTS).write_text("{}", encoding="utf-8")
        result = workspace.diagnose_workspace(self.root)
        self.assertEqual(result["workspace_health"], "needs_attention")
        self.assertIn("audit_invalid", result["issues"])
        self.assertFalse(result["synthetic_work_available"])

    def test_unknown_runtime_with_whitespace_cannot_be_recorded_as_reviewed(self):
        runtime = self.runtime()
        runtime["dpa_status"] = " unknown "
        with self.assertRaises(workspace.WorkspaceError):
            workspace.configure_runtime(self.root, runtime)

    def test_manual_runtime_configuration_change_invalidates_review(self):
        workspace.configure_runtime(self.root, self.runtime())
        runtime = self.read(workspace.RUNTIME)
        runtime["model_provider"] = "Another provider"
        (self.root / workspace.RUNTIME).write_text(json.dumps(runtime), encoding="utf-8")
        self.assertEqual(workspace.workspace_status(self.root)["data_processing_review"], "invalid")


if __name__ == "__main__":
    unittest.main()
