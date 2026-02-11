"""
GEO metadata generation for Medium publishing.
"""
import os
import re


def extract_h1(md_path):
    """Extract the first H1 heading from markdown file."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else "Untitled Article"
    except Exception:
        return "Untitled Article"


def extract_image_urls(md_path):
    """Extract all image URLs from markdown file."""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        pattern = r'!\[.*?\]\((.+?)\)'
        matches = re.findall(pattern, content)
        return matches
    except Exception:
        return []


def infer_topic_tag(name):
    """Infer topic tag from article name."""
    topic_map = {
        'draft': 'NFL Draft',
        'roi': 'Return on Investment',
        'salary': 'Salary Cap',
        'win': 'Win Probability',
        'probability': 'Predictive Analytics',
        'value': 'Player Valuation',
        'performance': 'Performance Metrics'
    }

    name_lower = name.lower()
    for key, tag in topic_map.items():
        if key in name_lower:
            return tag

    # Default fallback
    return 'NFL Analytics'


def generate_publish_info(article_dir, name, geo_data, model_name):
    """
    Generate MEDIUM_PUBLISH_INFO_{name}.md file.

    Args:
        article_dir: Path to article directory
        name: Article name (e.g., "draft_roi")
        geo_data: Dict with GEO optimization results
            - score: int (e.g., 96)
            - grade: str (e.g., "A")
            - meta_description: str (≤200 chars)
            - social_summary: str (≤280 chars)
            - strengths: str (bullet list)
            - improvements: str (bullet list)
        model_name: Current Claude model name

    Returns:
        (bool, str): (success, error_message or info_path)
    """
    md_path = os.path.join(article_dir, f"{name}_medium_draft.md")
    info_path = os.path.join(article_dir, f"MEDIUM_PUBLISH_INFO_{name}.md")
    template_path = os.path.join(
        os.path.dirname(__file__),
        "templates",
        "MEDIUM_PUBLISH_INFO_template.md"
    )

    # Extract article metadata
    title = extract_h1(md_path)
    image_urls = extract_image_urls(md_path)
    topic_tag = infer_topic_tag(name)

    # Format image list
    if image_urls:
        images_text = "\n".join([f"- {url}" for url in image_urls])
    else:
        images_text = "- (No images found in markdown)"

    # Read template
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except FileNotFoundError:
        return False, f"Template not found: {template_path}"
    except Exception as e:
        return False, f"Error reading template: {str(e)}"

    # Fill template with data
    content = template.format(
        title=title,
        meta_description=geo_data.get('meta_description', '(Generate via GEO optimization)'),
        social_summary=geo_data.get('social_summary', '(Generate via GEO optimization)'),
        topic_tag=topic_tag,
        images=images_text,
        score=geo_data.get('score', 0),
        grade=geo_data.get('grade', 'N/A'),
        strengths=geo_data.get('strengths', '- (Run GEO optimization to populate)'),
        improvements=geo_data.get('improvements', '- (Run GEO optimization to populate)'),
        model_name=model_name
    )

    # Write file
    try:
        with open(info_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return False, f"Error writing info file: {str(e)}"

    return True, info_path


if __name__ == "__main__":
    # Test with sample data
    test_geo_data = {
        'score': 96,
        'grade': 'A',
        'meta_description': 'Test description',
        'social_summary': 'Test summary',
        'strengths': '- Strong data citations\n- Clear headings',
        'improvements': '- Added FAQ section'
    }

    success, result = generate_publish_info(
        "../../article",
        "test",
        test_geo_data,
        "Claude Sonnet 4.5"
    )

    if success:
        print(f"✅ Info file generated: {result}")
    else:
        print(f"❌ Error: {result}")
