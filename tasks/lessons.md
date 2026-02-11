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

## Publishing Workflow (`/publish` skill)

### Medium Import — Errors & Fixes (2026-02-10)

**Error #1: Inefficient navigation**
- ❌ Navigated to `https://medium.com/new-story` first
- ❌ Tried clicking "..." menu and searching for "import" feature
- ❌ Wasted 3 tool calls on wrong page
- ✅ **Fix:** Go directly to `https://medium.com/p/import` — this is the dedicated import page

**Error #2: Form input method**
- ❌ Tried using `form_input` tool on URL field (failed - element was a DIV)
- ✅ **Fix:** Use `computer(action="left_click")` + `computer(action="type")` for Medium's custom input fields

**Error #3: Overcomplicated browser automation**
- ❌ Should have known Medium's import URL structure from documentation/previous experience
- ✅ **Fix:** Document common Medium URLs in skill README:
  - Import page: `https://medium.com/p/import`
  - New story: `https://medium.com/new-story`
  - Draft editor: `https://medium.com/p/{draft_id}/edit`

### Workflow Improvements

**What worked well:**
- ✅ GEO optimization workflow (Phase 1-5) executed perfectly
- ✅ HTML export with proper Medium-compatible styling
- ✅ Git commit/push automation with auth refresh fallback
- ✅ Browser automation eventually succeeded despite navigation inefficiency

**Should update:**
- Update `medium_automation.py` to use direct import URL: `https://medium.com/p/import`
- Add URL constants to avoid hardcoding and navigation guesswork
- Add fallback: if `form_input` fails on Medium fields, auto-retry with click+type pattern
- Consider adding a "Medium Import Troubleshooting" section to skill README

**Key lesson:** When browser automating known services (Medium, GitHub, etc.), use direct URLs for specific actions rather than navigating through menus. Saves 2-3 tool calls per workflow.
