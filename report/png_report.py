"""PNG scatter plot generation using matplotlib."""

import matplotlib
matplotlib.use("Agg")  # non-interactive backend
import matplotlib.pyplot as plt


def write_png_scatter(result, output_path: str) -> None:
    """Generate scatter plot (churn x, complexity y) and save as PNG.
    
    Top-right quadrant (both churn and complexity above median) highlighted
    as the hotspot zone.
    """
    files = result.all_files
    if not files:
        # Write a minimal blank PNG
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_title("Hotspot Analysis (no data)")
        ax.set_xlabel("Churn Score")
        ax.set_ylabel("Complexity Score")
        fig.savefig(output_path, dpi=100, bbox_inches="tight")
        plt.close(fig)
        return

    churns = [f.churn_score for f in files]
    complexities = [f.complexity_score for f in files]
    labels = [f.path for f in files]

    median_churn = sum(churns) / len(churns) if churns else 50
    median_complexity = sum(complexities) / len(complexities) if complexities else 50

    # Split into hotspot (top-right) and others
    hotspot_churns = [c for c, f in zip(churns, files) if c >= median_churn and f.complexity_score >= median_complexity]
    hotspot_complexities = [c for c, f in zip(complexities, files) if c >= median_churn and f.complexity_score >= median_complexity]
    other_churns = [c for c, f in zip(churns, files) if not (c >= median_churn and f.complexity_score >= median_complexity)]
    other_complexities = [c for c, f in zip(complexities, files) if not (c >= median_churn and f.complexity_score >= median_complexity)]

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.scatter(other_churns, other_complexities, c="blue", alpha=0.6, label="Normal")
    if hotspot_churns:
        ax.scatter(hotspot_churns, hotspot_complexities, c="red", alpha=0.8, s=80, label="Hotspot", zorder=5)

    # Draw quadrant lines
    ax.axvline(x=median_churn, color="gray", linestyle="--", linewidth=0.8)
    ax.axhline(y=median_complexity, color="gray", linestyle="--", linewidth=0.8)

    ax.set_xlabel("Churn Score")
    ax.set_ylabel("Complexity Score")
    ax.set_title("Code Hotspot Analysis")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=100, bbox_inches="tight")
    plt.close(fig)
