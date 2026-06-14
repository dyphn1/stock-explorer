## 2026-06-14 Technical Analysis — Round 33 Feature Directions (Post-Sprint 15)

### Current Architecture State

**Architecture Health: 🟢 HEALTHY**
- 37 service modules, ~50 page modules (including business_card sub-sections)
- 4-layer architecture consistently enforced (Data → Service → Router → View)
- 165+ tests passing
- L0: 106/106, L1: 20/20
- Sprint 14 complete: C126 Moat Comparison, C47 Education Academy, D-081/D-082/D-083 fixes
- Sprint 15 planned: D6 YAML migration → chart.py split → CI check → C101 Comprehension Check Quiz

**Key Existing Infrastructure (Reusable):**
- `adaptive_engine.py` — M5 event detection, verified with 8 real events
- `analogy_engine.py` — Plain-language translation for 8+ metrics
- `health_scoring.py` — 5-dimension health scoring (269 lines, complete)
- `risk_analyzer.py` — 3-dimension risk analysis (567 lines, complete)
- `moat_analyzer.py` — Moat analysis for 20 TW stocks
- `company_timeline.py` — Timeline page (View layer)
- `compare_stories.py` — Story comparison (View + Service)
- `revenue_tree.py` — Revenue treemap (View layer)
- `stock_screener.py` — Stock screener (View layer)
- `notification_center.py` — Notification center (View layer)
- `glossary_service.py` — Glossary with 99 terms
- `key_takeaways.py` — Auto-generated key takeaways
- `delta_engine.py` — "What Changed Recently" delta computation
- `event_interpretation_service.py` — Event interpretation
- `market_event_service.py` — Case study data
- `comprehension_quiz_service.py` — Quiz engine
- `financial_wellness_service.py` — Financial wellness
- `metric_education.py` — Metric education
- `story_feed.py` — Story feed for investor stories

**Architecture Debt (Still Open):**
- `chart.py` (842 lines) — Sprint 15 plans to split into chart_stock.py + chart_market.py
- `analogy_engine.py` — God module covering only 8 metrics; 15+ metrics on financial health page lack plain-language explanations
- `_financial.py` — Multi-responsibility (if it exists; may have been refactored)
- NEW-G16: ETF detection logic bug (5min fix, still open)
- NEW-G18: events.yaml schema extension for story timeline
- NEW-G19: User preference/state storage abstraction
- NEW-G20: analogy_engine.py coverage gap (30+ metrics need explanations)

---

### Feature Directions for Round 33

Based on analysis of:
1. **Competitor gaps** (Rounds 1-11): C02 Notifications, C14 Health Score, C28 Story Timeline, C42 Stock Screener, C43 Snowflake, C45 Valuation Band, C46 Moat Analysis
2. **Issue tracker P0/P1 items not yet done**: C02 (Notifications), C06 (PPT Export), C07 (Custom Thresholds), C40 (Mode Toggle — partially done as C105)
3. **Product vision alignment**: "Historian, not stock picker" + "Story first, data second" + "Ten-second test"
4. **Existing infrastructure leverage**: health_scoring.py, risk_analyzer.py, analogy_engine.py, adaptive_engine.py

---

#### Direction 1: C14 Health Score Visualization + C45 Valuation Band Chart — "At-a-Glance Company Snapshot"

**Technical Feasibility: 🟢 HIGH**

**What it is:** Combine two high-ROI, low-effort features into a single "Company Snapshot" card at the top of the business card page:
- **C14 Health Score**: Visual radar chart using existing `health_scoring.py` (269 lines, 5-dimension scoring complete). The service layer is DONE — only View-layer rendering is needed.
- **C45 Valuation Band Chart**: Horizontal bar chart showing current P/E vs 5-year historical range. Data source: FinMind price + EPS data (already available in `financial_metrics.py`).

**Estimated Effort: 10-14h**
- C14 Health Score radar chart: 4-6h (service layer exists, just need Plotly radar in View layer + plain-language explanations per axis)
- C45 Valuation Band chart: 3-4h (data already available, simple horizontal bar chart)
- Integration + testing: 3-4h

**Architecture Fit:**
- New chart functions in `chart.py` (or `chart_stock.py` after Sprint 15 split): `create_health_radar_chart()`, `create_valuation_band_chart()`
- View layer: Add "Company Snapshot" section to `business_card/_sections/` (new file or extend `_summary.py`)
- Service layer: `health_scoring.py` already has `compute_health_score()` — just need to wire it. `financial_metrics.py` already has P/E extraction.
- No new data sources needed. No new API calls needed.

**Pros:**
- **Highest ROI** — directly addresses the "ten-second test" design principle. A beginner can glance at the snapshot and immediately understand the company's health + valuation.
- **All infrastructure exists** — health_scoring.py (269 lines), risk_analyzer.py (567 lines), financial_metrics.py are complete. This is purely View-layer work.
- **Competitor-validated** — Simply Wall St (snowflake), Morningstar (stars), Stockopedia (StockRank) all prove demand. Our differentiator: plain-language explanations per axis.
- **C45 Valuation Band** is the single highest-ROI feature from Round 9 (8-10h, 財報狗 proves demand). P/E as a single number without context is meaningless to beginners.
- **Low risk** — no new data dependencies, no new API calls, no architectural changes.

