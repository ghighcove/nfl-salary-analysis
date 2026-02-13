"""
Generate PNG images for tables in RB Economics article.
Medium doesn't render HTML tables well, so we convert to images.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# Ensure output directory exists
output_dir = Path('article/images/rb_economics')
output_dir.mkdir(parents=True, exist_ok=True)

def create_table_image(data, headers, filename, title=""):
    """Create a clean, professional table PNG."""
    fig, ax = plt.subplots(figsize=(10, len(data) * 0.5 + 1))
    ax.axis('tight')
    ax.axis('off')

    # Create table
    table = ax.table(
        cellText=data,
        colLabels=headers,
        cellLoc='left',
        loc='center',
        colWidths=[0.25] * len(headers)
    )

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2)

    # Header styling (bold white text on dark background)
    for i in range(len(headers)):
        cell = table[(0, i)]
        cell.set_facecolor('#2C3E50')
        cell.set_text_props(weight='bold', color='white')

    # Data row styling (alternating colors)
    for i in range(1, len(data) + 1):
        for j in range(len(headers)):
            cell = table[(i, j)]
            if i % 2 == 0:
                cell.set_facecolor('#ECF0F1')
            else:
                cell.set_facecolor('white')
            cell.set_edgecolor('#BDC3C7')

    # Add title if provided
    if title:
        plt.title(title, fontsize=14, weight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(output_dir / filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"[OK] Generated: {filename}")


# Table 1: Draft Round Value Comparison
table1_data = [
    ['Round 3', '+0.555', '87', '8.0%'],
    ['Round 2', '+0.526', '76', '7.9%'],
    ['Round 5', '+0.404', '88', '5.7%'],
    ['Round 6', '+0.346', '65', '5.2%'],
    ['Round 4', '+0.332', '94', '4.3%'],
    ['Round 7', '+0.213', '87', '2.3%'],
    ['Round 1', '+0.015', '52', '1.9%'],
]
table1_headers = ['Draft Round', 'Avg Value Score', 'Sample Size', '% Bargains']
create_table_image(
    table1_data,
    table1_headers,
    'table_1_draft_round_comparison.png',
    'Average Value Score by Draft Round (RB Rookie Contract Years)'
)


# Table 2: RB Career Arc by Year
table2_data = [
    ['Year 1', '+0.505', '338'],
    ['Year 2', '+0.504', '282'],
    ['Year 3', '+0.069', '225'],
    ['Year 4', '-0.074', '175'],
    ['Year 5', '-0.156', '121'],
    ['Year 6+', '-0.300 avg', '108'],
]
table2_headers = ['Years Since Draft', 'Avg Value Score', 'Sample Size']
create_table_image(
    table2_data,
    table2_headers,
    'table_2_career_arc.png',
    'RB Career Arc: Value Score by Years of Experience'
)


# Table 3: Top 10 RB Bargains
table3_data = [
    ['Jahmyr Gibbs', '1', '12', '+1.451', '2'],
    ['James Cook', '2', '63', '+1.363', '3'],
    ['Jordan Howard', '5', '150', '+1.159', '5'],
    ['Marlon Mack', '5', '143', '+1.147', '3'],
    ['Kyren Williams', '6', '164', '+1.138', '3'],
    ['Dameon Pierce', '4', '107', '+1.087', '2'],
    ['Kenneth Walker III', '2', '41', '+1.073', '3'],
    ['Rachaad White', '3', '91', '+1.069', '3'],
    ['Tony Pollard', '4', '128', '+1.039', '3'],
    ['Aaron Jones', '5', '182', '+1.033', '4'],
]
table3_headers = ['Player', 'Draft Round', 'Pick #', 'Avg Value Score', 'Seasons']
create_table_image(
    table3_data,
    table3_headers,
    'table_3_top_bargains.png',
    'Top 10 RB Bargains (Career Average Value)'
)


# Table 4: Top 10 First-Round RB Busts
table4_data = [
    ['Marshawn Lynch', '12', '-2.057', '3', '5x Pro Bowl, Super Bowl Champion'],
    ['Jonathan Stewart', '13', '-2.052', '3', 'Super Bowl Finalist'],
    ['Christian McCaffrey', '8', '-2.051', '8', '4x Pro Bowl, All-Pro'],
    ['Ezekiel Elliott', '4', '-1.755', '9', '3x Pro Bowl, 2x Rushing Leader'],
    ['Doug Martin', '31', '-0.968', '4', '2x Pro Bowl'],
]
table4_headers = ['Player', 'Pick #', 'Avg Value Score', 'Seasons', 'Career Accolades']
create_table_image(
    table4_data,
    table4_headers,
    'table_4_top_busts.png',
    'Top 10 First-Round RB Busts (Career Average Value)'
)


# Table 5: Positional Replaceability
table5_data = [
    ['UDFA', '+0.065', '375'],
    ['Drafted', '-0.016', '874'],
]
table5_headers = ['Status', 'Avg Value Score', 'Sample Size']
create_table_image(
    table5_data,
    table5_headers,
    'table_5_replaceability.png',
    'Positional Replaceability: Drafted vs. UDFA Running Backs'
)

print("\n[OK] All 5 table images generated successfully!")
print(f"[OK] Saved to: {output_dir.absolute()}")
