import subprocess
import csv
import io
import os
import sys
import shutil
from collections import defaultdict


def _find_lizard() -> str:
    """Find the lizard executable."""
    # First try PATH
    lizard = shutil.which("lizard")
    if lizard:
        return lizard
    # Fallback: look next to the current Python executable
    python_dir = os.path.dirname(sys.executable)
    for candidate in [os.path.join(python_dir, "lizard"),
                      os.path.join(python_dir, "lizard.exe")]:
        if os.path.isfile(candidate):
            return candidate
    raise FileNotFoundError(
        "lizard not found in PATH or alongside Python. "
        "Install with: pip install lizard"
    )


# Functions with CCN >= this threshold are considered complex/hotspot functions
COMPLEXITY_THRESHOLD = 10


def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Merge overlapping or adjacent line ranges."""
    if not ranges:
        return []
    merged = []
    for start, end in sorted(ranges):
        if merged and start <= merged[-1][1] + 1:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    return merged


def compute_complexity(repo_path: str, files: list[str]) -> dict:
    """Run lizard on files and aggregate per-function complexity to file level.

    Returns dict mapping file_path to {max_complexity, avg_complexity, file_length}.
    Uses CCN (cyclomatic complexity number) as the primary metric.

    Lizard CSV columns (lizard >= 1.23.0):
    0:NLOC 1:CCN 2:token_count 3:parameter_count 4:function_length
    5:location 6:filename 7:function_name 8:signature 9:MCC 10:NPath
    """
    if not files:
        return {}

    lizard_cmd = _find_lizard()
    result = subprocess.run(
        [lizard_cmd, "--csv"] + files,
        capture_output=True, text=True, cwd=repo_path,
    )

    if not result.stdout.strip():
        return {}

    # Per-file accumulators: CCN values per file
    file_ccns = defaultdict(list)
    # Per-file: last line number (used as file_length)
    file_max_line = {}
    # Per-file: (ccn, start_line, end_line) for each function
    file_functions = defaultdict(list)

    repo_abs = os.path.abspath(str(repo_path))

    reader = csv.reader(io.StringIO(result.stdout))
    for row in reader:
        if len(row) < 11:
            continue

        # Column 1 = CCN (cyclomatic complexity)
        try:
            ccn = int(row[1])
        except (ValueError, IndexError):
            continue

        # Column 6 = filename (absolute path)
        filepath = row[6].strip()
        if not filepath:
            continue

        # Column 5 = location, format: "func_name@start-end@filepath"
        location = row[5].strip()
        if "@" in location:
            loc_parts = location.rsplit("@", 2)
            loc_file = loc_parts[2] if len(loc_parts) == 3 else loc_parts[-1]
            if os.path.abspath(loc_file) == os.path.abspath(filepath):
                func_info = location.rsplit("@", 2)[1]
                if "-" in func_info:
                    start_str, end_str = func_info.rsplit("-", 1)
                    try:
                        start_line = int(start_str.strip())
                        end_line = int(end_str.strip())
                        file_max_line[filepath] = max(
                            file_max_line.get(filepath, 0), end_line
                        )
                        # Collect (ccn, start, end) per function for hotspot line detection
                        file_functions[filepath].append((ccn, start_line, end_line))
                    except (ValueError, IndexError):
                        pass

        # Store CCN value
        file_ccns[filepath].append(ccn)

    # Aggregate to file level
    result_data = {}
    for filepath, ccns in file_ccns.items():
        # Resolve path relative to repo_path (since lizard was run with cwd=repo_path)
        if os.path.isabs(filepath):
            abs_path = os.path.abspath(filepath)
            if abs_path.startswith(repo_abs):
                rel_path = os.path.relpath(abs_path, repo_abs)
            else:
                rel_path = os.path.basename(filepath)
        else:
            # Lizard output relative paths — resolve from repo_path
            rel_path = os.path.relpath(
                os.path.join(repo_path, filepath), repo_abs
            )

        # Compute file_length from line count
        full_path = os.path.join(repo_abs, rel_path)
        try:
            with open(full_path, "r", errors="ignore") as f:
                file_length = sum(1 for _ in f)
        except (FileNotFoundError, PermissionError):
            file_length = 0

        # Collect line ranges from functions exceeding the complexity threshold
        hotspot_lines: list[tuple[int, int]] = [
            (start, end)
            for ccn, start, end in file_functions.get(filepath, [])
            if ccn >= COMPLEXITY_THRESHOLD
        ]
        # Remove overlaps by merging ranges
        hotspot_lines = _merge_ranges(hotspot_lines)

        result_data[rel_path] = {
            "max_complexity": max(ccns),
            "avg_complexity": sum(ccns) / len(ccns),
            "file_length": file_length,
            "hotspot_lines": hotspot_lines,
        }

    return result_data
