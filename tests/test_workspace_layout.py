"""The single private-workspace folder layout: mapping, intake, refusals and readable results."""
import json
import os
from pathlib import Path
from unittest.mock import patch
from pathlib import Path

from test_casework import CaseFixture
import test_casebank
import workspace as ws
from casefiles import accounting as ac, bank, folders, overview

NATIVE_MARK = "<!-- German Business Kit native overview v1 -->\n"
NAMES = {
    "en": {"guide": "START-HERE.md", "overview": "OVERVIEW.html", "inbox": "01 Inbox", "imported": "01 Inbox/Imported",
           "procedure": "03 Accounts/Procedure documentation", "documents": "02 Documents", "originals": "Originals",
           "visible": ["01 Inbox", "02 Documents", "03 Accounts", "04 Taxes", "05 Business"]},
    "ru": {"guide": "НАЧНИТЕ-ЗДЕСЬ.md", "overview": "ОБЗОР.html", "inbox": "01 Входящие", "imported": "01 Входящие/Импортировано",
           "procedure": "03 Учёт/Описание процессов", "documents": "02 Документы", "originals": "Оригиналы",
           "visible": ["01 Входящие", "02 Документы", "03 Учёт", "04 Налоги", "05 Бизнес"]},
    "de": {"guide": "HIER-STARTEN.md", "overview": "ÜBERSICHT.html", "inbox": "01 Eingang", "imported": "01 Eingang/Importiert",
           "procedure": "03 Buchhaltung/Verfahrensdokumentation", "documents": "02 Dokumente", "originals": "Originale",
           "visible": ["01 Eingang", "02 Dokumente", "03 Buchhaltung", "04 Steuern", "05 Unternehmen"]},
}


