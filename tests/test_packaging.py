"""Offline package/resource checks; not host discovery or desktop acceptance."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).absolute().parents[1]
BUILDER = ROOT / "tools" / "build_package.py"


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.source = self.base / "source"
        self.source.mkdir()
        for name in ("plugin.json", ".claude-plugin/plugin.json", "LICENSE",
                     "packaging/README.md", "packaging/README.ru.md", "VERSION"):
            target = self.source / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        shutil.copytree(ROOT / "skills", self.source / "skills")

    def build(self, output=None, success=True):
        output = output if output is not None else self.base / "build"
        result = subprocess.run(
            [sys.executable, "-B", str(BUILDER), "--source", str(self.source),
             "--output", str(output)], capture_output=True, text=True, encoding="utf-8")
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("Package build stopped:", result.stderr)
        return output

    def test_bundle_keeps_sibling_skill_links_after_source_removal(self):
        import re
        sibling = self.source / "skills/de-business-tax"
        sibling.mkdir(exist_ok=True)
        (sibling / "SKILL.md").write_text(
            "---\nname: de-business-tax\ndescription: Tax fixture.\n---\n"
            "[Shared](../de-business-kit/references/intake.md)\n")
        (sibling / "agents").mkdir(exist_ok=True)
        (sibling / "agents/openai.yaml").write_text('interface:\n  display_name: "Tax"\n')
        output = self.build()
        shutil.rmtree(self.source)
        for host in ("codex", "claude"):
            with zipfile.ZipFile(output / (host + ".zip")) as archive:
                names = set(archive.namelist())
                prefix = host + "/plugins/de-business-kit/skills/"
                self.assertIn(prefix + "de-business-tax/SKILL.md", names)
                self.assertIn(prefix + "de-business-kit/references/intake.md", names)

    def test_bundle_rejects_missing_skill(self):
        catalog = self.source / "skills/de-business-kit/assets/skill-set.json"
        catalog.write_text(json.dumps({"schema_version": 1,
            "skills": ["de-business-kit", "de-business-missing"]}))
        self.build(success=False)
        self.assertFalse((self.base / "build").exists())

    def test_sibling_reference_cannot_escape_package(self):
        sibling = self.source / "skills/de-business-tax/SKILL.md"
        sibling.write_text(sibling.read_text() + "\n[Private](../../LICENSE)\n")
        self.build(success=False)
        self.assertFalse((self.base / "build").exists())

    def test_extracted_host_packages_resolve_marketplaces_and_run_without_checkout(self):
        output = self.build()
        shutil.rmtree(self.source)
        for host in ("codex", "claude"):
            with self.subTest(host=host):
                extracted = self.base / (host + "-extracted")
                with zipfile.ZipFile(output / (host + ".zip")) as archive:
                    archive.extractall(extracted)
                marketplace_root = extracted / host
                catalog_name = ".agents/plugins/marketplace.json" if host == "codex" else ".claude-plugin/marketplace.json"
                catalog = json.loads((marketplace_root / catalog_name).read_text(encoding="utf-8"))
                entry, = catalog["plugins"]
                source_path = entry["source"]["path"] if host == "codex" else entry["source"]
                plugin = marketplace_root / source_path
                self.assertTrue(plugin.resolve().is_relative_to(marketplace_root.resolve()))
                manifest_path = "plugin.json" if host == "codex" else ".claude-plugin/plugin.json"
                manifest = json.loads((plugin / manifest_path).read_text(encoding="utf-8"))
                self.assertEqual(manifest["name"], entry["name"])
                self.assertEqual(manifest["version"], (ROOT / "VERSION").read_text().strip())
                for readme in ("README.md", "README.ru.md"):
                    content = (plugin / readme).read_bytes()
                    self.assertEqual(content, (ROOT / "packaging" / readme).read_bytes())
                    other = "README.ru.md" if readme == "README.md" else "README.md"
                    self.assertIn(("(" + other + ")").encode(), content)
                skill = plugin / "skills/de-business-kit"
                self.assertTrue((skill / "assets/readable-document.html").is_file())
                locales = json.loads((skill / "assets/locales.json").read_text(encoding="utf-8"))
                for script, arguments in (("workflows.py", ["catalog"]),
                                          ("workflows.py", ["template", "--kind", "international"]),
                                          ("payments.py", ["template"])):
                    result = subprocess.run([sys.executable, "-B", str(skill / "scripts" / script), *arguments],
                                            cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["schema_version"], 1)
                for language in ("en", "ru"):
                    for template in locales["languages"][language]["templates"].values():
                        self.assertTrue((skill / "assets" / template).is_file())
                    private = self.base / (host + "-" + language + "-private")
                    result = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/workspace.py"),
                         "init", "--root", str(private), "--year", "2026", "--language", language],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    status = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/workspace.py"),
                         "status", "--root", str(private)], cwd=self.base,
                        capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(status.returncode, 0, status.stderr)
                    self.assertEqual(json.loads(status.stdout)["language"], language)
                    choice = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/desk.py"), "accounting-status", "--root", str(private)],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(choice.returncode, 0, choice.stderr)
                    self.assertEqual(json.loads(choice.stdout)["accounting_system"], "undecided")
                    overview = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/desk.py"), "overview", "--root", str(private), "--period", "2026-10"],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(overview.returncode, 0, overview.stderr)
                    view = json.loads(overview.stdout)
                    self.assertTrue((private / view["html_path"]).is_file())
                    snapshot = json.loads((private / Path(view["html_path"]).with_suffix('.json')).read_text(encoding="utf-8"))
                    self.assertEqual(snapshot["capabilities"]["elster_submission"], "not_implemented")
                    backup = self.base / (host + "-" + language + "-backup")
                    recovered = self.base / (host + "-" + language + "-restored")
                    for args in (["backup", "--root", str(private), "--destination", str(backup)],
                                 ["restore", "--backup", str(backup), "--root", str(recovered)]):
                        recovery = subprocess.run([sys.executable, "-B", str(skill / "scripts/recovery.py"), *args],
                                                  cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                        self.assertEqual(recovery.returncode, 0, recovery.stderr)
                    self.assertEqual((private / Path(view["html_path"]).with_name("workspace.json")).read_bytes(),
                                     (recovered / Path(view["html_path"]).with_name("workspace.json")).read_bytes())
                    for native in ("windows-overview.ps1", "windows-locks.ps1", "recovery.ps1"):
                        self.assertTrue((skill / "scripts" / native).is_file())
                    source_folder = self.base / (host + "-" + language + "-existing")
                    source_folder.mkdir()
                    (source_folder / "invoice.pdf").write_bytes(b"Synthetic preserved file")
                    scanned = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/desk.py"), "scan-folder", "--root", str(private), "--source", str(source_folder)],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(scanned.returncode, 0, scanned.stderr)
                    self.assertEqual(json.loads(scanned.stdout)["counts"]["candidate"], 1)
                    seed = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/workflows.py"), "template", "--kind", "classification"],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(seed.returncode, 0, seed.stderr)
                    request = json.loads(seed.stdout)
                    request.update(record_id="packaged-synthetic", period="2026-10")
                    folders = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/workspace.py"), "folders", "--root", str(private)],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(folders.returncode, 0, folders.stderr)
                    inbox = json.loads(folders.stdout)["paths"]["00_admin/inbox"]
                    (private / inbox / "request.json").write_text(json.dumps(request), encoding="utf-8")
                    prepared = subprocess.run(
                        [sys.executable, "-B", str(skill / "scripts/workflows.py"), "prepare", "--root", str(private),
                         "--kind", "classification", "--input", "00_admin/inbox/request.json"],
                        cwd=self.base, capture_output=True, text=True, encoding="utf-8")
                    self.assertEqual(prepared.returncode, 0, prepared.stderr)
                    result = json.loads(prepared.stdout)
                    self.assertEqual(result["status"], "needs_review")
                    report = (private / result["markdown_path"]).read_text(encoding="utf-8")
                    self.assertIn("Подготовка" if language == "ru" else "Preparation", report)

    def test_archives_are_byte_deterministic_and_include_only_reviewed_resources(self):
        (self.source / ".env").write_text("DO_NOT_SHIP=synthetic\n", encoding="utf-8")
        (self.source / "private-record.json").write_text("{}\n", encoding="utf-8")
        first = self.build(self.base / "first")
        second = self.build(self.base / "second")
        for host in ("codex", "claude"):
            archive = first / (host + ".zip")
            self.assertEqual(archive.read_bytes(), (second / archive.name).read_bytes())
            with zipfile.ZipFile(archive) as package:
                names = package.namelist()
                self.assertEqual(names, sorted(names))
                self.assertFalse(any(".env" in name or "private-record" in name for name in names))
                self.assertFalse(any("hooks" in name or "mcp.json" in name for name in names))
                archived = package.read(host + "/plugins/de-business-kit/skills/de-business-kit/SKILL.md")
                self.assertEqual(archived, (self.source / "skills/de-business-kit/SKILL.md").read_bytes())
            self.assertIn(hashlib.sha256(archive.read_bytes()).hexdigest(),
                          (first / "SHA256SUMS").read_text(encoding="utf-8"))
        for source in (self.source / "skills/de-business-kit").rglob("*"):
            if source.is_file():
                relative = source.relative_to(self.source / "skills/de-business-kit")
                for host in ("codex", "claude"):
                    self.assertEqual(source.read_bytes(),
                                     (first / host / "plugins/de-business-kit/skills/de-business-kit" / relative).read_bytes())

    def test_installation_guides_keep_local_images_after_source_removal(self):
        import re
        output = self.build()
        shutil.rmtree(self.source)
        for host in ("codex", "claude"):
            extracted = self.base / (host + "-guide")
            with zipfile.ZipFile(output / (host + ".zip")) as archive:
                archive.extractall(extracted)
            guides = extracted / host / "plugins/de-business-kit/skills/de-business-kit/guides"
            for language in ("en", "ru"):
                guide = (guides / ("install." + language + ".md")).read_text(encoding="utf-8")
                images = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", guide)
                self.assertGreaterEqual(len(images), 2)
                for image in images:
                    local = (guides / image).resolve()
                    self.assertTrue(local.is_relative_to(guides))
                    self.assertEqual(local.read_bytes(),
                                     (ROOT / "skills/de-business-kit/guides" / image).read_bytes())

    def test_unreviewed_images_and_sibling_lookalikes_stop_packaging(self):
        for relative in ("de-business-kit/guides/images/unreviewed.png",
                         "de-business-kit/guides/images/unreviewed.svg",
                         "de-business-tax/guides/images/setup-map.en.svg"):
            with self.subTest(relative=relative):
                extra = self.source / "skills" / relative
                extra.parent.mkdir(parents=True, exist_ok=True)
                extra.write_bytes(b"unreviewed resource")
                try:
                    output = self.build(success=False)
                    self.assertFalse(output.exists())
                finally:
                    extra.unlink()

    def test_unreviewed_html_resource_still_stops_packaging(self):
        (self.source / "skills/de-business-kit/assets/unreviewed.html").write_text("<script>synthetic</script>")
        output = self.build(success=False)
        self.assertFalse(output.exists())

    def test_existing_output_is_preserved(self):
        output = self.base / "existing"
        output.mkdir()
        marker = output / "keep.txt"
        marker.write_text("local edits\n", encoding="utf-8")
        self.build(output, success=False)
        self.assertEqual(list(output.iterdir()), [marker])
        self.assertEqual(marker.read_text(encoding="utf-8"), "local edits\n")

    def test_parent_traversal_and_output_inside_source_are_rejected_before_writes(self):
        for output in (self.base / "missing" / ".." / "escape", self.source / "build"):
            with self.subTest(output=output):
                self.build(output, success=False)
                self.assertFalse(output.exists())
        self.assertFalse((self.base / "missing").exists())

    def test_manifest_version_mismatch_or_new_capability_requires_review(self):
        path = self.source / ".claude-plugin/plugin.json"
        original = json.loads(path.read_text(encoding="utf-8"))
        for change in ({"version": "different"}, {"hooks": "./hooks.json"}):
            with self.subTest(change=change):
                path.write_text(json.dumps(dict(original, **change)), encoding="utf-8")
                output = self.build(success=False)
                self.assertFalse(output.exists())

    def test_missing_runtime_resource_stops_build_before_output(self):
        (self.source / "skills/de-business-kit/assets/locales.json").unlink()
        output = self.build(success=False)
        self.assertFalse(output.exists())

    @unittest.skipIf(sys.platform == "win32", "Windows prevents creating this unsafe fixture")
    def test_windows_separator_in_source_name_cannot_create_unsafe_archive(self):
        resource = self.source / "skills/de-business-kit/references" / "nested\\..\\escape.md"
        resource.write_text("synthetic unsafe filename\n", encoding="utf-8")
        output = self.build(success=False)
        self.assertFalse(output.exists())

    def test_symlinked_source_and_output_ancestor_are_rejected(self):
        elsewhere = self.base / "elsewhere"
        elsewhere.mkdir()
        linked = self.source / "skills/de-business-kit/references/linked.md"
        alias = self.base / "alias"
        try:
            linked.symlink_to(self.source / "LICENSE")
            alias.symlink_to(elsewhere, target_is_directory=True)
        except (OSError, NotImplementedError):
            self.skipTest("Symlink creation unavailable on this platform/account")
        output = self.build(success=False)
        self.assertFalse(output.exists())
        linked.unlink()
        self.build(alias / "build", success=False)
        self.assertEqual(list(elsewhere.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
