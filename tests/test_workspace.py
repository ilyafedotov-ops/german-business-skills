"""Behavioral tests of private storage, evidence and explicit-ID reconciliation."""

from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).absolute().parents[1] / "skills" / "de-business-kit" / "scripts" / "workspace.py"
SPEC = importlib.util.spec_from_file_location("business_workspace", SCRIPT)
workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workspace)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "private"
        workspace.init_workspace(self.root, 2026, "ru")

    def load(self, relative):
        return json.loads((self.root / relative).read_text(encoding="utf-8"))

    def source(self, name="invoice.pdf", content=b"synthetic-original\n"):
        path = self.base / name
        path.write_bytes(content)
        return path

    def csvs(self, bank, ledger):
        bank_path = self.root / "03_banking" / "bank.csv"
        ledger_path = self.root / "04_accounting" / "ledger.csv"
        bank_path.write_text("transaction_id,booking_date,amount,currency\n" + bank, encoding="utf-8")
        ledger_path.write_text("entry_id,transaction_id,amount,currency\n" + ledger, encoding="utf-8")
        return bank_path, ledger_path

    def record(self, **changes):
        value = {"field": "legal_form", "value": "Einzelunternehmen", "status": "declared",
                 "source": {"kind": "user", "ref": "intake-1"},
                 "effective_from": "2026-10-01", "note": None}
        value.update(changes)
        return value

    def _symlink(self, link, target, is_directory=False):
        try:
            link.symlink_to(target, target_is_directory=is_directory)
        except (OSError, NotImplementedError):
            self.skipTest("Symlinks unavailable on this platform/account")

    def test_init_creates_blank_profile_and_year_layout_without_personal_defaults(self):
        profile = self.load(workspace.PROFILE)
        self.assertEqual(set(profile["facts"]), set(workspace.FIELDS))
        for fact in profile["facts"].values():
            self.assertIsNone(fact["value"])
            self.assertEqual(fact["status"], "unknown")
            self.assertEqual(fact["source"], {"kind": None, "ref": None})
        for month in range(1, 13):
            for part in ("originals", "derived", "proposals"):
                self.assertTrue((self.root / f"06_bookkeeping/2026/{month:02d}/{part}").is_dir())
        for name in ("tasks", "questions", "decisions"):
            self.assertEqual(self.load(f"00_admin/{name}.json"), [])
        self.assertEqual(self.load(workspace.DOCUMENTS)["documents"], [])
        self.assertEqual(self.load(workspace.MARKER)["mode"], "general")
        self.assertFalse((self.root / ".git").exists())
        if os.name == "posix":
            self.assertEqual(stat.S_IMODE(self.root.stat().st_mode), 0o700)
            self.assertEqual(stat.S_IMODE((self.root / workspace.PROFILE).stat().st_mode), 0o600)

    def test_init_persists_explicit_language_and_workflow_mode(self):
        target = self.base / "english-workspace"
        with redirect_stdout(io.StringIO()) as output:
            code = workspace.main(["init", "--root", str(target), "--year", "2026",
                                   "--language", "en", "--mode", "tax-consultant"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["mode"], "tax-consultant")
        status = workspace.workspace_status(target)
        self.assertEqual((status["language"], status["mode"]), ("en", "tax-consultant"))
        marker = json.loads((target / workspace.MARKER).read_text(encoding="utf-8"))
        self.assertEqual(marker["schema_version"], 1)
        self.assertEqual(marker["mode"], "tax-consultant")

    def test_configure_persists_preferences_and_history_without_changing_tax_facts(self):
        workspace.record_fact(self.root, self.record(field="vat_current_regime", value="Regelbesteuerung"))
        profile_before = (self.root / workspace.PROFILE).read_bytes()
        marker_before = self.load(workspace.MARKER)
        result = workspace.configure_workspace(self.root, language="en", mode="bookkeeping")
        marker_after = self.load(workspace.MARKER)
        self.assertEqual((marker_after["language"], marker_after["mode"]), ("en", "bookkeeping"))
        self.assertEqual(marker_after["workspace_id"], marker_before["workspace_id"])
        self.assertEqual(marker_after["created_at"], marker_before["created_at"])
        self.assertEqual(marker_after["initial_year"], marker_before["initial_year"])
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), profile_before)
        snapshot = self.load(f"09_audit/history/{result['history_id']}.json")
        self.assertEqual(snapshot["action"], "configure_workspace")
        self.assertEqual(snapshot["before"], marker_before)
        self.assertEqual(snapshot["after"], marker_after)
        event = self.load(workspace.EVENTS)[-1]
        self.assertEqual(event["action"], "workspace_configured")
        self.assertEqual(event["details"]["history_id"], result["history_id"])
        self.assertEqual(set(event["details"]["changed_fields"]), {"language", "mode"})
        status = workspace.workspace_status(self.root)
        self.assertEqual((status["language"], status["mode"]), ("en", "bookkeeping"))

    def test_configure_single_option_preserves_other_preference(self):
        workspace.configure_workspace(self.root, language="en", mode="bookkeeping")
        workspace.configure_workspace(self.root, mode="tax-consultant")
        status = workspace.workspace_status(self.root)
        self.assertEqual((status["language"], status["mode"]), ("en", "tax-consultant"))
        workspace.configure_workspace(self.root, language="ru")
        status = workspace.workspace_status(self.root)
        self.assertEqual((status["language"], status["mode"]), ("ru", "tax-consultant"))

    def test_legacy_marker_missing_mode_defaults_without_read_time_mutation(self):
        marker = self.load(workspace.MARKER)
        marker.pop("mode")
        marker["language"] = "de"
        path = self.root / workspace.MARKER
        path.write_text(json.dumps(marker), encoding="utf-8")
        marker_bytes = path.read_bytes()
        status = workspace.workspace_status(self.root)
        self.assertEqual((status["language"], status["mode"]), ("de", "general"))
        self.assertEqual(path.read_bytes(), marker_bytes)
        result = workspace.configure_workspace(self.root, mode="bookkeeping")
        self.assertEqual((result["language"], result["mode"]), ("de", "bookkeeping"))
        self.assertEqual(self.load(workspace.MARKER)["schema_version"], 1)
        history = self.load(f"09_audit/history/{result['history_id']}.json")
        self.assertNotIn("mode", history["before"])
        self.assertEqual(history["after"]["mode"], "bookkeeping")

    def test_configure_rejects_missing_or_invalid_options_without_changes(self):
        marker_before = (self.root / workspace.MARKER).read_bytes()
        profile_before = (self.root / workspace.PROFILE).read_bytes()
        events_before = (self.root / workspace.EVENTS).read_bytes()
        for kwargs in ({}, {"language": "fr"}, {"mode": "automatic-tax-filing"},
                       {"language": "en", "mode": "invalid"}):
            with self.subTest(options=kwargs):
                with self.assertRaises(workspace.WorkspaceError):
                    workspace.configure_workspace(self.root, **kwargs)
        self.assertEqual((self.root / workspace.MARKER).read_bytes(), marker_before)
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), profile_before)
        self.assertEqual((self.root / workspace.EVENTS).read_bytes(), events_before)
        self.assertEqual(list((self.root / "09_audit/history").iterdir()), [])
        target = self.base / "invalid-mode-workspace"
        with self.assertRaises(workspace.WorkspaceError):
            workspace.init_workspace(target, 2026, mode="invalid")
        self.assertFalse(target.exists())

    def test_configure_respects_lock_without_history_or_state_changes(self):
        marker_before = (self.root / workspace.MARKER).read_bytes()
        events_before = (self.root / workspace.EVENTS).read_bytes()
        lock = self.root / workspace.LOCK
        lock.write_text("another operation", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.configure_workspace(self.root, language="en", mode="bookkeeping")
        self.assertEqual(lock.read_text(), "another operation")
        self.assertEqual((self.root / workspace.MARKER).read_bytes(), marker_before)
        self.assertEqual((self.root / workspace.EVENTS).read_bytes(), events_before)
        self.assertEqual(list((self.root / "09_audit/history").iterdir()), [])

    def test_configure_unchanged_preferences_create_no_redundant_history(self):
        marker_before = (self.root / workspace.MARKER).read_bytes()
        events_before = (self.root / workspace.EVENTS).read_bytes()
        result = workspace.configure_workspace(self.root, language="ru", mode="general")
        self.assertEqual(result["status"], "unchanged")
        self.assertEqual((self.root / workspace.MARKER).read_bytes(), marker_before)
        self.assertEqual((self.root / workspace.EVENTS).read_bytes(), events_before)
        self.assertEqual(list((self.root / "09_audit/history").iterdir()), [])

    def test_configure_cli_requires_option_and_persists_selected_mode(self):
        with redirect_stderr(io.StringIO()):
            code = workspace.main(["configure", "--root", str(self.root)])
        self.assertEqual(code, 2)
        self.assertEqual(workspace.workspace_status(self.root)["mode"], "general")
        with redirect_stdout(io.StringIO()) as output:
            code = workspace.main(["configure", "--root", str(self.root), "--mode", "tax-consultant"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["mode"], "tax-consultant")
        self.assertEqual(workspace.workspace_status(self.root)["mode"], "tax-consultant")

    def test_init_never_overwrites_nonempty_directory(self):
        before = (self.root / workspace.PROFILE).read_bytes()
        with self.assertRaises(workspace.WorkspaceError):
            workspace.init_workspace(self.root, 2027)
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), before)
        occupied = self.base / "occupied"
        occupied.mkdir()
        sentinel = occupied / "keep.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.init_workspace(occupied, 2026)
        self.assertEqual(list(occupied.iterdir()), [sentinel])

    def test_init_rejects_git_worktree_and_skill_ancestry(self):
        for kind, marker in (("repo", ".git"), ("skill", "SKILL.md")):
            parent = self.base / kind
            parent.mkdir()
            (parent / marker).write_text("marker", encoding="utf-8")
            target = parent / "nested" / "data"
            with self.assertRaises(workspace.WorkspaceError):
                workspace.init_workspace(target, 2026)
            self.assertFalse(target.exists())
        normal = self.base / "normal-repo"
        (normal / ".git").mkdir(parents=True)
        (normal / ".git/HEAD").write_text("ref: refs/heads/main", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.init_workspace(normal / "data", 2026)
        bare = self.base / "bare"
        bare.mkdir()
        (bare / "HEAD").write_text("ref: refs/heads/main", encoding="utf-8")
        (bare / "objects").mkdir()
        (bare / "refs").mkdir()
        with self.assertRaises(workspace.WorkspaceError):
            workspace.init_workspace(bare / "data", 2026)

    def test_init_rejects_symlinked_parent(self):
        target = self.base / "real"
        target.mkdir()
        linked = self.base / "link"
        self._symlink(linked, target, True)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.init_workspace(linked / "data", 2026)
        self.assertEqual(list(target.iterdir()), [])

    def test_existing_workspace_made_git_repository_blocks_record_and_ingest(self):
        before = (self.root / workspace.PROFILE).read_bytes()
        registry_before = (self.root / workspace.DOCUMENTS).read_bytes()
        (self.root / ".git").mkdir()
        (self.root / ".git/HEAD").write_text("ref: refs/heads/main", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.record_fact(self.root, self.record())
        with self.assertRaises(workspace.WorkspaceError):
            workspace.ingest_document(self.root, self.source(), "2026-10")
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), before)
        self.assertEqual((self.root / workspace.DOCUMENTS).read_bytes(), registry_before)
        self.assertEqual(list((self.root / "06_bookkeeping/2026/10/originals").iterdir()), [])

    def test_record_keeps_before_after_history_and_evidence(self):
        first = workspace.record_fact(self.root, self.record())
        second = workspace.record_fact(self.root, self.record(status="needs_review", note="Check classification."))
        history = self.load(f"09_audit/history/{second['history_id']}.json")
        self.assertEqual(history["before"]["facts"]["legal_form"]["status"], "declared")
        self.assertEqual(history["after"]["facts"]["legal_form"]["status"], "needs_review")
        self.assertTrue((self.root / f"09_audit/history/{first['history_id']}.json").is_file())
        fact = self.load(workspace.PROFILE)["facts"]["legal_form"]
        self.assertEqual(fact["source"]["ref"], "intake-1")
        self.assertIsNotNone(fact["recorded_at"])
        self.assertEqual(len(self.load(workspace.EVENTS)), 3)

    def test_record_rejects_unknown_fields_missing_evidence_and_model_verification(self):
        before = (self.root / workspace.PROFILE).read_bytes()
        records = [self.record(field="password"), self.record(source={"kind": "user", "ref": ""}),
                   self.record(status="verified", source={"kind": "model", "ref": "confidence=.99"}),
                   self.record(effective_from="2026-02-30"), self.record(value=float("nan"))]
        for record in records:
            with self.subTest(record=record):
                with self.assertRaises(workspace.WorkspaceError):
                    workspace.record_fact(self.root, record)
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), before)
        self.assertEqual(list((self.root / "09_audit/history").iterdir()), [])

    def test_lock_prevents_mutation_and_is_not_removed_by_rejected_writer(self):
        before = (self.root / workspace.PROFILE).read_bytes()
        lock = self.root / workspace.LOCK
        lock.write_text("another operation", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.record_fact(self.root, self.record())
        self.assertEqual(lock.read_text(), "another operation")
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), before)

    def test_ingest_preserves_bytes_and_deduplicates_without_tax_verdict(self):
        content = b"<not-parsed><arbitrary-data/></not-parsed>\n"
        source = self.source("invoice.xml", content)
        first = workspace.ingest_document(self.root, source, "2026-10")
        second = workspace.ingest_document(self.root, source, "2026-11")
        self.assertEqual(first["document_id"], second["document_id"])
        self.assertEqual(second["status"], "existing_content")
        self.assertIn("not a tax duplicate", second["review_note"])
        documents = self.load(workspace.DOCUMENTS)["documents"]
        self.assertEqual(len(documents), 1)
        document = documents[0]
        self.assertEqual((self.root / document["path"]).read_bytes(), content)
        self.assertEqual(source.read_bytes(), content)
        self.assertEqual(document["status"], "imported")
        self.assertEqual(document["provider_state"], "unknown")
        self.assertEqual(document["period"], "2026-10")
        self.assertNotIn("tax_date", document)
        self.assertEqual(workspace.verify_workspace(self.root)["status"], "ok")

    def test_verify_detects_tamper_and_cli_returns_nonzero(self):
        workspace.ingest_document(self.root, self.source(), "2026-10")
        document = self.load(workspace.DOCUMENTS)["documents"][0]
        (self.root / document["path"]).write_bytes(b"altered")
        self.assertEqual(workspace.verify_workspace(self.root)["status"], "needs_review")
        with redirect_stdout(io.StringIO()):
            code = workspace.main(["verify", "--root", str(self.root)])
        self.assertEqual(code, 1)

    def test_reimport_does_not_conceal_or_overwrite_tampered_indexed_copy(self):
        source = self.source()
        workspace.ingest_document(self.root, source, "2026-10")
        document = self.load(workspace.DOCUMENTS)["documents"][0]
        saved = self.root / document["path"]
        saved.write_bytes(b"altered")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(saved.read_bytes(), b"altered")
        self.assertEqual(len(self.load(workspace.DOCUMENTS)["documents"]), 1)

    def test_verify_rejects_registry_path_escape(self):
        workspace.ingest_document(self.root, self.source(), "2026-10")
        registry = self.load(workspace.DOCUMENTS)
        registry["documents"][0]["path"] = "../../outside.pdf"
        (self.root / workspace.DOCUMENTS).write_text(json.dumps(registry), encoding="utf-8")
        result = workspace.verify_workspace(self.root)
        self.assertTrue(any("Parent-directory" in error["issue"] for error in result["errors"]))
        self.assertEqual(result["unindexed_originals"], 1)
        self.assertEqual(result["status"], "needs_review")

    def test_ingest_registry_write_failure_rolls_back_own_copy_and_can_retry(self):
        source = self.source()
        source_bytes = source.read_bytes()
        original_write = workspace._atomic_json

        def fail_registry(path, *args, **kwargs):
            if path == self.root / workspace.DOCUMENTS:
                raise OSError("Simulated registry write failure")
            return original_write(path, *args, **kwargs)

        with patch.object(workspace, "_atomic_json", side_effect=fail_registry):
            with self.assertRaises(OSError):
                workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(source.read_bytes(), source_bytes)
        self.assertEqual(list((self.root / "06_bookkeeping/2026/10/originals").iterdir()), [])
        self.assertEqual(self.load(workspace.DOCUMENTS)["documents"], [])
        self.assertEqual(workspace.ingest_document(self.root, source, "2026-10")["status"], "imported")
        self.assertEqual(workspace.verify_workspace(self.root)["status"], "ok")

    def test_failed_ingest_preserves_a_modified_copy_and_verify_flags_it(self):
        source = self.source()
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        target = self.root / f"06_bookkeeping/2026/10/originals/{digest}.pdf"
        original_write = workspace._atomic_json

        def fail_registry(path, *args, **kwargs):
            if path == self.root / workspace.DOCUMENTS:
                target.write_bytes(b"Changed by a separate operation")
                raise OSError("Simulated registry write failure")
            return original_write(path, *args, **kwargs)

        with patch.object(workspace, "_atomic_json", side_effect=fail_registry):
            with self.assertRaises(OSError):
                workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(target.read_bytes(), b"Changed by a separate operation")
        self.assertEqual(source.read_bytes(), b"synthetic-original\n")
        result = workspace.verify_workspace(self.root)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["unindexed_originals"], 1)

    def test_failed_ingest_does_not_delete_a_copy_after_registry_committed(self):
        source = self.source()
        original_write = workspace._atomic_json

        def fail_after_commit(path, *args, **kwargs):
            result = original_write(path, *args, **kwargs)
            if path == self.root / workspace.DOCUMENTS:
                raise OSError("Simulated error after registry replacement")
            return result

        with patch.object(workspace, "_atomic_json", side_effect=fail_after_commit):
            with self.assertRaises(OSError):
                workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(workspace.verify_workspace(self.root)["status"], "ok")
        self.assertEqual(workspace.ingest_document(self.root, source, "2026-10")["status"], "existing_content")

    def test_verify_flags_crash_orphan_without_following_originals_symlinks(self):
        original = self.root / "06_bookkeeping/2026/10/originals/orphan.pdf"
        original.write_bytes(b"Unindexed crash orphan")
        external = self.base / "outside-originals"
        external.mkdir()
        (external / "must-not-be-inventoried.pdf").write_bytes(b"External bytes")
        self._symlink(self.root / "06_bookkeeping/2026/10/originals/link", external, True)
        result = workspace.verify_workspace(self.root)
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["unindexed_originals"], 1)
        self.assertTrue(any(error.get("path", "").endswith("orphan.pdf") for error in result["errors"]))
        self.assertTrue(any("not followed" in error["issue"] for error in result["errors"]))
        self.assertNotIn("must-not-be-inventoried", json.dumps(result))
        self.assertEqual(original.read_bytes(), b"Unindexed crash orphan")

    def test_ingest_rejects_symlink_sources_destinations_and_unsupported_extensions(self):
        source = self.source()
        linked = self.base / "linked.pdf"
        self._symlink(linked, source)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.ingest_document(self.root, linked, "2026-10")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.ingest_document(self.root, self.source("key.pfx"), "2026-10")
        originals = self.root / "06_bookkeeping/2026/10/originals"
        originals.rmdir()
        outside = self.base / "outside"
        outside.mkdir()
        self._symlink(originals, outside, True)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual(self.load(workspace.DOCUMENTS)["documents"], [])

    def test_ingest_refuses_existing_unindexed_original(self):
        source = self.source()
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        target = self.root / f"06_bookkeeping/2026/10/originals/{digest}.pdf"
        target.write_bytes(b"preexisting-do-not-overwrite")
        with self.assertRaises(FileExistsError):
            workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(target.read_bytes(), b"preexisting-do-not-overwrite")
        self.assertEqual(self.load(workspace.DOCUMENTS)["documents"], [])

    def test_ingest_size_limit_prevents_copy(self):
        source = self.source("large.pdf")
        with source.open("wb") as stream:
            stream.truncate(workspace.MAX_BYTES + 1)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.ingest_document(self.root, source, "2026-10")
        self.assertEqual(self.load(workspace.DOCUMENTS)["documents"], [])

    def test_reconcile_supports_fee_groups_precise_decimals_and_multiple_currencies(self):
        bank, ledger = self.csvs("sale,2026-10-03,97.00,EUR\nsmall,2026-10-04,0.30,USD\n",
                                "revenue,sale,100.00,EUR\nfee,sale,-3.00,EUR\n"
                                "fraction-a,small,0.1,USD\nfraction-b,small,0.2,USD\n")
        before = (bank.read_bytes(), ledger.read_bytes())
        result = workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertEqual(result["status"], "matched")
        self.assertEqual(result["matched_groups"], 2)
        report = self.load(result["report"])
        self.assertEqual(set(report["totals_by_currency"]), {"EUR", "USD"})
        for values in report["totals_by_currency"].values():
            self.assertEqual(Decimal(values["difference"]), Decimal(0))
        self.assertEqual(report["sources"]["bank"]["sha256"], hashlib.sha256(before[0]).hexdigest())
        self.assertEqual((bank.read_bytes(), ledger.read_bytes()), before)
        self.assertNotEqual(report["status"], "posted")

    def test_reconcile_does_not_round_long_decimal_amounts(self):
        amount = "123456789012345678901234567890.123456789"
        bank, ledger = self.csvs(f"exact,2026-10-03,{amount},EUR\n", f"e,exact,{amount},EUR\n")
        result = workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertEqual(result["status"], "matched")

    def test_reconcile_empty_inputs_need_coverage_review(self):
        bank, ledger = self.csvs("", "")
        result = workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["coverage"], {"bank_rows": 0, "ledger_rows": 0, "matched_groups": 0})
        self.assertTrue(result["review_notes"])
        report = self.load(result["report"])
        self.assertEqual(report["coverage"], result["coverage"])
        self.assertEqual(report["status"], "needs_review")

    def test_reconcile_preserves_tiny_difference_beside_large_amount(self):
        large = "9" * 120
        tiny = "0." + "0" * 118 + "1"
        bank, ledger = self.csvs(f"exact,2026-10-03,{large},EUR\n",
                                f"large,exact,{large},EUR\ntiny,exact,{tiny},EUR\n")
        result = workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["matched_groups"], 0)
        report = self.load(result["report"])
        self.assertEqual(Decimal(report["differences"][0]["difference"]), Decimal(tiny).copy_negate())
        self.assertEqual(Decimal(report["totals_by_currency"]["EUR"]["difference"]), Decimal(tiny).copy_negate())

    def test_reconcile_flags_unmatched_unlinked_currency_mismatch_and_differences(self):
        bank, ledger = self.csvs("only-bank,2026-10-03,10,EUR\ndifference,2026-10-04,10,EUR\n"
                                "currency,2026-10-05,5,EUR\n",
                                "e1,difference,9,EUR\ne2,unknown,4,EUR\ne3,,2,USD\ne4,currency,5,USD\n")
        result = workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertEqual(result["status"], "needs_review")
        self.assertEqual(result["differences"], 1)
        self.assertEqual(result["unmatched_bank"], 2)
        self.assertEqual(result["unmatched_ledger"], 2)
        self.assertEqual(result["unlinked_ledger_entries"], 1)
        self.assertEqual(result["matched_groups"], 0)

    def test_reconcile_rejects_duplicates_bad_amounts_and_wrong_period_without_report(self):
        cases = [
            ("x,2026-10-01,1,EUR\nx,2026-10-02,1,EUR\n", "e,x,1,EUR\n"),
            ("x,2026-10-01,1,EUR\n", "e,x,1,EUR\ne,x,1,EUR\n"),
            ("x,2026-09-30,1,EUR\n", "e,x,1,EUR\n"),
        ]
        for amount in ("NaN", "Infinity", "-Infinity", "1e3", '"1,23"', "1.2.3"):
            cases.append((f"x,2026-10-01,{amount},EUR\n", "e,x,1,EUR\n"))
        for bank_text, ledger_text in cases:
            with self.subTest(bank=bank_text, ledger=ledger_text):
                bank, ledger = self.csvs(bank_text, ledger_text)
                with self.assertRaises(workspace.WorkspaceError):
                    workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertEqual(list((self.root / "07_exports").iterdir()), [])

    def test_reconcile_requires_private_input_paths(self):
        bank, ledger = self.csvs("x,2026-10-01,1,EUR\n", "e,x,1,EUR\n")
        external = self.base / "public-bank.csv"
        external.write_bytes(bank.read_bytes())
        with self.assertRaises(workspace.WorkspaceError):
            workspace.reconcile(self.root, external, ledger, "2026-10")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.reconcile(self.root, "../public-bank.csv", ledger, "2026-10")
        self.assertEqual(list((self.root / "07_exports").iterdir()), [])

    def test_reconciliation_reports_never_overwrite_previous_reports(self):
        bank, ledger = self.csvs("x,2026-10-01,1,EUR\n", "e,x,1,EUR\n")
        first = workspace.reconcile(self.root, bank, ledger, "2026-10")
        first_bytes = (self.root / first["report"]).read_bytes()
        second = workspace.reconcile(self.root, bank, ledger, "2026-10")
        self.assertNotEqual(first["report"], second["report"])
        self.assertEqual((self.root / first["report"]).read_bytes(), first_bytes)

    def test_corrupt_audit_log_blocks_mutation_before_profile_change(self):
        before = (self.root / workspace.PROFILE).read_bytes()
        (self.root / workspace.EVENTS).write_text("{}", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.record_fact(self.root, self.record())
        self.assertEqual((self.root / workspace.PROFILE).read_bytes(), before)

    def test_status_does_not_print_private_fact_values(self):
        workspace.record_fact(self.root, self.record(field="owner_name", value="Synthetic Private Name"))
        result = workspace.workspace_status(self.root)
        self.assertEqual(result["fact_status_counts"]["declared"], 1)
        self.assertNotIn("Synthetic Private Name", json.dumps(result))
        with redirect_stdout(io.StringIO()) as output:
            self.assertEqual(workspace.main(["status", "--root", str(self.root)]), 0)
        self.assertNotIn("Synthetic Private Name", output.getvalue())


if __name__ == "__main__":
    unittest.main()
