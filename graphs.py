from __future__ import annotations

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


RUNS_CSV = "out/runs.csv"
BUGS_SUMMARY_CSV = "out/bugs_summary.csv"
TOOLS_SUMMARY_CSV = "out/tools_summary_all.csv"
ACR_PATCHFILES_PER_PROJECT_CSV = "out/acr_patchfiles_per_project.csv"

OUTDIR = "plots"


# ----------------------------
# Helpers
# ----------------------------
def ensure_outdir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def savefig(name: str) -> None:
    path = os.path.join(OUTDIR, name)
    plt.tight_layout()
    plt.savefig(path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"saved: {path}")

def safe_numeric(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")
    return out

def top_n(series: pd.Series, n: int = 10) -> pd.Series:
    s = series.dropna()
    return s.value_counts().head(n)

def success_rate(success_col: pd.Series) -> float:
    s = pd.to_numeric(success_col, errors="coerce")
    s = s.dropna()
    if len(s) == 0:
        return float("nan")
    # In your data, success looks like 0/1
    return float((s == 1).mean())

def make_correlation_heatmap(df: pd.DataFrame, title: str, fname: str) -> None:
    # Use numeric cols only, and require some variance
    num = df.select_dtypes(include=[np.number]).copy()
    num = num.dropna(axis=1, how="all")
    num = num.loc[:, num.nunique(dropna=True) > 1]
    if num.shape[1] < 2:
        return

    corr = num.corr(numeric_only=True)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)
    im = ax.imshow(corr.values, aspect="auto")  # no explicit colormap
    ax.set_title(title)
    ax.set_xticks(range(corr.shape[1]))
    ax.set_yticks(range(corr.shape[0]))
    ax.set_xticklabels(corr.columns, rotation=60, ha="right")
    ax.set_yticklabels(corr.index)
    fig.colorbar(im, ax=ax, shrink=0.8)
    savefig(fname)


# ----------------------------
# Plots from tools_summary_all.csv
# ----------------------------
def plot_tools_summary(tools: pd.DataFrame) -> None:
    if tools.empty:
        return

    tools = safe_numeric(
        tools,
        ["runs_found", "unique_bugs", "success_runs", "failure_runs", "unknown_status_runs"],
    )
    tools = tools.sort_values("runs_found", ascending=False)

    # 1) Stacked bar: success/failure/unknown per tool
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    x = np.arange(len(tools))
    success = tools["success_runs"].fillna(0).to_numpy()
    failure = tools["failure_runs"].fillna(0).to_numpy()
    unknown = tools["unknown_status_runs"].fillna(0).to_numpy()

    ax.bar(x, success, label="success_runs")
    ax.bar(x, failure, bottom=success, label="failure_runs")
    ax.bar(x, unknown, bottom=success + failure, label="unknown_status_runs")

    ax.set_xticks(x)
    ax.set_xticklabels(tools["tool"].astype(str), rotation=30, ha="right")
    ax.set_ylabel("runs")
    ax.set_title("Runs by tool (stacked success/failure/unknown)")
    ax.legend()
    savefig("tools_stacked_success_failure_unknown.png")

    # 2) Success rate bar
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)

    denom = tools["runs_found"].replace(0, np.nan)
    rate = (tools["success_runs"] / denom).astype(float)
    ax.bar(np.arange(len(tools)), rate.to_numpy())
    ax.set_xticks(np.arange(len(tools)))
    ax.set_xticklabels(tools["tool"].astype(str), rotation=30, ha="right")
    ax.set_ylim(0, 1)
    ax.set_ylabel("success rate")
    ax.set_title("Success rate by tool (success_runs / runs_found)")
    savefig("tools_success_rate.png")


