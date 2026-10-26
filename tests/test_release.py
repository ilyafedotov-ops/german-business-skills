"""Release gates exercise real files, Git tags and distributable bytes."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name).resolve()
        self.repo = self.base / 'source'
        self.repo.mkdir()
        for name in ('tools', 'skills', 'packaging', '.claude-plugin'):
            shutil.copytree(ROOT / name, self.repo / name)
        for name in ('plugin.json', 'LICENSE', 'VERSION', 'CHANGELOG.md', 'CHANGELOG.ru.md'):
            shutil.copyfile(ROOT / name, self.repo / name)
        self.git('init', '-q')
        self.git('config', 'user.email', 'synthetic@example.invalid')
        self.git('config', 'user.name', 'Synthetic release test')
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        self.version = (self.repo / 'VERSION').read_text().strip()
        self.tag = 'v' + self.version
        self.git('-c', 'tag.gpgsign=false', 'tag', self.tag)

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.repo), *args], text=True).strip()

    def run_tool(self, *args, ok=True):
        result = subprocess.run([sys.executable, '-B', str(self.repo / 'tools/release.py'), *args],
                                capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0 if ok else 2, result.stdout + result.stderr)
        return result

    def test_reproducible_release_records_exact_commit_and_all_archive_files(self):
        for name in ('first', 'second'):
            self.run_tool('prepare', '--tag', self.tag, '--output', str(self.base / name))
        first, second = self.base / 'first', self.base / 'second'
        for path in first.iterdir():
            self.assertEqual(path.read_bytes(), (second / path.name).read_bytes())
        metadata = json.loads((first / 'release.json').read_text())
        self.assertEqual(metadata['source_commit'], self.git('rev-parse', 'HEAD'))
        self.assertEqual(metadata['version'], self.version)
        for host in ('codex', 'claude'):
            archive = first / f'de-business-kit-{self.version}-{host}.zip'
            with zipfile.ZipFile(archive) as stream:
                prefix = f'{host}/plugins/de-business-kit/'
                inventory = json.loads(stream.read(prefix + 'FILE-MANIFEST.json'))
                self.assertEqual(inventory['version'], self.version)
                actual = {name[len(prefix):]: hashlib.sha256(stream.read(name)).hexdigest()
                          for name in stream.namelist() if name.startswith(prefix)
                          and name != prefix + 'FILE-MANIFEST.json'}
                self.assertEqual(inventory['files'], actual)
        self.run_tool('verify', '--directory', str(first))
        archive.write_bytes(archive.read_bytes() + b'tampered')
        self.run_tool('verify', '--directory', str(first), ok=False)

    def test_mismatched_version_and_invalid_semver_fail_before_build(self):
        for version in ('01.2.3', '1.2', '1.2.3-preview.01', '9.0.0'):
            (self.repo / 'VERSION').write_text(version + '\n')
            self.run_tool('check', ok=False)
        self.assertFalse((self.base / 'build').exists())

    def test_wrong_tag_dirty_tree_and_missing_notes_fail_closed(self):
        self.run_tool('check', '--tag', 'v9.0.0', ok=False)
        (self.repo / 'LICENSE').write_text('changed')
        self.run_tool('prepare', '--tag', self.tag, '--output', str(self.base / 'build'), ok=False)
        self.assertFalse((self.base / 'build').exists())
        self.git('checkout', '--', 'LICENSE')
        (self.repo / 'CHANGELOG.ru.md').write_text('# Missing release\n')
        self.run_tool('check', ok=False)

    def test_tag_at_another_commit_is_rejected(self):
        (self.repo / 'LICENSE').write_text('changed')
        self.git('add', 'LICENSE')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'second')
        self.run_tool('check', '--tag', self.tag, ok=False)

    def test_checksum_manifest_cannot_escape_or_ignore_extra_files(self):
        directory = self.base / 'download'
        directory.mkdir()
        (directory / 'SHA256SUMS').write_text('0' * 64 + '  ../outside\n')
        self.run_tool('verify', '--directory', str(directory), ok=False)
        self.run_tool('prepare', '--tag', self.tag, '--output', str(self.base / 'valid'))
        (self.base / 'valid' / 'unexpected.zip').write_bytes(b'untrusted')
        self.run_tool('verify', '--directory', str(self.base / 'valid'), ok=False)


if __name__ == '__main__':
    unittest.main()
