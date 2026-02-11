"""
HTML export functionality for converting markdown to Medium-ready HTML.
"""
import os
import re
import markdown
from markdown.extensions.tables import TableExtension


def extract_h1(md_content):
    """Extract the first H1 heading from markdown content."""
    match = re.search(r'^#\s+(.+)$', md_content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled Article"


def extract_image_paths(md_content):
    """Extract all image paths from markdown content."""
    # Match ![alt](url) pattern
    pattern = r'!\[.*?\]\((.+?)\)'
    matches = re.findall(pattern, md_content)
    return matches


def export_html(article_dir, name):
    """
    Convert markdown to Medium-ready HTML.

    Args:
        article_dir: Path to article directory
        name: Article name (e.g., "draft_roi")

    Returns:
        (bool, str): (success, error_message or html_path)
    """
    md_path = os.path.join(article_dir, f"{name}_medium_draft.md")
    html_path = os.path.join(article_dir, f"{name}_medium_ready.html")
    template_path = os.path.join(
        os.path.dirname(__file__),
        "templates",
        "medium_ready_template.html"
    )

    # Read markdown content
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        return False, f"Markdown file not found: {md_path}"
    except Exception as e:
        return False, f"Error reading markdown: {str(e)}"

    # Extract title
    title = extract_h1(md_content)

    # Convert markdown to HTML with extensions
    try:
        html_body = markdown.markdown(
            md_content,
            extensions=[
                'tables',
                'fenced_code',
                'nl2br',
                'codehilite'
            ]
        )
    except Exception as e:
        return False, f"Error converting markdown to HTML: {str(e)}"

    # Read HTML template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        return False, f"HTML template not found: {template_path}"
    except Exception as e:
        return False, f"Error reading template: {str(e)}"

    # Generate full HTML by replacing placeholders
    full_html = template.format(
        title=title,
        content=html_body
    )

    # Write HTML file
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(full_html)
    except Exception as e:
        return False, f"Error writing HTML file: {str(e)}"

    return True, html_path


if __name__ == "__main__":
    # Test with draft_roi article
    success, result = export_html("../../article", "draft_roi")
    if success:
        print(f"✅ HTML exported to: {result}")
    else:
        print(f"❌ Error: {result}")
