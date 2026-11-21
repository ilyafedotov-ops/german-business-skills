"""The helper programs start the way assistant hosts run them."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "skills" / "de-business-kit" / "scripts"
PROGRAMS = ("workspace.py", "desk.py", "workflows.py", "payments.py", "recovery.py")


class EntryScriptTests(unittest.TestCase):
    def test_programs_start_in_isolated_mode_from_another_folder(self):
        # Hosts can run Python with -I for user files; it leaves the script folder off sys.path.
        with tempfile.TemporaryDirectory() as elsewhere:
            for program in PROGRAMS:
                with self.subTest(program=program):
                    result = subprocess.run([sys.executable, "-I", "-B", str(SCRIPTS / program), "--help"],
                                            cwd=elsewhere, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("usage:", result.stdout)


if __name__ == "__main__":
    unittest.main()
