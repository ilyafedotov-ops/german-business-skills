"""Native archive integrity and output boundaries; no interpreter installation."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import os
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import package_gui


class GuiPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.bundle = self.base / 'application'
        self.bundle.mkdir()
        (self.bundle / 'GermanBusinessKit.exe').write_bytes(b'synthetic executable fixture')
        self.manifest = {'version':(ROOT/'VERSION').read_text().strip(), 'platform':'win32',
                         'architecture':'AMD64', 'files':{'GermanBusinessKit.exe':hashlib.sha256((self.bundle/'GermanBusinessKit.exe').read_bytes()).hexdigest()}, 'symlinks':{}}
        self.save_manifest()

    def save_manifest(self):
        (self.bundle/'GUI-MANIFEST.json').write_text(json.dumps(self.manifest))

    def test_archive_checksum_covers_verified_application_and_refuses_overwrite(self):
        archive = package_gui.package(self.bundle, self.base/'archive')
        digest = (archive.parent/(archive.name+'.sha256')).read_text().split()[0]
        self.assertEqual(digest, hashlib.sha256(archive.read_bytes()).hexdigest())
        with self.assertRaises(ValueError):
            package_gui.package(self.bundle, self.base/'archive')

    def test_tampered_missing_and_unlisted_binary_bytes_are_rejected(self):
        binary = self.bundle/'GermanBusinessKit.exe'
        binary.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            package_gui.package(self.bundle, self.base/'archive')
        binary.unlink()
        with self.assertRaises(ValueError):
            package_gui.package(self.bundle, self.base/'archive')
        (self.bundle/'extra.txt').write_text('unexpected')
        with self.assertRaises(ValueError):
            package_gui.package(self.bundle, self.base/'archive')

    @unittest.skipUnless(hasattr(os, 'mkfifo'), 'FIFOs are not supported on Windows')
    def test_special_files_are_never_archived(self):
        os.mkfifo(self.bundle/'unmanifested-pipe')
        self.manifest.update(platform='darwin', architecture='arm64')
        self.save_manifest()
        with self.assertRaises(ValueError):
            package_gui.package(self.bundle, self.base/'archive')

    def test_changed_bytes_during_archive_are_not_accepted(self):
        original = package_gui.zipfile.ZipFile.write
        def changed(archive, filename, *args, **kwargs):
            if Path(filename).name == 'GermanBusinessKit.exe':
                Path(filename).write_bytes(b'changed after validation')
            return original(archive, filename, *args, **kwargs)
        with patch.object(package_gui.zipfile.ZipFile, 'write', changed):
            with self.assertRaises(ValueError):
                package_gui.package(self.bundle, self.base/'archive')
        self.assertEqual(list((self.base/'archive').glob('*.sha256')), [])

    def test_escaping_native_symlink_is_rejected(self):
        target = self.base/'outside.txt'
        target.write_text('outside')
        try:
            (self.bundle/'library').symlink_to(target)
        except OSError:
            self.skipTest('Symlink creation unavailable on this Windows test account')
        self.manifest['symlinks']['library'] = str(target)
        self.save_manifest()
        with self.assertRaises(ValueError):
            package_gui.package(self.bundle, self.base/'archive')


if __name__ == '__main__':
    unittest.main()
