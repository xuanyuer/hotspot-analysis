import subprocess
import fnmatch
from pathlib import Path


def fetch_files(repo_path: Path, main_branch: str, includes: list[str], excludes: list[str]) -> list[str]:
    """Get tracked git files, filtered by include/exclude glob patterns.

    Uses `git ls-files` for the file list. The main_branch parameter is
    accepted for API consistency with the main pipeline (branch selection
    is handled by the calling code).
    """
    result = subprocess.run(
        ["git", "-C", str(repo_path), "ls-files"],
        capture_output=True, text=True, check=True,
    )

    all_files = [f for f in result.stdout.strip().split("\n") if f.strip()]

    # Apply include filter
    if includes:
        filtered = []
        for f in all_files:
            if any(fnmatch.fnmatch(f, pattern) for pattern in includes):
                filtered.append(f)
        all_files = filtered

    # Apply exclude filter
    if excludes:
        all_files = [
            f for f in all_files
            if not any(fnmatch.fnmatch(f, pattern) for pattern in excludes)
        ]

    return all_files
