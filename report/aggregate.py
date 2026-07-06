"""Cross-repo aggregate report generation."""

from models.data import RankedResult, RunResult


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


def write_combined_csv(run: RunResult, output_path: str) -> None:
    """Write combined CSV with repo column across all repos, sorted by hotspot_score desc."""
    # Collect all files from all repos
    all_files = []
    for r in run.repos:
        for fi in r.all_files:
            all_files.append((r.repo_name, fi))

    # Sort by hotspot_score descending
    all_files.sort(key=lambda x: x[1].hotspot_score, reverse=True)

    with open(output_path, "w") as fh:
        fh.write("repo,file_path,churn_score,complexity_score,hotspot_score,commit_count,lines_added,lines_removed,author_count\n")
        for repo_name, fi in all_files:
            fh.write(f"{repo_name},{fi.path},{fi.churn_score:.2f},{fi.complexity_score:.2f},{fi.hotspot_score:.2f},{fi.commit_count},{fi.lines_added},{fi.lines_removed},{fi.author_count}\n")


def write_combined_markdown(run: RunResult, output_path: str) -> None:
    """Write combined Markdown report with summary + per-repo breakdown."""
    with open(output_path, "w") as fh:
        fh.write("# Cross-Repo Hotspot Summary\n\n")
        fh.write(f"**Total repos:** {run.total_repos} | **Total files:** {run.total_files} | **Hotspots:** {run.total_hotspots}\n\n")

        if run.failed_repos:
            fh.write(f"\n**Failed repos:** {', '.join(run.failed_repos)}\n\n")

        # Per-repo summary table
        fh.write("## Per-Repo Summary\n\n")
        fh.write("| Repo | Files | Hotspots | Ratio | Avg Hotspot Score |\n")
        fh.write("|------|-------|----------|-------|-------------------|\n")
        for r in run.repos:
            avg_score = sum(f.hotspot_score for f in r.all_files) / len(r.all_files) if r.all_files else 0
            fh.write(f"| {r.repo_name} | {r.total_files} | {r.hotspot_count} | {r.hotspot_ratio:.0%} | {avg_score:.1f} |\n")

        # Per-file ranked table
        fh.write("\n## All Files (Ranked by Hotspot Score)\n\n")
        fh.write("| Repo | File | Churn | Complexity | Hotspot | Commits |\n")
        fh.write("|------|------|-------|------------|---------|---------|\n")
        for r in run.repos:
            for fi in r.all_files:
                fh.write(f"| {r.repo_name} | {fi.path} | {fi.churn_score:.1f} | {fi.complexity_score:.1f} | {fi.hotspot_score:.1f} | {fi.commit_count} |\n")
