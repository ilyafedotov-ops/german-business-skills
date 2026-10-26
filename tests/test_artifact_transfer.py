"""Exercise the actual PR artifact verifier with valid and damaged payloads."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.name != 'nt' and shutil.which('bash') and shutil.which('sha256sum'),
                     'Artifact transfer verification runs on Ubuntu with Bash and sha256sum')
class ArtifactTransferTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.files = []
        for platform in ('windows-x64.zip', 'macos-arm64.tar.gz', 'macos-x86_64.tar.gz'):
            path = self.root / ('de-business-kit-0.7.0-preview.1-gui-' + platform)
            path.write_bytes(b'synthetic archived payload: ' + platform.encode())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            (self.root / (path.name + '.sha256')).write_text(f'{digest}  {path.name}\n')
            self.files.append(path)

    def verify(self, expected):
        workflow = (ROOT / '.github/workflows/checks.yml').read_text()
        job = workflow.split('\n  artifact-transfer:\n', 1)[1]
        script = textwrap.dedent(job.split('        run: |\n', 1)[1])
        result = subprocess.run(['bash', '-c', script], cwd=self.root, capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, expected, result.stdout + result.stderr)

    def test_three_matching_platform_archives_pass(self):
        self.verify(True)

    def test_tampered_payload_fails(self):
        self.files[0].write_bytes(b'changed after upload')
        self.verify(False)

    def test_missing_platform_is_not_replaced_by_duplicate_architecture(self):
        original = self.files[-1]
        replacement = self.root / original.name.replace('macos-x86_64', 'macos-arm64').replace('0.7.0', '0.8.0')
        original.rename(replacement)
        (self.root / (original.name + '.sha256')).unlink()
        digest = hashlib.sha256(replacement.read_bytes()).hexdigest()
        (self.root / (replacement.name + '.sha256')).write_text(f'{digest}  {replacement.name}\n')
        self.verify(False)

    def test_checksum_cannot_point_at_another_payload(self):
        (self.root / (self.files[0].name + '.sha256')).write_bytes(
            (self.root / (self.files[1].name + '.sha256')).read_bytes())
        self.verify(False)
