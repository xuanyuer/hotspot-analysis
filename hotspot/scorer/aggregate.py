from hotspot.models.data import FileInfo


def compute_hotspot_score(files: list[FileInfo]) -> list[FileInfo]:
    """Compute geometric mean hotspot score for each file."""
    for f in files:
        f.hotspot_score = (f.churn_score * f.complexity_score) ** 0.5
    return files
