# Two-Project Development Sprint - Testing Checklist

## Project 1: Medium Scheduling Automator + Article Tracker

### Medium Tracker CLI
- [ ] Run `python G:/ai/medium-publishing-standards/tools/medium_tracker.py --list`
  - Verify shows pending articles from NFL project
  - Check counts match reality (4 pending articles expected)
- [ ] Test filtering: `python medium_tracker.py --list --status pending`
- [ ] Test project filter: `python medium_tracker.py --list --project nfl`
- [ ] Generate HTML: `python medium_tracker.py --html`
  - Open `G:/ai/medium-publishing-standards/published/index.html`
  - Test sorting (click column headers)
  - Test filtering (All/Published/Pending buttons)
  - Test search (type "rb" or "nfl")

### Medium Date Picker Automation
- [ ] Run `/publish draft_roi` (or any article name)
- [ ] If prompted for scheduling, test date picker automation
  - Expected: Fills date/time fields and clicks Schedule
  - Fallback: Provides clear manual instructions if automation fails

### Archival Workflow
- [ ] After publishing an article to Medium, run archive command
- [ ] Verify INDEX.md updated
- [ ] Verify index.html regenerated
- [ ] Check dashboard shows new published article

---

## Project 2: Multi-Strategy Backtesting System

### Prerequisites
- [ ] Verify market data exists: `G:/ai/trading_bot/data/SPY_historical.csv`
  - If missing, download SPY historical data (CSV format with columns: timestamp, open, high, low, close, volume)

### Batch Backtest
- [ ] Run: `cd G:/ai/trading_bot && python scripts/run_batch_backtest.py --config config/batch_backtest.yaml`
- [ ] Verify:
  - All 5 strategies execute successfully
  - Parallel execution completes (check duration vs sequential)
  - CSV exported to `outputs/batch_results.csv`
  - JSON exported to `outputs/batch_results.json`
  - HTML report generated at `outputs/batch_report.html`
- [ ] Open HTML report:
  - Verify equity curves chart displays
  - Verify metrics bar chart displays
  - Verify comparison table is sortable
- [ ] Open CSV in Excel:
  - Verify all columns present
  - Verify metrics match HTML report

### Parameter Optimization
- [ ] Run: `python scripts/run_optimization.py --config config/optimize_ma.yaml`
- [ ] Verify:
  - Shows total combinations count (30 with constraints)
  - Completes all backtests
  - Displays top 10 parameter sets
  - Shows best parameters clearly
- [ ] Generate heatmap:
  ```bash
  python scripts/run_optimization.py --config config/optimize_ma.yaml \
    --heatmap-output outputs/ma_heatmap.png \
    --heatmap-x fast_period --heatmap-y slow_period
  ```
  - Requires: `pip install matplotlib seaborn`
  - Verify PNG generated and displays metric values

### Error Handling
- [ ] Test batch with invalid strategy class (should isolate failure)
- [ ] Test optimization with conflicting constraints (should skip invalid combos)
- [ ] Test without market data file (should show clear error)

### Performance
- [ ] Measure batch backtest duration (5 strategies):
  - Parallel (4 workers): Expected ~10-20 seconds
  - Sequential: Expected ~40-80 seconds
  - Speedup ratio: Should be 2.5x+ on 4-core machine

---

## Integration Tests

### Cross-Project Dashboard
- [ ] Publish article from NFL project
- [ ] Archive it
- [ ] Verify medium_tracker finds it across projects
- [ ] Check dashboard aggregates correctly

### Backward Compatibility
- [ ] Run existing single backtest: `python scripts/run_backtest.py`
  - Verify still works (not broken by new batch code)

---

## Known Limitations

### Medium Automation
- Date picker UI may change (Medium updates frequently)
- Screenshot debugging helps identify issues
- Graceful fallback to manual instructions

### Backtesting
- Requires historical data CSV files
- Large parameter grids (100+ combos) can be slow
- Heatmaps require matplotlib/seaborn (optional)

---

## Quick Verification Commands

```bash
# Test Medium tracker
python G:/ai/medium-publishing-standards/tools/medium_tracker.py --list

# Test batch backtest (if data available)
cd G:/ai/trading_bot
python scripts/run_batch_backtest.py --config config/batch_backtest.yaml --no-parallel

# Test optimization (if data available)
python scripts/run_optimization.py --config config/optimize_ma.yaml
```

---

## Success Criteria

**Medium Tracker:**
- ✅ CLI lists all articles with accurate counts
- ✅ HTML dashboard loads <2s with working sort/filter/search
- ✅ Cross-project tracking finds articles from multiple projects

**Multi-Strategy Backtester:**
- ✅ Batch backtest runs 10 strategies successfully
- ✅ Parallel execution achieves 2.5x+ speedup
- ✅ CSV/JSON/HTML exports generate valid output
- ✅ Optimization finds best parameters from grid
- ✅ Existing workflows still work (backward compatible)
- ✅ Error handling isolates failures
