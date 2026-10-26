from pathlib import Path
import tempfile
import unittest
import synthetic_journey


class MonthlyJourneyTests(unittest.TestCase):
    def test_cli_import_review_resume_and_optional_archive_in_both_languages(self):
        with tempfile.TemporaryDirectory() as temporary:
            for language in ("en", "ru"):
                with self.subTest(language=language):
                    result = synthetic_journey.run(Path(temporary).resolve() / language, language)
                    self.assertEqual(result["resumed"], "resumed")
                    self.assertEqual(result["overview"]["counts"]["documents"], 3)
                    self.assertEqual(result["overview"]["counts"]["unmatched_items"], 1)
                    self.assertEqual(result["verified"]["status"], "verified")
                    self.assertEqual(result["bundle"]["readiness"], "prepared_with_open_items")
                    html = (Path(result["root"]) / result["overview"]["html_path"]).read_text(encoding="utf-8")
                    self.assertIn('id="accounting-tax"', html)
                    snapshot = __import__("json").loads(synthetic_journey.ws._inside(Path(result["root"]), "00_admin/overview.json").read_text())
                    self.assertEqual(snapshot["capabilities"]["accounting_ledger"], "limited_cash_journal")
                    self.assertEqual(snapshot["capabilities"]["elster_submission"], "not_implemented")
                    self.assertIn("Clarify the authority request and its stated date", html)


if __name__ == "__main__":
    unittest.main()
