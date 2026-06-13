## 2026-06-13 Technical Analysis — Review Round 22

### Sprint 9 Architecture Assessment

Sprint 9 delivered 4 items: D-057 (prerequisite), C103 Lite, C101, and C98. All items are committed and L0/L1 verified (L0: 89/89, L1: 8/18 with 10 pre-existing event-alert failures unchanged).

#### D-057 (_section_title() Consolidation) — ✅ Verified
- **Commit**: `24ef84e`
- **What was claimed**: Remove duplicate `_section_title()` from `business_card/_helpers.py`, update 21 call sites to use `_router_base._section_title()`.
- **Code evidence**: `_helpers.py` (172 lines) no longer defines `_section_title()`. The function exists only in `_router_base.py`. All section files import from `_router_base`.
- **Verdict**: ✅ **Genuinely resolved**. Clean consolidation, no remaining duplicates.

#### C103 Lite (First Visit Guide) — ✅ Clean
- **File**: `src/pages/first_visit_guide.py` (48 lines)
- **Architecture assessment**:
  - ✅ Uses `_summary_card()` and `_白话_card()` from `_router_base` — zero inline HTML
  - ✅ Session-state pattern (`first_visit_dismissed` boolean) is appropriate for Lite scope
  - ⚠️ **Minor**: Unused import `from src.data.finmind_client import FinMindClient` (line 9). The `client` parameter is accepted but never used in the function body. This is a dead import, not an architecture violation.
  - ⚠️ **Minor**: `st.markdown("## 👋 歡迎使用股識")` uses raw markdown instead of `_section_title()`. Acceptable for a standalone page header.
- **Verdict**: ✅ **No architecture violations**. Clean, minimal page module.

#### C101 (Comprehension Check Quiz) — ⚠️ One Issue
- **Files**: `src/services/comprehension_quiz_service.py` (145 lines), `src/pages/comprehension_check.py` (191 lines), `config/comprehension_quiz.yaml`
- **Architecture assessment**:
  - ✅ Service module has **zero Streamlit imports** — clean service layer boundary
  - ✅ Quiz data in YAML (`config/comprehension_quiz.yaml`) — follows D6 pattern
  - ✅ Page uses `_info_card()`, `_section_title()`, `_白话_card()` from `_router_base`
  - ✅ Service API is clean: `get_questions()`, `check_answer()`, `calculate_score()`
  - ⚠️ **D-058 NOT addressed**: C101's `comprehension_quiz_service.py` duplicates the YAML-load-cache-and-score pattern from `financial_wellness_service.py` (C85). Both modules have nearly identical `_load_quiz_config()` / `_get_questions_raw()` / `calculate_score()` structures. The Round 21 recommendation to extract a shared `quiz_engine.py` (D-058, 1-2h) was not done. This is **new architecture debt** (see D-062 below).
  - ⚠️ **Inline HTML**: `comprehension_check.py` lines 151-166 use `unsafe_allow_html=True` for result cards (red/green bordered divs). This is 16 lines of inline HTML that could use a shared component.
- **Verdict**: ⚠️ **Mostly clean**. D-058 duplication is the primary concern.

#### C98 (Event Interpretation Engine) — ✅ Clean
- **Files**: `src/services/event_interpretation_service.py` (123 lines), `config/event_interpretation_templates.yaml`, modified `event_dashboard.py`
- **Architecture assessment**:
  - ✅ Service module has **zero Streamlit imports** — clean service layer boundary
  - ✅ Templates in YAML (`config/event_interpretation_templates.yaml`, 34 lines) — follows D6 pattern
  - ✅ Module-level in-memory cache (`_TEMPLATES` global) — same pattern as other services
  - ✅ `event_dashboard.py` uses `_summary_card()` and `_info_card()` from `_router_base` for interpretation display
  - ✅ `get_interpretation()` and `get_drilldown_interpretation()` are pure functions with graceful fallback
  - ✅ No LLM abstraction needed — Sprint 9 is explicitly template-only (LLM deferred)
  - ⚠️ **Minor**: `event_dashboard.py` lines 110-115 and 132-137 use `unsafe_allow_html=True` for key concept and disclaimer divs (3 lines each). These are minimal and don't duplicate card patterns.
- **Verdict**: ✅ **Clean**. Well-designed service module. Template-only approach is appropriate for Sprint 9.

