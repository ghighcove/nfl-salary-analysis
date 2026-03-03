# Tech Debt Queue — nfl

*Items Claude can process autonomously during `/idletime` sessions.*
*Created: 2026-02-22 | Phase 2 universal schema rollout*

---

## Legend

- **Risk**: LOW = safe without user input | MEDIUM = changes behavior, verify first
- **Est**: rough time estimate
- **Bucket**: `auto_sprint` = scheduled autonomous | `manual` = needs user | `billy_cron` = overnight | `blocked` = waiting
- **Status**: `open` | `in-progress` | `done` | `blocked`

---

## Priority 1 — Quick Wins (<10 min each)

| ID | Item | Risk | Est | Bucket | Status | Notes |
|----|------|------|-----|--------|--------|-------|
| TD-01 | Review tasks/context.md for stale state | LOW | 5 min | auto_sprint | done | Stale (Feb 13, 10 days). Key outdated: trading_bot now has GitHub remote; TE article (Feb 20) likely published. Full rewrite needs user — add to TDU queue. |
| TD-02 | Review tasks/todo.md and migrate open items to this file | LOW | 10 min | auto_sprint | done | Migrated: 2 Medium publish items → TDU-02/03; 4 future enhancements → TDU-04. See below. |

---

## Priority 2 — System Hygiene (10–20 min each)

| ID | Item | Risk | Est | Bucket | Status | Notes |
|----|------|------|-----|--------|--------|-------|
| TD-10 | Audit CLAUDE.md for bloat (target <60 lines) | LOW | 10 min | auto_sprint | done | 148 lines — CRITICAL bloat. Already flagged in TD-13 (manual/MEDIUM: create .claude/rules/, migrate publishing + platform sections). No autonomous action — needs user. |
| TD-11 | Review tasks/lessons.md for promotable patterns (2+ occurrences) | LOW | 15 min | auto_sprint | done | Reviewed 2026-02-25. 4 lessons sections: Medium import nav, Medium caching (already in CLAUDE.md), form_input fallback, and data join patterns. Caching pattern already promoted. Others are single occurrences — below 2+ threshold. No new promotions needed. |
| TD-12 | Run git log --oneline -10 and verify commit hygiene | LOW | 5 min | auto_sprint | done | Last commit Feb 22 (clean). Incomplete CLAUDE.md audit discarded — .claude/rules/ never created. See TD-13. |
| TD-13 | Proper CLAUDE.md audit: create .claude/rules/ and migrate content | MEDIUM | 30 min | manual | done | **DONE 2026-03-02.** CLAUDE.md 149→27 lines. Publishing workflow moved to .claude/rules/publishing.md. |

---

## Priority 3 — Requires User Input

| ID | Item | Risk | Est | Bucket | Status | Notes |
|----|------|------|-----|--------|--------|-------|
| TDU-01 | Define offseason data plan | — | 30 min | manual | done | **DONE 2026-03-02.** Decision: nothing runs until mid-July. Disabled: picks-daily-note, picks-evening-resolve, picks-weekly-article-writer (all Task Scheduler → Disabled). Re-enable mid-July when preseason data becomes relevant. |
| TDU-02 | Publish RB Economics to Medium | — | 10 min | manual | done | Published Feb 27. |
| TDU-03 | Publish QB Deep Dive to Medium | — | 10 min | manual | open | Ready. URL: ghighcove.github.io/nfl-salary-analysis/article/qb_deep_dive_20260211_1840.html. GEO 97/100. Publish after RB. Defer until 2026-03-09. |
| TDU-04 | Future enhancements — review and prioritize | — | 20 min | manual | open | From todo.md: play-by-play punter data, OL metrics (PFF?), de-dupe trade players, interactive dropdown widget. Defer until 2026-07-15 (after offseason, when season prep begins). |

---

## Completed

| ID | Item | Completed | Notes |
|----|------|-----------|-------|
| — | tech_debt.md initialized | 2026-02-22 | Phase 2 universal schema rollout |

---

*Add new items with next available ID. Idletime sessions pull P1→P2 in order.*
*Never move TDU-* items into autonomous batch — always requires user.*
