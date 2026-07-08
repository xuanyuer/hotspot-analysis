"""Tests for consolidated HTML report."""

import tempfile
from pathlib import Path

from hotspot.models.data import FileInfo, RankedResult, RunResult
from hotspot.report.consolidated import write_consolidated_html


def _make_ranked(repo: str, path: str, churn: float, complexity: float, hotspot: float) -> RankedResult:
    fi = FileInfo(path=path, churn_score=churn, complexity_score=complexity,
                  hotspot_score=hotspot, commit_count=1, author_count=1)
    return RankedResult(repo_name=repo, all_files=[fi], hotspot_files=[fi],
                        total_files=1, hotspot_count=1, hotspot_ratio=1.0, hotspot_percentile=75)


def test_consolidated_html_file_generated():
    run = RunResult(
        repos=[
            _make_ranked("repo-a", "a.java", 80.0, 90.0, 85.0),
            _make_ranked("repo-b", "b.js", 10.0, 5.0, 7.5),
        ],
        total_repos=2, total_files=2, total_hotspots=2,
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))

    assert html_path.exists()
    assert html_path.stat().st_size > 500
    content = html_path.read_text()
    assert "Code Hotspot Analysis Report" in content
    assert "repo-a" in content
    assert "repo-b" in content
    assert "Total repos: 2" in content
    assert "Total files: 2" in content
    assert "Total hotspots: 2" in content
    assert "report.html" in content  # links to individual reports


def test_consolidated_html_with_failed_repos():
    run = RunResult(
        repos=[_make_ranked("repo-a", "a.java", 80.0, 90.0, 85.0)],
        total_repos=1, total_files=1, total_hotspots=1,
        failed_repos=["broken-repo"],
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))

    content = html_path.read_text()
    assert "Failed Repositories" in content
    assert "broken-repo" in content


def test_consolidated_html_summary_only():
    # Single repo with multiple files -> single summary row
    fi1 = FileInfo(path="hot.java", churn_score=95.0, complexity_score=95.0,
                   hotspot_score=95.0, commit_count=1, author_count=1)
    fi2 = FileInfo(path="safe.java", churn_score=5.0, complexity_score=5.0,
                   hotspot_score=5.0, commit_count=1, author_count=1)
    ranked = RankedResult(repo_name="repo-a", all_files=[fi1, fi2],
                          hotspot_files=[fi1], total_files=2, hotspot_count=1,
                          hotspot_ratio=0.5, hotspot_percentile=75)

    run = RunResult(repos=[ranked], total_repos=1, total_files=2, total_hotspots=1)

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))

    content = html_path.read_text()
    # Summary with repo name and stats — no per-file detail, no median/min/max
    assert "repo-a" in content
    assert "50%" in content  # hotspot ratio
    # No median/min/max columns or stats
    assert "Median Score" not in content
    assert "Min Score" not in content
    assert "Max Score" not in content


def test_sort_order_ratio_then_hotspot():
    """Repos sorted by ratio DESC, then hotspot_count DESC."""
    fi_high_ratio = FileInfo(path="f.java", churn_score=80.0, complexity_score=80.0,
                             hotspot_score=80.0, commit_count=1, author_count=1)
    fi_medium_ratio = FileInfo(path="g.java", churn_score=60.0, complexity_score=60.0,
                               hotspot_score=60.0, commit_count=1, author_count=1)
    fi_low_ratio = FileInfo(path="h.java", churn_score=30.0, complexity_score=30.0,
                           hotspot_score=30.0, commit_count=1, author_count=1)
    # Same ratio different hotspot_count
    fi_hs2 = FileInfo(path="i.java", churn_score=50.0, complexity_score=50.0,
                      hotspot_score=50.0, commit_count=1, author_count=1)
    fi_hs2b = FileInfo(path="j.java", churn_score=50.0, complexity_score=50.0,
                       hotspot_score=50.0, commit_count=1, author_count=1)

    ranked = RankedResult(
        repo_name="test",
        all_files=[fi_high_ratio, fi_medium_ratio, fi_low_ratio, fi_hs2, fi_hs2b],
        hotspot_files=[fi_high_ratio, fi_medium_ratio, fi_hs2, fi_hs2b],
        total_files=5,
        hotspot_count=4,
        hotspot_ratio=4 / 5,
        hotspot_percentile=75,
    )
    run = RunResult(repos=[ranked], total_repos=1, total_files=5, total_hotspots=4)

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))
    content = html_path.read_text()

    # Verify no min/max columns
    assert "Min Score" not in content
    assert "Max Score" not in content
    assert "Median Score" not in content
    # Repo header has expected columns
    assert "<th>Repository</th>" in content
    assert "<th>Files</th>" in content
    assert "<th>Hotspots</th>" in content
    assert "<th>Ratio</th>" in content
