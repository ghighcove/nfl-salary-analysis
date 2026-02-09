# NFL Stats vs Salary Analysis - Session Context

## Last Updated: 2026-02-08

## Current State
- **Project PUBLISHED.** Article successfully imported to Medium. Repo public on GitHub with Pages enabled.
- 9,041 player-seasons scored across 3,211 unique players (2015-2024)
- All position groups covered: QB, WR, RB, TE, OL, DL, LB, DB, K
- 7 chart PNGs in `article/images/` (scatter grid, salary boxplot, top bargains, top overpaid, rookie vs veteran, Mahomes trajectory, team heatmap)
- 4 notebooks run end-to-end successfully
- Data cached as 12 parquet files in `data/` (~25 MB total)
- GitHub repo: `ghighcove/nfl-salary-analysis` — **public**, GitHub Pages enabled
- GitHub Pages URL: https://ghighcove.github.io/nfl-salary-analysis/
- Medium import URL: https://ghighcove.github.io/nfl-salary-analysis/article/medium_ready.html

## Active Work
- **Done.** Article published to Medium via GitHub Pages import.

## Key Design Decisions
- **Parquet engine**: `fastparquet==0.7.2` (not pyarrow — pyarrow won't compile on 32-bit Windows Python 3.8)
- **Defensive data**: Built from PFR `import_seasonal_pfr('def')` (2018+), not from weekly stats (which are offense-only). `build_defensive_players()` in cleaning.py creates defensive player-season records and appends them.
- **ID crosswalk**: `import_players()` bridges `pfr_id` ↔ `gsis_id` for snap counts and PFR data
- **Contract expansion**: Contracts exploded to one row per season covered (year_signed to year_signed + years - 1), deduped by most recent signing
- **Salary normalization**: `apy_cap_pct` from Over The Cap (already cap-normalized)
- **Value Score**: `performance_zscore - salary_zscore` within position groups. Positive = bargain, negative = overpaid
- **Seaborn**: Upgraded to 0.13.2 (0.10.1 incompatible with numpy 1.24+)
- **DataFrame sanitization**: Object columns converted to string before parquet save (fastparquet chokes on mixed types)
- **Medium import method**: GitHub Pages (not raw.githubusercontent.com) — raw URLs serve `text/plain` which Medium rejects. See superbowl project's `tasks/lessons.md` for full recipe.
- **Image URLs**: `raw.githubusercontent.com` URLs in both `.md` and `.html` — these work fine for `<img>` tags; the content-type issue only affects Medium's top-level import URL.

## Recent Changes (this session)
- Updated `article/medium_draft.md` — replaced 7 relative image paths with `raw.githubusercontent.com` URLs
- Created `article/medium_ready.html` — self-contained HTML with inline CSS, modeled on superbowl project pattern
- Made repo public (`gh repo edit --visibility public --accept-visibility-change-consequences`)
- Enabled GitHub Pages from master branch root (`gh api repos/.../pages -X POST`)
- Article imported to Medium via `medium.com/p/import` using GitHub Pages URL
- **GEO Audit applied (2026-02-09)**: Ran `seo-for-llms` skill audit. Score improved from 68/100 (C) to ~79/100 (B). Changes: promoted headings to H2, rewrote 9 headings to be descriptive, added Key Findings summary block, added BLUF intro sentence, defined PFR/EPA acronyms, added external source links. Applied to both `medium_draft.md` and `medium_ready.html`. Re-import to Medium needed to reflect changes.

## Blockers / Open Questions
- **No blockers.** Project is published.
- OL stats remain limited (snap count + games played as proxy)
- Punters excluded from scoring (P position has 99 rows but no scoring weights)
- Mid-season trades create duplicate entries (e.g., Marshon Lattimore "2TM" in PFR)
- K position only has 12 player-seasons with salary data — too few for meaningful analysis
- Aaron Donald shows as "overpaid" in 2023 because he retired mid-year (low stats, high cap hit)

## Next Steps
1. Re-import updated HTML to Medium: `https://ghighcove.github.io/nfl-salary-analysis/article/medium_ready.html`
2. Optional: Add tags and preview image in Medium editor
3. Consider deduplicating mid-season trade entries ("2TM" teams)
4. Add interactive dropdown widget (ipywidgets) for player selection in notebook 04
5. Consider play-by-play aggregation for punter stats

## Environment
- Platform: Windows (win32), Python 3.8.2 (32-bit)
- Working directory: G:\ai\nfl
- Key packages: nfl-data-py 0.3.3, fastparquet 0.7.2, pandas 2.0.3, seaborn 0.13.2, matplotlib 3.7.5, plotly 6.5.2, scikit-learn
- No pyarrow (32-bit Windows incompatible) — all parquet I/O uses `engine='fastparquet'`
- GitHub repo: ghighcove/nfl-salary-analysis (public, GitHub Pages enabled)
- GitHub Pages URL: https://ghighcove.github.io/nfl-salary-analysis/
