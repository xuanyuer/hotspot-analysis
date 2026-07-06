import subprocess
from collections import defaultdict


def compute_churn(repo_path: str, main_branch: str, files: list[str]) -> dict:
    """Parse git log --numstat for per-file churn statistics.

    Runs a single `git log --all --numstat` pass and accumulates per-file stats.
    Only tracks files in the `files` filter list.
    """
    if not files:
        return {}

    file_set = set(files)

    result = subprocess.run(
        ["git", "-C", str(repo_path), "log", "--all",
         "--numstat", "--pretty=format:COMMIT_START%n%h%n%an%n%ae%n%ad%n"],
        capture_output=True, text=True, check=True,
    )

    # Per-file accumulators
    stats = {f: {"commit_count": 0, "lines_added": 0, "lines_removed": 0,
                 "authors": set()} for f in file_set}

    lines = result.stdout.strip().split("\n")
    i = 0
    # Track seen file+commit pairs to avoid double-counting multi-file commits
    seen = set()

    while i < len(lines):
        if lines[i] == "COMMIT_START":
            i += 1
            commit_hash = lines[i].strip()
            author_name = lines[i + 1].strip()
            i += 4  # Skip: hash, author_name, author_email, date
            # Parse numstat lines until next COMMIT_START or EOF
            while i < len(lines):
                if lines[i] == "COMMIT_START":
                    break
                line = lines[i].strip()
                if line:
                    parts = line.split("\t")
                    if len(parts) == 3:
                        added, removed, filepath = parts
                        if filepath in file_set:
                            pair = (filepath, commit_hash)
                            if pair not in seen:
                                seen.add(pair)
                                stats[filepath]["commit_count"] += 1
                                stats[filepath]["lines_added"] += int(added) if added != "-" else 0
                                stats[filepath]["lines_removed"] += int(removed) if removed != "-" else 0
                                stats[filepath]["authors"].add(author_name)
                i += 1
        else:
            i += 1

    # Convert author sets to counts
    for f in stats:
        stats[f]["author_count"] = len(stats[f]["authors"])
        del stats[f]["authors"]

    return stats
