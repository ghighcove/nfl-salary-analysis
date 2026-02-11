"""
Generate chart images for Draft ROI Medium article
"""
import sys
sys.path.insert(0, '..')

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Load data
DATA_DIR = Path('../data')
scored = pd.read_parquet(DATA_DIR / 'scored.parquet', engine='fastparquet')
rosters = pd.read_parquet(DATA_DIR / 'rosters.parquet', engine='fastparquet')

# Get draft info
draft_info = rosters[rosters['draft_number'].notna()][['player_id', 'player_name', 'draft_number', 'draft_club', 'rookie_year']].drop_duplicates('player_id').copy()
draft_info['draft_number'] = pd.to_numeric(draft_info['draft_number'], errors='coerce')
draft_info['draft_round'] = ((draft_info['draft_number'] - 1) // 32 + 1).astype('Int64')
draft_info['draft_round'] = draft_info['draft_round'].clip(upper=7)

# Merge and filter to rookie contracts
df = scored.merge(draft_info, on=['player_id', 'player_name'], how='inner')
df['years_since_draft'] = df['season'] - df['rookie_year']
rookie_contracts = df[(df['years_since_draft'] >= 0) & (df['years_since_draft'] <= 3)].copy()

print("Data loaded successfully")
print(f"Rookie contracts: {len(rookie_contracts):,} player-seasons")

# Chart 1: Average Value Score by Draft Round (Bar Chart)
print("\nGenerating Chart 1: Draft Round Value...")
round_value = rookie_contracts.groupby('draft_round').agg(
    avg_value_score=('value_score', 'mean'),
    count=('value_score', 'size'),
    pct_bargains=('is_bargain', lambda x: x.sum() / len(x) * 100),
).reset_index()

fig1 = go.Figure()
fig1.add_trace(go.Bar(
    x=round_value['draft_round'],
    y=round_value['avg_value_score'],
    text=round_value['avg_value_score'].round(2),
    textposition='outside',
    marker_color=['#2ecc71' if v > 0.4 else '#3498db' if v > 0 else '#e74c3c' for v in round_value['avg_value_score']],
    hovertemplate='<b>Round %{x}</b><br>Avg Value: %{y:.2f}<br>N=%{customdata[0]:,}<br>% Bargains: %{customdata[1]:.1f}%<extra></extra>',
    customdata=round_value[['count', 'pct_bargains']]
))
fig1.update_layout(
    title='Average Value Score by Draft Round (Rookie Contract Years)',
    xaxis_title='Draft Round',
    yaxis_title='Average Value Score',
    width=900,
    height=500,
    showlegend=False,
    font=dict(size=14),
    plot_bgcolor='white',
    paper_bgcolor='white'
)
fig1.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig1.write_image('draft-round-value.png', width=900, height=500, scale=2)
print("* Chart 1 saved: draft-round-value.png")

# Chart 2: Position × Round Heatmap
print("\nGenerating Chart 2: Position-Round Heatmap...")
round_position_value = rookie_contracts.groupby(['draft_round', 'pos_group']).agg(
    avg_value_score=('value_score', 'mean'),
    count=('value_score', 'size'),
).reset_index()
round_position_value = round_position_value[round_position_value['count'] >= 10].copy()

heatmap_data = round_position_value.pivot(index='pos_group', columns='draft_round', values='avg_value_score')

fig2 = px.imshow(
    heatmap_data,
    labels=dict(x="Draft Round", y="Position Group", color="Avg Value Score"),
    x=heatmap_data.columns,
    y=heatmap_data.index,
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=0,
    aspect='auto',
    title='Average Value Score: Draft Round × Position Group'
)
fig2.update_layout(
    width=900,
    height=600,
    font=dict(size=14),
    xaxis=dict(side='top')
)
fig2.update_traces(text=heatmap_data.round(2), texttemplate='%{text}', textfont_size=12)
fig2.write_image('position-round-heatmap.png', width=900, height=600, scale=2)
print("* Chart 2 saved: position-round-heatmap.png")

# Chart 3: Top 10 Late-Round Steals (Horizontal Bar)
print("\nGenerating Chart 3: Late-Round Steals...")
late_round_steals = rookie_contracts[rookie_contracts['draft_round'] >= 3].nlargest(10, 'value_score')

fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=late_round_steals['value_score'],
    y=late_round_steals['player_name'] + ' (' + late_round_steals['pos_group'] + ', Rd ' + late_round_steals['draft_round'].astype(str) + ')',
    orientation='h',
    marker=dict(
        color=late_round_steals['value_score'],
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(title="Value Score")
    ),
    text=late_round_steals['value_score'].round(2),
    textposition='outside',
    hovertemplate='<b>%{y}</b><br>Value Score: %{x:.2f}<br>Pick #%{customdata}<extra></extra>',
    customdata=late_round_steals['draft_number']
))
fig3.update_layout(
    title='Top 10 Late-Round Draft Steals (Rounds 3+)',
    xaxis_title='Value Score',
    yaxis_title='',
    width=900,
    height=600,
    font=dict(size=12),
    yaxis={'categoryorder': 'total ascending'},
    plot_bgcolor='white',
    paper_bgcolor='white'
)
fig3.write_image('late-round-steals.png', width=900, height=600, scale=2)
print("* Chart 3 saved: late-round-steals.png")

# Chart 4: Position Strategy Summary (Enhanced Table Visualization)
print("\nGenerating Chart 4: Position Strategy Table...")
position_strategy = {
    'Position': ['QB', 'RB', 'WR', 'TE', 'OL', 'DL', 'LB', 'DB'],
    'Best Rounds': ['1-2, 5', '2-3', '2-4', '2, 5', '2-3', '2-4', '3-4', '2-3'],
    'Avoid': ['3-4, 6', '1', '7', '1', '1', '7', '1, 7', '1'],
    'Best Value': ['+0.62 (Rd 5)', '+0.55 (Rd 3)', '+0.55 (Rd 2)', '+0.58 (Rd 2)', '+0.30', '+0.41', '+0.35', '+0.60 (Rd 2-3)']
}

fig4 = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Position</b>', '<b>Best Rounds</b>', '<b>Avoid</b>', '<b>Avg Value</b>'],
        fill_color='#2c3e50',
        font=dict(color='white', size=14),
        align='left',
        height=40
    ),
    cells=dict(
        values=[position_strategy['Position'],
                position_strategy['Best Rounds'],
                position_strategy['Avoid'],
                position_strategy['Best Value']],
        fill_color=[['white', '#ecf0f1']*4],
        font=dict(size=13),
        align='left',
        height=35
    )
)])
fig4.update_layout(
    title='Optimal Draft Strategy by Position',
    width=900,
    height=500,
    font=dict(size=14)
)
fig4.write_image('position-strategy-table.png', width=900, height=500, scale=2)
print("* Chart 4 saved: position-strategy-table.png")

print("\n" + "="*60)
print("All 4 charts generated successfully!")
print("="*60)
print("\nFiles created in article/ directory:")
print("  - draft-round-value.png")
print("  - position-round-heatmap.png")
print("  - late-round-steals.png")
print("  - position-strategy-table.png")
