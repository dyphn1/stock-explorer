# Stock Explorer Developer Estimates - Review Cycle 46

## Feature Implementation Estimates

| ID | Title | Low Estimate (hrs) | High Estimate (hrs) | Risk Level |
|----|-------|-------------------|---------------------|------------|
| C199 | "Bear vs Bull" Visual Debate Cards | 8 | 12 | Medium |
| C200 | "What If I Had Invested?" Historical Scenario Calculator | 10 | 14 | Medium |
| C201 | "Daily Market Story" — 3-Minute Morning Briefing | 12 | 16 | High |
| C202 | "Story Arc" Timeline Labels | 8 | 10 | Low |
| C203 | "Supply Chain Impact" Visual Map | 14 | 18 | High |
| C204 | "Confidence Indicator" on AI Explanations | 4 | 6 | Low |
| C205 | "Read Time" Indicator on All Content | 2 | 4 | Low |
| C206 | "Recurring Investment" Concept Education | 6 | 8 | Low |

## Technical Debt Fix Estimates

| ID | Description | Low Estimate (hrs) | High Estimate (hrs) | Risk Level |
|----|-------------|-------------------|---------------------|------------|
| D-125 | Split `chart_stock.py` (818 lines) into focused sub-modules | 2 | 3 | Medium |
| D-126 | Extract `INDUSTRY_BENCHMARKS` dict to shared location | 0.5 | 0.5 | Low |
| D-127 | Split `_summary.py` (464 lines) when it exceeds 500 lines | 1 | 2 | Low |
| D-130 | Replace fragile `st.html()` JS approach in `_detail.py` with pure Streamlit | 1 | 2 | Low |

## Design Improvement Estimates

| ID | Description | Low Estimate (hrs) | High Estimate (hrs) | Risk Level |
|----|-------------|-------------------|---------------------|------------|
| D-121 | Document missing components in design system (`_mini_score_card`, `_glossary_tooltip`, `_so_what_box`) | 2 | 3 | Low |
| D-122 | Fix inconsistent card styling in `sector_heatmap.py` | 3 | 5 | Low |
| D-123 | Refactor `watchlist_page.py` to use card-based PPT style instead of dense table layout | 4 | 6 | Medium |
| D-124 | Replace inline HTML in `etf_browser.py` with standard components | 3 | 5 | Low |
| D-125 | Audit and replace raw `st.markdown` headers with `_section_title()` | 2 | 4 | Low |
| D-126 | Implement dark/light theme toggle with CSS variables | 8 | 12 | Medium |
| D-127 | Create `_infocard()` component for visual-first metric presentation | 6 | 9 | Medium |
| D-128 | Create `_calculator_card()` component for interactive financial tools | 8 | 12 | Medium |
| D-129 | Create `_ai_explanation_card()` component for AI-driven move explanations | 5 | 8 | Medium |
| D-130 | Implement structured beginner onboarding flow (3-step carousel) | 10 | 15 | High |

## Sprint Planning Recommendations

### What Can Fit in Sprint 21 (Next Sprint)
Based on the architect's recommendations and current sprint capacity:

**Prerequisites (Day 1 of Sprint 21):**
- D-125: Split `chart_stock.py` (2-3h) - **REQUIRED before C170/C194**
- D-126: Extract `INDUSTRY_BENCHMARKS` dedup (0.5h) - Quick win

**Week 1 (Lead Feature):**
- C170: Tappable Glossary (12-18h) - Already planned
- C205: Read Time Indicators (2-4h) - Quick win, high impact

**Week 2 (Retention Feature):**
- C188: Why Did This Move? (6-9h) - Already planned
- C204: Confidence Indicator on AI Explanations (4-6h) - Should be combined with C188

**Stretch Goals (if capacity allows):**
- C202: Story Arc Timeline Labels (8-10h) - Low risk, good ROI
- D-127: Monitor `_summary.py` split (1-2h) - Only if C170 pushes past 500 lines
- D-121: Document missing components in design system (2-3h)

### What Should Wait for Sprint 22+
**Short-term (Sprint 22-23):**
- C201: Daily Market Story (12-16h) - P1, elevated from C196
- C199: Bear vs Bull Visual Debate Cards (8-12h)
- D-123: Fix watchlist_page.py table layout (4-6h)
- D-126: Implement dark/light theme toggle (8-12h)
- D-127: Create _infocard() component (6-9h)
- C186: Daily 5-Min Finance Lesson (10-14h) - Concept-focused daily touchpoint

**Medium-term (Sprint 24+):**
- C200: What If I Had Invested? Calculator (10-14h)
- C203: Supply Chain Impact Visual Map (14-18h)
- C206: Recurring Investment Concept Education (6-8h)
- D-128: Create _calculator_card() component (8-12h)
- D-129: Create _ai_explanation_card() component (5-8h)
- D-130: Structured beginner onboarding flow (10-15h)

## Dependency Map