# ----------------------------
# Plots from bugs_summary.csv
# ----------------------------
def plot_bugs_summary(bugs: pd.DataFrame) -> None:
    if bugs.empty:
        return

    bugs = safe_numeric(
        bugs,
        ["runs_found", "success_runs", "failure_runs", "unknown_status_runs",
         "avg_duration_s", "min_duration_s", "max_duration_s", "avg_mem_gib", "max_mem_gib"],
    )

    # 3) Top subjects by total runs_found
    if "subject" in bugs.columns and "runs_found" in bugs.columns:
        subj = (
            bugs.groupby("subject", dropna=True)["runs_found"]
            .sum()
            .sort_values(ascending=False)
            .head(15)
        )
        fig = plt.figure(figsize=(10, 5))
        ax = fig.add_subplot(111)
        ax.bar(np.arange(len(subj)), subj.to_numpy())
        ax.set_xticks(np.arange(len(subj)))
        ax.set_xticklabels(subj.index.astype(str), rotation=30, ha="right")
        ax.set_ylabel("total runs_found")
        ax.set_title("Top subjects (projects) by total runs_found (bugs_summary)")
        savefig("bugs_top_subjects_by_runs_found.png")

    # 4) Tool x Subject heatmap: success rate
    # subject is your "project" (ambari, arja, ...)
    required = {"tool", "subject", "success_runs", "runs_found"}
    if required.issubset(bugs.columns):
        agg = (
            bugs.groupby(["tool", "subject"], dropna=False)[["success_runs", "runs_found"]]
            .sum()
            .reset_index()
        )
        agg["success_rate"] = agg["success_runs"] / agg["runs_found"]

        # Success-rate matrix
        mat_rate = agg.pivot(index="tool", columns="subject", values="success_rate")

        # Count matrix (so you can judge sample size)
        mat_n = agg.pivot(index="tool", columns="subject", values="runs_found")

        # remove empty (all-NaN) project columns
        mat_rate = mat_rate.dropna(axis=1, how="all")
        mat_n = mat_n.dropna(axis=1, how="all")

        # Drop subject/project columns with zero total runs across all tools
        valid_subjects = mat_n.sum(axis=0) > 0
        mat_rate = mat_rate.loc[:, valid_subjects]
        mat_n = mat_n.loc[:, valid_subjects]

        if mat_rate.shape[0] > 0 and mat_rate.shape[1] > 0:
            # Success rate heatmap
            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(111)
            im = ax.imshow(mat_rate.values, aspect="auto")  # no explicit colormap
            ax.set_title("Success rate heatmap (tool × project)")
            ax.set_xticks(range(mat_rate.shape[1]))
            ax.set_yticks(range(mat_rate.shape[0]))
            ax.set_xticklabels(mat_rate.columns.astype(str), rotation=45, ha="right")
            ax.set_yticklabels(mat_rate.index.astype(str))
            fig.colorbar(im, ax=ax, shrink=0.8)
            savefig("bugs_tool_by_subject_success_rate_heatmap.png")

            # Runs-found heatmap (volume)
            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(111)
            im = ax.imshow(mat_n.values, aspect="auto")  # no explicit colormap
            ax.set_title("Run volume heatmap (runs_found) (tool × project)")
            ax.set_xticks(range(mat_n.shape[1]))
            ax.set_yticks(range(mat_n.shape[0]))
            ax.set_xticklabels(mat_n.columns.astype(str), rotation=45, ha="right")
            ax.set_yticklabels(mat_n.index.astype(str))
            fig.colorbar(im, ax=ax, shrink=0.8)
            savefig("bugs_tool_by_subject_runs_found_heatmap.png")

    # 5) Distribution of avg_duration_s
    if "avg_duration_s" in bugs.columns:
        d = bugs["avg_duration_s"].dropna()
        if len(d) > 0:
            fig = plt.figure(figsize=(8, 5))
            ax = fig.add_subplot(111)
            ax.hist(d.to_numpy(), bins=30)
            ax.set_xlabel("avg_duration_s")
            ax.set_ylabel("count")
            ax.set_title("Histogram of avg_duration_s (bugs_summary)")
            savefig("bugs_avg_duration_hist.png")


