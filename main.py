#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import re
import statistics
from pathlib import Path
from collections import defaultdict


FILENAME_RE = re.compile(
    r"experiment-summary-"
    r"(?P<benchmark>[^-]+)-"
    r"(?P<tool>[^-]+)-"
    r"(?P<project>[^-]+)-"
    r"(?P<bug_id>[^-]+)-"
    r"(?P<TP>TP\d+)-"
    r"(?P<CP>CP\d+)-"
    r"(?P<run>\d+)-"
    r"(?P<hash>[a-f0-9]+)\.json"
)


# ----------------- basic parsing helpers -----------------

def parse_mem_gib(mem_str):
    if not mem_str:
        return None
    try:
        return float(str(mem_str).replace("GiB", "").strip())
    except Exception:
        return None


def load_json(path):
    try:
        with open(str(path), "r") as f:
            return json.load(f)
    except Exception:
        return None


def parse_bytes(x):
    if not x:
        return 0
    try:
        return int(str(x).replace("bytes", "").strip())
    except Exception:
        return 0


def normalize_space_int(x):
    # -1 appears to mean "not available"
    try:
        v = int(x)
    except Exception:
        return None
    return None if v < 0 else v


def safe_mean(values):
    return statistics.mean(values) if values else None


def safe_min(values):
    return min(values) if values else None


def safe_max(values):
    return max(values) if values else None


def ensure_dir(p):
    if not p.exists():
        p.mkdir(parents=True)


# ----------------- robust "space" key handling -----------------

def _norm_space_key(k):
    try:
        s = str(k)
    except Exception:
        return ""
    s = s.strip().lower()
    s = s.replace("_", " ").replace("-", " ")
    s = " ".join(s.split())
    return s


def get_space_metric(space_dict, *names):
    """
    Fetch a metric from details.space robustly across key variants.
    names are logical names like: "plausible", "generated", ...
    """
    if not isinstance(space_dict, dict):
        return None

    norm_map = {}
    for k, v in space_dict.items():
        norm_map[_norm_space_key(k)] = v

    for name in names:
        key = _norm_space_key(name)
        if key in norm_map:
            return normalize_space_int(norm_map.get(key))
    return None


def space_keys_signature(space_dict):
    if not isinstance(space_dict, dict):
        return []
    try:
        return sorted([str(k) for k in space_dict.keys()])
    except Exception:
        return []


# ----------------- discovery: support both layouts -----------------

def iter_summary_files(root):
    """
    Supports both:
    A) root/tools/experiment-summary-*.json (many)
    B) root/<run_folder>/tools/experiment-summary-*.json (one per run folder)
    We'll just recursively search for *tools/experiment-summary-*.json
    """
    root = Path(root).expanduser()
    if not root.exists():
        return
    # rglob is fine; we filter to parent directory named "tools"
    for p in root.rglob("experiment-summary-*.json"):
        try:
            if p.parent.name == "tools":
                yield p
        except Exception:
            continue


# ----------------- graphing -----------------

