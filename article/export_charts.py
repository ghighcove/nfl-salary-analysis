"""Export all article charts as PNG images to article/images/."""

import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt

from src.viz import (
    all_positions_scatter_grid,
    boxplot_salary_by_position,
    bar_chart_top_values,
    rookie_vs_veteran_comparison,
    player_trajectory,
    team_value_heatmap,
)

IMG_DIR = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(IMG_DIR, exist_ok=True)

DPI = 150


def save_fig(fig, filename):
    """Save a matplotlib or Plotly figure to PNG."""
    path = os.path.join(IMG_DIR, filename)
    if hasattr(fig, "write_image"):
        # Plotly figure
        fig.write_image(path, width=900, height=500, scale=2)
    else:
        # matplotlib figure
        fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor="white")
        plt.close(fig)
    print(f"  Saved {filename}")


def main():
    print("Loading scored.parquet...")
    df = pd.read_parquet(
        os.path.join(os.path.dirname(__file__), "..", "data", "scored.parquet"),
        engine="fastparquet",
    )
    print(f"  {len(df)} player-seasons loaded.\n")

    charts = [
        ("01_scatter_grid.png", lambda: all_positions_scatter_grid(df)),
        ("02_salary_boxplot.png", lambda: boxplot_salary_by_position(df)),
        ("03_top_bargains.png", lambda: bar_chart_top_values(df, chart_type="bargains")),
        ("04_top_overpaid.png", lambda: bar_chart_top_values(df, chart_type="overpaid")),
        ("05_rookie_vs_veteran.png", lambda: rookie_vs_veteran_comparison(df)),
        ("06_mahomes_trajectory.png", lambda: player_trajectory(df, "Mahomes")),
        ("07_team_heatmap.png", lambda: team_value_heatmap(df, [2022, 2023, 2024])),
    ]

    for filename, gen_func in charts:
        print(f"Generating {filename}...")
        fig = gen_func()
        if fig is None:
            print(f"  SKIPPED (no data)")
            continue
        save_fig(fig, filename)

    print(f"\nDone — {len(charts)} charts exported to {IMG_DIR}")


if __name__ == "__main__":
    main()
