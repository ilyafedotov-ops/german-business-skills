"""Opt-in folder layout v2: versioned mapping, internal register, root overview and year folders."""
from datetime import date
import json
from pathlib import Path

from test_casework import CaseFixture
import test_casebank
import test_payment_followup
import workspace as ws
from casefiles import accounting as ac, bank, folders, invoicing as inv, overview

NATIVE_MARK = "<!-- German Business Kit native overview v1 -->\n"
V2_NAMES = {
    "en": ("OVERVIEW.html", "03 Accounts/Procedure documentation"),
    "ru": ("ОБЗОР.html", "03 Учёт/Описание процессов"),
    "de": ("ÜBERSICHT.html", "03 Buchhaltung/Verfahrensdokumentation"),
}


class V2Fixture(CaseFixture):
    LAYOUT = "v2"


class LayoutVersionTests(V2Fixture):
    def test_v2_is_the_default_and_records_its_version(self):
        record = {"schema_version": 2, "language": "en"}
        self.assertEqual(json.loads((self.root / ws.LAYOUT).read_text()), record)
        self.assertEqual(ws._load(ws._inside(self.root, ws.MARKER))["folder_layout"], record)
        self.assertEqual(ws.workspace_status(self.root)["folder_layout_version"], 2)
        default = self.base / "default"
        ws.start_workspace(default, 2026, "en")
        self.assertEqual(ws.workspace_status(default)["folder_layout_version"], 2)
        cli = self.base / "cli"
        self.assertEqual(ws.main(["start", "--root", str(cli), "--year", "2026"]), 0)
        self.assertEqual(ws.workspace_status(cli)["folder_layout_version"], 2)
        earlier = self.base / "earlier"
        ws.start_workspace(earlier, 2026, "en", layout="localized")
        self.assertEqual(ws.workspace_status(earlier)["folder_layout_version"], 1)
        self.assertNotIn("00_admin/overview.html", ws.workspace_folders(earlier)["paths"])
        legacy = self.base / "legacy"
        ws.init_workspace(legacy, 2026, "en")
        self.assertIsNone(ws.workspace_status(legacy)["folder_layout_version"])

    def test_start_guide_explains_the_v2_folders_only_in_v2(self):
        for language, overview_name in (("en", "OVERVIEW.html"), ("ru", "ОБЗОР.html"), ("de", "ÜBERSICHT.html")):
            with self.subTest(language=language):
                v2, v1 = self.base / ("guide-v2-" + language), self.base / ("guide-v1-" + language)
                ws.start_workspace(v2, 2026, language)
                ws.start_workspace(v1, 2026, language, layout="localized")
                guide = ws.workspace_folders(v2)["guide"]
                self.assertIn(overview_name, (v2 / guide).read_text(encoding="utf-8"))
                self.assertNotIn(overview_name, (v1 / guide).read_text(encoding="utf-8"))
        demo = self.base / "demo"
        result = ws.create_demo(demo, 2026, "en")
        self.assertEqual(ws.workspace_status(demo)["folder_layout_version"], 2)
        self.assertIn("OVERVIEW.html", (demo / result["guide"]).read_text(encoding="utf-8"))

    def test_unknown_layout_version_fails_closed(self):
        (self.root / ws.LAYOUT).write_text(json.dumps({"schema_version": 3, "language": "en"}))
        with self.assertRaises(ws.WorkspaceError):
            ws.workspace_status(self.root)

    def test_v2_mapping_is_one_to_one_and_reversible_in_every_language(self):
        for language, (overview_name, procedure) in V2_NAMES.items():
            with self.subTest(language=language):
                root = self.base / ("v2-" + language)
                ws.start_workspace(root, 2026, language, layout="v2")
                paths = ws.workspace_folders(root)["paths"]
                self.assertEqual(paths["00_admin/overview.html"], overview_name)
                self.assertEqual(paths["04_accounting/procedure"], procedure)
                self.assertEqual(paths["04_accounting/register.json"], ".business-kit/admin/accounting-register.json")
                self.assertEqual(len(set(paths.values())), len(paths))
                for logical, physical in paths.items():
                    self.assertEqual(ws._logical(root, root / physical), logical)

    def test_accounting_register_is_internal_and_not_evidence(self):
        config = ac.template("configuration")
        config.update(system="local", account_reference="sample", method="EÜR", reviewer="owner",
                      evidence_file=self.evidence())
        ac.configure(self.root, config)
        self.assertTrue((self.root / ".business-kit/admin/accounting-register.json").is_file())
        self.assertEqual(list((self.root / "03 Accounts/Records").iterdir()), [])
        with self.assertRaises(ws.WorkspaceError):
            ws._evidence_path(self.root, ".business-kit/admin/accounting-register.json")


