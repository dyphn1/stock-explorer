# 2026-06-14 Technical Analysis — C163 + C40 Implementation Directions

## Context

**C163 (Learn First Gate)** and **C40 (Beginner/Expert Mode Toggle)** are the two remaining Sprint 20 features. Both target the same user segment — beginners — and both deal with progressive disclosure of complexity. They should be designed as a unified "beginner experience" system rather than two isolated features.

### Current State of the Codebase

Key findings from reading the architecture, source code, and competitor research:

1. **C105 (Simple/Detailed Toggle) already exists** in `src/pages/business_card/_main.py:208` — a `st.toggle("簡易模式", value=True)` that controls whether `_render_simple_overview()` or the full detail sections are shown. However, it only affects the business card page, the toggle resets to `True` on every render (no persistence), and it has no effect on other pages (operation checkup, financial health, peer comparison, etc.).

2. **C103 (First Visit Guide)** already exists in `src/pages/first_visit_guide.py` — a 2-card dismissible primer shown on first visit. It uses `st.session_state["first_visit_dismissed"]` and is routed via the "新手導覽" page in `router.py`. C163 is explicitly designed to **replace and absorb** C103, not coexist with it.

3. **C47 (Education Academy)** exists in `src/pages/academy.py` with 5 YAML lessons, quiz system, and progress tracking via `st.session_state["academy_progress"]`. C163 is a **gateway** (onboarding flow before data), while C47 is a **destination** (a page users visit to learn). These are complementary, not redundant.

4. **Session state pattern** is well-established: `st.session_state` is managed at the router level and used throughout the presentation layer. Keys follow the convention `snake_case` with optional prefixes for in-page state.

5. **The navbar** (`_render_navbar` in `router.py`) uses `st.radio` for page navigation. There is no existing toggle/switch in the navbar area.

6. **Competitor validation**: Simply Wall St (snowflake visual summary), Sharesies (complexity levels), NerdWallet ("Simple View"), and Webull ("Learn first, trade later") all have some form of complexity toggle or education-first onboarding. No TW competitor has either. This is a validated gap.

### Architectural Constraints

- **Layered architecture**: Data → Service → Router → Presentation. The mode toggle is purely a UI/presentation concern. The gate is a routing concern. Neither should introduce logic into the service or data layers.
- **Session state management** belongs at the router level. Views read from `st.session_state` but should not introduce new global state keys without router coordination.
- **Page switching** uses `navigate_to()` from `url_sync.py`, which syncs `st.session_state` to URL query params. Any gate or mode change must be compatible with this mechanism.
- **No `st.cache_data`** in the View layer (per architecture.md §3.3).

---

## Option A: Unified Beginner Experience System

**Concept**: Design C163 and C40 as two facets of a single "beginner experience" system. C163 is the **temporal gate** (first-visit onboarding), C40 is the **persistent toggle** (always-available complexity control). They share a common `user_experience_level` state.

### Implementation

1. **New session state key**: `st.session_state["user_experience_level"]` — values: `"beginner"` | `"intermediate"` | `"expert"`. Set to `"beginner"` by default for new users.

2. **C163 — Learn First Gate**: A new page (`"學習入門"`) that appears as the default landing page for first-time users (detected via `st.session_state.get("first_visit_dismissed", False)` being `False`). The gate presents 3-5 micro-lessons using existing `_summary_card` and `_info_card` components from `_router_base.py`. Each micro-lesson is a content block (heading, paragraph, callout) defined in a new YAML file (`config/lessons/gateway_lessons.yaml`). After completion (or explicit skip), set `first_visit_dismissed = True` and navigate to the business card page. **Replaces `first_visit_guide.py`** — the old "新手導覽" page is removed from the router.

