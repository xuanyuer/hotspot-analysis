"""HTML interactive report generation using plotly."""

import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def write_html_report(result, output_path: str) -> None:
    """Generate HTML report with interactive scatter plot and simple ranked table."""
    files = result.all_files

    churns = [f.churn_score for f in files]
    complexities = [f.complexity_score for f in files]
    labels = [f.path for f in files]
    hotspot_scores = [f.hotspot_score for f in files]
    commits = [f.commit_count for f in files]

    median_churn = sum(churns) / len(churns) if churns else 50
    median_complexity = sum(complexities) / len(complexities) if complexities else 50

    # Detect hotspot points
    is_hotspot = [c >= median_churn and cm >= median_complexity for c, cm in zip(churns, complexities)]
    hotspot_churns = [c for c, h in zip(churns, is_hotspot) if h]
    hotspot_complexities = [c for c, h in zip(complexities, is_hotspot) if h]
    other_churns = [c for c, h in zip(churns, is_hotspot) if not h]
    other_complexities = [c for c, h in zip(complexities, is_hotspot) if not h]

    # Build the simple ranked table HTML
    table_rows = ""
    for i, f in enumerate(files):
        is_hs = is_hotspot[i]
        row_class = "hotspot-row" if is_hs else ""
        table_rows += (f'<tr class="{row_class}">'
            f'<td class="file-cell">{f.path}</td>'
            f'<td>{f.churn_score:.1f}</td>'
            f'<td>{f.complexity_score:.1f}</td>'
            f'<td>{f.hotspot_score:.1f}</td>'
            f'<td>{f.commit_count}</td>'
            f'<td>{f.author_count}</td></tr>\n')

    # Build scatter traces JSON for Plotly.js
    traces = []
    if other_churns:
        traces.append(json.dumps({
            "type": "scatter", "x": other_churns, "y": other_complexities,
            "mode": "markers", "text": [l for l, h in zip(labels, is_hotspot) if not h],
            "hoverinfo": "text", "name": "Normal",
            "marker": {"color": "blue", "size": 10, "opacity": 0.6},
        }))
    if hotspot_churns:
        traces.append(json.dumps({
            "type": "scatter", "x": hotspot_churns, "y": hotspot_complexities,
            "mode": "markers", "text": [l for l, h in zip(labels, is_hotspot) if h],
            "hoverinfo": "text", "name": "Hotspot",
            "marker": {"color": "red", "size": 12, "symbol": "diamond"},
        }))

    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Code Hotspot Analysis Report</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; background: #f5f5f5; color: #333; }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    h1 {{ font-size: 1.4em; margin-bottom: 4px; color: #1a1a1a; }}
    p.subtitle {{ color: #666; margin-bottom: 24px; }}
    #chart {{ background: white; border-radius: 8px; padding: 16px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); height: 700px; }}
    .ranked-table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .ranked-table th {{ background: #2c3e50; color: white; padding: 12px 16px; text-align: left; font-weight: 600; }}
    .ranked-table td {{ padding: 8px 16px; border-top: 1px solid #eee; }}
    .ranked-table tr:hover {{ background: #f8f9fa; }}
    .ranked-table .file-cell {{ max-width: 600px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: monospace; font-size: 0.9em; }}
    .hotspot-row {{ background: #fff5f5; }}
    .hotspot-row:hover {{ background: #ffe8e8; }}
</style>
</head>
<body>
<div class="container">
    <h1>Code Hotspot Analysis Report</h1>
    <p class="subtitle">{result.total_files} files analyzed</p>
    <div id="chart"></div>
    <table class="ranked-table">
        <tr><th>File</th><th>Churn</th><th>Complexity</th><th>Hotspot</th><th>Commits</th><th>Authors</th></tr>
        {table_rows}
    </table>
</div>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<script>
var traces = [{','.join(traces)}];
var layout = {{
    title: "Churn vs Complexity",
    xaxis: {{ title: "Churn Score" }},
    yaxis: {{ title: "Complexity Score" }},
    showlegend: true,
    height: 650
}};
Plotly.newPlot('chart', traces, layout);
</script>
</body>
</html>"""

    with open(output_path, 'w') as f:
        f.write(full_html)
