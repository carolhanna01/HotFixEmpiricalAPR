#!/usr/bin/env python3
import argparse
import re
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


TS_RE = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})")


def parse_acr_bug_folder_name(name: str):
    # Example: flink_00863a28_2025-10-15_17-23-48
    parts = name.split("_")
    project = parts[0] if len(parts) >= 1 else "UNKNOWN"
    bug_id = parts[1] if len(parts) >= 2 else None
    return project, bug_id


def runtime_seconds_from_info_log(log_path: Path) -> float | None:
    """
    Runtime = last timestamp - first timestamp in the log.
    Returns seconds, or None if no timestamps found.
    """
    first = None
    last = None
    try:
        with log_path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                m = TS_RE.match(line)
                if not m:
                    continue
                t = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S.%f")
                if first is None:
                    first = t
                last = t
    except Exception:
        return None

    if first is None or last is None:
        return None
    return (last - first).total_seconds()


def plot_mode_runtimes(mode_dir: Path, out_png: Path):
    """
    mode_dir contains bug dirs: <project>_<bugid>_<timestamp>/
    each bug dir contains info.log
    """
    bug_labels = []
    runtimes = []

    for bug_dir in sorted([p for p in mode_dir.iterdir() if p.is_dir()]):
        log_path = bug_dir / "info.log"
        if not log_path.exists():
            continue

        rt = runtime_seconds_from_info_log(log_path)
        if rt is None:
            continue

        project, bug_id = parse_acr_bug_folder_name(bug_dir.name)
        label = f"{project}_{bug_id}" if bug_id else project

        bug_labels.append(label)
        runtimes.append(rt)

    if not runtimes:
        print(f"[WARN] No runtimes found under: {mode_dir}")
        return

    # Sort by runtime so the plot is readable
    order = sorted(range(len(runtimes)), key=lambda i: runtimes[i], reverse=True)

    # Keep top 50
    order = order[:50]

    bug_labels = [bug_labels[i] for i in order]
    runtimes = [runtimes[i] for i in order]


    plt.figure(figsize=(12, 5))
    plt.bar(bug_labels, runtimes)
    plt.xticks(rotation=90, fontsize=14)
    plt.ylabel("Runtime (seconds)", fontsize=14)
    plt.title(f"AutoCodeRover runtimes per bug for {mode_dir.name} (top 50)", fontsize=18)
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

    print(f"Wrote {out_png} ({len(runtimes)} bugs)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--acr", required=True, help="Path to ACR root containing llama3 and llama3:70b")
    ap.add_argument("--outdir", default="graph_2", help="Output directory (default: graph_2)")
    args = ap.parse_args()

    acr_root = Path(args.acr)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for mode in ["llama3", "llama3:70b"]:
        mode_dir = acr_root / mode
        if not mode_dir.exists():
            print(f"[WARN] Mode dir missing: {mode_dir}")
            continue

        safe_mode = mode.replace(":", "_")
        out_png = outdir / f"acr_runtime_per_bug__{safe_mode}.png"
        plot_mode_runtimes(mode_dir, out_png)


if __name__ == "__main__":
    main()
