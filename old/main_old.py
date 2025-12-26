#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import statistics
from pathlib import Path
from collections import defaultdict


# ----------------- basic parsing helpers -----------------

def load_json(path):
    try:
        with open(str(path), "r") as f:
            return json.load(f)
    except Exception:
        return None


def parse_mem_gib(mem_str):
    if not mem_str:
        return None
    try:
        return float(str(mem_str).replace("GiB", "").strip())
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


# ----------------- filename parsing (robust) -----------------

def parse_run_tp_cp_from_filename(filename):
    """
    Works even if benchmark/tool/project contain '-' by scanning tokens for TP/CP
    and reading run from the token just before the hash.
    Expected suffix: ...-TPx-CPy-<run>-<hash>.json

    Returns: (run:int|None, TP:str|None, CP:str|None)
    """
    name = filename
    if name.endswith(".json"):
        name = name[:-5]

    if name.startswith("experiment-summary-"):
        name = name[len("experiment-summary-"):]

    parts = name.split("-")
    if len(parts) < 4:
        return None, None, None

    # hash is last token, run is token before it
    run = None
    TP = None
    CP = None

    # run
    if len(parts) >= 2:
        try:
            run = int(parts[-2])
        except Exception:
            run = None

    # find TP/CP by scanning tokens
    for tok in parts:
        if tok.startswith("TP") and tok[2:].isdigit():
            TP = tok
        if tok.startswith("CP") and tok[2:].isdigit():
            CP = tok

    return run, TP, CP


# ----------------- discovery: explicit per-tool layouts -----------------

def iter_tool1_flat_files(root):
    """
    Tool1 (repairllama): root/tools/*.json
    """
    root = Path(root).expanduser()
    tools_dir = root / "tools"
    if not tools_dir.exists():
        return []
    return sorted(tools_dir.glob("experiment-summary-*.json"))


def iter_tool_nested_files(root):
    """
    Tool2/Tool3: root/<anything>/tools/*.json (separate folders per run)
    We search for */tools/experiment-summary-*.json under root.
    """
    root = Path(root).expanduser()
    if not root.exists():
        return []
    out = []
    for p in root.rglob("experiment-summary-*.json"):
        try:
            if p.parent.name == "tools":
                out.append(p)
        except Exception:
            pass
    return sorted(out)


# ----------------- graphing utilities -----------------

def grouped_bar(ax, categories, series, series_labels, title, ylabel, ylim=None):
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


def save_fig(plt, fig, out_dir, filename):
    fig.tight_layout()
    fig.savefig(str(Path(out_dir) / filename), dpi=150)
    plt.close(fig)


# ----------------- individual graph functions -----------------

def plot_success_rate_by_project_side_by_side(plt, summary_rows, out_dir, tool_labels):
    proj_tool_success = defaultdict(int)
    proj_tool_expected = defaultdict(int)

    for row in summary_rows:
        tl = row.get("tool_label")
        pr = row.get("project")
        proj_tool_success[(tl, pr)] += int(row.get("successes", 0))
        proj_tool_expected[(tl, pr)] += int(row.get("runs_expected", 0))

    projects = sorted(set((r.get("project") or "unknown") for r in summary_rows))

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            denom = float(proj_tool_expected.get((tl, pr), 0))
            vals.append((float(proj_tool_success.get((tl, pr), 0)) / denom) if denom > 0 else 0.0)
        series.append(vals)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Success rate by project (tools side-by-side)",
        ylabel="Success rate",
        ylim=(0.0, 1.0),
    )
    save_fig(plt, fig, out_dir, "success_rate_by_project_side_by_side.png")


def plot_duration_mean_by_project_side_by_side(plt, per_run_records, out_dir, tool_labels):
    tool_proj_durs = defaultdict(list)
    for r in per_run_records:
        d = r.get("duration")
        if d is not None:
            tool_proj_durs[(r["tool_label"], r["project"])].append(d)

    projects = sorted(
        set((r.get("project") or "unknown") for r in per_run_records)
    )

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            vals.append(safe_mean(tool_proj_durs.get((tl, pr), [])) or 0.0)
        series.append(vals)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Mean duration by project (tools side-by-side)",
        ylabel="Mean duration (s)",
    )
    save_fig(plt, fig, out_dir, "duration_mean_by_project_side_by_side.png")


