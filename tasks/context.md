# NFL Stats vs Salary Analysis - Session Context

## Last Updated: 2026-02-13

## Current State
- **Four articles complete:** Player Value, Draft ROI, Running Back Economics, Tight End Market Inefficiency
- Original article: Published to Medium, GitHub Pages enabled
- Draft ROI article: In Medium draft (pending final publication)
- **TE Market Inefficiency article:** Scheduled for Medium (Feb 20, 7:03 PM PST)
  - GEO score: 97/100 (A) — excellent LLM discoverability
  - 5 tags added, SEO description complete
- **RB Economics article: READY FOR RE-IMPORT WITH TABLE FIX**
  - GEO score: 95/100 (A+)
  - **Tables fixed:** All 5 data tables converted to PNG images for Medium compatibility
  - New HTML export: `rb_economics_20260213_1240.html` (unique timestamp)
  - **Pending:** Re-import to Medium and schedule to 2/24/2026
- 9,041 player-seasons (original) + 3,657 (draft ROI) + 1,249 RB seasons + 1,063 TE seasons analyzed
- GitHub repo: `ghighcove/nfl-salary-analysis` — public, GitHub Pages enabled
- **Shared library**: Uses `nfl-data-core` library from separate repo

## Active Work
- **COMPLETED: RB Economics table fix for Medium compatibility**
  - Generated 5 PNG table images using matplotlib
  - Updated markdown to reference PNG images (not markdown tables)
  - Created new timestamped HTML export (20260213_1240)
  - Committed and pushed to GitHub
  - Updated publishing metadata
  - **Reason:** Medium doesn't render HTML `<table>` tags well — PNG images ensure proper formatting

## Key Design Decisions

### Medium Table Handling — CRITICAL FIX APPLIED
**Problem:** Medium strips or mangles HTML `<table>` tags, causing tables to run together or misalign.

**Solution (PERMANENT RULE):**
- **Always convert tables to PNG images** for Medium articles
- Use matplotlib to generate clean, professional table visualizations
- Style: White background, dark header (white text), alternating row colors, 300 DPI
- Filename pattern: `table_{n}_{description}.png`
- Wrap images in `<p>` tags: `<p><img alt="..." src="..." /></p>`
- Descriptive alt text: "Table visualization showing [detailed table content summary]"

**This rule is documented in:**
- Global `~/.claude/CLAUDE.md`
- Project `CLAUDE.md`
- `G:\ai\medium-publishing-standards\STANDARDS.md`

### Medium Import Automation — CRITICAL UPDATES
**Unique Filename Generation (MANDATORY):**
- Medium caches imported URLs by filename aggressively
- **Solution:** Always generate unique timestamped filename for each import
- **Format:** `{article_name}_{YYYYMMDD}_{HHMM}.html`
- **Result:** Bypasses Medium cache, enables immediate re-imports after fixes

**Working Browser Automation Flow:**
1. Navigate to `https://medium.com/me/stories`
2. Click "Import a story" button
3. Paste GitHub Pages URL (unique filename)
4. Click "Import" button
5. Wait for import completion
6. Add tags via publish dialog
7. Add SEO description via story settings
8. Schedule publication date

**Image Format (VERIFIED WORKING):**
- Wrap images in `<p>` tags: `<p><img src="..." alt="..." /></p>`
- Use raw.githubusercontent.com URLs for images within content
- Table images (PNG) import perfectly when cache is bypassed

### Article Production Strategy
- **Pipeline focus**: 20 articles across 3 series (10 position, 8 team, 2 contract)
- **Quality standard**: 95+ GEO score (mandatory for portfolio visibility)
- **Automation:** `/publish` skill handles full pipeline (GEO → HTML → Git → Medium import)
- **Table handling:** Always convert to PNG for Medium (permanent rule)

### Article Analysis
- **Value Score**: `performance_zscore - salary_zscore` within position groups
- **Salary normalization**: `apy_cap_pct` (% of salary cap) for cross-year comparison
- **Minimum threshold**: 100 snaps/season for inclusion

## Recent Changes (this session)

### RB Economics Table Fix — COMPLETE
**Files created:**
- `article/images/rb_economics/table_1_draft_round_comparison.png`
- `article/images/rb_economics/table_2_career_arc.png`
- `article/images/rb_economics/table_3_top_bargains.png`
- `article/images/rb_economics/table_4_top_busts.png`
- `article/images/rb_economics/table_5_replaceability.png`
- `article/rb_economics_20260213_1240.html` (new timestamped HTML export)
- `generate_table_images.py` (utility script)
- `export_rb_economics_html.py` (utility script)

**Files modified:**
- `article/rb_economics_medium_draft.md` — Replaced markdown tables with PNG image references
- `article/MEDIUM_PUBLISH_INFO_rb_economics.md` — Updated metadata for table fix

