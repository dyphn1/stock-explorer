## 2026-06-16 Developer Estimates — Round 21 Discussion

### Sprint 12 Item Estimates

| Item | Low Hours | High Hours | Risk | Notes |
|------|-----------|------------|------|-------|
| C37 Key Takeaways QA | 1.0 | 2.0 | 🟢 Low | Ships today. QA = historian tone gate + verify content for top-20 fallback stocks. No code changes unless bugs found. |
| C39 Delta Card QA | 0.5 | 1.5 | 🟢 Low | Already rendering. QA = edge case test for stocks with <30 days of data, add minimum-data threshold if missing. |
| C43 Snowflake Health QA | 1.5 | 3.0 | 🟢 Low | Service (269 lines) + chart both exist. QA = validate scoring against known benchmarks (e.g., TSMC should score high on Profitability). Check color system compliance. |
| C45 Valuation Band QA | 0.5 | 1.0 | 🟢 Low | Pure chart function. QA = verify band calculation accuracy for 2-3 stocks manually. |
| Business Card Info Hierarchy | 8.0 | 14.0 | 🟡 Medium | 18+ sections → 3-tier progressive disclosure. Requires: design sign-off, `st.expander()` or session_state toggles, card style consistency audit across all tiers. **Hidden work**: every `_render_*` function needs Tier 3 sections wrapped in expanders. That's 10+ functions to modify. Dependency: must complete before C40. |
| C40 Beginner/Expert Mode | 10.0 | 18.0 | 🔴 High | Navbar toggle + audit ALL `_render_*` functions (10+ sections). Each section needs mode-aware conditional rendering. D24 must be confirmed complete first (D24 = business_card.py extraction). **Hidden work**: Challenger noted "beginner = hide Tier 3" but which 6 sections are core? This is a product decision that will generate debate. Also: state persistence across page reloads (session_state resets). Scope creep risk: simplifying text, showing tooltips, reducing chart complexity are all separate from "hide sections." Must define strict scope. |
| User Feedback Collection | 2.0 | 4.0 | 🟢 Low | 👍/👎 buttons + optional text. File-based storage with filelock. No analytics dashboard in Sprint 12. Standalone — can be built in parallel with anything. |
| **Sprint 12 TOTAL** | **23.5** | **43.5** | | Round 20 estimate was 26-38h. **Developer estimate: 24-44h** — upper bound exceeds budget by 6h due to Info Hierarchy hidden coupling with C40. If Info Hierarchy slips, C40 scope must shrink. |

**Critical path:** D24 confirmation (Day 1) → Info Hierarchy (8-14h) → C40 (10-18h). C37/C39/C43/C45 QA and User Feedback can run in parallel.

**Key observations:**
- D16 (analogy_engine split) and D24 (business_card extraction) are confirmed complete per Sprint 11 handoff. Architecture debt gate is CLEARED for C40.
- Info Hierarchy and C40 are the bottleneck pair. Info Hierarchy IS the prerequisite work for C40 — every section must be tiered before mode toggle can conditionally hide Tier 3.
- Recommendation: Treat Info Hierarchy + C40 as a single 18-32h block, not separate items.

---

### Post-Sprint 12 Top 3 Estimates

| Feature | Low Hours | High Hours | Risk | Priority Justification |
|---------|-----------|------------|------|----------------------|
| C33 Glossary/Tooltips | 8.0 | 14.0 | 🟡 Medium | **Highest ROI per hour.** Every page, every metric gets inline help. 50-100 terms in `glossary.yaml`. UI: ℹ️ icons via `st.tooltip()` or `st.expander()`. Reuses `metric_education.py` (250 lines, 15+ explanations exist). Beginner onboarding immediately improves. Competitor gap: none have systematic glossary. |
| C46 Moat Analysis | 14.0 | 20.0 | 🟡 Medium | **Best "historian" differentiator.** 5-dimension scoring (brand, switching costs, network effects, cost advantages, intangible assets). Reuses C43 scoring framework from `health_scoring.py`. Greenfield `moat_analyzer.py` (~80 lines). 40% content budget = manual moat scoring for top-20 TW stocks. Template-based fallback for rest. Pairs naturally with C36 in Sprint 13. |
| C36 Revenue Tree | 12.0 | 18.0 | 🟡 Medium | **Visual education, high engagement.** Plotly treemap/sunburst in `chart.py`. FinMind provides segment-level revenue data. Fallback: existing pie chart. New YAML data file for curated revenue hierarchies. Complements C46 ("how money flows" + "why it's hard to compete"). |

**Why these three over alternatives:**
- C02 Notifications (14-18h in-app) is P0-competitive-gap but pulls focus from " historian" differentiation. Already has `notification_service.py` (213 lines) + notification center page. Can be a quick follow-up after these three.
- C06 PPT Export (18-24H) was deprioritized by Challenger (advances zero core values). Technically interesting (python-pptx + kaleido) but low educational mission alignment. Defer to Sprint 15+.
- C47 Education Academy (22-32h) is highest long-term value but highest risk. Content creation dominates (9-13h pure writing). Should start content creation in Sprint 13 (parallel to C36/C46), ship scaffold Sprint 14.

---

### Hidden Complexity Flags

