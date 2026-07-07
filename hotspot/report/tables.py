"""CSV and Markdown report generation."""


def write_csv_report(result, output_path: str) -> None:
    """Write ranked CSV (all files, sorted by hotspot_score desc)."""
    with open(output_path, "w") as fh:
        fh.write("file_path,churn_score,complexity_score,hotspot_score,commit_count,lines_added,lines_removed,author_count,hotspot_lines\n")
        for fi in result.all_files:
            lines_str = ";".join(f"{s}-{e}" for s, e in fi.hotspot_lines) if fi.hotspot_lines else ""
            fh.write(f"{fi.path},{fi.churn_score:.2f},{fi.complexity_score:.2f},{fi.hotspot_score:.2f},{fi.commit_count},{fi.lines_added},{fi.lines_removed},{fi.author_count},{lines_str}\n")


def write_markdown_report(result, output_path: str) -> None:
    """Write ranked Markdown table."""
    with open(output_path, "w") as fh:
        fh.write("# Hotspot Analysis Report\n\n")
        fh.write(f"**Total files:** {result.total_files} | **Hotspots:** {result.hotspot_count} ({result.hotspot_ratio:.0%})\n\n")
        fh.write("| File | Churn | Complexity | Hotspot | Commits | Authors | Lines |\n")
        fh.write("|------|-------|------------|---------|---------|---------|-------|\n")
        for fi in result.all_files:
            lines_str = ", ".join(f"{s}-{e}" for s, e in fi.hotspot_lines)
            fh.write(f"| {fi.path} | {fi.churn_score:.1f} | {fi.complexity_score:.1f} | {fi.hotspot_score:.1f} | {fi.commit_count} | {fi.author_count} | {lines_str} |\n")
