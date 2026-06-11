# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Round 13
- **Date**: 2026-06-19
- **Participants**: PM, Architect, Designer, Developer, Challenger
- **Theme**: Round 13 Feature Directions — Education Core Expansion

## Idea Proposals
| ID | Feature | Owner | Status |
|----|---------|-------|--------|
| C34 | Company Story Timeline (Historical Event Timeline) | Dev | ✅ Approved — Sprint 6 (spike in Sprint 4) |
| B | Notification System for Learning Engagement | Dev | ✅ Approved — Sprint 6 (moved from Sprint 5) |
| C3 | AI-Augmented Historical Narrator | Dev | ❌ Indefinitely Deferred (overlap risk) |
| D | Quick Wins Bundle (C62+C60+C55) | Dev | ✅ Approved — Sprint 5 (confirmed from Round 12) |

## Decisions Made
1. **C3 (AI Narrator) indefinitely deferred** — Overlap risk with C34, C56, and C59 is too high. Can be revisited in Sprint 8+ after education core stabilizes. Saves 14-22h.
2. **Notification System moved to Sprint 6** — Value in Sprint 5 is limited (only Quick Wins content to notify about). Moving to Sprint 6 allows it to notify about C56, C34, and the full education core. Frees 8-14h in Sprint 5 for C56 content creation.
3. **C34 spike in Sprint 4 (4-6h)** — Prototype using Streamlit native components to de-risk Sprint 6 implementation. Validates concept without significant investment.
4. **C56 contingent on D24** — If D24 completes in Sprint 4, C56 is in Sprint 5. If D24 slips, C56 moves to Sprint 6.
5. **Content creation starts Sprint 4** — 19-30h content creation burden must start in Sprint 4 as parallel workstream. Non-negotiable for Sprint 5 readiness.
6. **Session state audit in Sprint 5** — Before adding more session state keys, audit current usage and consider session state manager pattern (D25).

## Revised Sprint Plan
| Sprint | Features | Effort | Dependencies |
|--------|----------|--------|-------------|
| **Sprint 3** (in progress) | C44 + C38 + D16 | 24-29h | — |
| **Sprint 4** | R3 + D24 + C51 + C48 + C53-1 + C34 spike | 28-39h | D16 |
| **Sprint 5** | C58 + C62 + C60 + C55 + C56 (if D24 ready) | 42-68h (50-82h w/ C56) | D24 |
| **Sprint 6** | C57 + C61 + C34 (full) + Notification System | 46-68h | C51, D24 |
| **Sprint 7+** | C59 | 18-28h | All education features stable |

## Revised Total Effort
- New (Round 13, revised): 52-80h code + 16-24h content = 68-104h
- With buffer: 82-125h
- Total remaining (all sprints): 154-260h (185-312h with buffer)

## New Architecture Decisions
- `historical_timeline.py` — New service for C34 (Sprint 6)
- `event_templates.yaml` — New data file for C34 event types (content creation Sprint 4-5)
- `notification_service.py` — New service for notification system (Sprint 6)
- `notification_templates.yaml` — New data file for notification templates
- New card type: `_timeline_card()` (gold border, #F4D03F) for C34

## New Architecture Debt
- D27: C34 timeline UI complexity — Streamlit has no native timeline component; prototype spike needed to validate approach — P2
- D28: Notification system session state tracking — adds 6+ new session state keys; monitor for D25 escalation — P2

## Challenger's 3-Round Summary
| Round | Focus | Resolution |
|-------|-------|------------|
| 1 | Feature Direction | ✅ PARTIALLY RESOLVED — C34 M3-before-M2 concern acknowledged; C3 overlap confirmed; Direction D scope inconsistency noted |
| 2 | Priority | ✅ RESOLVED with revision — C34 spike in Sprint 4; Notification System moved to Sprint 6 |
| 3 | Goal Alignment | ✅ RESOLVED with conditions — C3 indefinitely deferred; C56 contingent on D24; content creation starts Sprint 4 |

## Final PM Decision (Challenger ✅ Confirmed with 4 Conditions)
**"Education Core Expansion" direction adopted with revisions:**
- Sprint 5: C58 + C62 + C60 + C55 + C56 (if D24 ready)
- Sprint 4: C34 spike (4-6h prototype)
- Sprint 6: C34 (full) + C57 + C61 + Notification System
- Sprint 7+: C59
- C3 (AI Narrator) indefinitely deferred
- Content creation for all YAML files starts Sprint 4 as parallel workstream
- D24 is the single most critical enabler — non-negotiable for Sprint 4

**Pending Daniel's Decision** (unchanged from previous):
1. C34 vs C46 priority for Sprint 5
2. C47 Phase 1 scope: 5 vs 10 lessons
3. Business Card Page IA: "above the fold" definition

## Next Cycle Handoff
Next: 🔧 Development → Sprint 3 continued (C44 Risk Analysis MVP)
Read `docs/state/handoff.md` for Sprint 3 entry point.

## Full Discussion Docs
- Architect: `docs/design/architect_discussion_r13.md`
- Designer: `docs/design/designer_discussion_r13.md`
- Developer: `docs/design/developer_discussion_r13.md`
- Challenger: `docs/design/challenger_discussion_r13.md`
