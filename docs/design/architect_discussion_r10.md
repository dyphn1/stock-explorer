# Stock Explorer — Architect Discussion Round 10

> **Date**: 2026-06-15
> **Author**: System Architect
> **Purpose**: Technical feasibility analysis of Round 9 feature proposals (C42, C44, C46, C47) for Sprint 3+ planning
> **Context**: Sprint 2 complete (C37, C39, C45, C43 ✅). Sprint 3 next. C43 and C45 already implemented.

---

## Problem Description

Round 9 competitor research identified 6 feature gaps (C42-C47). Two were P1 (C42 Stock Screener, C43 Snowflake Health Viz) and four were P2 (C44 Risk Analysis, C45 Valuation Band, C46 Moat Analysis, C47 Education Academy). C43 and C45 were implemented in Sprint 2, leaving C42 (P1), C44 (P2), C46 (P2), and C47 (P2) for discussion.

The core strategic question for Round 10: **Which of these four remaining features should Stock Explorer build next, given our "historian, not stock picker" positioning, Streamlit-only constraint, FinMind data dependency, and current architecture state?**

Key constraints:
- **C42 (Stock Screener, P1, 16-24h)**: Transforms the product from lookup to discovery — the biggest strategic gap
- **C44 (Risk Analysis, P2, 10-14h)**: Unique "historian" differentiator — explain historical risks, don't predict
- **C46 (Moat Analysis, P2, 12-16h)**: No TW competitor has this; manual curation required
- **C47 (Education Academy, P2, 20-30h)**: Largest effort; transforms tool into platform

---

## Feature-by-Feasibility Analysis

### C42: Stock Screener / Discovery Engine

| Dimension | Assessment |
|-----------|------------|
| **Technical Feasibility** | 🟡 Medium — New page + service layer; no existing screener infrastructure |
| **Architecture Debt Dependencies** | D7 (N+1 API calls in category_browser) — the screener would face the same problem at scale. R3 (batch API) should be done first. D6 (hardcoded data) — screening presets would add more hardcoded data unless YAML-first approach is taken. |
| **Data Source Availability** | ✅ FinMind provides all needed metrics: P/E, ROE, dividend yield, revenue growth, debt ratio, etc. `get_stock_info()` already loads the full universe. Screening is a filtering/aggregation layer on top of existing data. |
| **Integration Complexity** | 🟡 Medium — New page (`src/pages/stock_screener.py`) + new service (`src/services/screener_engine.py`). Results link to existing `business_card.py` via `navigate_to()`. The category browser page already does similar filtering but with N+1 API pattern — the screener needs to avoid this by pre-loading `get_stock_info()` and filtering in-memory. |
| **Key Risk** | Performance. Screening 1,800+ stocks with multiple criteria requires either (a) pre-computed metric cache or (b) batch API calls. Option (a) is simpler: compute all screening metrics at page load from already-cached FinMind data. |
| **Unique Opportunity** | Position as "discovery for learning" not "screening for investing." Presets like "穩定收息" and "成長潛力" align with "historian" positioning. |

### C44: "What Could Go Wrong" Risk Analysis

| Dimension | Assessment |
|-----------|------------|
| **Technical Feasibility** | 🟡 Medium — Template-based risk descriptions are feasible; data-driven risk detection is harder |
| **Architecture Debt Dependencies** | D1/D2 (duplicate financial metrics) — risk calculations (debt ratio, customer concentration) need consistent financial metrics. R1 (extract financial_metrics.py) should be done first. D6 (hardcoded data) — risk data (customer concentration, industry risks) requires manual curation. |
| **Data Source Availability** | 🟡 Partial — FinMind provides financial ratios (debt ratio, current ratio) but NOT customer concentration, supply chain data, or industry risk data. These require manual curation or a new data source. |
| **Integration Complexity** | 🟢 Low — Add a section to existing `business_card.py`. New service `src/services/risk_analyzer.py` with template-based risk descriptions. Similar pattern to existing `analogy_engine.py`. |
| **Key Risk** | Data availability is the bottleneck. Customer concentration data (e.g., "90% of revenue from 3 customers") is NOT in FinMind. This means either: (a) manual curation for top 20 stocks, or (b) template-only risks based on available FinMind data (debt ratio, revenue volatility, P/E volatility). Option (b) is less compelling but requires zero manual curation. |
| **Unique Opportunity** | "Historian" positioning is perfect — explain historical risks that have materialized, don't predict. "TSMC's customer concentration risk became real in 2018 when Huawei was sanctioned" is factual and educational. |

### C46: Moat Analysis — Competitive Advantage Assessment

