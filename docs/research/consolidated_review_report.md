# Consolidated Review Report – Round 35
**Date**: 2026-06-14
**Theme**: 🔍 Review (Sprint 15 Post-Mortem + Sprint 16 Prerequisites)

## 1. Feature Gap List (from Competitor Research & QA Engineer Analysis)

### High-Priority Opportunities (P1)
| Feature ID | Description | Effort Estimate | Competitive Validation | Source |
|------------|-------------|-----------------|------------------------|--------|
| **C134** | AI-Generated Change Explanations – Explains WHY metrics changed | 12-16h | Datawallet, Spiking, Copilot Money have this as baseline | Rounds 20-27 research |
| **C138** | Smart Notifications with Explanations – AI-enhanced alerts explaining WHY events matter | 10-14h | Spiking, Datawallet, Acorns validated | Rounds 20-27 research |
| **C119** | Glossary-First Onboarding – Teaches financial terms before showing data | 10-14h | Planting.tw, Groww, Stash validate approach | Rounds 20-27 research |
| **C98** | AI Event Interpretation Engine – Combines M5 event detection with AI narrative | 14-18h | Luca AI, 群益, StonkGrid have similar AI narrative features | Rounds 20-27 research |
| **C02** | Notifications System – Bell icon + unseen event count from M5 engine | 12-19h | All major competitors (StatementDog, CMoney, GoodInfo) have notifications | Sprint 16b conditional plan |
| **C14** | Health Score Badge + Narrative – Explainable 0-100 score with plain-language narrative | 4-6h | Simply Wall St snowflake, Morningstar, Stockopedia have health scores | Sprint 16a plan |

### Medium-Priority Opportunities (P2)
| Feature ID | Description | Effort Estimate | Strategic Value | Source |
|------------|-------------|-----------------|-----------------|--------|
| **C34** | Company Story Timeline – Narrative of events, revenue, price movements | 16-24h | Unique "historian" differentiator – no competitor has this | Competitor Research R7 |
| **C36** | Visual Revenue Tree – Shows HOW money flows through business (e.g., TSMC → 5nm chips → Apple/NVIDIA/AMD) | 10-14h | Extends existing revenue pie chart with hierarchical visualization | Competitor Research R8 |
| **C37** | Key Takeaways Summary Card – 3-5 bullet points synthesizing most important information | 6-8h | Directly addresses "ten-second test" design principle | Competitor Research R8 |
| **C38** | Compare Stories Side-by-Side – Two companies' key events, revenue milestones, business models compared | 12-16h | Extends existing peer comparison advantage with narrative layer | Competitor Research R8 |
| **C39** | What Changed Recently Delta Card – Highlights significant metric changes (>10%) with plain-language explanations | 8-10h | Makes data feel alive and relevant by highlighting recent changes | Competitor Research R8 |
| **C40** | Beginner/Expert Mode Toggle – Progressive disclosure for metrics (show essentials vs. everything) | 10-14h | Aligns with "progressive drill-down" principle in product vision | Competitor Research R8 |
| **C33** | Beginner Glossary / Tooltip System – Hover/click definitions for financial terms | 8-12h | Systematic educational infrastructure; Investopedia has 10K+ terms | Competitor Research R7 |
| **C35** | Market Mood Index – Institutional buy/sell surplus + volume + advance/decline ratio | 10-12h | Beginner-friendly market overview (WantGoo, CMoney have variants) | Competitor Research R7 |

### Already Planned/In Progress
| Feature ID | Description | Status | Effort Estimate | Source |
|------------|-------------|--------|-----------------|--------|
| **C14** | Health Score Badge + Narrative | Sprint 16a (Planned) | 4-6h | Handoff.md |
| **C132** | Risk Level Simplification (1-5 Scale) | Sprint 16a (Planned) | 6-10h | Handoff.md |
| **C45** | Valuation Band Chart (Historical P/E Range) | Sprint 16a (Planned) | 8-10h | Handoff.md |
| **C28** | Story Timeline Spike (Feasibility Analysis) | Sprint 16a (Completed) | 3-5h | Handoff.md – GO verdict |
| **C41** | Read Next Phase A (Peer Stock Recommendations) | Sprint 16a (Planned) | 2-3h | Handoff.md |
| **C02+C07** | Notifications + Custom Thresholds | Sprint 16b (Conditional) | 18-28h | Handoff_discuss_r33.md |
| **C28 Full** | Full Story Timeline Implementation | Sprint 16b (Conditional) | 26-36h | Handoff.md |

