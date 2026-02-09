"""Reusable visualization functions for NFL salary-performance analysis."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Consistent color palette
TEAM_COLORS = {}  # Can be populated later
VALUE_CMAP = "RdYlGn"  # Red (overpaid) to Green (bargain)
sns.set_theme(style="whitegrid", palette="deep", font_scale=1.1)


def scatter_performance_vs_salary(
    df: pd.DataFrame,
    pos_group: str,
    highlight_threshold: float = 2.0,
    interactive: bool = True,
):
    """
    Scatter plot: salary (x) vs. performance (y) with regression line.
    Labels players beyond highlight_threshold std from regression line.
    """
    subset = df[df["pos_group"] == pos_group].copy()
    if len(subset) < 5:
        print(f"Not enough data for {pos_group}")
        return None

    if interactive:
        fig = px.scatter(
            subset,
            x="apy_cap_pct",
            y="performance_zscore",
            color="recent_team",
            size="total_snaps",
            size_max=15,
            hover_data=["player_name", "season", "value_score", "apy"],
            trendline="ols",
            title=f"{pos_group}: Performance vs. Salary (% of Cap)",
            labels={
                "apy_cap_pct": "Salary (% of Cap)",
                "performance_zscore": "Performance Z-Score",
            },
        )

        # Label outliers
        outliers = subset[subset["value_score"].abs() > highlight_threshold]
        for _, row in outliers.iterrows():
            fig.add_annotation(
                x=row["apy_cap_pct"],
                y=row["performance_zscore"],
                text=f"{row['player_name']} ({int(row['season'])})",
                showarrow=True,
                arrowhead=2,
                font=dict(size=9),
            )

        fig.update_layout(height=600, width=900)
        return fig
    else:
        fig, ax = plt.subplots(figsize=(12, 8))
        scatter = ax.scatter(
            subset["apy_cap_pct"],
            subset["performance_zscore"],
            c=subset["value_score"],
            cmap=VALUE_CMAP,
            alpha=0.6,
            s=subset["total_snaps"].fillna(100) / 10,
            edgecolors="gray",
            linewidth=0.5,
        )
        # Regression line
        z = np.polyfit(subset["apy_cap_pct"].fillna(0), subset["performance_zscore"].fillna(0), 1)
        p = np.poly1d(z)
        x_line = np.linspace(subset["apy_cap_pct"].min(), subset["apy_cap_pct"].max(), 100)
        ax.plot(x_line, p(x_line), "r--", alpha=0.7, label="Regression")

        # Label outliers
        outliers = subset[subset["value_score"].abs() > highlight_threshold]
        for _, row in outliers.iterrows():
            ax.annotate(
                f"{row['player_name']} ({int(row['season'])})",
                xy=(row["apy_cap_pct"], row["performance_zscore"]),
                fontsize=7, alpha=0.8,
                arrowprops=dict(arrowstyle="->", alpha=0.5),
            )

        plt.colorbar(scatter, label="Value Score")
        ax.set_xlabel("Salary (% of Cap)")
        ax.set_ylabel("Performance Z-Score")
        ax.set_title(f"{pos_group}: Performance vs. Salary (% of Cap)")
        ax.legend()
        plt.tight_layout()
        return fig


def bar_chart_top_values(
    df: pd.DataFrame,
    pos_group: str = None,
    n: int = 15,
    chart_type: str = "bargains",
):
    """Horizontal bar chart of top bargains or overpaid players."""
    subset = df.copy()
    if pos_group:
        subset = subset[subset["pos_group"] == pos_group]

    if chart_type == "bargains":
        top = subset.nlargest(n, "value_score")
        title = f"Top {n} Bargains" + (f" — {pos_group}" if pos_group else " — All Positions")
        color_col = "value_score"
    else:
        top = subset.nsmallest(n, "value_score")
        title = f"Top {n} Overpaid" + (f" — {pos_group}" if pos_group else " — All Positions")
        color_col = "value_score"

    top = top.sort_values("value_score", ascending=(chart_type != "bargains"))
    top["label"] = top["player_name"] + " (" + top["recent_team"] + ", " + top["season"].astype(int).astype(str) + ")"

    fig, ax = plt.subplots(figsize=(12, max(6, n * 0.4)))
    colors = plt.cm.RdYlGn(
        (top["value_score"] - top["value_score"].min())
        / (top["value_score"].max() - top["value_score"].min() + 1e-9)
    )
    bars = ax.barh(top["label"], top["value_score"], color=colors)

    ax.set_xlabel("Value Score")
    ax.set_title(title)
    ax.axvline(x=0, color="black", linewidth=0.8, linestyle="-")

    # Add value labels on bars
    for bar, val, cap_pct in zip(bars, top["value_score"], top["apy_cap_pct"]):
        x_pos = bar.get_width()
        ax.text(
            x_pos + (0.05 if x_pos >= 0 else -0.05),
            bar.get_y() + bar.get_height() / 2,
            f"{val:.2f} (cap: {cap_pct:.1%})",
            ha="left" if x_pos >= 0 else "right",
            va="center",
            fontsize=8,
        )

    plt.tight_layout()
    return fig


def boxplot_salary_by_position(df: pd.DataFrame):
    """Box plot of salary distribution by position group with strip overlay."""
    fig, ax = plt.subplots(figsize=(14, 7))

    order = ["QB", "WR", "RB", "TE", "OL", "DL", "LB", "DB", "K"]
    plot_df = df[df["pos_group"].isin(order)].copy()

    sns.boxplot(
        data=plot_df, x="pos_group", y="apy_cap_pct",
        order=order, ax=ax, showfliers=False, palette="Set2",
    )
    sns.stripplot(
        data=plot_df, x="pos_group", y="apy_cap_pct",
        order=order, ax=ax, alpha=0.3, size=3, jitter=True, color="black",
    )

    # Label top outliers per group
    for pos in order:
        grp = plot_df[plot_df["pos_group"] == pos]
        if len(grp) == 0:
            continue
        top_player = grp.nlargest(1, "apy_cap_pct").iloc[0]
        ax.annotate(
            top_player["player_name"],
            xy=(order.index(pos), top_player["apy_cap_pct"]),
            fontsize=7, alpha=0.8,
            xytext=(5, 5), textcoords="offset points",
        )

    ax.set_xlabel("Position Group")
    ax.set_ylabel("Salary (% of Cap)")
    ax.set_title("Salary Distribution by Position Group")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
    plt.tight_layout()
    return fig


def year_over_year_trends(df: pd.DataFrame):
    """Line chart: average value score by position group over seasons."""
    order = ["QB", "WR", "RB", "TE", "OL", "DL", "LB", "DB", "K"]
    plot_df = df[df["pos_group"].isin(order)].copy()

    trends = plot_df.groupby(["season", "pos_group"])["value_score"].mean().reset_index()

    fig = px.line(
        trends,
        x="season",
        y="value_score",
        color="pos_group",
        title="Average Value Score by Position Group Over Time",
        labels={"season": "Season", "value_score": "Avg Value Score", "pos_group": "Position"},
        category_orders={"pos_group": order},
    )
    fig.update_layout(height=500, width=900)
    fig.update_xaxes(dtick=1)
    return fig


def team_value_heatmap(df: pd.DataFrame, seasons: list = None):
    """Heatmap: teams x position groups, cell = avg value score."""
    pos_order = ["QB", "WR", "RB", "TE", "OL", "DL", "LB", "DB", "K"]
    subset = df[df["pos_group"].isin(pos_order)].copy()
    if seasons:
        subset = subset[subset["season"].isin(seasons)]

    pivot = subset.pivot_table(
        values="value_score", index="recent_team", columns="pos_group",
        aggfunc="mean"
    )
    # Reorder columns
    pivot = pivot[[c for c in pos_order if c in pivot.columns]]
    # Sort by overall average
    pivot["_avg"] = pivot.mean(axis=1)
    pivot = pivot.sort_values("_avg", ascending=False).drop(columns="_avg")

    fig, ax = plt.subplots(figsize=(14, max(8, len(pivot) * 0.35)))
    sns.heatmap(
        pivot, cmap=VALUE_CMAP, center=0, annot=True, fmt=".2f",
        linewidths=0.5, ax=ax, cbar_kws={"label": "Avg Value Score"},
    )
    season_label = f" ({min(seasons)}-{max(seasons)})" if seasons else ""
    ax.set_title(f"Best Value Teams by Position{season_label}")
    ax.set_ylabel("")
    plt.tight_layout()
    return fig


def rookie_vs_veteran_comparison(df: pd.DataFrame):
    """Side-by-side distributions: rookie vs. veteran contract value scores."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for i, (ct, title) in enumerate([("rookie", "Rookie Contracts"), ("veteran", "Veteran Contracts")]):
        subset = df[df["contract_type"] == ct]
        if len(subset) == 0:
            continue
        sns.histplot(subset["value_score"], kde=True, ax=axes[i], color="green" if ct == "rookie" else "steelblue")
        axes[i].set_title(title)
        axes[i].set_xlabel("Value Score")
        axes[i].axvline(x=0, color="black", linewidth=0.8, linestyle="--")
        axes[i].axvline(x=subset["value_score"].median(), color="red", linewidth=1, linestyle="--", label=f"Median: {subset['value_score'].median():.2f}")
        axes[i].legend()

    plt.suptitle("Rookie vs. Veteran Contract Value", fontsize=14)
    plt.tight_layout()
    return fig


