# NFL Player Stats vs. Salary Analysis

## Project Overview
Jupyter Notebook project analyzing NFL player performance statistics against salary data (2015-2024). Surfaces outliers — players who dramatically outperform or underperform their salary.

## Architecture
- `src/` — Reusable Python modules (data_loader, cleaning, value_score, viz)
- `notebooks/` — Sequential notebooks (01-04) that build on each other
- `data/` — Cached parquet files (gitignored)

## Key Conventions
- Salary is normalized as % of salary cap (`apy_cap_pct`) for cross-year comparison
- Primary join key: `gsis_id` (called `player_id` in weekly stats)
- Minimum 100 snaps/season threshold for inclusion
- Position groups: QB, RB, WR, TE, OL, DL, LB, DB, K, P
- Value Score = composite_performance_zscore - salary_cap_pct_zscore (positive = bargain)

## Data Sources
All data from `nfl_data_py` library. Cached as parquet in `data/`.

## Running
1. `pip install -r requirements.txt`
2. Run notebooks in order: 01 → 02 → 03 → 04
3. Each notebook saves outputs that the next one reads
