"""Data cleaning, merging, and position classification."""

import pandas as pd
import numpy as np


# Position group mapping — maps raw positions to analysis groups
POSITION_GROUP_MAP = {
    # Offense
    "QB": "QB",
    "RB": "RB", "FB": "RB", "HB": "RB",
    "WR": "WR",
    "TE": "TE",
    "T": "OL", "OT": "OL", "G": "OL", "OG": "OL", "C": "OL", "OL": "OL", "LS": "OL",
    # Defense
    "DE": "DL", "DT": "DL", "NT": "DL", "DL": "DL",
    "LB": "LB", "ILB": "LB", "OLB": "LB", "MLB": "LB", "EDGE": "DL",
    "CB": "DB", "S": "DB", "SS": "DB", "FS": "DB", "DB": "DB",
    # Special teams
    "K": "K", "PK": "K",
    "P": "P",
}

# Minimum snaps per season to include a player
MIN_SNAPS = 100


def classify_position(pos: str) -> str:
    """Map raw position string to analysis group."""
    if pd.isna(pos):
        return "UNK"
    return POSITION_GROUP_MAP.get(pos.strip().upper(), "UNK")


def aggregate_weekly_to_seasonal(weekly: pd.DataFrame) -> pd.DataFrame:
    """Aggregate weekly player stats to season totals."""
    # Only regular season + postseason
    weekly = weekly[weekly["season_type"].isin(["REG", "POST"])].copy()

    # Numeric columns to sum
    sum_cols = [
        "completions", "attempts", "passing_yards", "passing_tds", "interceptions",
        "sacks", "sack_fumbles", "sack_fumbles_lost",
        "passing_first_downs", "passing_2pt_conversions",
        "carries", "rushing_yards", "rushing_tds", "rushing_fumbles",
        "rushing_fumbles_lost", "rushing_first_downs", "rushing_2pt_conversions",
        "receptions", "targets", "receiving_yards", "receiving_tds",
        "receiving_fumbles", "receiving_fumbles_lost", "receiving_first_downs",
        "receiving_2pt_conversions",
        "special_teams_tds", "fantasy_points", "fantasy_points_ppr",
    ]
    # Keep only columns that exist
    sum_cols = [c for c in sum_cols if c in weekly.columns]

    # EPA columns to sum (they're additive)
    epa_cols = [c for c in weekly.columns if c.endswith("_epa")]
    sum_cols.extend(epa_cols)

    # Group by player + season
    grouped = weekly.groupby(["player_id", "season"]).agg(
        player_name=("player_display_name", "first"),
        position=("position", "first"),
        position_group=("position_group", "first"),
        recent_team=("recent_team", "last"),
        games_played=("week", "count"),
        **{col: (col, "sum") for col in sum_cols},
    ).reset_index()

    return grouped


def compute_rate_stats(seasonal: pd.DataFrame) -> pd.DataFrame:
    """Add computed rate stats to seasonal aggregates."""
    df = seasonal.copy()

    # Passing
    df["completion_pct"] = np.where(
        df["attempts"] > 0, df["completions"] / df["attempts"] * 100, np.nan
    )
    df["yards_per_attempt"] = np.where(
        df["attempts"] > 0, df["passing_yards"] / df["attempts"], np.nan
    )
    df["td_rate"] = np.where(
        df["attempts"] > 0, df["passing_tds"] / df["attempts"] * 100, np.nan
    )
    df["int_rate"] = np.where(
        df["attempts"] > 0, df["interceptions"] / df["attempts"] * 100, np.nan
    )
    # Simplified passer rating (NFL formula)
    df["passer_rating"] = _passer_rating(df)

    # Rushing
    df["yards_per_carry"] = np.where(
        df["carries"] > 0, df["rushing_yards"] / df["carries"], np.nan
    )

    # Receiving
    df["catch_rate"] = np.where(
        df["targets"] > 0, df["receptions"] / df["targets"] * 100, np.nan
    )
    df["yards_per_reception"] = np.where(
        df["receptions"] > 0, df["receiving_yards"] / df["receptions"], np.nan
    )

    return df


def _passer_rating(df: pd.DataFrame) -> pd.Series:
    """Calculate NFL passer rating."""
    att = df["attempts"].replace(0, np.nan)
    a = ((df["completions"] / att * 100) - 30) / 20
    b = ((df["passing_tds"] / att * 100) - 0) / 5  # fixed: no subtract
    c = (2.375 - (df["interceptions"] / att * 100 * 0.25))  # inverted
    d = ((df["passing_yards"] / att) - 3) / 4

    # Clip each component 0-2.375
    a = a.clip(0, 2.375)
    b = b.clip(0, 2.375)
    c = c.clip(0, 2.375)
    d = d.clip(0, 2.375)

    rating = ((a + b + c + d) / 6) * 100
    return rating