def player_trajectory(df: pd.DataFrame, player_name: str):
    """Interactive plot: single player's value score trajectory over seasons."""
    player_data = df[df["player_name"].str.contains(player_name, case=False, na=False)]
    if len(player_data) == 0:
        print(f"No data found for '{player_name}'")
        return None

    player_data = player_data.sort_values("season")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=player_data["season"],
            y=player_data["value_score"],
            name="Value Score",
            mode="lines+markers",
            marker=dict(size=10),
            line=dict(width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(
            x=player_data["season"],
            y=player_data["apy_cap_pct"],
            name="Salary (% Cap)",
            opacity=0.4,
            marker_color="orange",
        ),
        secondary_y=True,
    )
    fig.add_trace(
        go.Scatter(
            x=player_data["season"],
            y=player_data["performance_zscore"],
            name="Performance Z",
            mode="lines+markers",
            marker=dict(size=8),
            line=dict(dash="dash"),
        ),
        secondary_y=False,
    )

    # Mark contract signing years
    if "year_signed" in player_data.columns:
        contract_years = player_data.dropna(subset=["year_signed"])
        for _, row in contract_years.drop_duplicates(subset=["year_signed"]).iterrows():
            fig.add_vline(
                x=row["year_signed"], line_dash="dot", line_color="gray",
                annotation_text="Contract signed",
            )

    actual_name = player_data["player_name"].iloc[0]
    fig.update_layout(
        title=f"{actual_name} — Value Trajectory",
        xaxis_title="Season",
        height=500,
        width=900,
    )
    fig.update_yaxes(title_text="Z-Score", secondary_y=False)
    fig.update_yaxes(title_text="Salary (% of Cap)", secondary_y=True)
    fig.update_xaxes(dtick=1)

    return fig


