# Template for New NFL Research Project Repos

This document provides a step-by-step guide for creating new NFL analysis project repositories that use the shared `nfl-data-core` library.

## Quick Start Checklist

- [ ] Choose research question from list
- [ ] Create new repo on GitHub
- [ ] Set up local structure
- [ ] Add nfl-data-core to requirements
- [ ] Create first notebook
- [ ] Document findings in README

## Research Ideas Available

See the full plan document for detailed descriptions of each research direction:

1. **Draft Class ROI Analysis** - Which draft positions produce best value?
2. **Contract Year Performance Boost** - Do players perform better in contract years?
3. **Injury Impact on Salary Efficiency** - How do snap count drops affect value?
4. **Team Salary Cap Strategy** - Which teams consistently find bargains?
5. **Position Market Inflation** - How has salary by position changed over time?
6. **Pressure Rate Analysis** - QB/OL/DL pressure metrics vs. salary efficiency
7. **Contract Performance Decay** - When do veteran contracts start underperforming?

## Step-by-Step Setup

### 1. Create Repository

```bash
cd G:/ai
gh repo create nfl-<project-name> --private --description "<brief description>"
git clone https://github.com/ghighcove/nfl-<project-name>.git
cd nfl-<project-name>
```

**Example:**
```bash
gh repo create nfl-draft-roi --private --description "NFL Draft Class ROI Analysis - which positions/rounds produce best value?"
```

### 2. Create Directory Structure

```bash
mkdir notebooks
mkdir data
mkdir outputs
touch README.md
touch CLAUDE.md
touch requirements.txt
```

### 3. Create requirements.txt

```
git+https://github.com/ghighcove/nfl-data-core.git
jupyter
jupyterlab
```

### 4. Create .gitignore

```
# Data cache
data/
*.parquet

# Outputs
outputs/
*.png
*.jpg
*.html

# Python
__pycache__/
*.py[cod]
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
```

### 5. Create README.md Template

```markdown
# NFL [Project Name]

## Research Question
[Clear, specific question this analysis answers]

## Key Findings

### Finding 1: [Descriptive title]
[2-3 sentences summarizing the finding]

### Finding 2: [Descriptive title]
[2-3 sentences summarizing the finding]

### Finding 3: [Descriptive title]
[2-3 sentences summarizing the finding]

## Methodology

**Data Coverage:** 2015-2024 NFL seasons

**Data Sources:**
- Player statistics (via `nfl_data_py`)
- Contract data (Over The Cap)
- Snap counts
- [Any additional datasets specific to this project]

**Analysis Approach:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

## How to Run

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run notebooks in order:
   - `01_[descriptive_name].ipynb` - Data acquisition
   - `02_[descriptive_name].ipynb` - Analysis
   - `03_[descriptive_name].ipynb` - Visualizations
4. Outputs saved to `outputs/` directory

## Repository Structure

```
nfl-[project-name]/
├── notebooks/           # Jupyter notebooks (run in order)
├── data/                # Cached data (gitignored)
├── outputs/             # Generated charts and exports
├── requirements.txt     # Python dependencies
├── CLAUDE.md            # Project-specific instructions
└── README.md            # This file
```

## Shared Library

This project uses the [nfl-data-core](https://github.com/ghighcove/nfl-data-core) library for common data loading, cleaning, and analysis functions.

**Standard imports:**
```python
from nfl_analysis import data_loader, cleaning, value_score, viz
import pandas as pd
import plotly.express as px
```

## Author

Glenn Highcove
- LinkedIn: [linkedin.com/in/glennhighcove](https://www.linkedin.com/in/glennhighcove/)

## Related Projects

- [NFL Player Value Score Analysis](https://github.com/ghighcove/nfl-salary-analysis) - Original analysis
- [NFL Data Core Library](https://github.com/ghighcove/nfl-data-core) - Shared modules
```

### 6. Create CLAUDE.md Template

