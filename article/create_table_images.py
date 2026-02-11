"""
Extract markdown tables from TE article and convert to PNG images for Medium import.

This script parses te_market_inefficiency_medium_draft.md, extracts all markdown tables,
and converts them to styled PNG images suitable for Medium's import process.
"""

import re
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def extract_markdown_tables(md_text):
    """Extract all markdown tables from the markdown text."""
    # Split by lines
    lines = md_text.split('\n')

    tables = []
    current_table = []
    in_table = False
    table_index = 0

    for i, line in enumerate(lines):
        # Check if line is part of a markdown table (starts with |)
        if line.strip().startswith('|'):
            in_table = True
            current_table.append(line.strip())
        else:
            # If we were in a table and now we're not, save it
            if in_table and current_table:
                tables.append({
                    'lines': current_table,
                    'start_line': i - len(current_table),
                    'index': table_index
                })
                table_index += 1
                current_table = []
                in_table = False

    # Don't forget the last table if file ends with a table
    if in_table and current_table:
        tables.append({
            'lines': current_table,
            'start_line': len(lines) - len(current_table),
            'index': table_index
        })

    return tables

def parse_markdown_table_to_df(table_lines):
    """Convert markdown table lines to pandas DataFrame."""
    # Remove leading/trailing pipes and split by pipe
    rows = []
    for line in table_lines:
        # Skip separator line (contains dashes)
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue

        # Split by pipe and clean
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(cells)

    # First row is header
    if len(rows) > 0:
        df = pd.DataFrame(rows[1:], columns=rows[0])
        return df
    return None

def style_table_for_image(df, title, filename):
    """Create a styled table image from DataFrame."""
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, len(df) * 0.5 + 1))
    ax.axis('tight')
    ax.axis('off')

    # Add title
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    # Create table
    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='left',
        loc='center',
        colWidths=[0.25] * len(df.columns)
    )

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 2)

    # Style header row
    for i in range(len(df.columns)):
        cell = table[(0, i)]
        cell.set_facecolor('#1f77b4')
        cell.set_text_props(weight='bold', color='white')

    # Alternate row colors for readability
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#f0f0f0')
            else:
                cell.set_facecolor('#ffffff')

            # Bold key cells (those with ** in markdown)
            text = cell.get_text().get_text()
            if '**' in text:
                # Remove markdown bold markers
                clean_text = text.replace('**', '')
                cell.get_text().set_text(clean_text)
                cell.get_text().set_weight('bold')

    # Save with tight layout
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"[OK] Created: {filename}")

def main():
    # Read the markdown file
    md_path = Path('article/te_market_inefficiency_medium_draft.md')
    md_text = md_path.read_text(encoding='utf-8')

    # Extract all tables
    tables = extract_markdown_tables(md_text)
    print(f"Found {len(tables)} markdown tables in the article\n")

    # Define table titles and filenames
    table_metadata = [
        {
            'title': 'Draft ROI by Round - Average Value Scores',
            'filename': 'article/images/te_market_inefficiency/table_1_draft_roi.png',
            'alt_text': 'Table: Draft ROI by Round showing average value scores for TEs by draft round'
        },
        {
            'title': 'Career Arc by Years Since Draft',
            'filename': 'article/images/te_market_inefficiency/table_2_career_arc.png',
            'alt_text': 'Table: TE Career Arc showing value score by years of experience'
        },
        {
            'title': 'Top 10 TE Bargains (Career Average Value)',
            'filename': 'article/images/te_market_inefficiency/table_3_top_bargains.png',
            'alt_text': 'Table: Top 10 TE bargains ranked by career average value score'
        },
        {
            'title': 'Top 10 First-Round TE Busts',
            'filename': 'article/images/te_market_inefficiency/table_4_top_busts.png',
            'alt_text': 'Table: Top 10 first-round TE busts with negative career value scores'
        },
        {
            'title': 'Blocking vs Receiving TE Value Comparison',
            'filename': 'article/images/te_market_inefficiency/table_5_role_comparison.png',
            'alt_text': 'Table: Blocking vs Receiving TEs average value score comparison'
        }
    ]

    # Process each table
    for i, table in enumerate(tables):
        if i >= len(table_metadata):
            print(f"Warning: Table {i+1} has no metadata, skipping")
            continue

        metadata = table_metadata[i]

        # Parse to DataFrame
        df = parse_markdown_table_to_df(table['lines'])

        if df is not None and not df.empty:
            # Create image
            style_table_for_image(df, metadata['title'], metadata['filename'])
        else:
            print(f"[FAIL] Failed to parse table {i+1}")

    print(f"\n[OK] Created {len(tables)} table images")
    print("\nNext steps:")
    print("1. Review table images in article/images/te_market_inefficiency/")
    print("2. Run update script to replace markdown tables with image references")

if __name__ == '__main__':
    main()
