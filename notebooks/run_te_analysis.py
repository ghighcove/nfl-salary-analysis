"""
Execute TE Market Inefficiency Analysis
Generates all 6 visualizations for the article
"""

import sys
sys.path.insert(0, '..')

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set data directory
DATA_DIR = Path('../data')
OUTPUT_DIR = Path('../article/images/te_market_inefficiency')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("="*80)
print("TIGHT END MARKET INEFFICIENCY ANALYSIS")
print("="*80)

# 1. Load Data
print("\n1. Loading data...")
scored = pd.read_parquet(DATA_DIR / 'scored.parquet', engine='fastparquet')
rosters = pd.read_parquet(DATA_DIR / 'rosters.parquet', engine='fastparquet')
weekly = pd.read_parquet(DATA_DIR / 'weekly_stats.parquet', engine='fastparquet')

# Get draft info
draft_info = rosters[rosters['draft_number'].notna()][['player_id', 'player_name', 'draft_number', 'draft_club', 'rookie_year']].drop_duplicates('player_id').copy()
draft_info['draft_number'] = pd.to_numeric(draft_info['draft_number'], errors='coerce')
draft_info['draft_round'] = ((draft_info['draft_number'] - 1) // 32 + 1).astype('Int64')
draft_info['draft_round'] = draft_info['draft_round'].clip(upper=7)

print(f"   Scored data: {scored.shape[0]:,} player-seasons")
print(f"   Rosters data: {rosters.shape[0]:,} player-week records")
print(f"   Drafted players: {len(draft_info):,}")

# 2. Filter to Tight Ends
print("\n2. Filtering to tight ends...")
te_scored = scored[scored['pos_group'] == 'TE'].copy()
te_df = te_scored.merge(draft_info, on=['player_id', 'player_name'], how='left')
te_df['years_since_draft'] = te_df['season'] - te_df['rookie_year']

print(f"   TE player-seasons: {te_scored.shape[0]:,}")
print(f"   Unique TE players: {te_scored['player_id'].nunique():,}")
print(f"   TEs with draft info: {te_df['draft_number'].notna().sum():,}")

# 3. Career Arc Analysis
print("\n3. Generating career arc visualization...")
te_career = te_df[te_df['years_since_draft'].notna() & (te_df['years_since_draft'] >= 0)].copy()
te_career['years_since_draft'] = te_career['years_since_draft'].astype(int)
te_career = te_career[te_career['years_since_draft'] <= 10].copy()

career_arc = te_career.groupby('years_since_draft').agg(
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
    title='<b>TE Career Arc: Value Score by Years of Experience</b><br><sub>When Do Tight Ends Peak?</sub>',
    xaxis_title='Years Since Draft',
    yaxis_title='Average Value Score',
    width=900,
    height=500,
    hovermode='x'
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.write_image(OUTPUT_DIR / 'career_arc.png', width=900, height=500)
print(f"   [OK] Saved career_arc.png")

# 4. Draft ROI by Round
print("\n4. Generating draft ROI visualization...")
te_rookie = te_career[(te_career['years_since_draft'] >= 0) & (te_career['years_since_draft'] <= 3)].copy()

te_draft_roi = te_rookie.groupby('draft_round').agg(
    avg_value=('value_score', 'mean'),
    median_value=('value_score', 'median'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    count=('value_score', 'size'),
    pct_bargains=('is_bargain', lambda x: x.sum() / len(x) * 100 if len(x) > 0 else 0)
).reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=te_draft_roi['draft_round'],
    y=te_draft_roi['avg_value'],
    text=te_draft_roi['avg_value'].round(2),
    textposition='outside',
    marker_color=['green' if v > 0.3 else 'orange' if v > 0 else 'red' for v in te_draft_roi['avg_value']],
    hovertemplate='<b>Round %{x}</b><br>Avg Value: %{y:.2f}<br>N=%{customdata[0]:,}<br>% Bargains: %{customdata[1]:.1f}%<extra></extra>',
    customdata=te_draft_roi[['count', 'pct_bargains']]
))
fig.update_layout(
    title='<b>TE Draft ROI: Average Value by Round</b><br><sub>Rookie Contract Years Only | Why Round 5 Is the Best-Kept Secret</sub>',
    xaxis_title='Draft Round',
    yaxis_title='Average Value Score',
    width=800,
    height=500,
    showlegend=False
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.write_image(OUTPUT_DIR / 'draft_roi_by_round.png', width=800, height=500)
print(f"   [OK] Saved draft_roi_by_round.png")

# 5. Top Bargains
print("\n5. Generating top bargains visualization...")
te_player_agg = te_df[te_df['draft_number'].notna()].groupby(['player_name', 'draft_round', 'draft_number']).agg(
    avg_value=('value_score', 'mean'),
    total_seasons=('season', 'size'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    best_season=('season', 'max')
).reset_index()

te_player_agg = te_player_agg[te_player_agg['total_seasons'] >= 2].copy()
top_bargains = te_player_agg.nlargest(10, 'avg_value')

fig = px.bar(
    top_bargains,
    x='avg_value',
    y='player_name',
    color='draft_round',
    orientation='h',
    title='<b>Top 10 TE Bargains</b><br><sub>Highest Career Average Value Score (Min 2 Seasons)</sub>',
    labels={'avg_value': 'Avg Value Score', 'player_name': '', 'draft_round': 'Draft Round'},
    hover_data=['draft_number', 'total_seasons'],
    color_continuous_scale='Greens'
)
fig.update_layout(
    width=900,
    height=600,
    yaxis={'categoryorder': 'total ascending'}
)
fig.write_image(OUTPUT_DIR / 'top_bargains.png', width=900, height=600)
print(f"   [OK] Saved top_bargains.png")
print(f"   Top 5 bargains:")
for idx, row in top_bargains.head(5).iterrows():
    print(f"      {row['player_name']:20s} Round {row['draft_round']} Pick #{row['draft_number']:3.0f} Value: {row['avg_value']:+.2f}")

# 6. Top Busts
print("\n6. Generating top busts visualization...")
first_round_tes = te_player_agg[te_player_agg['draft_round'] == 1].copy()
top_busts = first_round_tes.nsmallest(min(10, len(first_round_tes)), 'avg_value')

if len(top_busts) > 0:
    fig = px.bar(
        top_busts,
        x='avg_value',
        y='player_name',
        color='draft_number',
        orientation='h',
        title='<b>First-Round TE Busts</b><br><sub>Lowest Career Average Value Score</sub>',
        labels={'avg_value': 'Avg Value Score', 'player_name': '', 'draft_number': 'Draft Pick #'},
        hover_data=['total_seasons'],
        color_continuous_scale='Reds'
    )
    fig.update_layout(
        width=900,
        height=600,
        yaxis={'categoryorder': 'total descending'}
    )
    fig.write_image(OUTPUT_DIR / 'top_busts.png', width=900, height=600)
    print(f"   [OK] Saved top_busts.png")
    print(f"   Top busts: {len(top_busts)}")
else:
    print(f"   [WARN] No first-round TEs found for bust analysis")

# 7. Red Zone Efficiency vs. Salary
print("\n7. Generating red zone efficiency visualization...")
te_weekly = weekly[weekly['position'] == 'TE'].copy()
te_td_stats = te_weekly.groupby(['player_id', 'season']).agg(
    total_tds=('receiving_tds', 'sum'),
    total_targets=('targets', 'sum')
).reset_index()
te_td_stats['td_per_target'] = te_td_stats['total_tds'] / te_td_stats['total_targets'].replace(0, np.nan)

te_redzone = te_scored.merge(te_td_stats, on=['player_id', 'season'], how='left')
te_redzone = te_redzone[(te_redzone['td_per_target'].notna()) & (te_redzone['total_targets'] >= 20)].copy()

fig = px.scatter(
    te_redzone,
    x='td_per_target',
    y='apy_cap_pct',
    color='value_score',
    hover_name='player_name',
    hover_data=['season', 'total_tds', 'total_targets'],
    title='<b>TE Red Zone Efficiency vs. Salary</b><br><sub>Touchdowns Per Target vs. Cap Hit (Min 20 Targets)</sub>',
    labels={
        'td_per_target': 'Touchdowns Per Target',
        'apy_cap_pct': 'Salary (% of Cap)',
        'value_score': 'Value Score'
    },
    color_continuous_scale='RdYlGn',
    color_continuous_midpoint=0
)
fig.update_layout(width=1000, height=600)
fig.write_image(OUTPUT_DIR / 'redzone_vs_salary.png', width=1000, height=600)
print(f"   [OK] Saved redzone_vs_salary.png")

# 8. Blocking vs. Receiving TEs
print("\n8. Generating blocking vs receiving TE visualization...")
te_targets = te_weekly.groupby(['player_id', 'season']).agg(
    total_targets=('targets', 'sum'),
    games=('week', 'nunique')
).reset_index()
te_targets['targets_per_game'] = te_targets['total_targets'] / te_targets['games']

te_role = te_scored.merge(te_targets, on=['player_id', 'season'], how='left')
te_role['role'] = te_role['targets_per_game'].apply(
    lambda x: 'Receiving TE' if x >= 4 else 'Blocking TE' if pd.notna(x) else 'Unknown'
)
te_role = te_role[te_role['role'] != 'Unknown'].copy()

role_comparison = te_role.groupby('role').agg(
    avg_value=('value_score', 'mean'),
    median_value=('value_score', 'median'),
    avg_performance=('performance_zscore', 'mean'),
    avg_salary_pct=('apy_cap_pct', 'mean'),
    count=('value_score', 'size')
).reset_index()

fig = go.Figure()
fig.add_trace(go.Bar(
    x=role_comparison['role'],
    y=role_comparison['avg_value'],
    text=role_comparison['avg_value'].round(2),
    textposition='outside',
    marker_color=['#2ca02c' if v > 0 else '#d62728' for v in role_comparison['avg_value']],
    hovertemplate='<b>%{x}</b><br>Avg Value: %{y:.2f}<br>N=%{customdata:,}<extra></extra>',
    customdata=role_comparison['count']
))
fig.update_layout(
    title='<b>Blocking vs. Receiving TE Value Comparison</b><br><sub>Average Value Score by TE Role</sub>',
    xaxis_title='',
    yaxis_title='Average Value Score',
    width=700,
    height=500,
    showlegend=False
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.write_image(OUTPUT_DIR / 'blocking_vs_receiving.png', width=700, height=500)
print(f"   [OK] Saved blocking_vs_receiving.png")

# Print summary
print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

print("\n1. CAREER ARC:")
print(f"   Peak Years: Years {career_arc.nlargest(3, 'avg_value')['years_since_draft'].tolist()}")

print("\n2. DRAFT ROI BY ROUND:")
print(te_draft_roi[['draft_round', 'avg_value', 'count']].to_string(index=False))

print("\n3. ROLE COMPARISON:")
print(role_comparison[['role', 'avg_value', 'count']].to_string(index=False))

print("\n" + "="*80)
print("[OK] All 6 visualizations generated successfully!")
print(f"[OK] Output directory: {OUTPUT_DIR.resolve()}")
print("="*80)
