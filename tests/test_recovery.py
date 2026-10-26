"""Whole-workspace recovery preserves user records and rejects unsafe backups."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/de-business-kit/scripts'
sys.path.insert(0, str(SCRIPTS))
import workspace as ws
import recovery


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / 'private'
        ws.start_workspace(self.root, 2026, 'ru')
        (self.root / 'Личные заметки').mkdir()
        (self.root / 'Личные заметки/Проверка.txt').write_text('Synthetic user notes', encoding='utf-8')
        (self.root / 'Пустая папка').mkdir()
        source = self.base / 'original.csv'
        source.write_bytes(b'amount,currency\n119.80,EUR\n')
        ws.ingest_document(self.root, source, '2026-10')
        self.backup = self.base / 'backup'

    def files(self, root):
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}

    def test_roundtrip_restores_all_records_empty_folders_and_localized_identity(self):
        original = self.files(self.root)
        created = recovery.backup_workspace(self.root, self.backup)
        self.assertEqual(created['status'], 'verified')
        self.assertEqual(self.files(self.root), original)
        self.assertEqual(recovery.verify_backup(self.backup)['status'], 'verified')
        restored = self.base / 'restored'
        result = recovery.restore_workspace(self.backup, restored)
        self.assertEqual(self.files(restored), original)
        self.assertTrue((restored / 'Пустая папка').is_dir())
        self.assertFalse((restored / ws.LOCK).exists())
        self.assertEqual(result['original_integrity'], 'ok')
        self.assertEqual(ws.workspace_folders(restored)['folder_language'], 'ru')

    def test_modified_missing_and_extra_members_fail_before_restore_creates_destination(self):
        for damage in ('modified', 'missing', 'extra'):
            with self.subTest(damage=damage):
                target = self.base / ('backup-' + damage)
                recovery.backup_workspace(self.root, target)
                member = target / 'files/Личные заметки/Проверка.txt'
                if damage == 'modified': member.write_text('Changed')
                elif damage == 'missing': member.unlink()
                else: (target / 'files/unlisted.txt').write_text('Extra')
                restored = self.base / ('restore-' + damage)
                with self.assertRaises(ws.WorkspaceError):
                    recovery.restore_workspace(target, restored)
                self.assertFalse(restored.exists())

    def test_refuses_overwrite_nested_destination_and_active_workspace(self):
        for destination in (self.root, self.root / 'nested', self.base):
            with self.assertRaises(ws.WorkspaceError):
                recovery.backup_workspace(self.root, destination)
        with ws._locked(self.root):
            with self.assertRaises(ws.WorkspaceError):
                recovery.backup_workspace(self.root, self.backup)
        self.assertFalse(self.backup.exists())
        recovery.backup_workspace(self.root, self.backup)
        with self.assertRaises(ws.WorkspaceError):
            recovery.restore_workspace(self.backup, self.root)

    def test_restore_blocks_a_cooperative_writer_until_copy_verification_finishes(self):
        recovery.backup_workspace(self.root, self.backup)
        target = self.base / 'restore-locked'
        inventory = recovery._inventory
        attempts = []
        def inspect_then_write(root, exclude_lock=False):
            result = inventory(root, exclude_lock)
            if root == target:
                with self.assertRaises(ws.WorkspaceError):
                    ws.save_entry(root, 'tasks', {'schema_version': 1, 'id': 'concurrent',
                                  'title': 'Concurrent write', 'owner': 'owner', 'status': 'pending'})
                attempts.append(True)
            return result
        with mock.patch.object(recovery, '_inventory', side_effect=inspect_then_write):
            recovery.restore_workspace(self.backup, target)
        self.assertEqual(attempts, [True])
        self.assertEqual(self.files(target), self.files(self.root))

    def test_manifest_traversal_case_collisions_and_unlisted_metadata_rejected(self):
        for path in ('../outside', 'C:/outside', 'a\\b', 'CON.txt', 'a. /b'):
            with self.subTest(path=path):
                target = self.base / ('bad-' + str(len(list(self.base.glob('bad-*')))))
                recovery.backup_workspace(self.root, target)
                manifest = json.loads((target / 'manifest.json').read_text())
                manifest['files'][0]['path'] = path
                (target / 'manifest.json').write_text(json.dumps(manifest))
                with self.assertRaises(ws.WorkspaceError): recovery.verify_backup(target)
        target = self.base / 'collision'
        recovery.backup_workspace(self.root, target)
        manifest = json.loads((target / 'manifest.json').read_text())
        copy = dict(manifest['files'][0]); copy['path'] = copy['path'].upper()
        manifest['files'].append(copy)
        (target / 'manifest.json').write_text(json.dumps(manifest))
        with self.assertRaises(ws.WorkspaceError): recovery.verify_backup(target)
        recovery.backup_workspace(self.root, self.backup)
        (self.backup / 'unexpected.txt').write_text('Extra')
        with self.assertRaises(ws.WorkspaceError): recovery.verify_backup(self.backup)

    def test_source_change_stops_completion_and_preserves_the_original_change(self):
        original_file = recovery._file
        changed = self.root / 'Личные заметки/Проверка.txt'
        def copy_then_change(path, destination=None):
            result = original_file(path, destination)
            if destination is not None and path == changed:
                changed.write_text('Concurrent user correction', encoding='utf-8')
            return result
        with mock.patch.object(recovery, '_file', side_effect=copy_then_change):
            with self.assertRaises(ws.WorkspaceError):
                recovery.backup_workspace(self.root, self.backup)
        self.assertEqual(changed.read_text(), 'Concurrent user correction')
        self.assertFalse((self.backup / 'manifest.json').exists())
        self.assertFalse((self.root / ws.LOCK).exists())

    def test_linked_paths_are_not_followed(self):
        outside = self.base / 'outside.txt'; outside.write_text('Outside')
        link = self.root / 'linked.txt'
        try: link.symlink_to(outside)
        except (OSError, NotImplementedError): self.skipTest('Symlink creation unavailable')
        with self.assertRaises(ws.WorkspaceError): recovery.backup_workspace(self.root, self.backup)
        self.assertEqual(outside.read_text(), 'Outside')


import os
import shutil
import subprocess


@unittest.skipUnless(os.name == 'nt' or os.environ.get('GBK_TEST_DOCKER_IMAGE'),
                     'Native recovery requires Windows or an explicit developer container')
class NativeRecoveryInteropTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.repo = Path(__file__).resolve().parents[1]
        self.root = self.base / 'Private [workspace]'
        ws.start_workspace(self.root, 2026, 'de')
        (self.root / 'Synthetic notes.txt').write_text('Complete workspace', encoding='utf-8')

    def native(self, action, expect_success=True, **options):
        image = os.environ.get('GBK_TEST_DOCKER_IMAGE')
        if image:
            command = ['docker', 'run', '--rm', '--network', 'none', '-v', f'{self.repo}:{self.repo}:ro',
                       '-v', f'{self.base}:{self.base}', image, 'pwsh']
        else:
            command = [shutil.which('powershell.exe') or 'powershell.exe']
        command += ['-NoProfile', '-NonInteractive', '-File', str(SCRIPTS / 'recovery.ps1'), '-Action', action]
        for key, value in options.items(): command += ['-' + key, str(value)]
        result = subprocess.run(command, capture_output=True, timeout=60, encoding='utf-8')
        if expect_success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def test_python_backup_restores_natively_and_native_backup_restores_in_python(self):
        python_backup = self.base / 'Python [backup]'
        recovery.backup_workspace(self.root, python_backup)
        self.assertEqual(self.native('verify', Backup=python_backup)['status'], 'verified')
        native_restored = self.base / 'Native [restored]'
        self.assertEqual(self.native('restore', Backup=python_backup, Root=native_restored)['original_integrity'], 'ok')
        self.assertEqual(ws.workspace_folders(native_restored)['folder_language'], 'de')
        native_backup = self.base / 'Native [backup]'
        self.assertEqual(self.native('backup', Root=native_restored, Destination=native_backup)['status'], 'verified')
        self.assertEqual(recovery.verify_backup(native_backup)['status'], 'verified')
        restored = self.base / 'Python restored'
        recovery.restore_workspace(native_backup, restored)
        expected = {p.relative_to(self.root).as_posix(): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        actual = {p.relative_to(restored).as_posix(): p.read_bytes() for p in restored.rglob('*') if p.is_file()}
        self.assertEqual(actual, expected)

    def test_native_manifest_validation_rejects_traversal_collisions_and_unknown_versions(self):
        for number, damage in enumerate(('traversal', 'collision', 'boolean-version', 'extra')):
            target = self.base / ('bad-' + str(number))
            recovery.backup_workspace(self.root, target)
            manifest_path = target / 'manifest.json'
            value = json.loads(manifest_path.read_text())
            if damage == 'traversal': value['files'][0]['path'] = '../outside'
            elif damage == 'collision':
                duplicate = dict(value['files'][0]); duplicate['path'] = duplicate['path'].upper()
                value['files'].append(duplicate)
            elif damage == 'boolean-version': value['schema_version'] = True
            else: (target / 'unlisted.txt').write_text('Extra')
            manifest_path.write_text(json.dumps(value))
            restored = self.base / ('must-not-exist-' + str(number))
            self.native('restore', expect_success=False, Backup=target, Root=restored)
            self.assertFalse(restored.exists())
