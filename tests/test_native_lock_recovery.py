"""Developer cross-runtime checks for the standalone native lock recovery route."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/de-business-kit/scripts'
sys.path.insert(0, str(SCRIPTS))
import workspace as ws

NATIVE = shutil.which('powershell.exe') if os.name == 'nt' else os.environ.get('GBK_TEST_NATIVE_PWSH')


@unittest.skipUnless(NATIVE, 'Requires Windows PowerShell or explicit GBK_TEST_NATIVE_PWSH')
class NativeLockRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / 'Private [workspace]'
        ws.start_workspace(self.root, 2026, 'ru')
        self.lock = self.root / ws.LOCK
        self.events = ws._path(self.root, ws.EVENTS)
        process = subprocess.Popen([sys.executable, '-c', 'pass'])
        process.wait()
        self.ended_pid = process.pid

    def native(self, action, success=True, **options):
        args = [NATIVE, '-NoProfile', '-NonInteractive', '-File', str(SCRIPTS / 'windows.ps1'),
                '-Action', action, '-Root', str(self.root)]
        for key, value in options.items():
            args.append('-' + key)
            if value is not True:
                args.append(str(value))
        result = subprocess.run(args, capture_output=True, text=True, timeout=45)
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        return result.stderr

    def leave(self, pid=None, host=None, raw=None):
        data = raw if raw is not None else json.dumps({'pid': pid or self.ended_pid,
            'host': host or socket.gethostname(), 'created_at': '2026-10-26T18:00:50.1234567Z'}).encode()
        self.lock.write_bytes(data)
        return hashlib.sha256(data).hexdigest()

    def test_stale_recovery_preserves_history_audit_and_resume(self):
        before = self.events.read_bytes()
        digest = self.leave()
        status = self.native('lock-status')
        self.assertEqual((status['lock']['assessment'], status['lock']['sha256']), ('stale', digest))
        self.assertEqual(self.events.read_bytes(), before)
        result = self.native('unlock', ExpectedSha256=digest)
        self.assertFalse(self.lock.exists())
        history = json.loads(ws._path(self.root, '09_audit/history/' + result['history_id'] + '.json').read_text())
        self.assertEqual(history['lock']['pid'], self.ended_pid)
        self.assertEqual(history['lock_sha256'], digest)
        self.assertEqual(json.loads(self.events.read_text())[-1]['action'], 'stale_lock_removed')
        self.assertEqual(self.native('start')['status'], 'resumed')
        self.assertIsNone(self.native('lock-status')['lock'])

    def test_active_changed_and_unconfirmed_locks_are_kept(self):
        for pid, host, expected, confirm in [
            (os.getpid(), socket.gethostname(), None, True),
            (self.ended_pid, socket.gethostname(), '0' * 64, True),
            (self.ended_pid, 'another-computer', None, False),
        ]:
            with self.subTest(pid=pid, host=host, expected=expected):
                digest = self.leave(pid, host)
                before = self.lock.read_bytes(), self.events.read_bytes()
                options = {'ExpectedSha256': expected or digest}
                if confirm:
                    options['ConfirmedNoWriter'] = True
                self.native('unlock', success=False, **options)
                self.assertEqual((self.lock.read_bytes(), self.events.read_bytes()), before)
        self.assertEqual(self.native('unlock', ExpectedSha256=digest, ConfirmedNoWriter=True)['status'], 'removed')

    def test_legacy_invalid_bytes_need_confirmation_and_preserve_exact_evidence(self):
        raw = b'legacy-token-\xff\x00'
        digest = self.leave(raw=raw)
        self.assertEqual(self.native('lock-status')['lock']['assessment'], 'unverifiable')
        self.native('unlock', success=False, ExpectedSha256=digest)
        result = self.native('unlock', ExpectedSha256=digest, ConfirmedNoWriter=True)
        evidence = ws._path(self.root, '09_audit/history/' + result['history_id'] + '.lock')
        self.assertEqual(evidence.read_bytes(), raw)

    def test_changed_lock_during_move_is_restored_and_refused(self):
        digest = self.leave()
        script = Path(self.temp.name) / 'race.ps1'
        script.write_text(r"""
param($Kit, $Root, $Digest)
. $Kit -Action lock-status -Root $Root | Out-Null
$ExpectedSha256=$Digest
$originalRead=${function:LockBytes}
function LockBytes([string]$path) {
    if ([IO.Path]::GetFileName($path).StartsWith('.stale-lock-')) {
        [IO.File]::WriteAllText($path, 'replacement-lock', (New-Object Text.UTF8Encoding($false)))
    }
    & $originalRead $path
}
try { UnlockWorkspace | Out-Null; throw 'UNEXPECTED_SUCCESS' }
catch {
    if ($_.Exception.Message -notlike '*changed during removal*') { throw }
}
""", encoding='utf-8')
        result = subprocess.run([NATIVE, '-NoProfile', '-NonInteractive', '-File', str(script),
                                 str(SCRIPTS / 'windows.ps1'), str(self.root), digest],
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.lock.read_bytes(), b'replacement-lock')
        self.assertFalse(list(self.root.glob('.stale-lock-*')))
        self.assertEqual(len(json.loads(self.events.read_text())), 1)

    def test_concurrent_writer_after_move_keeps_both_locks(self):
        digest = self.leave()
        original = self.lock.read_bytes()
        script = Path(self.temp.name) / 'race.ps1'
        script.write_text(r"""
param($Kit, $Root, $Digest)
. $Kit -Action lock-status -Root $Root | Out-Null
$ExpectedSha256=$Digest
$originalOpen=${function:OpenNativeLock}
function OpenNativeLock([string]$path) {
    [IO.File]::WriteAllText($path, 'concurrent-writer', (New-Object Text.UTF8Encoding($false)))
    & $originalOpen $path
}
$failed=$false
try { UnlockWorkspace | Out-Null } catch { $failed=$true }
if (-not $failed) { throw 'Concurrent writer was displaced' }
""", encoding='utf-8')
        result = subprocess.run([NATIVE, '-NoProfile', '-NonInteractive', '-File', str(script),
                                 str(SCRIPTS / 'windows.ps1'), str(self.root), digest],
                                capture_output=True, text=True, timeout=45)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.lock.read_bytes(), b'concurrent-writer')
        moved = list(self.root.glob('.stale-lock-*'))
        self.assertEqual(len(moved), 1)
        self.assertEqual(moved[0].read_bytes(), original)
        self.assertEqual(len(json.loads(self.events.read_text())), 1)

    def test_corrupt_audit_blocks_recovery_before_lock_moves(self):
        digest = self.leave()
        self.events.write_bytes(b'[null]')
        before = self.lock.read_bytes()
        self.assertIn('Invalid audit log', self.native('unlock', success=False, ExpectedSha256=digest))
        self.assertEqual(self.lock.read_bytes(), before)
        self.assertEqual(self.events.read_bytes(), b'[null]')
        self.assertFalse(list(self.root.glob('.stale-lock-*')))


if __name__ == '__main__':
    unittest.main()