def build_pfr_id_map(players: pd.DataFrame) -> pd.DataFrame:
    """Create a gsis_id <-> pfr_id crosswalk from players table."""
    crosswalk = players[["gsis_id", "pfr_id"]].dropna(subset=["gsis_id", "pfr_id"])
    crosswalk = crosswalk.drop_duplicates(subset=["pfr_id"])
    return crosswalk


def aggregate_snap_counts(snaps: pd.DataFrame, pfr_to_gsis: pd.DataFrame) -> pd.DataFrame:
    """Aggregate snap counts to seasonal totals and map to gsis_id."""
    seasonal_snaps = snaps.groupby(["pfr_player_id", "season"]).agg(
        total_offense_snaps=("offense_snaps", "sum"),
        total_defense_snaps=("defense_snaps", "sum"),
        total_st_snaps=("st_snaps", "sum"),
        snap_games=("game_id", "count"),
    ).reset_index()

    seasonal_snaps["total_snaps"] = (
        seasonal_snaps["total_offense_snaps"]
        + seasonal_snaps["total_defense_snaps"]
        + seasonal_snaps["total_st_snaps"]
    )

    # Map pfr_id to gsis_id
    seasonal_snaps = seasonal_snaps.merge(
        pfr_to_gsis, left_on="pfr_player_id", right_on="pfr_id", how="left"
    )
    return seasonal_snaps


def prepare_contracts(contracts: pd.DataFrame) -> pd.DataFrame:
    """Clean contracts data and extract per-season salary info."""
    df = contracts.copy()

    # Keep rows with valid gsis_id and salary info
    df = df.dropna(subset=["gsis_id"])
    df = df[df["apy_cap_pct"].notna() & (df["apy_cap_pct"] > 0)]

    # De-duplicate: keep the most recent contract per player (highest apy_cap_pct if ties)
    # We'll match contracts to seasons by checking if the season falls within the contract window
    df["year_signed"] = df["year_signed"].astype(int)
    df["contract_end_year"] = df["year_signed"] + df["years"].fillna(1).astype(int) - 1

    # Explode to one row per season the contract covers
    rows = []
    for _, row in df.iterrows():
        for season in range(row["year_signed"], row["contract_end_year"] + 1):
            new_row = row.copy()
            new_row["season"] = season
            rows.append(new_row)

    if not rows:
        return pd.DataFrame()

    expanded = pd.DataFrame(rows)

    # Keep only seasons in our range
    expanded = expanded[expanded["season"].isin(range(2015, 2025))]

    # If multiple contracts cover the same season, keep the one signed most recently
    expanded = expanded.sort_values("year_signed", ascending=False)
    expanded = expanded.drop_duplicates(subset=["gsis_id", "season"], keep="first")

    # Flag contract type
    expanded["contract_type"] = np.where(
        expanded["years"].fillna(1) <= 4,
        np.where(expanded["apy_cap_pct"] < 0.02, "rookie", "veteran"),
        "veteran",
    )

    keep_cols = [
        "gsis_id", "season", "player", "position", "team",
        "apy_cap_pct", "apy", "value", "guaranteed", "years",
        "year_signed", "contract_type",
    ]
    keep_cols = [c for c in keep_cols if c in expanded.columns]
    return expanded[keep_cols].rename(columns={
        "player": "contract_player_name",
        "position": "contract_position",
        "team": "contract_team",
    })


def build_defensive_players(
    pfr_def: pd.DataFrame,
    pfr_to_gsis: pd.DataFrame,
    players: pd.DataFrame,
) -> pd.DataFrame:
    """Build defensive player-season records from PFR data (not in weekly stats)."""
    if pfr_def is None or pfr_to_gsis is None:
        return pd.DataFrame()

    df = pfr_def.merge(pfr_to_gsis, on="pfr_id", how="left")
    df = df.dropna(subset=["gsis_id"])

    # Map PFR def columns to friendly names
    pfr_col_map = {
        "sk": "def_sacks", "int": "def_ints", "comb": "def_tackles",
        "prss": "def_pressures", "qbkd": "def_qb_hits",
        "m_tkl": "def_missed_tackles", "bltz": "def_blitzes",
    }
    for src, dst in pfr_col_map.items():
        if src in df.columns:
            df[dst] = pd.to_numeric(df[src], errors="coerce")

    # Get player names and positions from players table
    player_info = players[["gsis_id", "display_name", "position"]].dropna(subset=["gsis_id"])
    player_info = player_info.drop_duplicates(subset=["gsis_id"])

    df = df.merge(player_info, on="gsis_id", how="left")

    # Use PFR 'pos' if available, fallback to players table
    if "pos" in df.columns:
        df["position"] = df["pos"].fillna(df.get("position", ""))
    df["player_name"] = df.get("player", df.get("display_name", "Unknown"))

    # Build standardized records
    records = df[["gsis_id", "season", "player_name", "position"]].copy()
    records = records.rename(columns={"gsis_id": "player_id"})
    records["position_group"] = records["position"].apply(classify_position)
    records["games_played"] = pd.to_numeric(df.get("g", 0), errors="coerce").fillna(0).astype(int)

    # Attach def stats
    for dst in pfr_col_map.values():
        if dst in df.columns:
            records[dst] = df[dst].values

    # Get team from PFR
    if "tm" in df.columns:
        records["recent_team"] = df["tm"]

    return records


