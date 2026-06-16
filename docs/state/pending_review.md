# Pending Review — Daniel Decisions

> **Last Updated**: 2026-06-17
> **Source**: Discussion Round 48 — Sprint 23 Planning

## Open Questions for Daniel

### Sprint 23 Decisions (Round 48) — NEED CONFIRMATION

#### 1. C200 Deferral Criteria — Auto-Defer Threshold
- **Context**: Revised Sprint 23 estimate is 37-57h (+2-3h gate), significantly above original 31-47h.
- **Proposal**: If C202 + C199 combined exceed 30h, C200 auto-deferred to Sprint 24.
- **Rationale**: C200 is COULD priority. If MUST + SHOULD consume >30h, the sprint doesn't have capacity for COULD.
- **Status**: ⏳ Pending Daniel — approve the 30h threshold?

#### 2. Four-Safeguard Pattern for C199 — Design Approval
- **Context**: C199 (Bear vs Bull Debate Cards) cannot start without the four-safeguard pattern designed.
- **Proposal**: PM + Designer define the pattern before C199 development. Pattern includes:
  1. Disclaimer at bottom
  2. "自動產生" label on each card
  3. Data-driven points only (no speculation)
  4. Banned word list enforcement
- **Status**: ⏳ Pending Daniel — any additional safeguards required?

#### 3. i18n Strategy — Services Return Keys, Pages Call t()
- **Context**: Standardizing i18n approach after discovering `story_arc_detector.py` returns raw Chinese.
- **Proposal**: All service-layer modules return keys (e.g., `growth`, `decline`). Page-level code calls `t()`.
- **Impact**: Requires refactoring `story_arc_detector.py` (211 lines).
- **Status**: ⏳ Pending Daniel — approve this as the standard pattern?

#### 4. story_arcs.yaml Scope Reduction
- **Context**: `story_arcs.yaml` currently contains display strings (Chinese labels, descriptions) that duplicate locale file purpose.
- **Proposal**: Move display strings to `locales/zh-TW.yaml` and `locales/en.yaml`. Keep only thresholds/colors in `story_arcs.yaml`.
- **Status**: ⏳ Pending Daniel — approve the scope reduction?

### Previously Open Items (Still Pending)

#### 5. C34 vs C46 Priority for Sprint 5 (from Round 10)
- **Context**: Sprint 5 can fit C34 (Company Story Timeline) + one of C46 (Moat Analysis) or C47 Phase 1.
- **Recommendation**: C34 is the vision P1 — should be Sprint 5 primary feature.
- **Status**: ⏳ Pending Daniel

#### 6. Dark/Light Theme Implementation (D-126)
- **Context**: Design review identified missing dark/light theme implementation.
- **Proposal**: Add theme preference in settings with CSS variables.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel

#### 7. Missing Component: _infocard() for Visual-First Metrics (D-127)
- **Context**: Missing _infocard() component for infographic-style visual cards.
- **Proposal**: Create _infocard(icon, sparkline_data, label, value, analogy) component.
- **Estimated Effort**: 6-9h
- **Status**: ⏳ Pending Daniel

#### 8. Missing Component: _calculator_card() for Interactive Tools (D-128)
- **Context**: Missing _calculator_card() component for interactive financial modeling.
- **Proposal**: Create _calculator_card() component with input fields and real-time output.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel

#### 9. Missing Component: _ai_explanation_card() for AI Explanations (D-129)
- **Context**: Missing _ai_explanation_card() component for AI-driven explanations.
- **Proposal**: Create _ai_explanation_card() component with visual indicator.
- **Estimated Effort**: 5-8h
- **Status**: ⏳ Pending Daniel

## Resolved This Cycle (Round 48)

| Item | Decision |
|------|----------|
| Locale directory conflict | Keep `locales/`, delete `src/core/locales/` |
| C202 i18n compliance | Refactor to return keys, page calls `t()` |
| story_arcs.yaml scope | Config only, display strings to locale files |
| C200 deferral criteria | C202 + C199 > 30h → auto-defer to Sprint 24 |
| C199 pre-sprint dependency | Four-safeguard pattern must be designed before development |
| C200 Week 1 gate | API caching + data completeness + historian framing |
| Sprint 23 total estimate | 37-57h (+2-3h gate), up from 31-47h |

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*
