# NFL Project — Publishing Rules

## Automated Publishing Workflow

Run `/publish <article_name>` to automate the full pipeline:
1. GEO optimization (`/seo-for-llms` audit)
2. Metadata generation → `article/MEDIUM_PUBLISH_INFO_{name}.md`
3. HTML export → `article/{name}_medium_ready.html`
4. Git commit + push to GitHub (updates GitHub Pages)
5. Optional Medium import via browser automation

## Article Preparation

Before `/publish`, ensure:
- `article/{name}_medium_draft.md` exists
- Charts saved to `article/` or `article/images/`
- Image URLs use `raw.githubusercontent.com`:
  ```markdown
  ![Chart](https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/chart.png)
  ```
- Attribution block between subtitle and `---` separator (see global `rules/publishing/article-attribution.md`)

## GEO Guidelines

- H2 headings: topic + key finding (not clever/vague labels)
- "Key Findings" summary block near top for RAG retrieval
- BLUF structure: conclusion first, then narrative
- Define acronyms on first use (PFR, EPA, etc.)
- Link data sources inline

## Medium Import Technical Notes

**CRITICAL: Medium caches imported URLs by filename.** Always use unique timestamped filename per import:
- Required format: `{article_name}_{YYYYMMDD}_{HHMM}.html`
- Example: `te_market_inefficiency_20260211_1630.html`
- Never reuse `*_medium_ready.html` after updating content

**Import URL**: GitHub Pages only — `https://ghighcove.github.io/nfl-salary-analysis/article/{unique}.html`
- Medium REJECTS `raw.githubusercontent.com` URLs for import
- Images inside the article CAN use `raw.githubusercontent.com` — that's fine

**Tables**: Must be PNG images. Medium strips `<table>` tags. Wrap in `<p>` tags:
```html
<p><img alt="Table visualization showing [description]" src="..." /></p>
```

## Publishing Options

**Automated (recommended)**: Run `/publish {name}`, accept Medium import prompt.

**Manual import**:
1. `/publish {name}` (decline import)
2. Medium → New Story → Import → paste GitHub Pages URL
3. Add tags from `MEDIUM_PUBLISH_INFO_{name}.md` (5 max)
4. Add SEO description in Medium Settings → More settings

**Commit format**: `feat: Add {Topic} Medium article (GEO: {score}/100)`
