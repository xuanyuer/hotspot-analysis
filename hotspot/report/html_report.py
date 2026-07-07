"""HTML interactive report generation using plotly."""

import html
import json


def write_html_report(result, output_path: str) -> None:
    """Generate HTML report with histogram of hotspot scores and ranked table."""
    files = result.all_files
    hotspot_paths = {f.path for f in result.hotspot_files}

    # Build histogram bins (0-100, step 10)
    n_bins = 10
    total_per_bin = [0] * n_bins
    hotspot_per_bin = [0] * n_bins
    for f in files:
        idx = min(int(f.hotspot_score // 10), n_bins - 1)
        total_per_bin[idx] += 1
        if f.path in hotspot_paths:
            hotspot_per_bin[idx] += 1
    normal_per_bin = [total_per_bin[i] - hotspot_per_bin[i] for i in range(n_bins)]

    # Build the ranked table HTML
    table_rows = ""
    for f in files:
        is_hs = f.path in hotspot_paths
        row_class = "hotspot-row" if is_hs else ""
        # Format hotspot lines as "start-end" or "start-end, start-end"
        line_display = ""
        if f.hotspot_lines:
            line_display = ", ".join(f"{s}-{e}" for s, e in f.hotspot_lines)
        table_rows += (f'<tr class="{row_class}">'
            f'<td class="file-cell">{f.path}</td>'
            f'<td class="num-cell">{f.churn_score:.1f}</td>'
            f'<td class="num-cell">{f.complexity_score:.1f}</td>'
            f'<td class="num-cell">{f.hotspot_score:.1f}</td>'
            f'<td class="num-cell">{f.commit_count}</td>'
            f'<td class="num-cell">{f.author_count}</td>'
            f'<td class="lines-cell" title="{html.escape(line_display)}">{line_display}</td>'
            f'</tr>\n')

    bin_labels = [i * 10 for i in range(n_bins)]
    threshold_val = result.threshold_score

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Code Hotspot Analysis Report</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 16px; background: #f5f5f5; color: #333; }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    h1 {{ font-size: 1.4em; margin-bottom: 4px; color: #1a1a1a; }}
    p.subtitle {{ color: #666; margin-bottom: 16px; }}
    #chart {{ background: white; border-radius: 8px; padding: 12px; margin-bottom: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .stats {{ display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }}
    .stat-card {{ background: white; border-radius: 8px; padding: 12px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); flex: 1; min-width: 140px; }}
    .stat-card .label {{ font-size: 0.8em; color: #666; text-transform: uppercase; }}
    .stat-card .value {{ font-size: 1.6em; font-weight: 600; margin-top: 4px; }}
    .stat-card.hotspot .value {{ color: #e53e3e; }}
    .stat-card.files .value {{ color: #2b6cb0; }}
    .table-wrapper {{ background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); overflow-x: auto; margin-bottom: 16px; -webkit-overflow-scrolling: touch; }}
    .ranked-table {{ width: 100%; border-collapse: collapse; min-width: 550px; }}
    .ranked-table th {{ background: #2c3e50; color: white; padding: 10px 14px; text-align: left; font-weight: 600; position: sticky; top: 0; }}
    .ranked-table td {{ padding: 8px 14px; border-top: 1px solid #eee; white-space: nowrap; }}
    .ranked-table tr:hover {{ background: #f8f9fa; }}
    .ranked-table .file-cell {{ font-family: monospace; font-size: 0.85em; max-width: 500px; overflow: hidden; text-overflow: ellipsis; }}
    .ranked-table .num-cell {{ text-align: right; font-variant-numeric: tabular-nums; min-width: 60px; }}
    .ranked-table .lines-cell {{ font-family: monospace; font-size: 0.8em; color: #c53030; min-width: 80px; }}
    .hotspot-row {{ background: #fff5f5; }}
    .hotspot-row:hover {{ background: #ffe8e8; }}
    @media (max-width: 768px) {{
        body {{ padding: 8px; }}
        h1 {{ font-size: 1.2em; }}
        .stat-card {{ padding: 10px 12px; min-width: 120px; }}
        .stat-card .value {{ font-size: 1.3em; }}
        #chart {{ padding: 8px; }}
    }}
</style>
</head>
<body>
<div class="container">
    <h1>Code Hotspot Analysis Report</h1>
    <p class="subtitle">{result.total_files} files analyzed</p>
    <div class="stats">
        <div class="stat-card files">
            <div class="label">Total Files</div>
            <div class="value">{result.total_files}</div>
        </div>
        <div class="stat-card hotspot">
            <div class="label">Hotspots</div>
            <div class="value">{result.hotspot_count} ({result.hotspot_ratio:.0%})</div>
        </div>
    </div>
    <div id="chart"></div>
    <div class="table-wrapper">
        <table class="ranked-table">
            <tr><th>File</th><th class="num-cell">Churn</th><th class="num-cell">Complexity</th><th class="num-cell">Hotspot</th><th class="num-cell">Commits</th><th class="num-cell">Authors</th><th>Lines</th></tr>
            {table_rows}
        </table>
    </div>
</div>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<script>
var binLabels = {json.dumps(bin_labels)};
var totalBars = {json.dumps(total_per_bin)};
var hotspotBars = {json.dumps(hotspot_per_bin)};
var normalBars = {json.dumps(normal_per_bin)};

var layout = {{
    barmode: 'stack',
    xaxis: {{ title: 'Hotspot Score (0-100)', range: [-5, 105] }},
    yaxis: {{ title: 'File Count', fixedrange: true }},
    shapes: [{{
        type: 'line', x0: {threshold_val}, x1: {threshold_val},
        y0: 0, y1: 1, yref: 'paper',
        line: {{ color: '#e53e3e', width: 2, dash: 'dash' }}
    }}],
    annotations: [{{
        x: {threshold_val}, y: 1, yref: 'paper',
        text: 'Threshold: {threshold_val}',
        showarrow: false, yshift: -10,
        font: {{ size: 12, color: '#e53e3e' }}
    }}],
    margin: {{ t: 60, b: 50, l: 50, r: 20 }},
    height: 400
}};

var traces = [
    {{
        type: 'bar', x: binLabels, y: normalBars,
        name: 'Normal', marker: {{ color: '#63b3ed', opacity: 0.7 }}
    }},
    {{
        type: 'bar', x: binLabels, y: hotspotBars,
        name: 'Hotspot', marker: {{ color: '#fc8181' }}
    }}
];

var config = {{ responsive: true, displayModeBar: false }};
Plotly.newPlot('chart', traces, layout, config);
</script>
</body>
</html>"""

    with open(output_path, 'w') as f:
        f.write(full_html)
