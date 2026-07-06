"""Tests for consolidated HTML report."""

import tempfile
from pathlib import Path

from models.data import FileInfo, RankedResult, RunResult
from report.consolidated import write_consolidated_html


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
    assert html_path.stat().st_size > 1000
    content = html_path.read_text()
    assert "Code Hotspot Analysis Report" in content
    assert "repo-a" in content
    assert "repo-b" in content
    assert "a.java" in content
    assert "b.js" in content
    assert "Total repos: 2" in content
    assert "Total files: 2" in content
    assert "Total hotspots: 2" in content


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


def test_consolidated_html_hotspot_highlighting():
    run = RunResult(
        repos=[
            _make_ranked("repo-a", "hot.java", 95.0, 95.0, 95.0),
            _make_ranked("repo-a", "safe.java", 5.0, 5.0, 5.0),
        ],
        total_repos=1, total_files=2, total_hotspots=2,
    )

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        html_path = Path(f.name)

    write_consolidated_html(run, str(html_path))

    content = html_path.read_text()
    # hot.java should be in a highlighted row
    assert 'class="hotspot"' in content
    assert "95.0" in content
