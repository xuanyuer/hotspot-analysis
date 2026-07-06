"""Consolidated HTML report generation for multi-repo runs."""

import html as html_mod
from datetime import datetime


def write_consolidated_html(run, output_path: str) -> None:
    """Generate a single self-contained HTML report for management review."""
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Build per-repo section rows
    repo_sections = ""
    for r in run.repos:
        avg_score = sum(f.hotspot_score for f in r.all_files) / len(r.all_files) if r.all_files else 0
        top3 = r.all_files[:3]

        section = f"""
        <div class="repo-section">
            <h3>{html_mod.escape(r.repo_name)}</h3>
            <div class="repo-stats">
                <span>Files: {r.total_files}</span>
                <span>Hotspots: {r.hotspot_count} ({r.hotspot_ratio:.0%})</span>
                <span>Avg Score: {avg_score:.1f}</span>
            </div>
            <table class="file-table">
                <thead><tr><th>File</th><th>Churn</th><th>Complexity</th><th>Hotspot</th><th>Commits</th></tr></thead>
                <tbody>"""
        for fi in r.all_files:
            hotspot_class = " hotspot" if fi.hotspot_score > 0 else ""
            section += f'<tr class="{html_mod.escape(hotspot_class.strip())}">'
            section += f"<td>{html_mod.escape(fi.path)}</td>"
            section += f"<td>{fi.churn_score:.1f}</td>"
            section += f"<td>{fi.complexity_score:.1f}</td>"
            section += f"<td>{fi.hotspot_score:.1f}</td>"
            section += f"<td>{fi.commit_count}</td>"
            section += "</tr>"
        section += "</tbody></table>"

        # Top 3 callouts
        if top3:
            section += '<div class="top-hotspots"><strong>Top 3 Hotspots:</strong><ul>'
            for fi in top3:
                section += f"<li>{html_mod.escape(fi.path)} (score: {fi.hotspot_score:.1f})</li>"
            section += "</ul></div>"

        section += "</div>"
        repo_sections += section

    # Combined ranked table rows
    all_files_sorted = sorted(run.repos[0].all_files if run.repos else [], key=lambda f: 0)
    all_sorted = []
    for r in run.repos:
        all_sorted.extend([(r.repo_name, fi) for fi in r.all_files])
    all_sorted.sort(key=lambda x: x[1].hotspot_score, reverse=True)

    combined_rows = ""
    for repo_name, fi in all_sorted:
        hotspot_class = " hotspot" if fi.hotspot_score > 0 else ""
        combined_rows += f'<tr class="{html_mod.escape(hotspot_class.strip())}">'
        combined_rows += f"<td>{html_mod.escape(repo_name)}</td>"
        combined_rows += f"<td>{html_mod.escape(fi.path)}</td>"
        combined_rows += f"<td>{fi.churn_score:.1f}</td>"
        combined_rows += f"<td>{fi.complexity_score:.1f}</td>"
        combined_rows += f"<td>{fi.hotspot_score:.1f}</td>"
        combined_rows += f"<td>{fi.commit_count}</td>"
        combined_rows += "</tr>"

    # Failed repos section
    failed_section = ""
    if run.failed_repos:
        failed_section = '<div class="failed-repos"><h3>Failed Repositories</h3><ul>'
        for fr in run.failed_repos:
            failed_section += f"<li>{html_mod.escape(fr)}</li>"
        failed_section += "</ul></div>"

    run_level_stats = (
        f"<div class='run-stats'>"
        f"<span>Total repos: {run.total_repos}</span> "
        f"<span>Total files: {run.total_files}</span> "
        f"<span>Total hotspots: {run.total_hotspots}</span> "
        f"</div>"
    )

    # Repo ranking by max hotspot score
    repo_ranking = ""
    repo_max_scores = [(r.repo_name, max((f.hotspot_score for f in r.all_files), default=0)) for r in run.repos]
    repo_max_scores.sort(key=lambda x: x[1], reverse=True)
    if repo_max_scores:
        repo_ranking = """<div class="repo-ranking"><h3>Repos Ranked by Risk</h3><ol>
"""
        for i, (name, score) in enumerate(repo_max_scores, 1):
            repo_ranking += f"<li>{html_mod.escape(name)} (max score: {score:.1f})</li>\n"
        repo_ranking += "</ol></div>"

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Code Hotspot Analysis Report</title>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 24px; background: #f5f5f5; color: #333; line-height: 1.6; }}
    .container {{ max-width: 1100px; margin: 0 auto; }}
    h1 {{ font-size: 1.5em; margin-bottom: 4px; color: #1a1a1a; }}
    h2 {{ font-size: 1.2em; margin: 24px 0 12px; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
    h3 {{ font-size: 1.1em; margin: 12px 0 8px; color: #444; }}
    .meta {{ font-size: 0.9em; color: #666; margin-bottom: 16px; }}
    .run-stats {{ background: #e8f4f8; padding: 12px 16px; border-radius: 6px; display: flex; gap: 24px; margin-bottom: 24px; flex-wrap: wrap; }}
    .run-stats span {{ font-weight: 500; }}
    .repo-section {{ background: #fff; border: 1px solid #e0e0e0; border-radius: 6px; padding: 16px; margin-bottom: 16px; }}
    .repo-stats {{ display: flex; gap: 16px; margin-bottom: 12px; font-size: 0.9em; color: #666; flex-wrap: wrap; }}
    .file-table {{ width: 100%; border-collapse: collapse; font-size: 0.9em; }}
    .file-table th {{ background: #f8f8f8; text-align: left; padding: 8px 12px; border-bottom: 2px solid #ddd; font-weight: 600; }}
    .file-table td {{ padding: 6px 12px; border-bottom: 1px solid #eee; }}
    .file-table tr.hotspot {{ background: #fff3f3; }}
    .file-table tr:hover {{ background: #f0f0f0; }}
    .top-hotspots {{ background: #fff8e1; padding: 8px 12px; border-radius: 4px; margin-top: 8px; font-size: 0.9em; }}
    .top-hotspots ul {{ margin-left: 20px; margin-top: 4px; }}
    .failed-repos {{ background: #fde8e8; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; color: #c62828; }}
    .failed-repos ul {{ margin-left: 20px; margin-top: 8px; }}
    .repo-ranking {{ background: #f0f8e8; padding: 12px 16px; border-radius: 6px; margin-bottom: 16px; }}
    .repo-ranking ol {{ margin-left: 20px; margin-top: 8px; }}
</style>
</head>
<body>
<div class="container">
    <h1>Code Hotspot Analysis Report</h1>
    <div class="meta">Generated: {date_str} | Repos: {run.total_repos} | Files: {run.total_files} | Hotspots: {run.total_hotspots}</div>
    {run_level_stats}
    {repo_ranking}
    <h2>Per-Repository Analysis</h2>
    {repo_sections}
    <h2>Combined Ranked Table</h2>
    <table class="file-table">
        <thead><tr><th>Repo</th><th>File</th><th>Churn</th><th>Complexity</th><th>Hotspot</th><th>Commits</th></tr></thead>
        <tbody>{combined_rows}</tbody>
    </table>
    {failed_section}
</div>
</body>
</html>"""

    with open(output_path, "w") as f:
        f.write(html_content)