```markdown
# NFL [Project Name]

## Project Overview
[2-3 sentence description of what this project analyzes]

## Research Question
[Specific question this project answers]

## Architecture
- `notebooks/` — Jupyter notebooks for analysis pipeline
- `data/` — Cached parquet files (gitignored)
- `outputs/` — Generated visualizations and exports
- **Shared Library**: Uses [nfl-data-core](https://github.com/ghighcove/nfl-data-core) for reusable modules

## Data Conventions
- **Time range**: 2015-2024 (10 seasons)
- **Primary join key**: `gsis_id` (called `player_id` in weekly stats)
- **Salary normalization**: `apy_cap_pct` (APY as % of salary cap)
- **Minimum threshold**: 100 snaps/season for inclusion
- **Position groups**: QB, RB, WR, TE, OL, DL, LB, DB, K, P

## Running
1. `pip install -r requirements.txt` (installs nfl-data-core from GitHub)
2. Run notebooks in sequence
3. Outputs saved to `outputs/`

**Import Pattern:**
```python
from nfl_analysis import data_loader, cleaning, value_score, viz
```

## Project-Specific Notes
[Add any unique conventions or notes specific to this analysis]

## Key Variables
[Document important calculated fields unique to this project]
```

### 7. Create First Notebook

Create `notebooks/01_data_acquisition.ipynb` with this structure:

```python
# Cell 1: Imports
import sys
sys.path.insert(0, '..')

from nfl_analysis import data_loader
import pandas as pd

print(f"Data directory: {data_loader.DATA_DIR}")

# Cell 2: Load data
FORCE = False  # Set True to re-download

# Load standard datasets
contracts, weekly_stats, snaps, rosters = data_loader.load_all(
    start_year=2015,
    end_year=2024,
    force_refresh=FORCE
)

print("\n=== Dataset Summary ===")
print(f"Contracts: {len(contracts):,} rows")
print(f"Weekly Stats: {len(weekly_stats):,} rows")
print(f"Snaps: {len(snaps):,} rows")
print(f"Rosters: {len(rosters):,} rows")

# Cell 3: [Project-specific data loading or preparation]
```

### 8. Initial Commit

```bash
git add .
git commit -m "Initial commit: Project setup for [project name]

- Add project structure (notebooks/, data/, outputs/)
- Configure requirements.txt with nfl-data-core
- Document research question and methodology in README
- Create first notebook for data acquisition

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
git push -u origin master
```

### 9. Enable GitHub Actions (Optional)

If you want to run notebooks automatically on push, create `.github/workflows/run-notebooks.yml`.

## Standard Notebook Sequence

Most projects follow this pattern:

1. **01_data_acquisition.ipynb** - Load and cache data
2. **02_analysis.ipynb** - Core analysis and calculations
3. **03_visualizations.ipynb** - Create charts and interactive plots
4. **04_export.ipynb** (optional) - Export for publishing

## Tips for New Projects

### Data Loading
- Use `data_loader.load_all()` for standard datasets
- Add project-specific loaders if needed (e.g., `load_draft_info()`)
- Always cache to parquet for faster reruns

### Analysis Modules
- Import `cleaning.py` functions for data prep
- Use `value_score.py` if calculating player value metrics
- Extend with project-specific functions in notebooks

### Visualization
- Import from `viz.py` for standard chart types
- Plotly preferred for interactive exploration
- Matplotlib for static exports

### Performance
- Filter early (by position, year range, snap thresholds)
- Use parquet caching aggressively
- Aggregate before visualizing large datasets

## Example: Draft Class ROI Project

```bash
# 1. Create repo
gh repo create nfl-draft-roi --private
git clone https://github.com/ghighcove/nfl-draft-roi.git
cd nfl-draft-roi

# 2. Set up structure
mkdir notebooks data outputs
echo "git+https://github.com/ghighcove/nfl-data-core.git\njupyter\njupyterlab" > requirements.txt

# 3. Create README and CLAUDE.md (using templates above)

# 4. Create first notebook
# (Jupyter Lab: File -> New -> Notebook)

# 5. Commit and push
git add .
git commit -m "Initial commit: Draft Class ROI analysis setup"
git push -u origin master
```

## Updating the Shared Library

If you need to modify the shared library (`nfl-data-core`):

```bash
cd G:/ai/nfl-data-core
# Make your changes
git add .
git commit -m "Add new function: [description]"
git push

# Then update in your project
cd G:/ai/nfl-[your-project]
pip install --upgrade git+https://github.com/ghighcove/nfl-data-core.git
```

## Questions?

Refer to:
- [nfl-data-core README](https://github.com/ghighcove/nfl-data-core)
- [Original nfl project](https://github.com/ghighcove/nfl-salary-analysis) for examples
- Research plan document for detailed project ideas
