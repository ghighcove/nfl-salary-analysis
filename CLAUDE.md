# NFL Player Stats vs. Salary Analysis

## Project Overview
Jupyter Notebook project analyzing NFL player performance statistics against salary data (2015-2024). Surfaces outliers — players who dramatically outperform or underperform their salary.

## Architecture
- `notebooks/` — Sequential notebooks (01-04) that build on each other
- `data/` — Cached parquet files (gitignored)
- `article/` — Medium article draft and published HTML (GitHub Pages)
- **Shared Library**: Analysis modules (data_loader, cleaning, value_score, viz) imported from [nfl-data-core](https://github.com/ghighcove/nfl-data-core) library

## Key Conventions
- Salary is normalized as % of salary cap (`apy_cap_pct`) for cross-year comparison
- Primary join key: `gsis_id` (called `player_id` in weekly stats)
- Minimum 100 snaps/season threshold for inclusion
- Position groups: QB, RB, WR, TE, OL, DL, LB, DB, K, P
- Value Score = composite_performance_zscore - salary_cap_pct_zscore (positive = bargain)

## Data Sources
All data from `nfl_data_py` library. Cached as parquet in `data/`.

## Running
1. `pip install -r requirements.txt` (installs nfl-data-core library from GitHub)
2. Run notebooks in order: 01 → 02 → 03 → 04
3. Each notebook saves outputs that the next one reads

**Import Pattern in Notebooks:**
```python
from nfl_analysis import data_loader, cleaning, value_score, viz
```

## Automated Publishing Workflow

### Quick Start

To publish a new NFL analysis article:

```bash
/publish <article_name>
```

**Examples:**
- `/publish draft_roi`
- `/publish win_probability`
- `/publish player_value_trends`

The `/publish` skill automates the entire publishing pipeline:
1. ✅ **GEO Optimization** - Runs `/seo-for-llms` audit for LLM discoverability
2. ✅ **Metadata Generation** - Creates `MEDIUM_PUBLISH_INFO_{name}.md` with SEO descriptions and tags
3. ✅ **HTML Export** - Converts markdown to Medium-compatible HTML
4. ✅ **Git Workflow** - Commits and pushes to GitHub (updates GitHub Pages)
5. ✅ **URL Output** - Provides GitHub Pages and markdown URLs
6. ✅ **Medium Import** - Optional browser automation for importing to Medium draft
7. ✅ **Scheduling** - Optional publication date scheduling

### Article Preparation

Before running `/publish`, ensure:

1. **Create markdown file:** `article/{name}_medium_draft.md`
2. **Generate visualizations:** Save charts/images to `article/` or `article/images/`
3. **Use correct image URLs:**
   ```markdown
   ![Chart](https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/chart.png)
   ```
4. **Include attribution:** Between subtitle and `---` separator:
   ```markdown
   # Article Title
   *Subtitle goes here*

   *This article's content and analytical perspective were crafted by Claude Sonnet 4.5. The project genesis and direction came from Glenn Highcove. For more information and feedback, connect with Glenn on [LinkedIn](https://www.linkedin.com/in/glennhighcove/).*

   ---

   [Article content begins...]
   ```

### Article Optimization Guidelines (GEO)

For LLM discoverability and AI search optimization:
- Use descriptive H2 headings (topic + key finding), not clever/vague labels
- Include a "Key Findings" summary block near the top for RAG retrieval
- Lead sections with conclusions (BLUF), then support with narrative
- Define acronyms on first use (PFR, EPA, etc.)
- Link data sources inline, not just in a footer
- The `/publish` skill automatically generates SEO meta descriptions (≤200 chars)

### Workflow Output

After running `/publish {name}`, you'll receive:

**Files Created:**
- `article/{name}_medium_ready.html` - Medium-compatible HTML export
- `article/MEDIUM_PUBLISH_INFO_{name}.md` - Publishing metadata and checklist

**URLs Provided:**
- **GitHub Pages** (for Medium import): `https://ghighcove.github.io/nfl-salary-analysis/article/{name}_medium_ready.html`
- **GitHub Markdown** (browser-friendly): `https://github.com/ghighcove/nfl-salary-analysis/blob/master/article/{name}_medium_draft.md`

**Git Commit:**
- Message format: `feat: Add {Topic} Medium article (GEO: {score}/100)`
- Automatically pushed to `master` branch

### Medium Publishing

**Option 1: Automated (Recommended)**
1. Run `/publish {name}`
2. Accept "Push to Medium as draft?" prompt (defaults to Yes)
3. Browser automation imports article to Medium
4. Review and publish in Medium editor

**Option 2: Manual Import**
1. Run `/publish {name}` (decline Medium import if prompted)
2. Copy GitHub Pages URL from output
3. Go to Medium → New Story → Import a story
4. Paste GitHub Pages URL (**NOT** `raw.githubusercontent.com`)
5. Import completes → review in editor

**Post-Import Steps:**
1. Reformat tables if needed (data preserved, columns may run together)
2. Add tags from `MEDIUM_PUBLISH_INFO_{name}.md` (5 max)
3. Add SEO description in Medium settings (Settings → More settings → SEO description)
4. Preview and publish

### Medium Import Technical Notes

**CRITICAL: Use GitHub Pages URLs for Import**
- Medium **ONLY accepts GitHub Pages URLs** for importing articles
- Import URL format: `https://ghighcove.github.io/nfl-salary-analysis/article/{name}_medium_ready.html`
- Medium **REJECTS** `raw.githubusercontent.com` URLs (returns "Import failed" error)
- Images WITHIN the article content can use `raw.githubusercontent.com` URLs and will load correctly

**Table Handling:**
- HTML `<table>` elements import with data intact but lose column formatting
- Options: (1) Reformat manually in Medium editor, (2) Use image-based tables, (3) Convert to prose/lists
- Image-based tables (screenshots of formatted tables) import perfectly
