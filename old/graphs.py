from pathlib import Path
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

METRICS = ["generated", "plausible", "implausible", "non_compilable", "enumerations", "search_space"]

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def sanitize_filename(s: str) -> str:
    s = (s or "UNKNOWN").strip()
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:120] if len(s) > 120 else s

def _clean(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    # project name (what you called "per project")
    if "bug_subject" not in out.columns:
        out["bug_subject"] = "UNKNOWN"
    out["bug_subject"] = out["bug_subject"].fillna("UNKNOWN").astype(str)

    # numeric fields
    for c in METRICS:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
            out.loc[out[c] < 0, c] = np.nan  # treat -1 as missing

    out["total_duration_seconds"] = pd.to_numeric(out.get("total_duration_seconds"), errors="coerce")
    return out

def plot_metric_per_project_avg_per_run(runs: pd.DataFrame, outdir: Path, metric: str, top_n_projects: int = 30):
    df = _clean(runs)
    if metric not in df.columns:
        return

    # average per run per (project, tool)
    pivot = (
        df.groupby(["bug_subject", "tool"])[metric]
        .mean()
        .unstack("tool")
    )

    # keep the projects with the most data / highest total runs (helps readability)
    counts = df.groupby("bug_subject").size().sort_values(ascending=False)
    keep = counts.head(top_n_projects).index
    pivot = pivot.loc[pivot.index.intersection(keep)]

    pivot = pivot.sort_index()

    pivot.plot(kind="bar", figsize=(12, 5))
    plt.title(f"{metric}: average per run (per project)")
    plt.xlabel("Project (bug_subject)")
    plt.ylabel("Average count per run")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(outdir / f"per_project_patch_metrics_avg_per_run__{sanitize_filename(metric)}.png")
    plt.close()

def plot_metric_per_project_avg_per_second(runs: pd.DataFrame, outdir: Path, metric: str, top_n_projects: int = 30):
    df = _clean(runs)
    if metric not in df.columns:
        return

    # only runs with valid duration
    df = df[df["total_duration_seconds"].notna() & (df["total_duration_seconds"] > 0)].copy()
    df[f"{metric}_per_s"] = df[metric] / df["total_duration_seconds"]

    pivot = (
        df.groupby(["bug_subject", "tool"])[f"{metric}_per_s"]
        .mean()
        .unstack("tool")
    )

    counts = df.groupby("bug_subject").size().sort_values(ascending=False)
    keep = counts.head(top_n_projects).index
    pivot = pivot.loc[pivot.index.intersection(keep)]
    pivot = pivot.sort_index()

    pivot.plot(kind="bar", figsize=(12, 5))
    plt.title(f"{metric}: average per second (per project)")
    plt.xlabel("Project (bug_subject)")
    plt.ylabel("Average count / second")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(outdir / f"per_project_patch_metrics_avg_per_second__{sanitize_filename(metric)}.png")
    plt.close()

def plot_plausible_share_per_project(runs: pd.DataFrame, outdir: Path, top_n_projects: int = 30):
    df = _clean(runs)

    # plausible / generated where generated > 0
    df = df[df["generated"].notna() & (df["generated"] > 0)].copy()
    df["plausible_share"] = df["plausible"] / df["generated"]

    pivot = (
        df.groupby(["bug_subject", "tool"])["plausible_share"]
        .mean()
        .unstack("tool")
    )

    counts = df.groupby("bug_subject").size().sort_values(ascending=False)
    keep = counts.head(top_n_projects).index
    pivot = pivot.loc[pivot.index.intersection(keep)]
    pivot = pivot.sort_index()

    pivot.plot(kind="bar", figsize=(12, 5))
    plt.title("Plausible share (plausible / generated), averaged over runs (per project)")
    plt.xlabel("Project (bug_subject)")
    plt.ylabel("Share")
    plt.ylim(0, 1)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(outdir / "per_project_plausible_share.png")
    plt.close()

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def plot_total_generated_per_tool_per_project(runs: pd.DataFrame, outdir: Path):
    df = runs.copy()

    # Ensure required columns exist
    df["bug_subject"] = df["bug_subject"].fillna("UNKNOWN").astype(str)

    # Clean generated values
    df["generated"] = pd.to_numeric(df["generated"], errors="coerce")
    df.loc[df["generated"] < 0, "generated"] = np.nan

    # Aggregate: SUM generated per (project, tool)
    pivot = (
        df.groupby(["bug_subject", "tool"])["generated"]
        .sum(min_count=1)   # min_count avoids turning all-NaN into 0
        .unstack("tool")
        .fillna(0)
        .sort_index()
    )

    # Plot
    pivot.plot(kind="bar", figsize=(12, 5))
    plt.title("Total generated patches per tool per project")
    plt.xlabel("Project")
    plt.ylabel("Total generated patches")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    outpath = outdir / "total_generated_per_tool_per_project.png"
    plt.savefig(outpath)
    plt.close()

    print(f"Wrote {outpath}")


def main():
    runs = pd.read_csv("out/runs.csv")

    outdir = Path("graph_2")
    ensure_dir(outdir)

    # # One chart per metric (so it stays readable)
    # for m in ["generated", "plausible", "implausible", "non_compilable", "enumerations"]:
    #     plot_metric_per_project_avg_per_run(runs, outdir, m, top_n_projects=30)
    #     plot_metric_per_project_avg_per_second(runs, outdir, m, top_n_projects=30)

    # plot_plausible_share_per_project(runs, outdir, top_n_projects=30)
    plot_total_generated_per_tool_per_project(runs, outdir)

    print(f"Per-project graphs written to {outdir}/")

if __name__ == "__main__":
    main()
