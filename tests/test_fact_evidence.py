import json
import unittest
from test_casework import CaseFixture
import workspace as ws


class FactEvidenceTests(CaseFixture):
    def fact(self, source):
        return {"field": "legal_form", "value": "Einzelunternehmen", "status": "verified", "source": source}

    def test_verified_requires_real_preserved_file_and_changed_evidence_is_reported(self):
        with self.assertRaises(ws.WorkspaceError):
            ws.record_fact(self.root, self.fact({"kind": "user_statement", "ref": "trust me"}))
        evidence = self.evidence()
        ws.record_fact(self.root, self.fact({"kind": "file", "ref": evidence}))
        self.assertEqual(ws.workspace_status(self.root)["verified_fact_evidence_issues"], [])
        (self.root / evidence).write_text("Changed evidence", encoding="utf-8")
        self.assertEqual(ws.workspace_status(self.root)["verified_fact_evidence_issues"], ["legal_form"])

    def test_legacy_verified_fact_is_preserved_and_needs_reassessment(self):
        profile = self.root / ws.PROFILE
        value = json.loads(profile.read_text())
        value["facts"]["legal_form"].update(value="Einzelunternehmen", status="verified", source={"kind": "letter", "ref": "old text"})
        profile.write_text(json.dumps(value))
        before = profile.read_bytes()
        self.assertIn("legal_form", ws.workspace_status(self.root)["verified_fact_evidence_issues"])
        self.assertEqual(profile.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