3. **C40 — Beginner/Expert Mode Toggle**: A toggle in the navbar area (added to `_render_navbar` in `router.py`) that switches between `"beginner"` and `"expert"`. The toggle value is persisted in `st.session_state["user_experience_level"]`. In beginner mode:
   - Business card page: uses existing C105 simple mode (already shows 3-4 key metrics, no advanced sections)
   - Other stock pages (operation checkup, financial health, peer comparison): show only the first 1-2 sections, with remaining sections collapsed behind expanders labeled "🔬 進階內容"
   - Academy page: shows beginner-level lessons first
   - All pages: glossary tooltips (C170) are auto-shown on first occurrence of financial terms

4. **Shared infrastructure**: A new `src/services/experience_service.py` that provides:
   - `get_experience_level()` → reads from session state
   - `is_beginner_mode()` → convenience check
   - `get_gateway_lessons()` → loads gateway lesson content from YAML
   - This keeps the service layer free of Streamlit imports (pure functions), while the presentation layer handles session state.

### Pros
- **Cohesive user experience**: Beginner onboarding (C163) naturally leads into beginner mode (C40). The user journey is: "Learn the basics → Explore with guidance → Graduate to expert mode."
- **Minimal code duplication**: Both features share the `user_experience_level` state and the gateway lesson YAML infrastructure. The existing C105 toggle in `_main.py` is simply extended, not rewritten.
- **Clean architecture**: The experience service is a pure service (no Streamlit imports). The gate is a routing concern (router level). The mode toggle is a UI concern (presentation layer). No layer violations.
- **Future-proof**: The `user_experience_level` state can later be used by C165 (Varsity Mode), C122 (Adaptive Learning), and C35 (Market Mood) to personalize content.
- **Replaces C103 cleanly**: No coexistence confusion. The old `first_visit_guide.py` is removed.

### Cons
- **Broader scope**: Affects multiple pages (business card, operation checkup, financial health, peer comparison). Each page needs to check `is_beginner_mode()` and conditionally render sections. This is more effort than a single-page change.
- **Risk of inconsistent beginner experience**: If some pages don't implement the beginner mode check, users see an inconsistent experience. Requires a per-page audit.
- **Navbar modification**: Adding a toggle to `_render_navbar` affects all stock pages. The toggle must be carefully placed to avoid cluttering the navbar (which already has 26 page tabs).
- **Effort estimate**: 18-24h (C163: 8-10h, C40: 8-10h, shared infrastructure: 2-4h). This exceeds the individual estimates (8-12h + 10-14h = 18-26h) but the shared infrastructure reduces total effort by ~4-6h.

### Architectural Impact
- **Router layer**: Modified — new default landing page for first-time users, navbar toggle added.
- **Presentation layer**: Modified — multiple pages need beginner mode checks. New gateway page created. Old `first_visit_guide.py` removed.
- **Service layer**: New — `experience_service.py` added (pure functions, no Streamlit).
- **Data layer**: New — `config/lessons/gateway_lessons.yaml` added.
- **Session state**: New keys — `user_experience_level`, `gateway_lesson_progress`. Existing key `first_visit_dismissed` retained but managed by the gate.

---

## Option B: Minimal Viable Implementation

**Concept**: Implement C163 and C40 as independently as possible, minimizing cross-feature dependencies. C163 is a standalone gate page. C40 is a renamed/persisted version of the existing C105 toggle, scoped to the business card page only.

### Implementation

1. **C163 — Learn First Gate**: Same as Option A (new gateway page with micro-lessons, replaces C103), but **no connection** to the mode toggle. The gate simply sets `first_visit_dismissed = True` and navigates to the business card page. No `user_experience_level` state is introduced.

2. **C40 — Beginner/Expert Mode Toggle**: Rename the existing C105 toggle from "簡易模式" to "🌱 新手模式" / "🔬 進階模式". Add persistence via `st.session_state["simple_mode"]` (already exists at line 209 of `_main.py`). Add a `st.session_state` initialization in the router to persist the choice across page switches. **Scope is limited to the business card page only** — other pages are unchanged.

