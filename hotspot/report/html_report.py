"""HTML interactive report generation using plotly."""

import json


def write_html_report(result, output_path: str) -> None:
    """Generate HTML report with interactive scatter plot and simple ranked table."""
    files = result.all_files

    churns = [f.churn_score for f in files]
    complexities = [f.complexity_score for f in files]
    labels = [f.path for f in files]

    median_churn = sum(churns) / len(churns) if churns else 50
    median_complexity = sum(complexities) / len(complexities) if complexities else 50

    # Detect hotspot points
    is_hotspot = [c >= median_churn and cm >= median_complexity for c, cm in zip(churns, complexities)]

    # Group points by (x, y) position to detect overlaps
    from collections import defaultdict
    position_groups = defaultdict(list)
    for i, f in enumerate(files):
        key = (churns[i], complexities[i])
        position_groups[key].append(i)

    # Build scatter data with jitter for overlapping points
    jittered_x = []
    jittered_y = []
    jittered_texts = []
    jittered_hotspot = []

    for i, f in enumerate(files):
        is_hs = is_hotspot[i]
        x, y = churns[i], complexities[i]

        group = position_groups[(x, y)]
        if len(group) > 1:
            idx_in_group = group.index(i)
            total = len(group)
            # Distribute points in a circle around center
            import math
            angle = (2 * math.pi * idx_in_group) / total
            radius = 0.8
            x += radius * math.cos(angle)
            y += radius * math.sin(angle)

        jittered_x.append(x)
        jittered_y.append(y)
        jittered_texts.append(f.path)
        jittered_hotspot.append(is_hs)

    # Build traces
    traces = []

    if any(not h for h in jittered_hotspot):
        traces.append(json.dumps({
            "type": "scatter",
            "x": [x for x, m in zip(jittered_x, [not h for h in jittered_hotspot]) if m],
            "y": [y for y, m in zip(jittered_y, [not h for h in jittered_hotspot]) if m],
            "text": [t for t, m in zip(jittered_texts, [not h for h in jittered_hotspot]) if m],
            "mode": "markers",
            "hovertemplate": "%{text}<extra></extra>",
            "name": "Normal",
            "marker": {"color": "blue", "size": 10, "opacity": 0.6},
        }))

    if any(jittered_hotspot):
        traces.append(json.dumps({
            "type": "scatter",
            "x": [x for x, m in zip(jittered_x, jittered_hotspot) if m],
            "y": [y for y, m in zip(jittered_y, jittered_hotspot) if m],
            "text": [t for t, m in zip(jittered_texts, jittered_hotspot) if m],
            "mode": "markers",
            "hovertemplate": "%{text}<extra></extra>",
            "name": "Hotspot",
            "marker": {"color": "red", "size": 12, "symbol": "diamond"},
        }))

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
