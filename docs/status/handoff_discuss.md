# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡)
- **Date**: 2026-06-10
- **Participants**: Product Manager, Architect, Developer, Design Reviewer, QA Engineer, Challenger

## Idea Proposals
| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| C02 | Notification / Push System (Email phase) | Architect + Dev | Approved — needs D02 architecture first |
| C04 | Market Thermometer | Dev | Approved — ~14h |
| C05 | Portfolio P&L Management | Dev | Needs Daniel approval — positioning risk |
| C06 | Auto-Generate PPT | Dev | Moved to Phase 2/3 — fix pages first |
| C07 | Customizable Event Thresholds | Dev | Depends on D01 (M5 verification) |
| C11 | Company Timeline Narrative | Architect | New — from review |
| C12 | Beginner Glossary | Design Reviewer | New — from review |

## Decisions Made
- **C05 (Portfolio P&L) needs Daniel decision** — may conflict with "historian, not stock picker" positioning
- **C06 moved to Phase 2/3** — standardize card components first, then export to PPT
- **C02 elevated in priority** — P0 gap, every competitor has it
- **D01 (M5 Verification) is #1 priority** — unverified engine blocks C07
- **D02 (Background Worker) must start now** — Streamlit is request-response only

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| D01 | M5 Event Detection Verification with real FinMind data | QA Engineer | Next dev cycle |
| D02 | Background Worker Architecture investigation | Architect | Next dev cycle |
| C05-decision | Daniel to decide on Portfolio P&L direction | Daniel | Pending |

## Next Cycle Handoff
Next theme: 🔍 Review (pm-review)
Read this file + issues.md to restore context.
