# NFL Analysis — Lessons Learned

## Environment
- Python 3.8 (32-bit) on Windows — pyarrow won't compile (requires 64-bit). Use `fastparquet==0.7.2` instead.
- Seaborn 0.10 is incompatible with numpy 1.24+ (`np.float` removed). Need seaborn >= 0.12.
- `fastparquet` chokes on mixed-type object columns. Sanitize DataFrames (convert object cols to string) before saving to parquet.

## Data
- `nfl_data_py.import_weekly_data()` only contains offensive stats. Defensive players only appear if they have offensive stats (fumble recovery TD, etc.).
- Real defensive data comes from `import_seasonal_pfr('def')` which is PFR-sourced and only available 2018+.
- Must build defensive player-season records from PFR data and append them to the offensive-focused weekly stats.
- `import_snap_counts()` uses `pfr_player_id` not `gsis_id` — need the `import_players()` crosswalk to bridge.
- Contract data needs to be "exploded" to one row per season the contract covers (year_signed through year_signed + years - 1).
- Mid-season trades create duplicate entries (e.g., "2TM" team codes in PFR).

## Scoring
- Z-score normalization within position groups works well for cross-position comparison.
- Value = performance_z - salary_z: positive = bargain, negative = overpaid.
- Rookie-deal stars (Nick Bosa pre-extension, Sam LaPorta) naturally surface as top bargains.
- Injured high-salary players (Joey Bosa, Marshon Lattimore) naturally surface as overpaid due to low stats.
