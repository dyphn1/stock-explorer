# Developer Discussion — Round 33: Implementation Cost Estimates

> **Date**: 2026-06-14
> **Author**: Developer (owl-alpha)
> **Purpose**: Estimate implementation costs for candidate features in the next development cycle after Sprint 15
> **Context**: Sprint 15 = D6 YAML migration → chart.py split → CI check → C101 Comprehension Check Quiz

---

## Codebase Snapshot

| Metric | Value |
|--------|-------|
| Service modules | 37 (`src/services/`) |
| Page modules | 42 (`src/pages/`) |
| Data YAML files | 17 (`src/data/`) |
| Architecture | 4-layer (Data → Service → Router → View) |
| API | FinMind (TW stock data) |
| Framework | Python + Streamlit + Plotly |

### Already-Built Infrastructure (Reusable)

The following services/pages already exist and can be leveraged:

| Component | File | Status | Reuse Potential |
|-----------|------|--------|-----------------|
| Notification service | `notification_service.py` | ✅ Built | C02 needs UI wiring + email sender |
| Health scoring | `health_scoring.py` | ✅ Built (scoring logic) | C14 needs radar chart + UI wiring |
| Health snowflake chart | `chart_stock.py` | ✅ Built | C14 can reuse directly |
| Comparison radar chart | `chart_stock.py` | ✅ Built | C38 can reuse |
| Key takeaways | `key_takeaways.py` + `key_takeaways.yaml` | ✅ Built + wired | C37 done |
| Delta engine | `delta_engine.py` | ✅ Built + wired | C39 done |
| Glossary service | `glossary_service.py` + `glossary.yaml` | ✅ Built | C33 needs UI tooltips |
| Compare stories service | `compare_stories.py` | ✅ Built | C38 needs UI wiring |
| Revenue tree page | `revenue_tree.py` | ✅ Built | C36 done |
| Company timeline page | `company_timeline.py` | ✅ Built | C28 needs narrative layer |
| Company facts | `company_facts.py` + YAML | ✅ Built | C16 done |
| Notification center page | `notification_center.py` | ✅ Built | C02 partially done |

**Key insight**: Many "pending" features actually have their service layers already built. The remaining work is primarily UI wiring, integration, and content creation — not greenfield development.

---

## Feature Selection Rationale

After Sprint 15 (which focuses on infrastructure: YAML migration, chart.py split, CI, and C101 Quiz), the next development cycle should prioritize features that:

1. **Advance "Story first"** — the #1 core value that Challenger has repeatedly flagged as under-delivered
2. **Have high ROI** — leverage existing infrastructure to minimize new code
3. **Address P0/P1 gaps** — especially C02 (Notifications), which all competitors have
4. **Are blocked by Sprint 15 completion** — features that need the YAML migration or chart.py split finished

### Top 5 Candidate Features (Post-Sprint 15)

| Rank | ID | Feature | Priority | ROI | Why This One |
|-------|-----|---------|----------|-----|--------------|
| 1 | C02 | Notification/Push System | P0 | 🔴 Highest | All competitors have it; M5 engine is wasted without it; service layer already built |
| 2 | C28 | Company Story Timeline (Narrative) | P1 | 🔴 High | Unique differentiator; no competitor has it; event data + timeline page already exist |
| 3 | C14 | Company Health Score (Radar) | P1 | 🟡 High | Scoring logic + snowflake chart already built; needs UI wiring |
| 4 | C33 | Glossary Tooltip System | P2 | 🟡 Medium-High | Service + data already built; needs UI integration across pages |
| 5 | C07 | Custom Event Thresholds | P1 | 🟡 Medium | Unlocks C02 personalization; needs settings page + adaptive_engine integration |

---

## Feature 1: C02 — Notification/Push System

### Current State
- `notification_service.py` ✅ — Full service layer: settings CRUD, pending notifications, severity filtering, acknowledgment tracking
- `notification_center.py` ✅ — Page exists with UI for viewing/acknowledging notifications
- `adaptive_engine.py` ✅ — M5 event detection verified working with real FinMind data
- **Gap**: No email delivery mechanism; no background worker; "pull on next visit" only

### Implementation Approach

#### Phase 1A: Email Notification (Recommended First)
| Task | Files | Hours |
|------|-------|-------|
| Add SMTP email sender function | New `src/services/email_sender.py` | 2-3 |
| Create email template (HTML, TW language) | New `src/templates/notification_email.html` | 1-2 |
| Wire notification_service to send email on new high-severity event | Modify `notification_service.py` | 2-3 |
| Add email settings to notification preferences UI | Modify `notification_center.py` | 1-2 |
| Add email test button + validation | Modify `notification_center.py` | 1 |
| **Subtotal** | | **7-11h** |

