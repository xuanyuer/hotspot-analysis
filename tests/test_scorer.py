import pytest
from hotspot.models.data import FileInfo, RankedResult
from hotspot.scorer.normalize import normalize_churn, normalize_complexity
from hotspot.scorer.aggregate import compute_hotspot_score
from hotspot.scorer.rank import rank_files


class TestNormalizeChurn:
    def test_basic_min_max(self):
        """Files at min and max churn get scores 0 and 100."""
        data = {
            "low.py": {"commit_count": 1, "lines_added": 10, "lines_removed": 5, "author_count": 1},
            "mid.py": {"commit_count": 5, "lines_added": 50, "lines_removed": 20, "author_count": 2},
            "high.py": {"commit_count": 10, "lines_added": 100, "lines_removed": 50, "author_count": 3},
        }
        result = normalize_churn(data)

        assert abs(result["low.py"] - 0.0) < 0.01
        assert abs(result["mid.py"] - 44.44) < 0.01
        assert abs(result["high.py"] - 100.0) < 0.01

    def test_single_file(self):
        """Single file gets score 0."""
        result = normalize_churn({
            "only.py": {"commit_count": 5, "lines_added": 50, "lines_removed": 20, "author_count": 1},
        })
        assert result["only.py"] == 0.0

    def test_outlier_capping(self):
        """Outlier values are capped, preserving relative ordering."""
        data = {
            "f1.py": {"commit_count": 1, "lines_added": 1, "lines_removed": 1, "author_count": 1},
            "f2.py": {"commit_count": 2, "lines_added": 2, "lines_removed": 2, "author_count": 1},
            "f3.py": {"commit_count": 3, "lines_added": 3, "lines_removed": 3, "author_count": 1},
            "f4.py": {"commit_count": 4, "lines_added": 4, "lines_removed": 4, "author_count": 1},
            "f5.py": {"commit_count": 100, "lines_added": 100, "lines_removed": 100, "author_count": 100},
        }
        result = normalize_churn(data)

        assert abs(result["f5.py"] - 100.0) < 0.01
        assert abs(result["f4.py"] - 50.0) < 0.01
        assert abs(result["f1.py"] - 0.0) < 0.01

    def test_all_same_values(self):
        """All same churn values → all get 0."""
        data = {
            "f1.py": {"commit_count": 5, "lines_added": 5, "lines_removed": 5, "author_count": 1},
            "f2.py": {"commit_count": 5, "lines_added": 5, "lines_removed": 5, "author_count": 1},
            "f3.py": {"commit_count": 5, "lines_added": 5, "lines_removed": 5, "author_count": 1},
        }
        result = normalize_churn(data)
        assert all(v == 0.0 for v in result.values())


class TestNormalizeComplexity:
    def test_basic_min_max(self):
        """Files at min and max complexity get scores 0 and 100."""
        data = {
            "low.js": {"max_complexity": 2, "avg_complexity": 2, "file_length": 50},
            "mid.js": {"max_complexity": 10, "avg_complexity": 8, "file_length": 200},
            "high.js": {"max_complexity": 20, "avg_complexity": 18, "file_length": 500},
        }
        result = normalize_complexity(data)

        assert abs(result["low.js"] - 0.0) < 0.01
        assert abs(result["high.js"] - 100.0) < 0.01

    def test_single_file(self):
        """Single file gets score 0."""
        result = normalize_complexity({
            "only.java": {"max_complexity": 15, "avg_complexity": 10, "file_length": 300},
        })
        assert result["only.java"] == 0.0


class TestRankFiles:
    def test_ranks_descending(self):
        """Files are ranked by hotspot_score descending."""
        files = [
            FileInfo(path="a.js", hotspot_score=20.0),
            FileInfo(path="b.js", hotspot_score=80.0),
            FileInfo(path="c.js", hotspot_score=50.0),
        ]
        result = rank_files(files, percentile=75)

        scores = [f.hotspot_score for f in result.hotspot_files]
        assert scores == sorted(scores, reverse=True)

    def test_hotspot_count_at_percentile(self):
        """Files above the 75th percentile are flagged as hotspots."""
        files = [
            FileInfo(path=f"f{i}.js", hotspot_score=i * 10)
            for i in range(1, 11)
        ]
        result = rank_files(files, percentile=75)

        # 75th percentile of [10..100] = 75, files >= 75: 80, 90, 100
        assert result.hotspot_count == 3
        assert abs(result.hotspot_ratio - 0.3) < 0.01

    def test_empty_files(self):
        """Empty input produces empty result."""
        result = rank_files([], percentile=75)
        assert len(result.hotspot_files) == 0
        assert result.hotspot_count == 0
        assert result.total_files == 0

    def test_low_percentile_all_hotspots(self):
        """Very low percentile flags nearly all files as hotspots."""
        files = [
            FileInfo(path=f"f{i}.js", hotspot_score=10.0 + i)
            for i in range(10)
        ]  # scores: 10, 11, ..., 19
        result = rank_files(files, percentile=10)

        # 10th percentile of [10..19] ~ 10.9, most files >= 10.9
        assert result.hotspot_count >= 8