### What Blocks What
- **D-125** blocks C170 (Tappable Glossary chart additions) and C194 (glossary-related charts)
- **D-126** prevents data divergence when adding new industry benchmarks
- **C170** (Tappable Glossary) is foundational for:
  - C204 (Confidence Indicators on explanations)
  - C205 (Read Time Indicators on glossary terms)
  - Future AI explanation features
- **C188** (Why Did This Move?) provides the AI explanation foundation for:
  - C204 (Confidence Indicators)
  - D-129 (_ai_explanation_card() component)
- **D-127** (_infocard() component) enables:
  - Visual-first metric presentation in business card
  - Competitive parity with Simply Wall St infographics
- **D-126** (dark/light theme) is a prerequisite for:
  - Modern UI expectations
  - Accessibility compliance
- **C201** (Daily Market Story) depends on:
  - M5 event detection (existing)
  - Analogy engine (existing)
  - Homepage card infrastructure
- **C203** (Supply Chain Impact) depends on:
  - Existing group structure mapping (point-to-point)
  - Customer-supplier relationship data (manual curation needed)
- **D-129** (_ai_explanation_card()) depends on:
  - C188 implementation
  - Confidence indicator system (C204)

### Critical Path for Sprint 21
1. D-125 → C170 → (C204 + C205) → C188
2. D-126 (can be done in parallel)

## Risk Assessment

### High-Risk Items That Need Spikes
1. **C201: Daily Market Story** (12-16h, High risk)
   - Risk: Content freshness and relevance - need to verify M5 event detection reliability
   - Spike needed: 2h to test M5 integration with analogy engine for daily story generation

2. **C203: Supply Chain Impact Visual Map** (14-18h, High risk)
   - Risk: Data acquisition and manual curation effort for customer-supplier relationships
   - Spike needed: 3h to research data sources and design mapping approach

3. **D-130: Structured beginner onboarding flow** (10-15h, High risk)
   - Risk: User experience design and educational effectiveness
   - Spike needed: 2h to prototype onboarding flow with comprehension_check framework

4. **C200: What If I Had Invested? Calculator** (10-14h, Medium risk)
   - Risk: Historical data accuracy and edge case handling (splits, dividends)
   - Spike needed: 2h to test FinMind historical data integration

### Medium-Risk Items
- **D-123: Watchlist page refactor** (4-6h, Medium risk)
  - Risk: Breaking existing user workflows; need to maintain functionality while improving UI
- **D-126: Dark/light theme implementation** (8-12h, Medium risk)
  - Risk: CSS variable integration and chart/adaptation compatibility

### Low-Risk Items (Safe for Sprint 21)
- C202, C204, C205, C206, D-125, D-126, D-127, D-128, D-129 (design system docs, styling fixes)

## Total Estimated Effort

### Feature Implementation Estimates
- Low: 8 + 10 + 12 + 8 + 14 + 4 + 2 + 6 = **64 hours**
- High: 12 + 14 + 16 + 10 + 18 + 6 + 4 + 8 = **98 hours**
- Average: **81 hours**

### Technical Debt Fix Estimates
- Low: 2 + 0.5 + 1 + 1 = **4.5 hours**
- High: 3 + 0.5 + 2 + 2 = **7.5 hours**
- Average: **6 hours**

### Design Improvement Estimates
- Low: 2 + 3 + 4 + 3 + 2 + 8 + 6 + 8 + 5 + 10 = **51 hours**
- High: 3 + 5 + 6 + 5 + 4 + 12 + 9 + 12 + 8 + 15 = **79 hours**
- Average: **65 hours**

### Overall Total Estimated Effort
- Low: 64 + 4.5 + 51 = **119.5 hours**
- High: 98 + 7.5 + 79 = **184.5 hours**
- Average: **152 hours**

## Summary for PM Consolidation

Based on Review Cycle 46 analysis, Stock Explorer has clear opportunities to enhance its competitive position through targeted feature investments and necessary technical debt resolution. 

**Key Priorities for Sprint 21:**
1. **Resolve blocking technical debt first**: D-125 (chart split) and D-126 (benchmark dedup) are prerequisites for planned features
2. **Leverage quick wins**: C205 (Read Time Indicators) offers high impact for low effort
3. **Combine related work**: C204 (Confidence Indicators) should be implemented alongside C188 (Why Did This Move?)
4. **Address retention-critical features**: C201 (Daily Market Story) addresses the #1 retention pattern identified in competitor research

**Risk Mitigation:**
- Spike high-risk items (C201, C203, D-130) before committing to estimates
- Monitor file sizes to prevent new technical debt accumulation
- Maintain focus on beginner-friendly execution per core value #1

**Competitive Advantage Opportunities:**
- C202 (Story Arc Timeline Labels) represents a unique differentiator with no competitor offering
- C199 (Bear vs Bull Visual Debate Cards) strengthens the "historian" positioning
- D-127 (_infocard()) closes the visual-first gap with Simply Wall St

The estimated effort for immediate actionable items in Sprint 21 ranges from 34.5-50.5 hours, leaving capacity for the planned C170 and C188 features within a typical sprint allocation.