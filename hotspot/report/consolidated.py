"""Consolidated HTML report — simple summary with links to individual reports."""

import html as html_mod
import statistics
from datetime import datetime


def write_consolidated_html(run, output_path: str) -> None:
    """Generate a simple consolidated HTML report for management review.

    Shows a high-level summary table of all repos with links to their
    individual HTML reports. No per-file detail — just the summary.
    """
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Repo summary rows — sorted by ratio > hotspot > median, all descending
    repo_scores = []
    all_min = None
    all_max = None
    for r in run.repos:
        scores = [f.hotspot_score for f in r.all_files]
        median_score = statistics.median(scores) if scores else 0
        min_score = min(scores) if scores else 0
        max_score = max(scores) if scores else 0
        if all_min is None:
            all_min = min_score
            all_max = max_score
        else:
            all_min = min(all_min, min_score)
            all_max = max(all_max, max_score)
        repo_scores.append((median_score, r, min_score, max_score))
    repo_scores.sort(key=lambda x: (x[1].hotspot_ratio, x[1].hotspot_count, x[0]), reverse=True)

    min_str = f"{all_min:.1f}" if all_min is not None else "N/A"
    max_str = f"{all_max:.1f}" if all_max is not None else "N/A"

    repo_rows = ""
    for median_score, r, min_score, max_score in repo_scores:
        link = f"{r.repo_name}/report.html"
        repo_rows += f"""<tr>
            <td><a href="{html_mod.escape(link)}">{html_mod.escape(r.repo_name)}</a></td>
            <td>{r.total_files}</td>
            <td>{r.hotspot_count}</td>
            <td>{r.hotspot_ratio:.0%}</td>
            <td class="num-cell">{median_score:.1f}</td>
            <td class="num-cell">{min_score:.1f}</td>
            <td class="num-cell">{max_score:.1f}</td>
        </tr>"""

    # Failed repos
    failed_section = ""
    if run.failed_repos:
        failed_section = f"""
        <div class="failed">
            <h3>Failed Repositories</h3>
            <ul>{"".join(f"<li>{html_mod.escape(r)}</li>" for r in run.failed_repos)}</ul>
        </div>"""

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Code Hotspot Analysis Report</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 16px; background: #f5f5f5; color: #333; line-height: 1.6; }}
    .container {{ max-width: 1000px; margin: 0 auto; }}
    h1 {{ font-size: 1.4em; margin-bottom: 4px; color: #1a1a1a; }}
    .meta {{ font-size: 0.9em; color: #666; margin-bottom: 20px; }}
    .stats {{ background: #e8f4f8; padding: 14px 18px; border-radius: 6px; display: flex; gap: 20px; margin-bottom: 20px; flex-wrap: wrap; }}
    .stats span {{ font-weight: 500; }}
    .table-wrapper {{ overflow-x: auto; -webkit-overflow-scrolling: touch; margin-bottom: 16px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); min-width: 500px; }}
    th {{ background: #4a90d9; color: white; text-align: left; padding: 10px 14px; font-weight: 600; position: sticky; top: 0; }}
    td {{ padding: 10px 14px; border-bottom: 1px solid #eee; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover {{ background: #f8f8f8; }}
    a {{ color: #4a90d9; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .failed {{ background: #fde8e8; padding: 14px 18px; border-radius: 6px; margin-top: 20px; color: #c62828; }}
    .failed h3 {{ font-size: 1em; margin-bottom: 6px; }}
    .failed ul {{ margin-left: 18px; margin-top: 4px; }}
    h2 {{ font-size: 1.1em; margin: 16px 0 10px; color: #333; }}
    @media (max-width: 768px) {{
        body {{ padding: 8px; }}
        h1 {{ font-size: 1.2em; }}
        .stats {{ gap: 12px; padding: 10px 14px; }}
        .stats span {{ font-size: 0.9em; }}
    }}
</style>
</head>
<body>
<div class="container">
    <h1>Code Hotspot Analysis Report</h1>
    <div class="meta">Generated: {date_str}</div>
    <div class="stats">
        <span>Total repos: {run.total_repos}</span>
        <span>Total files: {run.total_files}</span>
        <span>Total hotspots: {run.total_hotspots}</span>
        <span>Min score: {min_str}</span>
        <span>Max score: {max_str}</span>
    </div>
    <h2>Repos</h2>
    <div class="table-wrapper">
        <table>
            <thead><tr><th>Repository</th><th>Files</th><th>Hotspots</th><th>Ratio</th><th>Median Score</th><th>Min Score</th><th>Max Score</th></tr></thead>
            <tbody>{repo_rows}</tbody>
        </table>
    </div>
    {failed_section}
</div>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html_content)
