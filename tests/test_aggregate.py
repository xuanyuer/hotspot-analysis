"""Tests for cross-repo aggregate report generation."""

import csv
import tempfile
from pathlib import Path

from models.data import FileInfo, RankedResult
from report.aggregate import write_combined_csv, write_combined_markdown, build_run_result


def _make_ranked(repo: str, path: str, churn: float, complexity: float, hotspot: float,
                 commits: int = 0, authors: int = 0) -> RankedResult:
    fi = FileInfo(path=path, churn_score=churn, complexity_score=complexity,
                  hotspot_score=hotspot, commit_count=commits, author_count=authors)
    return RankedResult(repo_name=repo, all_files=[fi], hotspot_files=[fi],
                        total_files=1, hotspot_count=1, hotspot_ratio=1.0, hotspot_percentile=75)


class TestBuildRunResult:
    def test_aggregates_multiple_repos(self):
        repos = [
            _make_ranked("repo-a", "a.java", 80.0, 90.0, 85.0),
            _make_ranked("repo-b", "b.java", 10.0, 5.0, 7.5, commits=2),
        ]
        run = build_run_result(repos)

        assert run.total_repos == 2
        assert run.total_files == 2
        assert run.total_hotspots == 2
        assert len(run.repos) == 2

    def test_tracks_failed_repos(self):
        repos = [
            _make_ranked("repo-a", "a.java", 80.0, 90.0, 85.0),
        ]
        run = build_run_result(repos, failed_repos=["repo-b", "repo-c"])

        assert run.failed_repos == ["repo-b", "repo-c"]
        assert run.total_repos == 1


class TestWriteCombinedCsv:
    def test_includes_repo_column(self):
        run = build_run_result([
            _make_ranked("repo-a", "a.java", 80.0, 90.0, 85.0),
            _make_ranked("repo-b", "b.java", 10.0, 5.0, 7.5),
        ])

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = Path(f.name)

        write_combined_csv(run, str(csv_path))

        with open(csv_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        headers = list(rows[0].keys())
        assert "repo" in headers
        assert rows[0]["repo"] == "repo-a"
        assert rows[1]["repo"] == "repo-b"

    def test_sorted_by_hotspot_descending(self):
        run = build_run_result([
            _make_ranked("repo-b", "b.java", 10.0, 5.0, 7.5),
            _make_ranked("repo-a", "a.java", 90.0, 95.0, 92.0),
        ])

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as f:
            csv_path = Path(f.name)

        write_combined_csv(run, str(csv_path))

        with open(csv_path) as f:
            rows = list(csv.DictReader(f))

        assert float(rows[0]["hotspot_score"]) > float(rows[1]["hotspot_score"])


class TestWriteCombinedMarkdown:
    def test_includes_summary_and_ranked_table(self):
        run = build_run_result([
            _make_ranked("repo-a", "a.java", 80.0, 90.0, 85.0),
            _make_ranked("repo-b", "b.java", 10.0, 5.0, 7.5),
        ])

        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            md_path = Path(f.name)

        write_combined_markdown(run, str(md_path))

        content = md_path.read_text()

        assert "# Cross-Repo Hotspot Summary" in content
        assert "**Total repos:** 2" in content
        assert "**Total files:** 2" in content
        assert "repo-a" in content
        assert "repo-b" in content
        assert "a.java" in content
        assert "b.java" in content