def generate_graphs(summary_rows, per_run_records, out_dir, tool_labels):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print("WARNING: Could not import matplotlib. Skipping graphs. Error: {}".format(e))
        return

    ensure_dir(out_dir)

    def save_fig(fig, filename):
        fig.tight_layout()
        fig.savefig(str(out_dir / filename), dpi=150)
        plt.close(fig)

    def grouped_bar(ax, categories, series, series_labels, title, ylabel, ylim=None):
        """
        categories: list[str]
        series: list[list[float]] aligned with categories
        series_labels: list[str]
        """
        n_cat = len(categories)
        n_ser = len(series_labels)
        if n_cat == 0 or n_ser == 0:
            ax.text(0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
            return

        base_x = list(range(n_cat))
        total_width = 0.8
        width = total_width / float(max(1, n_ser))

        for i in range(n_ser):
            vals = series[i]
            xs = [bx - total_width / 2.0 + (i + 0.5) * width for bx in base_x]
            ax.bar(xs, vals, width, label=series_labels[i])

        ax.set_xticks(base_x)
        ax.set_xticklabels(categories, rotation=45, ha="right", fontsize=8)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.legend(fontsize=8, loc="best")
        if ylim is not None:
            ax.set_ylim(ylim)

    # ---------- Success rate by project (side-by-side for the 3 tools) ----------
    # Compute per tool_label, per project: successes/expected from summary_rows
    proj_tool_success = defaultdict(int)
    proj_tool_expected = defaultdict(int)

    for row in summary_rows:
        tl = row.get("tool_label")
        pr = row.get("project")
        proj_tool_success[(tl, pr)] += int(row.get("successes", 0))
        proj_tool_expected[(tl, pr)] += int(row.get("runs_expected", 0))

    projects = sorted(set([r.get("project") for r in summary_rows]))
    fig = plt.figure()
    ax = fig.add_subplot(111)

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            denom = float(proj_tool_expected.get((tl, pr), 0))
            if denom <= 0.0:
                vals.append(0.0)
            else:
                vals.append(float(proj_tool_success.get((tl, pr), 0)) / denom)
        series.append(vals)

    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Success rate by project (tools side-by-side)",
        ylabel="Success rate",
        ylim=(0.0, 1.0),
    )
    save_fig(fig, "success_rate_by_project_side_by_side.png")

    # ---------- Mean duration by project (side-by-side) using per_run_records ----------
    tool_proj_durs = defaultdict(list)
    for r in per_run_records:
        d = r.get("duration")
        if d is None:
            continue
        tool_proj_durs[(r["tool_label"], r["project"])].append(d)

    projects = sorted(set([r.get("project") for r in per_run_records]))
    fig = plt.figure()
    ax = fig.add_subplot(111)

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            vals.append(safe_mean(tool_proj_durs.get((tl, pr), [])) or 0.0)
        series.append(vals)

    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Mean duration by project (tools side-by-side)",
        ylabel="Mean duration (s)",
        ylim=None,
    )
    save_fig(fig, "duration_mean_by_project_side_by_side.png")

    # ---------- Generated patches: mean by project (side-by-side) ----------
    tool_proj_gen = defaultdict(list)
    for r in per_run_records:
        g = r.get("space_generated")
        if g is None:
            continue
        tool_proj_gen[(r["tool_label"], r["project"])].append(g)

    projects = sorted(set([r.get("project") for r in per_run_records]))
    fig = plt.figure()
    ax = fig.add_subplot(111)

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            vals.append(safe_mean(tool_proj_gen.get((tl, pr), [])) or 0.0)
        series.append(vals)

    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Mean generated patches by project (tools side-by-side)",
        ylabel="Mean generated patches",
        ylim=None,
    )
    save_fig(fig, "generated_mean_by_project_side_by_side.png")

    # ---------- Plausible coverage by project (side-by-side) ----------
    # fraction of runs where plausible is present (not None)
    tool_proj_total = defaultdict(int)
    tool_proj_pl_present = defaultdict(int)

    for r in per_run_records:
        tl = r["tool_label"]
        pr = r["project"]
        tool_proj_total[(tl, pr)] += 1
        if r.get("space_plausible") is not None:
            tool_proj_pl_present[(tl, pr)] += 1

    projects = sorted(set([r.get("project") for r in per_run_records]))
    fig = plt.figure()
    ax = fig.add_subplot(111)

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            denom = float(tool_proj_total.get((tl, pr), 0))
            if denom <= 0.0:
                vals.append(0.0)
            else:
                vals.append(float(tool_proj_pl_present.get((tl, pr), 0)) / denom)
        series.append(vals)

    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Plausible field coverage by project (tools side-by-side)",
        ylabel="Coverage (fraction of runs)",
        ylim=(0.0, 1.0),
    )
    save_fig(fig, "plausible_coverage_by_project_side_by_side.png")

    # ---------- Histograms per tool (generated) ----------
    # (These are useful even when "side-by-side bars" exist)
    for tl in tool_labels:
        vals = [r.get("space_generated") for r in per_run_records
                if r.get("tool_label") == tl and r.get("space_generated") is not None]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if vals:
            ax.hist(vals, bins=30)
            ax.set_xlabel("Generated patches")
            ax.set_ylabel("Count")
            ax.set_title("Generated patches distribution ({})".format(tl))
        else:
            ax.text(0.5, 0.5, "No generated data found", ha="center", va="center", transform=ax.transAxes)
            ax.set_axis_off()
        save_fig(fig, "generated_hist_{}.png".format(tl))

    print("Wrote graphs to {}".format(out_dir))