class NumberedOriginalTests(V2Fixture):
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

    def test_verify_flags_a_renamed_original_and_legacy_keeps_hash_names(self):
        result = self.ingest("invoice.pdf", b"synthetic", "2026-10")
        stored = self.root / result["path"]
        stored.rename(stored.with_name("2026-00009_invoice.pdf"))
        self.assertEqual(ws.verify_workspace(self.root)["status"], "needs_review")
        legacy = self.base / "legacy"
        ws.init_workspace(legacy, 2026, "en")
        source = self.base / "sources" / "invoice.pdf"
        imported = ws.ingest_document(legacy, source, "2026-10")
        self.assertEqual(Path(imported["path"]).stem, ws._documents(legacy)["documents"][0]["sha256"])
        self.assertNotIn("document_number", ws._documents(legacy)["documents"][0])


class ManagedInboxTests(V2Fixture):
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

    def test_earlier_layouts_leave_the_inbox_source_in_place(self):
        root = self.base / "v1"
        ws.start_workspace(root, 2026, "en", layout="localized")
        source = root / "01 Inbox/receipt.pdf"
        source.write_bytes(b"kept")
        self.assertIsNone(ws.ingest_document(root, source, "2026-10").get("source_moved_to"))
        self.assertTrue(source.exists())


class RootOverviewTests(V2Fixture):
    def test_overview_page_is_at_the_root_and_details_stay_internal(self):
        result = overview.generate(self.root, "2026-10", language="en")
        self.assertEqual(result["html_path"], "OVERVIEW.html")
        self.assertTrue(result["markdown_path"].startswith(".business-kit/admin/"))
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

    def test_earlier_layouts_keep_overview_and_register_in_place(self):
        root = self.base / "v1"
        ws.start_workspace(root, 2026, "en", layout="localized")
        self.assertEqual(overview.generate(root, "2026-10", language="en")["html_path"], ".business-kit/admin/overview.html")
        self.assertEqual(ws._physical(root, "04_accounting/register.json"), "03 Accounts/Records/register.json")


class BankYearFolderTests(V2Fixture):
    mapping = test_casebank.BankMappingTests.mapping

    def test_normalized_statement_is_saved_under_its_period_year(self):
        doc = self.receive("bank.csv", "ID;Buchungstag;Betrag;Text\n1;02.10.2026;12,00;Synthetic sale\n".encode(), "bank_statement")
        preview = bank.preview(self.root, doc["document_id"], self.mapping(), "2026-10")
        approved = bank.approve(self.root, preview["path"], preview["sha256"], "owner", self.evidence())
        self.assertTrue(approved["csv_path"].startswith("03 Accounts/Bank/2026/normalized/"), approved["csv_path"])
        self.assertTrue((self.root / approved["csv_path"]).is_file())


class CorrespondenceYearFolderTests(test_payment_followup.FollowupTests):
    """Reruns the follow-up journey on v2 and checks where each saved file lands."""
    LAYOUT = "v2"

    def test_saved_reports_use_the_year_they_were_saved(self):
        folder = "05 Business/Correspondence/" + str(date.today().year) + "/"
        self.assertTrue(self.comparison["path"].startswith(folder + "payment-comparisons/"), self.comparison["path"])
        self.assertTrue(self.prepare()["path"].startswith(folder + "payment-followups/"))
        self.assertTrue(inv.export(self.root, "invoice-1")["path"].startswith(folder + "invoice-status-"))

    def test_issued_invoice_copy_is_kept_with_the_documents_of_its_issue_month(self):
        record = inv.show(self.root, "invoice-1")["record"]
        issued = record["issued"]["document"]["path"]
        self.assertTrue(issued.startswith("02 Documents/2026/10/Outgoing invoices/NUMBER-invoice-1_"), issued)
        self.assertTrue(issued.endswith(".md"))
        draft = record["draft"]["path"]
        self.assertTrue(draft.startswith("05 Business/Correspondence/" + str(date.today().year) + "/invoice-evidence/"), draft)
