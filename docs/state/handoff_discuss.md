# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Round 11
- **Date**: 2026-06-18
- **Participants**: PM, Architect, Designer, Developer, Challenger
- **Theme**: Round 11 Feature Proposals (C48-C54) from Competitor Research

## Idea Proposals
| ID | Feature | Owner | Status |
|----|---------|-------|--------|
| C48 | Company Story Card (replaces C37) | Dev | ✅ Approved — Sprint 4 |
| C49 | Daily Market Pulse | Dev | ✅ Approved — Sprint 5 |
| C50 | Learning Progress Tracker | Dev | ⏳ Deferred — Sprint 5+ (needs D22 persistence layer) |
| C51 | Sector Heatmap | Dev | ✅ Approved — Sprint 4 |
| C52 | Quiz Mode (20-question MVP) | Dev | ✅ Approved — Sprint 5 |
| C53 | Social Sharing (2-phase) | Dev | ✅ Approved — Sprint 4 (URL) + Sprint 5 (Image) |
| C54 | Video/Audio Explanation | Dev | ⏳ Deferred — Sprint 5+ (needs R7 LLM + TTS) |

## Decisions Made
1. **C48 replaces C37** (not alongside) — avoids page overload, fixes D-016 hero card style simultaneously
2. **C51 is Sprint 4's highest priority** — introduces `market_data.py` shared infrastructure for market-level data
3. **C49 follows C51 in Sprint 5** — reuses `market_data.py`, adds scheduling complexity
4. **C52 scoped to 20-question MVP** — reduces content creation from 10-15h to 5h
5. **C53 in two phases** — URL sharing (2-3h) in Sprint 4, image generation (5-9h) in Sprint 5
6. **C50 and C54 deferred** — remain in backlog with infrastructure blockers documented (D22, R7)
7. **New tone guidelines for market-level features** — "過去發生" language, factual not predictive
8. **R3 and D16 are hard prerequisites for Sprint 4** — if they slip, defer C51 and keep C48 + C53-1

## New Architecture Decisions
- `market_data.py` — new service for market-level data aggregation (shared by C49, C51)
- `story_composer.py` — new service for composing company stories (C48)
- `export_service.py` — new utility for HTML-to-image rendering (shared by C48, C53)
- `sector_mapping.yaml` — new YAML data file for sector classifications
- `quiz_questions.yaml` — new YAML data file for quiz question bank

## New Architecture Debt
- D23: Tone guidelines needed for market-level features (C49, C51) — P2
- D24: business_card.py will grow further with C48 — consider extracting to sub-directory — P2

## Sprint Plan
| Sprint | Features | Est. Hours | Core Value |
|--------|----------|------------|------------|
| 3 (in progress) | C44 + C41 + C38 + R1 + D16 | 33-50h | #1 Story, #3 Adaptive |
| 4 | C51 + C48 + C53(Phase 1) | 24-33h | #4 Visual-first, #1 Story |
| 5 | C49 + C52 + C53(Phase 2) | 33-47h | #3 Daily engagement, #5 Assessment |
| 5+ | C50 + C54 | 46-69h | #2 Structured education |

## Challenger's 3-Round Summary
| Round | Focus | Resolution |
|-------|-------|------------|
| 1 | Feature Direction | ✅ RESOLVED — C48 replaces C37; market_data.py is right direction; C52 scoped to 20 questions |
| 2 | Priority | ✅ RESOLVED — C51 first (new infrastructure), C48 second (replaces existing), C49 after C51 |
| 3 | Goal Alignment | ✅ RESOLVED — Market features align with historian positioning IF tone guidelines enforced; Sprint 4 load manageable; C50/C54 stay in backlog |

## Final PM Decision (Challenger ✅ Confirmed)
**Direction A ("Quick Wins + Visual Impact") adopted with modifications:**
- C48 replaces C37 (fixes D-016)
- C51 first in Sprint 4 (introduces market_data.py)
- C49 in Sprint 5 (reuses market_data.py)
- C52 scoped to 20-question MVP
- C53 in two phases (URL → image)
- C50 and C54 deferred with blockers documented

## Pending Daniel's Decision
(No new items — existing items remain)
1. C34 vs C46 priority for Sprint 5
2. C47 Phase 1 scope (5 vs 10 lessons)
3. Business Card Page IA: "above the fold" definition

## Next Cycle Handoff
Next: 🔧 Development → Sprint 3 (C44 + C41 + C38 + R1 + D16)
Read `docs/state/handoff.md` for Sprint 3 entry point.

## Full Discussion Docs
- Architect: `docs/design/architect_discussion_r11.md`
- Designer: `docs/design/designer_discussion_r11.md`
- Developer: `docs/design/developer_discussion_r11.md`
- Challenger: `docs/design/challenger_discussion_r11.md`
