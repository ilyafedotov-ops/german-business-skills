"""Cash entries carry VAT as stated on documents and links to approved proposals."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace as ws
from casefiles import accounting as ac, documents, overview, reviews


class CashVatFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "private"
        ws.init_workspace(self.root, 2026, "en")
        self.proof = "08_correspondence/review.md"
        (self.root / self.proof).write_text("Synthetic owner review of the payment evidence", encoding="utf-8")
        config = ac.template("configuration")
        config.update(system="local", account_reference="business-one", method="EÜR",
                      reviewer="owner", evidence_file=self.proof)
        ac.configure(self.root, config)

    def line(self, amount, kind="income", status="stated", net=None, tax=None, rate=None,
             activity="consulting", proposal=None):
        return {"kind": kind, "amount": amount, "category": "Synthetic " + kind, "activity_id": activity,
                "proposal_id": proposal, "vat": {"status": status, "net": net, "tax": tax, "rate": rate}}

    def entry(self, identifier, amount, *lines, **changes):
        value = ac.template("entry")
        value.update(entry_id=identifier, date="2026-10-20", account="bank", transaction_id=identifier,
                     amount=amount, currency="EUR", reviewer="owner", evidence_file=self.proof,
                     note="Synthetic reviewed cash movement", lines=list(lines))
        value.update(changes)
        return value


class StatedVatTests(CashVatFixture):
    def test_new_entry_template_asks_for_line_vat_and_optional_proposal(self):
        value = ac.template("entry")
        self.assertEqual(value["schema_version"], 2)
        self.assertEqual(value["lines"][0]["proposal_id"], None)
        self.assertEqual(value["lines"][0]["vat"], {"status": "unresolved", "net": None, "tax": None, "rate": None})

    def test_period_report_groups_stated_vat_by_currency_kind_and_rate(self):
        ac.post(self.root, self.entry("sale-19", "119.00", self.line("119.00", net="100.00", tax="19.00", rate="19")))
        ac.post(self.root, self.entry("sale-7", "107.00", self.line("107.00", net="100.00", tax="7.00", rate="7.00")))
        ac.post(self.root, self.entry("purchase", "-11.90", self.line("-11.90", "expense", net="-10.00", tax="-1.90", rate="19.0")))
        ac.post(self.root, self.entry("fee", "-3.00", self.line("-3.00", "expense", status="none_stated")))
        report = ac.period_report(self.root, "2026-10")
        self.assertEqual(report["vat"], [
            {"currency": "EUR", "kind": "expense", "rate": "19", "net": "-10.00", "tax": "-1.90"},
            {"currency": "EUR", "kind": "income", "rate": "19", "net": "100.00", "tax": "19.00"},
            {"currency": "EUR", "kind": "income", "rate": "7", "net": "100.00", "tax": "7.00"},
        ])
        self.assertEqual(report["totals"]["EUR"]["income"], "226.00")
        self.assertEqual(report["tax_return_status"], "not_calculated")
        self.assertFalse({"vat_unresolved", "vat_not_recorded"} & set(report["open_items"]))

    def test_inconsistent_or_partial_vat_is_rejected_without_recording(self):
        cases = {
            "net plus VAT differs": self.line("119.00", net="100.00", tax="18.00", rate="19"),
            "opposite signs": self.line("119.00", net="200.00", tax="-81.00"),
            "missing VAT": self.line("119.00", net="119.00"),
            "rate above 100": self.line("119.00", net="100.00", tax="19.00", rate="119"),
            "amounts on none_stated": self.line("119.00", status="none_stated", net="119.00", tax="0.00"),
            "unknown status": self.line("119.00", status="exempt"),
            "line without VAT": {key: value for key, value in self.line("119.00").items() if key != "vat"},
        }
        for name, line in cases.items():
            with self.subTest(name):
                with self.assertRaises(ws.WorkspaceError):
                    ac.post(self.root, self.entry("bad", "119.00", line))
        self.assertEqual(ac.status(self.root)["entry_count"], 0)

    def test_unresolved_vat_keeps_the_period_open(self):
        ac.post(self.root, self.entry("sale", "119.00", self.line("119.00", status="unresolved")))
        report = ac.period_report(self.root, "2026-10")
        self.assertIn("vat_unresolved", report["open_items"])
        self.assertEqual(report["vat"], [])
        view = overview.generate(self.root, "2026-10", "2026-10-26")
        self.assertIn("VAT on some cash lines is not yet determined", (self.root / view["markdown_path"]).read_text(encoding="utf-8"))


class LegacyEntryTests(CashVatFixture):
    def legacy(self, identifier, amount):
        # Simulates an entry recorded before line VAT existed, through the real register writer.
        with ac._edit(self.root, "cash_entry_recorded") as state:
            state["entries"][identifier] = {
                "entry_id": identifier, "date": "2026-10-20", "account": "bank", "transaction_id": identifier,
                "amount": amount, "currency": "EUR", "reviewer": "owner", "evidence_file": self.proof,
                "note": "Recorded before line VAT", "replaces": None, "reverses": None, "recorded_at": ws._now(),
                "evidence": ac.st.evidence(self.root, self.proof),
                "lines": [{"kind": "income", "amount": amount, "category": "sale", "activity_id": "consulting"}]}

    def test_entries_without_line_vat_cannot_be_posted(self):
        value = self.entry("old-shape", "100.00")
        del value["schema_version"]
        value["lines"] = [{"kind": "income", "amount": "100.00", "category": "sale", "activity_id": "consulting"}]
        with self.assertRaisesRegex(ws.WorkspaceError, "accounting-template"):
            ac.post(self.root, value)

    def test_recorded_legacy_entries_stay_reportable_and_correctable(self):
        self.legacy("old-sale", "100.00")
        report = ac.period_report(self.root, "2026-10")
        self.assertEqual(report["totals"]["EUR"]["income"], "100.00")
        self.assertIn("vat_not_recorded", report["open_items"])
        ac.reverse(self.root, "old-sale", "old-sale-reversal", self.proof, "owner", "Record the stated VAT")
        ac.post(self.root, self.entry("old-sale-fixed", "100.00", self.line("100.00", status="none_stated"),
                                      transaction_id="old-sale", replaces="old-sale"))
        report = ac.period_report(self.root, "2026-10")
        self.assertEqual(report["totals"]["EUR"]["income"], "100.00")
        self.assertEqual(len(report["entries"]), 3)


class ProposalLinkTests(CashVatFixture):
    def setUp(self):
        super().setUp()
        source = self.base / "invoice.pdf"
        source.write_bytes(b"Synthetic invoice SYN-1")
        self.document = documents.receive(self.root, source, "2026-10", "2026-10-02", "invoice")["document_id"]
        reviews.save_source_check(self.root, {
            "schema_version": 1, "source_check_id": "rule-1", "url": "https://www.gesetze-im-internet.de/ustg_1980/__12.html",
            "title": "Synthetic rule check", "checked_on": "2026-10-25", "applicable_period": "2026-10",
            "assumptions": ["Synthetic facts only"], "conclusion": "Synthetic applicability note",
            "review_after": "2099-01-01", "reviewer": "owner", "evidence_file": self.proof})

    def proposal(self, identifier, approve=True, supersedes=None):
        def field(value):
            return {"raw": value, "value": value, "location": "page 1", "status": "reviewed", "reviewer": "owner", "note": None}
        record = reviews.proposal_template()
        record.update(proposal_id=identifier, document_id=self.document, period="2026-10", activity_id="consulting",
                      supersedes=supersedes)
        record["fields"] = {key: field(value) for key, value in {
            "invoice_number": "SYN-1", "invoice_date": "2026-10-01", "currency": "EUR",
            "net": "100.00", "tax": "19.00", "gross": "119.00"}.items()}
        record["proposed_treatment"] = {"category": "Synthetic service", "tax_rule": "Synthetic reviewed assumption",
                                         "reason": "Training fixture only", "source_check_ids": ["rule-1"]}
        saved = reviews.save_proposal(self.root, record)
        if approve:
            record["review"].update(status="approved", reviewer="owner", reviewed_on="2026-10-25", note="Synthetic approval")
            reviews.save_proposal(self.root, record, saved["sha256"])

    def paid(self, identifier="paid", proposal="proposal-1", activity="consulting"):
        return self.entry(identifier, "119.00", self.line("119.00", net="100.00", tax="19.00", rate="19",
                                                         activity=activity, proposal=proposal))

    def change_proposal(self, identifier):
        path = self.root / "00_admin/casework.json"
        state = json.loads(path.read_text(encoding="utf-8"))
        state["proposals"][identifier]["review"]["note"] = "Changed outside the reviewed writer"
        path.write_text(json.dumps(state), encoding="utf-8")

    def test_linked_line_is_fingerprinted_and_a_later_proposal_change_blocks_the_report(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        entry = ac.period_report(self.root, "2026-10")["entries"][0]
        self.assertEqual(list(entry["linked_proposals"]), ["proposal-1"])
        self.change_proposal("proposal-1")
        with self.assertRaisesRegex(ws.WorkspaceError, "linked proposal"):
            ac.period_report(self.root, "2026-10")

    def test_links_need_a_current_approved_proposal_for_the_same_activity(self):
        self.proposal("proposal-1")
        self.proposal("draft-only", approve=False)
        cases = {"unknown": self.paid(proposal="missing"), "draft": self.paid(proposal="draft-only"),
                 "other activity": self.paid(activity="translation")}
        for name, value in cases.items():
            with self.subTest(name):
                with self.assertRaises(ws.WorkspaceError):
                    ac.post(self.root, value)
        self.proposal("proposal-2", supersedes="proposal-1")
        with self.assertRaisesRegex(ws.WorkspaceError, "current approved"):
            ac.post(self.root, self.paid())
        ac.post(self.root, self.paid(proposal="proposal-2"))
        self.assertEqual(ac.status(self.root)["entry_count"], 1)

    def test_filing_preflight_notices_a_changed_linked_proposal(self):
        self.proposal("proposal-1")
        ac.post(self.root, self.paid())
        report = ac.export_report(self.root, "2026-10")
        payload = "05_tax/2026/external-tool-output.txt"
        ws._inside(self.root, payload).write_text("SYNTHETIC external tool output", encoding="utf-8")
        filing = ac.template("filing")
        filing.update(filing_id="return-1", form="ustva", form_version="2026", period="2026-10",
                      recipient="synthetic-finanzamt", payload_file=payload,
                      source_files=[ws._logical(self.root, self.root / report["path"])])
        ac.create_filing(self.root, filing)
        self.assertEqual(ac.check_filing(self.root, "return-1")["issues"], [])
        self.change_proposal("proposal-1")
        codes = {issue["code"] for issue in ac.check_filing(self.root, "return-1")["issues"]}
        self.assertIn("local_report_invalid", codes)


class ReversalAndExportTests(CashVatFixture):
    def test_reversal_negates_stated_vat(self):
        ac.post(self.root, self.entry("sale", "119.00", self.line("119.00", net="100.00", tax="19.00", rate="19")))
        ac.reverse(self.root, "sale", "sale-reversal", self.proof, "owner", "Wrong customer")
        report = ac.period_report(self.root, "2026-10")
        reversal = next(entry for entry in report["entries"] if entry["entry_id"] == "sale-reversal")
        self.assertEqual(reversal["lines"][0]["vat"], {"status": "stated", "net": "-100.00", "tax": "-19.00", "rate": "19"})
        self.assertEqual(report["vat"], [{"currency": "EUR", "kind": "income", "rate": "19", "net": "0.00", "tax": "0.00"}])

    def test_exported_report_lists_stated_vat_in_the_workspace_language(self):
        ac.post(self.root, self.entry("sale", "119.00", self.line("119.00", net="100.00", tax="19.00", rate="19")))
        markdown = (self.root / ac.export_report(self.root, "2026-10")["markdown_path"]).read_text(encoding="utf-8")
        self.assertIn("## VAT as stated on documents (EUR)", markdown)
        self.assertIn("- Receipts · 19 %: net 100.00, VAT 19.00", markdown)
        ws.configure_workspace(self.root, language="ru")
        markdown = (self.root / ac.export_report(self.root, "2026-10")["markdown_path"]).read_text(encoding="utf-8")
        self.assertIn("## НДС по документам (EUR)", markdown)
        self.assertIn("- Поступления · 19 %: нетто 100.00, НДС 19.00", markdown)


if __name__ == "__main__":
    unittest.main()