def plot_generated_mean_by_project_side_by_side(plt, per_run_records, out_dir, tool_labels):
    tool_proj_gen = defaultdict(list)
    for r in per_run_records:
        g = r.get("space_generated")
        if g is not None:
            tool_proj_gen[(r["tool_label"], r["project"])].append(g)

    projects = sorted(set((r.get("project") or "unknown") for r in per_run_records))


    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            vals.append(safe_mean(tool_proj_gen.get((tl, pr), [])) or 0.0)
        series.append(vals)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Mean generated patches by project (tools side-by-side)",
        ylabel="Mean generated patches",
    )
    save_fig(plt, fig, out_dir, "generated_mean_by_project_side_by_side.png")


def plot_plausible_coverage_by_project_side_by_side(plt, per_run_records, out_dir, tool_labels):
    tool_proj_total = defaultdict(int)
    tool_proj_pl_present = defaultdict(int)

    for r in per_run_records:
        tl = r["tool_label"]
        pr = r["project"]
        tool_proj_total[(tl, pr)] += 1
        if r.get("space_plausible") is not None:
            tool_proj_pl_present[(tl, pr)] += 1

    projects = sorted(set((r.get("project") or "unknown") for r in per_run_records))

    series = []
    for tl in tool_labels:
        vals = []
        for pr in projects:
            denom = float(tool_proj_total.get((tl, pr), 0))
            vals.append((float(tool_proj_pl_present.get((tl, pr), 0)) / denom) if denom > 0 else 0.0)
        series.append(vals)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    grouped_bar(
        ax=ax,
        categories=projects,
        series=series,
        series_labels=tool_labels,
        title="Plausible field coverage by project (tools side-by-side)",
        ylabel="Coverage (fraction of runs)",
        ylim=(0.0, 1.0),
    )
    save_fig(plt, fig, out_dir, "plausible_coverage_by_project_side_by_side.png")


def plot_generated_histograms_per_tool(plt, per_run_records, out_dir, tool_labels):
    for tl in tool_labels:
        vals = [
            r.get("space_generated")
            for r in per_run_records
            if r.get("tool_label") == tl and r.get("space_generated") is not None
        ]
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
        save_fig(plt, fig, out_dir, "generated_hist_{}.png".format(tl))


def generate_graphs(summary_rows, per_run_records, out_dir, tool_labels):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print("WARNING: Could not import matplotlib. Skipping graphs. Error: {}".format(e))
        return

    ensure_dir(Path(out_dir))

    plot_success_rate_by_project_side_by_side(plt, summary_rows, out_dir, tool_labels)
    plot_duration_mean_by_project_side_by_side(plt, per_run_records, out_dir, tool_labels)
    plot_generated_mean_by_project_side_by_side(plt, per_run_records, out_dir, tool_labels)
    plot_plausible_coverage_by_project_side_by_side(plt, per_run_records, out_dir, tool_labels)
    plot_generated_histograms_per_tool(plt, per_run_records, out_dir, tool_labels)

    print("Wrote graphs to {}".format(out_dir))


# ----------------- extraction from JSON -----------------

def extract_identity(data, fallback_benchmark=None, fallback_project=None, fallback_bug_id=None):
    """
    Prefer JSON info (more reliable), fallback to filename-derived bits.
    """
    benchmark = fallback_benchmark
    project = fallback_project
    bug_id = fallback_bug_id

    info = (data or {}).get("info", {})
    bug_info = info.get("bug-info", {}) if isinstance(info, dict) else {}

    # common fields in your example
    if isinstance(bug_info, dict):
        if bug_info.get("benchmark"):
            benchmark = bug_info.get("benchmark")
        if bug_info.get("subject"):
            project = bug_info.get("subject")
        if bug_info.get("bug_id"):
            bug_id = bug_info.get("bug_id")

    return benchmark, project, bug_id

def sort_key_tuple_with_nones(t):
    return tuple("" if x is None else str(x) for x in t)