**C40 Beginner/Expert Mode — scope underestimated by 4-8h:**
- Challenger Round 2 flagged "Zone A violation" — the product vision never defines content as "expert-only." Deciding WHICH sections are beginner vs. expert is a product decision that will generate ongoing debate beyond the sprint.
- Every future feature must now tag "beginner" or "expert" at design time — adds overhead to every sprint going forward.
- `session_state` resets on page reload = user must re-select mode each visit = poor UX. Fixing this requires cookie/localStorage (not native in Streamlit) or config file.
- **Developer's view:** C40's 10-18h estimate assumes strict scope (hide Tier 3 + simplify Tier 2 text). If scope expands to "simplify all text in beginner mode" = +6-10h for rewriting.

**Business Card Info Hierarchy — coupling with C40 undercounted:**
- Info Hierarchy work (8-14h) must be 100% complete before C40 can be built. C40's conditional rendering depends on sections being organized into tiers.
- Effective combined estimate: 18-32h, not 18-26h. The gap is the integration testing between hierarchy tiers and mode toggle.

**C36 Revenue Tree — data availability risk:**
- FinMind segment data may be incomplete or inconsistent for non-top-20 stocks. Manual curation fallback is acceptable but requires domain knowledge.
- Plotly treemap/sunburst rendering can be finicky with deeply nested hierarchies. Testing across 20 stocks = ~2h additional QA.

**C47 Education Academy (future sprint) — 40% content budget is optimistic:**
- Prior estimates: 9-13h content creation for 7 lessons. At 2-3h per lesson, that's 7 lessons minimum. More realistically 10-15h for polished content.
- Quiz integration assumes `quiz_engine.py` and `comprehension_quiz_service.py` are stable. Neither has been tested for lesson-context questions.
- If content creation starts in Sprint 13 (parallel to C36/C46), creator bandwidth is shared risk.

**C02 Notifications (future sprint) — architecture investigation overdue:**
- D02 (background worker architecture investigation) is still 📋 Todo. Streamlit is request-response only. True push notifications require external cron or APScheduler.
- Recommendation: MVP = pull-on-next-visit model (14-18h). Full push requires architecture investigation (add 4-6h).

**C06 PPT Export — python-pptx + kaleido dependency risk:**
- Kaleido (for chart→image) has known issues with bundling, Playwright dependency, and cross-platform rendering.
- Each page's PPT rendering must be tested separately. 8 pages × 1h testing = 8h QA.
- Accurate estimate: 18-30h (not 18-24h) when QA and edge cases included.

**C33 Glossary — maintenance burden underestimated:**
- 50-100 terms initially seems small. But every new metric added to the app needs a glossary entry. Ongoing maintenance: ~1h/sprint.
- UI integration: adding ℹ️ icons next to terms across ALL pages = more surface area than expected. Estimate 2-4h just for UI placement across 8+ pages.

---

### Scope Recommendations

**Sprint 12 developer estimate: 24-44h (midpoint: 34h).** This fits within the 38h budget at midpoint but the high end exceeds it by 6h.

**Recommendation 1: Split Info Hierarchy from C40 if sprint starts with <2 weeks capacity.**
- If Sprint 12 is a 1-week sprint (≤20h effective): Drop C40. Do C37/C39/C43/C45 QA (3-8h) + User Feedback (2-4h) + Info Hierarchy v1 (8-12h). C40 moves to Sprint 13.
- If Sprint 12 is a 2-week sprint (≥30h effective): Info Hierarchy (10-12h) + C40 (12-16h) + QA (4-6h) + Feedback (2-4h) = 28-38h. Tight but doable.

**Recommendation 2: Strict scope lock on Info Hierarchy.**
- Tier 1: Header + Takeaways + One-liner + Key Metrics — MUST ship.
- Tier 2: Story Card + Deltas + Health Snowflake + Revenue Pie — MUST ship.
- Tier 3: Risk + Dividend + Valuation + Compare Stories + News + Expert Analysis — wrap in `st.expander()`, no content changes. NO debate about which sections belong in which tier in Sprint 12.

**Recommendation 3: C40 scope = conditional rendering only, no text simplification.**
- Beginner mode: hide Tier 3 sections entirely, show Tier 1 + Tier 2 as-is.
- Do NOT add any text simplification, tooltip enrichment, or chart reduction to Sprint 12 C40 scope.
- This keeps C40 at 10-12h (low end) rather than 16-18h.

**Recommendation 4: Start C47 content creation immediately.**
- Even if Sprint 12 can't build C47, assign content creation for first 4 lessons (revenue, margins, ROE, P/E) to a content owner NOW. These lessons use existing data and don't depend on new features. Having lessons ready when Sprint 14 starts eliminates the #1 risk (content bottleneck).

**Optimized Sprint 12 plan (32-36h target):**

| Item | Hours | Owner | Priority |
|------|-------|-------|----------|
| C37/C39/C43/C45 QA | 3-6h | Dev + QA | Block everything else from shipping |
| Info Hierarchy Tier 1+2 | 8-10h | Dev + Designer | Prerequisite for C40 |
| Info Hierarchy Tier 3 (expanders only) | 1-2h | Dev | Prerequisite for C40 |
| C40 Mode Toggle | 10-12h | Dev | Core Sprint 12 deliverable |
| User Feedback | 2-4h | Dev | Parallel, anytime |
| TOTAL | **24-34h** | | Within 38h budget |

---

*Developer: owl-alpha | Date: 2026-06-16 | Round 21*
