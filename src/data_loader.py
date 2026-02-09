"""Fetch and cache NFL data from nfl_data_py to local parquet files."""

import os
from pathlib import Path

import nfl_data_py as nfl
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

YEARS = list(range(2015, 2025))
PFR_YEARS = list(range(2018, 2025))  # PFR data only available 2018+


def _cache_path(name: str) -> Path:
    return DATA_DIR / f"{name}.parquet"


def _sanitize_for_parquet(df: pd.DataFrame) -> pd.DataFrame:
    """Fix mixed-type columns that fastparquet can't handle."""
    out = df.copy()
    for col in out.columns:
        if out[col].dtype == object:
            # Convert object columns to string, handling NaN
            out[col] = out[col].astype(str).replace("nan", pd.NA).replace("None", pd.NA)
    return out


def _load_or_fetch(name: str, fetch_fn, force_refresh: bool = False) -> pd.DataFrame:
    """Load from cache if exists, otherwise fetch and save."""
    path = _cache_path(name)
    if path.exists() and not force_refresh:
        print(f"Loading cached {name} from {path}")
        return pd.read_parquet(path, engine="fastparquet")

    print(f"Fetching {name}...")
    df = fetch_fn()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    sanitized = _sanitize_for_parquet(df)
    sanitized.to_parquet(path, engine="fastparquet", index=False)
    print(f"Saved {name} ({df.shape[0]:,} rows, {df.shape[1]} cols) to {path}")
    return df


def load_weekly_stats(force_refresh: bool = False) -> pd.DataFrame:
    return _load_or_fetch(
        "weekly_stats",
        lambda: nfl.import_weekly_data(YEARS),
        force_refresh,
    )


def load_rosters(force_refresh: bool = False) -> pd.DataFrame:
    return _load_or_fetch(
        "rosters",
        lambda: nfl.import_seasonal_rosters(YEARS),
        force_refresh,
    )


def load_contracts(force_refresh: bool = False) -> pd.DataFrame:
    return _load_or_fetch(
        "contracts",
        lambda: nfl.import_contracts(),
        force_refresh,
    )


def load_snap_counts(force_refresh: bool = False) -> pd.DataFrame:
    return _load_or_fetch(
        "snap_counts",
        lambda: nfl.import_snap_counts(YEARS),
        force_refresh,
    )


def load_players(force_refresh: bool = False) -> pd.DataFrame:
    return _load_or_fetch(
        "players",
        lambda: nfl.import_players(),
        force_refresh,
    )


def load_ids(force_refresh: bool = False) -> pd.DataFrame:
    return _load_or_fetch(
        "ids",
        lambda: nfl.import_ids(),
        force_refresh,
    )


def load_pfr_stats(stat_type: str, force_refresh: bool = False) -> pd.DataFrame:
    """Load PFR seasonal stats. stat_type: 'pass', 'rush', 'rec', 'def'."""
    return _load_or_fetch(
        f"pfr_{stat_type}",
        lambda: nfl.import_seasonal_pfr(stat_type, PFR_YEARS),
        force_refresh,
    )


def load_all(force_refresh: bool = False) -> dict:
    """Load all datasets, returning a dict keyed by name."""
    datasets = {}
    datasets["weekly_stats"] = load_weekly_stats(force_refresh)
    datasets["rosters"] = load_rosters(force_refresh)
    datasets["contracts"] = load_contracts(force_refresh)
    datasets["snap_counts"] = load_snap_counts(force_refresh)
    datasets["players"] = load_players(force_refresh)
    datasets["ids"] = load_ids(force_refresh)
    for stat_type in ["pass", "rush", "rec", "def"]:
        datasets[f"pfr_{stat_type}"] = load_pfr_stats(stat_type, force_refresh)
    return datasets