3. **No shared infrastructure**: No `experience_service.py`. No `user_experience_level` state. Each feature is independent.

### Pros
- **Lowest risk**: Minimal changes to existing code. C40 is essentially a rename + persistence of existing C105. C163 is a new page with no dependencies on other features.
- **Fits within Sprint 20 budget**: C163: 8-10h, C40: 4-6h. Total: 12-16h, well within the 16-28h remaining after C167.
- **Easy to test**: Each feature can be tested independently. No cross-feature interactions to verify.
- **No architectural changes**: No new service layer files. No router modifications (C163 is just another standalone page like C103 was).

### Cons
- **Missed opportunity**: C163 and C40 are related but implemented independently. The gate teaches concepts, but the mode toggle doesn't reinforce them. No shared `user_experience_level` state means future features (C165, C122) can't leverage it.
- **C40 scope is too narrow**: Limiting the toggle to the business card page means beginners still see the full complexity of operation checkup, financial health, and peer comparison pages. This partially defeats the purpose of C40.
- **No navbar toggle**: The toggle remains on the business card page (in the content area), not in the navbar. This is less discoverable and doesn't match the competitor research (Sharesies/NerdWallet have the toggle in the global navigation).
- **Technical debt**: The existing C105 toggle in `_main.py` is a page-level concern that duplicates what should be a router-level state. Persisting it at the router level without a proper service is a partial fix that may need rework later.

### Architectural Impact
- **Router layer**: Minimal — C163 is added as a standalone page (same pattern as C103). Session state initialization for `simple_mode` added.
- **Presentation layer**: Modified — new gateway page, renamed toggle on business card page only.
- **Service layer**: No changes.
- **Data layer**: New — `config/lessons/gateway_lessons.yaml` added.
- **Session state**: Existing key `simple_mode` retained. Key `first_visit_dismissed` retained.

---

## Option C: Router-Centric Gate + View-Level Mode

**Concept**: Implement C163 as a router-level gate (intercepting page rendering for first-time users) and C40 as a pure presentation-layer concern (each view checks a session state key and adjusts rendering accordingly). The router is the single point of control for both features.

### Implementation

1. **C163 — Router-Level Gate**: Instead of a separate page, the gate is implemented as a **router interception**. In `load_and_render_page()`, before rendering any stock page, check `st.session_state.get("first_visit_dismissed", False)`. If `False`, render the gateway content (micro-lessons) inline, with a "Continue to stock data" button that sets the flag and triggers `st.rerun()`. This means the gate is not a separate page — it's a conditional overlay that appears before any stock data is shown.

2. **C40 — View-Level Mode**: Each view function (`_render_business_card`, `_render_operation_checkup`, `_render_financial_health`, etc.) checks `st.session_state.get("simple_mode", True)` and adjusts rendering. The toggle is placed in the navbar via a custom column. The key difference from Option A is that there's no `experience_service.py` — each view directly reads `st.session_state`.

3. **Shared session state**: Both features use `st.session_state` directly, with no service layer abstraction. The router initializes defaults for `first_visit_dismissed` and `simple_mode`.

### Pros
- **Strong architectural gate**: The router is the single point of control for the gate, which aligns with the architecture's principle that "router is the only place that can decide when to load what data" (architecture.md §2.3).
- **No new service layer**: Avoids creating a new service for what is essentially a UI state concern.
- **Per-page control**: Each view decides how to render in beginner mode, allowing page-specific optimizations (e.g., operation checkup shows only revenue trend; financial health shows only profit funnel).

