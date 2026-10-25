"""Mixed-folder previews preserve sources and expose incomplete coverage."""
import json
import os
from contextlib import contextmanager
from types import SimpleNamespace
from unittest import mock
from pathlib import Path
import subprocess
import sys
import unittest

from test_casework import CaseFixture, SCRIPTS
from casefiles import folders
import workspace as ws


class FolderIntakeTests(CaseFixture):
    def source_folder(self):
        folder = self.base / "existing"
        folder.mkdir()
        return folder

    def report(self, source, **options):
        result = folders.scan(self.root, source, **options)
        return json.loads((self.root / result["path"]).read_text())

    def test_mixed_folder_preview_preserves_source_and_does_not_import(self):
        source = self.source_folder()
        (source / "invoices").mkdir()
        (source / "invoices/invoice.pdf").write_bytes(b"Synthetic PDF bytes")
        (source / "statement.csv").write_bytes(b"Synthetic CSV bytes")
        (source / "mail.eml").write_bytes(b"Synthetic original email")
        (source / "legacy.zip").write_bytes(b"Synthetic archive; never unpack")
        (source / "certificate.pfx").write_bytes(b"synthetic-protected-content")
        (source / ".hidden").mkdir()
        (source / ".hidden/private.pdf").write_bytes(b"do not visit")
        before = {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()}
        report = self.report(source)
        entries = {row["path"]: row for row in report["entries"]}
        self.assertEqual({p for p, row in entries.items() if row["status"] == "candidate"}, {"invoices/invoice.pdf", "statement.csv"})
        self.assertEqual(entries["mail.eml"]["reason"], "unsupported_format")
        self.assertEqual(entries["certificate.pfx"]["reason"], "credential_or_key")
        self.assertNotIn(".hidden/private.pdf", entries)
        self.assertEqual(before, {p.relative_to(source): p.read_bytes() for p in source.rglob("*") if p.is_file()})
        self.assertEqual(ws._documents(self.root)["documents"], [])
        self.assertNotIn("synthetic-protected-content", json.dumps(report))

    def test_symlinks_and_nested_workspaces_are_not_followed(self):
        source = self.source_folder()
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "private.pdf").write_bytes(b"Synthetic private")
        try:
            (source / "alias").symlink_to(outside, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable")
        ws.init_workspace(source / "old-workspace", 2026, "en")
        report = self.report(source)
        entries = {row["path"]: row for row in report["entries"]}
        self.assertEqual(entries["alias"]["reason"], "link_or_reparse_point")
        self.assertEqual(entries["old-workspace"]["reason"], "existing_workspace")
        self.assertFalse(any("/" in path for path in entries))

    def test_limits_and_large_files_are_explicit_not_false_complete(self):
        source = self.source_folder()
        for number in range(4):
            (source / f"{number}.pdf").write_bytes(b"Synthetic")
        report = self.report(source, max_entries=2)
        self.assertFalse(report["traversal_complete"])
        self.assertEqual(len(report["entries"]), 2)
        self.assertIn("entry_limit", report["warnings"])
        deep = source / "deep"
        deep.mkdir()
        (deep / "child.pdf").write_bytes(b"Synthetic")
        report = self.report(source, max_depth=0)
        self.assertFalse(report["traversal_complete"])
        self.assertIn("depth_limit", report["warnings"])
        with (source / "big.pdf").open("wb") as stream:
            stream.truncate(ws.MAX_BYTES + 1)
        report = self.report(source)
        self.assertEqual(next(row for row in report["entries"] if row["path"] == "big.pdf")["reason"], "file_too_large")

    def test_native_hidden_flags_exclude_files_and_directory_subtrees(self):
        source = self.source_folder()
        (source / "hidden.pdf").write_bytes(b"Synthetic hidden content")
        (source / "hidden-folder").mkdir()
        (source / "hidden-folder/inside.pdf").write_bytes(b"Never enumerate")
        original_scandir = os.scandir
        for flag in ({"st_file_attributes": 2}, {"st_flags": 0x8000}):
            @contextmanager
            def native_hidden(path):
                with original_scandir(path) as children:
                    wrapped = []
                    for child in children:
                        info = child.stat(follow_symlinks=False)
                        metadata = SimpleNamespace(st_mode=info.st_mode, st_size=info.st_size,
                                                   st_mtime_ns=info.st_mtime_ns, **flag)
                        wrapped.append(SimpleNamespace(name=child.name, path=child.path,
                                                       stat=lambda follow_symlinks=False, value=metadata: value))
                    yield iter(wrapped)
            with self.subTest(flag=flag), mock.patch.object(folders.os, "scandir", native_hidden):
                report = self.report(source)
            self.assertEqual(report["counts"]["candidate"], 0)
            self.assertEqual(len(report["entries"]), 2)
            self.assertTrue(all(row["reason"] == "hidden_entry" for row in report["entries"]))

    def test_workspace_overlap_and_existing_workspace_source_are_rejected(self):
        for source in (self.root, self.root / "00_admin", self.base):
            with self.subTest(source=source), self.assertRaises(ws.WorkspaceError):
                self.report(source)
        other = self.base / "other-workspace"
        ws.init_workspace(other, 2026, "en")
        with self.assertRaises(ws.WorkspaceError):
            self.report(other)

    def test_cli_saves_private_preview_and_returns_no_import_claim(self):
        source = self.source_folder()
        (source / "invoice.pdf").write_bytes(b"Synthetic")
        result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "desk.py"), "scan-folder", "--root", str(self.root), "--source", str(source)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "preview")
        self.assertEqual(payload["counts"]["candidate"], 1)
        self.assertTrue((self.root / payload["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
