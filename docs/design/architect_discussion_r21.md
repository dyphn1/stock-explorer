## Saturday, June 13, 2026 Technical Analysis — Round 21 Discussion

### Executive Summary

Sprint 11 is complete. Sprint 12 is next with a plan spanning QA/polish (C37/C39/C43/C45), Business Card Info Hierarchy redesign, C40 Beginner/Expert Mode navbar toggle, and User Feedback collection. Beyond Sprint 12, three features remain entirely unbuilt: C36 Revenue Tree, C46 Moat Analysis, and C47 Education Academy. This analysis evaluates the technical feasibility of Sprint 12 items, identifies risks, and proposes post-Sprint 12 directions.

**Key Context:**
- Codebase: ~8,000+ LOC, 29 service modules, 36 page modules, 4 data modules
- Architecture: 4-layer model healthy, 88% of services <300 lines, 100% Streamlit-free in services, 0 god modules
- Sprint 11 delivered: D16 (analogy_engine split), D24 (business_card extraction), C34 (Company Timeline), C105 (Simple/Detailed Toggle), M5 remediation, D-061 (test infra)
- Competitor landscape: 14+ rounds of research; narrative features and AI explanations becoming table stakes globally

---

### Sprint 12 Technical Feasibility

#### 1. C37/C39/C43/C45 QA + Content Polish

**Feasibility: 🟢 HIGH — Low risk, well-scoped**

| Item | Current State | Remaining Work | Risk |
|------|--------------|----------------|------|
| C37 Key Takeaways | `key_takeaways.py` (232 lines) + `_render_takeaways()` wired | Content QA pass, verify takeaway quality across top 20 stocks | 🟢 Low — template-based, deterministic |
| C39 What Changed | `delta_engine.py` (164 lines) + `_render_deltas()` wired | QA pass, edge case testing for stocks with <30 days data | 🟢 Low — already rendering |
| C43 Snowflake Health | `health_scoring.py` (269 lines) + `create_health_snowflake()` in chart.py | QA pass, validate scoring against known benchmarks | 🟢 Low — service + chart both exist |
| C45 Valuation Band | `create_valuation_band_chart()` in chart.py | QA pass, verify band calculation accuracy | 🟢 Low — pure chart function |

**Risks:**
- **Content staleness**: C37 takeaways are template-based with manual curation for top 20 stocks. Beyond top 20, fallback generation may produce generic or awkward text. Not a blocker — acceptable degradation.
- **Delta edge cases**: C39 may show misleading deltas for stocks with recent splits or special events. Mitigation: add a minimum-data threshold (skip if <15 data points).

**Blockers:** None.

**Estimated effort:** 6-10h total (QA + minor fixes + content review).

---

#### 2. Business Card Info Hierarchy Redesign

**Feasibility: 🟡 MEDIUM — Design-intensive, moderate architectural impact**

The Challenger (Round 2, Sprint 12 challenge) identified "Feature Overload on Business Card Page" as Risk 1. C37 + C39 + C43 + C45 + C48 (story card) + C41 (read next) + C105 (simple/detailed toggle) all render on the same page. The current section order is:

```
Header → Story Card → Takeaways → Deltas → Health → Risk → One-liner → Key Metrics → Dividend → Revenue Breakdown → Revenue Trend → Valuation → Compare Stories → Read Next → News → Expert Analysis → Historical Scenarios → Study Log → Share → Footer
```

That's **18+ sections** in a single scroll. The ten-second test is failing — users see a wall of content.

**Proposed hierarchy (progressive disclosure):**
- **Tier 1 (immediate):** Header + Takeaways (3-5 bullets) + One-liner + Key Metrics (4 cards)
- **Tier 2 (scroll):** Story Card + Deltas + Health Snowflake + Revenue Pie
- **Tier 3 (expand/click):** Risk + Dividend + Valuation + Compare Stories + News + Expert Analysis + Historical Scenarios

**Risks:**
- **No expand/collapse primitive**: Streamlit has no native accordion that works well across sections. Must use `st.expander()` or session_state toggles. `st.expander()` is the lower-risk choice but limits layout control.
- **Section count**: 18 sections with 3 tiers means ~6 sections per tier. Tier 2 alone may still be overwhelming.
- **Design system consistency**: Each section uses `_info_card()` / `_summary_card()` / raw `st.markdown()`. Inconsistent card styles across tiers will look messy.

