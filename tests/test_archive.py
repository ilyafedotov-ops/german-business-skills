import hashlib
import json
from pathlib import Path
import unittest

from test_casework import CaseFixture
import workspace as ws
from casefiles import documents, archive, overview, storage


class ArchiveTests(CaseFixture):
    def test_mixed_intake_resume_and_archive_preserve_review_gaps_and_verify_bytes(self):
        invoice = self.receive()
        self.receive("letter.pdf", b"Synthetic deadline letter", "authority_letter")
        ws.save_entry(self.root, "tasks", {"schema_version": 1, "id": "task-1", "title": "Inspect authority request",
            "owner": "owner", "status": "pending", "due_date": "2026-10-24", "deadline_source": "Synthetic letter; legal deadline unconfirmed"})
        original_state = (self.root / storage.STATE).read_bytes()
        rendered = overview.generate(self.root, "2026-10", as_of="2026-10-25")
        self.assertEqual((self.root / storage.STATE).read_bytes(), original_state)
        self.assertEqual(rendered["counts"]["documents"], 2)
        self.assertEqual(rendered["counts"]["overdue_tasks"], 1)
        self.assertTrue((self.root / "START-HERE.md").exists())
        self.assertEqual(ws.start_workspace(self.root, 2026, "en")["action"], "resumed")
        result = archive.build(self.root, "2026-10", as_of="2026-10-25")
        self.assertEqual(result["integrity"], "verified")
        self.assertEqual(result["readiness"], "prepared_with_open_items")
        manifest = json.loads((self.root / result["path"] / "manifest.json").read_text())
        self.assertEqual(len(manifest["included_document_ids"]), 2)
        self.assertTrue(any(item["code"] == "document_review_open" for item in manifest["open_items"]))
        self.assertEqual(archive.verify(self.root / result["zip_path"])["status"], "verified")
        first = next(item for item in manifest["files"] if item["role"] == "original")
        (self.root / result["path"] / first["path"]).write_bytes(b"corrupt")
        self.assertEqual(archive.verify(self.root / result["path"])["status"], "failed")

    def test_bundle_selection_includes_related_originals_and_lists_exclusions(self):
        current = self.receive()
        external = self.base / "previous.pdf"
        external.write_bytes(b"Synthetic earlier original")
        earlier = documents.receive(self.root, external, "2026-09", "2026-09-10", "invoice")
        unrelated = self.base / "unrelated.pdf"
        unrelated.write_bytes(b"Synthetic unrelated material")
        excluded = documents.receive(self.root, unrelated, "2026-09", "2026-09-12", "other")
        record = documents.get(self.root, current["document_id"])
        record["relations"] = [{"relation": "corrects", "document_id": earlier["document_id"]}]
        documents.save(self.root, record, current["sha256"])
        built = archive.build(self.root, "2026-10", as_of="2026-10-25")
        manifest = json.loads((self.root / built["path"] / "manifest.json").read_text())
        self.assertEqual(set(manifest["included_document_ids"]), {current["document_id"], earlier["document_id"]})
        self.assertEqual(manifest["excluded_documents"][0]["document_id"], excluded["document_id"])
        paths = [item["path"] for item in manifest["files"]]
        self.assertFalse(any("business.json" in path or "runtime.json" in path for path in paths))

    def test_identical_inputs_build_identical_zip_bytes_and_unlisted_files_fail_verification(self):
        self.receive()
        one = archive.build(self.root, "2026-10", as_of="2026-10-25")
        two = archive.build(self.root, "2026-10", as_of="2026-10-25")
        self.assertNotEqual(one["path"], two["path"])
        self.assertEqual((self.root / one["zip_path"]).read_bytes(), (self.root / two["zip_path"]).read_bytes())
        (self.root / one["path"] / "unlisted.txt").write_text("extra")
        self.assertEqual(archive.verify(self.root / one["path"])["status"], "failed")

    def test_tampered_original_or_unsafe_manifest_stops_export_or_verification(self):
        received = self.receive()
        original = documents.original(self.root, received["document_id"])
        (self.root / original["path"]).write_bytes(b"changed")
        with self.assertRaises(ws.WorkspaceError):
            archive.build(self.root, "2026-10", as_of="2026-10-25")
        malicious = self.base / "malicious"
        malicious.mkdir()
        (malicious / "manifest.json").write_text(json.dumps({"schema_version": 1, "files": [
            {"path": "../outside.txt", "sha256": "0" * 64, "size_bytes": 0, "role": "original"}]}))
        with self.assertRaises(ws.WorkspaceError):
            archive.verify(malicious)

    def test_linked_task_cannot_copy_excluded_or_unselected_original_as_evidence(self):
        current = self.receive("contract.pdf", b"Synthetic selected contract", "contract")
        private = self.receive("private.pdf", b"DO-NOT-ARCHIVE-PRIVATE-EVIDENCE", "other")
        original = documents.original(self.root, private["document_id"])
        ws.save_entry(self.root, "tasks", {"schema_version": 1, "id": "t1", "title": "Review contract",
            "owner": "user", "status": "pending", "evidence_file": original["path"]})
        record = documents.get(self.root, current["document_id"])
        record["links"]["task_ids"] = ["t1"]
        documents.save(self.root, record, current["sha256"])
        record = documents.get(self.root, private["document_id"])
        record.update(review_status="excluded", reviewer="user", review_note="Private material")
        saved = documents.save(self.root, record, private["sha256"])
        with self.assertRaisesRegex(ws.WorkspaceError, "excluded|unselected"):
            archive.build(self.root, "2026-10", as_of="2026-10-25")
        record.update(review_status="reviewed", periods=["2026-09"], review_note="Outside this archive")
        documents.save(self.root, record, saved["sha256"])
        with self.assertRaisesRegex(ws.WorkspaceError, "excluded|unselected"):
            archive.build(self.root, "2026-10", as_of="2026-10-25")

    def test_overview_escapes_document_text_and_reports_empty_or_corrupt_state(self):
        empty = overview.generate(self.root, "2026-10", as_of="2026-10-25", language="ru")
        self.assertEqual(empty["counts"]["documents"], 0)
        self.assertIsNone(empty["counts"]["unmatched_items"])
        self.assertIn("Не оценено", (self.root / empty["html_path"]).read_text())
        received = self.receive()
        record = documents.get(self.root, received["document_id"])
        record["title"] = '<script>alert("synthetic")</script>'
        documents.save(self.root, record, received["sha256"])
        result = overview.generate(self.root, "2026-10", as_of="2026-10-25")
        html = (self.root / result["html_path"]).read_text()
        self.assertIn("&lt;script&gt;", html)
        self.assertNotIn('<script>alert', html)
        self.assertIn('Content-Security-Policy', html)
        (self.root / storage.STATE).write_text('{"schema_version":99}')
        broken = overview.generate(self.root, "2026-10", as_of="2026-10-25")
        self.assertEqual(broken["health"], "needs_review")
        self.assertTrue(broken["errors"])


if __name__ == "__main__":
    unittest.main()