#### Phase 1B: Background Worker Investigation (D02)
| Task | Files | Hours |
|------|-------|-------|
| Investigate APScheduler vs external cron for Streamlit | Research doc | 2-3 |
| Implement "pull on next visit" enhancement (check on every page load) | Modify `_router_base.py` | 2-3 |
| Add notification badge count to navbar | Modify `router.py` or main layout | 1-2 |
| **Subtotal** | | **5-8h** |

#### Phase 2: Line Notify (Future)
| Task | Files | Hours |
|------|-------|-------|
| LINE Bot account setup + API integration | New `src/services/line_notifier.py` | 3-4 |
| User LINE ID binding in settings | Modify `notification_center.py` | 2-3 |
| **Subtotal** | | **5-7h** |

### Time Estimate
| Phase | Low | High |
|-------|-----|------|
| Phase 1A: Email | 7h | 11h |
| Phase 1B: Worker + Badge | 5h | 8h |
| Phase 2: Line Notify | 5h | 7h |
| **Total (Phase 1A+1B)** | **12h** | **19h** |
| **Total (all phases)** | **17h** | **26h** |

### Technical Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| Streamlit is request-response only; no true push | High | Phase 1A uses "pull on next visit" + email for true push |
| SMTP deliverability (spam filters) | Medium | Use established SMTP provider (Gmail/SES); add SPF/DKIM |
| FinMind API rate limits during batch detection | Medium | Already handled in `notification_service.py` with try/except per stock |
| Email frequency overwhelming users | Low | Severity filtering (default: high only) + digest mode option |

### Dependencies
- **D02** (Background Worker Architecture Investigation) — must decide on approach before Phase 1B
- **C07** (Custom Thresholds) — should follow C02 to allow notification personalization
- **M5 verification** ✅ Already done (D01 complete)

### Existing Infrastructure Reuse
- `notification_service.py` — 100% reuse for settings, pending, acknowledgment
- `notification_center.py` — 100% reuse for UI; add email settings panel
- `adaptive_engine.py` — 100% reuse for event detection
- `watchlist.py` — 100% reuse for subscribed stocks

---

## Feature 2: C28 — Company Story Timeline (AI-Generated Narrative)

### Current State
- `company_timeline.py` ✅ — Basic event timeline page exists (shows events as cards)
- `adaptive_engine.py` ✅ — Event detection with false positive filtering
- `events.yaml` ✅ — 8 real events from real FinMind data
- `analogy_engine.py` ✅ — Plain-language analogy generation for 8+ metrics
- **Gap**: Events are disconnected list; no narrative thread connecting them; no "Turning Points" algorithm

### Implementation Approach

#### Spike (Recommended First — 3h validation)
| Task | Files | Hours |
|------|-------|-------|
| Validate event data richness: can existing events support narrative? | Analyze `events.yaml` | 1 |
| Prototype narrative template with 1 stock (TSMC) | Jupyter/experimental | 1 |
| Validate output quality with Challenger criteria | Review | 1 |
| **Spike Total** | | **3h** |

#### Full Implementation (Post-Spike)
| Task | Files | Hours |
|------|-------|-------|
| Design `narrative_engine.py` — chronological narrative from events + metrics | New `src/services/narrative_engine.py` | 4-6 |
| Implement "Turning Points" algorithm (top 5-10 events by impact) | Part of `narrative_engine.py` | 3-4 |
| Extend `events.yaml` schema with `narrative_category` field (NEW-G18) | Modify `config/events.yaml` + `adaptive_engine.py` | 2-3 |
| Redesign `company_timeline.py` with narrative sections + turning points | Modify `src/pages/company_timeline.py` | 3-4 |
| Add "Story" tab to business card page linking to timeline | Modify `business_card/_sections/` | 1-2 |
| Add "Story Updates" section for recent events on business card | Modify `business_card/_sections/_story.py` | 2-3 |
| Content creation: seed narrative templates for top 10 stocks | New `src/data/narrative_templates.yaml` | 3-4 |
| **Implementation Total** | | **18-26h** |

### Time Estimate
| Scope | Low | High |
|-------|-----|------|
| Spike only | 3h | 3h |
| Full implementation (post-spike) | 18h | 26h |
| **Total** | **21h** | **29h** |

