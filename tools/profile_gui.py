#!/usr/bin/env python3
"""Profile GUI snapshots using disposable synthetic records, never user files."""
import argparse
import cProfile
import json
from pathlib import Path
import pstats
import statistics
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "gui"))
import server


def profile(filings=12, samples=3):
    if not 1 <= filings <= 120 or not 1 <= samples <= 20:
        raise ValueError("Use 1–120 synthetic filings and 1–20 samples.")
    with tempfile.TemporaryDirectory(prefix="gbk-gui-profile-") as directory:
        root = Path(directory).resolve() / "workspace"
        server.ws.init_workspace(root, 2026, "en")
        proof = "08_correspondence/synthetic.txt"
        (root / proof).write_text("Synthetic configuration and external draft evidence; no transmission.", encoding="utf-8")
        config = server.accounting.template("configuration")
        config.update(system="external", product="Synthetic software", method="unresolved",
                      account_reference="synthetic", reviewer="synthetic", evidence_file=proof)
        server.accounting.configure(root, config)
        for index in range(filings):
            value = server.accounting.template("filing")
            value.update(filing_id="synthetic-" + str(index), form="ustva", form_version="2026",
                         period=f"{2026 + index // 12:04d}-{index % 12 + 1:02d}", recipient="synthetic",
                         payload_file=proof, source_files=[proof])
            server.accounting.create_filing(root, value)
        app = server.Application(root)
        app.snapshot("2026-10")
        profiler = cProfile.Profile()
        elapsed = []
        for _ in range(samples):
            start = time.perf_counter()
            profiler.runcall(app.snapshot, "2026-10")
            elapsed.append((time.perf_counter() - start) * 1000)
        watched = {"snapshot", "_check_filing", "_load", "check_evidence", "files"}
        functions = [{"module": Path(key[0]).name, "function": key[2], "calls": values[1],
                      "cumulative_ms": round(values[3] * 1000, 3)}
                     for key, values in pstats.Stats(profiler).stats.items() if key[2] in watched]
        return {"scope": "Synthetic local snapshots; no Windows or customer-workspace acceptance",
                "filings": filings, "samples": samples, "median_ms": round(statistics.median(elapsed), 3),
                "max_ms": round(max(elapsed), 3), "functions": sorted(functions, key=lambda row: -row["cumulative_ms"])}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filings", type=int, default=12)
    parser.add_argument("--samples", type=int, default=3)
    args = parser.parse_args()
    print(json.dumps(profile(args.filings, args.samples), indent=2))
