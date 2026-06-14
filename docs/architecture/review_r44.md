# Architecture Review — Round 44 (2026-06-14)

## Architecture Health Assessment
- Overall Grade: 🟢 HEALTHY
- Key Metrics: 47 service modules, 0 god modules, 100% Streamlit-free, 319 tests passing (1 tone QA failure fixed)
- Changes since Round 41:
  - D-123 tone QA fix completed (replaced "建議" with "可" in screener_explanation_provider.py)
  - C167 AI Screener Explanations fully implemented and tested
  - Architecture remains HEALTHY with no new god modules introduced
  - Service count increased from 45 to 47 with the addition of screener_explanation_provider.py and stock_screener_service.py
  - Test count: 319 passed, 0 failed (tone QA fix resolved the 1 failure)

## C167 Architecture Assessment
- ScreenerExplanationProvider design:
  - ✅ Excellent adherence to ExplanationProvider protocol
  - ✅ Compose-and-enrich pattern using TemplateExplanationProvider as base
  - ✅ Zero Streamlit imports (pure service layer)
  - ✅ Historian tone enforced with mandatory disclaimer
  - ✅ Clean separation of explanation building and implication generation
  - ⚠️ Templates hardcoded in Python (D-121) rather than loaded from screener_templates.yaml
  - ✅ 27+ unit tests covering all preset types, custom filters, edge cases, and historian tone compliance

- screener_templates.yaml:
  - ✅ Well-structured YAML file with preset explanations, custom filter explanations, thresholds, and disclaimer
  - ⚠️ Currently unused by ScreenerExplanationProvider (templates hardcoded in Python)
  - ✅ Represents the intended future state for template management
  - ✅ Follows established YAML patterns from company_facts.yaml and case_studies.yaml

- New debt introduced:
  - D-121: Screener templates hardcoded, YAML not loaded (Medium severity, 1-2h effort)
    - The screener_explanation_provider.py contains hardcoded template dictionaries (_DIVIDEND_TEMPLATES, _GROWTH_TEMPLATES, etc.) instead of loading from src/data/screener_templates.yaml
    - This violates the D6 YAML migration pattern and creates maintenance overhead
    - The YAML file exists but is not utilized, creating duplication

## C163 + C40 Architecture Prerequisites
- experience_service.py feasibility:
  - ✅ Highly feasible - follows established pure service pattern
  - Should contain functions for: lesson progression tracking, gateway assessment, experience level determination
  - Must be zero Streamlit imports to maintain service layer purity
  - Will interface with session state for user_experience_level (beginner/expert only)

- gateway_lessons.yaml data design:
  - ✅ Should follow existing YAML patterns (company_facts.yaml, screener_templates.yaml)
  - Structure: lessons array with id, title, content, key_takeaways, quiz_questions
  - Must support the 4-lesson full-page soft gate for C163
  - Content should be in historian tone (past tense, factual) where applicable

- Session state impact:
  - ✅ Minimal impact - single shared key: user_experience_level (2 values: beginner/expert)
  - Binding Condition #1: 2-level session state only prevents complexity explosion
  - No additional session state keys beyond what's strictly necessary
  - State should be initialized on first visit and persist across sessions

- Architecture risks:
  - ⚠️ Per-page beginner mode specs (3-5 key sections) could lead to fragmentation if not standardized
  - ⚠️ Sidebar toggle (Zone B, NOT Zone A) requires consistent implementation across all 40+ pages
  - ⚠️ C163-alone ships with "coming soon" banner requires conditional rendering logic
  - ✅ Sprint 21 hard cut-line provides clear deadline for technical debt accumulation prevention

## New Debt Items
| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-121 | Screener templates hardcoded, YAML not loaded | Medium | 1-2h |
| D-122 | stock_screener.py 4 unsafe_allow_html instances | Medium | 1-2h |
| D-124 | TemplateExplanationProvider zero test coverage | Medium | 1-2h |

## Top 3 Recommendations
1. **Resolve D-121**: Refactor ScreenerExplanationProvider to load templates from src/data/screener_templates.yaml instead of hardcoding them in Python. This aligns with the D6 YAML migration pattern and eliminates template duplication.
2. **Resolve D-122**: Replace the 4 unsafe_allow_html instances in stock_screener.py with shared components from _router_base.py (_info_card, _summary_card) or create new reusable components in ui_components.py.
3. **Resolve D-124**: Add unit test coverage for TemplateExplanationProvider (similar to the existing test_screener_explanation.py structure) to ensure the fallback implementation remains reliable.

## Sprint 20 Mid-Cycle Verdict
The architecture remains HEALTHY post-C167 implementation with only minor debt introduced. The C167 feature successfully implemented the ExplanationProtocol pattern with zero Streamlit imports and comprehensive test coverage. The D-123 tone QA fix has been verified as complete. C163 and C40 are architecturally feasible with minimal session state impact and clear implementation paths. The three binding conditions provide appropriate guardrails to prevent architectural drift. Addressing the identified debt items (D-121, D-122, D-124) will maintain the HEALTHY architecture grade through the remainder of Sprint 20.