| Dimension | Assessment |
|-----------|------------|
| **Technical Feasibility** | 🟢 High (for template-based) — Purely a presentation layer feature with manual curation |
| **Architecture Debt Dependencies** | D6 (hardcoded data) — moat data MUST go in YAML, not Python. Otherwise minimal debt interaction. |
| **Data Source Availability** | 🔴 Manual only — No API provides moat analysis. This is 100% manually curated content. FinMind data can support (e.g.,毛利率 trends to validate technology moat) but the moat narrative itself is human-written. |
| **Integration Complexity** | 🟢 Low — Add a section to `business_card.py`. New service `src/services/moat_analyzer.py` with YAML data file. Very similar to existing `analogy_engine.py` pattern. |
| **Key Risk** | Scalability. Manual curation for 20 stocks is ~8-10h of research/writing. For 1,800 stocks, it's impossible. Must be limited to top 20-30 stocks with a template fallback for others. |
| **Unique Opportunity** | No TW competitor has moat analysis. Morningstar's moat rating is iconic but US-only. This is a perfect "historian" feature — explain what the moat IS and how it has protected the company historically. |

### C47: Financial Education Academy

| Dimension | Assessment |
|-----------|------------|
| **Technical Feasibility** | 🟡 Medium — Structured content delivery is simple; quiz/interactive elements add complexity in Streamlit |
| **Architecture Debt Dependencies** | D5 (no LLM integration) — the Academy would benefit from LLM-generated explanations but works fine with templates. D3 (inline HTML duplication) — lesson content needs reusable UI components. |
| **Data Source Availability** | 🟡 Mixed — Lesson content is manually written. Real TW stock examples use FinMind data (exists). Quiz questions are manually created. |
| **Integration Complexity** | 🟡 Medium — New page (`src/pages/learning_academy.py`) + new service (`src/services/lesson_engine.py`) + YAML lesson files. The most complex of the four remaining features because it's a full new section, not just a card on an existing page. |
| **Key Risk** | Effort (20-30h) is 2-3x the other P2 features. Content creation (writing 10-15 lessons) is the bulk of the effort, not coding. Streamlit's limited interactivity makes quizzes/basic. |
| **Unique Opportunity** | Transforms Stock Explorer from a tool into a platform. "No TW competitor has structured learning paths with TW stock examples" is the strongest competitive gap statement. This is the endgame feature. |

---

## Feature Direction A: "Discovery + Narrative" (C42 + C44 Combined)

**Build the Stock Screener (C42) and Risk Analysis (C44) together as a "Discover & Understand" sprint theme.**

- **C42 Stock Screener**: New page with beginner-friendly presets + custom screening. Uses in-memory filtering of `get_stock_info()` data (no new API calls). Results link to business cards.
- **C44 Risk Analysis**: New section on business card page. Template-based risks using available FinMind data (debt ratio, revenue volatility, P/E volatility). Manual curation for top 20 stocks' customer concentration risks.
- **Combined Effort**: 26-38h (C42: 16-24h + C44: 10-14h)
- **Sprint Allocation**: Sprint 3 (C42) + Sprint 4 (C44)

