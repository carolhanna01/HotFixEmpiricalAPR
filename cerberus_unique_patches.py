import sys
import hashlib
from pathlib import Path
from collections import defaultdict

def normalize_patch(text: str) -> str:
    """
    Normalize a patch for semantic uniqueness.
    """
    lines = []
    for line in text.splitlines():
        if line.startswith('--- ') or line.startswith('+++ '):
            continue
        if line.startswith('@@'):
            continue
        lines.append(line.rstrip())
    return "\n".join(lines)

def get_bug_id(root: Path, patch_file: Path) -> str:
    """
    Extract bug ID from directory name:
    bugsdotjar-repairllama-hbase-190c253c-TP1-CP1-2-e02d73e5c0
    -> bugsdotjar-repairllama-hbase-190c253c
    """
    rel = patch_file.relative_to(root)
    dirname = rel.parts[0]
    return "-".join(dirname.split("-")[:4])

def main(root_dir: str):
    root = Path(root_dir)
    if not root.exists():
        print(f"Error: path does not exist: {root_dir}")
        sys.exit(1)

    # bug_id -> list of patch files
    bug_to_patches = defaultdict(list)

    for patch_file in root.rglob("*.patch"):
        bug_id = get_bug_id(root, patch_file)
        bug_to_patches[bug_id].append(patch_file)

    # bug_id -> set of unique patch hashes
    bug_unique_hashes = defaultdict(set)

    for bug_id, patches in bug_to_patches.items():
        for patch_file in patches:
            try:
                content = patch_file.read_text(errors="ignore")
            except Exception:
                continue

            normalized = normalize_patch(content)
            h = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
            bug_unique_hashes[bug_id].add(h)

    # Print summary
    header = f"{'bug_id':35}  {'total_patch_files':18}  {'unique_patches'}"
    print(header)

    total_files = 0
    total_unique = 0

    for bug_id in sorted(bug_to_patches.keys()):
        total = len(bug_to_patches[bug_id])
        unique = len(bug_unique_hashes[bug_id])

        total_files += total
        total_unique += unique

        print(f"{bug_id:35}  {total:<18}  {unique}")

    print(f"{'TOTAL':35}  {total_files:<18}  {total_unique}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize_unique_patches.py <results_root_dir>")
        sys.exit(1)

    main(sys.argv[1])
