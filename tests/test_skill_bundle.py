"""Complete-set installation and native preflight, using private synthetic roots."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from tools import install

ROOT = Path(__file__).resolve().parents[1]
SHELL = shutil.which('powershell.exe') or shutil.which('pwsh')
NAMES = ('de-business-kit', 'de-business-start', 'de-business-operations',
         'de-business-accounting', 'de-business-tax', 'de-business-services', 'de-business-changes')


class CompleteBundleTests(unittest.TestCase):
    def test_default_installer_delivers_complete_set_with_shared_core(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp).resolve()
            paths = install.install(target='both', scope='project', project=target)
            self.assertEqual(len(paths), 14)
            for host in ('.agents', '.claude'):
                folder = target / host / 'skills'
                self.assertEqual({p.name for p in folder.iterdir()}, set(NAMES))
                for name in NAMES:
                    self.assertEqual((folder / name / 'SKILL.md').read_bytes(),
                                     (ROOT / 'skills' / name / 'SKILL.md').read_bytes())
                self.assertTrue((folder / 'de-business-kit/references/shared-context.md').is_file())


@unittest.skipUnless(SHELL, 'No PowerShell available; native Windows acceptance remains separate')
class NativeBundleTests(unittest.TestCase):
    def setUp(self):
        # Deep per-user macOS temp roots hit the 90s limit in local trials;
        # use a short canonical root with the same production path checks.
        temp = tempfile.TemporaryDirectory(dir="/private/tmp" if sys.platform == "darwin" else None)
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name).resolve()
        self.source = self.base / 'source'
        shutil.copytree(ROOT / 'skills', self.source)
        self.target = self.base / 'target'
        self.target.mkdir()

    def invoke(self, *extra):
        return subprocess.run([SHELL, '-NoProfile', '-NonInteractive', '-File',
            str(self.source / 'de-business-kit/scripts/windows.ps1'), '-Action', 'install',
            '-Root', str(self.target), '-Target', 'both', *extra],
            capture_output=True, text=True, encoding='utf-8', timeout=90)

    def test_dry_run_then_detached_complete_install(self):
        preview = self.invoke('-DryRun')
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(len(json.loads(preview.stdout)['destinations']), 14)
        self.assertEqual(list(self.target.iterdir()), [])
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stderr)
        shutil.rmtree(self.source)
        for host in ('.agents', '.claude'):
            for name in NAMES:
                self.assertTrue((self.target / host / 'skills' / name / 'SKILL.md').is_file())
        detached = self.target / '.agents/skills/de-business-kit/scripts/windows.ps1'
        other = self.base / 'other'
        other.mkdir()
        repeat = subprocess.run([SHELL, '-NoProfile', '-NonInteractive', '-File', str(detached),
            '-Action', 'install', '-Root', str(other), '-DryRun'], capture_output=True,
            text=True, encoding='utf-8', timeout=90)
        self.assertEqual(repeat.returncode, 0, repeat.stderr)

    def test_missing_sibling_or_cross_bundle_link_refuses_before_writes(self):
        sibling = self.source / 'de-business-tax'
        entry = sibling / 'SKILL.md'
        entry.write_text(entry.read_text() + '\n[Escaping](../../outside.md)\n')
        (self.base / 'outside.md').write_text('Not part of the bundle')
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.target.iterdir()), [])
        shutil.rmtree(sibling)
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_late_sibling_collision_preserves_all_existing_work(self):
        occupied = self.target / '.claude/skills/de-business-changes'
        occupied.mkdir(parents=True)
        (occupied / 'keep.txt').write_text('User work')
        result = self.invoke()
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.target / '.agents').exists())
        self.assertFalse((occupied.parent / 'de-business-kit').exists())
        self.assertEqual((occupied / 'keep.txt').read_text(), 'User work')
