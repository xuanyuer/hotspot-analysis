from hotspot.models.data import FileInfo, RankedResult
import statistics


def compute_global_threshold(scores: list[float], percentile: float = 75) -> float:
    """Compute percentile threshold from global score distribution."""
    if not scores:
        return 0.0
    return max(1, statistics.quantiles(scores, n=100, method='inclusive')[int(percentile) - 1])


def rank_files(files: list[FileInfo], percentile: float = 75, global_threshold: float = None) -> RankedResult:
    """Rank files by hotspot_score descending, flag files above threshold.
    
    If global_threshold is provided, use it. Otherwise compute from per-repo percentile.
    """
    if not files:
        return RankedResult(
            all_files=[], hotspot_files=[], total_files=0, hotspot_count=0,
            hotspot_ratio=0.0, hotspot_percentile=percentile,
            threshold_score=0.0,
        )

    sorted_files = sorted(files, key=lambda f: f.hotspot_score, reverse=True)

    scores = [f.hotspot_score for f in sorted_files]
    if global_threshold is not None:
        threshold = max(1.0, global_threshold)
    else:
        threshold = max(1, statistics.quantiles(scores, n=100, method='inclusive')[int(percentile) - 1])

    hotspot_files = [f for f in sorted_files if f.hotspot_score >= threshold]

    return RankedResult(
        all_files=sorted_files,
        hotspot_files=hotspot_files,
        total_files=len(files),
        hotspot_count=len(hotspot_files),
        hotspot_ratio=len(hotspot_files) / len(files),
        hotspot_percentile=percentile,
        threshold_score=round(threshold, 1),
    )
