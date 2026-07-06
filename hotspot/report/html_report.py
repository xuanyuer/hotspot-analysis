"""HTML interactive report generation using plotly."""

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def write_html_report(result, output_path: str) -> None:
    """Generate interactive HTML report with scatter plot and ranked table."""
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
    hotspot_labels = [l for l, h in zip(labels, is_hotspot) if h]
    other_churns = [c for c, h in zip(churns, is_hotspot) if not h]
    other_complexities = [c for c, h in zip(complexities, is_hotspot) if not h]
    other_labels = [l for l, h in zip(labels, is_hotspot) if not h]

    fig = make_subplots(rows=2, cols=1, specs=[[{"type": "scatter"}], [{"type": "table"}]],
                        row_heights=[0.6, 0.4], subplot_titles=["Churn vs Complexity", "Ranked Files"])

    # Scatter plot
    if other_labels:
        fig.add_trace(go.Scatter(
            x=other_churns, y=other_complexities,
            mode="markers", text=other_labels, hoverinfo="text",
            marker=dict(color="blue", size=10, opacity=0.6),
            name="Normal",
        ), row=1, col=1)

    if hotspot_labels:
        fig.add_trace(go.Scatter(
            x=hotspot_churns, y=hotspot_complexities,
            mode="markers", text=hotspot_labels, hoverinfo="text",
            marker=dict(color="red", size=12, symbol="diamond"),
            name="Hotspot",
        ), row=1, col=1)

    # Axes
    fig.update_xaxes(title_text="Churn Score", row=1, col=1)
    fig.update_yaxes(title_text="Complexity Score", row=1, col=1)
    fig.update_layout(height=700, title_text="Code Hotspot Analysis", showlegend=True)

    # Table
    if files:
        fig.add_trace(go.Table(
            header=dict(values=["File", "Churn", "Complexity", "Hotspot", "Commits", "Authors"],
                       fill_color="steelblue", font=dict(color="white")),
            cells=dict(values=[
                [f.path for f in files],
                [f"{f.churn_score:.1f}" for f in files],
                [f"{f.complexity_score:.1f}" for f in files],
                [f"{f.hotspot_score:.1f}" for f in files],
                [f.commit_count for f in files],
                [f.author_count for f in files],
            ], fill_color="lavender"),
        ), row=2, col=1)

    fig.write_html(output_path)
