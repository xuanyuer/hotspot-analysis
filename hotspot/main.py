"""Code Hotspot Analysis Tool - CLI entry point."""

import argparse
import sys
from pathlib import Path

from hotspot.git_analyzer.fetch_files import fetch_files
from hotspot.git_analyzer.fetch_churn import compute_churn
from hotspot.complexity_analyzer.lizard_wrapper import compute_complexity
from hotspot.scorer.normalize import normalize_churn, normalize_complexity
from hotspot.scorer.aggregate import compute_hotspot_score
from hotspot.scorer.rank import rank_files
from hotspot.models.data import FileInfo
from hotspot.report.tables import write_csv_report, write_markdown_report
from hotspot.report.png_report import write_png_scatter
from hotspot.report.html_report import write_html_report
from hotspot.report.aggregate import build_run_result
from hotspot.report.consolidated import write_consolidated_html
from hotspot.config import EXCLUDE_DEFAULTS, DEFAULT_HOTSPOT_PERCENTILE
from hotspot.git_analyzer.repo_list import parse_config


def detect_main_branch(repo_path: Path) -> str:
    """Detect the main branch: prefer 'develop', fallback to 'main'."""
    result = __import__("subprocess").run(
        ["git", "-C", str(repo_path), "branch", "--list"],
        capture_output=True, text=True, check=True,
    )
    branches = [b.strip().lstrip("* ").rstrip() for b in result.stdout.strip().split("\n")]
    if "develop" in branches:
        return "develop"
    if "main" in branches:
        return "main"
    return "main"  # final fallback


def detect_language(repo_path: Path) -> str:
    """Detect primary language from file extensions in the repo."""
    import subprocess
    result = subprocess.run(
        ["git", "-C", str(repo_path), "ls-files"],
        capture_output=True, text=True, check=True,
    )
    extensions = {}
    for f in result.stdout.strip().split("\n"):
        if f:
            ext = f.rsplit(".", 1)[-1] if "." in f else ""
            extensions[ext] = extensions.get(ext, 0) + 1
    if extensions.get("java", 0) > 0 or extensions.get("class", 0) > 0:
        return "java"
    if extensions.get("py", 0) > 0:
        return "python"
    if extensions.get("js", 0) > 0 or extensions.get("ts", 0) > 0:
        return "js"
    return "default"


