"""Global normalization: files with same raw metric get same score across repos."""
import pytest
from hotspot.scorer.normalize import normalize_churn, normalize_complexity
from hotspot.scorer.rank import rank_files, compute_global_threshold
from hotspot.models.data import FileInfo


class TestComputeGlobalThreshold:
    def test_75th_percentile_of_global_scores(self):
        """Global threshold at 75th percentile of all hotspot scores."""
        scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]  # 10 files
        threshold = compute_global_threshold(scores, 75.0)
        # 75th percentile of [10..100] ≈ 75
        assert abs(threshold - 75.0) < 5.0

    def test_low_percentile_low_threshold(self):
        """Lower percentile → lower threshold."""
        scores = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        low = compute_global_threshold(scores, 50.0)
        high = compute_global_threshold(scores, 90.0)
        assert low < high

    def test_empty_scores(self):
        """Empty scores returns 0."""
        assert compute_global_threshold([], 75.0) == 0.0


class TestGlobalNormalization:
    def test_same_commit_count_same_score(self):
        """Files with identical commit_count get identical churn_score when normalized together."""
        data = {
            "repo-a/extract_gcms.py": {"commit_count": 3, "lines_added": 254, "lines_removed": 2, "author_count": 1},
            "repo-b/file1.java": {"commit_count": 3, "lines_added": 100, "lines_removed": 50, "author_count": 1},
            "repo-b/file2.java": {"commit_count": 10, "lines_added": 500, "lines_removed": 100, "author_count": 2},
        }
        result = normalize_churn(data)
        assert result["repo-a/extract_gcms.py"] == pytest.approx(result["repo-b/file1.java"])

    def test_same_complexity_same_score(self):
        """Files with identical max_complexity get identical complexity_score when normalized together."""
        data = {
            "repo-a/file1.py": {"max_complexity": 12, "avg_complexity": 5, "file_length": 200},
            "repo-b/file2.java": {"max_complexity": 12, "avg_complexity": 8, "file_length": 300},
            "repo-b/file3.java": {"max_complexity": 25, "avg_complexity": 20, "file_length": 800},
        }
        result = normalize_complexity(data)
        assert result["repo-a/file1.py"] == pytest.approx(result["repo-b/file2.java"])

    def test_outlier_repo_file_ranks_correctly_globally(self):
        """A file with 3 commits in a small repo should not score 100 when normalized globally."""
        data = {
            "small-repo/only.py": {"commit_count": 3, "lines_added": 254, "lines_removed": 2, "author_count": 1},
            "big-repo/file1.java": {"commit_count": 166, "lines_added": 5000, "lines_removed": 2000, "author_count": 15},
            "big-repo/file2.java": {"commit_count": 80, "lines_added": 2000, "lines_removed": 800, "author_count": 8},
            "big-repo/file3.java": {"commit_count": 50, "lines_added": 1000, "lines_removed": 400, "author_count": 5},
        }
        result = normalize_churn(data)
        # 3 commits is the minimum → should be 0 or very close
        assert result["small-repo/only.py"] < 10.0
        # 166 commits is the maximum → should be 100
        assert result["big-repo/file1.java"] == pytest.approx(100.0)
