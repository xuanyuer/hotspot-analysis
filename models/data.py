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


@dataclass
class RankedResult:
    all_files: list[FileInfo]
    hotspot_files: list[FileInfo]
    total_files: int
    hotspot_count: int
    hotspot_ratio: float
    hotspot_percentile: float