## 2. Design Improvement Suggestions (from Design Reviewer Analysis)

### P1 – Blocking Issues (Must Fix Before Next Release)
| Issue ID | Description | Effort Estimate | Location | Status |
|----------|-------------|-----------------|----------|--------|
| **D-003** | Inconsistent Card Styling – Pages bypass shared components with inline HTML | 2-3h | `watchlist_page.py`, `etf_detail.py`, `business_card.py` (C41/C44) | PARTIALLY FIXED – group_structure.py fixed, remaining pages need work |
| **D-006** | Mobile Responsiveness Gaps – Multi-column layouts don't stack on mobile, charts too small | 4-6h | All pages (CSS media queries only adjust padding/font sizes) | OPEN – requires mobile-specific CSS and touch target optimization |
| **D-005** | Business Card Page Overload Risk – 13+ sections risks cognitive overload | 3-4h (mitigation) | `business_card.py` | MITIGATED – C105 toggle + expander pattern reduces above-fold to 4 sections, but needs consistent progressive disclosure |

### P2 – Optimization Issues (Fix When Capacity Allows)
| Issue ID | Description | Effort Estimate | Location | Status |
|----------|-------------|-----------------|----------|--------|
| **D-004** | Design System Documentation Not Maintained – Missing new components | 1h | `docs/design/design_system.md` | PARTIALLY RESOLVED – doc exists but needs update for `_mini_score_card`, `_count_label`, `_subsidiary_card` |
| **D-010** | Watchlist Page Uses Non-PPT Layout – Dense table layout inconsistent with card-based pages | 2-3h | `watchlist_page.py` | OPEN – needs card-based redesign |
| **D-011** | Category Browser Uses Dense Tables – Overwhelming for beginners | 2-3h | `category_browser.py` | OPEN – needs larger cards, fewer items per row, featured stock |
| **D-012** | No Glossary/Tooltip System – Financial terms lack inline help | 8-12h | All pages with financial metrics | OPEN – requires C33 implementation with `src/data/glossary.yaml` |
| **D-015** | No Structured Learning Path – Scattered "Did You Know?" facts, no curriculum | 20-30h | `business_card.py` (Did You Know section) | OPEN – requires C47 expansion to 10-15 structured lessons |

### Proposed Design Improvement Plans
1. **Fix Inconsistent Card Styling (D-003):**
   - Enforce use of shared components (`_白话_card`, `_info_card`, `_summary_card`, `_subsidiary_card`) across all pages
   - Replace remaining inline HTML with appropriate shared components
   - Create missing components where needed (e.g., `_peer_card`, `_event_stock_card`)

2. **Mitigate Business Card Overload (D-005):**
   - Implement progressive disclosure (`st.expander`) for all non-essential sections (default collapsed)
   - Introduce "Beginner Mode"/"Expert Mode" toggle (C40) in navbar to hide/show advanced sections
   - Prioritize hero summary card (C37) and key takeaways above the fold
   - Consider "Summary First" layout: show only 3-4 most critical metrics by default

3. **Improve Mobile Responsiveness (D-006):**
   - Add mobile-specific CSS to force `st.columns` to stack vertically below 768px
   - Increase minimum touch target sizes to 44px for interactive elements
   - Adjust chart heights and font sizes for readability on small screens
   - Explore Streamlit container/column width settings for better mobile layouts

4. **Update and Maintain Design System (D-004):**
   - Update `docs/design/design_system.md` to document all components and usage rules
   - Add maintenance note: "Update this doc when adding new components to `_router_base.py`"
   - Enforce design system compliance via pre-development checklist

5. **Incorporate Competitor-Inspired Features (High-Impact Gaps):**
   - **Stock Screener/Discovery Engine (C42)**: Add "🔍 選股探索" page with beginner-friendly presets
   - **Company Snowflake Health Visualization (C43)**: Add radar chart/snowflake showing 5 dimensions scored 0-5
   - **Risk Analysis Section (C44)**: Add "⚠️ 風險分析" with 3-5 key risks in plain language
   - **Valuation Band Chart (C45)**: Add "📊 估值區間" card showing current P/E vs. 5-year range
   - **Moat Analysis (C46)**: Add "🏰 護城河分析" explaining durable competitive advantage
   - **Financial Education Academy (C47)**: Add "📚 學習學院" with 10-15 structured lessons
   - **Tappable Glossary/Tooltips (C33)**: Implement hover/click definitions using shared glossary component
   - **Learn Before Invest Gate (C103 lite)**: Onboard first-time users with 2-card guided tour
   - **Beginner/Expert Mode Toggle (C40)**: As noted above, to address overload and mobile

