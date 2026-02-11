"""Export RB Economics visualizations to PNG files for article."""

import sys
sys.path.insert(0, '..')

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set paths
DATA_DIR = Path('../data')
OUTPUT_DIR = Path('../article/images/rb_economics')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Loading data...")
scored = pd.read_parquet(DATA_DIR / 'scored.parquet', engine='fastparquet')
rosters = pd.read_parquet(DATA_DIR / 'rosters.parquet', engine='fastparquet')

# Get draft info
draft_info = rosters[rosters['draft_number'].notna()][['player_id', 'player_name', 'draft_number', 'draft_club', 'rookie_year']].drop_duplicates('player_id').copy()
draft_info['draft_number'] = pd.to_numeric(draft_info['draft_number'], errors='coerce')
draft_info['draft_round'] = ((draft_info['draft_number'] - 1) // 32 + 1).astype('Int64')
draft_info['draft_round'] = draft_info['draft_round'].clip(upper=7)

# Filter to RBs
rb_scored = scored[scored['pos_group'] == 'RB'].copy()
rb_df = rb_scored.merge(draft_info, on=['player_id', 'player_name'], how='left')
rb_df['years_since_draft'] = rb_df['season'] - rb_df['rookie_year']

print(f"RB player-seasons: {len(rb_df):,}")

# ========================================
# VIZ 1: Career Arc
# ========================================
print("\n1. Generating career_arc.png...")
rb_career = rb_df[rb_df['years_since_draft'].notna() & (rb_df['years_since_draft'] >= 0)].copy()
rb_career['years_since_draft'] = rb_career['years_since_draft'].astype(int)
rb_career = rb_career[rb_career['years_since_draft'] <= 10].copy()

career_arc = rb_career.groupby('years_since_draft').agg(
    avg_value=('value_score', 'mean'),
    median_value=('value_score', 'median'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    count=('value_score', 'size')
).reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=career_arc['years_since_draft'],
    y=career_arc['avg_value'],
    mode='lines+markers',
    name='Avg Value Score',
    marker=dict(size=10),
    line=dict(width=3),
    hovertemplate='<b>Year %{x}</b><br>Avg Value: %{y:.2f}<br>N=%{customdata:,}<extra></extra>',
    customdata=career_arc['count']
))
fig.update_layout(
    title='<b>RB Career Arc: Value Score by Years of Experience</b><br><sub>When Do Running Backs Peak?</sub>',
    xaxis_title='Years Since Draft',
    yaxis_title='Average Value Score',
    width=900,
    height=500,
    hovermode='x'
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.write_image(OUTPUT_DIR / 'career_arc.png')
print("   [OK] Saved career_arc.png")

# ========================================
# VIZ 2: Draft ROI by Round
# ========================================
print("\n2. Generating draft_roi_by_round.png...")
rb_rookie = rb_career[(rb_career['years_since_draft'] >= 0) & (rb_career['years_since_draft'] <= 3)].copy()

rb_draft_roi = rb_rookie.groupby('draft_round').agg(
    avg_value=('value_score', 'mean'),
    median_value=('value_score', 'median'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    count=('value_score', 'size'),
    pct_bargains=('is_bargain', lambda x: x.sum() / len(x) * 100)
).reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=rb_draft_roi['draft_round'],
    y=rb_draft_roi['avg_value'],
    text=rb_draft_roi['avg_value'].round(2),
    textposition='outside',
    marker_color=['green' if v > 0.3 else 'orange' if v > 0 else 'red' for v in rb_draft_roi['avg_value']],
    hovertemplate='<b>Round %{x}</b><br>Avg Value: %{y:.2f}<br>N=%{customdata[0]:,}<br>% Bargains: %{customdata[1]:.1f}%<extra></extra>',
    customdata=rb_draft_roi[['count', 'pct_bargains']]
))
fig.update_layout(
    title='<b>RB Draft ROI: Average Value by Round</b><br><sub>Rookie Contract Years Only | Why First-Round RBs Are Poor Investments</sub>',
    xaxis_title='Draft Round',
    yaxis_title='Average Value Score',
    width=800,
    height=500,
    showlegend=False
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.write_image(OUTPUT_DIR / 'draft_roi_by_round.png')
print("   [OK] Saved draft_roi_by_round.png")

# ========================================
# VIZ 3: Top 10 Bargains
# ========================================
print("\n3. Generating top_bargains.png...")
rb_player_agg = rb_df[rb_df['draft_number'].notna()].groupby(['player_name', 'draft_round', 'draft_number']).agg(
    avg_value=('value_score', 'mean'),
    total_seasons=('season', 'size'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    best_season=('season', 'max')
).reset_index()
rb_player_agg = rb_player_agg[rb_player_agg['total_seasons'] >= 2].copy()

top_bargains = rb_player_agg.nlargest(10, 'avg_value')

fig = px.bar(
    top_bargains,
    x='avg_value',
    y='player_name',
    color='draft_round',
    orientation='h',
    title='<b>Top 10 RB Bargains</b><br><sub>Highest Career Average Value Score (Min 2 Seasons)</sub>',
    labels={'avg_value': 'Avg Value Score', 'player_name': '', 'draft_round': 'Draft Round'},
    hover_data=['draft_number', 'total_seasons'],
    color_continuous_scale='Greens'
)
fig.update_layout(
    width=900,
    height=600,
    yaxis={'categoryorder': 'total ascending'}
)
fig.write_image(OUTPUT_DIR / 'top_bargains.png')
print("   [OK] Saved top_bargains.png")

# ========================================
# VIZ 4: Top 10 Busts
# ========================================
print("\n4. Generating top_busts.png...")
first_round_rbs = rb_player_agg[rb_player_agg['draft_round'] == 1].copy()
top_busts = first_round_rbs.nsmallest(10, 'avg_value')

fig = px.bar(
    top_busts,
    x='avg_value',
    y='player_name',
    color='draft_number',
    orientation='h',
    title='<b>Top 10 First-Round RB Busts</b><br><sub>Lowest Career Average Value Score</sub>',
    labels={'avg_value': 'Avg Value Score', 'player_name': '', 'draft_number': 'Draft Pick #'},
    hover_data=['total_seasons'],
    color_continuous_scale='Reds'
)
fig.update_layout(
    width=900,
    height=600,
    yaxis={'categoryorder': 'total descending'}
)
fig.write_image(OUTPUT_DIR / 'top_busts.png')
print("   [OK] Saved top_busts.png")

# ========================================
# VIZ 5: Performance vs. Salary
# ========================================
print("\n5. Generating performance_vs_salary.png...")
fig = px.scatter(
    rb_player_agg,
    x='avg_salary_pct',
    y='avg_performance',
    color='draft_round',
    size='total_seasons',
    hover_name='player_name',
    title='<b>RB Performance vs. Salary</b><br><sub>Career Averages | Size = Total Seasons</sub>',
    labels={
        'avg_salary_pct': 'Avg Salary (% of Cap)',
        'avg_performance': 'Avg Performance Z-Score',
        'draft_round': 'Draft Round',
        'total_seasons': 'Seasons'
    },
    color_continuous_scale='Viridis'
)
fig.update_layout(width=1000, height=600)
fig.add_shape(
    type="line",
    x0=0, y0=-2, x1=0.1, y1=3,
    line=dict(dash="dash", color="gray", width=2)
)
fig.write_image(OUTPUT_DIR / 'performance_vs_salary.png')
print("   [OK] Saved performance_vs_salary.png")

# ========================================
# VIZ 6: Replaceability
# ========================================
print("\n6. Generating replaceability.png...")
rb_df['is_drafted'] = rb_df['draft_number'].notna()

replaceability = rb_df.groupby('is_drafted').agg(
    avg_value=('value_score', 'mean'),
    median_value=('value_score', 'median'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    count=('value_score', 'size')
).reset_index()
replaceability['status'] = replaceability['is_drafted'].map({True: 'Drafted', False: 'UDFA'})

fig = go.Figure()
fig.add_trace(go.Bar(
    x=replaceability['status'],
    y=replaceability['avg_value'],
    text=replaceability['avg_value'].round(2),
    textposition='outside',
    marker_color=['blue', 'orange'],
    hovertemplate='<b>%{x}</b><br>Avg Value: %{y:.2f}<br>N=%{customdata:,}<extra></extra>',
    customdata=replaceability['count']
))
fig.update_layout(
    title='<b>RB Positional Replaceability</b><br><sub>Drafted vs. Undrafted Free Agent Performance</sub>',
    xaxis_title='',
    yaxis_title='Average Value Score',
    width=600,
    height=500,
    showlegend=False
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.write_image(OUTPUT_DIR / 'replaceability.png')
print("   [OK] Saved replaceability.png")

print("\n" + "="*60)
print("All 6 visualizations exported successfully!")
print(f"Output directory: {OUTPUT_DIR.absolute()}")
print("="*60)