# ----------------- main -----------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "roots",
        nargs=3,
        help="Three result roots (one per tool). Each root may contain tools/ directly or run-subfolders each containing tools/."
    )
    parser.add_argument(
        "--labels",
        default="tool1,tool2,tool3",
        help="Comma-separated labels for the 3 tools (default: tool1,tool2,tool3)"
    )
    parser.add_argument(
        "--expected-runs",
        type=int,
        default=3,
        help="Expected number of runs per bug (default: 3)"
    )
    parser.add_argument(
        "--no-graphs",
        action="store_true",
        help="Disable PNG graph generation"
    )
    args = parser.parse_args()

    tool_labels = [s.strip() for s in str(args.labels).split(",") if s.strip()]
    if len(tool_labels) != 3:
        raise RuntimeError("--labels must contain exactly 3 comma-separated labels")

    # data/ next to main.py
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    ensure_dir(data_dir)
    graphs_dir = data_dir / "graphs"
    ensure_dir(graphs_dir)

    groups = defaultdict(list)
    per_run_records = []
    all_summary_rows = []

    # Read all three roots, annotate each record with tool_label from args
    for root, tool_label in zip(args.roots, tool_labels):
        root_path = Path(root).expanduser()
        if not root_path.exists():
            print("WARNING: root does not exist: {}".format(root_path))
            continue

        # discover json files under this root
        for path in iter_summary_files(root_path):
            m = FILENAME_RE.match(path.name)
            if not m:
                continue

            info = m.groupdict()
            run = int(info["run"])

            data = load_json(path)
            if not data:
                continue

            status = data.get("status")

            details = data.get("details", {})
            time_info = details.get("time", {})
            container = details.get("container", {})
            network = container.get("network_usage", {})
            space = details.get("space", {})

            duration = time_info.get("total duration")
            mem_gib = parse_mem_gib(container.get("mem_usage"))
            rx_b = parse_bytes(network.get("total_received"))
            tx_b = parse_bytes(network.get("total_transmitted"))

            # robust space extraction
            space_search_space = get_space_metric(space, "search space", "search_space")
            space_enumerations = get_space_metric(space, "enumerations", "enumeration")
            space_non_compilable = get_space_metric(space, "non compilable", "non-compilable", "non_compilable")
            space_plausible = get_space_metric(space, "plausible", "plausible patches", "plausible_patches")
            space_implausible = get_space_metric(space, "implausible", "implausible patches", "implausible_patches")
            space_generated = get_space_metric(space, "generated", "generated patches", "generated_patches")

            # diagnostics
            raw_space_keys = space_keys_signature(space)
            raw_plausible = space.get("plausible") if isinstance(space, dict) else None

            record = {
                "run": run,
                "status": status,
                "duration": duration,
                "mem_gib": mem_gib,
                "rx_bytes": rx_b,
                "tx_bytes": tx_b,
                "space_search_space": space_search_space,
                "space_enumerations": space_enumerations,
                "space_non_compilable": space_non_compilable,
                "space_plausible": space_plausible,
                "space_implausible": space_implausible,
                "space_generated": space_generated,
            }

            # IMPORTANT: key includes tool_label, so tools stay separate for aggregation/graphs
            key = (
                tool_label,
                info["benchmark"],
                info["project"],
                info["bug_id"],
                info["TP"],
                info["CP"],
            )
            groups[key].append(record)

            per_run_records.append({
                "tool_label": tool_label,
                "benchmark": info["benchmark"],
                "tool_in_filename": info["tool"],
                "project": info["project"],
                "bug_id": info["bug_id"],
                "TP": info["TP"],
                "CP": info["CP"],
                "run": run,
                "status": status,
                "duration": duration,
                "mem_gib": mem_gib,
                "rx_bytes": rx_b,
                "tx_bytes": tx_b,
                "space_search_space": space_search_space,
                "space_enumerations": space_enumerations,
                "space_non_compilable": space_non_compilable,
                "space_plausible": space_plausible,
                "space_implausible": space_implausible,
                "space_generated": space_generated,
                "raw_space_keys": raw_space_keys,
                "raw_plausible": raw_plausible,
                "file": str(path),
            })

    # ---------- Coverage per tool ----------
    coverage_by_tool = {}
    for tl in tool_labels:
        runs = [r for r in per_run_records if r.get("tool_label") == tl]
        cov = {
            "runs_total": len(runs),
            "runs_with_generated": sum(1 for r in runs if r.get("space_generated") is not None),
            "runs_with_plausible": sum(1 for r in runs if r.get("space_plausible") is not None),
            "runs_with_implausible": sum(1 for r in runs if r.get("space_implausible") is not None),
            "runs_with_non_compilable": sum(1 for r in runs if r.get("space_non_compilable") is not None),
            "runs_with_enumerations": sum(1 for r in runs if r.get("space_enumerations") is not None),
            "runs_with_search_space": sum(1 for r in runs if r.get("space_search_space") is not None),
        }

        if cov["runs_with_plausible"] == 0:
            sigs = []
            seen = set()
            for r in runs:
                keys = tuple(r.get("raw_space_keys") or [])
                if keys and keys not in seen:
                    seen.add(keys)
                    sigs.append(list(keys))
                if len(sigs) >= 5:
                    break
            cov["example_space_key_sets"] = sigs

            raw_pl = []
            for r in runs:
                if r.get("raw_plausible") is not None:
                    raw_pl.append(r.get("raw_plausible"))
                if len(raw_pl) >= 10:
                    break
            cov["raw_plausible_samples"] = raw_pl

        coverage_by_tool[tl] = cov

    with open(str(data_dir / "coverage_by_tool.json"), "w") as f:
        json.dump(coverage_by_tool, f, indent=2)
    print("Wrote {}".format(data_dir / "coverage_by_tool.json"))
    print("Coverage by tool: {}".format(coverage_by_tool))

    # ---------- Per-group summary (now includes tool_label) ----------
    summary_rows = []

    for key in sorted(groups.keys()):
        tool_label, benchmark, project, bug_id, TP, CP = key
        records = groups[key]

        runs_found = set([r["run"] for r in records])
        missing_runs = sorted(set(range(args.expected_runs)) - runs_found)

        successes = [r for r in records if r.get("status") == "Success"]
        durations = [r["duration"] for r in records if r.get("duration") is not None]
        mems = [r["mem_gib"] for r in records if r.get("mem_gib") is not None]

        generated = [r["space_generated"] for r in records if r.get("space_generated") is not None]
        plausible = [r["space_plausible"] for r in records if r.get("space_plausible") is not None]
        implausible = [r["space_implausible"] for r in records if r.get("space_implausible") is not None]
        noncomp = [r["space_non_compilable"] for r in records if r.get("space_non_compilable") is not None]
        enumerations = [r["space_enumerations"] for r in records if r.get("space_enumerations") is not None]
        search_space = [r["space_search_space"] for r in records if r.get("space_search_space") is not None]

        row = {
            "tool_label": tool_label,
            "benchmark": benchmark,
            "project": project,
            "bug_id": bug_id,
            "TP": TP,
            "CP": CP,
            "runs_found": len(records),
            "runs_expected": args.expected_runs,
            "missing_runs": ",".join([str(x) for x in missing_runs]),
            "successes": len(successes),
            "success_rate": float(len(successes)) / float(args.expected_runs) if args.expected_runs else 0.0,
            "duration_mean": safe_mean(durations),
            "duration_min": safe_min(durations),
            "duration_max": safe_max(durations),
            "mem_mean_gib": safe_mean(mems),
            "mem_max_gib": safe_max(mems),
            "rx_bytes_total": sum([int(r.get("rx_bytes", 0)) for r in records]),
            "tx_bytes_total": sum([int(r.get("tx_bytes", 0)) for r in records]),
            "statuses": ";".join(
                ["{}:{}".format(r["run"], r.get("status")) for r in sorted(records, key=lambda x: x["run"])]
            ),

            # Patch-space aggregates
            "generated_mean": safe_mean(generated),
            "generated_sum": sum(generated) if generated else None,
            "plausible_mean": safe_mean(plausible),
            "plausible_sum": sum(plausible) if plausible else None,
            "implausible_mean": safe_mean(implausible),
            "implausible_sum": sum(implausible) if implausible else None,
            "non_compilable_mean": safe_mean(noncomp),
            "non_compilable_sum": sum(noncomp) if noncomp else None,
            "enumerations_mean": safe_mean(enumerations),
            "enumerations_sum": sum(enumerations) if enumerations else None,
            "search_space_mean": safe_mean(search_space),
            "search_space_sum": sum(search_space) if search_space else None,
        }

        summary_rows.append(row)

    # ---------- Write CSV/JSON ----------
    csv_path = data_dir / "summary.csv"
    with open(str(csv_path), "w") as f:
        if summary_rows:
            headers = list(summary_rows[0].keys())
            f.write(",".join(headers) + "\n")
            for row in summary_rows:
                f.write(",".join("" if row[h] is None else str(row[h]) for h in headers) + "\n")

    json_path = data_dir / "summary.json"
    with open(str(json_path), "w") as f:
        json.dump(summary_rows, f, indent=2)

    print("Wrote {}".format(csv_path))
    print("Wrote {}".format(json_path))

    # ---------- Graphs (side-by-side for the 3 tools) ----------
    if not args.no_graphs:
        generate_graphs(
            summary_rows=summary_rows,
            per_run_records=per_run_records,
            out_dir=graphs_dir,
            tool_labels=tool_labels
        )


if __name__ == "__main__":
    main()
