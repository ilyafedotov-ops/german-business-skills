"""Installer safety tests; these are not desktop-app integration tests."""

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).absolute().parents[1] / "tools" / "install.py"
SPEC = importlib.util.spec_from_file_location("business_skill_installer", SCRIPT)
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "package" / "de-business-kit"
        (self.source / "references").mkdir(parents=True)
        (self.source / "scripts").mkdir()
        (self.source / "SKILL.md").write_text(
            "---\nname: de-business-kit\ndescription: Test fixture.\n---\n"
            "Read references/intake.md.\n", encoding="utf-8")
        (self.source / "references" / "intake.md").write_text("Synthetic fixture.\n", encoding="utf-8")
        (self.source / "scripts" / "check.py").write_text("print('fixture')\n", encoding="utf-8")
        self.project = self.root / "private-business"
        self.project.mkdir()

    def run_install(self, **options):
        options.setdefault("target", "both")
        options.setdefault("scope", "project")
        if options["scope"] == "project":
            options.setdefault("project", self.project)
        return installer.install(source_skill=self.source, **options)

    def test_both_targets_preserve_resources_and_existing_configuration(self):
        (self.project / ".claude").mkdir()
        settings = self.project / ".claude" / "settings.json"
        settings.write_text('{"permissions": {}}\n', encoding="utf-8")
        instructions = self.project / "CLAUDE.md"
        instructions.write_text("Existing instructions.\n", encoding="utf-8")
        result = self.run_install()
        self.assertEqual(result, (
            self.project / ".agents" / "skills" / "de-business-kit",
            self.project / ".claude" / "skills" / "de-business-kit",
        ))
        for destination in result:
            for relative in ("SKILL.md", "references/intake.md", "scripts/check.py"):
                self.assertEqual((destination / relative).read_bytes(),
                                 (self.source / relative).read_bytes())
        self.assertEqual(settings.read_text(), '{"permissions": {}}\n')
        self.assertEqual(instructions.read_text(), "Existing instructions.\n")
        self.assertFalse((self.project / ".mcp.json").exists())

    def test_second_target_collision_creates_nothing_in_first_target(self):
        existing = self.project / ".claude" / "skills" / "de-business-kit"
        existing.mkdir(parents=True)
        marker = existing / "local-edits.txt"
        marker.write_text("Keep me.\n", encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(marker.read_text(), "Keep me.\n")
        self.assertEqual(list(existing.iterdir()), [marker])

    def test_reinstall_refuses_to_overwrite_modified_skill(self):
        destination, = self.run_install(target="codex")
        manifest = destination / "SKILL.md"
        manifest.write_text("User modified skill.\n", encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            self.run_install(target="codex")
        self.assertEqual(manifest.read_text(), "User modified skill.\n")

    def test_dry_run_has_no_filesystem_side_effects(self):
        paths = self.run_install(dry_run=True)
        self.assertEqual(len(paths), 2)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_install_does_not_try_to_create_existing_drive_root(self):
        original_mkdir = Path.mkdir

        def windows_root_mkdir(path, *args, **kwargs):
            if path == Path(path.anchor):
                raise PermissionError("Windows denies mkdir on an existing drive root")
            return original_mkdir(path, *args, **kwargs)

        with mock.patch.object(Path, "mkdir", windows_root_mkdir):
            destinations = self.run_install()
        for destination in destinations:
            self.assertEqual((destination / "SKILL.md").read_bytes(),
                             (self.source / "SKILL.md").read_bytes())

    def test_user_scope_accepts_explicit_home_without_global_changes(self):
        test_home = self.root / "test-home"
        test_home.mkdir()
        paths = self.run_install(scope="user", home=test_home)
        self.assertEqual(paths[0], test_home / ".agents" / "skills" / "de-business-kit")
        self.assertEqual(paths[1], test_home / ".claude" / "skills" / "de-business-kit")
        self.assertEqual(list(self.project.iterdir()), [])

    def test_project_scope_requires_project_and_rejects_parent_traversal(self):
        with self.assertRaises(installer.InstallError):
            installer.install(target="codex", scope="project", source_skill=self.source)
        with self.assertRaises(installer.InstallError):
            self.run_install(project=self.project / ".." / "elsewhere")
        self.assertFalse((self.root / "elsewhere").exists())

    def test_existing_parent_file_is_rejected_before_any_target_changes(self):
        blocker = self.project / ".claude"
        blocker.write_text("not a directory", encoding="utf-8")
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(blocker.read_text(), "not a directory")

    def _symlink(self, destination, source, is_directory=False):
        try:
            destination.symlink_to(source, target_is_directory=is_directory)
        except (OSError, NotImplementedError):
            self.skipTest("Creating symlinks is unavailable for this test user/platform")

    def test_source_symlink_is_rejected(self):
        self._symlink(self.source / "references" / "linked.md", self.source / "SKILL.md")
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertEqual(list(self.project.iterdir()), [])

    def test_destination_ancestor_symlink_is_rejected(self):
        external = self.root / "external"
        external.mkdir()
        self._symlink(self.project / ".claude", external, is_directory=True)
        with self.assertRaises(installer.InstallError):
            self.run_install()
        self.assertFalse((self.project / ".agents").exists())
        self.assertEqual(list(external.iterdir()), [])

    def test_dangling_destination_symlink_is_rejected(self):
        parent = self.project / ".agents" / "skills"
        parent.mkdir(parents=True)
        self._symlink(parent / "de-business-kit", self.root / "absent", is_directory=True)
        with self.assertRaises(installer.InstallError):
            self.run_install(target="codex")
        self.assertFalse((self.root / "absent").exists())


if __name__ == "__main__":
    unittest.main()
