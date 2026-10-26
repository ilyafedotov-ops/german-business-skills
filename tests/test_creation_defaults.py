"""Creation language agrees across entry points without migrating old workspaces."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace as ws


class CreationDefaultsTests(unittest.TestCase):
    def test_init_cli_and_start_default_to_english(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory).resolve()
            result = subprocess.run([sys.executable, "-B", str(SCRIPTS / "workspace.py"), "init",
                                     "--root", str(base / "init"), "--year", "2026"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(ws.workspace_status(base / "init")["language"], "en")
            self.assertEqual(ws.start_workspace(base / "start", year=2026)["language"], "en")

    def test_api_default_is_english_and_resume_keeps_existing_choice(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve() / "workspace"
            ws.init_workspace(root, 2026)
            self.assertEqual(ws.workspace_status(root)["language"], "en")
            ws.configure_workspace(root, language="ru")
            before = (root / ws.MARKER).read_bytes()
            self.assertEqual(ws.start_workspace(root)["language"], "ru")
            self.assertEqual((root / ws.MARKER).read_bytes(), before)