class StructureTests(CaseFixture):
    def test_start_creates_the_documented_folders_guide_and_procedure_draft(self):
        for language, names in NAMES.items():
            with self.subTest(language=language):
                root = self.base / ("start-" + language)
                ws.start_workspace(root, 2026, language)
                record = {"schema_version": 2, "language": language}
                self.assertEqual(json.loads((root / ws.LAYOUT).read_text()), record)
                self.assertEqual(ws._load(ws._inside(root, ws.MARKER))["folder_layout"], record)
                visible = sorted(p.name for p in root.iterdir() if p.is_dir() and not p.name.startswith("."))
                self.assertEqual(visible, names["visible"])
                self.assertFalse(any((root / name).exists() for name in ("00_admin", "06_bookkeeping", "09_audit")))
                guide = (root / names["guide"]).read_text(encoding="utf-8")
                for text in (names["overview"], names["imported"].split("/")[1], "2026-00007"):
                    self.assertIn(text, guide)
                drafts = list((root / names["procedure"]).glob("*.md"))
                self.assertEqual(len(drafts), 1)
                self.assertIn("§147 AO", drafts[0].read_text(encoding="utf-8"))
                self.assertEqual(ws.workspace_folders(root)["guide"], names["guide"])

    def test_mapping_is_one_to_one_and_reversible_in_every_language(self):
        for language, names in NAMES.items():
            with self.subTest(language=language):
                root = self.base / ("map-" + language)
                ws.start_workspace(root, 2026, language)
                paths = ws.workspace_folders(root)["paths"]
                self.assertEqual(paths["00_admin/overview.html"], names["overview"])
                self.assertEqual(paths["00_admin/inbox/imported"], names["imported"])
                self.assertEqual(paths["04_accounting/procedure"], names["procedure"])
                self.assertEqual(paths["04_accounting/register.json"], ".business-kit/admin/accounting-register.json")
                self.assertEqual(paths["00_admin/work"], ".business-kit/admin/work")
                self.assertEqual(len(set(paths.values())), len(paths))
                for logical, physical in paths.items():
                    self.assertEqual(ws._logical(root, root / physical), logical)
                self.assertEqual(ws._inside(root, "00_admin/work/fact.json"), root / ".business-kit/admin/work/fact.json")

    def test_language_change_keeps_physical_folders_and_originals(self):
        root = self.base / "ru"
        ws.start_workspace(root, 2026, "ru")
        source = root / "01 Входящие/Счёт.csv"
        source.write_text("amount,currency\n12.34,EUR\n", encoding="utf-8")
        imported = ws.ingest_document(root, source, "2026-10")
        stored = root / imported["path"]
        before = stored.read_bytes()
        ws.configure_workspace(root, language="de")
        ws.start_workspace(root, 2027, "en")
        self.assertEqual(stored.read_bytes(), before)
        self.assertFalse((root / "02 Dokumente").exists())
        self.assertEqual(ws.workspace_status(root)["folder_language"], "ru")
        self.assertEqual(ws.verify_workspace(root)["status"], "ok")
        for internal in (ws.DOCUMENTS, ".business-kit/admin/documents.json", ".workspace-layout.json"):
            with self.assertRaises(ws.WorkspaceError):
                ws._evidence_path(root, internal)

    def test_canonical_references_and_physical_paths_resolve_to_the_same_file(self):
        root = self.base / "de"
        ws.start_workspace(root, 2026, "de")
        path = ws._inside(root, "03_banking/statement.csv")
        self.assertEqual(path, root / "03 Buchhaltung/Bank/statement.csv")
        ws._write_exclusive(path, b"example")
        self.assertEqual(ws._inside(root, "03 Buchhaltung/Bank/statement.csv"), path)
        self.assertEqual(ws.verify_workspace(root)["status"], "ok")

    def test_earlier_preview_layouts_are_refused_without_changes(self):
        earlier = self.base / "earlier"
        (earlier / "00_admin").mkdir(parents=True)
        (earlier / "00_admin/workspace.json").write_text("{}")
        version_one = self.base / "version-one"
        (version_one / ".business-kit").mkdir(parents=True)
        (version_one / ws.LAYOUT).write_text('{"schema_version": 1, "language": "en"}')
        newer = self.base / "newer"
        newer.mkdir()
        (newer / ws.LAYOUT).write_text('{"schema_version": 3, "language": "en"}')
        for root, message in ((earlier, "earlier preview"), (version_one, "earlier preview"), (newer, "newer kit")):
            with self.subTest(root=root.name):
                before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
                for operation in (ws.workspace_status, ws.start_workspace, ws.verify_workspace):
                    with self.assertRaisesRegex(ws.WorkspaceError, message):
                        operation(root)
                self.assertEqual({p: p.read_bytes() for p in root.rglob("*") if p.is_file()}, before)

    def test_modified_layout_or_shadow_record_folders_fail_closed(self):
        descriptor = self.root / ws.LAYOUT
        original = descriptor.read_bytes()
        descriptor.write_text(json.dumps({"schema_version": 2, "language": "de"}))
        with self.assertRaises(ws.WorkspaceError):
            ws.workspace_status(self.root)
        descriptor.write_bytes(original)
        (self.root / "00_admin").mkdir()
        with self.assertRaises(ws.WorkspaceError):
            ws.workspace_status(self.root)

    def test_accounting_register_is_internal_and_not_evidence(self):
        config = ac.template("configuration")
        config.update(system="local", account_reference="sample", method="EÜR", reviewer="owner",
                      evidence_file=self.evidence())
        ac.configure(self.root, config)
        self.assertTrue((self.root / ".business-kit/admin/accounting-register.json").is_file())
        self.assertEqual(list((self.root / "03 Accounts/Records").iterdir()), [])
        with self.assertRaises(ws.WorkspaceError):
            ws._evidence_path(self.root, ".business-kit/admin/accounting-register.json")


