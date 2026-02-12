# NFL Stats vs Salary Analysis - Session Context

## Last Updated: 2026-02-11

## Current State
- **Three articles complete:** Player Value, Draft ROI, Tight End Market Inefficiency
- Original article: Published to Medium, GitHub Pages enabled
- Draft ROI article: In Medium draft (pending final publication)
- **TE Market Inefficiency article: IMPORTED TO MEDIUM** (Draft ID: 535ee5028fc9)
  - GEO score: 97/100 (A) — excellent LLM discoverability
  - Successfully imported with unique timestamped filename
  - **5 tags added:** NFL Draft, NFL, Data Analysis, Sports Analytics, Football
  - **Pending:** Manual schedule adjustment (Feb 18, 4:09 PM PST) and SEO description
- **Medium caching issue RESOLVED** — Unique filename generation working
- `/publish` skill fully functional with automated Medium import
- 9,041 player-seasons (original) + 3,657 (draft ROI) + 1,063 TE seasons analyzed
- GitHub repo: `ghighcove/nfl-salary-analysis` — public, GitHub Pages enabled
- **Shared library**: Uses `nfl-data-core` library from separate repo

## Active Work
- **COMPLETED: TE Market Inefficiency article automation**
  - Fixed Medium caching bug (unique filename generation)
  - Automated Medium import with browser automation
  - Successfully imported article with all 11 images (6 charts + 5 tables)
  - All 5 tags added automatically
  - Article ready for manual scheduling and SEO description

## Key Design Decisions

### Medium Import Automation — CRITICAL UPDATES
**Unique Filename Generation (MANDATORY):**
- Medium caches imported URLs by filename aggressively
- **Solution:** Always generate unique timestamped filename for each import
- **Format:** `{article_name}_{YYYYMMDD}_{HHMM}_{hash}.html`
- **Implementation:** Updated `convert_to_html.py` with `generate_unique_filename()` function
- **Result:** Bypasses Medium cache, enables immediate re-imports after fixes

**Working Browser Automation Flow:**
1. Navigate directly to `https://medium.com/p/import`
2. Click URL input field
3. Type GitHub Pages URL (unique filename)
4. Click "Import" button
5. Wait for import completion
6. Add tags via typing + Enter (5 tags max)
7. Manual steps: Schedule date/time, add SEO description in settings

**Medium Date Picker Issue:**
- Automated clicks on calendar dates don't register reliably
- **Workaround:** User manually adjusts publication date after tag automation
- **SEO Description:** Added via story settings (... menu → Story settings → Advanced → SEO description)

**Image Format (VERIFIED WORKING):**
- Wrap images in `<p>` tags: `<p><img src="..." alt="..." /></p>`
- Use raw.githubusercontent.com URLs for images within content
- Table images import perfectly as PNGs when cache is bypassed

### Article Production Strategy
- **Pipeline focus**: 20 articles across 3 series (10 position, 8 team, 2 contract)
- **Quality standard**: 95+ GEO score (mandatory for portfolio visibility)
- **Automation:** `/publish` skill handles full pipeline (GEO → HTML → Git → Medium import)

### Article Analysis
- **Value Score**: `performance_zscore - salary_zscore` within position groups
- **Salary normalization**: `apy_cap_pct` (% of salary cap) for cross-year comparison
- **Minimum threshold**: 100 snaps/season for inclusion

## Recent Changes (this session)

### Medium Caching Fix — CRITICAL
**Problem discovered:**
- Medium caches imported article URLs by filename
- Updating file content doesn't bust cache
- Wasted 2+ hours debugging "broken" fixes that were actually cached

**Solution implemented:**
- Updated `convert_to_html.py` with unique filename generation
- Format: `{article_name}_{YYYYMMDD}_{HHMM}_{hash}.html`
- Example: `te_market_inefficiency_20260211_1730_36aad799.html`
- Uses MD5 hash of content for uniqueness

**Files modified:**
- `article/convert_to_html.py` — Added `generate_unique_filename()` function
- `tasks/lessons.md` — Documented caching issue with detailed troubleshooting
- `CLAUDE.md` — Added mandatory unique filename requirement

