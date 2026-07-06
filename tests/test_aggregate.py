"""Tests for cross-repo aggregate report generation."""

from hotspot.models.data import FileInfo, RankedResult
from hotspot.report.aggregate import build_run_result


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