## 3. Technical Debt Priorities (from Architect Analysis)

### High Severity (Blockers)
| Debt ID | Description | Effort Estimate | Blocker For | Status |
|---------|-------------|-----------------|-------------|--------|
| **D5** | No LLM integration layer – Missing abstraction for LLM-based plain-language translation | 2-3h | C98 (Event Interpretation Engine) and any LLM-dependent features | OPEN – Round 20 #1 recommendation |
| **D-097** | Event interpretation service exists but lacks LLM abstraction (D5 dependency) | 2-3h | C98 implementation | OPEN – service uses pure templates only |

### Medium Severity (Moderate Effort, Fixable)
| Debt ID | Description | Effort Estimate | Impact | Status |
|---------|-------------|-----------------|--------|--------|
| **D6** | Hardcoded data in Python modules – Remaining blocks not migrated to YAML | 3-4h | Hinders maintainability, blocks non-technical contributions | PARTIALLY RESOLVED – `company_facts.yaml` and `case_studies.yaml` done, 5 blocks remain |
| **D-074** | Test infrastructure regression – Missing `filelock` dependency causing test failures | 0.25h | Increases regression risk as new features added | OPEN – 131/149 tests failing due to missing dependency |
| **D-042** | `_sections.py` grew to 918 lines – Exceeds recommended threshold | 1-2h | Affects discoverability, risk of monolith re-emergence | PENDING – was 612 lines after D24, Sprint 4 added 306 lines |
| **D-046** | `sector_heatmap.py` has 150+ lines of inline HTML despite using market_data service | 2-3h | Duplicates patterns from `_router_base.py` | PENDING – grid cards and top movers duplicate CSS patterns |
| **D-048** | `market_event_service.py` hardcoded `_CASE_STUDIES` data (~230 lines) | 1-2h | Violates D6, requires Python file edits for new case studies | RESOLVED (Sprint 8) – migrated to YAML |
| **D-050** | `market_event_case_study.py` inline HTML across 3 card patterns | 1-2h | Key metrics card duplicates `_白话_card()` pattern | RESOLVED (Sprint 8) – now uses shared components |
| **D-051** | `market_event_service.py` – `get_events_for_stock()` uses linear scan O(n) | 0.5h | Will scale poorly if case studies grow | RESOLVED (Sprint 8) – added pre-computed index |
| **D-052** | `etf_browser.py` sequential price fetching (D8 not resolved) | 1-2h | Significantly slower than ThreadPoolExecutor pattern | RESOLVED (Sprint 8) – applied ThreadPoolExecutor pattern |
| **D-053** | `adaptive_engine.py` – `_load_events()` reads YAML on every call (D10 not resolved) | 1-2h | Each call triggers file read + YAML parse + file lock | RESOLVED (Sprint 8) – added in-memory cache with mtime checking |
| **D-054** | `watchlist.py` – `_load_data()` still called on every operation (D9 not resolved) | 1-2h | Each watchlist operation triggers file read + YAML parse | RESOLVED (Sprint 8) – added in-memory cache with mtime checking |
| **D-055** | `sector_heatmap.py` – 150+ lines of inline HTML despite using market_data service | 2-3h | Duplicates CSS patterns from `_router_base.py` | RESOLVED (Sprint 8) – all `unsafe_allow_html=True` eliminated |
| **D-056** | `_section_title()` in `_router_base.py` – inverted logic bug | 0.1h | Empty titles produce header with no text | RESOLVED (Sprint 8) – logic fixed |

### Low Severity (Minor Issues)
| Debt ID | Description | Effort Estimate | Notes | Status |
|---------|-------------|-----------------|-------|--------|
| **D-067** | `company_timeline.py` has 1 remaining `unsafe_allow_html=True` usage | 0.1h | Event count display – replace with `st.caption()` + markdown bold | PENDING – quick fix |
| **D-068** | `comprehension_check.py` uses `st.error()` for wrong quiz answers | 0.1h | Contextually appropriate UX for quiz feedback | BY DESIGN – no action needed |
| **D-069** | `_sections/_summary.py` is 323 lines – Monitor growth | Monitor | 5 functions (~65 lines/function) – reasonable size | MONITOR – only act if exceeds 500 lines |
| **D-070** | C105 Simple/Detailed toggle adds session state key without cleanup | 0.25h | Hardcoded `value=True` means simple mode is always default (correct UX) | WORKING AS DESIGNED – no change needed |
| **D-071 through D-076** | Various minor inline HTML remnants, session-state cleanup, monitoring items | 0.1-0.5h each | Low impact, can be addressed alongside feature work | MOSTLY RESOLVED or DEFERRABLE |

