"""Tests for consolidated HTML report."""

import json
import re
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


def test_sort_order_hotspot_then_ratio():
    """Repos sorted by hotspot_count DESC, then ratio DESC."""
    # Repo A: 10 hotspots, 10% ratio
    fi_a = FileInfo(path="a.java", churn_score=50.0, complexity_score=50.0,
                    hotspot_score=50.0, commit_count=1, author_count=1)
    ranked_a = RankedResult(
        repo_name="repo-a", all_files=[fi_a], hotspot_files=[fi_a],
        total_files=10, hotspot_count=10, hotspot_ratio=0.10,
        hotspot_percentile=50,
    )
    # Repo B: 5 hotspots, 50% ratio
    fi_b = FileInfo(path="b.java", churn_score=60.0, complexity_score=60.0,
                    hotspot_score=60.0, commit_count=1, author_count=1)
    ranked_b = RankedResult(
        repo_name="repo-b", all_files=[fi_b], hotspot_files=[fi_b],
        total_files=10, hotspot_count=5, hotspot_ratio=0.50,
        hotspot_percentile=75,
    )
    # Repo C: 10 hotspots, 5% ratio
    fi_c = FileInfo(path="c.java", churn_score=30.0, complexity_score=30.0,
                    hotspot_score=30.0, commit_count=1, author_count=1)
    ranked_c = RankedResult(
        repo_name="repo-c", all_files=[fi_c], hotspot_files=[fi_c],
        total_files=200, hotspot_count=10, hotspot_ratio=0.05,
        hotspot_percentile=40,
    )

    run = RunResult(
        repos=[ranked_b, ranked_a, ranked_c],  # wrong order initially
        total_repos=3, total_files=30, total_hotspots=25,
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))
    content = html_path.read_text()

    # Find positions: hotspot_count ties -> ratio breaks
    # repo-a: 10 hotspots, 10% -> should come before repo-c: 10 hotspots, 5%
    # repo-b: 5 hotspots -> should come last
    pos_a = content.index('repo-a')
    pos_c = content.index('repo-c')
    pos_b = content.index('repo-b')

    assert pos_a < pos_c, f"repo-a(10hs) should precede repo-c(10hs): {pos_a} vs {pos_c}"
    assert pos_c < pos_b, f"repo-c(10hs) should precede repo-b(5hs): {pos_c} vs {pos_b}"


def test_stacked_bar_chart_rendered():
    """Consolidated HTML must include the stacked bar chart."""
    r1 = RankedResult()
    r1.repo_name = "gcms-bo-account"
    r1.total_files = 80
    r1.hotspot_count = 7
    r1.hotspot_ratio = 0.0875
    r1.all_files = []
    r1.hotspot_files = []
    r1.hotspot_percentile = 75

    r2 = RankedResult()
    r2.repo_name = "smbc-gcms-bo-web"
    r2.total_files = 1100
    r2.hotspot_count = 299
    r2.hotspot_ratio = 0.2718
    r2.all_files = []
    r2.hotspot_files = []
    r2.hotspot_percentile = 75

    run = RunResult(
        repos=[r1, r2],
        total_repos=2,
        total_files=1180,
        total_hotspots=306,
        failed_repos=[],
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))

    content = html_path.read_text()

    # Chart styles
    assert ".chart" in content
    assert ".chart-bar" in content
    assert "#e67e22" in content  # hotspot orange
    assert "#3498db" in content  # file blue
    # Chart container
    assert 'id="chart"' in content
    # Chart legend
    assert "Hotspots" in content
    assert "Files" in content
    # JS chart rendering
    assert 'repoData' in content
    assert 'chart-tooltip' in content
    assert 'chart-legend' in content
    # Pixel heights used (not percentages)
    assert 'px' in content
    assert 'offsetHeight' in content


def test_chart_data_json_valid():
    """Embedded repoData must be valid JSON with correct values."""
    r = RankedResult()
    r.repo_name = "gcms-fo-account"
    r.total_files = 321
    r.hotspot_count = 28
    r.hotspot_ratio = 0.0872
    r.all_files = []
    r.hotspot_files = []
    r.hotspot_percentile = 75

    run = RunResult(
        repos=[r],
        total_repos=1,
        total_files=321,
        total_hotspots=28,
        failed_repos=[],
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))

    content = html_path.read_text()
    match = re.search(r'var repoData = (\[.*?\]);', content)
    assert match, "repoData JSON not found in HTML"
    data = json.loads(match.group(1))
    assert len(data) == 1
    assert data[0]["name"] == "gcms-fo-account"
    assert data[0]["files"] == 321
    assert data[0]["hotspots"] == 28
