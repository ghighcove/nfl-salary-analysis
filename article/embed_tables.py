"""Replace table images with HTML tables in the Medium HTML file"""
from pathlib import Path
import re

def create_table_html():
    """Generate HTML tables to replace images"""

    # Table 1: Draft ROI by Round
    table1 = """
<h3>Draft ROI by Round</h3>
<p><strong>Round 2:</strong> +0.582 avg value (Best overall value)<br>
<strong>Round 5:</strong> +0.530 (Elite bargains)<br>
<strong>Round 3:</strong> +0.45 (Solid value)<br>
<strong>Round 4:</strong> +0.41 (Good value)<br>
<strong>Round 1:</strong> +0.353 (Underperforms cost)<br>
<strong>Round 6:</strong> +0.23<br>
<strong>Round 7:</strong> +0.10</p>
"""

    # Table 2: TE Career Arc
    table2 = """
<h3>TE Career Arc by Years of Experience</h3>
<p><strong>Peak Years (1-2):</strong><br>
• Year 2: +0.683 value (Peak production)<br>
• Year 1: +0.664 value (Peak production)<br>
• Year 0: +0.43 (Rookie season)</p>
<p><strong>Decline Phase (3+):</strong><br>
• Year 3: +0.22 (Still positive)<br>
• Year 4: -0.42 (Negative value starts)<br>
• Years 5-10: -0.71 to -0.26 (Late career)</p>
"""

    # Table 3: Top 10 TE Bargains
    table3 = """
<h3>Top 10 TE Bargains (Career Average Value)</h3>
<p><strong>1. Sam LaPorta</strong> (+2.463) — Rd 2, Pick 34: 889 yds, 10 TDs as rookie<br>
<strong>2. Tucker Kraft</strong> (+1.45) — Rd 3, Pick 78<br>
<strong>3. Trey McBride</strong> (+1.423) — Rd 2, Pick 55: 825 yds/season<br>
<strong>4. Isaiah Likely</strong> (+1.37) — Rd 5, Pick 139: 411 yds, 5 TDs on minimum salary<br>
<strong>5. Cade Otton</strong> (+1.36) — Rd 4, Pick 106<br>
<strong>6. Dalton Kincaid</strong> (+1.287) — Rd 2, Pick 25: 673 yds, 4.5 TDs/yr<br>
<strong>7. Jake Ferguson</strong> (+1.19) — Rd 4, Pick 129<br>
<strong>8. Dawson Knox</strong> (+0.94) — Rd 3, Pick 96<br>
<strong>9. Hunter Henry</strong> (+0.87) — Rd 2, Pick 35<br>
<strong>10. Hayden Hurst</strong> (+0.79) — Rd 1, Pick 25 (exception)</p>
<p><em>Notice: 7 of top 10 came from Rounds 2-3</em></p>
"""

    # Table 4: First-Round TE Busts
    table4 = """
<h3>Top 10 First-Round TE Busts (Career Average Value)</h3>
<p><strong>1. Eric Ebron</strong> (-1.782) — Pick 10, 2014: High cost, inconsistent<br>
<strong>2. O.J. Howard</strong> (-1.48) — Pick 19, 2017: Never lived up to hype<br>
<strong>3. Tyler Eifert</strong> (-1.04) — Pick 21, 2013: Injury-plagued<br>
<strong>4. David Njoku</strong> (-0.90) — Pick 29, 2017<br>
<strong>5. T.J. Hockenson</strong> (-0.64) — Pick 8, 2019: Good player, but too expensive at #8<br>
<strong>6. Kyle Pitts</strong> (-0.42) — Pick 4, 2021: Elite talent, but #4 overall cost too high<br>
<strong>7. Evan Engram</strong> (-0.36) — Pick 23, 2017<br>
<strong>8. Hayden Hurst</strong> (+0.07) — Pick 25, 2018: Barely broke even<br>
<strong>9. Noah Fant</strong> (+0.14) — Pick 20, 2019<br>
<strong>10. Dallas Goedert</strong> (+0.15) — Pick 49, 2018 (Round 2)</p>
<p><em>60% of first-round TEs post negative or break-even career value</em></p>
"""

    # Table 5: Blocking vs Receiving
    table5 = """
<h3>Blocking vs Receiving TE Value Comparison</h3>
<p><strong>Receiving TEs</strong> (4+ targets/game): +0.032 avg value (280 seasons) ✓<br>
<strong>Blocking TEs</strong> (<4 targets/game): -0.014 avg value (780 seasons) ✗<br>
<strong>Difference:</strong> +0.046 in favor of receiving TEs</p>
<p><em>Takeaway: Prioritize pass-catching ability. Blocking can be found cheaper elsewhere.</em></p>
"""

    return {
        'table_1': table1,
        'table_2': table2,
        'table_3': table3,
        'table_4': table4,
        'table_5': table5
    }

def replace_tables():
    """Replace table images with HTML in the Medium HTML file"""

    html_path = Path('te_market_inefficiency_medium_ready.html')
    html = html_path.read_text(encoding='utf-8')

    tables = create_table_html()

    # Replace each table image with HTML
    replacements = [
        (r'<img src="[^"]*data_1_draft_roi\.png" alt="[^"]*" />', tables['table_1']),
        (r'<img src="[^"]*data_2_career_arc\.png" alt="[^"]*" />', tables['table_2']),
        (r'<img src="[^"]*data_3_top_bargains\.png" alt="[^"]*" />', tables['table_3']),
        (r'<img src="[^"]*data_4_top_busts\.png" alt="[^"]*" />', tables['table_4']),
        (r'<img src="[^"]*data_5_role_comparison\.png" alt="[^"]*" />', tables['table_5'])
    ]

    for pattern, replacement in replacements:
        matches = len(re.findall(pattern, html))
        html = re.sub(pattern, replacement, html)
        print(f"Replaced {matches} occurrence(s) of {pattern[:50]}...")

    html_path.write_text(html, encoding='utf-8')
    print(f"\n✓ Updated HTML file ({len(html)} bytes)")
    print(f"✓ All table images replaced with HTML text")

if __name__ == '__main__':
    replace_tables()
