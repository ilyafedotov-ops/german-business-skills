"""Release scanning must block serious findings, not just finish analysis."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SecurityGateTests(unittest.TestCase):
    def check(self, payload, expected):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            if payload is not None:
                (path / 'result.sarif').write_text(json.dumps(payload), encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', str(ROOT / 'tools/check_security.py'), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)

    def test_clean_analysis_passes_but_missing_results_fail(self):
        self.check({'runs': [{'tool': {'driver': {'rules': []}}, 'results': []}]}, 0)
        self.check(None, 2)
        self.check({'runs': []}, 2)

    def test_high_critical_and_error_results_block_release(self):
        for severity in ('7.0', '9.8'):
            self.check({'runs': [{'tool': {'driver': {'rules': [
                {'id': 'synthetic', 'properties': {'security-severity': severity}}]}},
                'results': [{'ruleId': 'synthetic', 'level': 'warning'}]}]}, 2)
        self.check({'runs': [{'tool': {'driver': {'rules': []}},
                             'results': [{'ruleId': 'other', 'level': 'error'}]}]}, 2)

    def test_lower_severity_is_reported_without_blocking(self):
        self.check({'runs': [{'tool': {'driver': {'rules': [
            {'id': 'synthetic', 'properties': {'security-severity': '4.0'}}]}},
            'results': [{'ruleId': 'synthetic', 'level': 'warning'}]}]}, 0)