**Pros:**
- C42 is the P1 gap — transforms product from lookup to discovery, which is the #1 strategic gap
- C44 is the lowest-effort P2 feature that adds unique "historian" value
- Both use existing FinMind data (no new data sources needed for the screener; C44 needs minimal manual curation)
- C42's screener naturally drives traffic to business cards where C44's risk analysis lives — they reinforce each other
- Together they address the two biggest competitive gaps: discovery (財報狗's #1 feature) and risk education (no TW competitor has it)

**Cons:**
- Combined 26-38h is a large sprint commitment
- C42's performance at scale (1,800+ stocks) needs careful design — pre-computed metrics or in-memory filtering
- C44's risk analysis is limited by FinMind data — customer concentration and supply chain data require manual curation
- C42 depends on R3 (batch API) being done first, or it needs to use the in-memory approach

**Effort:** 26-38h (C42: 16-24h + C44: 10-14h)
**Feasibility:** 🟡 Medium — C42 is architecturally new (new page + service); C44 is a straightforward extension

---

## Feature Direction B: "Deep Company Analysis" (C44 + C46 Combined)

**Build Risk Analysis (C44) and Moat Analysis (C46) together as a "Company Quality" sprint theme.**

- **C44 Risk Analysis**: Template-based risks + manual curation for top 20 stocks. Section on business card.
- **C46 Moat Analysis**: Manual curation for top 20 stocks with YAML data file. Section on business card. Template fallback for other stocks.
- **Combined Effort**: 22-30h (C44: 10-14h + C46: 12-16h)
- **Sprint Allocation**: Sprint 3 (C44) + Sprint 4 (C46)

**Pros:**
- Both are business card enhancements — no new pages needed, lower integration risk
- Both align perfectly with "historian" positioning — explain risks and competitive advantages historically
- Moat analysis is a unique differentiator — no TW competitor has it
- Both use the same manual curation workflow (research top 20 stocks → write content → YAML files)
- Lower technical risk than C42 (no new page, no performance concerns)
- Combined effort (22-30h) is more manageable than Direction A

**Cons:**
- Defers C42 (the P1 gap) — Stock Explorer remains a lookup tool, not a discovery tool
- Both features require significant manual curation (research + writing for top 20 stocks)
- Moat analysis doesn't scale beyond top 20-30 stocks
- Less strategic impact than Direction A — enhancing business cards vs. transforming the product

**Effort:** 22-30h (C44: 10-14h + C46: 12-16h)
**Feasibility:** 🟢 High — Both are straightforward extensions to the business card page with existing patterns

---

## Feature Direction C: "Platform Play" (C42 + C47 Phased)

**Build the Stock Screener (C42) now and the Education Academy (C47) as a multi-sprint phased effort.**

- **C42 Stock Screener**: Sprint 3. New page + service. In-memory filtering approach.
- **C47 Education Academy**: Sprint 4-5. Phase 1: 5 beginner lessons + basic page (10h). Phase 2: 10 intermediate lessons + quizzes (10-15h). Phase 3: Advanced lessons + dictionary integration (5-10h).
- **Combined Effort**: 36-54h across 2-3 sprints
- **Sprint Allocation**: Sprint 3 (C42) + Sprint 4-5 (C47 phased)

**Pros:**
- Addresses both P1 gap (C42) and the endgame platform vision (C47)
- C47 phased approach reduces risk — ship 5 lessons first, validate, then expand
- C42 drives user acquisition (discovery → business card); C47 drives retention (education → repeat visits)
- Together they transform Stock Explorer from a tool into a platform
- C47 Phase 1 (5 lessons, 10h) is achievable in a single sprint

**Cons:**
- Highest total effort (36-54h) — requires 2-3 sprints
- C47's content creation (writing lessons) is the bottleneck, not coding
- Streamlit's limited interactivity constrains quiz/learning features
- C47 depends on D3 (UI component standardization) for consistent lesson rendering
- Risk of scope creep — C47 could expand indefinitely

**Effort:** 36-54h across 2-3 sprints (C42: 16-24h + C47: 20-30h phased)
**Feasibility:** 🟡 Medium — C42 is architecturally new; C47 is straightforward but content-heavy

---

## Recommendation

**Recommend Direction A (C42 + C44) for the following reasons:**

### Strategic Rationale

1. **C42 is the P1 gap that must be addressed.** 財報狗's #1 feature is its stock screener. Stock Explorer requires users to know which stock to look up, which is a fundamental barrier for beginners. Without discovery, Stock Encyclopedia remains a reference tool, not an exploration tool. This is the single most important feature to build.

2. **C44 is the right P2 complement to C42.** Users who discover stocks via the screener land on business cards. Adding risk analysis to business cards enhances the "historian" positioning and provides unique value no TW competitor offers. The two features form a natural "discover → understand" flow.

3. **Direction B defers the P1 gap.** While C44+C46 are lower-risk and align well with "historian" positioning, they don't address the fundamental discovery problem. Stock Explorer remains a lookup tool.

4. **Direction C is too ambitious for Sprint 3.** C47's 20-30h effort and content creation burden make it a poor fit for the next sprint. It's better suited for Sprint 4-5 after C42 proves the discovery model.

### Technical Rationale

1. **C42 can reuse existing data.** `get_stock_info()` already loads the full universe. Screening is an in-memory filtering problem, not a data acquisition problem. This is architecturally clean.

2. **C44 has manageable data requirements.** Template-based risks using FinMind data (debt ratio, revenue volatility) require zero manual curation. Customer concentration data for top 20 stocks is ~4-5h of research — acceptable.

3. **Both features follow existing patterns.** C42 follows the `category_browser.py` pattern (filtering stocks) but with better architecture. C44 follows the `analogy_engine.py` pattern (template-based explanations). No new architectural abstractions needed.

4. **Architecture debt alignment.** Both features benefit from R1 (financial metrics extraction) and R3 (batch API) but don't strictly depend on them. C42 can use in-memory filtering; C44 uses data already loaded by the router.

### Suggested Sprint Plan

| Sprint | Features | Effort | Notes |
|--------|----------|--------|-------|
| Sprint 3 | C42 Stock Screener | 16-24h | New page + service. In-memory filtering. |
| Sprint 4 | C44 Risk Analysis | 10-14h | Business card section. Template + manual curation. |
| Sprint 5 | C46 Moat Analysis | 12-16h | Business card section. Manual curation for top 20. |
| Sprint 6 | C47 Academy Phase 1 | 10h | 5 beginner lessons. Validate before expanding. |

### Pre-conditions

Before starting C42:
- **R3 (batch API calls)** should be implemented or C42 must use in-memory filtering from `get_stock_info()` cache
- **R6 (standardize __init__.py)** — quick win (0.5h) that makes adding new services cleaner

Before starting C44:
- **R1 (extract financial_metrics.py)** — risk calculations need consistent financial metrics
- Manual research for top 20 stocks' customer concentration data (can be done in parallel with C42 development)

---

*Created: 2026-06-15*
*Maintainer: System Architect*
*Next review: After Sprint 3 planning decision*
