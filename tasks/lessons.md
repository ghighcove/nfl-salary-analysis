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

---

## CRITICAL: Medium Import Caching Issue (2026-02-11)

### Problem
**Medium aggressively caches imported article URLs by filename.** When we fixed issues with the TE article, Medium continued serving the OLD cached version, making it appear that fixes weren't working.

### Symptoms
- Table images showed as garbled OCR text in Medium
- Multiple "fixes" (base64 embedding, URL changes, file renaming) all appeared to fail
- Same garbled text persisted across dozens of import attempts over 2+ hours
- Version markers added to title didn't appear (proof of caching)

### Root Cause Discovery
After creating a file with a **completely new filename** (`te_market_feb11_2026.html`), the import worked immediately. The content was identical, only the filename changed.

**Conclusion:** Medium caches by GitHub Pages URL path. Updating file content doesn't bust the cache. Only a new filename works.

### Solution (MANDATORY for /publish automation)

**Always generate unique filename for each Medium import:**

```python
import hashlib
from datetime import datetime

# Generate unique filename
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
content_hash = hashlib.md5(html_content.encode()).hexdigest()[:8]
filename = f"{article_name}_{timestamp}_{content_hash}.html"
```

✅ **Good:** `te_market_20260211_1630_a3f2b1c4.html`
❌ **Bad:** Reusing `te_market_inefficiency_medium_ready.html` after updates

### What Actually Works for Medium (Confirmed)

**Table Images (RECOMMENDED):**
- ✅ PNG images with `raw.githubusercontent.com` URLs
- ✅ Images wrapped in `<p>` tags: `<p><img alt="..." src="..." /></p>`
- ✅ Alt text: "Table visualization showing [detailed description]"
- ✅ Filenames like `table_1_draft_roi.png` work fine

**What We Wasted Time On (all due to caching, not actual issues):**
- ❌ Base64 data URI embedding (unnecessary - PNGs work)
- ❌ Testing GitHub Pages vs raw.githubusercontent URLs (both work)
- ❌ Renaming files from `table_*` to `data_*` (unnecessary)
- ❌ Converting tables to HTML text lists (works but less visual)

### Working Template (from draft_roi success)

```html
<p><img alt="Table visualization showing optimal draft strategy by position. QB: best in rounds 1-2 and 5, avoid 3-4 and 6. Color-coded green for recommended rounds, red for rounds to avoid."
        src="https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/images/analysis_name/table_1_description.png" /></p>
```

### Automation Requirements

**The `/publish` skill MUST:**
1. Generate **unique timestamped filename** for HTML export
2. Never reuse existing `*_medium_ready.html` filenames
3. Keep table images as PNGs (they work perfectly)
4. Use working image format: `<p><img>` with descriptive alt text
5. Commit new file to git with unique name
6. Return the unique GitHub Pages URL for Medium import

**File Naming Pattern:**
```
article/{article_name}_{YYYYMMDD}_{HHMM}.html
```

Example: `article/te_market_inefficiency_20260211_1630.html`

### Testing Protocol

When debugging Medium imports:
1. **Always create a NEW file** - never modify existing imported file
2. Add version marker to title to verify cache status
3. If import seems broken, try completely new filename first
4. Don't waste time on content fixes until cache is ruled out

### Success Metrics

- ✅ First article (draft_roi): Worked immediately with table images
- ✅ TE article (after cache fix): Worked immediately with table images
- ⏱️ Time wasted on false debugging: ~2 hours
- 💡 Lesson: Cache first, content second

---

**PROMOTE TO CLAUDE.md:** This caching issue is critical and must be encoded in the automated workflow permanently.
