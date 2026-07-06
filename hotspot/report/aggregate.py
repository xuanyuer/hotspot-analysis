"""Cross-repo aggregate report generation."""

from hotspot.models.data import RankedResult, RunResult


def build_run_result(repos: list[RankedResult], failed_repos: list[str] | None = None) -> RunResult:
    """Build cross-repo aggregate from per-repo results."""
    all_files = []
    total_hotspots = 0
    total_files = 0

    for r in repos:
        all_files.extend(r.all_files)
        total_hotspots += r.hotspot_count
        total_files += r.total_files

    return RunResult(
        repos=repos,
        total_repos=len(repos),
        total_files=total_files,
        total_hotspots=total_hotspots,
        failed_repos=failed_repos or [],
    )