### Cons
- **Router bloat**: `load_and_render_page()` is already 270 lines with 20+ page branches. Adding gate logic and navbar toggle logic will make it harder to maintain.
- **Gate is not a page**: Implementing the gate as a router interception means it can't be navigated to directly, can't be bookmarked, and doesn't appear in the URL. This breaks the URL sync mechanism (`url_sync.py`). Users who dismiss the gate can't revisit it.
- **Inconsistent with existing patterns**: C103 (First Visit Guide) is a standalone page, not a router interception. C47 (Academy) is a standalone page. Making C163 a router interception breaks the pattern.
- **Testing difficulty**: Router-level gate logic is harder to test in isolation than a standalone page.
- **Effort estimate**: 20-26h (C163: 10-12h for router modifications + gateway UI, C40: 10-14h for per-page mode checks). This is the highest effort option.

### Architectural Impact
- **Router layer**: Significantly modified — gate logic, navbar toggle, session state initialization all in `router.py`.
- **Presentation layer**: Modified — all stock pages need beginner mode checks.
- **Service layer**: No changes.
- **Data layer**: New — `config/lessons/gateway_lessons.yaml` added.
- **Session state**: Keys `first_visit_dismissed` and `simple_mode` managed at router level.

---

## Recommendation

**Option A (Unified Beginner Experience System)** is the recommended approach.

### Why Option A

1. **Product coherence**: C163 and C40 are two sides of the same coin — both control how much complexity a beginner sees. Implementing them as a unified system with shared `user_experience_level` state creates a coherent user journey: "Learn first → Explore with guidance → Graduate to expert."

2. **Architecturally sound**: The experience service (`experience_service.py`) is a pure service with no Streamlit imports, keeping the service layer clean. The gate is a routing concern (new default landing page). The mode toggle is a presentation concern (navbar + per-page checks). Each layer has clear responsibilities.

3. **Future-proof**: The `user_experience_level` state becomes a platform-level primitive that future features can leverage:
   - C165 (Varsity Mode): uses experience level to recommend lessons
   - C122 (Adaptive Learning): adjusts level based on comprehension check scores
   - C35 (Market Mood): simplifies display for beginners
   - C170 (Tappable Glossary): auto-shows in beginner mode

