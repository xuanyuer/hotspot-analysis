from dataclasses import dataclass, field


@dataclass
class FileInfo:
    path: str
    language: str = ""
    commit_count: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    author_count: int = 0
    churn_score: float = 0.0
    complexity_score: float = 0.0
    hotspot_score: float = 0.0
    hotspot_lines: list[tuple[int, int]] = field(default_factory=list)  # (start, end) line ranges


@dataclass
class RankedResult:
    repo_name: str = ""
    all_files: list[FileInfo] = field(default_factory=list)
    hotspot_files: list[FileInfo] = field(default_factory=list)
    total_files: int = 0
    hotspot_count: int = 0
    hotspot_ratio: float = 0.0
    hotspot_percentile: float = 75.0
    threshold_score: float = 0.0


@dataclass
class RunResult:
    """Cross-repo aggregate result."""
    repos: list[RankedResult]
    total_repos: int = 0
    total_files: int = 0
    total_hotspots: int = 0
    failed_repos: list[str] = field(default_factory=list)