#### D-057 (LLM Abstraction) — ⚠️ Misunderstood
- **What was claimed**: D-057 was listed as a Sprint 9 prerequisite.
- **What actually happened**: The Sprint 9 plan conflated two different D-057 items. The original D-057 (Round 21) was about `_section_title()` consolidation, which was completed. The HIGH-severity D-057 from Round 21 (LLM abstraction layer, formerly D5) was **not** addressed — and did not need to be, since C98 is explicitly template-only.
- **Verdict**: ✅ **Acceptable**. The LLM abstraction (D5) remains open but is not a blocker for C98's template-only approach. C98's docstring says "Sprint 9: Template-only approach. LLM integration deferred." — this is the correct sequencing.

---

### Sprint 10 Feasibility Analysis

Sprint 10 plan: C34 (Company Story Timeline) + C105 (Simple/Detailed Toggle) + M5 remediation + D-061 (test infrastructure).

#### C34: Company Story Timeline

**Problem**: Streamlit has no native timeline component. The `timeline_controls.py` module (74 lines) provides a time-range *selector* (1Y/3Y/5Y/ALL buttons) but not a visual timeline of company events.

**Three approaches evaluated**:

**Option A: Vertical st.expander Chain**
- Use `st.expander` for each event, ordered chronologically, with emoji/date headers
- Pros: Pure Streamlit, zero new dependencies, works today
- Cons: Not visually a "timeline" — looks like a FAQ list. No connecting lines or visual flow.
- Effort: 8-12h
- Verdict: ⚠️ Feasible but underwhelming UX

**Option B: Custom HTML/CSS Timeline**
- Build a vertical timeline using HTML/CSS injected via `st.markdown(unsafe_allow_html=True)`
- Pros: Visually compelling, matches PPT-style design, no external dependencies
- Cons: 50-80 lines of inline HTML in page code (violates D3 pattern). Requires careful responsive CSS.
- Effort: 12-16h
- Verdict: ✅ Recommended — create a reusable `_timeline_card()` helper in `_router_base.py` to avoid inline HTML proliferation

**Option C: streamlit-timeline (Third-party)**
- Install `streamlit-timeline` or similar component
- Pros: Purpose-built timeline component
- Cons: External dependency, may have compatibility issues, limited customization
- Effort: 16-24h (including integration risk)
- Verdict: 🔴 Not recommended — adds dependency risk for a single-use component

**Recommendation**: **Option B** with a reusable helper. Create `_timeline_event(date, title, description, icon, color)` in `_router_base.py` that renders a single timeline node. The page assembles a list of events and calls the helper in a loop. This keeps the HTML encapsulated and reusable. The `event_interpretation_service.py` already provides `get_drilldown_interpretation()` which can supply the timeline content.

**Data source**: Events come from `adaptive_engine.get_events_for_stock()` (already filtered by date) + `market_event_service.get_case_studies_for_stock()`. The timeline should merge both sources and sort chronologically.

**Estimated effort**: 14-18h (including helper creation, data merging, and page integration).

#### C105: Simple/Detailed Toggle

**Problem**: Add a session-state toggle that switches between "simple" (beginner) and "detailed" (advanced) views on content-heavy pages.

**Architecture assessment**:
- ✅ **Low risk** — This is a session-state pattern, not a new component architecture
- ✅ The toggle itself is a single `st.session_state["view_mode"]` key (`"simple"` or `""detailed"`)
- ✅ Each section checks the toggle and renders abbreviated or full content
- ⚠️ **Scope concern**: Which pages get the toggle? Business card page is the obvious first target (15+ sections). But applying it to *every* page multiplies implementation effort.
- ⚠️ **State proliferation**: This adds at least 1 new session_state key. Combined with existing keys (`first_visit_dismissed`, `comprehension_quiz_done`, `comprehension_show_form`, `comprehension_answers`, `comprehension_quiz_done`, `timeline_range`, notification keys, etc.), session_state is growing. D28 (session state tracking) remains unaddressed.

**Recommendation**: 
1. Start with business card page only (highest impact)
2. Use a single `st.session_state["content_depth"]` key with values `"simple"` / `"detailed"`
3. Place the toggle in the navbar or as a floating button — not inline with content
4. Each section function accepts an optional `depth` parameter (default: `None` = auto-detect from session_state)
5. Defer D28 (session state manager) — the ad-hoc pattern still works for this scope

**Estimated effort**: 10-14h for business card page only.

#### M5 Remediation: Fix 10 L1 Event-Alert Failures

**Current state**: L1 tests show 8/18 passing, with 10 pre-existing event-alert failures unchanged since Sprint 7. These are described as "pre-existing" but the exact root cause has not been architecturally analyzed.

**Root cause analysis**:

The 10 L1 event-alert failures are in the M5 (adaptive engine) alert delivery path. Tracing the code:

