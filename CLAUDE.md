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

## Article Optimization (GEO)
When writing or updating the Medium article (`article/medium_draft.md` + `article/medium_ready.html`):
- Run the `seo-for-llms` skill before publishing to audit LLM discoverability
- Both files must be edited in sync — markdown source and HTML are maintained independently
- Use descriptive H2 headings (topic + key finding), not clever/vague labels
- Include a "Key Findings" summary block near the top for RAG retrieval
- Lead sections with conclusions (BLUF), then support with narrative
- Define acronyms on first use (PFR, EPA, etc.)
- Link data sources inline, not just in a footer
- Use the SEO meta description output (≤200 chars) for Medium/CMS description field
- After edits, commit and push to update the GitHub Pages URL that Medium reads from

## Medium Article Publishing

**CRITICAL: Image URL Format for Medium Import**
- For Medium article publishing: **always use `raw.githubusercontent.com` URLs** for images in the markdown/HTML source files
- Example: `https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/image.png`
- **Never use GitHub Pages URLs** (`ghighcove.github.io`) in article source files for Medium import
- Medium rejects GitHub Pages URLs because they serve with `text/plain` content-type, blocking image imports
- GitHub Pages URLs are for web viewing only, not Medium import

### Medium Import Methods

**Preferred:** Import markdown files directly
- URL format: `https://raw.githubusercontent.com/USER/REPO/master/article/filename.md`
- Medium can parse markdown tables natively
- Simpler than HTML import
- Use for articles with data tables

**Alternative:** Import hand-crafted HTML (like original article)
- Must use `<figure>` tags for images (not `<p><img /></p>`)
- Avoid HTML tables if possible (Medium's parser has limitations)
- Add `lang="en"` to `<html>` tag
- Use serif fonts, avoid self-closing tags
- Use for articles with complex formatting that requires manual control

**Don't:** Import auto-generated HTML from markdown
- Complex table structures cause parsing failures
- Self-closing tags and `<p>`-wrapped images may be rejected
- Medium's HTML parser is stricter than markdown parser
