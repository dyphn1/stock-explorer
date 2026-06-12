# Handoff – Development

## Summary
- **Topic**: Development (🔧) — Sprint 9
- **Date**: 2026-06-13
- **Participants**: Product Manager, Developer

## Sprint Goal
Implement Sprint 9 features (C98 + C101 + C103 Lite) after Day 1 prerequisite D-057.

## Prerequisites (Day 1)
- **D-057**: Consolidate duplicate `_section_title()` — `_router_base.py` version is canonical (with emoji-prefix logic + empty-title guard). `_helpers.py` version (icon, title signature) must be removed and all callers updated to use `_router_base._section_title`. Effort: 3-4h.

## Completed Items
| Issue ID | Description | Owner | Result |
|----------|-------------|-------|--------|
| D-057 | LLM abstraction / _section_title consolidation | Dev | 🔄 In Progress |
| C103 Lite | First Visit Guide (2-card primer) | Dev | 🔄 In Progress |
| C101 | Comprehension Check Quiz (5-8 generic questions) | Dev | 🔄 In Progress |

## Pending Items
| Issue ID | Description | Owner | Next Steps |
|----------|-------------|-------|------------|
| C98 | Event Interpretation Engine (Hybrid) | Dev | ⏸️ Waiting for D-057 completion |
| D-058 | Quiz engine deduplication | Dev | 📋 After C101 |
| D-060 | Event interpretation facade | Dev | 📋 After C98 |

## Feature Specs

### C103 Lite — First Visit Guide
- **Pattern**: 2-card dismissible primer shown on first visit
- **Card 1**: "你將學到什麼" — what the user will learn from Stock Explorer
- **Card 2**: "免責聲明" — historian disclaimer (not a stock picker)
- **Behavior**: Dismissible with single "我知道了" button, uses `st.session_state` to track dismissal
- **Mobile**: Optimized for mobile layout
- **Files**: New `src/pages/first_visit_guide.py`, import in `router.py`
- **Effort**: 8-11.5h

### C101 — Comprehension Check Quiz
- **Pattern**: 5-8 generic questions (not stock-specific in Sprint 9)
- **Reuses**: `financial_wellness_service.py` pattern (YAML config, service layer, page layer)
- **Config**: New `config/comprehension_quiz.yaml` with questions
- **Service**: New `src/services/comprehension_quiz_service.py`
- **Page**: New `src/pages/comprehension_check.py` — embedded in business card sections (after story section)
- **Display**: Inline quiz card pattern using `_白话_card()` and form components
- **Effort**: 8-12h

### C98 — Event Interpretation Engine (Hybrid)
- **Approach**: Templates for dashboard event summaries (replacing plain summaries), LLM for individual event drill-down
- **Spike**: 2h to validate LLM approach (confirm LLM client exists or create one)
- **Dashboard**: Interpretation card replaces event summary on event_dashboard.py
- **Drill-down**: Clicking an event opens detailed plain-language explanation
- **Ten-second test**: User can restate the core concept within 10 seconds
- **Files**: `src/services/event_interpretation_service.py` (new), modifies `event_dashboard.py`
- **Effort**: 16-23.5h + 2h spike

## Decisions Made
1. D-057 is Day 1 prerequisite — must complete before C98 coding begins
2. C103 and C101 are independent — can proceed in parallel with D-057
3. Implementation order: C103 Lite → C101 → C98 (lowest to highest risk)
4. Mid-sprint checkpoint after C103 + C101 complete

## Next Cycle Handoff
🔧 Development → Sprint 9 (C98 + C101 + C103 Lite) → 🔍 Review Round 22 → Sprint 10 (C34 + M5 remediation + D-061)
