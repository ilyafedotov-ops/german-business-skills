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
                self.assertEqual(record, json.loads(ws._path(root, relative).read_text()), relative)
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
        index = json.loads((ws._path(self.root, ws.DOCUMENTS)).read_text(encoding='utf-8'))
        self.assertEqual(index['documents'][0]['original_name'], source.name)
        self.assertEqual(ws.verify_workspace(self.root)['status'], 'ok')
        self.assertEqual(ws.workspace_status(self.root)['language'], 'ru')
        self.assertEqual(ws.ingest_document(self.root, source, '2026-10')['status'], 'existing_content')
        self.assertEqual(self.run_native('verify')['indexed_documents'], 1)
        events = json.loads((ws._path(self.root, '09_audit/events.json')).read_text())
        self.assertEqual(len(events), 3)
        self.assertTrue(all(isinstance(event, dict) and 'action' in event for event in events))

    def test_native_resumes_python_workspace_preserves_facts_and_detects_orphan(self):
        ws.init_workspace(self.root, 2026, 'en', 'bookkeeping')
        before = (ws._path(self.root, ws.PROFILE)).read_bytes()
        result = self.run_native('start', Language='ru', Mode='general')
        self.assertEqual((result['language'], result['mode']), ('en', 'bookkeeping'))
        self.assertEqual((ws._path(self.root, ws.PROFILE)).read_bytes(), before)
        original = ws._path(self.root, '06_bookkeeping/2026/10/originals/orphan.csv')
        original.parent.mkdir(parents=True)
        original.write_bytes(b'unindexed')
        result = self.run_native('verify')
        self.assertEqual(result['status'], 'needs_review')
        self.assertEqual(result['unindexed_originals'], 1)
        self.assertEqual(original.read_bytes(), b'unindexed')

    def test_both_runtimes_give_the_same_setup_check(self):
        def summary(report):
            # The native helper cannot test write access without writing, so it reports not_checked.
            checks = {row['id']: row['result'] for row in report['checks'] if row['id'] != 'folder_writable'}
            return report['status'], report['folder']['state'], report['kit']['skills_missing'], checks
        cases = {'missing': lambda: None, 'empty': lambda: self.root.mkdir(),
                 'workspace': lambda: ws.start_workspace(self.root, year=2026, language='de'),
                 'has_files': lambda: (self.root.mkdir(), (self.root / 'invoice.pdf').write_bytes(b'%PDF'))}
        for state, prepare in cases.items():
            with self.subTest(state=state):
                if self.root.exists():
                    shutil.rmtree(self.root)
                prepare()
                native = self.run_native('setup-check')
                self.assertEqual(summary(native), summary(ws.setup_check(self.root)))
                self.assertEqual(native['folder']['state'], state)
                self.assertEqual(native['kit']['version'], (REPO / 'VERSION').read_text().strip())
                self.assertEqual(native['folder'].get('workspace', {}).get('folder_language'),
                                 'de' if state == 'workspace' else None)

    def test_both_runtimes_share_paths_numbering_and_integrity(self):
        for language, inbox, archive in [('ru', '01 Входящие', '02 Документы'), ('de', '01 Eingang', '02 Dokumente')]:
            with self.subTest(language=language):
                self.root = self.base / language
                self.run_native('start', Language=language, Year=2026)
                self.assertTrue((ws._path(self.root, inbox)).is_dir())
                self.assertTrue((ws._path(self.root, archive)).is_dir())
                source = ws._path(self.root, inbox) / 'example.csv'
                source.write_bytes(b'amount,currency\n12.34,EUR\n')
                filed = self.run_native('ingest', Source=source, Period='2026-10')
                self.assertEqual(filed['document_number'], '2026-00001')
                self.assertFalse(source.exists())
                self.assertEqual(ws.verify_workspace(self.root)['status'], 'ok')
                again = ws.ingest_document(self.root, self.root / filed['source_moved_to'], '2026-10')
                self.assertEqual((again['status'], again['source_moved_to']), ('existing_content', None))
                ws.configure_workspace(self.root, language='en')
                self.assertEqual(self.run_native('start', Language='de')['language'], 'en')
                self.assertEqual(self.run_native('verify')['status'], 'ok')
                orphan = ws._path(self.root, '06_bookkeeping/2026/10/originals/orphan.csv')
                orphan.write_bytes(b'preserve me')
                self.assertEqual(self.run_native('verify')['unindexed_originals'], 1)
                self.assertEqual(ws.verify_workspace(self.root)['unindexed_originals'], 1)
        self.root = self.base / 'python-first'
        ws.start_workspace(self.root, 2026, 'de')
        self.assertEqual(self.run_native('start')['status'], 'resumed')
        self.assertEqual(self.run_native('verify')['status'], 'ok')