**Blockers:** None hard. Requires design review sign-off before implementation.

**Estimated effort:** 8-12h (design + implementation + QA across all tiers).

---

#### 3. C40 Beginner/Expert Mode Navbar Toggle

**Feasibility: 🟡 MEDIUM — Cross-cutting concern, underestimated coupling**

The developer analysis (Round 19) found `_render_simple_overview()` already exists in `_main.py` (lines 62-187) but there's no toggle UI. The Challenger revised C40 estimate from 6-10h to 10-16h, citing cross-section coupling.

**Technical approach:**
- Add `st.session_state["_mode"]` ("beginner" | "expert") — default "beginner"
- Navbar toggle button (🌱 新手 / 🔬 進階) in `router.py` or `_main.py`
- Each `_render_*` function checks mode and conditionally renders

**Risks:**
- **Cross-section coupling (HIGH RISK)**: Every section in `_main.py` and `_sections/*.py` must respect the mode flag. Missing one section = expert content leaking into beginner mode. Requires auditing ALL `_render_*` functions.
- **D24 dependency**: If business_card.py extraction (D24) isn't fully stable, adding mode toggles on top will compound complexity. **Must confirm D24 completion before starting C40.**
- **Scope creep**: "Beginner mode" could mean: hide sections, simplify text, show tooltips, reduce chart complexity. Must define a strict scope: **beginner = hide Tier 3 sections + simplify Tier 2 text.**
- **State persistence**: `session_state` resets on page reload. Users must re-select mode each visit. Acceptable for MVP.

**Blockers:**
- **D24 (business_card.py extraction)** must be confirmed complete. If D24 is delayed, C40 slips to Sprint 13.

**Estimated effort:** 10-16h (toggle UI + audit all sections + conditional rendering + QA).

---

#### 4. User Feedback Collection Mechanism

**Feasibility: 🟢 HIGH — Low risk, standalone feature**

The Challenger (Round 2) recommended adding a simple feedback mechanism in Sprint 2 to address "feature fatigue" risk. After 10+ sprints of dense feature delivery, the team needs user signal on what's working.

**Proposed implementation:**
- Add 👍/👎 buttons at the bottom of the business card page (or in the footer section)
- Store feedback in `config/user_feedback.yaml` with timestamp, stock_id, page, and optional text
- No backend required — file-based storage with `filelock` (same pattern as `notification_service.py`)

**Risks:**
- **File write conflicts**: Multiple concurrent users writing to same YAML file. Mitigation: use `filelock` (already used in `notification_service.py`).
- **No analytics dashboard**: Feedback is collected but not visualized. Acceptable for Sprint 12 — analytics can be added later.
- **Low engagement**: Users may not click feedback buttons. Mitigation: make it prominent but not intrusive (footer placement).

**Blockers:** None.

**Estimated effort:** 2-4h (service + UI + file storage).

---

### Sprint 12 Summary Table

| Item | Feasibility | Risk Level | Blocker | Effort |
|------|------------|------------|---------|--------|
| C37/C39/C43/C45 QA | 🟢 High | Low | None | 6-10h |
| Info Hierarchy | 🟡 Medium | Medium | Design sign-off | 8-12h |
| C40 Mode Toggle | 🟡 Medium | High | D24 completion | 10-16h |
| User Feedback | 🟢 High | Low | None | 2-4h |
| **TOTAL** | | | | **26-42h** |

**Recommendation:** Sprint 12 is feasible at **26-42h** (13-21h/week for a 2-week sprint). The critical path is D24 → C40. If D24 is confirmed complete on Day 1, all items can proceed in parallel. If D24 is delayed, C40 slips and Sprint 12 becomes a lighter QA + Feedback sprint.

---

### Post-Sprint 12 Feature Directions

Three unbuilt features remain from the C36-C47 candidate pool:
- **C36**: Visual Revenue Tree (12-16h)
- **C46**: Moat Analysis (14-18h)
- **C47**: Education Academy (22-32h)

From the broader backlog, these also remain:
- **C02**: Notifications (P0 gap, all competitors have it)
- **C04**: Market Thermometer (P1, beginner-friendly market overview)
- **C06**: PPT Export (P1, leverages unique PPT-style CSS)
- **C33**: Glossary/Tooltips (P2, 8-12h)
- **C34**: Story Timeline — **already shipped** (confirmed in Sprint 11)
- **C35**: Market Mood (P1, conditional on data validation)