### Technical Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| Event data too sparse for meaningful narrative | High | Spike validates this first; fallback: template-based narrative from metrics alone |
| Narrative quality inconsistent across stocks | Medium | Curated templates for top 20 stocks; rule-based fallback for others |
| `events.yaml` schema migration (NEW-G18) | Low | Additive schema change; backward compatible |
| LLM dependency for quality narrative | Medium | Phase 1: template-based only (no LLM); LLM enhancement deferred to C17 |

### Dependencies
- **NEW-G18** (events.yaml schema extension) — must be done before narrative engine
- **M5 verification** ✅ Already done
- **Spike validation** — must pass before committing to full implementation

### Existing Infrastructure Reuse
- `adaptive_engine.py` — Event detection, loading, filtering
- `company_timeline.py` — Page structure, event card rendering
- `analogy_engine.py` — Plain-language explanations for metrics
- `events.yaml` — Existing event data
- `chart_stock.py` — Timeline visualization patterns

---

## Feature 3: C14 — Company Health Score (5-Axis Radar)

### Current State
- `health_scoring.py` ✅ — Full scoring logic: 5 axes (Profitability, Growth, Financial Health, Dividend, Valuation), 0-100 per axis
- `chart_stock.py` ✅ — `create_health_snowflake()` function exists
- `chart_stock.py` ✅ — `create_comparison_radar()` function exists
- `financial_metrics.py` ✅ — All required financial metrics calculable
- **Gap**: Not wired into any page; no plain-language explanation per axis; no UI

### Implementation Approach

#### Option A: Health Score Badge (Reduced Scope)
| Task | Files | Hours |
|------|-------|-------|
| Create badge component (score + color + one-line summary) | New function in `business_card/_sections/_health.py` | 2-3 |
| Wire `compute_health_scores()` into business card data flow | Modify `_router_base.py` or business card | 1-2 |
| Add plain-language summary per axis | Extend `health_scoring.py` `get_health_summary()` | 1-2 |
| **Option A Total** | | **4-7h** |

#### Option B: Full 5-Axis Radar Chart (Recommended)
| Task | Files | Hours |
|------|-------|-------|
| Wire `compute_health_scores()` into `_router_base.py` data dict | Modify `_router_base.py` | 1-2 |
| Create radar chart section on business card using `create_health_snowflake()` | Modify `business_card/_sections/_health.py` | 3-4 |
| Add plain-language explanation per axis ("Your Profitability is 85/100 because...") | New `src/services/health_explainer.py` | 3-4 |
| Add compare mode: overlay two companies' radars | Modify `peer_comparison.py` | 2-3 |
| Add health score to key metrics summary | Modify `business_card/_sections/_summary.py` | 1-2 |
| Testing with real data for 5+ stocks | Test scripts | 1-2 |
| **Option B Total** | | **11-17h** |

### Time Estimate
| Option | Low | High |
|--------|-----|------|
| Option A: Badge only | 4h | 7h |
| Option B: Full radar | 11h | 17h |
| **Recommended (Option B)** | **11h** | **17h** |

### Technical Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| Missing financial data for some stocks (causing None scores) | Medium | Already handled: `compute_health_scores()` defaults to 50.0 for missing data |
| Scoring algorithm calibration (are thresholds right?) | Medium | Start with current thresholds; iterate after testing with 10+ stocks |
| Radar chart readability on mobile | Low | Streamlit's Plotly renderer handles responsive; test with `use_container_width=True` |
| Health explainer text quality | Low | Reuse `analogy_engine.py` patterns; template-based |

### Dependencies
- **business_card.py completion** — Health score must be wired into a functional business card page
- **D-002-NEW fix** ✅ Already done (business_card.py restored to 370+ lines)
- **financial_metrics.py** ✅ Already provides all required inputs

### Existing Infrastructure Reuse
- `health_scoring.py` — 100% reuse for scoring logic
- `chart_stock.py` — 100% reuse for `create_health_snowflake()` and `create_comparison_radar()`
- `financial_metrics.py` — 100% reuse for metric extraction
- `analogy_engine.py` — Pattern reuse for health explanations
- `business_card/_sections/_health.py` — Existing section file to extend

---

## Feature 4: C33 — Glossary Tooltip System

### Current State
- `glossary_service.py` ✅ — Service layer with `get_glossary_term()`, `get_all_terms()`, `search_terms()`
- `glossary.yaml` ✅ — Data file with term definitions
- **Gap**: No UI integration; no tooltips on any page; glossary data may be incomplete

### Implementation Approach

