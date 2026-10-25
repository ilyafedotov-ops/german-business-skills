"""Developer-only cross-runtime contract checks; end users do not need Python."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / 'skills' / 'de-business-kit'
sys.path.insert(0, str(SKILL / 'scripts'))
import workspace as ws


class NativeSeedTests(unittest.TestCase):
    def test_native_seed_matches_canonical_empty_workspace(self):
        seed = json.loads((SKILL / 'assets/workspace-seed.json').read_text())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve() / 'private'
            ws.init_workspace(root, 2026, 'en', 'general')
            for relative, record in seed.items():
                self.assertEqual(record, json.loads((root / relative).read_text()), relative)
            self.assertEqual(set(seed['01_profile/business.json']['facts']), set(ws.FIELDS))


@unittest.skipUnless(os.name == 'nt' or os.environ.get('GBK_TEST_DOCKER_IMAGE'),
                     'Native PowerShell test: use Windows or explicit developer container')
class NativeInteropTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'Private [workspace]'

    def run_native(self, action, **options):
        image = os.environ.get('GBK_TEST_DOCKER_IMAGE')
        if image:
            command = ['docker', 'run', '--rm', '--network', 'none',
                       '-v', f'{REPO}:{REPO}:ro', '-v', f'{self.base}:{self.base}',
                       image, 'pwsh']
        else:
            command = [shutil.which('powershell.exe') or 'powershell.exe']
        command += ['-NoProfile', '-NonInteractive', '-File', str(SKILL / 'scripts/windows.ps1'),
                    '-Action', action, '-Root', str(self.root)]
        for key, value in options.items():
            command += ['-' + key, str(value)]
        result = subprocess.run(command, capture_output=True, timeout=40, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_native_workspace_and_intake_are_readable_by_python_without_migration(self):
        self.assertEqual(self.run_native('start', Year=2026, Language='ru')['status'], 'initialized')
        source = self.base / 'invoice [1] ü.csv'
        source.write_bytes(b'amount,currency\n12.34,EUR\n')
        self.run_native('ingest', Source=source, Period='2026-10')
        index = json.loads((self.root / ws.DOCUMENTS).read_text(encoding='utf-8'))
        self.assertEqual(index['documents'][0]['original_name'], source.name)
        self.assertEqual(ws.verify_workspace(self.root)['status'], 'ok')
        self.assertEqual(ws.workspace_status(self.root)['language'], 'ru')
        self.assertEqual(ws.ingest_document(self.root, source, '2026-10')['status'], 'existing_content')
        self.assertEqual(self.run_native('verify')['indexed_documents'], 1)
        events = json.loads((self.root / '09_audit/events.json').read_text())
        self.assertEqual(len(events), 3)
        self.assertTrue(all(isinstance(event, dict) and 'action' in event for event in events))

    def test_native_resumes_python_workspace_preserves_facts_and_detects_orphan(self):
        ws.init_workspace(self.root, 2026, 'en', 'bookkeeping')
        before = (self.root / ws.PROFILE).read_bytes()
        result = self.run_native('start', Language='ru', Mode='general')
        self.assertEqual((result['language'], result['mode']), ('en', 'bookkeeping'))
        self.assertEqual((self.root / ws.PROFILE).read_bytes(), before)
        original = self.root / '06_bookkeeping/2026/10/originals/orphan.csv'
        original.parent.mkdir(parents=True)
        original.write_bytes(b'unindexed')
        result = self.run_native('verify')
        self.assertEqual(result['status'], 'needs_review')
        self.assertEqual(result['unindexed_originals'], 1)
        self.assertEqual(original.read_bytes(), b'unindexed')
