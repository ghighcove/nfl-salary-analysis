# Draft Class ROI Analysis - Key Findings

## Overview
Analysis of **3,657 player-seasons** from **1,644 drafted players** during their **first 4 years** (rookie contract).
**Seasons:** 2015-2024

---

## 🏆 Top Insights

### 1. Best Value by Draft Round
**Round 2 provides the best overall ROI** during rookie contracts:

| Draft Round | Avg Value Score | Sample Size | % Bargains |
|-------------|-----------------|-------------|------------|
| **Round 2** | **+0.51** | 610 | 4.9% |
| Round 3 | +0.47 | 556 | 4.1% |
| Round 1 | +0.36 | 568 | 3.3% |
| Round 4 | +0.34 | 508 | 2.4% |
| Round 5 | +0.32 | 445 | 2.0% |
| Round 6 | +0.26 | 403 | 1.7% |
| Round 7 | +0.15 | 567 | 0.9% |

✅ **All rounds produce positive value on average** — rookie contracts are team-friendly across the board.

---

### 2. Sweet Spots: Best Round × Position Combos

| Rank | Position | Round | Avg Value | Sample Size |
|------|----------|-------|-----------|-------------|
| 🥇 1 | **QB** | **5** | **+0.62** | 16 |
| 🥈 2 | **DB** | **3** | **+0.60** | 92 |
| 🥉 3 | **DB** | **2** | **+0.60** | 146 |
| 4 | **TE** | **2** | **+0.58** | 73 |
| 5 | **QB** | **2** | **+0.56** | 16 |
| 6 | **RB** | **3** | **+0.55** | 87 |
| 7 | **WR** | **2** | **+0.55** | 159 |
| 8 | **TE** | **5** | **+0.53** | 70 |
| 9 | **RB** | **2** | **+0.53** | 76 |
| 10 | **QB** | **1** | **+0.52** | 105 |

**Key Takeaways:**
- **Round 5 QBs** are the #1 value play (e.g., Brock Purdy, Russell Wilson)
- **Rounds 2-3 DBs** consistently outperform expectations
- **Round 2 WRs/TEs** are excellent value (large sample sizes)
- **Round 1 QBs** still provide good value despite high salaries

---

### 3. Avoid These Draft Traps

| Rank | Position | Round | Avg Value | Sample Size |
|------|----------|-------|-----------|-------------|
| ❌ 1 | **QB** | **6** | **-0.09** | 10 |
| ❌ 2 | **RB** | **1** | **+0.02** | 52 |
| ❌ 3 | **DB** | **1** | **+0.04** | 78 |
| ❌ 4 | **LB** | **7** | **+0.04** | 88 |
| ❌ 5 | **OL** | **1** | **+0.06** | 13 |

**Key Takeaways:**
- **First-round RBs** barely break even (0.02 value) — the data confirms conventional wisdom
- **Round 6 QBs** are negative value (too late for franchise QBs, too expensive for backups)
- **Round 7 picks** struggle across most positions (low hit rate)

---

### 4. Top 10 Late-Round Steals (Rounds 3+)

| Player | Position | Season | Round | Pick # | Value Score |
|--------|----------|--------|-------|--------|-------------|
| **Justin Madubuike** | DL | 2023 | 3 | 71 | **+3.95** |
| **Kerby Joseph** | DB | 2024 | 4 | 97 | **+3.40** |
| **Jordan Reed** | TE | 2015 | 3 | 85 | **+3.29** |
| **Amon-Ra St. Brown** | WR | 2023 | 4 | 112 | **+3.12** |
| **Terrel Bernard** | LB | 2023 | 3 | 89 | **+2.90** |
| **Tyreek Hill** | WR | 2018 | 5 | 165 | **+2.73** |
| **Damontae Kazee** | DB | 2018 | 5 | 149 | **+2.70** |
| **George Kittle** | TE | 2018 | 5 | 146 | **+2.68** |
| **Dalton Schultz** | TE | 2021 | 5 | 137 | **+2.66** |
| **Joe Schobert** | LB | 2019 | 4 | 99 | **+2.63** |

---

### 5. First-Round "Busts" (Relative to Salary)

| Player | Position | Season | Pick # | Value Score |
|--------|----------|--------|--------|-------------|
| **Christian McCaffrey** | RB | 2020 | 8 | **-4.64** |
| **Ezekiel Elliott** | RB | 2019 | 4 | **-3.07** |
| **Jaylen Waddle** | WR | 2024 | 6 | **-2.74** |
| **Vita Vea** | DL | 2021 | 12 | **-2.52** |
| **Penei Sewell** | OL | 2024 | 7 | **-2.25** |
| **Joe Burrow** | QB | 2023 | 1 | **-2.25** |
| **Todd Gurley** | RB | 2018 | 10 | **-2.22** |
| **Trevor Lawrence** | QB | 2024 | 1 | **-2.20** |
| **Saquon Barkley** | RB | 2021 | 2 | **-2.09** |
| **Chase Young** | DL | 2022 | 2 | **-1.98** |

⚠️ **Important Context:**
These are "busts" **relative to their salary**, not overall performance. CMC, Zeke, and Barkley were elite players — but their rookie contract salary (as top-10 picks) was so high that their value score suffered. This reinforces: **don't draft RBs in Round 1**.

---

## 📊 Visualizations Available

The notebook (`05_draft_roi_analysis.ipynb`) includes:
1. **Heatmap:** Draft round × position → avg value score
2. **Bar Charts:** Value by round, top steals, worst busts
3. **Line Chart:** Performance trajectory over 4-year rookie contracts
4. **Scatter Plots:** QB-specific draft pick analysis
5. **Position Sweet Spot Analysis**

---

## 💡 Practical Applications

**For NFL Teams:**
- Prioritize **Round 2-3 DBs** and **Round 5 QBs** for value
- Avoid **Round 1 RBs** unless generational talent
- **Round 2 WRs/TEs** are consistent value plays
- **Late-round TEs** (Round 5) outperform expectations

**For Fantasy Players:**
- Target **Round 3-5 rookie TEs/WRs** — high upside, low draft capital
- Be cautious with **1st-round RBs** — often overhyped
- **Round 2-3 RBs** provide better fantasy ROI

---

## 🔗 Data Sources
- **nfl_data_py** library (2015-2024)
- **nfl-data-core** shared analysis library
- Minimum 100 snaps/season threshold

---

## 📁 File Location
- **Notebook:** `notebooks/05_draft_roi_analysis.ipynb`
- **Summary:** `notebooks/05_DRAFT_ROI_SUMMARY.md`

---

**Generated:** 2026-02-10
**Analysis:** Draft Class ROI (Rookie Contract Years 1-4)