| Task | Files | Hours |
|------|-------|-------|
| Audit glossary.yaml coverage (how many terms? how many used in pages?) | Analyze `glossary.yaml` + page files | 1-2 |
| Create reusable tooltip component (`_glossary_tooltip()`) | Add to `_router_base.py` or shared components | 2-3 |
| Add tooltips to financial terms on business card page | Modify `business_card/_sections/*.py` (4 files) | 2-3 |
| Add tooltips to financial health page | Modify `financial_health.py` | 1-2 |
| Add tooltips to peer comparison page | Modify `peer_comparison.py` | 1-2 |
| Add tooltips to operation checkup page | Modify `operation_checkup.py` | 1-2 |
| Create glossary reference page (full list, searchable) | New `src/pages/glossary_page.py` | 2-3 |
| Expand glossary.yaml to cover all terms used in pages | Modify `glossary.yaml` | 2-3 |
| **Total** | | **14-20h** |

### Time Estimate
| Scope | Low | High |
|-------|-----|------|
| Core: tooltips on 4 key pages + component | 8h | 12h |
| Full: all pages + glossary page + data expansion | 14h | 20h |
| **Recommended (core first)** | **8h** | **12h** |

### Technical Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| Streamlit tooltip limitations (no native hover) | Medium | Use `st.popover()` or `st.tooltip()` (Streamlit 1.35+) or expandable `st.expander()` |
| Glossary data incomplete for all terms | Low | Start with terms that appear in pages; expand incrementally |
| Performance: loading glossary on every page render | Low | `glossary_service.py` already has in-memory cache |
| Maintenance: new terms added without glossary entries | Low | Add linting check in CI (post-Sprint 15) |

### Dependencies
- **Sprint 15 CI check** — Can add glossary coverage lint after CI is established
- **Streamlit version** — `st.tooltip()` requires Streamlit ≥1.35; verify version

### Existing Infrastructure Reuse
- `glossary_service.py` — 100% reuse
- `glossary.yaml` — 100% reuse (expand)
- `_router_base.py` — Add shared tooltip component
- All page modules — Add tooltip calls at financial term locations

---

## Feature 5: C07 — Custom Event Thresholds

### Current State
- `adaptive_engine.py` ✅ — Event detection with hardcoded thresholds (revenue ±30%, price ±7%)
- `notification_service.py` ✅ — Notification settings with severity preferences
- **Gap**: No UI for customizing thresholds; no settings page for event detection sensitivity

### Implementation Approach

| Task | Files | Hours |
|------|-------|-------|
| Create settings page for event thresholds | New `src/pages/settings.py` | 3-4 |
| Add threshold configuration to `adaptive_engine.py` (parameterize hardcoded values) | Modify `adaptive_engine.py` | 2-3 |
| Add new event types (institutional consecutive days, revenue consecutive months) | Modify `adaptive_engine.py` | 3-4 |
| Persist user thresholds (extend `notification_service.py` or `user_prefs.py`) | Modify `notification_service.py` or NEW-G19 | 1-2 |
| Wire thresholds into notification filtering | Modify `notification_service.py` | 1-2 |
| Add threshold presets (Conservative / Normal / Sensitive) | Modify `settings.py` | 1-2 |
| **Total** | | **11-17h** |

### Time Estimate
| Scope | Low | High |
|-------|-----|------|
| Core: settings page + parameterize existing thresholds | 6h | 9h |
| Full: + new event types + presets | 11h | 17h |
| **Recommended (core first)** | **6h** | **9h** |

### Technical Risks
| Risk | Severity | Mitigation |
|------|----------|------------|
| New event types may have high false positive rate | Medium | Start with conservative thresholds; test with historical data |
| Threshold persistence across sessions | Low | Use `st.session_state` for anonymous; YAML for persistent (NEW-G19) |
| Settings page adds complexity to navigation | Low | Add to sidebar as "⚙️ 設定" — low prominence |
| Interaction with C02 notifications | Medium | Ensure threshold changes immediately affect notification filtering |

### Dependencies
- **D01 M5 verification** ✅ Already done
- **NEW-G19** (User Preference Storage Abstraction) — Recommended before C07 for clean persistence
- **C02** — C07 should precede or accompany C02 for full notification personalization

### Existing Infrastructure Reuse
- `adaptive_engine.py` — Parameterize existing detection functions
- `notification_service.py` — Extend settings with threshold config
- `events.yaml` — Existing event storage format
- `FinMindClient` — All data sources already available

---

## ROI Ranking