def run_analysis(repo_path: Path, include: list[str], exclude: list[str],
                 since: str, output_dir: Path, percentile: float) -> RankedResult:
    """Run the full analysis pipeline for a single repo. Returns RankedResult."""
    main_branch = detect_main_branch(repo_path)
    repo_name = repo_path.name
    lang = detect_language(repo_path)

    # Merge default excludes with user excludes
    lang_excludes = EXCLUDE_DEFAULTS.get(lang, EXCLUDE_DEFAULTS["default"])
    default_excludes = EXCLUDE_DEFAULTS.get("default", [])
    all_excludes = list(set(lang_excludes + default_excludes + exclude))

    # 1. Fetch files
    print(f"  Fetching files from {repo_path}... (lang={lang})")
    files = fetch_files(repo_path, main_branch, include, all_excludes)
    print(f"  Found {len(files)} files")

    if not files:
        print(f"  No files to analyze. Skipping.")
        return RankedResult(repo_name=repo_name)

    # 2. Compute churn
    print(f"  Computing churn from git history...")
    churn_data = compute_churn(str(repo_path), main_branch, files)

    # 3. Compute complexity
    print(f"  Computing complexity via lizard...")
    complexity_data = compute_complexity(str(repo_path), files)

    # 4. Normalize
    print(f"  Normalizing scores...")
    churn_scores = normalize_churn(churn_data)
    complexity_scores = normalize_complexity(complexity_data)

    # 5. Build FileInfo objects
    files_info = []
    for filepath in files:
        churn_score = churn_scores.get(filepath, 0.0)
        complexity_score = complexity_scores.get(filepath, 0.0)
        c = churn_data.get(filepath, {})
        co = complexity_data.get(filepath, {})

        fi = FileInfo(
            path=filepath,
            commit_count=c.get("commit_count", 0),
            lines_added=c.get("lines_added", 0),
            lines_removed=c.get("lines_removed", 0),
            author_count=c.get("author_count", 0),
            churn_score=churn_score,
            complexity_score=complexity_score,
        )
        files_info.append(fi)

    # 6. Compute hotspot scores
    print(f"  Computing hotspot scores...")
    files_info = compute_hotspot_score(files_info)

    # 7. Rank
    print(f"  Ranking files...")
    result = rank_files(files_info, percentile=percentile)

    # 8. Output
    repo_output = output_dir / repo_name
    repo_output.mkdir(parents=True, exist_ok=True)

    # Write CSV
    csv_path = repo_output / "ranked.csv"
    write_csv_report(result, str(csv_path))
    print(f"  Written: {csv_path}")

    # Write Markdown
    md_path = repo_output / "ranked.md"
    write_markdown_report(result, str(md_path))
    print(f"  Written: {md_path}")

    # Write PNG scatter plot
    png_path = repo_output / "scatter.png"
    write_png_scatter(result, str(png_path))
    print(f"  Written: {png_path}")

    # Write HTML interactive report
    html_path = repo_output / "report.html"
    write_html_report(result, str(html_path))
    print(f"  Written: {html_path}")

    # Set repo name
    result.repo_name = repo_name

    # Summary
    print(f"\n  Summary:")
    print(f"    Total files: {result.total_files}")
    print(f"    Hotspot count: {result.hotspot_count} ({result.hotspot_ratio:.0%})")
    print(f"    Threshold: {result.hotspot_percentile}th percentile")
    if result.hotspot_files:
        print(f"\n  Top 5 hotspots:")
        for f in result.hotspot_files[:5]:
            print(f"    {f.path} (score: {f.hotspot_score:.1f})")

    return result





def main():
    parser = argparse.ArgumentParser(description="Code Churn & Complexity Hotspot Analysis Tool")
    parser.add_argument("--repo-list", type=str, default=None,
                       help="Path to repos.yaml (defaults to ./repos.yaml in current directory)")
    parser.add_argument("--since", type=str, default="full", help="Time window for churn analysis (e.g., 6months)")
    parser.add_argument("--output", type=str, default="./hotspot-report", help="Output directory")
    parser.add_argument("--hotspot-percentile", type=float, default=75, help="Percentile threshold for hotspots")

    args = parser.parse_args()

    # Auto-discover repos.yaml or use --repo-list flag
    config_path = args.repo_list
    if config_path is None:
        config_path = str(Path.cwd() / "repos.yaml")

    try:
        entries = parse_config(config_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(2)

    if not entries:
        print("Error: no repos defined in config file")
        sys.exit(2)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build list of (repo_path, include, exclude) tuples
    repo_tasks = [(entry.path, entry.include_patterns, entry.exclude_patterns) for entry in entries]

    results = []
    failed_repos = []
    fatal_error = False

    for repo_path, include, exclude in repo_tasks:
        print(f"\nAnalyzing: {repo_path}")
        try:
            ranked = run_analysis(repo_path, include, exclude,
                                  args.since, output_dir, args.hotspot_percentile)
            if ranked:
                results.append(ranked)
        except SystemExit:
            raise
        except Exception as e:
            print(f"  ERROR: {e}")
            failed_repos.append(str(repo_path))

    # Write consolidated index (when multiple repos)
    if len(repo_tasks) > 1:
        run = build_run_result(results, failed_repos)

        index_html = output_dir / "index.html"
        write_consolidated_html(run, str(index_html))
        print(f"\n  Written index: {index_html}")

        print(f"\n  Run summary: {run.total_repos} repos, {run.total_files} files, {run.total_hotspots} hotspots")
        if failed_repos:
            print(f"  Failed repos: {', '.join(failed_repos)}")

    # Exit code: 0 = all success, 1 = some failures, 2 = fatal error
    if fatal_error:
        sys.exit(2)
    elif failed_repos:
        sys.exit(1)


if __name__ == "__main__":
    main()