1. **Alert trigger path**: `router.py:load_and_render_page()` → `run_auto_detection(stock_id, data)` (line 148) → detects events → writes to `events.yaml`
2. **Alert display path**: `_render_event_alerts(stock_id)` (line 154) → `get_events_for_stock(stock_id, days=30)` → renders `st.error()` / `st.warning()` banners
3. **Notification path**: `notification_service.get_pending_notifications()` → `run_auto_detection()` for each subscribed stock → reads `events.yaml` → filters by acknowledged IDs

**Identified root causes for the 10 failures**:

**Cause 1: Alert suppression by try/except** (router.py:159)
- The entire M5 block (detection + banner + alerts + freshness) is wrapped in a `try/except Exception` that silently logs a warning. If `run_auto_detection()` raises for a specific stock, **no alerts are shown at all** for that stock. The user sees zero indication that detection failed.
- **Impact**: High. Any data error (missing columns, API timeout, malformed DataFrame) silently kills the alert path.

**Cause 2: `_render_event_alerts()` only shows alerts on stock pages** (router.py:154)
- Event alerts are only rendered when `load_and_render_page()` is called with a stock_id. The standalone event dashboard page (`_render_event_dashboard`) does NOT call `_render_event_alerts()` — it has its own expander-based display.
- **Impact**: Medium. Users who navigate to the event dashboard don't see the alert banners.

**Cause 3: Alert display uses `st.error()` / `st.warning()` which may not trigger L1 test detection**
- The L1 tests likely check for specific UI elements or text patterns. `st.error()` and `st.warning()` produce Streamlit alert boxes that may not be captured by the test framework if the test expects different selectors.
- **Impact**: Medium. This is a test-infrastructure issue as much as a code issue.

**Cause 4: No events in test data**
- The `events.yaml` file may not contain events for the stocks used in L1 testing. `run_auto_detection()` only records events when thresholds are met (revenue YoY ±30%, price change ±7%, news keywords). Test stocks may not trigger these thresholds.
- **Impact**: High. If test data doesn't trigger detection, `_render_event_alerts()` returns early (line 210-211) and no alerts are rendered.

**Recommended remediation approach** (8-12h):
1. **Separate detection from display** — Don't wrap the entire M5 block in one try/except. Wrap detection separately from display.
2. **Add test-mode event injection** — Create a function to inject test events into `events.yaml` for L1 test stocks. This ensures alerts are always available during testing.
3. **Fix alert rendering** — Ensure `_render_event_alerts()` produces testable output (use `st.markdown` with data-testid or specific CSS classes instead of bare `st.error()`/`st.warning()`).
4. **Add detection status indicator** — Show a subtle "事件偵測完成" or "事件偵測失敗" message so users know the system is working.

#### D-061: Test Infrastructure

**Current state**: `tests/test_business_logic.py` (807 lines) already exists with 50+ test cases covering `calc_roe_ttm`, `_is_etf`, `filter_by_timeline`, `validate_stock_id`, `detect_revenue_event`, `detect_price_abnormal`, `detect_news_event`, `check_data_freshness`, `detect_company_type`, and `extract_dividend_summary`. Tests use pytest.

**Assessment**: Test infrastructure **already exists** and is substantial. D-061 is partially resolved.

**What's missing**:
- No `conftest.py` with shared fixtures
- No `pytest.ini` or `pyproject.toml` pytest configuration
- No tests for: `event_interpretation_service`, `comprehension_quiz_service`, `notification_service`, `financial_wellness_service`, `market_event_service`, `adaptive_engine.run_auto_detection`, page render functions
- No integration tests (Streamlit page rendering tests)
- No CI configuration

**Recommendation** (3-4h):
1. Add `conftest.py` with shared fixtures (mock FinMindClient, sample DataFrames)
2. Add `pyproject.toml` pytest config section
3. Add tests for new Sprint 9 services (`event_interpretation_service`, `comprehension_quiz_service`)
4. Add L1 event-alert integration tests (the M5 remediation depends on this)

---

### New Architecture Debt (from Sprint 9)

#### D-062: `comprehension_quiz_service.py` duplicates `financial_wellness_service.py` quiz pattern
- **Severity**: 🟡 Medium
- **Effort**: 1-2h (extract shared `quiz_engine.py`)
- **Description**: `comprehension_quiz_service.py` (C101) and `financial_wellness_service.py` (C85) share nearly identical patterns:
  - Module-level YAML path + in-memory cache
  - `_load_quiz_config()` / `_get_questions_raw()` functions
  - `get_questions()` with options tuple conversion
  - `calculate_score()` with question_map lookup