def merge_all(
    seasonal_stats: pd.DataFrame,
    contracts: pd.DataFrame,
    snap_counts: pd.DataFrame,
    pfr_def: pd.DataFrame = None,
    pfr_to_gsis: pd.DataFrame = None,
    players: pd.DataFrame = None,
) -> pd.DataFrame:
    """Merge seasonal stats with contracts, snap counts, and defensive stats."""
    df = seasonal_stats.copy()

    # Classify positions
    df["pos_group"] = df["position"].apply(classify_position)

    # Build defensive player records and append them
    if pfr_def is not None and pfr_to_gsis is not None and players is not None:
        def_players = build_defensive_players(pfr_def, pfr_to_gsis, players)
        if len(def_players) > 0:
            # Only add defensive players NOT already in the stats (by player_id + season)
            existing_keys = set(zip(df["player_id"], df["season"]))
            mask = [
                (pid, s) not in existing_keys
                for pid, s in zip(def_players["player_id"], def_players["season"])
            ]
            new_def = def_players[mask].copy()
            # Ensure columns align (add missing cols as NaN)
            for col in df.columns:
                if col not in new_def.columns:
                    new_def[col] = np.nan
            new_def = new_def[df.columns.tolist() + [c for c in new_def.columns if c not in df.columns]]
            df = pd.concat([df, new_def], ignore_index=True, sort=False)
            # Re-classify positions for new rows
            df["pos_group"] = df["position"].apply(classify_position)

    # Merge contracts
    df = df.merge(
        contracts,
        left_on=["player_id", "season"],
        right_on=["gsis_id", "season"],
        how="left",
    )

    # Merge snap counts
    snap_cols = ["gsis_id", "season", "total_offense_snaps", "total_defense_snaps",
                 "total_st_snaps", "total_snaps", "snap_games"]
    snap_cols = [c for c in snap_cols if c in snap_counts.columns]
    df = df.merge(
        snap_counts[snap_cols],
        left_on=["player_id", "season"],
        right_on=["gsis_id", "season"],
        how="left",
        suffixes=("", "_snap"),
    )

    # For offensive players, also merge PFR defensive stats (some LBs/DBs have offensive stats too)
    if pfr_def is not None and pfr_to_gsis is not None:
        pfr_def_with_gsis = pfr_def.merge(pfr_to_gsis, on="pfr_id", how="left")
        def_merge_cols = ["gsis_id", "season"]
        pfr_col_map = {
            "sk": "def_sacks", "int": "def_ints", "comb": "def_tackles",
            "prss": "def_pressures", "qbkd": "def_qb_hits",
            "m_tkl": "def_missed_tackles", "bltz": "def_blitzes",
        }
        for src, dst in pfr_col_map.items():
            if src in pfr_def_with_gsis.columns:
                if dst not in df.columns:
                    pfr_def_with_gsis[dst] = pd.to_numeric(pfr_def_with_gsis[src], errors="coerce")
                    def_merge_cols.append(dst)

        if len(def_merge_cols) > 2:
            pfr_def_with_gsis = pfr_def_with_gsis[def_merge_cols].dropna(subset=["gsis_id"])
            # Only merge for rows that don't already have def stats
            needs_def = df["def_sacks"].isna() if "def_sacks" in df.columns else pd.Series(True, index=df.index)
            df_needs = df[needs_def]
            df_has = df[~needs_def]

            if len(df_needs) > 0:
                df_needs = df_needs.drop(
                    columns=[c for c in def_merge_cols if c != "gsis_id" and c != "season" and c in df_needs.columns],
                    errors="ignore",
                )
                df_needs = df_needs.merge(
                    pfr_def_with_gsis,
                    left_on=["player_id", "season"],
                    right_on=["gsis_id", "season"],
                    how="left",
                    suffixes=("", "_def"),
                )
                df = pd.concat([df_has, df_needs], ignore_index=True, sort=False)

    # Apply minimum snap threshold
    df["has_salary"] = df["apy_cap_pct"].notna()
    df["meets_snap_threshold"] = df["total_snaps"].fillna(0) >= MIN_SNAPS

    return df


def get_analysis_ready(merged: pd.DataFrame) -> pd.DataFrame:
    """Filter to players with both salary data and minimum snaps."""
    df = merged[merged["has_salary"] & merged["meets_snap_threshold"]].copy()
    # Drop unknown position groups
    df = df[df["pos_group"] != "UNK"]
    return df
