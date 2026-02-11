#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main workflow orchestration for NFL article publishing.

Usage:
    python main.py <article_name>

Example:
    python main.py draft_roi
"""
import os
import sys
import subprocess
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Import skill modules
from html_exporter import export_html, extract_image_paths
from geo_metadata import generate_publish_info


def get_project_root():
    """Get the project root directory (where article/ folder lives)."""
    # From .claude/skills/nfl-article-publish/ to project root
    # Path is: G:\ai\nfl\.claude\skills\nfl-article-publish\main.py
    # Need to go up 3 levels to get to G:\ai\nfl
    skill_dir = Path(__file__).parent.resolve()
    return str(skill_dir.parent.parent.parent)


def validate_article(article_dir, name):
    """
    Validate article exists and all dependencies are ready.

    Returns:
        (bool, str): (success, error_message)
    """
    md_path = os.path.join(article_dir, f"{name}_medium_draft.md")

    # Check markdown file exists
    if not os.path.exists(md_path):
        return False, f"❌ Markdown file not found: {md_path}\n\nCreate the markdown file first with your article content."

    # Read markdown to check for images
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract image paths
        images = extract_image_paths(content)

        # Check if images exist (only for local paths, skip URLs)
        missing_images = []
        for img_path in images:
            if not img_path.startswith('http'):
                # Local path - check existence
                full_path = os.path.join(article_dir, img_path)
                if not os.path.exists(full_path):
                    missing_images.append(img_path)

        if missing_images:
            return False, f"❌ Missing image files:\n" + "\n".join([f"  - {img}" for img in missing_images])

    except Exception as e:
        return False, f"❌ Error reading markdown file: {str(e)}"

    # Check git status
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            cwd=get_project_root()
        )

        if result.returncode == 0 and result.stdout.strip():
            # Check if the dirty files are related to this article
            dirty_files = result.stdout.strip().split('\n')
            article_related = [f for f in dirty_files if name in f or 'article/' in f]

            if article_related:
                print("⚠️  Warning: Git working tree has uncommitted changes:")
                for file_line in article_related:
                    print(f"  {file_line}")
                print("\nThese changes will be included in the commit.\n")

    except Exception:
        # Git check is non-critical
        pass

    return True, ""


def git_commit_and_push(article_dir, name, geo_score):
    """
    Commit article files and push to GitHub.

    Returns:
        (bool, str): (success, error_message)
    """
    project_root = get_project_root()

    files_to_commit = [
        f"article/{name}_medium_draft.md",
        f"article/{name}_medium_ready.html",
        f"article/MEDIUM_PUBLISH_INFO_{name}.md"
    ]

    try:
        # Stage files
        for file_path in files_to_commit:
            result = subprocess.run(
                ['git', 'add', file_path],
                capture_output=True,
                text=True,
                cwd=project_root
            )
            if result.returncode != 0:
                print(f"⚠️  Warning: Could not stage {file_path}: {result.stderr}")

        # Create commit message
        topic = name.replace('_', ' ').title()
        commit_msg = f"feat: Add {topic} Medium article (GEO: {geo_score}/100)"

        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        if result.returncode != 0:
            # Check if error is "nothing to commit"
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("ℹ️  No new changes to commit (files may already be committed)")
            else:
                return False, f"Git commit failed: {result.stderr}"

        # Push to remote
        print("\n📤 Pushing to GitHub...")
        result = subprocess.run(
            ['git', 'push', 'origin', 'master'],
            capture_output=True,
            text=True,
            cwd=project_root
        )

        if result.returncode != 0:
            # Try auth refresh and retry
            print("⚠️  Push failed, refreshing GitHub auth...")
            subprocess.run(
                ['gh', 'auth', 'refresh', '-s', 'workflow'],
                capture_output=True,
                cwd=project_root
            )

            # Retry push
            result = subprocess.run(
                ['git', 'push', 'origin', 'master'],
                capture_output=True,
                text=True,
                cwd=project_root
            )

            if result.returncode != 0:
                return False, f"Git push failed after auth refresh: {result.stderr}"

        print("✅ Changes pushed to GitHub")
        return True, ""

    except Exception as e:
        return False, f"Git operation error: {str(e)}"


def generate_urls(name):
    """Generate all article URLs."""
    return {
        'github_pages': f"https://ghighcove.github.io/nfl-salary-analysis/article/{name}_medium_ready.html",
        'github_markdown': f"https://github.com/ghighcove/nfl-salary-analysis/blob/master/article/{name}_medium_draft.md",
        'publish_info': f"article/MEDIUM_PUBLISH_INFO_{name}.md"
    }


def print_urls(urls):
    """Print formatted URL output."""
    print("\n" + "="*70)
    print("📄 Article URLs Generated")
    print("="*70)
    print(f"\n**GitHub Pages (Medium Import URL):**")
    print(f"{urls['github_pages']}")
    print(f"\n**Browser-Friendly Markdown:**")
    print(f"{urls['github_markdown']}")
    print(f"\n**Publishing Info:**")
    print(f"{urls['publish_info']}")
    print("\n" + "="*70 + "\n")


def main(article_name):
    """
    Main workflow execution.

    Args:
        article_name: Name of the article (e.g., "draft_roi")
    """
    project_root = get_project_root()
    article_dir = os.path.join(project_root, "article")

    print(f"\n🚀 Starting NFL Article Publishing Workflow")
    print(f"Article: {article_name}")
    print(f"Project: {project_root}\n")

    # Phase 1: Pre-Flight Checks
    print("Phase 1: Pre-Flight Checks")
    print("-" * 40)
    success, error = validate_article(article_dir, article_name)
    if not success:
        print(error)
        return 1

    print("✅ Article file validated")
    print("✅ All images found")
    print("✅ Pre-flight checks passed\n")

    # Phase 2: GEO Optimization (Note for skill executor)
    print("Phase 2: GEO Optimization")
    print("-" * 40)
    print("⏭️  GEO optimization should be run by Claude via /seo-for-llms skill")
    print("    This script expects GEO data to be provided by the skill executor.\n")

    # For standalone testing, use placeholder data
    geo_data = {
        'score': 0,
        'grade': 'Pending',
        'meta_description': '(Run GEO optimization to generate)',
        'social_summary': '(Run GEO optimization to generate)',
        'strengths': '- (Run GEO optimization to populate)',
        'improvements': '- (Run GEO optimization to populate)'
    }

    # Phase 3: Generate Publishing Info
    print("Phase 3: Generate Publishing Info")
    print("-" * 40)
    model_name = "Claude Sonnet 4.5"  # Will be replaced by skill executor
    success, result = generate_publish_info(
        article_dir,
        article_name,
        geo_data,
        model_name
    )

    if not success:
        print(f"❌ {result}")
        return 1

    print(f"✅ Publishing info generated: {os.path.basename(result)}\n")

    # Phase 4: HTML Export
    print("Phase 4: HTML Export")
    print("-" * 40)
    success, result = export_html(article_dir, article_name)

    if not success:
        print(f"❌ {result}")
        return 1

    print(f"✅ HTML exported: {os.path.basename(result)}\n")

    # Phase 5: Git Workflow
    print("Phase 5: Git Workflow")
    print("-" * 40)
    success, error = git_commit_and_push(article_dir, article_name, geo_data['score'])

    if not success:
        print(f"❌ {error}")
        print("\nℹ️  You can manually push with:")
        print(f"   cd {project_root}")
        print("   git push origin master\n")
        # Continue to URL output even if push fails
    else:
        print("⏳ Waiting 10 seconds for GitHub Pages to rebuild...")
        import time
        time.sleep(10)

    # Phase 6: URL Output (Always)
    urls = generate_urls(article_name)
    print_urls(urls)

    print("✅ Workflow Complete!")
    print("\nNext Steps:")
    print("1. Review article at GitHub Pages URL")
    print("2. Import to Medium using the GitHub Pages URL (not raw.githubusercontent.com)")
    print("3. Check MEDIUM_PUBLISH_INFO_{}_md for metadata and checklist\n".format(article_name))

    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <article_name>")
        print("Example: python main.py draft_roi")
        sys.exit(1)

    article_name = sys.argv[1]
    sys.exit(main(article_name))
