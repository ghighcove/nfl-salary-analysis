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
| TD-01 | Review tasks/context.md for stale state | LOW | 5 min | auto_sprint | open | Last context save may be stale |
| TD-02 | Review tasks/todo.md and migrate open items to this file | LOW | 10 min | auto_sprint | open | Consolidate todo.md into tech_debt queue format |

---

## Priority 2 — System Hygiene (10–20 min each)

| ID | Item | Risk | Est | Bucket | Status | Notes |
|----|------|------|-----|--------|--------|-------|
| TD-10 | Audit CLAUDE.md for bloat (target <60 lines) | LOW | 10 min | auto_sprint | open | Run /claude-md-audit if >60 lines |
| TD-11 | Review tasks/lessons.md for promotable patterns (2+ occurrences) | LOW | 15 min | auto_sprint | open | Promote critical patterns to CLAUDE.md |
| TD-12 | Run git log --oneline -10 and verify commit hygiene | LOW | 5 min | auto_sprint | done | Last commit Feb 22 (clean). CLAUDED.md has large uncommitted rewrite (148→9 lines) — likely incomplete audit, flagged for user review |

---

## Priority 3 — Requires User Input

| ID | Item | Risk | Est | Bucket | Status | Notes |
|----|------|------|-----|--------|--------|-------|
| TDU-01 | Define offseason data plan | — | 30 min | manual | blocked | NFL season ended; determine what weekly processes to disable/pause |

---

## Completed

| ID | Item | Completed | Notes |
|----|------|-----------|-------|
| — | tech_debt.md initialized | 2026-02-22 | Phase 2 universal schema rollout |

---

*Add new items with next available ID. Idletime sessions pull P1→P2 in order.*
*Never move TDU-* items into autonomous batch — always requires user.*