**Git commits:**
- 24c63e7: "feat: Add unique filename generation to bypass Medium cache"
- 52c6550: "feat: Add TE Market Inefficiency article with unique filename"

### TE Market Inefficiency Article
**Files created:**
- `article/te_market_inefficiency_20260211_1730_36aad799.html` — Unique timestamped HTML
- Successfully imported to Medium (Draft ID: 535ee5028fc9)

**Automation success:**
- ✅ Article import via GitHub Pages URL
- ✅ All 11 images imported correctly (6 charts + 5 tables)
- ✅ 5 tags added automatically (NFL Draft, NFL, Data Analysis, Sports Analytics, Football)
- ⏸️ Manual completion needed: Schedule date (Feb 18, 4:09 PM PST) and SEO description

**SEO description (ready to paste):**
```
Round 2 TEs deliver +0.582 value (highest ROI), while first-round picks have 60% bust rate. Sam LaPorta, George Kittle data analysis of 1,063 TE seasons (2015-2024).
```

### Uncommitted Files
- `.claude/settings.local.json` (1 file modified)

## Blockers / Open Questions
- **No blockers.** TE article successfully imported, automation working.
- **Minor:** Medium date picker doesn't respond to automated clicks (manual workaround works)

## Next Steps
1. **Complete TE article publication** (5-10 min manual)
   - Open Medium draft: https://medium.com/p/535ee5028fc9/edit
   - Click "Publish" → "Schedule for later"
   - Set date: Feb 18, 2026, 4:09 PM PST
   - Add SEO description in story settings (180 chars ready)
   - Publish/schedule

2. **Finish Draft ROI article** (30-60 min)
   - Open Medium draft (ID: f2cdfa739f9e)
   - Complete final publication steps

3. **Document automation workflow** (DONE in this session)
   - Updated lessons.md with caching fix
   - Updated CLAUDE.md with mandatory requirements
   - Automation now reliable and repeatable

4. **Start Article #4: Next position deep dive** (1 week)
   - Continue through pipeline (PROJECT_PIPELINE.md)

## Environment
- Platform: Windows (win32), Python 3.8.2 (32-bit)
- Working directory: G:\ai\nfl
- Key packages: nfl-data-py, fastparquet 0.7.2, pandas 2.0.3, plotly, markdown 3.4.3
- GitHub repo: ghighcove/nfl-salary-analysis (public, GitHub Pages enabled)
- Browser automation: claude-in-chrome MCP server (for Medium import)

## Quick Reference
- **Project CLAUDE.md**: `G:\ai\nfl\CLAUDE.md`
- **Project Pipeline**: `G:\ai\nfl\PROJECT_PIPELINE.md` (20-article roadmap)
- **Git repo**: https://github.com/ghighcove/nfl-salary-analysis (branch: master)
- **Lessons learned**: `tasks/lessons.md` (includes Medium caching fix)
- **Session context**: `tasks/context.md`

### Article URLs
**TE Market Inefficiency (Article #3):**
- Medium draft: https://medium.com/p/535ee5028fc9/edit
- GitHub Pages: https://ghighcove.github.io/nfl-salary-analysis/article/te_market_inefficiency_20260211_1730_36aad799.html
- Publishing info: `article/MEDIUM_PUBLISH_INFO_te_market_inefficiency.md`
- GEO score: 97/100 (A)
- Status: Imported, tags added, awaiting manual schedule + SEO description

**Draft ROI (Article #2):**
- Medium draft: https://medium.com/p/f2cdfa739f9e/edit
- GEO score: 99/100 (A+)
- Status: Pending final publication

**Original Player Value (Article #1):**
- GitHub Pages: https://ghighcove.github.io/nfl-salary-analysis/article/medium_ready.html
- Status: Published

### Pipeline Status
- **Completed:** 3 of 20 articles (Player Value, Draft ROI, TE Market Inefficiency)
- **In progress:** Finalizing articles #2 and #3 for publication
- **Target:** 5-10 articles in 2-3 months
