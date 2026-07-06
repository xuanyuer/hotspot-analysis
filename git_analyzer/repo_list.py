"""Parse repo-list file with per-repo include/exclude patterns."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RepoEntry:
    """A single repo entry with optional per-repo filters."""
    path: Path
    include_patterns: list[str]
    exclude_patterns: list[str]


def parse_repo_list(repo_list_path: str, global_include: list[str], global_exclude: list[str]) -> list[RepoEntry]:
    """Parse a repo list file.

    Format: one repo path per line, optional inline patterns:
        # comment
        /path/to/repo
        /path/to/repo include:*.java exclude:build/*
        /path/to/repo include:*.js include:*.ts exclude:test/*

    Per-repo patterns override global --include/--exclude.
    If per-repo has include/exclude lists, they replace (not merge with) global.
    """
    entries = []
    with open(repo_list_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Parse inline patterns
            parts = line.split()
            repo_path = Path(parts[0])
            include = []
            exclude = []

            i = 1
            while i < len(parts):
                token = parts[i]
                if token.startswith("include:"):
                    include.append(token[len("include:"):])
                elif token.startswith("exclude:"):
                    exclude.append(token[len("exclude:"):])
                else:
                    # Unknown token — ignore silently
                    pass
                i += 1

            # Determine final include/exclude:
            # - If per-repo has any patterns, use them exclusively (override global)
            # - If per-repo has no patterns, fall back to global
            if include or exclude:
                final_include = include if include else global_include
                final_exclude = exclude if exclude else global_exclude
            else:
                final_include = global_include
                final_exclude = global_exclude

            entries.append(RepoEntry(
                path=repo_path,
                include_patterns=final_include,
                exclude_patterns=final_exclude,
            ))

    return entries
