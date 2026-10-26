"""The publication verifier tolerates delayed proof availability, never bypasses it."""
from pathlib import Path
import os
import re
import shutil
import subprocess
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name != 'nt' and shutil.which('bash'),
                     'Publication runs in POSIX Bash; Windows user scripts have separate native tests')
class ReleaseRetryTests(unittest.TestCase):
    def run_verifier(self, command):
        workflow = (ROOT / '.github/workflows/release.yml').read_text(encoding='utf-8')
        match = re.search(r'(?ms)^          verify_with_retry\(\) \{.*?^          \}', workflow)
        self.assertIsNotNone(match, 'Missing verification retry function')
        script = textwrap.dedent(match.group()) + '\nsleep() { :; }\n' + command
        result = subprocess.run([shutil.which('bash'), '-c', script], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_delayed_attestation_is_retried_then_stops_at_verified_success(self):
        self.run_verifier('''
calls=0
proof() { calls=$((calls + 1)); test "$calls" -ge 3; }
verify_with_retry proof && test "$calls" -eq 3
''')

    def test_unverifiable_proof_fails_after_bounded_attempts(self):
        self.run_verifier('''
calls=0
proof() { calls=$((calls + 1)); return 1; }
if verify_with_retry proof; then exit 1; fi
test "$calls" -eq 6
''')
