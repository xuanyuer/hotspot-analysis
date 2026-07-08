"""Consolidated HTML report — simple summary with links to individual reports."""

import html as html_mod
import json
from datetime import datetime
from typing import Any


def write_consolidated_html(run, output_path: str) -> None:
    """Generate a simple consolidated HTML report for management review.

    Shows a high-level summary table of all repos with links to their
    individual HTML reports. No per-file detail — just the summary.
    """
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Repo summary rows — sorted by hotspot count > ratio, all descending
    repo_scores = []
    for r in run.repos:
        repo_scores.append((r.hotspot_count, r.hotspot_ratio, r))
    repo_scores.sort(key=lambda x: (x[0], x[1]), reverse=True)

    repo_rows = ""
    repo_data: list[dict[str, Any]] = []
    for hotspot_count, ratio, r in repo_scores:
        link = f"{r.repo_name}/report.html"
        repo_rows += f"""<tr>
            <td><a href="{html_mod.escape(link)}">{html_mod.escape(r.repo_name)}</a></td>
            <td>{r.total_files}</td>
            <td>{r.hotspot_count}</td>
            <td>{r.hotspot_ratio:.0%}</td>
        </tr>"""
        repo_data.append({
            'name': r.repo_name,
            'files': r.total_files,
            'hotspots': r.hotspot_count,
        })

    # Embedded chart data
    json_data = json.dumps(repo_data)

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
    .chart {{ display: flex; gap: 2px; min-height: 200px; padding: 10px 0 120px; margin-bottom: 16px; overflow-x: auto; overflow-y: visible; }}
    .chart-bar {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-end; flex: 1; min-width: 18px; max-width: 36px; height: 200px; cursor: pointer; position: relative; }}
    .chart-bar:hover .chart-tooltip {{ opacity: 1; pointer-events: auto; }}
    .bar-stack {{ width: 100%; display: flex; flex-direction: column; }}
    .bar-segment {{ width: 100%; }}
    .bar-segment.hotspots {{ background: #e67e22; }}
    .bar-segment.files {{ background: #3498db; }}
    .chart-label {{ font-size: 9px; color: #666; text-align: center; position: absolute; top: 105%; left: 50%; transform: translateX(-50%); writing-mode: vertical-rl; white-space: nowrap; overflow: hidden; width: 14px; text-overflow: ellipsis; }}
    .chart-tooltip {{ position: absolute; top: -60px; left: 50%; transform: translateX(-50%); background: #333; color: #fff; padding: 6px 10px; border-radius: 4px; font-size: 11px; white-space: nowrap; opacity: 0; pointer-events: none; z-index: 100; transition: opacity 0.15s; }}
    .chart-tooltip::after {{ content: ''; position: absolute; top: 100%; left: 50%; transform: translateX(-50%); border: 5px solid transparent; border-top-color: #333; }}
    .chart-legend {{ display: flex; gap: 16px; margin-bottom: 10px; }}
    .chart-legend span {{ display: flex; align-items: center; gap: 6px; font-size: 0.85em; }}
    .chart-legend .dot {{ width: 10px; height: 10px; border-radius: 2px; }}
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
    </div>
    <h2>Hotspots by Repository</h2>
    <div class="chart-legend">
        <span><span class="dot" style="background:#e67e22"></span> Hotspots</span>
        <span><span class="dot" style="background:#3498db"></span> Files</span>
    </div>
    <div class="chart" id="chart"></div>
    <h2>Repos</h2>
    <div class="table-wrapper">
        <table>
            <thead><tr><th>Repository</th><th>Files</th><th>Hotspots</th><th>Ratio</th></tr></thead>
            <tbody>{repo_rows}</tbody>
        </table>
    </div>
    {failed_section}
</div>

<script>
(function() {{
    var repoData = {json_data};
    var maxTotal = Math.max.apply(null, repoData.map(function(r) {{ return r.files; }}));
    var chartEl = document.getElementById('chart');
    var barWidth = Math.max(14, Math.min(28, Math.floor(1300 / repoData.length)));

    // Wait for DOM to render chart container, then compute pixel heights
    function renderBars() {{
        var chartHeight = chartEl.offsetHeight || 200;

        repoData.forEach(function(repo) {{
            var nonHotspot = repo.files - repo.hotspots;
            var fileH = Math.max(1, Math.round((repo.files / maxTotal) * chartHeight));
            var hotspotH = Math.max(0, Math.round((repo.hotspots / maxTotal) * chartHeight));
            var nonH = fileH - hotspotH;

            var bar = document.createElement('div');
            bar.className = 'chart-bar';
            bar.style.width = barWidth + 'px';

            var tooltip = document.createElement('div');
            tooltip.className = 'chart-tooltip';
            tooltip.textContent = repo.name + ': ' + repo.hotspots + '/' + repo.files;
            bar.appendChild(tooltip);

            var stack = document.createElement('div');
            stack.className = 'bar-stack';
            stack.style.height = fileH + 'px';

            if (nonH > 0) {{
                var segF = document.createElement('div');
                segF.className = 'bar-segment files';
                segF.style.height = nonH + 'px';
                stack.appendChild(segF);
            }}

            if (hotspotH > 0) {{
                var segH = document.createElement('div');
                segH.className = 'bar-segment hotspots';
                segH.style.height = hotspotH + 'px';
                stack.appendChild(segH);
            }}

            bar.appendChild(stack);

            var label = document.createElement('div');
            label.className = 'chart-label';
            label.textContent = repo.name;
            bar.appendChild(label);

            chartEl.appendChild(bar);
        }});
    }}

    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', renderBars);
    }} else {{
        renderBars();
    }}
}})();
</script>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html_content)