# ----------------- main -----------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root1", help="Tool1 root (repairllama): expects root1/tools/*.json")
    parser.add_argument("root2", help="Tool2 root (nested): expects */tools/*.json under root2")
    parser.add_argument("root3", help="Tool3 root (nested): expects */tools/*.json under root3")
    parser.add_argument(
        "--labels",
        default="tool1,tool2,tool3",
        help="Comma-separated labels for tool1,tool2,tool3 (default: tool1,tool2,tool3)",
    )
    parser.add_argument("--expected-runs", type=int, default=3)
    parser.add_argument("--no-graphs", action="store_true")
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

    # Explicit layouts per tool (this is the key fix)
    roots = [args.root1, args.root2, args.root3]
    discoverers = [iter_tool1_flat_files, iter_tool_nested_files, iter_tool_nested_files]

    groups = defaultdict(list)
    per_run_records = []

    for root, discover, tool_label in zip(roots, discoverers, tool_labels):
        files = discover(root)
        if not files:
            print("WARNING: No files found for {} at {}".format(tool_label, root))
            continue

        for path in files:
            print(root)
            data = load_json(path)
            if not data:
                continue

            # parse run/TP/CP from filename robustly
            run, TP, CP = parse_run_tp_cp_from_filename(path.name)

            details = (data or {}).get("details", {})
            time_info = details.get("time", {}) if isinstance(details, dict) else {}
            container = details.get("container", {}) if isinstance(details, dict) else {}
            network = container.get("network_usage", {}) if isinstance(container, dict) else {}
            space = details.get("space", {}) if isinstance(details, dict) else {}

            duration = time_info.get("total duration") if isinstance(time_info, dict) else None
            mem_gib = parse_mem_gib(container.get("mem_usage") if isinstance(container, dict) else None)
            rx_b = parse_bytes(network.get("total_received") if isinstance(network, dict) else None)
            tx_b = parse_bytes(network.get("total_transmitted") if isinstance(network, dict) else None)

            # robust space extraction
            space_search_space = get_space_metric(space, "search space", "search_space")
            space_enumerations = get_space_metric(space, "enumerations", "enumeration")
            space_non_compilable = get_space_metric(space, "non compilable", "non-compilable", "non_compilable")
            space_plausible = get_space_metric(space, "plausible", "plausible patches", "plausible_patches")
            space_implausible = get_space_metric(space, "implausible", "implausible patches", "implausible_patches")
            space_generated = get_space_metric(space, "generated", "generated patches", "generated_patches")

            raw_space_keys = space_keys_signature(space)
            raw_plausible = space.get("plausible") if isinstance(space, dict) else None

            status = data.get("status")

            # identity from JSON (best effort)
            benchmark, project, bug_id = extract_identity(data)

            # If TP/CP missing in filename, fallback to None (kept as None in output)
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

            # group key: tool_label + identity
            key = (tool_label, benchmark, project, bug_id, TP, CP)
            groups[key].append(record)

            per_run_records.append({
                "tool_label": tool_label,
                "benchmark": benchmark,
                "project": project,
                "bug_id": bug_id,
                "TP": TP,
                "CP": CP,
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

    # ---------- Coverage per tool (diagnostics) ----------
    coverage_by_tool = {}
    for tl in tool_labels:
        runs = [r for r in per_run_records if r.get("tool_label") == tl]
        cov = {
            "runs_total": len(runs),
            "runs_with_generated": sum(1 for r in runs if r.get("space_generated") is not None),
            "runs_with_plausible": sum(1 for r in runs if r.get("space_plausible") is not None),
        }
        coverage_by_tool[tl] = cov

    with open(str(data_dir / "coverage_by_tool.json"), "w") as f:
        json.dump(coverage_by_tool, f, indent=2)
    print("Wrote {}".format(data_dir / "coverage_by_tool.json"))
    print("Coverage by tool: {}".format(coverage_by_tool))

    # ---------- Per-group summary ----------
    summary_rows = []
    for key in sorted(groups.keys(), key=sort_key_tuple_with_nones):
        tool_label, benchmark, project, bug_id, TP, CP = key
        records = groups[key]

        runs_found = set([r["run"] for r in records if r.get("run") is not None])
        missing_runs = sorted(set(range(args.expected_runs)) - runs_found) if runs_found else list(range(args.expected_runs))

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
            "success_rate": float(len(successes)) / float(args.expected_runs),
            "duration_mean": safe_mean(durations),
            "duration_min": safe_min(durations),
            "duration_max": safe_max(durations),
            "mem_mean_gib": safe_mean(mems),
            "mem_max_gib": safe_max(mems),
            "rx_bytes_total": sum([int(r.get("rx_bytes", 0)) for r in records]),
            "tx_bytes_total": sum([int(r.get("tx_bytes", 0)) for r in records]),
            "statuses": ";".join(
                ["{}:{}".format(r.get("run"), r.get("status")) for r in sorted(records, key=lambda x: (x.get("run") is None, x.get("run")))]
            ),

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

    # ---------- Write outputs ----------
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

    # ---------- Graphs ----------
    if not args.no_graphs:
        generate_graphs(summary_rows, per_run_records, graphs_dir, tool_labels)


if __name__ == "__main__":
    main()