def all_positions_scatter_grid(df: pd.DataFrame, highlight_threshold: float = 2.0):
    """Grid of scatter plots for all position groups."""
    pos_order = ["QB", "WR", "RB", "TE", "OL", "DL", "LB", "DB", "K"]
    positions = [p for p in pos_order if p in df["pos_group"].unique()]

    n_cols = 3
    n_rows = (len(positions) + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 5 * n_rows))
    axes = axes.flatten() if n_rows > 1 else [axes] if n_rows == 1 and n_cols == 1 else axes.flatten()

    for idx, pos in enumerate(positions):
        ax = axes[idx]
        subset = df[df["pos_group"] == pos]

        scatter = ax.scatter(
            subset["apy_cap_pct"],
            subset["performance_zscore"],
            c=subset["value_score"],
            cmap=VALUE_CMAP,
            alpha=0.5,
            s=30,
            edgecolors="gray",
            linewidth=0.3,
        )

        # Regression line
        valid = subset.dropna(subset=["apy_cap_pct", "performance_zscore"])
        if len(valid) > 2:
            z = np.polyfit(valid["apy_cap_pct"], valid["performance_zscore"], 1)
            p = np.poly1d(z)
            x_line = np.linspace(valid["apy_cap_pct"].min(), valid["apy_cap_pct"].max(), 50)
            ax.plot(x_line, p(x_line), "r--", alpha=0.7, linewidth=1)

        # Label top outliers
        outlier_mask = subset["value_score"].abs() > highlight_threshold
        if outlier_mask.sum() > 0:
            outlier_pool = subset[outlier_mask]
            outliers = pd.concat([outlier_pool.nlargest(3, "value_score"), outlier_pool.nsmallest(3, "value_score")])
        else:
            outliers = pd.DataFrame()

        for _, row in outliers.head(4).iterrows():
            ax.annotate(
                row["player_name"].split()[-1],
                xy=(row["apy_cap_pct"], row["performance_zscore"]),
                fontsize=6, alpha=0.7,
            )

        ax.set_title(pos, fontweight="bold")
        ax.set_xlabel("Cap %")
        ax.set_ylabel("Performance Z")

    # Hide unused axes
    for idx in range(len(positions), len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle("Performance vs. Salary by Position Group", fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig
