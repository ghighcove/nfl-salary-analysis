# NFL Player Stats vs. Salary Analysis

**Version 1.0.0**

**Research Project:** Analyzing NFL player performance statistics against salary data (2015-2024)

## Overview

This project analyzes 10 years of NFL player data to identify:
- **Bargain players** who dramatically outperform their salary
- **Overpaid players** who underperform relative to compensation
- **Draft value trends** by round and position
- **Position market inefficiencies**

All analysis uses the [nfl-data-core](https://github.com/ghighcove/nfl-data-core) shared library for data loading, cleaning, scoring, and visualization.

---

## Available Analyses

### 1. Player Value Analysis (Notebooks 01-04)
**Original analysis** comparing player performance to salary across all positions.

**Notebooks:**
- `01_data_acquisition.ipynb` — Load data from nfl_data_py
- `02_data_cleaning.ipynb` — Clean, merge, and prepare datasets
- `03_value_scoring.ipynb` — Calculate composite performance and value scores
- `04_visualizations.ipynb` — Interactive charts and player deep dives

**Key Outputs:**
- Scatter plots: Performance vs. Salary by position
- Top bargains and overpaid players by position
- Team salary cap efficiency heatmaps
- Player trajectory visualizations

**Published Article:**
- Medium draft: `article/medium_draft.md`
- GitHub Pages: `article/medium_ready.html`

---

### 2. Draft Class ROI Analysis (Notebook 05) 🆕
**Research Question:** Which draft positions/rounds produce the best value over their first rookie contracts?

**Notebook:**
- `05_draft_roi_analysis.ipynb` — Draft value analysis (rookie contracts years 1-4)

**Key Findings:**
- **Round 2 provides best overall ROI** (avg value: +0.51)
- **Round 5 QBs** are the #1 value combo (+0.62 avg)
- **First-round RBs** barely break even (+0.02) — data confirms conventional wisdom
- **Late-round steals:** Tyreek Hill (Rd 6), George Kittle (Rd 5), Amon-Ra St. Brown (Rd 4)
- **Round 2-3 DBs** consistently outperform expectations

**Summary:** See `notebooks/05_DRAFT_ROI_SUMMARY.md` for full findings

---

## Quick Start

### Installation
```bash
# Install dependencies (includes nfl-data-core from GitHub)
pip install -r requirements.txt
```

### Running Notebooks
```bash
# Run notebooks in order
jupyter notebook notebooks/01_data_acquisition.ipynb
# ... continue through 02, 03, 04, 05
```

Each notebook saves outputs that subsequent notebooks read. Run in sequence on first use.

---

## Data Sources

All data from **nfl_data_py** library:
- Weekly player stats (2015-2024)
- Snap counts (offense, defense, special teams)
- Salary/contract data (OverTheCap)
- Pro Football Reference advanced stats (2018+)
- Rosters and draft information

Cached locally in `data/` as parquet files (gitignored).

---

## Key Metrics

### Value Score
```
Value Score = Performance Z-Score - Salary Cap % Z-Score
```

**Interpretation:**
- **Positive score** = Bargain (outperforming salary)
- **Negative score** = Overpaid (underperforming salary)
- **Z-score normalization** allows cross-position comparisons

### Performance Scoring
Position-specific composite metrics:
- **QB:** Passing EPA, completion %, TD rate, INT rate
- **RB:** Rushing EPA, yards per carry, receiving production
- **WR/TE:** Receiving EPA, yards per reception, catch rate, TDs
- **Defense:** Tackles, sacks, pressures, turnovers
- **Minimum threshold:** 100 snaps/season

### Salary Normalization
- **APY Cap %** = Average salary / Salary cap for that season
- Enables fair comparison across years (accounts for cap inflation)

---

## Project Structure

```
nfl/
├── notebooks/              # Jupyter notebooks (01-05)
├── data/                   # Cached parquet files (gitignored)
├── article/                # Medium article draft + HTML
├── requirements.txt        # Python dependencies
└── CLAUDE.md              # Project conventions and guidelines
```

**Import pattern in notebooks:**
```python
from nfl_analysis import data_loader, cleaning, value_score, viz
```

---

## Article Production Pipeline

See **`PROJECT_PIPELINE.md`** for the complete article production roadmap:

**20 articles planned across 3 series:**
- **Position Deep Dives** (10 articles) — RB, QB, WR, TE, DB, LB, DL, OL, K/P, Special Teams
- **Team Strategy** (8 articles) — Best drafting teams, cap management, draft vs. FA ROI, front office patterns
- **Contract Market Trends** (2 articles) — Salary inflation, contract year performance

**Next article:** Running Back Economics (extends draft ROI findings)
**Production target:** 5-10 articles published in 2-3 months
**Quality standard:** 95+ GEO score for LLM discoverability

---

## Article Publishing

The original player value analysis is published as a Medium article. See:
- `article/medium_draft.md` — Markdown source
- `article/medium_ready.html` — HTML formatted for Medium import
- Images hosted via GitHub Pages: `https://ghighcove.github.io/nfl/...`

**SEO/GEO optimized** for LLM discoverability (scored ~79/100).

---

## Attribution

*Project genesis and direction: Glenn Highcove*
*Analysis framework: Claude Sonnet 4.5*

For questions or feedback, connect on [LinkedIn](https://www.linkedin.com/in/glennhighcove/).

---

## License

Data sourced from publicly available NFL statistics via **nfl_data_py**. Analysis code and visualizations are original work.
