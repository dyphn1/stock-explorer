# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Round 12
- **Date**: 2026-06-18
- **Participants**: PM, Architect, Designer, Developer, Challenger
- **Theme**: Round 12 Feature Proposals (C55-C62) from Competitor Research

## Idea Proposals
| ID | Feature | Owner | Status |
|----|---------|-------|--------|
| C55 | Investment Diary (Personal Reflection Journal) | Dev | ✅ Approved — Sprint 6 |
| C56 | Explain This Metric (Interactive Concept Explainer) | Dev | ✅ Approved — Sprint 5 (P1) |
| C57 | Compare Concepts (Financial Concept Comparison) | Dev | ✅ Approved — Sprint 6 |
| C58 | Beginner Onboarding Flow (Guided First Experience) | Dev | ✅ Approved — Sprint 5 (P1) |
| C59 | AI Q&A Chatbot (Natural Language Stock Questions) | Dev | ✅ Approved — Sprint 7+ |
| C60 | Concept Mastery Badges (Gamified Learning) | Dev | ✅ Approved — Sprint 5 |
| C61 | Sector Rotation Visualizer (Market Momentum Map) | Dev | ✅ Approved — Sprint 6 |
| C62 | Pre-Investment Checklist (Educational Scaffolding) | Dev | ✅ Approved — Sprint 5 |

## Decisions Made
1. **"Foundation + Education Core" direction adopted** — Reframed from "Education-First" to accurately reflect that C58 (onboarding) is UX, C60 (badges) is engagement, C59 (chatbot) is interface — all supporting the education core (C56 + C57 + C62).
2. **C58 moved to Sprint 5** — All three roles agree onboarding is a prerequisite for C56/C62 effectiveness. Users who bounce before onboarding won't benefit from metric explanations.
3. **C60 moved to Sprint 5** — Lowest-effort feature (8-14h), can be session-only MVP. Deferring to Sprint 7+ was unnecessarily conservative.
4. **Content creation starts Sprint 4** — C56 (10 metric explanations), C57 (10 concept pairs), C62 (7 checklist items) require significant content work. Begin in Sprint 4 as parallel workstream.
5. **C59 deferred to Sprint 7+** — Highest risk (18-28h), benefits from all education features being stable first.
6. **C61 depends on C51** — Sector Rotation Visualizer extends C51's market_data.py. Natural Sprint 6 placement after C51 completes in Sprint 4.
7. **business_card.py bloat mitigated** — D-025 (Sprint 3) + D24 (Sprint 4) are non-negotiable before C56/C62 touch the file.

## New Architecture Decisions
- `metric_explanations.yaml` — New YAML data file for metric explanations (C56)
- `concept_pairs.yaml` — New YAML data file for concept comparisons (C57)
- `badges.yaml` — New YAML data file for badge definitions (C60)
- `checklist_items.yaml` — New YAML data file for checklist content (C62)
- New card types: `_diary_card()` (green), `_checklist_card()` (amber), `_badge_card()` (blue)
- New page layouts: Investment Diary, Compare Concepts, AI Chatbot, Concept Mastery Badges

## New Architecture Debt
- D25: Session state scalability — 4 new features (C55, C60, C62, C58) add session state keys. Monitor and refactor to session state manager if needed. — P2
- D26: Content creation bottleneck — C56/C57/C62 require ~15h of content writing. Must start in Sprint 4 to avoid blocking Sprint 5-6. — P2

## Sprint Plan
| Sprint | Features | Est. Hours | Core Value |
|--------|----------|------------|------------|
| 3 (in progress) | C41 + C44 + C38 + D16 + D-025 | 33-50h | #1 Story, #3 Adaptive |
| 4 | R3 + D24 + C51 + C48 + C53-1 | 24-33h | #4 Visual-first, #1 Story |
| 5 | C58 + C62 + C56 + C60 | 42-68h | #4 Point-to-point, Ten-second test |
| 6 | C57 + C55 + C61 | 30-46h | #1 Story, #5 Benchmark |
| 7+ | C59 | 18-28h | #1 Story, #4 Point-to-point |

## Challenger's 3-Round Summary
| Round | Focus | Resolution |
|-------|-------|------------|
| 1 | Feature Direction | ✅ RESOLVED — "Education-First" reframed as "Foundation + Education Core"; only 4/8 features are purely educational |
| 2 | Priority | ✅ RESOLVED with revision — C58 moved to Sprint 5 (before/alongside C56); C60 moved to Sprint 5 |
| 3 | Goal Alignment | ✅ RESOLVED with conditions — M2 milestone partially addressed by C56/C58; business_card.py risk mitigated by D-025/D24; content creation starts Sprint 4 |

## Final PM Decision (Challenger ✅ Confirmed with Conditions)
**"Foundation + Education Core" direction adopted with revisions:**
- Sprint 5: C58 (Onboarding) + C62 (Checklist) + C56 (Explain Metric) + C60 (Badges)
- Sprint 6: C57 (Compare Concepts) + C55 (Diary) + C61 (Sector Rotation)
- Sprint 7+: C59 (AI Chatbot)
- Content creation for C56/C57/C62 starts in Sprint 4 as parallel workstream
- C58 uses modal-based tour (not CSS overlays) to work around Streamlit limitations
- C56 starts with 5 metrics, expands to 10 based on user feedback
- C60 is session-only MVP with clear user communication about ephemerality
- C59 uses pattern matching (not LLM) with strict historian guardrail

**Pending Daniel's Decision** (unchanged from previous):
1. C34 vs C46 priority for Sprint 5
2. C47 Phase 1 scope: 5 vs 10 lessons
3. Business Card Page IA: "above the fold" definition

## Next Cycle Handoff
Next: 🔧 Development → Sprint 3 continued (C41 + C44 + C38 + D16 + D-025)
Read `docs/state/handoff.md` for Sprint 3 entry point.

## Full Discussion Docs
- Architect: `docs/design/architect_discussion_r12.md`
- Designer: `docs/design/designer_discussion_r12.md`
- Developer: `docs/design/developer_discussion_r12.md`
- Challenger: `docs/design/challenger_discussion_r12.md`