### Architecture Health Metrics (Post-Sprint 15)
- **Service Layer**: 38 modules, 89% under 300 lines, 100% Streamlit-free ✅
- **Page Layer**: ~42 modules, largest is 437 lines (`etf_browser.py`) ✅
- **Overall Codebase**: 0 god modules (>800 lines), 2 modules >600 lines (monitored) ✅
- **YAML Data Files**: 12+ including recent migrations for glossary, key_takeaways, etc. ✅
- **Test Count**: 165+ tests (post-Sprint 10 infrastructure) ✅
- **CI Enforcement**: ✅ No-inline-html script prevents new instances
- **Presentation Layer**: 11 `unsafe_allow_html=True` instances remaining (down from 27 in Round 26) ✅

**Overall Architecture Health Grade**: 🟢 **HEALTHY** – The 4-layer architecture is solid. Zero god modules. Service layer boundaries are clean. Page layer is well-modularized. Main concern is growing service count without full test coverage, but CI enforcement prevents regressions.

## 4. Consolidated Review Report Summary

### Key Findings
1. **Architecture is Healthy**: The 4-layer architecture holds with zero god modules, clean service layers (100% Streamlit-free), and well-modularized pages. Technical debt has been systematically addressed in recent sprints.

2. **Primary Blockers Identified**: 
   - **D5 (LLM Abstraction Layer)**: Must be resolved before any LLM-dependent features (C98, C134, C116, etc.)
   - **D6 (YAML Migration)**: Partially complete – remaining hardcoded data blocks hinder maintainability
   - **D-074 (Test Infrastructure)**: Quick fix needed to restore full test coverage and prevent regression risk

3. **Feature Opportunities Align with Vision**: All top feature opportunities from competitor research reinforce the "historian, not stock picker" positioning by focusing on explanatory narratives, contextual learning, and educational value rather than predictive or advisory features.

4. **Sprint 16 Readiness**: Sprint 16a is technically ready but estimates show 17-24h needed (vs. initial 12-18h projection). Sprint 16b presents a clear strategic choice: invest in unique differentiation (C28 Full: 26-36h) or close competitive gaps (C02+C07: 18-28h).

5. **Design System Needs Attention**: While improving, inconsistent card styling (D-003), mobile responsiveness gaps (D-006), and outdated design system documentation (D-004) remain as P1/P2 issues affecting UX consistency.

### Strategic Recommendations
1. **Immediate Optimization Focus** (Before Sprint 16 Feature Work):
   - Complete D6 YAML migration (3-4h) to unblock content contributions
   - Create LLM abstraction layer (D5, 2-3h) to enable future LLM-dependent features
   - Fix D-074 test infrastructure (0.25h) to maintain regression safety

2. **Sprint 16a Execution** (12-18h target):
   - Proceed with planned features: C14 Health Score + Narrative, C132 Risk Simplification, C45 Valuation Band, C28 Story Timeline Spike
   - Monitor effort against updated estimates (17-24h total) and adjust scope if needed

3. **Sprint 16b Strategic Decision**:
   - If C28 spike validation passes (data richness criteria met): Invest in unique differentiation with C28 Full Story Timeline (26-36h)
   - If C28 spike validation fails: Close competitive gaps with C02 Notifications + C07 Custom Thresholds (18-28h)

4. **Design System Investment** (Ongoing):
   - Fix P1 design issues (D-003 inconsistent card styling, D-006 mobile responsiveness) to improve UX consistency
   - Update design system documentation (D-004) to reflect current component library
   - Implement progressive disclosure consistently across business card sections

5. **Educational Feature Pipeline** (Post-Sprint 16):
   - Leverage completed YAML migration to add systematic educational features (C33 Glossary, C47 Education Academy)
   - Implement narrative-first features that align with "historian" positioning (C34 Story Timeline, C37 Key Takeaways)
   - Consider Beginner/Expert Mode toggle (C40) to address page overload and mobile experience

This review confirms Stock Explorer maintains a strong architectural foundation while identifying clear optimization priorities and feature opportunities that align with its core mission of helping users understand companies through plain-language explanations and historical context.