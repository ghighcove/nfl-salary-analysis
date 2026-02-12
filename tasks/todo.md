# NFL Analysis — TODO

## Deferred Medium Publishing

User is waiting 3-5 days before posting more articles to Medium. Both articles below are READY for import.

### Running Back Economics
- **Status:** Ready for Medium import (deferred)
- **GitHub Pages URL:** https://ghighcove.github.io/nfl-salary-analysis/article/rb_economics_20260211_1825.html
- **GEO Score:** 95/100 (A+)
- **Metadata:** See `article/MEDIUM_PUBLISH_INFO_rb_economics.md`
- **Created:** 2026-02-11
- **Key Findings:**
  - Round 3 RBs deliver +0.555 avg value (best ROI)
  - First-round RBs: +0.015 avg (near-zero value)
  - RBs peak in Years 1-2, crater by Year 3
  - UDFAs outperform drafted RBs (+0.065 vs -0.016)

### Quarterback Value Deep Dive
- **Status:** Ready for Medium import (deferred)
- **GitHub Pages URL:** https://ghighcove.github.io/nfl-salary-analysis/article/qb_deep_dive_20260211_1840.html
- **GEO Score:** 97/100 (A+)
- **Metadata:** See `article/MEDIUM_PUBLISH_INFO_qb_deep_dive.md`
- **Created:** 2026-02-11
- **Key Findings:**
  - Round 5 QBs deliver +0.623 avg value (best ROI)
  - Rookie contracts = +0.455, second contracts = -0.353 (value crater)
  - QB salaries grew 30.8% as % of cap (2015-2024)
  - Brock Purdy (+1.541) leads all QBs in career value

### When Ready to Publish (3-5 days)
For each article:
1. Go to Medium → New Story → Import a story
2. Paste GitHub Pages URL (from above)
3. Review table formatting in Medium editor
4. Add 5 tags from respective `MEDIUM_PUBLISH_INFO_*.md` file
5. Add SEO description in Medium settings (⋯ menu → Story settings → Advanced)
6. Preview and publish/schedule

---

## Completed
- [x] Project setup and dependency installation
- [x] Data acquisition (src/data_loader.py + notebook 01)
- [x] Data cleaning & merging (src/cleaning.py + notebook 02)
- [x] Value scoring (src/value_score.py + notebook 03)
- [x] Visualizations (src/viz.py + notebook 04)
- [x] End-to-end verification

## Future Enhancements
- [ ] Add play-by-play data for punter analysis
- [ ] Improve OL metrics beyond snap count (penalties, PFF grades if available)
- [ ] De-duplicate mid-season trade players (e.g., Lattimore "2TM" entries)
- [ ] Add interactive dropdown widget for player selection in notebook 04
