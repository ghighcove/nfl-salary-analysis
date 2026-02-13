"""
Export RB Economics markdown to Medium-compatible HTML with unique timestamp.
"""

import markdown
from datetime import datetime
from pathlib import Path

# Generate unique timestamped filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
input_file = Path('article/rb_economics_medium_draft.md')
output_file = Path(f'article/rb_economics_{timestamp}.html')

print(f"Reading markdown from: {input_file}")
print(f"Generating HTML with timestamp: {timestamp}")

# Read markdown content
with open(input_file, 'r', encoding='utf-8') as f:
    markdown_content = f.read()

# Convert to HTML using Python markdown library
html_body = markdown.markdown(
    markdown_content,
    extensions=['extra', 'nl2br', 'sane_lists']
)

# Wrap images in <p> tags for Medium formatting
# Medium expects: <p><img alt="..." src="..." /></p>
html_body = html_body.replace('<img alt=', '<p><img alt=')
html_body = html_body.replace('.png">', '.png"></p>')

# Create full HTML document structure
html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Running Back Economics: Why First-Round RBs Are the NFL Draft's Worst Investment</title>
    <meta name="description" content="A data-driven analysis of career arcs, draft value, and positional replaceability reveals the truth about running back contracts (2015-2024)">
</head>
<body>
{html_body}
</body>
</html>"""

# Write HTML file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"[OK] HTML export created: {output_file}")
print(f"\nGitHub Pages URL for Medium import:")
print(f"https://ghighcove.github.io/nfl-salary-analysis/article/rb_economics_{timestamp}.html")
print(f"\nNext steps:")
print(f"1. Commit and push to GitHub")
print(f"2. Wait 1-2 minutes for GitHub Pages to update")
print(f"3. Go to Medium > New Story > Import a story")
print(f"4. Paste the GitHub Pages URL above (NOT raw.githubusercontent.com)")
print(f"5. Verify tables display as images")