class LookupCostTests(CaseFixture):
    """Windows pays per filesystem metadata call; layout reads must not repeat per record."""

    def test_evidence_check_finds_hardlinked_record_with_one_layout_lookup(self):
        root = self.base / "ru"
        ws.init_workspace(root, 2026, "ru")
        profile = ws._inside(root, ws.PROFILE)
        self.assertEqual(profile, root / ".business-kit/profile/business.json")
        alias = ws._inside(root, "08_correspondence/profile-copy.json")
        os.link(profile, alias)
        review = ws._inside(root, "08_correspondence/review.md")
        review.write_text("Synthetic review.", encoding="utf-8")
        lookups = []
        original = ws._layout

        def counted(location):
            lookups.append(location)
            return original(location)
        with patch.object(ws, "_layout", counted):
            with self.assertRaises(ws.WorkspaceError):
                ws._evidence_path(root, "05 Бизнес/Переписка/profile-copy.json")
            refused = len(lookups)
            self.assertEqual(ws._evidence_path(root, "08_correspondence/review.md"), review)
        # Each lookup rereads layout files; it must not repeat per protected record.
        self.assertLessEqual(refused, 3)

    def test_shipped_folder_catalog_is_not_reread_for_each_path(self):
        root = self.base / "de"
        ws.init_workspace(root, 2026, "de")
        reads = []
        original = ws._read_regular

        def counted(path, *args):
            reads.append(Path(path).name)
            return original(path, *args)
        with patch.object(ws, "_read_regular", counted):
            for _ in range(5):
                self.assertEqual(ws._path(root, "03_banking"), root / "03 Buchhaltung/Bank")
        # The workspace's own layout record is still checked on every lookup.
        self.assertEqual(reads.count(ws.LAYOUT), 5)
        self.assertLessEqual(reads.count("folder-layouts.json"), 1)


class NumberedOriginalTests(CaseFixture):
    def ingest(self, name, data, period):
        source = self.base / "sources" / name
        source.parent.mkdir(exist_ok=True)
        source.write_bytes(data)
        return ws.ingest_document(self.root, source, period)

    def test_originals_get_a_running_number_per_year_and_a_readable_name(self):
        first = self.ingest("Rechnung Oktober.pdf", b"first", "2026-10")
        second = self.ingest("receipt.csv", b"second", "2026-11")
        third = self.ingest("statement.pdf", b"third", "2027-01")
        self.assertEqual(first["path"], "02 Documents/2026/10/Originals/2026-00001_Rechnung Oktober.pdf")
        self.assertEqual(second["path"], "02 Documents/2026/11/Originals/2026-00002_receipt.csv")
        self.assertEqual(third["path"], "02 Documents/2027/01/Originals/2027-00001_statement.pdf")
        numbers = [d["document_number"] for d in ws._documents(self.root)["documents"]]
        self.assertEqual(numbers, ["2026-00001", "2026-00002", "2027-00001"])
        again = self.ingest("copy of receipt.csv", b"second", "2026-12")
        self.assertEqual(again["status"], "existing_content")
        self.assertEqual(len(ws._documents(self.root)["documents"]), 3)
        self.assertEqual(ws.verify_workspace(self.root)["status"], "ok")

    def test_unsafe_long_or_empty_names_become_portable(self):
        cases = (('bad<>:"|?*name.pdf', "2026-00001_bad-------name.pdf"),
                 ("x" * 120 + ".pdf", "2026-00002_" + "x" * 60 + ".pdf"),
                 ("***.pdf", "2026-00003_document.pdf"))
        for number, (name, expected) in enumerate(cases):
            with self.subTest(name=name):
                result = self.ingest(name, str(number).encode(), "2026-10")
                self.assertEqual(result["path"].rsplit("/", 1)[1], expected)
        self.assertEqual(ws.verify_workspace(self.root)["status"], "ok")

    def test_verify_flags_renamed_or_hash_named_originals(self):
        result = self.ingest("invoice.pdf", b"synthetic", "2026-10")
        stored = self.root / result["path"]
        renamed = stored.with_name("2026-00009_invoice.pdf")
        stored.rename(renamed)
        self.assertEqual(ws.verify_workspace(self.root)["status"], "needs_review")
        registry = ws._documents(self.root)
        document = registry["documents"][0]
        hashed = renamed.with_name(document["sha256"] + ".pdf")
        renamed.rename(hashed)
        document["path"] = ws._logical(self.root, hashed)
        ws._atomic_json(ws._inside(self.root, ws.DOCUMENTS), registry, replace=True)
        self.assertEqual(ws.verify_workspace(self.root)["status"], "needs_review")


