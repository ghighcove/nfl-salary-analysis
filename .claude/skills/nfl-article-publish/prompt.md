# NFL Article Publishing Workflow

You are executing the automated NFL article publishing workflow for the article: `{{args}}`

## Workflow Steps

### Phase 1: Pre-Flight Validation

Use the Python validation utilities to check:
1. Article file `article/{{args}}_medium_draft.md` exists
2. All referenced images are accessible
3. Git working tree status

Run:
```bash
cd .claude/skills/nfl-article-publish && python -c "
from main import validate_article, get_project_root
import os
project_root = get_project_root()
article_dir = os.path.join(project_root, 'article')
success, error = validate_article(article_dir, '{{args}}')
if not success:
    print(error)
    exit(1)
print('✅ Pre-flight checks passed')
"
```

If this fails, report the error to the user and stop.

### Phase 2: GEO Optimization

Run the SEO optimization skill on the article:

```
/seo-for-llms article/{{args}}_medium_draft.md
```

Capture the GEO results from the skill output:
- **GEO Score** (e.g., 96/100)
- **Grade** (e.g., A, B, C)
- **Meta Description** (≤200 characters)
- **Social Summary** (≤280 characters)
- **Key Strengths** (bullet list)
- **Applied Improvements** (bullet list)

Store these for Phase 3.

### Phase 3: Generate Publishing Metadata

Use the captured GEO data to generate `MEDIUM_PUBLISH_INFO_{{args}}.md`:

```python
from geo_metadata import generate_publish_info
from main import get_project_root
import os

geo_data = {
    'score': <captured_score>,
    'grade': '<captured_grade>',
    'meta_description': '<captured_meta_description>',
    'social_summary': '<captured_social_summary>',
    'strengths': '<captured_strengths>',
    'improvements': '<captured_improvements>'
}

project_root = get_project_root()
article_dir = os.path.join(project_root, 'article')
model_name = "Claude Sonnet 4.5"  # Use your current model name

success, result = generate_publish_info(article_dir, '{{args}}', geo_data, model_name)
if success:
    print(f'✅ Publishing info generated: {result}')
else:
    print(f'❌ Error: {result}')
```

### Phase 4: HTML Export

Convert markdown to Medium-ready HTML:

```bash
cd .claude/skills/nfl-article-publish && python -c "
from html_exporter import export_html
from main import get_project_root
import os
project_root = get_project_root()
article_dir = os.path.join(project_root, 'article')
success, result = export_html(article_dir, '{{args}}')
if success:
    print(f'✅ HTML exported: {result}')
else:
    print(f'❌ Error: {result}')
    exit(1)
"
```

### Phase 5: Git Workflow

Commit and push the article files:

```bash
cd .claude/skills/nfl-article-publish && python -c "
from main import git_commit_and_push, get_project_root
import os
project_root = get_project_root()
article_dir = os.path.join(project_root, 'article')
success, error = git_commit_and_push(article_dir, '{{args}}', <geo_score>)
if success:
    print('✅ Changes pushed to GitHub')
else:
    print(f'⚠️  {error}')
"
```

Wait 10 seconds for GitHub Pages to rebuild:
```bash
sleep 10
```

### Phase 6: URL Output (Always Display)

Display the following URLs to the user:

```
📄 Article URLs Generated

**GitHub Pages (Medium Import URL):**
https://ghighcove.github.io/nfl-salary-analysis/article/{{args}}_medium_ready.html

**Browser-Friendly Markdown:**
https://github.com/ghighcove/nfl-salary-analysis/blob/master/article/{{args}}_medium_draft.md

**Publishing Info:**
article/MEDIUM_PUBLISH_INFO_{{args}}.md

**GEO Score:** <score>/100 (<grade>)
```

### Phase 7: Medium Import (Optional)

Use AskUserQuestion to prompt:
```
Push to Medium as draft?
Options:
  - "Yes (Recommended)" → Proceed with Medium import
  - "No - I'll import manually" → Skip to final output
```

If user selects **"Yes"**:

1. Use the `mcp__claude-in-chrome__*` tools to automate Medium import
2. Get tab context: `tabs_context_mcp(createIfEmpty=True)`
3. Navigate to: `https://medium.com/new-story`
4. Find and click "Import a story" link
5. Enter GitHub Pages URL in import field
6. Click "Import" button
7. Wait for import to complete
8. Extract Medium draft URL from browser location
9. Display Medium draft URL to user

If import succeeds, proceed to Phase 8. If it fails, provide manual import instructions.

### Phase 8: Medium Scheduling (Optional, only if Phase 7 succeeded)

If Medium import succeeded, ask:
```
Set go-live date for this article in Medium?
Options:
  - "Yes - Schedule publication" → Proceed with scheduling
  - "No - Leave as draft" → Skip to final output
```

If user selects **"Yes - Schedule publication"**:

1. Ask user for publication date/time (use AskUserQuestion)
2. Navigate to Medium draft URL (from Phase 7)
3. Use browser automation to access scheduling interface
4. Set publication date/time
5. Confirm scheduling

### Phase 9: Final Output & Summary

Display completion summary:

```
✅ Article Published Successfully

## URLs
| Type | URL |
|------|-----|
| GitHub Pages (HTML) | https://ghighcove.github.io/nfl-salary-analysis/article/{{args}}_medium_ready.html |
| GitHub Markdown | https://github.com/ghighcove/nfl-salary-analysis/blob/master/article/{{args}}_medium_draft.md |
| Medium Draft | <medium_draft_url> | ← [Only if imported]
| Publishing Info | article/MEDIUM_PUBLISH_INFO_{{args}}.md |

## GEO Score
<score>/100 (<grade>)

## Next Steps
[If Medium import succeeded:]
1. Review article in Medium editor: <medium_draft_url>
2. Reformat tables if needed (data preserved, columns may run together)
3. Add tags from MEDIUM_PUBLISH_INFO_{{args}}.md (5 max)
4. Add SEO meta description (Settings → More settings → SEO description)
5. Preview and publish when ready

[If Medium import skipped:]
1. Review article at GitHub Pages URL
2. Import manually to Medium if desired using GitHub Pages URL
3. See MEDIUM_PUBLISH_INFO_{{args}}.md for publishing checklist
```

## Error Handling

- If pre-flight validation fails → Stop and report error
- If GEO optimization fails → Ask user if they want to continue without GEO data
- If HTML export fails → Stop and report error
- If git push fails → Continue to URL output, provide manual push command
- If Medium import fails → Provide manual import instructions and continue
- If scheduling fails → Provide manual scheduling instructions

## Important Notes

- Always use GitHub Pages URLs for Medium import, never `raw.githubusercontent.com`
- HTML tables will import with data but lose formatting (warn user to reformat)
- Images within content can use `raw.githubusercontent.com` URLs
- All phases except Medium import and scheduling are required
