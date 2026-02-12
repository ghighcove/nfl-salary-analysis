"""
Convert markdown to Medium-compatible HTML with unique timestamped filename

CRITICAL: Always generates unique filename to bypass Medium's aggressive caching.
"""

import re
import sys
import hashlib
from pathlib import Path
from datetime import datetime

def markdown_to_html(md_text):
    """Convert markdown to clean HTML for Medium import"""

    html = md_text

    # Convert headers (must be done before other conversions)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)

    # Convert images with alt text - WRAP IN <p> TAGS (Medium import requirement)
    html = re.sub(r'!\[([^\]]+)\]\(([^\)]+)\)', r'<p><img src="\2" alt="\1" /></p>', html)

    # Convert links
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Convert bold and italic (do bold before italic to handle ***)
    html = re.sub(r'\*\*\*([^\*]+)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', html)

    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Convert horizontal rules
    html = re.sub(r'^---$', r'<hr />', html, flags=re.MULTILINE)

    # Convert tables
    lines = html.split('\n')
    in_table = False
    table_lines = []
    processed_lines = []

    for i, line in enumerate(lines):
        # Detect table (lines with |)
        if '|' in line and not line.startswith('<'):
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                # Process accumulated table
                processed_lines.append(convert_table(table_lines))
                in_table = False
                table_lines = []
            processed_lines.append(line)

    # Handle table at end of file
    if in_table:
        processed_lines.append(convert_table(table_lines))

    html = '\n'.join(processed_lines)

    # Convert unordered lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # Wrap consecutive <li> in <ul>
    html = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', html, flags=re.DOTALL)

    # Convert numbered lists
    html = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)

    # Wrap consecutive numbered <li> in <ol>
    html = re.sub(r'(<li>.*?</li>\n)+', lambda m: '<ol>\n' + m.group(0) + '</ol>\n' if re.search(r'\d+\.', m.string[max(0, m.start()-20):m.start()]) else m.group(0), html, flags=re.DOTALL)

    # Wrap paragraphs (any line not already in a tag)
    lines = html.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if line and not re.match(r'^<[^>]+>', line):
            # Check if it's a list item or table cell
            if not line.startswith('|') and not re.match(r'^\d+\.', line) and not line.startswith('-'):
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)
        else:
            result.append(line)

    html = '\n'.join(result)

    # Clean up empty paragraphs
    html = re.sub(r'<p>\s*</p>', '', html)

    # Clean up multiple blank lines
    html = re.sub(r'\n{3,}', '\n\n', html)

    return html.strip()

def convert_table(table_lines):
    """Convert markdown table to HTML table"""
    if len(table_lines) < 2:
        return '\n'.join(table_lines)

    # Remove separator line (the one with dashes)
    table_data = [line for line in table_lines if not re.match(r'^\|[\s\-:|]+\|$', line)]

    if not table_data:
        return ''

    html = ['<table>']

    # First row is header
    header = table_data[0]
    cells = [cell.strip() for cell in header.split('|') if cell.strip()]
    html.append('<thead><tr>')
    for cell in cells:
        # Remove markdown formatting from headers
        cell = re.sub(r'\*\*([^\*]+)\*\*', r'\1', cell)
        html.append(f'<th>{cell}</th>')
    html.append('</tr></thead>')

    # Remaining rows are body
    if len(table_data) > 1:
        html.append('<tbody>')
        for row in table_data[1:]:
            cells = [cell.strip() for cell in row.split('|') if cell.strip()]
            html.append('<tr>')
            for cell in cells:
                # Convert markdown formatting in cells
                cell = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', cell)
                cell = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', cell)
                html.append(f'<td>{cell}</td>')
            html.append('</tr>')
        html.append('</tbody>')

    html.append('</table>')

    return '\n'.join(html)

def generate_unique_filename(article_name, content):
    """
    Generate unique timestamped filename to bypass Medium caching.

    CRITICAL: Medium caches imported URLs by filename. Using the same filename
    will serve cached version even if content changes. Always use unique names.

    Format: {article_name}_{YYYYMMDD}_{HHMM}_{hash}.html
    Example: te_market_inefficiency_20260211_1630_a3f2b1c4.html
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
    return f"{article_name}_{timestamp}_{content_hash}.html"

def convert_article(article_name):
    """Convert markdown article to Medium-ready HTML with unique filename"""

    input_file = Path(f'{article_name}_medium_draft.md')

    if not input_file.exists():
        print(f"❌ Error: {input_file} not found")
        print(f"\nUsage: python convert_to_html.py <article_name>")
        print(f"Example: python convert_to_html.py te_market_inefficiency")
        return None

    print(f"Reading {input_file}...")
    md_content = input_file.read_text(encoding='utf-8')

    print("Converting markdown to HTML...")
    html_content = markdown_to_html(md_content)

    # Extract title from markdown (first # header)
    title_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    title = title_match.group(1) if title_match else article_name.replace('_', ' ').title()

    # Wrap in basic HTML structure
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
{html_content}
</body>
</html>"""

    # Generate unique filename (CRITICAL for Medium import)
    output_filename = generate_unique_filename(article_name, full_html)
    output_file = Path(output_filename)

    print(f"Writing {output_file}...")
    output_file.write_text(full_html, encoding='utf-8')

    # Generate GitHub Pages URL
    github_pages_url = f"https://ghighcove.github.io/nfl-salary-analysis/article/{output_filename}"

    print(f"\n✓ Conversion complete!")
    print(f"✓ Output: {output_file.resolve()}")
    print(f"\n📋 Medium import URL (copy this):")
    print(f"{github_pages_url}")
    print(f"\n⚠️  IMPORTANT: This is a unique timestamped URL to bypass Medium's cache.")
    print(f"   Do NOT reuse old filenames - always run this script for fresh imports.")

    return output_filename

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_to_html.py <article_name>")
        print("\nExample:")
        print("  python convert_to_html.py te_market_inefficiency")
        print("\nThis will convert:")
        print("  te_market_inefficiency_medium_draft.md")
        print("To:")
        print("  te_market_inefficiency_YYYYMMDD_HHMM_hash.html")
        sys.exit(1)

    article_name = sys.argv[1]
    convert_article(article_name)
