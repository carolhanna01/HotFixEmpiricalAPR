#!/usr/bin/env python3
import argparse
import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List, Optional, Tuple


# ----------------------------
# Helpers
# ----------------------------

def safe_get(d: Any, path: List[str], default=None):
    cur = d
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def to_float(x) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None


def to_int(x) -> Optional[int]:
    try:
        if x is None:
            return None
        if isinstance(x, bool):
            return int(x)
        if isinstance(x, int):
            return x
        if isinstance(x, float):
            return int(x)
        if isinstance(x, str):
            m = re.search(r"-?\d+", x)
            return int(m.group(0)) if m else None
        return None
    except Exception:
        return None


def parse_bytes(s: Any) -> Optional[int]:
    if s is None:
        return None
    if isinstance(s, int):
        return s
    if isinstance(s, float):
        return int(s)
    if isinstance(s, str):
        m = re.search(r"(-?\d+)", s)
        if m:
            try:
                return int(m.group(1))
            except Exception:
                return None
    return None


def parse_mem_gib(s: Any) -> Optional[float]:
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return float(s)
    if not isinstance(s, str):
        return None

    m = re.search(r"([0-9]*\.?[0-9]+)\s*(GiB|MiB|KiB|B|bytes)\b", s, flags=re.IGNORECASE)
    if not m:
        return None

    val = float(m.group(1))
    unit = m.group(2).lower()
    if unit == "gib":
        return val
    if unit == "mib":
        return val / 1024.0
    if unit == "kib":
        return val / (1024.0 * 1024.0)
    if unit in ("b", "bytes"):
        return val / (1024.0 ** 3)
    return None


def detect_run_id_from_path(p: Path) -> Optional[str]:
    parts = [seg.lower() for seg in p.parts]
    patterns = [
        r"^run[_-]?(\d+)$",
        r"^seed[_-]?(\d+)$",
        r"^rep(?:licate)?[_-]?(\d+)$",
        r"^repeat[_-]?(\d+)$",
        r"^trial[_-]?(\d+)$",
    ]
    for seg in reversed(parts):
        for pat in patterns:
            m = re.match(pat, seg)
            if m:
                base = re.sub(r"[_-]?\d+$", "", seg)
                return f"{base}{m.group(1)}"
    return None


def is_run_json(obj: Any) -> bool:
    return isinstance(obj, dict) and ("status" in obj) and ("details" in obj or "info" in obj)


def find_candidate_jsons(root: Path) -> List[Path]:
    candidates: List[Path] = []
    for p in root.rglob("*.json"):
        if p.name.lower() in ("package.json", "composer.json"):
            continue
        try:
            if p.stat().st_size > 50 * 1024 * 1024:
                continue
        except Exception:
            pass
        candidates.append(p)
    return candidates


def is_success_status(status: Optional[str]) -> Optional[bool]:
    if status is None:
        return None
    s = status.lower()
    if "non-zero" in s or "error" in s or "failed" in s:
        return False
    if "success" in s or "ok" in s or "completed" in s:
        return True
    return None