- **Difference**: C85 uses score-based options (a/b/c/d → 1-4 points), C101 uses correct-key options (a/b/c/d → correct/incorrect with explanation). The scoring logic differs but the YAML loading and question running are identical.
- **Recommended Action**: Extract `src/services/quiz_engine.py` with generic `load_question_bank(yaml_path)` and `run_quiz(questions, answers)` functions. Both C85 and C101 consume this. Do alongside C105 or as Sprint 10 first task.

#### D-063: `first_visit_guide.py` has unused `FinMindClient` import
- **Severity**: 🟢 Low (code smell, not architecture violation)
- **Effort**: <0.1h (remove import)
- **Description**: `first_visit_guide.py` line 9 imports `FinMindClient` but never uses it. The function accepts `client: FinMindClient` as parameter but doesn't reference it in the body.
- **Recommended Action**: Remove the unused import. The `client` parameter can also be removed from the function signature (but this requires updating the router call site).

#### D-064: `comprehension_check.py` inline HTML for result cards (16 lines)
- **Severity**: 🟢 Low
- **Effort**: 0.5h (extract to reusable component)
- **Description**: `comprehension_check.py` lines 151-166 use `unsafe_allow_html=True` for per-question result cards with colored borders. This duplicates the card pattern from `_router_base.py`.
- **Recommended Action**: Create `_quiz_result_card(question_text, is_correct, explanation)` in `_router_base.py` or a new `ui_components.py`. Do alongside D-062.

#### D-065: Session state key proliferation (D28 escalation)
- **Severity**: 🟡 Medium (escalating)
- **Effort**: 2-3h (session state manager)
- **Description**: Sprint 9 added 5+ new session_state keys: `first_visit_dismissed`, `comprehension_quiz_done`, `comprehension_show_form`, `comprehension_answers`, plus per-question keys `comprehension_q_{id}`. Combined with existing keys from other features, `st.session_state` now has 15+ keys with no namespacing or documentation.
- **Recommended Action**: Defer to Sprint 11. For Sprint 10, add a session_state key registry comment block in `main.py` documenting all keys. C105 will add at least 1 more key (`content_depth`).

---

### Architecture Health Metrics

#### Service Layer (`src/services/`)
| Metric | Round 21 | Round 22 | Change |
|--------|----------|----------|--------|
| **Total service modules** | 22 | 24 | +2 (`event_interpretation_service`, `comprehension_quiz_service`) |
| **Largest service** | `chart.py` — 787 lines | `chart.py` — 787 lines | No change |
| **2nd largest** | `adaptive_engine.py` — 622 lines | `adaptive_engine.py` — 622 lines | No change |
| **3rd largest** | `risk_analyzer.py` — 567 lines | `risk_analyzer.py` — 567 lines | No change |
| **Services under 300 lines** | 19 of 22 (86%) | 21 of 24 (87.5%) | ✅ Both new services are small |
| **Services with zero Streamlit imports** | 18 of 22 (82%) | 20 of 24 (83%) | ✅ Both new services are clean |
| **New services this sprint** | 0 | 2 | `event_interpretation_service` (123 lines), `comprehension_quiz_service` (145 lines) |

#### Page Layer (`src/pages/`)
| Metric | Round 21 | Round 22 | Change |
|--------|----------|----------|--------|
| **Total page modules** | 33 | 35 | +2 (`first_visit_guide`, `comprehension_check`) |
| **Largest page** | `etf_browser.py` — 437 lines | `etf_browser.py` — 437 lines | No change |
| **business_card/ sub-modules** | 10 files | 13 files | +3 (`_sections/_summary`, `_sections/_financial`, `_sections/_health`, `_sections/_story`, `_sections/_detail` — wait, these were already created in Sprint 5. The count increase is from `_sections/__init__.py` being new) |
| **Pages using `_router_base` components** | 8+ | 10+ | +2 (first_visit_guide, comprehension_check) |

#### Overall Codebase
| Metric | Round 21 | Round 22 | Change |
|--------|----------|----------|--------|
| **Total Python source files** | ~95 | ~99 | +4 |
| **Largest file overall** | `chart.py` — 787 lines | `chart.py` — 787 lines | No change |
| **God modules (>800 lines)** | 0 ✅ | 0 ✅ | No change |
| **Modules >600 lines** | 2 | 2 | No change |
| **YAML data files** | 5 | 7 | +2 (`event_interpretation_templates.yaml`, `comprehension_quiz.yaml`) |
| **Test files** | 1 (`test_business_logic.py`) | 1 | No change |
| **Test coverage** | ~50 test cases | ~50 test cases | No change (new services untested) |

