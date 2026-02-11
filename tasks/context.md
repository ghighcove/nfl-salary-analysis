# NFL Stats vs Salary Analysis - Session Context

## Last Updated: 2026-02-11

## Current State
- **Two articles complete:** Original player value analysis + Draft ROI analysis
- Original article: Published to Medium, GitHub Pages enabled
- **Draft ROI article: In Medium draft** (Draft ID: f2cdfa739f9e) — awaiting final publication
  - GEO score: 99/100 (A+) — near-perfect LLM discoverability
  - All optimizations applied, imported successfully
  - **Final step pending:** Reformat tables, add tags/SEO, publish
- **NEW: PROJECT_PIPELINE.md** — 20-article production roadmap created
- **NEW: Running Back Economics notebook** — Template ready for article #3
- `/publish` skill implemented and tested (GEO → HTML → Git → Medium automation)
- 9,041 player-seasons (original analysis) + 3,657 player-seasons (draft ROI analysis)
- All notebooks run end-to-end successfully
- Data cached as parquet files in `data/` directory
- GitHub repo: `ghighcove/nfl-salary-analysis` — **public**, GitHub Pages enabled
- **Shared library migration complete**: Uses `nfl-data-core` library from separate repo

## Active Work
- **COMPLETED: Project pipeline implementation** — Implemented full 20-article roadmap
  - Created `PROJECT_PIPELINE.md` with 3 article series (Position Deep Dives, Team Strategy, Contract Trends)
  - Added GEO optimization checklist (95+ score requirements)
  - Documented article production workflow (1-2 weeks per article)
  - Created `06_rb_economics.ipynb` template for next article
  - Updated README.md to reference pipeline
  - Committed and pushed to GitHub (commit: 3877e3a)

## Key Design Decisions

### Article Production Strategy
- **Pipeline focus**: 20 articles across 3 series (10 position, 8 team, 2 contract)
- **Production velocity**: 2-3 articles/month → 5-10 articles in 2-3 months
- **Quality standard**: 95+ GEO score (mandatory for portfolio visibility)
- **Template approach**: Reuse notebook structure from `05_draft_roi_analysis.ipynb`
- **Priority queue**: Position deep dives first (highest reader interest, standardized structure)

### Article Analysis
- **Parquet engine**: `fastparquet==0.7.2` (not pyarrow — 32-bit Windows incompatible)
- **Value Score**: `performance_zscore - salary_zscore` within position groups
- **Salary normalization**: `apy_cap_pct` (% of salary cap) for cross-year comparison
- **Minimum threshold**: 100 snaps/season for inclusion
- **Draft ROI scope**: Rookie contract years 1-4 only (standard rookie deal window)

### Publishing Workflow (`/publish` skill)
- **GEO optimization first** — Run `/seo-for-llms` before HTML export
- **GitHub Pages for Medium import** — ONLY GitHub Pages URLs work (not raw.githubusercontent.com)
- **Medium navigation**: Go directly to `https://medium.com/p/import` (not /new-story)
- **Form input method**: Use `click + type` for Medium's custom fields (form_input fails)
- **HTML export**: Python markdown library with tables, fenced_code, nl2br extensions
- **Git automation**: Auto-refresh auth on push failure, 10-second wait for GitHub Pages rebuild

### Medium Import URLs — VERIFIED
**CRITICAL: Medium is picky about URLs**

- **Import URL for Medium**: Use GitHub Pages URL to HTML file
  - Format: `https://ghighcove.github.io/nfl-salary-analysis/article/filename.html`
  - Medium **REJECTS** raw.githubusercontent.com URLs (both markdown and HTML)
  - Testing confirmed: raw.githubusercontent.com imports fail with "Import failed" error

- **Image URLs WITHIN content**: Use raw.githubusercontent.com format
  - Format: `https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/image.png`
  - These load correctly when HTML is imported via GitHub Pages URL

- **Table handling**:
  - HTML `<table>` elements import with data intact but lose column formatting
  - Options: (1) Manually reformat in Medium editor, (2) Use image-based tables, (3) Convert to prose
  - Image-based tables (like position strategy table) import perfectly

## Recent Changes (this session)

