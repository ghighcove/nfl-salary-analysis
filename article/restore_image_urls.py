import re
from pathlib import Path

def restore_image_urls():
    """Restore raw.githubusercontent.com URLs for table images"""

    html_path = Path('te_market_inefficiency_medium_ready.html')
    html = html_path.read_text(encoding='utf-8')

    # Table image mapping
    tables = {
        1: ('table_1_draft_roi.png', 'Table: Draft ROI by Round showing average value scores for TEs by draft round'),
        2: ('table_2_career_arc.png', 'Table: TE Career Arc showing value score by years of experience'),
        3: ('table_3_top_bargains.png', 'Table: Top 10 TE bargains ranked by career average value score'),
        4: ('table_4_top_busts.png', 'Table: Top 10 first-round TE busts with negative career value scores'),
        5: ('table_5_role_comparison.png', 'Table: Blocking vs Receiving TEs average value score comparison')
    }

    # Convert table image URLs to raw.githubusercontent.com format
    for num, (filename, alt_text) in tables.items():
        # Match base64, raw.githubusercontent.com, OR GitHub Pages URLs
        base64_pattern = rf'<img src="data:image/png;base64,[^"]*" alt="{re.escape(alt_text)}" />'
        raw_github_pattern = rf'<img src="https://raw\.githubusercontent\.com/[^"]*/{re.escape(filename)}" alt="{re.escape(alt_text)}" />'
        gh_pages_pattern = rf'<img src="https://ghighcove\.github\.io/[^"]*/{re.escape(filename)}" alt="{re.escape(alt_text)}" />'

        url = f'https://raw.githubusercontent.com/ghighcove/nfl-salary-analysis/master/article/images/te_market_inefficiency/{filename}'
        replacement = f'<img src="{url}" alt="{alt_text}" />'

        # Try all three patterns
        if re.search(base64_pattern, html):
            html = re.sub(base64_pattern, replacement, html)
            print(f"Converted base64 to raw.githubusercontent.com for {filename}")
        elif re.search(gh_pages_pattern, html):
            html = re.sub(gh_pages_pattern, replacement, html)
            print(f"Converted GitHub Pages to raw.githubusercontent.com for {filename}")
        elif re.search(raw_github_pattern, html):
            print(f"Already using raw.githubusercontent.com for {filename}")
        else:
            print(f"No match found for {filename}")

    html_path.write_text(html, encoding='utf-8')
    print(f"\nHTML file updated - size now: {len(html)} bytes")

if __name__ == '__main__':
    restore_image_urls()
