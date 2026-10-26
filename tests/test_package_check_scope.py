"""Installed development tools are outside the source/package check boundary."""
from pathlib import Path
import tempfile
import unittest

from tools.check_package import checked_files


class PackageCheckScopeTests(unittest.TestCase):
    def test_dev_dependencies_and_outputs_are_excluded_but_skill_paths_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            names = ["node_modules/third-party/broken.md", "output/report.json",
                     ".venv/lib/metadata.json", "docs/guide.md",
                     "skills/de-business-kit/node_modules/unexpected.json"]
            for name in names:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("fixture", encoding="utf-8")
            found = {p.relative_to(root).as_posix() for p in checked_files(root) if p.is_file()}
            self.assertEqual(found, {"docs/guide.md", "skills/de-business-kit/node_modules/unexpected.json"})
