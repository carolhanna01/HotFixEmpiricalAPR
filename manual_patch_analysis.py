#!/usr/bin/env python3
import os
import re
import sys
import hashlib
from collections import defaultdict

# --- ACR "pseudo patch" format ---
FILE_RE = re.compile(r"<file>(.*?)</file>", re.DOTALL)
PATCHED_RE = re.compile(r"<patched>(.*?)</patched>", re.DOTALL)

# --- Unified diff format (RepairLLaMA etc.) ---
DIFF_FILE_RE = re.compile(r"^\+\+\+\s+(.*)$", re.MULTILINE)  # +++ b/path or +++ path or +++ /dev/null
DIFF_GIT_RE = re.compile(r"^diff --git\s+a/(.*?)\s+b/(.*?)\s*$", re.MULTILINE)

def normalize(s: str) -> str:
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    return s

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def bug_id_from_relpath(relpath: str) -> str:
    """
    Works for both layouts as long as "root" is the folder containing bug folders.

    Example ACR:
      root/ambari_xxx/output_0/patch_raw_0.md -> bug_id = ambari_xxx

    Example RepairLLaMA:
      root/bugsdotjar-repairllama-flink-.../output/patches/1.patch -> bug_id = bugsdotjar-repairllama-flink-...
    """
    parts = relpath.split(os.sep)
    return parts[0] if parts else relpath

def extract_pairs_acr(text: str):
    """Return list of (file_path, patched_block) for ACR-style patches."""
    files = [normalize(x) for x in FILE_RE.findall(text)]
    blocks = [normalize(x) for x in PATCHED_RE.findall(text)]
    if not blocks:
        return []

    if len(files) == len(blocks):
        return list(zip(files, blocks))

    if not files:
        return [("UNKNOWN_FILE", b) for b in blocks]

    # heuristic: assign blocks in order to files, reuse last file if needed
    pairs = []
    last = files[0]
    for i, b in enumerate(blocks):
        f = files[i] if i < len(files) else last
        last = f
        pairs.append((f, b))
    return pairs

def patch_signature_acr(pairs):
    """Signature for an ACR patch file, accounting for multiple blocks; keeps order."""
    if not pairs:
        return sha1("NO_PATCHED_BLOCKS")
    canonical = []
    for f, b in pairs:
        canonical.append(f"FILE:{f}\nPATCHED:\n{b}\nEND_PATCHED\n")
    return sha1("\n".join(canonical))

def extract_diff_files(diff_text: str):
    """
    Extract modified file paths from a unified diff.
    Prefer diff --git, fall back to +++ lines.
    """
    files = set()

    for a, b in DIFF_GIT_RE.findall(diff_text):
        # usually b is the new path; keep b for readability
        files.add(b.strip())

    if not files:
        for m in DIFF_FILE_RE.findall(diff_text):
            p = m.strip()
            if p.endswith("/dev/null") or p == "/dev/null":
                continue
            # strip common prefixes
            if p.startswith("b/"):
                p = p[2:]
            elif p.startswith("a/"):
                p = p[2:]
            files.add(p)

    return sorted(files)

def normalize_diff_for_signature(diff_text: str) -> str:
    """
    Normalize diff text to make signatures stable:
    - normalize newlines
    - strip trailing spaces
    - remove some metadata lines that can vary but do not change semantics
      (feel free to tweak if you want stricter/looser uniqueness)
    """
    lines = normalize(diff_text).split("\n")
    cleaned = []
    for line in lines:
        # optional: drop index lines (often changes with repo state)
        if line.startswith("index "):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()

def patch_signature_diff(diff_text: str) -> str:
    canonical = normalize_diff_for_signature(diff_text)
    if not canonical:
        return sha1("EMPTY_DIFF")
    return sha1(canonical)