4. **Effort is manageable**: 18-24h total, which fits within the 16-28h remaining Sprint 20 budget (after C167's ~14h). The shared infrastructure reduces total effort compared to implementing C163 and C40 independently.

5. **Clean replacement of C103**: C163 absorbs C103's role, avoiding the confusion of having both a "新手導覽" page and a "學習入門" page. The old `first_visit_guide.py` is removed.

6. **Competitor-aligned**: Sharesies and NerdWallet both have global complexity toggles (navbar-level). Webull has education-first onboarding (gate). Option A combines both patterns, matching the competitive landscape.

### Why Not Option B
Option B is too minimal. Limiting C40 to the business card page means beginners still see full complexity on operation checkup, financial health, and peer comparison pages. This defeats the purpose of a "beginner mode." The lack of shared `user_experience_level` state creates technical debt for future features.

### Why Not Option C
Option C violates the existing page pattern (C103 and C47 are standalone pages, not router interceptions). It breaks URL sync. It concentrates too much logic in the router, which is already complex. The effort (20-26h) is the highest of the three options.

---

## Prerequisites

Before implementing Option A, the following prerequisites must be addressed:

### P1: Define "Beginner Mode" Spec per Page
Each stock page needs a clear definition of what "beginner mode" means:
- **Business card**: Already implemented (C105 simple mode — 3-4 key metrics, no advanced sections)
- **Operation checkup**: Beginner = revenue trend + revenue analogy only (hide institutional charts, volume analysis)
- **Financial health**: Beginner = profit funnel + key ratios only (hide debt analysis, cash flow, dividend details)
- **Peer comparison**: Beginner = top-3 peers + plain-language comparison only (hide detailed metric tables)
- **Group structure**: Beginner = parent company + top-3 subsidiaries only (hide full tree)

**Effort**: 2-3h (content design, not coding). Should be done by PM/Designer before Sprint 20 coding begins.

### P2: Gateway Lesson Content
The 3-5 micro-lessons for C163 need to be written. These should cover:
1. What is a stock? (ownership, not gambling)
2. How to read a company card (revenue, margins, P/E)
3. What is P/E ratio? (price vs. earnings, "years to pay back")
4. What is ROE? (how well the company uses your money)
5. How to use Stock Explorer (historian, not stock picker)

**Effort**: 3-4h (content writing). Can be done in parallel with coding by a non-developer.

### P3: Remove C103 (First Visit Guide)
`first_visit_guide.py` must be removed from the router and the codebase before C163 is added. The "新手導覽" page entry should be removed from the navbar page lists in `router.py`.

**Effort**: 0.5h (remove import, remove router branch, remove file). Should be done as part of C163 implementation.

### P4: Navbar Toggle Placement
The navbar in `_render_navbar` uses `st.radio` for 26 page tabs. Adding a toggle requires either:
- A separate row above/below the radio buttons (using `st.columns`)
- Replacing the radio with a custom button row that includes the toggle

**Decision needed**: Should the toggle be in the navbar (global, always visible) or in the sidebar (global, but collapsible)? The competitor research suggests navbar placement (Sharesies/NerdWallet), but Streamlit's sidebar may be more practical given the 26-tab radio already in the navbar.

**Recommendation**: Place the toggle in the **sidebar** as a prominent element above the search box. This avoids navbar clutter, is always visible (sidebar default is expanded), and is consistent with Streamlit conventions. The sidebar is Zone B (navigation), which is the correct zone for a global control per the design system.

### P5: Session State Initialization Order
The router must initialize `user_experience_level` and `first_visit_dismissed` **before** any page rendering occurs. Currently, session state initialization is scattered across pages (e.g., `academy.py` initializes `academy_progress` on first access). For C163/C40, the initialization must be centralized in the router to ensure the gate check happens before any data loading.

**Implementation**: Add initialization in `sync_url_to_session()` (in `url_sync.py`) or at the top of `load_and_render_page()`. Recommended: add to `sync_url_to_session()` since it runs before every render and already handles `page` and `stock_id` initialization.

---

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Sprint 20 overflow (C163 + C40 exceed remaining budget) | High | Option A effort is 18-24h, remaining budget is 16-28h. Tight but feasible. If C167 took less than 14h, there's buffer. Cut-line rule: if C163 is done but C40 is not, C40 carries over and displaces C171 (stretch) in Sprint 21. |
| Per-page beginner mode inconsistency | Medium | P1 prerequisite (define spec per page) ensures all pages have a clear beginner mode definition before coding starts. |
| Gateway lesson content not ready | Low | P2 prerequisite. Content can be written in parallel. If not ready, C163 ships with placeholder content and is updated in Sprint 21. |
| URL sync conflict with gate | Low | The gate is a page (not a router interception), so `navigate_to()` handles URL sync naturally. No conflict. |
| Toggle state lost on page switch | Medium | The toggle value is stored in `st.session_state["user_experience_level"]` which persists across page switches (session state is global). The router initializes it once. No loss. |
| Navbar clutter from toggle | Medium | P4 prerequisite. Sidebar placement avoids navbar clutter. |

---

## Effort Summary

| Component | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| C163 (Learn First Gate) | 8-10h | 8-10h | 10-12h |
| C40 (Beginner/Expert Mode) | 8-10h | 4-6h | 10-14h |
| Shared infrastructure | 2-4h | 0h | 0h |
| **Total** | **18-24h** | **12-16h** | **20-26h** |
| Prerequisites (P1+P2) | 5-7h | 5-7h | 5-7h |

---

*Analysis by: System Architect (openrouter/nvidia/nemotron-3-super-120b-a12b:free)*
*Date: 2026-06-14*
*References: architecture.md, competitor_research.md (R7-R18), design_system.md, review40_challenger.md, review40_architect.md, CHALLENGE_LOG.md*
*Key source files examined: router.py, business_card/_main.py, academy.py, first_visit_guide.py, _router_base.py, url_sync.py, lesson_service.py, settings.py*
