"""Offline documentation links are checked against real, synthetic files."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tools.check_doc_links import check_paths, repository_markdown_paths


ROOT = Path(__file__).resolve().parents[1]


class DocLinksTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def write(self, name, text=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_relative_files_directories_fragments_and_percent_encoding(self):
        self.write("guides/My guide.md", "# Über `cash` and **VAT**\n")
        self.write("assets/logo.svg", "<svg/>")
        source = self.write("README.md", """# Start
[guide](guides/My%20guide.md#%C3%BCber-cash-and-vat)
[titled](<guides/My guide.md#über-cash-and-vat> "Guide")
[image](assets/logo.svg) [folder](guides/) [here](#start)
""")
        result = check_paths([source])
        self.assertEqual(result.errors, [])
        self.assertEqual((result.files, result.links), (1, 5))

    def test_missing_file_and_unknown_fragment_fail_with_source_location(self):
        source = self.write("README.md", "# Start\n[missing](gone.md)\n[wrong](#absent)\n")
        result = check_paths([source])
        self.assertEqual(len(result.errors), 2)
        self.assertIn("README.md:2: missing path: gone.md", result.errors[0])
        self.assertIn("README.md:3: missing anchor: #absent", result.errors[1])

    def test_unicode_code_emphasis_and_duplicate_heading_anchors(self):
        source = self.write("README.md", """# Привет: `налог` и _учёт_
# Same
# Same
# Same-1
Setext `code`
-------------
[unicode](#привет-налог-и-учёт) [first](#same) [second](#same-1)
[collision](#same-1-1) [setext](#setext-code)
""")
        self.assertEqual(check_paths([source]).errors, [])

    def test_external_protocols_are_ignored_without_network(self):
        source = self.write("README.md", """[web](https://invalid.example/missing#no)
[email](mailto:synthetic@example.invalid) [custom](plugin://not-installed)
[network](//invalid.example/path) [ftp](ftp://invalid.example/file)
""")
        result = check_paths([source])
        self.assertEqual((result.links, result.errors), (0, []))

    def test_code_examples_do_not_create_links_or_headings(self):
        source = self.write("README.md", """# Real
`[inline](missing.md)`
````markdown
# Phantom
[example](missing.md)
````
    [indented](missing.md)
[real](#real)
""")
        result = check_paths([source])
        self.assertEqual((result.links, result.errors), (1, []))
        source.write_text(source.read_text() + "[wrong](#phantom)\n", encoding="utf-8")
        self.assertEqual(len(check_paths([source]).errors), 1)

    def test_reference_links_html_anchors_and_balanced_parentheses(self):
        self.write("notes (draft).md", '<a id="explicit-anchor"></a>\n')
        source = self.write("README.md", """[read][guide] [guide][] [guide]
[guide]: <notes (draft).md#explicit-anchor> "Notes"
[parentheses](notes%20(draft).md#explicit-anchor)
""")
        result = check_paths([source])
        self.assertEqual((result.links, result.errors), (4, []))

    def test_default_inventory_excludes_skill_runtime_and_dependencies(self):
        names = ["README.md", "docs/index.md", "docs/nested/detail.md", "packaging/codex/README.md"]
        for name in names + ["skills/core/SKILL.md", "node_modules/vendor/README.md", "output/result.md"]:
            self.write(name)
        actual = {path.relative_to(self.root).as_posix() for path in repository_markdown_paths(self.root)}
        self.assertEqual(actual, set(names))

    def test_cli_reports_counts_and_returns_failure_for_broken_link(self):
        source = self.write("README.md", "[broken](missing.md)\n")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/check_doc_links.py"), str(source)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("Checked 1 local links/anchors in 1 Markdown files; 1 errors", result.stdout)
        source.write_text("# Fine\n[valid](#fine)\n", encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(ROOT / "tools/check_doc_links.py"), str(source)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
