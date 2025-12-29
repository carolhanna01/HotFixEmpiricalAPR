#!/usr/bin/env python3
import os
import re
import sys
import hashlib
from collections import defaultdict

# --------- Customize this if needed ----------
# Bug id is assumed to be the first 2 path components under the root:
#   root/BUGID/.../patch_raw_*.md
# Example path:
#   llama3:70b/ambari_f4e0f6ca_2025-10-31_14-49-27/output_0/patch_raw_0.md
# Bug id becomes:
#   ambari_f4e0f6ca_2025-10-31_14-49-27
def bug_id_from_relpath(relpath: str) -> str:
    parts = relpath.split(os.sep)
    return parts[0] if len(parts) >= 2 else relpath
# --------------------------------------------

FILE_RE = re.compile(r"<file>(.*?)</file>", re.DOTALL)
PATCHED_RE = re.compile(r"<patched>(.*?)</patched>", re.DOTALL)

def normalize(s: str) -> str:
    # Normalize whitespace to make matching stable across formatting differences
    s = s.replace("\r\n", "\n").replace("\r", "\n").strip()
    # collapse trailing spaces per line
    s = "\n".join(line.rstrip() for line in s.split("\n"))
    return s

def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def extract_patch_signature(text: str) -> str:
    """
    Build a canonical signature for ONE patch file:
    - Extract all <file>...</file> and <patched>...</patched> blocks
    - Pair them best-effort
    - Canonicalize into a single string and hash it
    """
    files = [normalize(x) for x in FILE_RE.findall(text)]
    patched_blocks = [normalize(x) for x in PATCHED_RE.findall(text)]

    # If no patched blocks -> signature for "empty/invalid patch"
    if not patched_blocks:
        return sha1("NO_PATCHED_BLOCKS")

    # Best-effort pairing.
    # Common case: one <file> per <patched>.
    pairs = []
    if len(files) == len(patched_blocks):
        pairs = list(zip(files, patched_blocks))
    elif len(files) == 0:
        pairs = [("UNKNOWN_FILE", b) for b in patched_blocks]
    else:
        # Heuristic: if mismatch, attach blocks in order to available files,
        # reusing the last file if blocks > files.
        last = files[0]
        for i, b in enumerate(patched_blocks):
            f = files[i] if i < len(files) else last
            last = f
            pairs.append((f, b))

    # Canonical representation of the entire patch file.
    # IMPORTANT: we keep ORDER, because two patches with same blocks but
    # different ordering might not be truly identical in intent.
    canonical = []
    for f, b in pairs:
        canonical.append(f"FILE:{f}\nPATCHED:\n{b}\nEND_PATCHED\n")
    canonical_text = "\n".join(canonical)

    return sha1(canonical_text)

def main(root: str):
    # Per bug:
    # - total patch files
    # - unique patch signatures
    total_patch_files = defaultdict(int)
    unique_patch_sigs = defaultdict(set)

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if "patch_raw" not in name:
                continue
            fullpath = os.path.join(dirpath, name)
            relpath = os.path.relpath(fullpath, start=root)
            bug = bug_id_from_relpath(relpath)

            total_patch_files[bug] += 1

            try:
                with open(fullpath, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception:
                # unreadable file -> treat as unique "unreadable"
                unique_patch_sigs[bug].add(sha1(f"UNREADABLE:{relpath}"))
                continue

            sig = extract_patch_signature(text)
            unique_patch_sigs[bug].add(sig)

    bugs = sorted(set(total_patch_files.keys()) | set(unique_patch_sigs.keys()))
    print("bug_id\ttotal_patch_files\tunique_patches")

    sum_files = 0
    sum_unique = 0

    for bug in bugs:
        tf = total_patch_files[bug]
        up = len(unique_patch_sigs[bug])
        sum_files += tf
        sum_unique += up
        print(f"{bug}\t{tf}\t{up}")

    print(f"TOTAL\t{sum_files}\t{sum_unique}")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    main(root)