class ManagedInboxTests(CaseFixture):
    def drop(self, name, data):
        path = self.root / "01 Inbox" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_the_inbox_can_be_previewed_and_already_imported_files_are_skipped(self):
        self.drop("receipt.pdf", b"new")
        self.drop("Imported/2026-10/old.pdf", b"old")
        result = folders.scan(self.root, self.root / "01 Inbox")
        rows = {row["path"]: row for row in json.loads((self.root / result["path"]).read_text())["entries"]}
        self.assertEqual(rows["receipt.pdf"]["status"], "candidate")
        self.assertEqual(rows["Imported"]["reason"], "already_imported")
        self.assertNotIn("Imported/2026-10/old.pdf", rows)
        for internal in (self.root, self.root / ".business-kit", self.root / "02 Documents"):
            with self.subTest(source=internal.name), self.assertRaises(ws.WorkspaceError):
                folders.scan(self.root, internal)

    def test_an_import_from_the_inbox_files_the_source_without_overwriting(self):
        first = ws.ingest_document(self.root, self.drop("Rechnung.pdf", b"one"), "2026-10")
        self.assertEqual(first["source_moved_to"], "01 Inbox/Imported/2026-10/Rechnung.pdf")
        self.assertFalse((self.root / "01 Inbox/Rechnung.pdf").exists())
        self.assertEqual((self.root / first["source_moved_to"]).read_bytes(), b"one")
        second = ws.ingest_document(self.root, self.drop("Rechnung.pdf", b"two"), "2026-10")
        self.assertEqual(second["source_moved_to"], "01 Inbox/Imported/2026-10/Rechnung (2).pdf")
        again = ws.ingest_document(self.root, self.drop("copy.pdf", b"one"), "2026-11")
        self.assertEqual((again["status"], again["source_moved_to"]), ("existing_content", "01 Inbox/Imported/2026-11/copy.pdf"))
        outside = self.base / "outside.pdf"
        outside.write_bytes(b"three")
        self.assertIsNone(ws.ingest_document(self.root, outside, "2026-10")["source_moved_to"])
        self.assertTrue(outside.exists())
        self.assertEqual(ws.verify_workspace(self.root)["status"], "ok")


class RootOverviewTests(CaseFixture):
    def test_overview_page_is_at_the_root_and_details_stay_internal(self):
        result = overview.generate(self.root, "2026-10", language="en")
        self.assertEqual(result["html_path"], "OVERVIEW.html")
        self.assertTrue(result["markdown_path"].startswith(".business-kit/admin/"))
        self.assertTrue(result["json_path"].startswith(".business-kit/admin/"))
        self.assertTrue((self.root / "OVERVIEW.html").read_text(encoding="utf-8").startswith(overview.MARK))
        overview.generate(self.root, "2026-10", language="en")
        self.assertEqual([p.name for p in self.root.iterdir() if p.name.endswith(".tmp")], [])

    def test_native_page_is_refreshed_but_a_user_file_is_preserved(self):
        page = self.root / "OVERVIEW.html"
        page.write_text(NATIVE_MARK + "<p>native</p>", encoding="utf-8")
        overview.generate(self.root, "2026-10", language="en")
        self.assertTrue(page.read_text(encoding="utf-8").startswith(overview.MARK))
        page.write_text("USER OWNED FILE", encoding="utf-8")
        with self.assertRaises(ws.WorkspaceError):
            overview.generate(self.root, "2026-10", language="en")
        self.assertEqual(page.read_text(encoding="utf-8"), "USER OWNED FILE")


class BankYearFolderTests(CaseFixture):
    mapping = test_casebank.BankMappingTests.mapping

    def test_normalized_statement_is_saved_under_its_period_year(self):
        doc = self.receive("bank.csv", "ID;Buchungstag;Betrag;Text\n1;02.10.2026;12,00;Synthetic sale\n".encode(), "bank_statement")
        preview = bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")
        approved = bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        self.assertTrue(approved["csv_path"].startswith("03 Accounts/Bank/2026/normalized/"), approved["csv_path"])
        self.assertTrue((self.root / approved["csv_path"]).is_file())


if __name__ == "__main__":
    import unittest
    unittest.main()