**Cons:**
- **Business card page is already dense** — adding a snapshot card at the top could push content below the fold. Must be compact (max 2 cards: radar + band chart).
- **chart.py is 842 lines** — adding 2 new chart functions before Sprint 15's split could increase debt. Mitigation: add to `chart_stock.py` if split is done; otherwise, add to `chart.py` and mark for reorganization.
- **Health score scoring thresholds** — `health_scoring.py` uses hardcoded thresholds that may not be optimal for all industries. May need industry-specific benchmarks (soft dependency on `peer_comparison.py` industry data).

**Recommendation: ✅ STRONGLY RECOMMEND.** This is the single highest-impact, lowest-risk direction. It directly addresses the "ten-second test" (core design principle), leverages existing infrastructure, and fills a P1 competitor gap. The health score service is DONE — we're just not showing it to users yet.

---

#### Direction 2: C02 Notification System — Phase 1 "Pull-on-Visit" + C07 Custom Event Thresholds

**Technical Feasibility: 🟡 MEDIUM**

**What it is:** Implement C02 Notifications as a "pull-on-visit" model (D02's recommended approach) combined with C07 Custom Event Thresholds:
- **C02 Phase 1**: Instead of true push notifications (requires background worker, D02 still open), show a notification badge on the navbar when the user returns to the app. "You have 3 new events since your last visit." Click to view in `notification_center.py` (already built).
- **C07 Custom Thresholds**: Allow users to adjust event detection sensitivity (revenue ±30% → user-configurable). Settings stored in `session_state` (existing pattern) or `user_prefs.py` (NEW-G19, still open).

**Estimated Effort: 12-18h**
- C02 Pull-on-visit: 6-8h (track last visit timestamp, compare with events.yaml, show badge count)
- C07 Custom Thresholds: 4-6h (settings UI in event_dashboard.py or new settings page, wire to adaptive_engine.py)
- Integration + testing: 2-4h

**Architecture Fit:**
- `notification_center.py` already exists as a View layer page
- `adaptive_engine.py` already has `run_auto_detection()` wired in `router.py`
- `events.yaml` already stores detected events with timestamps
- NEW-G19 (user_prefs.py) is a soft dependency — can use `session_state` for MVP
- No new data sources needed. No background worker needed (pull model avoids D02 blocker).

**Pros:**
- **P0 competitor gap** — ALL competitors have notifications (StatementDog: Line, CMoney: Push, GoodInfo: Email, Yahoo: App Push). This is the #1 feature gap.
- **M5 event detection is wasted without notifications** — the adaptive engine detects events but users only see them when they happen to visit the stock page. Notifications close the loop.
- **Pull-on-visit avoids D02 blocker** — no background worker architecture investigation needed. Simple timestamp comparison.
- **C07 Custom Thresholds** are a natural extension of the M5 engine and unlock personalization.
- **notification_center.py already built** — the View layer exists; we just need to wire the badge count.

**Cons:**
- **Pull-on-visit is not true push** — users won't see events until they return to the app. Less engaging than push notifications. Phase 2 (true push) still blocked by D02.
- **Settings page is new UI** — C07 requires a settings page that doesn't exist yet. Adds UI complexity.
- **Session state loss** — `session_state` is ephemeral. Custom thresholds reset on page switch unless NEW-G19 (user_prefs.py) is implemented first.
- **Events.yaml staleness** — if events aren't pruned or refreshed properly, the notification badge could show stale data. D03 (90-day retention) is done, but freshness logic needs verification.

**Recommendation: ✅ RECOMMEND (Conditional).** This is the P0 gap and should be prioritized, but with conditions: (1) implement as pull-on-visit only (avoid D02 blocker), (2) use session_state for custom thresholds (defer NEW-G19), (3) wire existing notification_center.py rather than building new UI. The combination of C02 + C07 delivers the core notification loop without requiring background worker architecture.

---

#### Direction 3: C28 Company Story Timeline — Spike + Template-Based Narrative

**Technical Feasibility: 🟡 MEDIUM**

**What it is:** Implement a "Company Story" tab that weaves events, revenue milestones, and price movements into a chronological narrative. This is the #1 unique differentiator — NO competitor has narrative timelines (verified across 40+ competitors in Rounds 1-11).

**Scope for Round 33: SPIKE ONLY (3-5h)**
- Validate the narrative generation approach with a template-based (non-LLM) prototype
- Use existing `events.yaml` (8 real events) + `adaptive_engine.py` + `analogy_engine.py`
- Build a minimal `src/pages/company_story.py` with 3-5 events rendered as a timeline
- Do NOT commit to full 20-30h implementation yet — spike first

**Estimated Effort: 3-5h (spike) → 20-30h (full implementation)**
- Spike: 3-5h (template-based timeline rendering, 3-5 events, no LLM)
- Full implementation (future sprint): 20-30h (narrative engine, turning points algorithm, compare stories)

**Architecture Fit:**
- `company_timeline.py` already exists as a View layer page — can be extended or serve as template
- `adaptive_engine.py` provides event data (verified, 8 real events in events.yaml)
- `analogy_engine.py` provides plain-language explanations for metrics at each timeline point
- `compare_stories.py` already exists as a service — can be extended for "Compare Stories" mode
- NEW-G18 (events.yaml schema extension) is a soft dependency — current schema works for spike

**Pros:**
- **Unique differentiator** — NO competitor (TW or international) has narrative timelines. This is the feature that best embodies "historian, not stock picker" positioning.
- **Validates "Story first, data second"** — the #1 core value. All other features support this value; this feature IS this value.
- **Spike-first approach minimizes risk** — 3-5h validates the approach before committing 20-30h.
- **Existing infrastructure** — events.yaml, adaptive_engine, analogy_engine, company_timeline.py all exist.
- **Competitive threat validated** — StockStory (Singapore, 2025) and Stockopedia AI (2025 relaunch) both have AI-generated narratives for TW stocks. This is becoming table stakes.

**Cons:**
- **Full implementation is expensive** — 20-30h for narrative engine, turning points algorithm, and compare stories. Spike doesn't deliver user value.
- **Content quality risk** — template-based narratives may feel mechanical. LLM-based narratives (C17) are higher quality but higher risk (hallucination, cost).
- **events.yaml has only 8 events** — for the spike, this is enough. For full implementation, need richer event data (NEW-G18 schema extension).
- **Business card page is already the target for C14/C45** — adding Story Timeline as a separate tab avoids page overload, but adds a new navigation entry.

**Recommendation: ⚠️ RECOMMEND AS SPIKE ONLY.** The full C28 is the most strategically important feature (unique differentiator, "Story first" embodiment), but 20-30h is too large for a single sprint alongside C14/C45. Recommend a 3-5h spike to validate the template-based approach, then schedule full implementation for Sprint 16+.

---

### Comparative Analysis

| Dimension | Direction 1: Health + Valuation | Direction 2: Notifications | Direction 3: Story Timeline |
|-----------|-------------------------------|---------------------------|---------------------------|
| **Technical Feasibility** | 🟢 HIGH | 🟡 MEDIUM | 🟡 MEDIUM |
| **Effort** | 10-14h | 12-18h | 3-5h (spike) / 20-30h (full) |
| **Core Value Alignment** | #1 Ten-second test + #5 Benchmark | #3 Adaptive | #1 Story first (BEST) |
| **Competitor Gap** | 🔴 P1 (all competitors have it) | 🔴 P0 (ALL competitors have it) | 🔴 Unique (NO competitor has it) |
| **Existing Infrastructure** | ✅ health_scoring.py DONE | ✅ notification_center.py DONE | ✅ events.yaml + timeline DONE |
| **Risk** | Low | Medium (D02 blocker avoided) | Medium (content quality) |
| **User Impact** | High (immediate understanding) | Medium (engagement loop) | Very High (differentiator) |

---

### Recommendation

**Primary Recommendation: Direction 1 (C14 Health Score + C45 Valuation Band) as the main focus for the next sprint after Sprint 15.**

**Rationale:**
1. **Highest ROI** — 10-14h for two features that directly address the "ten-second test" and fill P1 competitor gaps
2. **All infrastructure exists** — purely View-layer work, no new data sources, no architectural changes
3. **Low risk** — no blockers, no dependencies, no new API calls
4. **Complements Sprint 15** — after chart.py split and C101 Quiz, the business card page will have a solid foundation. Adding a "Company Snapshot" card is the natural next step.

**Secondary Recommendation: Direction 3 (C28 Story Spike) as a 3-5h spike in the same sprint.**

**Rationale:**
1. Validates the narrative approach before committing 20-30h in a future sprint
2. Uses existing events.yaml (8 real events) — no new data needed
3. If the spike succeeds, C28 becomes the #1 priority for Sprint 16

**Tertiary Recommendation: Direction 2 (C02 + C07) deferred to Sprint 16+.**

**Rationale:**
1. P0 gap but pull-on-visit model is a compromise (not true push)
2. D02 (background worker investigation) is still open and represents architectural risk
3. C02 is more valuable AFTER the business card page has a complete snapshot (C14 + C45) — notifications should point users to rich content, not empty pages

---

### Proposed Sprint 16 Scope (Post-Sprint 15)

| Priority | Item | Effort | Core Value |
|----------|------|--------|------------|
| 1 | C14 Health Score Visualization | 4-6h | #1 Ten-second test |
| 2 | C45 Valuation Band Chart | 3-4h | #1 Story + #5 Benchmark |
| 3 | C28 Story Timeline Spike | 3-5h | #1 Story first |
| 4 | NEW-G16 ETF Detection Bug Fix | 5min | Correctness |
| 5 | NEW-G19 User Prefs Abstraction | 2-3h | Infrastructure |
| **Total** | | **12-18h** | |

**Buffer: 32-38h remaining** for bug fixes, tech debt, and unexpected issues.

---

*Last updated: 2026-06-14*