#### 4-Layer Architecture Assessment
| Layer | Round 21 | Round 22 | Notes |
|-------|----------|----------|-------|
| **Data** (`src/data/`) | ✅ Clean | ✅ Clean | No changes |
| **Service** (`src/services/`) | ✅ Clean | ✅ Clean | 2 new services, both clean boundaries |
| **Page** (`src/pages/`) | ✅ Clean | ✅ Clean | 2 new pages, both use shared components |
| **Presentation** (inline) | ⚠️ Improving | ⚠️ Improving | `comprehension_check.py` added 16 lines of inline HTML. Net effect: roughly unchanged. |

**Architecture Health Grade**: 🟢 **HEALTHY** — The 4-layer architecture continues to hold. No god modules. Service layer boundaries remain clean (83% zero Streamlit imports). Both new Sprint 9 services follow established patterns. The main concern is D-062 (quiz service duplication) and the growing session state count.

---

### Top 3 Recommendations for Sprint 10

#### 1. 🟡 Extract Shared Quiz Engine (D-062) — First Task of Sprint 10
- **Effort**: 1-2h
- **Why**: C101 and C85 have nearly identical quiz infrastructure. Before C105 adds more quiz-like features, extract a shared `quiz_engine.py` to prevent further duplication.
- **What**: Create `src/services/quiz_engine.py` with generic `load_question_bank(yaml_path)` and `run_quiz(questions, answers)` functions. Refactor both `comprehension_quiz_service.py` and `financial_wellness_service.py` to use the shared engine.
- **When**: **First task of Sprint 10**, before C34 or C105 coding begins.
- **Risk if deferred**: Duplication will grow if C105 or future features add more quiz-like patterns.

#### 2. 🟡 Create Reusable Timeline Component for C34 (Option B)
- **Effort**: 14-18h (including helper creation)
- **Why**: C34 is the highest-effort Sprint 10 feature. Building a reusable `_timeline_event()` helper in `_router_base.py` prevents 50-80 lines of inline HTML in the page file and creates a component that can be used on other pages (e.g., company history, event dashboard).
- **What**: 
  - Create `_timeline_event(date, title, description, icon, color)` in `_router_base.py`
  - Build `company_story_timeline.py` page that merges events from `adaptive_engine` + `market_event_service`
  - Sort chronologically, group by year, use alternating left/right layout
- **When**: Core C34 implementation.
- **Risk if deferred**: Without a reusable helper, C34 will add 50-80 lines of inline HTML (D3 regression).

#### 3. 🟡 Fix M5 Alert Delivery + Add Test Infrastructure (M5 + D-061)
- **Effort**: 10-14h (8-12h M5 + 2-4h test infra)
- **Why**: The 10 L1 event-alert failures have been "pre-existing" for 5+ sprints. M5 remediation is explicitly in the Sprint 10 plan. The test infrastructure (D-061) is needed to verify the M5 fix and prevent regressions.
- **What**:
  - Separate detection from display in router.py (don't wrap both in one try/except)
  - Add test-mode event injection for L1 test stocks
  - Fix alert rendering to use testable elements
  - Add `conftest.py` with shared fixtures
  - Add tests for `event_interpretation_service` and `comprehension_quiz_service`
  - Add L1 event-alert integration tests
- **When**: Alongside C34 implementation (parallel track).
- **Risk if deferred**: L1 failures will continue to be "pre-existing" indefinitely. Without test infrastructure, M5 fixes cannot be verified automatically.

---

### Sprint 10 Readiness Gate

| Prerequisite | Status | Action Required |
|-------------|--------|-----------------|
| D-062 (quiz engine extraction) | 🟡 NOT STARTED | Do as first Sprint 10 task |
| C34 timeline approach | 🟡 Option B approved | Create `_timeline_event()` helper in `_router_base.py` |
| C105 toggle scope | 🟡 Business card only | Defer other pages to Sprint 11 |
| M5 root cause | 🟡 Analyzed (this document) | Separate detection from display; add test injection |
| D-061 test infra | 🟡 Partially exists | Add conftest.py + new service tests |
| D-063 (unused import) | 🟢 TRIVIAL | Fix during C105 (same file) |
| D-064 (inline HTML) | 🟢 LOW | Fix alongside D-062 |
| D-065 (session state) | 🟢 DEFER | Document keys in main.py comment block |

**Verdict**: Sprint 10 can proceed. D-062 should be the first task (1-2h, low risk, high leverage). C34 and M5 remediation can proceed in parallel. C105 is straightforward and can be done last.

---

*Created: 2026-06-13*
*Reviewer: System Architect*
*Next review: Sprint 10 mid-point or Sprint 11 kickoff*