### Project Pipeline Implementation
**Files created:**
- `PROJECT_PIPELINE.md` — Complete 20-article production roadmap
  - Series 1: Position Deep Dives (10 articles) — RB, QB, WR, TE, DB, LB, DL, OL, K/P, ST
  - Series 2: Team Strategy (8 articles) — Drafting, cap management, FA ROI, rebuilding
  - Series 3: Contract Market Trends (2 articles) — Salary inflation, contract year
  - GEO optimization checklist (95+ score requirements from Draft ROI success)
  - Article production workflow (4-phase cycle: Analysis → Writing → Publishing → Finalization)
  - Priority queue with next 5 articles identified
  - Progress tracking: 2 of 20 articles completed

**Files updated:**
- `README.md` — Replaced RESEARCH_OPTIONS.md reference with pipeline overview
- `notebooks/06_rb_economics.ipynb` — Template notebook for next article
  - Career arc analysis (when do RBs peak?)
  - Draft ROI by round (confirm first-round RBs barely break even)
  - Top 10 bargains (late-round steals)
  - Top 10 busts (first-round disappointments)
  - Positional replaceability analysis (drafted vs. UDFA)
  - 6 visualizations planned

**Git commits:**
- 3877e3a: "feat: Add project pipeline with 20-article roadmap"
  - 1,126 lines added across 3 files
  - Pushed to GitHub successfully

## Blockers / Open Questions
- **No blockers.** Pipeline fully implemented and documented.
- **Minor pending:** Draft ROI article final publication (tables, tags, SEO)

## Next Steps
1. **Finish Draft ROI article** (30-60 min)
   - Open Medium draft (ID: f2cdfa739f9e)
   - Reformat tables in editor
   - Add tags from `MEDIUM_PUBLISH_INFO_draft_roi.md` (NFL, NFL Draft, Data Analysis, Sports Analytics, Football)
   - Add SEO meta description in Medium settings
   - Preview and publish

2. **Start Article #3: Running Back Economics** (1 week)
   - Run `06_rb_economics.ipynb` notebook
   - Generate 6 visualizations (save to `article/images/rb_economics/`)
   - Write `article/rb_economics_medium_draft.md`
   - Run `/publish rb_economics` skill

3. **Track Progress**
   - Update PROJECT_PIPELINE.md checkboxes as articles complete
   - Maintain velocity: 2-3 articles/month

## Environment
- Platform: Windows (win32), Python 3.8.2 (32-bit)
- Working directory: G:\ai\nfl
- Additional working dirs: G:\ai\nfl-data-core\nfl_analysis, G:\ai\nfl-data-core
- Key packages: nfl-data-py, fastparquet 0.7.2, pandas 2.0.3, plotly, scikit-learn, markdown 3.4.3, beautifulsoup4 4.12.2
- GitHub repo: ghighcove/nfl-salary-analysis (public, GitHub Pages enabled)
- Shared library: nfl-data-core (imported as `nfl_analysis`)
- Browser automation: claude-in-chrome MCP server (for Medium import)

## Quick Reference
- **Project CLAUDE.md**: `G:\ai\nfl\CLAUDE.md` (includes `/publish` skill documentation)
- **Project Pipeline**: `G:\ai\nfl\PROJECT_PIPELINE.md` (20-article roadmap)
- **Global CLAUDE.md**: `C:\Users\ghigh\.claude\CLAUDE.md`
- **Git repo**: https://github.com/ghighcove/nfl-salary-analysis (branch: master)
- **Publishing skill**: `.claude/skills/nfl-article-publish/` (usage: `/publish <article_name>`)
- **Lessons learned**: `tasks/lessons.md` (includes Medium import errors & fixes)
- **Session context**: `tasks/context.md`

### Article URLs
**Original article:**
- GitHub Pages: https://ghighcove.github.io/nfl-salary-analysis/article/medium_ready.html

**Draft ROI article:**
- GitHub Pages: https://ghighcove.github.io/nfl-salary-analysis/article/draft_roi_medium_ready.html
- GitHub Markdown: https://github.com/ghighcove/nfl-salary-analysis/blob/master/article/draft_roi_medium_draft.md
- Medium draft: https://medium.com/p/f2cdfa739f9e/edit
- Publishing info: `article/MEDIUM_PUBLISH_INFO_draft_roi.md`
- GEO score: 99/100 (A+)

### Pipeline Status
- **Completed:** 2 of 20 articles (Player Value Analysis, Draft ROI Analysis)
- **Next up:** Running Back Economics (notebook template ready)
- **Target:** 5-10 articles in 2-3 months (velocity: 2-3/month)
