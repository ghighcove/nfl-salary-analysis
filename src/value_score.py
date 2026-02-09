"""Composite value score calculation by position group."""

import pandas as pd
import numpy as np
from scipy import stats as scipy_stats


# Position-specific stat weights for composite performance score
POSITION_WEIGHTS = {
    "QB": {
        "passing_yards": 0.20,
        "passing_tds": 0.25,
        "int_rate_inv": 0.15,  # inverted — lower is better
        "passer_rating": 0.20,
        "completion_pct": 0.10,
        "rushing_yards": 0.10,
    },
    "RB": {
        "rushing_yards": 0.30,
        "rushing_tds": 0.25,
        "yards_per_carry": 0.15,
        "receiving_yards": 0.20,
        "fumbles_inv": 0.10,  # inverted
    },
    "WR": {
        "receiving_yards": 0.30,
        "receptions": 0.20,
        "receiving_tds": 0.30,
        "catch_rate": 0.20,
    },
    "TE": {
        "receiving_yards": 0.30,
        "receptions": 0.20,
        "receiving_tds": 0.30,
        "catch_rate": 0.20,
    },
    "OL": {
        "total_snaps": 0.70,
        "games_played": 0.30,
    },
    "DL": {
        "def_sacks": 0.35,
        "def_qb_hits": 0.25,
        "def_tackles": 0.25,
        "def_pressures": 0.15,
    },
    "LB": {
        "def_tackles": 0.25,
        "def_sacks": 0.20,
        "def_ints": 0.20,
        "def_pressures": 0.20,
        "total_snaps": 0.15,
    },
    "DB": {
        "def_ints": 0.30,
        "def_tackles": 0.25,
        "def_pressures": 0.15,
        "total_snaps": 0.30,
    },
    "K": {
        "fg_pct": 0.40,
        "fg_made": 0.40,
        "xp_pct": 0.20,
    },
}


def _prepare_inverted_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Create inverted versions of stats where lower is better."""
    out = df.copy()

    # INT rate inverted (lower INT rate = better)
    if "int_rate" in out.columns:
        out["int_rate_inv"] = -out["int_rate"].fillna(0)

    # Fumbles inverted
    fumble_cols = ["rushing_fumbles", "receiving_fumbles"]
    existing_fumble_cols = [c for c in fumble_cols if c in out.columns]
    if existing_fumble_cols:
        out["fumbles_inv"] = -out[existing_fumble_cols].fillna(0).sum(axis=1)

    return out


def _zscore_within_group(series: pd.Series) -> pd.Series:
    """Z-score normalize a series, handling NaN and zero-variance."""
    valid = series.dropna()
    if len(valid) < 3 or valid.std() == 0:
        return pd.Series(0.0, index=series.index)
    return (series - series.mean()) / series.std()


def compute_composite_score(df: pd.DataFrame, pos_group: str) -> pd.Series:
    """Compute weighted composite performance z-score for a position group."""
    weights = POSITION_WEIGHTS.get(pos_group)
    if weights is None:
        return pd.Series(np.nan, index=df.index)

    prepared = _prepare_inverted_stats(df)

    composite = pd.Series(0.0, index=df.index)
    total_weight = 0.0

    for stat, weight in weights.items():
        if stat in prepared.columns:
            z = _zscore_within_group(prepared[stat].astype(float))
            composite += z * weight
            total_weight += weight

    if total_weight > 0:
        composite /= total_weight  # Normalize by actual weight used

    return composite


def compute_salary_zscore(df: pd.DataFrame) -> pd.Series:
    """Z-score normalize salary (apy_cap_pct) within position group."""
    return _zscore_within_group(df["apy_cap_pct"].astype(float))


def compute_value_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Compute value scores for all players. Operates within position groups."""
    results = []

    for pos_group in df["pos_group"].unique():
        if pos_group not in POSITION_WEIGHTS:
            continue

        mask = df["pos_group"] == pos_group
        group = df[mask].copy()

        if len(group) < 5:
            continue

        # Performance composite
        group["performance_zscore"] = compute_composite_score(group, pos_group)

        # Salary z-score (within position)
        group["salary_zscore"] = compute_salary_zscore(group)

        # Value score = performance - salary
        # Positive = outperforming salary (bargain)
        # Negative = underperforming salary (overpaid)
        group["value_score"] = group["performance_zscore"] - group["salary_zscore"]

        # Percentile rank within position group
        group["value_percentile"] = group["value_score"].rank(pct=True) * 100

        # Flag outliers (>2 std from 0)
        group["is_bargain"] = group["value_score"] > 2.0
        group["is_overpaid"] = group["value_score"] < -2.0

        results.append(group)

    if not results:
        return df.assign(
            performance_zscore=np.nan,
            salary_zscore=np.nan,
            value_score=np.nan,
            value_percentile=np.nan,
            is_bargain=False,
            is_overpaid=False,
        )

    return pd.concat(results, ignore_index=True)


def top_bargains(df: pd.DataFrame, pos_group: str = None, n: int = 15) -> pd.DataFrame:
    """Get top N bargain players (highest value score)."""
    subset = df.copy()
    if pos_group:
        subset = subset[subset["pos_group"] == pos_group]
    return subset.nlargest(n, "value_score")[
        ["player_name", "pos_group", "recent_team", "season",
         "apy_cap_pct", "performance_zscore", "salary_zscore", "value_score"]
    ]


def top_overpaid(df: pd.DataFrame, pos_group: str = None, n: int = 15) -> pd.DataFrame:
    """Get top N overpaid players (lowest value score)."""
    subset = df.copy()
    if pos_group:
        subset = subset[subset["pos_group"] == pos_group]
    return subset.nsmallest(n, "value_score")[
        ["player_name", "pos_group", "recent_team", "season",
         "apy_cap_pct", "performance_zscore", "salary_zscore", "value_score"]
    ]
