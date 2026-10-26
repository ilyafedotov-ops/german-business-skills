"""Brief waits for cooperating writers and evidence-preserving stale-lock recovery."""
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts"
sys.path.insert(0, str(SCRIPTS))
import workspace as ws


def finished_pid():
    process = subprocess.Popen([sys.executable, "-c", "pass"])
    process.wait()
    return process.pid


class LockFixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "private"
        ws.init_workspace(self.root, 2026, "en")
        self.lock = self.root / ws.LOCK

    def leave_lock(self, pid, host=None, text=None):
        content = text if text is not None else json.dumps(
            {"pid": pid, "created_at": "2026-10-26T18:00:50.1234567Z", **({"host": host} if host else {})})
        self.lock.write_text(content, encoding="utf-8")
        return hashlib.sha256(content.encode("utf-8")).hexdigest()


class BoundedWaitTests(LockFixture):
    def test_writer_waits_for_a_lock_that_another_writer_releases(self):
        held, release = threading.Event(), threading.Event()

        def hold():
            with ws._locked(self.root):
                held.set()
                release.wait(5)
        holder = threading.Thread(target=hold)
        holder.start()
        held.wait(5)
        threading.Timer(0.4, release.set).start()
        ws.configure_workspace(self.root, language="ru")
        holder.join(5)
        self.assertEqual(ws.workspace_status(self.root)["language"], "ru")

    def test_writer_still_refuses_a_lock_held_beyond_the_wait(self):
        self.leave_lock(None, text="another operation")
        with patch.object(ws, "LOCK_WAIT_SECONDS", 0.3):
            started = time.monotonic()
            with self.assertRaisesRegex(ws.WorkspaceError, "locked"):
                ws.configure_workspace(self.root, language="ru")
        self.assertGreaterEqual(time.monotonic() - started, 0.3)
        self.assertEqual(self.lock.read_text(encoding="utf-8"), "another operation")


class LockDiagnosisTests(LockFixture):
    def test_lock_left_by_a_finished_process_on_this_computer_is_stale(self):
        digest = self.leave_lock(finished_pid(), socket.gethostname())
        result = ws.diagnose_workspace(self.root)
        self.assertEqual(result["lock"]["assessment"], "stale")
        self.assertEqual(result["lock"]["sha256"], digest)
        self.assertIn("unlock", result["next_action"])

    def test_lock_of_a_running_writer_is_active(self):
        with ws._locked(self.root):
            self.assertEqual(ws.diagnose_workspace(self.root)["lock"]["assessment"], "active")

    def test_other_computers_and_unreadable_locks_cannot_be_assessed(self):
        for content in ({"host": "another-computer", "pid": finished_pid()}, {"pid": finished_pid()}, {"text": "active writer"}):
            with self.subTest(content):
                self.leave_lock(content.get("pid"), content.get("host"), content.get("text"))
                self.assertEqual(ws.diagnose_workspace(self.root)["lock"]["assessment"], "unverifiable")


class UnlockTests(LockFixture):
    def test_unverifiable_lock_preserves_exact_opaque_bytes(self):
        data = b"legacy-token-\xff\x00"
        self.lock.write_bytes(data)
        result = ws.unlock_workspace(self.root, hashlib.sha256(data).hexdigest(), confirmed_no_writer=True)
        self.assertEqual((self.root / "09_audit/history" / (result["history_id"] + ".lock")).read_bytes(), data)

    def test_stale_lock_is_removed_with_history_and_writes_resume(self):
        pid = finished_pid()
        digest = self.leave_lock(pid, socket.gethostname())
        run = subprocess.run([sys.executable, "-B", str(SCRIPTS / "workspace.py"), "unlock", "--root", str(self.root),
                              "--expected-sha256", digest], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        result = json.loads(run.stdout)
        self.assertEqual(result["status"], "removed")
        self.assertFalse(self.lock.exists())
        history = json.loads((self.root / "09_audit/history" / (result["history_id"] + ".json")).read_text(encoding="utf-8"))
        self.assertEqual((history["lock"]["pid"], history["lock_sha256"]), (pid, digest))
        events = json.loads((self.root / ws.EVENTS).read_text(encoding="utf-8"))
        self.assertEqual(events[-1]["action"], "stale_lock_removed")
        ws.configure_workspace(self.root, language="ru")

    def test_active_changed_or_unconfirmed_locks_are_kept(self):
        with ws._locked(self.root):
            digest = hashlib.sha256(self.lock.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ws.WorkspaceError, "running"):
                ws.unlock_workspace(self.root, digest, confirmed_no_writer=True)
        stale = self.leave_lock(finished_pid(), socket.gethostname())
        with self.assertRaisesRegex(ws.WorkspaceError, "changed"):
            ws.unlock_workspace(self.root, "0" * 64)
        unverifiable = self.leave_lock(finished_pid(), "another-computer")
        with self.assertRaisesRegex(ws.WorkspaceError, "confirm"):
            ws.unlock_workspace(self.root, unverifiable)
        self.assertTrue(self.lock.exists())
        self.assertNotEqual(stale, unverifiable)
        self.assertEqual(ws.unlock_workspace(self.root, unverifiable, confirmed_no_writer=True)["status"], "removed")
        self.assertFalse(self.lock.exists())


if __name__ == "__main__":
    unittest.main()