def write_csv(path: Path, rows: List[Dict[str, Any]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ----------------------------
# JSON-tool record model
# ----------------------------

@dataclass
class RunRecord:
    tool: str
    json_path: str
    run_id: Optional[str]

    bug_subject: Optional[str]
    bug_benchmark: Optional[str]
    bug_id_str: Optional[str]
    bug_numeric_id: Optional[int]

    config_id: Optional[str]
    timeout_minutes: Optional[float]
    test_timeout_seconds: Optional[float]
    fault_location: Optional[str]
    passing_test_ratio: Optional[float]
    cpus: Optional[str]
    gpus: Optional[str]
    params: Optional[str]
    tag: Optional[str]
    container_id: Optional[str]

    status: Optional[str]
    total_duration_seconds: Optional[float]
    mem_gib: Optional[float]
    net_rx_bytes: Optional[int]
    net_tx_bytes: Optional[int]
    interfaces_count: Optional[int]

    search_space: Optional[int]
    enumerations: Optional[int]
    non_compilable: Optional[int]
    plausible: Optional[int]
    implausible: Optional[int]
    generated: Optional[int]


def normalize_record(tool: str, path: Path, obj: Dict[str, Any]) -> RunRecord:
    bug_info = safe_get(obj, ["info", "bug-info"], {}) or {}
    cfg_info = safe_get(obj, ["info", "config-info"], {}) or {}
    details = safe_get(obj, ["details"], {}) or {}
    time_d = safe_get(details, ["time"], {}) or {}
    cont_d = safe_get(details, ["container"], {}) or {}
    net_d = safe_get(cont_d, ["network_usage"], {}) or {}
    space_d = safe_get(details, ["space"], {}) or {}

    run_id = detect_run_id_from_path(path)

    bug_numeric_id = None
    if isinstance(bug_info.get("id"), int):
        bug_numeric_id = bug_info.get("id")
    else:
        try:
            bug_numeric_id = int(bug_info.get("id")) if bug_info.get("id") is not None else None
        except Exception:
            bug_numeric_id = None

    return RunRecord(
        tool=tool,
        json_path=str(path),
        run_id=run_id,

        bug_subject=bug_info.get("subject"),
        bug_benchmark=bug_info.get("benchmark"),
        bug_id_str=bug_info.get("bug_id"),
        bug_numeric_id=bug_numeric_id,

        config_id=cfg_info.get("id"),
        timeout_minutes=to_float(cfg_info.get("timeout")),
        test_timeout_seconds=to_float(cfg_info.get("test_timeout")),
        fault_location=cfg_info.get("fault_location"),
        passing_test_ratio=to_float(cfg_info.get("passing_test_ratio")),
        cpus=",".join(map(str, cfg_info.get("cpus", []))) if isinstance(cfg_info.get("cpus"), list) else (
            str(cfg_info.get("cpus")) if cfg_info.get("cpus") is not None else None
        ),
        gpus=",".join(map(str, cfg_info.get("gpus", []))) if isinstance(cfg_info.get("gpus"), list) else (
            str(cfg_info.get("gpus")) if cfg_info.get("gpus") is not None else None
        ),
        params=cfg_info.get("params"),
        tag=cfg_info.get("tag"),
        container_id=cfg_info.get("container-id"),

        status=obj.get("status"),
        total_duration_seconds=to_float(safe_get(time_d, ["total duration"])),
        mem_gib=parse_mem_gib(cont_d.get("mem_usage")),
        net_rx_bytes=parse_bytes(net_d.get("total_received")),
        net_tx_bytes=parse_bytes(net_d.get("total_transmitted")),
        interfaces_count=(int(net_d.get("interfaces_count")) if isinstance(net_d.get("interfaces_count"), int) else None),

        search_space=to_int(space_d.get("search space")),
        enumerations=to_int(space_d.get("enumerations")),
        non_compilable=to_int(space_d.get("non-compilable")),
        plausible=to_int(space_d.get("plausible")),
        implausible=to_int(space_d.get("implausible")),
        generated=to_int(space_d.get("generated")),
    )


def load_records(tool_name: str, tool_root: Path, strict_schema: bool = False) -> List[RunRecord]:
    records: List[RunRecord] = []
    for p in find_candidate_jsons(tool_root):
        try:
            with p.open("r", encoding="utf-8") as f:
                obj = json.load(f)
        except Exception:
            continue

        if not is_run_json(obj):
            if strict_schema:
                continue
            continue

        records.append(normalize_record(tool_name, p, obj))
    return records


def runrecord_to_dict(r: RunRecord) -> Dict[str, Any]:
    return {
        "tool": r.tool,
        "acr_setting": None,
        "patch_files": None,

        "json_path": r.json_path,
        "run_id": r.run_id,

        "bug_subject": r.bug_subject,
        "bug_benchmark": r.bug_benchmark,
        "bug_id": r.bug_id_str,
        "bug_numeric_id": r.bug_numeric_id,

        "config_id": r.config_id,
        "timeout_minutes": r.timeout_minutes,
        "test_timeout_seconds": r.test_timeout_seconds,
        "fault_location": r.fault_location,
        "passing_test_ratio": r.passing_test_ratio,
        "cpus": r.cpus,
        "gpus": r.gpus,
        "params": r.params,
        "tag": r.tag,
        "container_id": r.container_id,

        "status": r.status,
        "success": is_success_status(r.status),
        "total_duration_seconds": r.total_duration_seconds,
        "mem_gib": r.mem_gib,
        "net_rx_bytes": r.net_rx_bytes,
        "net_tx_bytes": r.net_tx_bytes,
        "interfaces_count": r.interfaces_count,

        "search_space": r.search_space,
        "enumerations": r.enumerations,
        "non_compilable": r.non_compilable,
        "plausible": r.plausible,
        "implausible": r.implausible,
        "generated": r.generated,
    }


# ----------------------------
# ACR collector (robust discovery)
# ----------------------------

def parse_acr_bug_folder_name(name: str):
    """
    Example: hadoop_0308423b_2025-10-16_21-33-55
    Returns: (project, bug_id, timestamp_str)
    """
    parts = name.split("_")
    project = parts[0] if len(parts) >= 1 else "UNKNOWN"
    bug_id = parts[1] if len(parts) >= 2 else None
    timestamp = "_".join(parts[2:]) if len(parts) >= 3 else None
    return project, bug_id, timestamp


def count_patch_files_in_dir(output_dir: Path) -> int:
    n = 0
    for p in output_dir.rglob("*"):
        if p.is_file() and "patch" in p.name.lower():
            n += 1
    return n


def _find_bugs_dirs(setting_dir: Path) -> List[Path]:
    """
    Find directories named 'bugs' under setting_dir (up to a few levels).
    """
    found: List[Path] = []
    # depth-limited search: setting_dir/*/bugs, setting_dir/*/*/bugs, setting_dir/bugs
    candidates = [
        setting_dir / "bugs",
    ]
    for d1 in setting_dir.iterdir() if setting_dir.exists() else []:
        if d1.is_dir():
            candidates.append(d1 / "bugs")
            for d2 in d1.iterdir():
                if d2.is_dir():
                    candidates.append(d2 / "bugs")

    for c in candidates:
        if c.exists() and c.is_dir() and c.name == "bugs":
            found.append(c)

    # de-dup
    uniq = []
    seen = set()
    for p in found:
        rp = str(p.resolve())
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return uniq


def collect_acr_runs(acr_root: Path, verbose: bool = False) -> List[Dict[str, Any]]:
    """
    For ACR:
    - One row per (tool, bug)
    - success = True if ANY output_* contains >=1 patch file
    - generated = total number of patch files across ALL outputs
    """
    rows: List[Dict[str, Any]] = []

    if not acr_root.exists() or not acr_root.is_dir():
        return rows

    # settings = llama3, llama3:70b
    setting_dirs = [p for p in acr_root.iterdir() if p.is_dir()]

    if verbose:
        print(f"[ACR] settings: {[p.name for p in setting_dirs]}")

    for setting_dir in setting_dirs:
        tool_name = f"acr_{setting_dir.name.replace(':', '_')}"

        bug_dirs = [p for p in setting_dir.iterdir() if p.is_dir()]

        if verbose:
            print(f"[ACR] {tool_name}: {len(bug_dirs)} bug dirs")

        for bug_dir in bug_dirs:
            project, bug_id, _ts = parse_acr_bug_folder_name(bug_dir.name)

            out_dirs = [
                p for p in bug_dir.iterdir()
                if p.is_dir() and p.name.lower().startswith("output_")
            ]

            total_patches = 0
            success = False

            for out_dir in out_dirs:
                patch_files = count_patch_files_in_dir(out_dir)
                total_patches += patch_files
                if patch_files > 0:
                    success = True

                if verbose:
                    print(
                        f"[ACR] {tool_name} | {bug_dir.name} | "
                        f"{out_dir.name} | patches={patch_files}"
                    )

            if verbose:
                print(
                    f"[ACR-BUG] {tool_name} | {bug_dir.name} | "
                    f"success={success} | generated={total_patches}"
                )

            rows.append({
                "tool": tool_name,
                "patch_files": total_patches,   # keep for debugging if you like

                "json_path": str(bug_dir),
                "run_id": bug_dir.name,         # bug-level run id

                "bug_subject": project,
                "bug_benchmark": None,
                "bug_id": bug_id,
                "bug_numeric_id": None,

                "config_id": None,
                "timeout_minutes": None,
                "test_timeout_seconds": None,
                "fault_location": None,
                "passing_test_ratio": None,
                "cpus": None,
                "gpus": None,
                "params": None,
                "tag": None,
                "container_id": None,

                "status": "filesystem_aggregated",
                "success": success,             # ✅ per bug
                "total_duration_seconds": None,
                "mem_gib": None,
                "net_rx_bytes": None,
                "net_tx_bytes": None,
                "interfaces_count": None,

                "search_space": None,
                "enumerations": None,
                "non_compilable": None,
                "plausible": None,
                "implausible": None,
                "generated": total_patches,     # ✅ per bug
            })

    if verbose:
        print(f"[ACR] total ACR bug-level rows collected: {len(rows)}")

    return rows


# ----------------------------
# Aggregations (dict-row based, includes ACR)
# ----------------------------

def aggregate_per_tool_from_rows(run_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_tool: Dict[str, List[Dict[str, Any]]] = {}
    for r in run_rows:
        by_tool.setdefault(r.get("tool", "UNKNOWN"), []).append(r)

    out: List[Dict[str, Any]] = []
    for tool, rs in sorted(by_tool.items()):
        bugs = set((r.get("bug_id") or str(r.get("bug_numeric_id")) or "UNKNOWN_BUG") for r in rs)
        out.append({
            "tool": tool,
            "runs_found": len(rs),
            "unique_bugs": len(bugs),
            "success_runs": sum(1 for r in rs if r.get("success") is True),
            "failure_runs": sum(1 for r in rs if r.get("success") is False),
            "unknown_status_runs": sum(1 for r in rs if r.get("success") is None),
        })
    return out


def record_key_from_row(r: Dict[str, Any]) -> Tuple[str, str]:
    bug = r.get("bug_id") or (str(r.get("bug_numeric_id")) if r.get("bug_numeric_id") is not None else "UNKNOWN_BUG")
    return (r.get("tool", "UNKNOWN"), bug)


def aggregate_per_bug_from_rows(run_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_bug: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for r in run_rows:
        by_bug.setdefault(record_key_from_row(r), []).append(r)

    out: List[Dict[str, Any]] = []
    for (tool, bug), rs in sorted(by_bug.items(), key=lambda x: (x[0][0], x[0][1])):
        durations = [r.get("total_duration_seconds") for r in rs if isinstance(r.get("total_duration_seconds"), (int, float))]
        mems = [r.get("mem_gib") for r in rs if isinstance(r.get("mem_gib"), (int, float))]

        succ = [r.get("success") for r in rs]
        succ_known = [s for s in succ if s is not None]

        out.append({
            "tool": tool,
            "bug": bug,
            "subject": next((r.get("bug_subject") for r in rs if r.get("bug_subject")), None),
            "benchmark": next((r.get("bug_benchmark") for r in rs if r.get("bug_benchmark")), None),

            "runs_found": len(rs),
            "success_runs": sum(1 for s in succ_known if s is True),
            "failure_runs": sum(1 for s in succ_known if s is False),
            "unknown_status_runs": sum(1 for s in succ if s is None),

            "avg_duration_s": (mean(durations) if durations else None),
            "min_duration_s": (min(durations) if durations else None),
            "max_duration_s": (max(durations) if durations else None),

            "avg_mem_gib": (mean(mems) if mems else None),
            "max_mem_gib": (max(mems) if mems else None),
        })
    return out


def aggregate_acr_patchfiles_per_project(run_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = [r for r in run_rows if r.get("tool") == "acr"]
    by: Dict[Tuple[str, str], int] = {}
    for r in rows:
        key = (r.get("acr_setting") or "UNKNOWN", r.get("bug_subject") or "UNKNOWN")
        by[key] = by.get(key, 0) + int(r.get("patch_files") or 0)

    out: List[Dict[str, Any]] = []
    for (setting, project), total in sorted(by.items()):
        out.append({
            "acr_setting": setting,
            "project": project,
            "total_patch_files": total,
        })
    return out


# ----------------------------
# CLI + Main
# ----------------------------

def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Analyze APRTools JSON outputs + ACR patch-file counting."
    )
    ap.add_argument("--repairllama", type=str, required=True, help="Path to repairllama root directory")
    ap.add_argument("--cardumen", type=str, required=True, help="Path to cardumen root directory")
    ap.add_argument("--arja", type=str, required=True, help="Path to arja root directory")
    ap.add_argument("--acr", type=str, default=None, help="Path to ACR root directory (optional)")
    ap.add_argument("--out", type=str, default="out", help="Output directory (default: out)")
    ap.add_argument("--jsonl", action="store_true", help="Also write runs.jsonl")
    ap.add_argument("--strict", action="store_true", help="Strictly require run-json schema")
    ap.add_argument("--verbose", action="store_true", help="Verbose discovery output (especially for ACR)")
    return ap.parse_args()


def main() -> int:
    args = parse_args()
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # JSON tools only
    tool_paths = {
        "repairllama": Path(args.repairllama),
        "cardumen": Path(args.cardumen),
        "arja": Path(args.arja),
    }

    all_records: List[RunRecord] = []
    for tool, root in tool_paths.items():
        if not root.exists():
            raise FileNotFoundError(f"{tool} path does not exist: {root}")
        all_records.extend(load_records(tool, root, strict_schema=args.strict))

    run_rows: List[Dict[str, Any]] = [runrecord_to_dict(r) for r in all_records]

    # Add ACR rows
    if args.acr:
        acr_root = Path(args.acr)
        if not acr_root.exists():
            raise FileNotFoundError(f"ACR path does not exist: {acr_root}")
        acr_rows = collect_acr_runs(acr_root, verbose=args.verbose)
        run_rows.extend(acr_rows)

        if args.verbose:
            print(f"[ACR] appended {len(acr_rows)} rows to run_rows")

    # runs.csv schema (fixed order)
    run_fields = [
        "tool", "acr_setting", "patch_files",
        "json_path", "run_id",
        "bug_subject", "bug_benchmark", "bug_id", "bug_numeric_id",
        "config_id", "timeout_minutes", "test_timeout_seconds", "fault_location", "passing_test_ratio",
        "cpus", "gpus", "params", "tag", "container_id",
        "status", "success", "total_duration_seconds",
        "mem_gib", "net_rx_bytes", "net_tx_bytes", "interfaces_count",
        "search_space", "enumerations", "non_compilable", "plausible", "implausible", "generated",
    ]

    write_csv(out_dir / "runs.csv", run_rows, run_fields)
    if args.jsonl:
        write_jsonl(out_dir / "runs.jsonl", run_rows)

    # Summaries INCLUDE ACR (dict-row based)
    bug_rows = aggregate_per_bug_from_rows(run_rows)
    write_csv(
        out_dir / "bugs_summary.csv",
        bug_rows,
        [
            "tool", "bug", "subject", "benchmark",
            "runs_found", "success_runs", "failure_runs", "unknown_status_runs",
            "avg_duration_s", "min_duration_s", "max_duration_s",
            "avg_mem_gib", "max_mem_gib",
        ],
    )

    tool_rows = aggregate_per_tool_from_rows(run_rows)
    write_csv(
        out_dir / "tools_summary_all.csv",
        tool_rows,
        ["tool", "runs_found", "unique_bugs", "success_runs", "failure_runs", "unknown_status_runs"],
    )

    if args.acr:
        acr_proj_rows = aggregate_acr_patchfiles_per_project(run_rows)
        write_csv(
            out_dir / "acr_patchfiles_per_project.csv",
            acr_proj_rows,
            ["acr_setting", "project", "total_patch_files"],
        )

    # Console summary
    print(f"Parsed JSON-tool run records: {len(all_records)}")
    print(f"Total run rows (including ACR if provided): {len(run_rows)}")
    print(f"Wrote: {out_dir / 'runs.csv'}")
    print(f"Wrote: {out_dir / 'bugs_summary.csv'}")
    print(f"Wrote: {out_dir / 'tools_summary_all.csv'}")
    if args.acr:
        print(f"Wrote: {out_dir / 'acr_patchfiles_per_project.csv'}")
    if args.jsonl:
        print(f"Wrote: {out_dir / 'runs.jsonl'}")

    for row in tool_rows:
        print(
            f"- {row['tool']}: runs={row['runs_found']}, bugs={row['unique_bugs']}, "
            f"success={row['success_runs']}, fail={row['failure_runs']}, unknown={row['unknown_status_runs']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
