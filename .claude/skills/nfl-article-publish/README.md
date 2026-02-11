# NFL Article Publishing Skill

Automated workflow for publishing NFL analysis articles to Medium with GEO optimization, HTML export, git automation, and optional browser-based Medium import.

## Features

- ✅ **Pre-flight validation** - Checks article file exists, images are present, git status
- ✅ **GEO optimization** - Runs `/seo-for-llms` skill for LLM discoverability
- ✅ **Metadata generation** - Auto-creates `MEDIUM_PUBLISH_INFO_{name}.md` with SEO descriptions, tags, checklists
- ✅ **HTML export** - Converts markdown to Medium-compatible HTML with proper styling
- ✅ **Git automation** - Commits and pushes to GitHub to update GitHub Pages
- ✅ **URL generation** - Outputs GitHub Pages and markdown URLs for easy access
- ✅ **Medium import** - Optional browser automation for importing to Medium (requires claude-in-chrome)
- ✅ **Scheduling** - Optional publication date scheduling in Medium

## Usage

### Command Syntax

```bash
/publish <article_name>
```

### Examples

```bash
/publish draft_roi
/publish win_probability
/publish player_value_trends
```

## Workflow Phases

### 1. Pre-Flight Checks
- Validates `article/{name}_medium_draft.md` exists
- Checks all referenced images are accessible
- Reports git working tree status

### 2. GEO Optimization
- Runs `/seo-for-llms` skill on the markdown file
- Captures GEO score, meta description, social summary
- Generates optimization recommendations

### 3. Metadata Generation
- Creates `MEDIUM_PUBLISH_INFO_{name}.md` with:
  - SEO meta description (≤200 chars)
  - Social summary for X/LinkedIn (≤280 chars)
  - Suggested Medium tags
  - Image URL list
  - Publishing checklist
  - Attribution template

### 4. HTML Export
- Converts markdown to HTML using Python `markdown` library
- Applies Medium-compatible styling
- Supports tables, code blocks, images
- Outputs to `article/{name}_medium_ready.html`

### 5. Git Workflow
- Stages article files (markdown, HTML, metadata)
- Creates commit: `feat: Add {Topic} Medium article (GEO: {score}/100)`
- Pushes to GitHub master branch
- Waits 10 seconds for GitHub Pages rebuild

### 6. URL Output (Always)
Displays:
- **GitHub Pages URL** (for Medium import): `https://ghighcove.github.io/nfl-salary-analysis/article/{name}_medium_ready.html`
- **GitHub Markdown URL** (browser-friendly): `https://github.com/ghighcove/nfl-salary-analysis/blob/master/article/{name}_medium_draft.md`
- **Publishing Info Path**: `article/MEDIUM_PUBLISH_INFO_{name}.md`

### 7. Medium Import (Optional)
- Prompts: "Push to Medium as draft? [Yes (Recommended)] [No]"
- If yes: Uses browser automation to import HTML via GitHub Pages URL
- Extracts Medium draft URL for editing
- If no: Skips to completion

### 8. Medium Scheduling (Optional)
- Only appears if Medium import succeeded
- Prompts for publication date/time
- Navigates to Medium scheduling interface

## File Structure

```
.claude/skills/nfl-article-publish/
├── skill.json                          # Skill metadata
├── main.py                             # Main workflow orchestration
├── html_exporter.py                    # Markdown to HTML converter
├── geo_metadata.py                     # MEDIUM_PUBLISH_INFO generator
├── medium_automation.py                # Browser automation for Medium
├── requirements.txt                    # Python dependencies
├── README.md                           # This file
└── templates/
    ├── MEDIUM_PUBLISH_INFO_template.md # Metadata file template
    └── medium_ready_template.html      # HTML export template
```

## Requirements

### Python Packages
```
markdown>=3.4.3
beautifulsoup4>=4.12.2
```

Install with:
```bash
pip install -r .claude/skills/nfl-article-publish/requirements.txt
```

### Browser Automation (Optional)
- Requires `claude-in-chrome` MCP server for Medium import/scheduling features
- If not available, workflow provides manual import URL

### Git Configuration
- GitHub authentication (`gh auth status`)
- `workflow` scope for pushing to GitHub

## Article Preparation

Before running `/publish`, ensure:

1. **Markdown file exists**: `article/{name}_medium_draft.md`
2. **Images generated**: All referenced images in `article/` or `article/images/`
3. **Image URLs use GitHub format**: `https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/{image}.png`
4. **Attribution present**: Between subtitle and `---` separator (will be validated by GEO optimization)

## Output Files

After running `/publish draft_roi`, you'll have:

- `article/draft_roi_medium_draft.md` - Original markdown (possibly modified by GEO)
- `article/draft_roi_medium_ready.html` - Medium-compatible HTML export
- `article/MEDIUM_PUBLISH_INFO_draft_roi.md` - Publishing metadata and checklist

## Medium Publishing Workflow

### Automated Path (Recommended)
1. Run `/publish {name}`
2. Accept Medium import prompt
3. Review draft in Medium editor
4. Reformat tables if needed (data preserved, columns may run together)
5. Add tags from MEDIUM_PUBLISH_INFO
6. Add SEO description in Medium settings
7. Preview and publish

### Manual Path
1. Run `/publish {name}` and decline Medium import
2. Copy GitHub Pages URL from output
3. Go to Medium → New Story → Import
4. Paste GitHub Pages URL (NOT raw.githubusercontent.com)
5. Follow steps 3-7 above

## Troubleshooting

### "Markdown file not found"
- Create `article/{name}_medium_draft.md` first
- Check spelling of article name

### "Missing image files"
- Generate charts/images and save to `article/`
- Verify image filenames match markdown references
- Use `https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/{image}.png` format

### "Git push failed"
- Run `gh auth status` to check authentication
- Run `gh auth refresh -s workflow` to refresh token
- Check network connection

### "Medium import failed"
- Ensure using GitHub Pages URL, not raw.githubusercontent.com
- Check Medium is accessible in browser
- Try manual import as fallback

### "Tables not formatted in Medium"
- HTML tables import with data intact but lose column formatting
- Manually reformat in Medium editor after import
- Or use image-based tables (table screenshots)

## Version History

- **1.0.0** (2026-02-10) - Initial release with full workflow automation

## Author

Glenn Highcove - [LinkedIn](https://www.linkedin.com/in/glennhighcove/)
