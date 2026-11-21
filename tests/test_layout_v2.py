"""Opt-in folder layout v2: versioned mapping, internal register, root overview and year folders."""
from datetime import date
import json

from test_casework import CaseFixture
import test_casebank
import test_payment_followup
import workspace as ws
from casefiles import accounting as ac, bank, invoicing as inv, overview

NATIVE_MARK = "<!-- German Business Kit native overview v1 -->\n"
V2_NAMES = {
    "en": ("OVERVIEW.html", "03 Accounts/Procedure documentation"),
    "ru": ("ОБЗОР.html", "03 Учёт/Описание процессов"),
    "de": ("ÜBERSICHT.html", "03 Buchhaltung/Verfahrensdokumentation"),
}


class V2Fixture(CaseFixture):
    LAYOUT = "v2"


class LayoutVersionTests(V2Fixture):
    def test_v2_is_opt_in_and_records_its_version(self):
        record = {"schema_version": 2, "language": "en"}
        self.assertEqual(json.loads((self.root / ws.LAYOUT).read_text()), record)
        self.assertEqual(ws._load(ws._inside(self.root, ws.MARKER))["folder_layout"], record)
        self.assertEqual(ws.workspace_status(self.root)["folder_layout_version"], 2)
        default = self.base / "default"
        ws.start_workspace(default, 2026, "en")
        self.assertEqual(ws.workspace_status(default)["folder_layout_version"], 1)
        self.assertNotIn("00_admin/overview.html", ws.workspace_folders(default)["paths"])
        legacy = self.base / "legacy"
        ws.init_workspace(legacy, 2026, "en")
        self.assertIsNone(ws.workspace_status(legacy)["folder_layout_version"])

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
        ws.start_workspace(root, 2026, "en")
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