def fence_language_from_path(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    return {
        ".py": "python",
        ".java": "java",
        ".kt": "kotlin",
        ".scala": "scala",
        ".go": "go",
        ".js": "javascript",
        ".ts": "typescript",
        ".c": "c",
        ".cc": "cpp",
        ".cpp": "cpp",
        ".h": "c",
        ".hpp": "cpp",
        ".rb": "ruby",
        ".php": "php",
        ".sh": "bash",
        ".xml": "xml",
        ".yml": "yaml",
        ".yaml": "yaml",
        ".json": "json",
        ".md": "markdown",
    }.get(ext, "")

def safe_mkdir(path: str):
    os.makedirs(path, exist_ok=True)

def is_patch_file(filename: str) -> bool:
    return ("patch_raw" in filename) or filename.endswith(".patch")

def classify_patch(text: str, filename: str) -> str:
    """
    Returns "acr" or "diff" or "unknown"
    """
    if "<patched>" in text and "</patched>" in text:
        return "acr"
    # unified diff heuristics
    if "diff --git " in text or ("\n--- " in text and "\n+++ " in text) or text.startswith("--- "):
        return "diff"
    # RepairLLaMA patches are typically *.patch; treat those as diff even if minimal
    if filename.endswith(".patch"):
        return "diff"
    return "unknown"

def main(root: str, out_dir: str):
    # bug -> list of patch files
    bug_to_patchfiles = defaultdict(list)

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if not is_patch_file(name):
                continue
            fullpath = os.path.join(dirpath, name)
            relpath = os.path.relpath(fullpath, start=root)
            bug = bug_id_from_relpath(relpath)
            bug_to_patchfiles[bug].append(fullpath)

    safe_mkdir(out_dir)

    for bug, patchfiles in sorted(bug_to_patchfiles.items()):
        # signature -> sources + representative rendering payload
        sig_to_sources = defaultdict(list)   # sig -> [paths]
        sig_to_repr = {}                     # sig -> dict(kind=..., ...)
        invalid = []                         # files unreadable/unknown/no patch content

        for pf in sorted(patchfiles):
            try:
                with open(pf, "r", encoding="utf-8", errors="ignore") as f:
                    txt = f.read()
            except Exception:
                invalid.append((pf, "unreadable"))
                continue

            kind = classify_patch(txt, os.path.basename(pf))

            if kind == "acr":
                pairs = extract_pairs_acr(txt)
                if not pairs:
                    invalid.append((pf, "no <patched> blocks"))
                    continue
                sig = patch_signature_acr(pairs)
                sig_to_sources[sig].append(pf)
                if sig not in sig_to_repr:
                    sig_to_repr[sig] = {"kind": "acr", "pairs": pairs}

            elif kind == "diff":
                norm = normalize(txt)
                if not norm:
                    invalid.append((pf, "empty diff"))
                    continue
                sig = patch_signature_diff(norm)
                sig_to_sources[sig].append(pf)
                if sig not in sig_to_repr:
                    sig_to_repr[sig] = {
                        "kind": "diff",
                        "diff": norm,
                        "files": extract_diff_files(norm),
                    }
            else:
                invalid.append((pf, "unknown format"))
                continue

        bug_out = os.path.join(out_dir, bug)
        safe_mkdir(bug_out)

        readme_path = os.path.join(bug_out, "README.md")
        total_patch_files = len(patchfiles)
        unique_patches = len(sig_to_sources)

        with open(readme_path, "w", encoding="utf-8") as out:
            out.write(f"# Bug: {bug}\n\n")
            out.write("## Summary\n")
            out.write(f"- Total patch files: **{total_patch_files}**\n")
            out.write(f"- Unique patches: **{unique_patches}**\n")
            out.write(f"- Invalid/unparseable patch files: **{len(invalid)}**\n\n")

            if invalid:
                out.write("## Invalid / unparseable patch files\n")
                for pf, reason in invalid:
                    out.write(f"- `{os.path.relpath(pf, start=root)}` — {reason}\n")
                out.write("\n---\n\n")

            for idx, (sig, sources) in enumerate(sorted(sig_to_sources.items()), start=1):
                short_sig = sig[:10]
                out.write(f"## Patch {idx} (signature: `{short_sig}`)\n\n")
                out.write("**Source patch files (duplicates):**\n")
                for s in sources:
                    out.write(f"- `{os.path.relpath(s, start=root)}`\n")
                out.write("\n")

                rep = sig_to_repr[sig]
                if rep["kind"] == "acr":
                    pairs = rep["pairs"]

                    file_to_blocks = defaultdict(list)
                    for fpath, block in pairs:
                        file_to_blocks[fpath].append(block)

                    out.write("**Modifications (ACR `<patched>` blocks):**\n\n")
                    for fpath, blocks in file_to_blocks.items():
                        out.write(f"### `{fpath}`\n\n")
                        lang = fence_language_from_path(fpath)
                        for b_i, block in enumerate(blocks, start=1):
                            if len(blocks) > 1:
                                out.write(f"**Block {b_i}:**\n\n")
                            out.write(f"```{lang}\n{block}\n```\n\n")

                elif rep["kind"] == "diff":
                    files = rep.get("files", [])
                    out.write("**Modifications (unified diff):**\n\n")
                    if files:
                        out.write("**Files modified:**\n")
                        for fp in files:
                            out.write(f"- `{fp}`\n")
                        out.write("\n")
                    out.write("```diff\n")
                    out.write(rep["diff"])
                    out.write("\n```\n\n")

                out.write("---\n\n")

        print(f"Wrote: {readme_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 make_patch_dossiers.py <ROOT_DIR> <OUT_DIR>")
        print("Example: python3 make_patch_dossiers.py 'llama3:70b' analysis")
        print("Example: python3 make_patch_dossiers.py '.' analysis")
        sys.exit(1)

    root_dir = sys.argv[1]
    out_dir = sys.argv[2]
    main(root_dir, out_dir)