| Rank | Feature | Impact | Effort (mid) | ROI (Impact/Effort) | Priority |
|------|---------|--------|--------------|---------------------|----------|
| 1 | C02 Notifications (Phase 1A+1B) | 9/10 | 15.5h | 0.58 | P0 |
| 2 | C14 Health Score (Option B) | 8/10 | 14h | 0.57 | P1 |
| 3 | C07 Custom Thresholds (core) | 7/10 | 7.5h | 0.93 | P1 |
| 4 | C33 Glossary Tooltips (core) | 6/10 | 10h | 0.60 | P2 |
| 5 | C28 Story Timeline (full) | 9/10 | 24.5h | 0.37 | P1 |

**Note**: C28 has the highest impact but also the highest effort. The spike-first approach (3h) de-risks it. C07 has the highest ROI because it's a force multiplier for C02.

---

## Recommended Sprint Plan (Post-Sprint 15)

### Sprint 16 — Foundation + Quick Wins
| Order | Feature | Hours | Core Value |
|-------|---------|-------|------------|
| 1 | C07 Custom Thresholds (core) | 6-9h | #3 Adaptive |
| 2 | C02 Notifications Phase 1A (Email) | 7-11h | #3 Adaptive |
| 3 | C33 Glossary Tooltips (core) | 8-12h | #4 Point-to-point |
| | **Sprint Total** | **21-32h** | |

### Sprint 17 — Core Features
| Order | Feature | Hours | Core Value |
|-------|---------|-------|------------|
| 1 | C28 Story Timeline (Spike → Full) | 3h spike + 18-26h | #1 Story first |
| 2 | C14 Health Score (Option B) | 11-17h | #2 PPT-style, #5 Benchmark |
| | **Sprint Total** | **32-46h** | |

### Sprint 18 — Polish + Expand
| Order | Feature | Hours | Core Value |
|-------|---------|-------|------------|
| 1 | C02 Notifications Phase 1B (Worker + Badge) | 5-8h | #3 Adaptive |
| 2 | C33 Glossary (full: all pages + glossary page) | 6-8h | #4 Point-to-point |
| 3 | C02 Notifications Phase 2 (Line Notify) | 5-7h | #3 Adaptive |
| | **Sprint Total** | **16-23h** | |

### Grand Total (3 Sprints)
| | Low | High |
|--|-----|------|
| Sprint 16 | 21h | 32h |
| Sprint 17 | 32h | 46h |
| Sprint 18 | 16h | 23h |
| **Total** | **69h** | **101h** |
| With 20% buffer | **83h** | **121h** |

---

## Key Risks Across All Features

| Risk | Features Affected | Mitigation |
|------|-------------------|------------|
| Sprint 15 delays (YAML migration, chart.py split) | All | These are prerequisites; monitor Sprint 15 progress |
| Streamlit architecture limitations (no true push, no hover) | C02, C33 | Use email for push; use popover/expander for tooltips |
| FinMind API rate limits | C02, C07, C28 | Already handled in data layer; batch detection is per-stock with try/except |
| Content creation bottleneck (narrative templates, glossary terms) | C28, C33 | Prioritize top 20 stocks; use rule-based fallback for others |
| business_card.py stability | C14, C28 | P0 fix already done; add regression tests in CI |

---

## Notes for Discussion

1. **C37 (Key Takeaways) and C39 (What Changed Recently) are already implemented** — discovered during codebase review. The issues.md backlog was stale. These should be marked ✅ Done.

2. **C36 (Revenue Tree) page already exists** — `revenue_tree.py` is built with treemap visualization. C36 should be verified and marked ✅ Done or updated with remaining work.

3. **C38 (Compare Stories) service + page already exist** — `compare_stories.py` (service) and `compare_stories.py` (page) are both built. Needs verification of completeness.

4. **C16 (Did You Know? Company Facts) is already implemented** — `company_facts.py` + `company_facts.yaml` with 70 facts for 7 stocks. Already wired into business_card.py.

5. **The "historian" positioning is validated by international competitors** — StockStory, Stockopedia AI, and Stocksera all launched narrative features in 2025. Stock Explorer's advantage is explainable, plain-language narratives grounded in verified FinMind data.

6. **C02 is the most critical P0 gap** — All competitors have notifications. Our M5 event detection engine is built and verified but wasted without proactive notification. Even Phase 1A (email) closes this gap.

---

*Developer estimates based on codebase review of 37 service modules, 42 page modules, and 17 data YAML files. All estimates assume single developer (owl-alpha) working with existing architecture patterns. Estimates include implementation + unit testing but NOT design review or Challenger rounds.*
