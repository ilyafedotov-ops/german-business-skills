"""Developer-only synthetic real-workspace views for browser acceptance."""
import json
import os
from pathlib import Path
import subprocess
import sys

from test_overview import OverviewTests
from casefiles import accounting as ac, overview
import workspace as ws


output = Path(sys.argv[1]).resolve()
output.mkdir(parents=True, exist_ok=True)
for language in ("en", "ru"):
    for scenario in ("empty", "blocked", "corrupt"):
        case = OverviewTests()
        case.setUp()
        try:
            if scenario != "empty":
                case.configure()
                ac.post(case.root, case.entry())
                case.filing(unresolved_items=['Check invoice evidence <script>alert(1)</script>'])
                ws.save_entry(case.root, "questions", {"schema_version": 1, "id": "question-1", "owner": "owner",
                              "status": "open", "title": "Clarify invoice country"})
            if scenario == "corrupt":
                (case.root / ac.STATE).unlink()
            rendered = overview.generate(case.root, "2026-10", "2026-10-26", language)
            (output / (language + "-" + scenario + ".html")).write_bytes((case.root / rendered["html_path"]).read_bytes())
            ws.configure_workspace(case.root, language=language)
            native = None
            if sys.platform == "win32":
                native = ["powershell.exe", "-NoProfile", "-NonInteractive", "-File",
                          str(Path(__file__).resolve().parents[1] / "skills/de-business-kit/scripts/windows.ps1"),
                          "-Action", "overview", "-Root", str(case.root), "-Period", "2026-10"]
            elif os.environ.get("GBK_TEST_DOCKER_IMAGE"):
                native = ["docker", "run", "--rm", "--network", "none", "-v",
                          str(Path(__file__).resolve().parents[1]) + ":/repo:ro", "-v", str(case.base) + ":/data",
                          os.environ["GBK_TEST_DOCKER_IMAGE"], "pwsh", "-NoProfile", "-File",
                          "/repo/skills/de-business-kit/scripts/windows.ps1", "-Action", "overview",
                          "-Root", "/data/private", "-Period", "2026-10"]
            if native:
                run = subprocess.run(native, capture_output=True, encoding="utf-8-sig", timeout=60)
                if run.returncode:
                    raise RuntimeError(run.stdout + run.stderr)
                view = json.loads(run.stdout)
                if scenario != "corrupt" and view["health"] != "ok":
                    raise RuntimeError(str(view["errors"]))
                (output / (language + "-" + scenario + "-native.html")).write_bytes(
                    (case.root / view["html_path"]).read_bytes())
        finally:
            case.doCleanups()
print(json.dumps({"fixtures": 6, "scope": "synthetic canonical records; no external integration"}))
