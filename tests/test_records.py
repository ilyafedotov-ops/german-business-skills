"""Shared register writes must preserve evidence and reject stale updates."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts/workspace.py"
SPEC = importlib.util.spec_from_file_location("records_workspace", SCRIPT)
workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workspace)


class RegisterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "private"
        workspace.init_workspace(self.root, 2026, "en")

    def task(self, **changes):
        return dict({"schema_version": 1, "id": "task-1", "title": "Inspect synthetic evidence",
                     "owner": "user", "status": "pending", "depends_on": []}, **changes)

    def test_task_completion_requires_evidence_and_preserves_other_entries(self):
        result = workspace.save_entry(self.root, "tasks", self.task())
        workspace.save_entry(self.root, "tasks", self.task(id="task-2"))
        completed = self.task(status="completed")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", completed, result["sha256"])
        (self.root / "00_admin/evidence.md").write_text("Synthetic inspected result", encoding="utf-8")
        completed["evidence_file"] = "00_admin/evidence.md"
        saved = workspace.save_entry(self.root, "tasks", completed, result["sha256"])
        records = json.loads((self.root / "00_admin/tasks.json").read_text())
        self.assertEqual([r["status"] for r in records], ["completed", "pending"])
        self.assertTrue(records[0]["evidence_sha256"])
        self.assertTrue((self.root / f"09_audit/history/{saved['history_id']}.json").exists())

    def test_update_requires_exact_previous_version(self):
        result = workspace.save_entry(self.root, "tasks", self.task())
        workspace.save_entry(self.root, "tasks", self.task(status="in_progress"), result["sha256"])
        before = (self.root / "00_admin/tasks.json").read_bytes()
        for expected in (None, result["sha256"]):
            with self.assertRaises(workspace.WorkspaceError):
                workspace.save_entry(self.root, "tasks", self.task(status="blocked"), expected)
        self.assertEqual((self.root / "00_admin/tasks.json").read_bytes(), before)

    def test_new_approved_decision_and_completion_without_dependencies_are_rejected(self):
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "decisions", self.task(status="approved", reviewer="user"))
        first = workspace.save_entry(self.root, "tasks", self.task())
        second = workspace.save_entry(self.root, "tasks", self.task(id="task-2", depends_on=["task-1"]))
        (self.root / "00_admin/result.md").write_text("Synthetic result", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task(id="task-2", status="completed", depends_on=["task-1"], evidence_file="00_admin/result.md"), second["sha256"])

    def test_deadline_needs_source_and_terminal_entries_cannot_be_reopened(self):
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task(due_date="2026-11-01"))
        first = workspace.save_entry(self.root, "tasks", self.task())
        second = workspace.save_entry(self.root, "tasks", self.task(status="cancelled"), first["sha256"])
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task(), second["sha256"])

    def test_decision_requires_reviewer_and_evidence_before_approval(self):
        proposed = self.task(status="proposed")
        first = workspace.save_entry(self.root, "decisions", proposed)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "decisions", dict(proposed, status="approved"), first["sha256"])
        (self.root / "00_admin/decision.md").write_text("Synthetic reviewer decision", encoding="utf-8")
        saved = workspace.save_entry(self.root, "decisions", dict(proposed, status="approved", reviewer="user", evidence_file="00_admin/decision.md"), first["sha256"])
        summary = workspace.entry_status(self.root, "decisions", "task-1")
        self.assertEqual(summary["sha256"], saved["sha256"])
        self.assertEqual(summary["status"], "approved")
        self.assertNotIn("title", summary)

    @patch.object(workspace, "LOCK_WAIT_SECONDS", 0)  # Refusal, not the wait, is under test.
    def test_active_lock_and_unknown_record_fields_do_not_write(self):
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task(automatic_submission=True))
        lock = self.root / workspace.LOCK
        lock.write_text("active", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task())
        self.assertEqual(json.loads((self.root / "00_admin/tasks.json").read_text()), [])
        self.assertEqual(lock.read_text(), "active")

    def test_legacy_untyped_register_is_reported_without_rewriting(self):
        path = self.root / "00_admin/tasks.json"
        path.write_text('[{"old": "untyped"}]', encoding="utf-8")
        before = path.read_bytes()
        status = workspace.workspace_status(self.root)
        self.assertIn("tasks_invalid", status["issues"])
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task())
        self.assertEqual(path.read_bytes(), before)

    def test_changed_evidence_allows_inspection_and_linked_correction(self):
        evidence = self.root / "00_admin/result.md"
        evidence.write_text("First result", encoding="utf-8")
        original = workspace.save_entry(self.root, "tasks", self.task(evidence_file="00_admin/result.md"))
        evidence.write_text("Changed result", encoding="utf-8")
        summary = workspace.entry_status(self.root, "tasks", "task-1")
        self.assertEqual(summary["sha256"], original["sha256"])
        self.assertEqual(summary["evidence_status"], "needs_review")
        workspace.save_entry(self.root, "tasks", self.task(id="task-2", supersedes="task-1"))
        self.assertIn("tasks_invalid", workspace.workspace_status(self.root)["issues"])

    def test_mutable_administrative_files_cannot_be_used_as_evidence(self):
        for name in (workspace.PROFILE, workspace.EVENTS, "00_admin/tasks.json", workspace.RUNTIME):
            with self.subTest(name=name):
                with self.assertRaises(workspace.WorkspaceError):
                    workspace.save_entry(self.root, "tasks", self.task(evidence_file=name))
        self.assertEqual(json.loads((self.root / "00_admin/tasks.json").read_text()), [])

    def test_superseding_decision_requires_approved_replacement_and_preserves_old_review(self):
        evidence = self.root / "00_admin/result.md"
        evidence.write_text("Synthetic decision", encoding="utf-8")
        first = workspace.save_entry(self.root, "decisions", self.task(status="proposed"))
        approved = self.task(status="approved", reviewer="owner", evidence_file="00_admin/result.md")
        old = workspace.save_entry(self.root, "decisions", approved, first["sha256"])
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "decisions", dict(approved, status="superseded", superseded_by="missing"), old["sha256"])
        replacement = self.task(id="decision-2", status="proposed", supersedes="task-1")
        new = workspace.save_entry(self.root, "decisions", replacement)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "decisions", dict(approved, status="superseded", superseded_by="decision-2"), old["sha256"])
        workspace.save_entry(self.root, "decisions", dict(replacement, status="approved", reviewer="owner", evidence_file="00_admin/result.md"), new["sha256"])
        workspace.save_entry(self.root, "decisions", dict(approved, status="superseded", superseded_by="decision-2"), old["sha256"])
        self.assertEqual(workspace.entry_status(self.root, "decisions", "task-1")["status"], "superseded")

    def test_status_detects_missing_dependencies(self):
        workspace.save_entry(self.root, "tasks", self.task())
        path = self.root / "00_admin/tasks.json"
        entries = json.loads(path.read_text())
        entries[0]["depends_on"] = ["missing"]
        path.write_text(json.dumps(entries), encoding="utf-8")
        self.assertIn("tasks_invalid", workspace.workspace_status(self.root)["issues"])

    def test_mutable_evidence_alias_is_rejected_on_case_insensitive_filesystem(self):
        alias = self.root / "00_ADMIN/TASKS.JSON"
        if not alias.exists():
            self.skipTest("Filesystem is case-sensitive")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "tasks", self.task(evidence_file="00_ADMIN/TASKS.JSON"))

    def test_replacement_with_changed_evidence_cannot_supersede_reviewed_decision(self):
        for name in ("old.md", "new.md"):
            (self.root / "00_admin" / name).write_text(name, encoding="utf-8")
        first = workspace.save_entry(self.root, "decisions", self.task(status="proposed"))
        approved = self.task(status="approved", reviewer="owner", evidence_file="00_admin/old.md")
        old = workspace.save_entry(self.root, "decisions", approved, first["sha256"])
        replacement = self.task(id="decision-2", status="proposed", supersedes="task-1")
        new = workspace.save_entry(self.root, "decisions", replacement)
        workspace.save_entry(self.root, "decisions", dict(replacement, status="approved", reviewer="owner", evidence_file="00_admin/new.md"), new["sha256"])
        (self.root / "00_admin/new.md").write_text("changed", encoding="utf-8")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "decisions", dict(approved, status="superseded", superseded_by="decision-2"), old["sha256"])

    def test_supersedes_links_cannot_form_cycle(self):
        first = workspace.save_entry(self.root, "decisions", self.task(status="proposed"))
        workspace.save_entry(self.root, "decisions", self.task(id="decision-2", status="proposed", supersedes="task-1"))
        with self.assertRaises(workspace.WorkspaceError):
            workspace.save_entry(self.root, "decisions", self.task(status="proposed", supersedes="decision-2"), first["sha256"])


if __name__ == "__main__":
    unittest.main()
