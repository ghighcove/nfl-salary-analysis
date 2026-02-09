# NFL Stats vs Salary Analysis - Session Context

## Last Updated: 2026-02-08

## Current State
- **Project fully implemented and verified.** All 4 notebooks run end-to-end successfully.
- 9,041 player-seasons scored across 3,211 unique players (2015-2024)
- All position groups covered: QB, WR, RB, TE, OL, DL, LB, DB, K
- 7 visualization types working (interactive Plotly + static matplotlib/seaborn)
- Data cached as 12 parquet files in `data/` (~25 MB total)

## Active Work
- Implementation complete. Session wrapped up after full verification pass.

## Key Design Decisions
- **Parquet engine**: `fastparquet==0.7.2` (not pyarrow — pyarrow won't compile on 32-bit Windows Python 3.8)
- **Defensive data**: Built from PFR `import_seasonal_pfr('def')` (2018+), not from weekly stats (which are offense-only). `build_defensive_players()` in cleaning.py creates defensive player-season records and appends them.
- **ID crosswalk**: `import_players()` bridges `pfr_id` ↔ `gsis_id` for snap counts and PFR data
- **Contract expansion**: Contracts exploded to one row per season covered (year_signed to year_signed + years - 1), deduped by most recent signing
- **Salary normalization**: `apy_cap_pct` from Over The Cap (already cap-normalized)
- **Value Score**: `performance_zscore - salary_zscore` within position groups. Positive = bargain, negative = overpaid
- **Seaborn**: Upgraded to 0.13.2 (0.10.1 incompatible with numpy 1.24+)
- **DataFrame sanitization**: Object columns converted to string before parquet save (fastparquet chokes on mixed types)

## Recent Changes
- Created full project: `src/data_loader.py`, `src/cleaning.py`, `src/value_score.py`, `src/viz.py`
- Created 4 notebooks: `01_data_acquisition`, `02_data_cleaning`, `03_value_scoring`, `04_visualizations`
- Fixed defensive player coverage (was 15 DL → now 1,257 DL after PFR integration)
- Fixed seaborn/matplotlib/fastparquet compatibility issues for Python 3.8 32-bit Windows
- Saved `data/analysis_ready.parquet` and `data/scored.parquet` as intermediate outputs

## Blockers / Open Questions
- OL stats remain limited (snap count + games played as proxy)
- Punters excluded from scoring (P position has 99 rows but no scoring weights)
- Mid-season trades create duplicate entries (e.g., Marshon Lattimore "2TM" in PFR)
- K position only has 12 player-seasons with salary data — too few for meaningful analysis
- Aaron Donald shows as "overpaid" in 2023 because he retired mid-year (low stats, high cap hit)

## Next Steps
1. Consider deduplicating mid-season trade entries ("2TM" teams)
2. Add interactive dropdown widget (ipywidgets) for player selection in notebook 04
3. Consider play-by-play aggregation for punter stats
4. Potential: GitHub repo setup for version control

## Environment
- Platform: Windows (win32), Python 3.8.2 (32-bit)
- Working directory: G:\ai\nfl
- Key packages: nfl-data-py 0.3.3, fastparquet 0.7.2, pandas 2.0.3, seaborn 0.13.2, matplotlib 3.7.5, plotly 6.5.2, scikit-learn
- No pyarrow (32-bit Windows incompatible) — all parquet I/O uses `engine='fastparquet'`
- No git repo initialized yet
