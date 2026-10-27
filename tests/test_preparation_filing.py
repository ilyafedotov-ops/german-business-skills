"""Receipt evidence must survive the preparation-to-filing handoff."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"))
import workspace as ws
import workflows as wf
from casefiles import accounting as ac


class PreparationFilingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve() / "private"
        ws.init_workspace(self.root, 2026, "en")
        self.proof = "08_correspondence/choice.md"
        self.receipt = "08_correspondence/receipt.txt"
        self.write(self.proof, "Synthetic explicit external-accounting choice and action evidence")
        self.write(self.receipt, "Synthetic receipt: net 100, VAT 19, gross 119")
        choice = ac.template("configuration")
        choice.update(system="external", product="Synthetic books", account_reference="business",
                      method="EÜR", reviewer="owner", evidence_file=self.proof)
        ac.configure(self.root, choice)

    def write(self, name, value):
        (self.root / name).write_text(value if isinstance(value, str) else json.dumps(value))
        return name

    def preparation(self, incomplete=False):
        value = wf.template("elster")
        value.update(record_id="period-1", period="2026-10", activity_ids=["services"],
                     evidence=[{"id": "receipt", "path": self.receipt}])
        value["facts"].update(form_id="ustva", form_version="2026", authority="Synthetic authority",
                              eligibility_reason="Synthetic supplied review", portal_checked_on="2026-10-27",
                              account_capability="Synthetic export", deadline_basis="Synthetic supplied date",
                              calculation_notes="Fixture only, not an actual return")
        value["fields"] = [{"label": "Synthetic observed field", "value": "19.00",
                            "status": "proposed" if incomplete else "reviewed", "evidence_ids": ["receipt"],
                            "reviewer": "fixture reviewer", "note": None}]
        value["source_checks"] = [{"url": "https://example.test/synthetic-rule", "checked_on": "2026-10-27",
                                   "applicable_period": "2026-10", "conclusion": "Synthetic fixture",
                                   "evidence_ids": ["receipt"]}]
        return wf.prepare(self.root, "elster", self.write("00_admin/inbox/preparation.json", value))["path"]

    def filing(self, report, identifier="return-1", **changes):
        value = ac.template("filing")
        value.update(filing_id=identifier, form="ustva", form_version="2026", period="2026-10",
                     recipient="Synthetic authority", payload_file=self.write("05_tax/2026/payload.json", {"synthetic": True}),
                     source_files=[report], unresolved_items=[])
        value.update(changes)
        return ac.create_filing(self.root, value)

    def action(self, action, identifier="return-1", **changes):
        current = ac.get_filing(self.root, identifier)
        value = ac.template("filing-action")
        value.update(filing_id=identifier, action=action, actor="fixture reviewer", evidence_file=self.proof,
                     note="Synthetic explicit instruction for this action", **changes)
        return ac.filing_action(self.root, value, current["sha256"])

    def test_changed_receipt_blocks_continuation_through_preparation_report(self):
        report = self.preparation()
        self.filing(report)
        self.assertEqual(ac.check_filing(self.root, "return-1")["next_step"], "review")
        self.write(self.receipt, "Corrected receipt: changed evidence")
        check = ac.check_filing(self.root, "return-1")
        self.assertEqual(check["next_step"], "resolve_issues")
        self.assertEqual(check["allowed_preflight_actions"], [])
        with self.assertRaises(ws.WorkspaceError):
            self.action("review")

    def test_preparation_dependencies_are_frozen_with_filing(self):
        report = self.preparation()
        self.filing(report)
        record = ac.get_filing(self.root, "return-1")["record"]
        frozen = {item["source"]["path"]: item for item in record["sources"]}
        self.assertIn(self.receipt, frozen)
        self.assertIn("00_admin/inbox/preparation.json", frozen)
        self.assertEqual((self.root / frozen[self.receipt]["path"]).read_bytes(),
                         (self.root / self.receipt).read_bytes())

    def test_unresolved_preparation_and_preparation_payload_cannot_advance(self):
        report = self.preparation(incomplete=True)
        self.filing(report)
        self.assertEqual(ac.check_filing(self.root, "return-1")["next_step"], "resolve_issues")
        with self.assertRaises(ws.WorkspaceError):
            self.action("review")

    def test_preparation_is_supporting_evidence_not_return_payload(self):
        report = self.preparation()
        self.filing(report, payload_file=report)
        self.assertEqual(ac.check_filing(self.root, "return-1")["next_step"], "resolve_issues")

    def assert_change_blocks(self, prior_actions, next_action):
        self.filing(self.preparation())
        for action in prior_actions:
            self.action(action)
        self.write(self.receipt, "Changed receipt")
        self.assertEqual(ac.check_filing(self.root, "return-1")["allowed_preflight_actions"], [])
        with self.assertRaises(ws.WorkspaceError):
            self.action(next_action)

    def test_changed_receipt_blocks_authorization(self):
        self.assert_change_blocks(["review"], "authorize")

    def test_changed_receipt_blocks_attempt(self):
        self.assert_change_blocks(["review", "authorize"], "begin")

    def test_uncertain_outcome_uses_frozen_dependencies_after_originals_disappear(self):
        report = self.preparation()
        self.filing(report)
        for action in ["review", "authorize", "begin"]:
            self.action(action)
        (self.root / self.receipt).unlink()
        (self.root / "00_admin/inbox/preparation.json").unlink()
        check = ac.check_filing(self.root, "return-1")
        self.assertEqual(check["next_step"], "resolve_submission_outcome")
        self.assertEqual(check["source_scope"], "frozen_evidence_only")
        with self.assertRaises(ws.WorkspaceError):
            self.action("cancel")
        with self.assertRaises(ws.WorkspaceError):
            self.filing(report, "duplicate", supersedes="return-1")
        self.action("receipt", external_id="synthetic-receipt")
        self.action("response", response_kind="assessment")
        self.assertEqual(ac.get_filing(self.root, "return-1")["record"]["state"], "submitted")

    def test_corrupt_frozen_dependency_blocks_historical_receipt(self):
        self.filing(self.preparation())
        for action in ["review", "authorize", "begin"]:
            self.action(action)
        record = ac.get_filing(self.root, "return-1")["record"]
        dependency = next(item for item in record["sources"] if item["source"]["path"] == self.receipt)
        self.write(dependency["path"], "Damaged frozen receipt")
        self.assertIn("snapshot_changed", [item["code"] for item in ac.check_filing(self.root, "return-1")["issues"]])
        with self.assertRaises(ws.WorkspaceError):
            self.action("receipt", external_id="synthetic-receipt")

    def test_incomplete_or_falsified_dependency_metadata_is_rejected_before_capture(self):
        report = self.preparation()
        original = json.loads((self.root / report).read_text())
        variants = []
        omitted = json.loads(json.dumps(original))
        omitted["sources"].pop()
        variants.append(omitted)
        malformed = json.loads(json.dumps(original))
        malformed["sources"] = [None]
        variants.append(malformed)
        bad_language = json.loads(json.dumps(original))
        bad_language["language"] = []
        variants.append(bad_language)
        mismatch = json.loads(json.dumps(original))
        mismatch["input"]["fields"][0]["value"] = "999.00"
        variants.append(mismatch)
        for value in variants:
            with self.subTest(value=value):
                self.write(report, value)
                with self.assertRaises(ws.WorkspaceError):
                    self.filing(report)
                self.assertEqual(ac.status(self.root)["filings"], [])

    def test_nested_preparation_collects_shared_receipt_once(self):
        first = self.preparation()
        value = json.loads((self.root / "00_admin/inbox/preparation.json").read_text())
        value["record_id"] = "outer"
        value["evidence"].append({"id": "inner", "path": first})
        second = wf.prepare(self.root, "elster", self.write("00_admin/inbox/outer.json", value))["path"]
        self.filing(second)
        record = ac.get_filing(self.root, "return-1")["record"]
        paths = [item["source"]["path"] for item in record["sources"]]
        self.assertEqual(paths.count(self.receipt), 1)
        self.assertIn(first, paths)
        self.assertEqual(ac.check_filing(self.root, "return-1")["next_step"], "review")
        self.write(self.receipt, "Revised nested source")
        self.assertEqual(ac.check_filing(self.root, "return-1")["next_step"], "resolve_issues")

    def test_stale_report_cannot_freeze_new_receipt_under_old_fingerprint(self):
        report = self.preparation()
        self.write(self.receipt, "Changed before creating draft")
        with self.assertRaises(ws.WorkspaceError):
            self.filing(report)

    def test_concurrent_receipt_edit_cannot_replace_selected_dependency_digest(self):
        report = self.preparation()
        original = ac.st.evidence
        calls = 0

        def capture(root, path):
            nonlocal calls
            if path == self.receipt:
                calls += 1
                if calls == 2:
                    self.write(self.receipt, "Noncooperating edit during capture")
            return original(root, path)

        with patch.object(ac.st, "evidence", side_effect=capture):
            with self.assertRaises(ws.WorkspaceError):
                self.filing(report)
        self.assertEqual(ac.status(self.root)["filings"], [])

    def test_nested_cash_report_keeps_existing_freshness_checks(self):
        choice = ac.template("configuration")
        choice.update(system="local", account_reference="business", method="EÜR",
                      reviewer="owner", evidence_file=self.proof)
        ac.configure(self.root, choice, ac.status(self.root)["configuration_sha256"])
        entry = ac.template("entry")
        entry.update(entry_id="payment", date="2026-10-20", account="bank", transaction_id="t1",
                     amount="-119.00", currency="EUR", reviewer="fixture reviewer", evidence_file=self.receipt,
                     note="Synthetic reviewed payment")
        entry["lines"] = [{"kind": "expense", "amount": "-119.00", "category": "services", "activity_id": "services",
                           "proposal_id": None, "vat": {"status": "stated", "net": "-100.00", "tax": "-19.00", "rate": "19"}}]
        ac.post(self.root, entry)
        cash = ac.export_report(self.root, "2026-10")
        self.preparation()
        value = json.loads((self.root / "00_admin/inbox/preparation.json").read_text())
        value["evidence"].append({"id": "cash", "path": cash["path"]})
        report = wf.prepare(self.root, "elster", self.write("00_admin/inbox/with-cash.json", value))["path"]
        self.filing(report)
        entry.update(entry_id="later", transaction_id="t2")
        ac.post(self.root, entry)
        self.assertIn("local_report_invalid", [item["code"] for item in ac.check_filing(self.root, "return-1")["issues"]])

    def test_dependency_depth_is_bounded_before_any_filing_is_saved(self):
        previous = self.preparation()
        base = json.loads((self.root / "00_admin/inbox/preparation.json").read_text())
        for depth in range(18):
            value = json.loads(json.dumps(base))
            value["record_id"] = "nested-" + str(depth)
            value["evidence"].append({"id": "previous", "path": previous})
            previous = wf.prepare(self.root, "elster", self.write("00_admin/inbox/nested-" + str(depth) + ".json", value))["path"]
        with self.assertRaisesRegex(ws.WorkspaceError, "dependency limit"):
            self.filing(previous)
        self.assertEqual(ac.status(self.root)["filings"], [])

    def test_other_supported_preparations_are_frozen_and_checked(self):
        self.preparation()
        base = json.loads((self.root / "00_admin/inbox/preparation.json").read_text())
        prior = None
        for kind in ["classification", "international"]:
            with self.subTest(kind=kind):
                value = wf.template(kind)
                value.update({key: base[key] for key in ["record_id", "period", "activity_ids", "evidence", "source_checks"]})
                for key, rule in wf.FIELDS[kind].items():
                    value["facts"][key] = (rule[0] if isinstance(rule, list) else False if rule is bool
                                           else {"date": "2026-10-20", "currency": "EUR", "money": "100.00"}.get(rule, "Synthetic reviewed fact"))
                report = wf.prepare(self.root, kind, self.write("00_admin/inbox/" + kind + ".json", value))["path"]
                self.filing(report, kind, supersedes=prior)
                self.assertEqual(ac.check_filing(self.root, kind)["next_step"], "review")
                record = ac.get_filing(self.root, kind)["record"]
                self.assertIn(self.receipt, [item["source"]["path"] for item in record["sources"]])
                self.action("cancel", kind)
                prior = kind


if __name__ == "__main__":
    unittest.main()
