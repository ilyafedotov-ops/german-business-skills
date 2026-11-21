"""First-run self-check for the welcome flow: read-only, plain findings, one next action."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
sys.path.insert(0, str(SKILLS / "de-business-kit" / "scripts"))
import workspace as ws


class SetupCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / "home"
        self.home.mkdir()
        # A copy of the bundle, like an installed plugin, outside any Git repository.
        self.bundle = self.base / "plugin" / "skills"
        shutil.copytree(SKILLS, self.bundle)
        self.kit = self.bundle / "de-business-kit"

    def check(self, folder):
        return ws.setup_check(folder, home=self.home, skill_directory=self.kit)

    def results(self, report):
        return {row["id"]: row["result"] for row in report["checks"]}

    def test_complete_kit_and_empty_folder_are_ready_and_nothing_is_written(self):
        folder = self.base / "My business"
        folder.mkdir()
        report = self.check(folder)
        self.assertEqual(report["status"], "ready")
        self.assertEqual(report["kit"]["version"], (ROOT / "VERSION").read_text().strip())
        self.assertEqual(report["kit"]["skills_missing"], [])
        self.assertEqual(len(report["kit"]["skills_found"]), 7)
        self.assertEqual(report["folder"]["state"], "empty")
        self.assertEqual(self.results(report), {"kit_complete": "ok", "single_installation": "ok",
                                                "helper_runtime": "ok", "private_location": "ok",
                                                "folder_writable": "ok"})
        self.assertEqual(list(folder.iterdir()), [])
        self.assertIn("start", report["next_action"])

    def test_a_missing_skill_or_a_second_copy_is_reported(self):
        shutil.rmtree(self.bundle / "de-business-tax")
        copy = self.home / ".claude" / "skills" / "de-business-kit"
        copy.mkdir(parents=True)
        (copy / "SKILL.md").write_text("---\nname: de-business-kit\n---\n", encoding="utf-8")
        report = self.check(self.base)
        self.assertEqual(report["status"], "needs_attention")
        self.assertEqual(report["kit"]["skills_missing"], ["de-business-tax"])
        self.assertEqual(self.results(report)["kit_complete"], "problem")
        self.assertEqual(self.results(report)["single_installation"], "warning")
        self.assertEqual(report["kit"]["other_installations"], [str(copy)])

    def test_folder_states_and_unsafe_locations(self):
        workspace = self.base / "existing"
        ws.start_workspace(workspace, year=2026, language="de")
        report = self.check(workspace)
        self.assertEqual(report["folder"]["state"], "workspace")
        self.assertEqual(report["folder"]["workspace"]["folder_language"], "de")
        self.assertIn("start", report["next_action"])

        earlier = self.base / "earlier"
        (earlier / "00_admin").mkdir(parents=True)
        (earlier / "00_admin" / "workspace.json").write_text("{}", encoding="utf-8")
        report = self.check(earlier)
        self.assertEqual((report["folder"]["state"], report["status"]), ("unsupported_workspace", "needs_attention"))

        files = self.base / "old records"
        files.mkdir()
        (files / "invoice.pdf").write_bytes(b"%PDF")
        self.assertEqual(self.check(files)["folder"]["state"], "has_files")

        repository = self.base / "repo"
        (repository / ".git").mkdir(parents=True)
        (repository / ".git" / "HEAD").write_text("ref: refs/heads/main\n", encoding="utf-8")
        report = self.check(repository / "business")
        self.assertEqual(report["folder"]["state"], "missing")
        self.assertEqual(self.results(report)["private_location"], "problem")

        synced = self.base / "Library" / "CloudStorage" / "OneDrive-Personal" / "Business"
        synced.mkdir(parents=True)
        report = self.check(synced)
        self.assertEqual(self.results(report)["synced_folder"], "warning")
        self.assertEqual(report["status"], "ready")

    def test_cli_runs_in_isolated_mode_and_prints_the_report(self):
        folder = self.base / "cli"
        result = subprocess.run([sys.executable, "-I", "-B", str(self.kit / "scripts" / "workspace.py"),
                                 "setup-check", "--folder", str(folder)],
                                cwd=self.base, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["folder"]["state"], "missing")
        self.assertFalse(folder.exists())


if __name__ == "__main__":
    unittest.main()
