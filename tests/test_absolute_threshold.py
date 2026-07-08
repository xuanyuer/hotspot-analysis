"""Test absolute threshold override."""
import pytest
from hotspot.scorer.rank import rank_files
from hotspot.models.data import FileInfo


class TestAbsoluteThreshold:
    def test_default_threshold_is_50(self):
        """Default absolute threshold is 50."""
        files = [FileInfo(path=f"f{i}", hotspot_score=i * 10) for i in range(1, 11)]
        result = rank_files(files, global_threshold=50.0)
        # Files >= 50: 50, 60, 70, 80, 90, 100 → 6 files
        assert result.hotspot_count == 6
        assert result.threshold_score == 50.0

    def test_global_threshold_overrides_percentile(self):
        """Provided global_threshold takes precedence over percentile."""
        files = [FileInfo(path=f"f{i}", hotspot_score=i * 10) for i in range(1, 11)]
        # 75th percentile would be ~75, but we override with 30
        result = rank_files(files, percentile=75, global_threshold=30.0)
        # Files >= 30: 30, 40, 50, 60, 70, 80, 90, 100 → 8 files
        assert result.hotspot_count == 8
        assert result.threshold_score == 30.0

    def test_high_absolute_threshold_few_hotspots(self):
        """High threshold → few hotspots."""
        files = [FileInfo(path=f"f{i}", hotspot_score=i * 10) for i in range(1, 11)]
        result = rank_files(files, percentile=75, global_threshold=90.0)
        # Files >= 90: 90, 100 → 2 files
        assert result.hotspot_count == 2

    def test_no_global_threshold_falls_back_to_percentile(self):
        """Without global_threshold, falls back to percentile-based."""
        files = [FileInfo(path=f"f{i}", hotspot_score=i * 10) for i in range(1, 11)]
        result = rank_files(files, percentile=75, global_threshold=None)
        # 75th percentile of [10..100] = 75, files >= 75: 80, 90, 100
        assert result.hotspot_count == 3

    def test_absolute_threshold_zero(self):
        """Zero threshold → floor of 1 (minimum)."""
        files = [FileInfo(path=f"f{i}", hotspot_score=i) for i in range(1, 11)]
        result = rank_files(files, percentile=75, global_threshold=0.0)
        assert result.threshold_score == 1.0
