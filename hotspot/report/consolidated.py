"""Consolidated HTML report — simple summary with links to individual reports."""

import html as html_mod
from datetime import datetime


def write_consolidated_html(run, output_path: str) -> None:
    """Generate a simple consolidated HTML report for management review.

    Shows a high-level summary table of all repos with links to their
    individual HTML reports. No per-file detail — just the summary.
    """
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Repo summary rows
    repo_rows = ""
    for r in run.repos:
        avg_score = sum(f.hotspot_score for f in r.all_files) / len(r.all_files) if r.all_files else 0
        link = f"{r.repo_name}/report.html"
        repo_rows += f"""<tr>
            <td><a href="{html_mod.escape(link)}">{html_mod.escape(r.repo_name)}</a></td>
            <td>{r.total_files}</td>
            <td>{r.hotspot_count}</td>
            <td>{r.hotspot_ratio:.0%}</td>
            <td>{avg_score:.1f}</td>
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
<title>Code Hotspot Analysis Report</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; background: #f5f5f5; color: #333; line-height: 1.6; }}
    .container {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ font-size: 1.4em; margin-bottom: 4px; color: #1a1a1a; }}
    .meta {{ font-size: 0.9em; color: #666; margin-bottom: 20px; }}
    .stats {{ background: #e8f4f8; padding: 14px 18px; border-radius: 6px; display: flex; gap: 28px; margin-bottom: 24px; flex-wrap: wrap; }}
    .stats span {{ font-weight: 500; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border-radius: 6px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    th {{ background: #4a90d9; color: white; text-align: left; padding: 10px 14px; font-weight: 600; }}
    td {{ padding: 10px 14px; border-bottom: 1px solid #eee; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:hover {{ background: #f8f8f8; }}
    a {{ color: #4a90d9; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    .failed {{ background: #fde8e8; padding: 14px 18px; border-radius: 6px; margin-top: 24px; color: #c62828; }}
    .failed h3 {{ font-size: 1em; margin-bottom: 6px; }}
    .failed ul {{ margin-left: 18px; margin-top: 4px; }}
    h2 {{ font-size: 1.1em; margin: 20px 0 12px; color: #333; }}
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
    </div>
    <h2>Repos</h2>
    <table>
        <thead><tr><th>Repository</th><th>Files</th><th>Hotspots</th><th>Ratio</th><th>Avg Score</th></tr></thead>
        <tbody>{repo_rows}</tbody>
    </table>
    {failed_section}
</div>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html_content)