**Git commits:**
1. `fix: Convert RB Economics tables to PNG for Medium compatibility` (commit e32ef3c)
   - Generated 5 PNG table images
   - Updated markdown with image references
   - Created timestamped HTML export
2. `docs: Update RB Economics publishing metadata for table fix` (commit 9607e8c)
   - Updated GitHub Pages URL to new timestamped version
   - Documented table PNG conversion
   - Updated image count (11 total: 6 charts + 5 table PNGs)

**Implementation details:**
- Used matplotlib to create clean table visualizations
- Style: Dark header (#2C3E50) with white text, alternating row colors, 12pt font, 300 DPI
- Fixed Unicode encoding issue on Windows (replaced ✓ with [OK] in print statements)
- All changes committed and pushed to GitHub

### Uncommitted Files (Outstanding)
- `.claude/settings.local.json` (modified)
- `README.md` (modified)
- `article/MEDIUM_PUBLISH_INFO_te_market_inefficiency.md` (modified)
- `src/__init__.py` (modified)
- `tasks/context.md` (this file — modified)
- `VERSION` (untracked)
- **Total:** 5 modified, 1 untracked

## Blockers / Open Questions
- **No blockers.** RB Economics article ready for re-import with table fix.
- TE article scheduled for Feb 20, 7:03 PM PST
- Table-to-PNG workflow validated and documented

## Next Steps
1. **User: Re-import RB Economics article to Medium** (5-10 min)
   - Wait 1-2 minutes for GitHub Pages to update
   - Go to Medium → New Story → Import a story
   - Paste GitHub Pages URL: `https://ghighcove.github.io/nfl-salary-analysis/article/rb_economics_20260213_1240.html`
   - Verify all 11 images load (6 charts + 5 table PNGs)
   - Verify tables display as images (not HTML tables)
   - Add tags and SEO description (metadata file has details)
   - Delete old draft with HTML tables
   - Schedule to Feb 24, 2026

2. **Commit remaining uncommitted files** (5 min)
   - Review modified files (5 modified, 1 untracked)
   - Commit message: "docs: Update session context and metadata"
   - Push to GitHub

3. **Start Article #5: Next position deep dive** (Future session)
   - Options: QB Value Deep Dive, WR Value Windows, OL analysis
   - Continue through pipeline (PROJECT_PIPELINE.md)
   - **Always apply table-to-PNG rule** for any Medium articles

## Environment
- Platform: Windows (win32), Python 3.8.2 (32-bit)
- Working directory: G:\ai\nfl
- Key packages: nfl-data-py, fastparquet 0.7.2, pandas 2.0.3, plotly, markdown 3.4.3, matplotlib
- GitHub repo: ghighcove/nfl-salary-analysis (public, GitHub Pages enabled)
- Browser automation: claude-in-chrome MCP server (for Medium import)

## Quick Reference
- **Project CLAUDE.md**: `G:\ai\nfl\CLAUDE.md`
- **Publishing Standards**: `G:\ai\medium-publishing-standards\STANDARDS.md`
- **Project Pipeline**: `G:\ai\nfl\PROJECT_PIPELINE.md` (20-article roadmap)
- **Git repo**: https://github.com/ghighcove/nfl-salary-analysis (branch: master)
- **Lessons learned**: `tasks/lessons.md`
- **Session context**: `tasks/context.md`

### Article URLs
**RB Economics (Article #3):**
- **New GitHub Pages URL (with table fix):** https://ghighcove.github.io/nfl-salary-analysis/article/rb_economics_20260213_1240.html
- Old URL (deprecated): ~~https://ghighcove.github.io/nfl-salary-analysis/article/rb_economics_20260211_1825.html~~
- Publishing info: `article/MEDIUM_PUBLISH_INFO_rb_economics.md`
- GEO score: 95/100 (A+)
- Status: Ready for re-import with table fix (11 images: 6 charts + 5 table PNGs)

**TE Market Inefficiency (Article #4):**
- Medium: Scheduled for Feb 20, 7:03 PM PST
- Publishing info: `article/MEDIUM_PUBLISH_INFO_te_market_inefficiency.md`
- GEO score: 97/100 (A)
- Status: Complete and scheduled

**Draft ROI (Article #2):**
- Medium draft: https://medium.com/p/f2cdfa739f9e/edit
- GEO score: 99/100 (A+)
- Status: Pending final publication

**Original Player Value (Article #1):**
- GitHub Pages: https://ghighcove.github.io/nfl-salary-analysis/article/medium_ready.html
- Status: Published

### Pipeline Status
- **Completed:** 4 of 20 articles (Player Value, Draft ROI, RB Economics, TE Market Inefficiency)
- **In progress:** Finalizing articles #2 and #3 for publication
- **Next:** QB Value Deep Dive or WR Value Windows
- **Target:** 5-10 articles in 2-3 months
- **New rule applied:** Tables → PNG images for all Medium articles
