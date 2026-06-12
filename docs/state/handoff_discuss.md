# Handoff – Discussion (Round 14)

## Summary
- **Topic**: Discussion (💡) — Round 14
- **Date**: 2026-06-19
- **Participants**: Product Manager, System Architect, Developer, Designer, Challenger

## Features Evaluated (C63-C68, from Round 13 Competitor Research)

### Idea Proposals
| ID | Feature | Effort | Direction | Sprint |
|----|---------|--------|-----------|--------|
| C63 | Audio Market Story (weekly) | 18-24h | Content-first | Sprint 8 |
| C64 | Community Q&A | 26-38h | Community | Sprint 8 |
| C65 | Company Story Game | 22-32h | Engagement | Sprint 7 |
| C66 | Conversational Tone | 13-20h | Quick win | Sprint 3/4 fast-track |
| C67 | Community-Curated Stories | 26-38h | Community | Sprint 9+ |
| C68 | Financial Concept Storytelling | 30-44h | Education (P1) | Sprint 6-7 |

## Decisions Made
1. **C66 fast-tracked** — Zero dependency, can start immediately in late Sprint 3 / Sprint 4
2. **C63 deferred to Sprint 8** — D28 audio infrastructure risk too high for Sprint 7
3. **C63 scope: weekly not daily** — 52/year max to limit content burden
4. **D22 promoted to Sprint 6 P0** — Persistence layer hard prerequisite for C64/C67
5. **Content cap: 100 items max** — Hard limit until team capacity proven
6. **Content creation starts Sprint 4** — Parallel workstream for C68/C63/C65 content
7. **Mandatory historian tone QA gate** — Cross-cutting checkpoint before any content feature ships
8. **C68 split 5+5 concepts** — First 5 in Sprint 6, remaining 5 in Sprint 7
9. **Sprint 5/6 cut-line rules** — Must be defined before Sprint 5 starts

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| C66 | Start conversational tone rewrite (parallel workstream) | Dev + Designer | Sprint 3 late |
| D22 | Build persistence layer (YAML-based, following watchlist pattern) | Dev | Sprint 6 |
| C68-content | Write first 5 concept stories (P/E, ROE, P/B, Gross Margin, Debt Ratio) | PM/Designer | Sprint 4-5 |
| C63-content | Write weekly audio script templates (5-7 templates) | PM/Designer | Sprint 4-5 |
| C65-content | Extend company_facts.yaml to 15+ companies | PM/Designer | Sprint 4-5 |
| QA-gate | Define historian tone QA checklist | Designer | Sprint 4 |
| Cut-line | Define Sprint 5/6 cut-line rules | PM | Before Sprint 5 |

## Challenger 3-Round Summary
- **Round 1 (Feature Direction)**: ✅ RESOLVED — Hour inflation explained; C63 dependency chain clarified; C65 redefinition validated; D22 commitment required
- **Round 2 (Priority)**: ✅ RESOLVED — C66 fast-tracked; C63/C65 sequencing reversed; content creation parallelized; D22 promoted to P0
- **Round 3 (Goal Alignment)**: ✅ RESOLVED — Content sustainability cap added; historian tone QA gate mandated; sprint cut-line rules required

## Final PM Decision
Direction B ("Quick Wins + Shared Infrastructure") adopted with 7 Challenger conditions:
- Sprint 3/4: C66 (immediate, parallel)
- Sprint 6: C68 (first 5 concepts) + D22 persistence layer
- Sprint 7: C65 game + C68 (remaining 5 concepts)
- Sprint 8: C63 (weekly audio) + C64 (community Q&A)
- Sprint 9+: C67 (community stories, after C64 stable)
- Content cap: 100 items max; C63 weekly only
- Mandatory historian tone QA gate before each feature ships
- Sprint 5/6 cut-line rules defined before Sprint 5

## New Architecture Debt
- D28: Audio service layer for C63 — Medium
- D29: Community service layer for C64/C67 — Medium
- D30: Game state management for C65 — Medium
- D22: Persistence layer promoted to P0 — unblocks C64/C67

## Competitor Insights Addressed
- Audio modality (C63 weekly audio story)
- Social learning (C64 community Q&A, C67 community stories)
- Gamification (C65 company story game)
- Conversational tone (C66 UX writing overhaul)
- Narrative-based education (C68 concept storytelling)
- User-generated content (C67 community stories)

## Next Cycle Handoff
Next: 🔧 Development → Sprint 3 continued (C41 + C44 + C38 + D16 + D-025)