I propose **three directions** ranked by architectural leverage:

---

#### Direction A: "Historian's Deep Dive" — C36 Revenue Tree + C46 Moat Analysis

**Alignment:** Core Value #1 "Story first" + "Historian" positioning. Both features explain *how the company works* and *why it's hard to compete with* — the essence of the historian perspective.

**C36 Revenue Tree:**
- **Data availability: 🟡 MEDIUM.** FinMind provides segment-level revenue breakdown (by product/region). For top 20 stocks, manual curation of customer-supplier relationships is needed (~40% content budget). Fallback: existing pie chart for non-curated stocks.
- **Architectural impact: LOW.** New function in `chart.py` (Plotly treemap/sunburst), new section in business card, new YAML data file. No new service layer needed.
- **Dependency risk: LOW.** No external API dependencies. Manual curation is a content task, not a technical blocker.

**C46 Moat Analysis:**
- **Data availability: 🟡 MEDIUM.** Moat analysis is inherently qualitative. FinMind provides some quantitative proxies (gross margin stability, ROE consistency, market share). The 5 dimensions (brand, switching costs, network effects, cost advantages, intangible assets) require manual scoring for top 20 stocks.
- **Architectural impact: MEDIUM.** New `moat_analyzer.py` service (5-dimension scoring), new section in business card, new YAML data file. Must integrate with existing `analogy_engine.py` for plain-language explanations.
- **Dependency risk: MEDIUM.** Content creation (manual moat scoring for 20 stocks) is the bottleneck, not code. If content isn't ready, the service layer can ship with placeholder data.

**Pros:**
- Directly advances "historian" positioning — no TW competitor has either feature
- C36 and C46 are complementary: "How money flows" + "Why it's hard to compete"
- Moderate effort (26-34h total), well-scoped
- Both features are self-contained (single service + single page section each)

**Cons:**
- Manual curation for top 20 stocks is a content bottleneck
- Moat analysis is inherently subjective — may face criticism for oversimplification
- Neither feature drives daily engagement (unlike C02 Notifications)

**Estimated effort:** 26-34h (Sprint 13)

---

#### Direction B: "User Retention Loop" — C02 Notifications + C33 Glossary

**Alignment:** C02 addresses the #1 competitive gap (all competitors have notifications). C33 addresses the #1 UX gap (beginners encounter jargon with no help). Together they create a "come back + understand better" loop.

**C02 Notifications:**
- **Data availability: 🟢 HIGH.** M5 event detection (D04, completed in Sprint 11) already detects events. `notification_service.py` (213 lines) already exists with preference management. The gap is delivery: in-app notification center exists (`notification_center.py`) but no push/external delivery.
- **Architectural impact: MEDIUM.** For MVP: in-app notification badge + notification center page (both exist). For full: email/LINE integration requires external API. **Recommendation: MVP = in-app only (leverage existing infrastructure).**
- **Dependency risk: LOW.** M5 is done. Notification service exists. The remaining work is wiring M5 events → notification creation → badge display.

**C33 Glossary/Tooltips:**
- **Data availability: 🟢 HIGH.** Content task only. `metric_education.py` (250 lines) already has 15+ metric explanations. A `glossary.yaml` with 50-100 terms is straightforward.
- **Architectural impact: LOW-MEDIUM.** New `src/data/glossary.yaml`. UI: add ℹ️ icons next to financial terms across all pages. Streamlit's `st.tooltip()` or `st.expander()` works for this.
- **Dependency risk: LOW.** No external dependencies. Pure content + UI.

**Pros:**
- C02 is the #1 competitive gap — all 14+ competitor research rounds flagged it
- C33 is the highest-ROI beginner feature — every page benefits
- Both features are infrastructure that makes ALL other features better
- Combined effort is moderate (12-20h)

**Cons:**
- C02 in-app notifications are table stakes, not differentiators
- C33 glossary is a content maintenance burden (50-100 terms to write and keep current)
- Neither feature is unique to "historian" positioning

**Estimated effort:** 12-20h (Sprint 13 or 14)

---

#### Direction C: "Education Platform" — C47 Education Academy MVP

