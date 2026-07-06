"""Parse repos.yaml config file with global defaults and per-repo overrides."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class RepoEntry:
    """A single repo entry with include/exclude patterns."""
    path: Path
    include_patterns: list[str]
    exclude_patterns: list[str]


def parse_config(config_path: str | None = None) -> list[RepoEntry]:
    """Parse repos.yaml config file.

    If config_path is None, auto-discovers repos.yaml in the current working directory.

    Returns RepoEntry list with per-repo overrides applied.
    """
    if config_path is None:
        config_path = str(Path.cwd() / "repos.yaml")

    with open(config_path) as f:
        data = yaml.safe_load(f)

    if data is None:
        data = {}

    global_include = data.get("global", {}).get("include", [])
    global_exclude = data.get("global", {}).get("exclude", [])

    repos = data.get("repos", {}) or {}

    entries = []
    for repo_path, overrides in repos.items():
        path = Path(repo_path)
        if not path.exists():
            raise FileNotFoundError(f"Repo path does not exist: {repo_path}")

        include = overrides.get("include", global_include) if overrides else global_include
        exclude = overrides.get("exclude", global_exclude) if overrides else global_exclude

        entries.append(RepoEntry(
            path=path,
            include_patterns=include or [],
            exclude_patterns=exclude or [],
        ))

    return entries