# ----------------------------
# Plots from runs.csv
# ----------------------------
def plot_runs(runs: pd.DataFrame) -> None:
    if runs.empty:
        return

    # Coerce common numeric columns
    num_cols = [
        "patch_files", "passing_test_ratio", "cpus", "gpus", "params",
        "total_duration_seconds", "mem_gib", "net_rx_bytes", "net_tx_bytes",
        "interfaces_count", "timeout_minutes", "test_timeout_seconds",
        "search_space", "enumerations", "non_compilable", "plausible",
        "implausible", "generated",
    ]
    runs = safe_numeric(runs, num_cols)

    # 6) Status counts by tool (stacked)
    if {"tool", "status"}.issubset(runs.columns):
        ctab = pd.crosstab(runs["tool"], runs["status"]).sort_index()
        if ctab.shape[0] > 0 and ctab.shape[1] > 0:
            fig = plt.figure(figsize=(12, 6))
            ax = fig.add_subplot(111)

            x = np.arange(ctab.shape[0])
            bottom = np.zeros(ctab.shape[0])

            for col in ctab.columns:
                vals = ctab[col].to_numpy()
                ax.bar(x, vals, bottom=bottom, label=str(col))
                bottom = bottom + vals

            ax.set_xticks(x)
            ax.set_xticklabels(ctab.index.astype(str), rotation=30, ha="right")
            ax.set_ylabel("count")
            ax.set_title("Run status distribution by tool (runs.csv)")
            ax.legend(ncol=2, fontsize=8)
            savefig("runs_status_by_tool_stacked.png")

    # 7) Success rate by tool with 95% Wilson CI (nice + informative)
    if {"tool", "success"}.issubset(runs.columns):
        grp = runs.groupby("tool")["success"]
        tools = []
        rates = []
        lo = []
        hi = []
        nvals = []

        for tool, s in grp:
            s = pd.to_numeric(s, errors="coerce").dropna()
            n = len(s)
            if n == 0:
                continue
            k = int((s == 1).sum())
            phat = k / n

            # Wilson interval
            z = 1.96
            denom = 1 + (z**2) / n
            center = (phat + (z**2) / (2*n)) / denom
            half = (z * math.sqrt((phat*(1-phat)/n) + (z**2)/(4*n*n))) / denom
            tools.append(str(tool))
            rates.append(phat)
            lo.append(max(0.0, center - half))
            hi.append(min(1.0, center + half))
            nvals.append(n)

        if tools:
            order = np.argsort(rates)[::-1]
            tools = [tools[i] for i in order]
            rates = np.array([rates[i] for i in order])
            lo = np.array([lo[i] for i in order])
            hi = np.array([hi[i] for i in order])

            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            x = np.arange(len(tools))
            ax.bar(x, rates)
            ax.errorbar(x, rates, yerr=[rates - lo, hi - rates], fmt="none", capsize=3)

            ax.set_xticks(x)
            ax.set_xticklabels(tools, rotation=30, ha="right")
            ax.set_ylim(0, 1)
            ax.set_ylabel("success rate")
            ax.set_title("Success rate by tool with 95% Wilson CI (runs.csv)")
            savefig("runs_success_rate_wilson_ci.png")

    # 8) Boxplot: total_duration_seconds by tool (log10 scale via transform)
    if {"tool", "total_duration_seconds"}.issubset(runs.columns):
        tmp = runs[["tool", "total_duration_seconds"]].dropna()
        if len(tmp) > 0:
            # log transform for readability, keep only positive durations
            tmp = tmp[tmp["total_duration_seconds"] > 0]
            if len(tmp) > 0:
                tmp["log10_duration"] = np.log10(tmp["total_duration_seconds"].astype(float))

                # take top tools by count for readability
                counts = tmp["tool"].value_counts().head(10).index
                tmp = tmp[tmp["tool"].isin(counts)]

                data = [tmp.loc[tmp["tool"] == t, "log10_duration"].to_numpy() for t in counts]

                fig = plt.figure(figsize=(10, 6))
                ax = fig.add_subplot(111)
                ax.boxplot(data, labels=[str(t) for t in counts], showfliers=False)
                ax.set_ylabel("log10(total_duration_seconds)")
                ax.set_title("Duration by tool (boxplot, log10 scale) (runs.csv)")
                plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
                savefig("runs_duration_boxplot_log10_by_tool.png")

    # 9) Scatter: patch_files vs duration, colored by tool (small multiple via legend)
    if {"patch_files", "total_duration_seconds", "tool"}.issubset(runs.columns):
        tmp = runs[["patch_files", "total_duration_seconds", "tool"]].dropna()
        tmp = tmp[(tmp["patch_files"] >= 0) & (tmp["total_duration_seconds"] > 0)]
        if len(tmp) > 0:
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)

            # plot each tool separately so matplotlib assigns different colors automatically
            for tool, sub in tmp.groupby("tool"):
                ax.scatter(sub["patch_files"].to_numpy(), sub["total_duration_seconds"].to_numpy(), s=18, alpha=0.7, label=str(tool))

            ax.set_yscale("log")
            ax.set_xlabel("patch_files")
            ax.set_ylabel("total_duration_seconds (log scale)")
            ax.set_title("Patch files vs duration (runs.csv)")
            ax.legend(fontsize=8, ncol=2)
            savefig("runs_patch_files_vs_duration_scatter.png")

    # 10) Correlation heatmap of numeric metrics
    make_correlation_heatmap(runs, "Correlation (numeric metrics) (runs.csv)", "runs_numeric_correlation_heatmap.png")


# ----------------------------
# Optional: ACR patchfiles per project (yours is empty right now)
# ----------------------------
def plot_acr_patchfiles(acr: pd.DataFrame) -> None:
    if acr.empty:
        print("note: acr_patchfiles_per_project.csv is empty (0 rows), skipping its plots.")
        return

    acr = safe_numeric(acr, ["total_patch_files"])

    # 11) Top projects by total_patch_files, grouped by acr_setting
    if {"acr_setting", "project", "total_patch_files"}.issubset(acr.columns):
        top = acr.sort_values("total_patch_files", ascending=False).head(20)
        fig = plt.figure(figsize=(12, 6))
        ax = fig.add_subplot(111)

        # encode acr_setting via different markers/colors (matplotlib will auto color)
        for setting, sub in top.groupby("acr_setting"):
            ax.scatter(np.arange(len(sub)), sub["total_patch_files"].to_numpy(), s=30, alpha=0.8, label=str(setting))

        ax.set_xticks(np.arange(len(top)))
        ax.set_xticklabels(top["project"].astype(str), rotation=45, ha="right")
        ax.set_ylabel("total_patch_files")
        ax.set_title("Top projects by total_patch_files (colored by acr_setting)")
        ax.legend(fontsize=8)
        savefig("acr_top_projects_patch_files_scatter.png")


def main() -> None:
    ensure_outdir(OUTDIR)

    # Load
    runs = pd.read_csv(RUNS_CSV)
    bugs = pd.read_csv(BUGS_SUMMARY_CSV)
    tools = pd.read_csv(TOOLS_SUMMARY_CSV)
    acr = pd.read_csv(ACR_PATCHFILES_PER_PROJECT_CSV)

    # Plot
    plot_tools_summary(tools)
    plot_bugs_summary(bugs)
    plot_runs(runs)
    plot_acr_patchfiles(acr)

    print("done.")


if __name__ == "__main__":
    main()