**Alignment:** Core Value #4 "Point-to-point knowledge construction" + "Historian" positioning. The endgame for Stock Explorer is not just analyzing companies but teaching users *how to analyze companies themselves*.

**C47 Education Academy:**
- **Data availability: 🟡 MEDIUM.** Lessons use existing FinMind data + analogy engine + metric education. 40% content budget = lesson text, examples, quiz questions. Can start with 7 lessons covering: revenue, margins, ROE, P/E, dividends, health scoring, moat analysis.
- **Architectural impact: HIGH.** New `lesson_service.py`, new `learning_academy.py` page, new YAML lesson data (10-15 lessons), progress tracking (session_state or YAML), quiz integration (leverage existing `quiz_engine.py` + `comprehension_quiz_service.py`).
- **Dependency risk: HIGH.** Content creation is the dominant risk. 7 lessons × 2-3h each = 14-21h of content writing. If content isn't ready, the scaffold ships empty.

**Pros:**
- Unique in TW market — no competitor has structured stock education platform
- Highest long-term retention driver (learning > browsing)
- Leverages ALL existing features (each lesson uses real data from existing services)
- Creates a "learning path" that connects features into a coherent journey

**Cons:**
- Largest single item (22-32h)
- Content creation is external dependency (not fully controllable)
- ROI is long-term, not immediate
- Risk of shipping an empty scaffold if content lags

**Estimated effort:** 22-32h (Sprint 14, with content creation starting in Sprint 13)

---

### Technical Recommendations

**Prioritized by architectural leverage (impact ÷ effort):**

| Priority | Direction | Architectural Leverage | Rationale |
|----------|-----------|----------------------|-----------|
| **1** | **B: C02 + C33** | **HIGHEST** | Infrastructure that improves every page. C02 closes #1 competitive gap. C33 has the widest surface area (all pages, all metrics). Combined 12-20h for foundational infrastructure. |
| **2** | **A: C36 + C46** | **HIGH** | Directly advances "historian" differentiation. Self-contained, moderate effort. No external dependencies. Perfect for Sprint 13. |
| **3** | **C: C47** | **MEDIUM** | Highest long-term value but highest risk. Should start content creation in Sprint 13 (parallel to Direction A) with scaffold shipping in Sprint 14. |

**Recommended Sprint 13-14 Plan:**

| Sprint | Items | Hours | Gate |
|--------|-------|-------|------|
| **Sprint 13** | C36 Revenue Tree + C46 Moat Analysis + C02 in-app notification polish + C33 glossary (first 30 terms) | 38-54h | All features render on business card page |
| **Sprint 14** | C47 Education Academy scaffold + 7 lessons + C33 remaining terms + C04 Market Thermometer spike | 30-42h | First lesson renders with real data |

**Critical architectural note:** C47 Education Academy should NOT be built in isolation. It must reuse:
- `analogy_engine.py` (plain-language explanations)
- `metric_education.py` (metric definitions + analogies)
- `quiz_engine.py` / `comprehension_quiz_service.py` (existing quiz infrastructure)
- `health_scoring.py` (health score lessons)
- `company_facts.py` (example data for lessons)

If these services need extension for C47, extend them in Sprint 13 (alongside C36/C46) so C47 in Sprint 14 is primarily content + page assembly, not service creation.

---

### Open Risks & Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| D24 (business_card extraction) incomplete → C40 blocked | 🔴 High | Day 1 gate in Sprint 12: confirm D24 completion. If delayed, C40 → Sprint 13 |
| Content creation (C36/C46/C47) slower than code | 🟡 Medium | Start content creation in Sprint 13 for Sprint 14 features. Ship scaffold first, content fills in. |
| Business card page performance with 18+ sections | 🟡 Medium | Info hierarchy (Sprint 12) addresses this. Lazy-load Tier 3 sections. |
| Feature fatigue — users overwhelmed by new features | 🟡 Medium | User feedback (Sprint 12) provides signal. C40 beginner mode reduces cognitive load. |
| C47 Education Academy scope creep | 🟡 Medium | Strict MVP: 7 lessons, no video, no AI chatbot, no social features. Scaffold + content only. |

---

*Last updated: 2026-06-13 (Round 21 — System Architect analysis for Sprint 12 feasibility + post-Sprint 12 directions)*
