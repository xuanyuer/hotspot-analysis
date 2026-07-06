"""Code Hotspot Analysis Tool - CLI entry point."""

import argparse
import sys
from pathlib import Path

from git_analyzer.fetch_files import fetch_files
from git_analyzer.fetch_churn import compute_churn
from complexity_analyzer.lizard_wrapper import compute_complexity
from scorer.normalize import normalize_churn, normalize_complexity
from scorer.aggregate import compute_hotspot_score
from scorer.rank import rank_files
from models.data import FileInfo


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


def run_analysis(repo_path: Path, include: list[str], exclude: list[str],
                 since: str, output_dir: Path, percentile: float) -> None:
    """Run the full analysis pipeline for a single repo."""
    main_branch = detect_main_branch(repo_path)
    repo_name = repo_path.name

    # 1. Fetch files
    print(f"  Fetching files from {repo_path}...")
    files = fetch_files(repo_path, main_branch, include, exclude)
    print(f"  Found {len(files)} files")

    if not files:
        print(f"  No files to analyze. Skipping.")
        return

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
    write_csv(result, str(csv_path))
    print(f"  Written: {csv_path}")

    # Write Markdown
    md_path = repo_output / "ranked.md"
    write_markdown(result, str(md_path))
    print(f"  Written: {md_path}")

    # Summary
    print(f"\n  Summary:")
    print(f"    Total files: {result.total_files}")
    print(f"    Hotspot count: {result.hotspot_count} ({result.hotspot_ratio:.0%})")
    print(f"    Threshold: {result.hotspot_percentile}th percentile")
    if result.hotspot_files:
        print(f"\n  Top 5 hotspots:")
        for f in result.hotspot_files[:5]:
            print(f"    {f.path} (score: {f.hotspot_score:.1f})")


def write_csv(result, output_path: str) -> None:
    """Write ranked CSV (all files)."""
    with open(output_path, "w") as fh:
        fh.write("file_path,churn_score,complexity_score,hotspot_score,commit_count,lines_added,lines_removed,author_count\n")
        for fi in result.all_files:
            fh.write(f"{fi.path},{fi.churn_score:.2f},{fi.complexity_score:.2f},{fi.hotspot_score:.2f},{fi.commit_count},{fi.lines_added},{fi.lines_removed},{fi.author_count}\n")


def write_markdown(result, output_path: str) -> None:
    """Write ranked Markdown table."""
    with open(output_path, "w") as fh:
        fh.write("# Hotspot Analysis Report\n\n")
        fh.write(f"**Total files:** {result.total_files} | **Hotspots:** {result.hotspot_count} ({result.hotspot_ratio:.0%})\n\n")
        fh.write("| File | Churn | Complexity | Hotspot | Commits | Authors |\n")
        fh.write("|------|-------|------------|---------|---------|---------|\n")
        for fi in result.all_files:
            fh.write(f"| {fi.path} | {fi.churn_score:.1f} | {fi.complexity_score:.1f} | {fi.hotspot_score:.1f} | {fi.commit_count} | {fi.author_count} |\n")


def main():
    parser = argparse.ArgumentParser(description="Code Churn & Complexity Hotspot Analysis Tool")
    parser.add_argument("--repo", type=str, help="Path to git repository")
    parser.add_argument("--repo-list", type=str, help="Path to file with repo paths (one per line)")
    parser.add_argument("--include", nargs="+", help="Include glob patterns")
    parser.add_argument("--exclude", nargs="+", help="Exclude glob patterns")
    parser.add_argument("--since", type=str, default="full", help="Time window for churn analysis (e.g., 6months)")
    parser.add_argument("--output", type=str, default="./hotspot-output", help="Output directory")
    parser.add_argument("--hotspot-percentile", type=float, default=75, help="Percentile threshold for hotspots")

    args = parser.parse_args()

    if not args.repo and not args.repo_list:
        print("Error: specify --repo or --repo-list")
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    repos = []
    if args.repo:
        repos.append(Path(args.repo))
    if args.repo_list:
        with open(args.repo_list) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    repos.append(Path(line))

    for repo in repos:
        print(f"\nAnalyzing: {repo}")
        try:
            run_analysis(repo, args.include or [], args.exclude or [],
                        args.since, output_dir, args.hotspot_percentile)
        except Exception as e:
            print(f"  ERROR: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
