# Developer Estimates — Discussion Round 10

## 2026-06-16 Developer Estimates — Round 10 (Post-Sprint 2)

---

## Context Update: What Changed Since Round 9

Sprint 2 delivered C37 (Key Takeaways), C39 (What Changed Delta), C45 (Valuation Band), and C43 (Snowflake Health Visualization). Key observations from the delivered code:

1. **No separate service modules were extracted** — C37/C39/C43 features were likely folded into `business_card.py` or `_router_base.py`, not built as standalone `summary_engine.py`/`delta_engine.py` services. This means:
   - The "add a new service module" pattern from Sprint 2 is **unproven** — we need to verify it works
   - `_router_base.py` is now **more overloaded** — risk of further debt accumulation
   - Future features (C42, C44, C46, C47) should follow a clean service-layer pattern from the start

2. **Architecture debt R1 (financial_metrics extraction) is STILL outstanding** — This is now a P0 blocker for C44 and C46, both of which need consistent financial metric calculations. Every feature built without R1 adds to the duplication.

3. **Sprint 3 capacity is ~40h but already allocated** — C41 (6.5h) + C38 (8-10h) + C44 (10-14h) + R5 (4-6h) = ~35-40h. C42, C46, and C47 will need to go in Sprint 4 or later.

4. **C44 is already in Sprint 3** — The handoff confirms C44 is planned for Sprint 3. My estimate below validates whether that's realistic.

---

### C42: Stock Screener / Discovery Engine

- **Implementation breakdown**:
  - New page file `src/pages/screener.py` (entry point + layout): 3h
  - Data layer: batch-fetch metrics for ~1,800 stocks (reuse ThreadPoolExecutor pattern from `_router_base.py`): 4-5h
  - Filtering engine: multi-criteria filter logic (ROE, P/E, dividend yield, revenue growth, industry) with UI controls (`st.selectbox`, `st.slider`): 3-4h
  - Preset system: 3-4 beginner-friendly presets ("穩定收息", "成長潛力", "便宜估值") with YAML config: 2h
  - Results table: `st.dataframe` with clickable links to business card pages, sorting, column selection: 2-3h
  - UI polish: stock count, loading states, empty-state handling, mobile layout: 1-2h
  - L0 + L1 verification: 1h
- **Total estimate**: 16-20h (implementation) + 3-4h (testing) = **19-24h**
- **Technical risks**:
  - **FinMind API rate limits**: 1,800 stocks × multiple metrics = potential 5,000+ API calls. The batch ThreadPoolExecutor pattern from `_router_base.py` mitigates this, but rate limit detection/retry logic is untested at this scale. Risk: **HIGH**.
  - **Data completeness**: Not all 1,800 stocks have complete financial data. Need graceful handling of missing fields (NaN filtering). Risk: **MEDIUM**.
  - **UI responsiveness**: Filtering 1,800 rows client-side with Streamlit requires careful state management. `st.session_state` caching of the full dataset is essential. Risk: **MEDIUM**.
  - **Filter interaction complexity**: Combining AND/OR logic across 5+ filter criteria with range sliders is more complex than it appears. Risk: **MEDIUM**.
- **Dependencies**:
  - **R3 (batch API calls)**: If R3 was done during Sprint 2, this is already solved. If not, C42 will be painfully slow. **Must verify R3 status before starting C42.**
  - **FinMindClient.get_stock_info()**: Already used by `category_browser.py`. Proven pattern.
  - **No dependency on R1 (financial_metrics)**: C42 uses raw FinMind data, not computed metrics like gross_margin or ROE. However, if we want to filter on computed metrics (ROE, margins), R1 becomes a dependency.
  - **Depends on Sprint 2's business_card.py**: Results link to business card pages. If C43/C45 changed the business card layout, verify navigation still works.
- **Testing effort**: 3-4h
  - L0 import test for new page
  - L1 render test with mock FinMind data
  - Filter logic unit tests (pure functions, no Streamlit dependency)
  - Edge cases: empty results, all stocks filtered out, missing data fields
- **Realistic for sprint capacity?**: **NO for Sprint 3** (already full). **YES for Sprint 4** — fits alongside C36 (8-10h) if C42 is scoped to MVP (presets only, no custom filters) at ~16h. Full custom screener (20h) would need its own sprint or pair with a smaller feature.

---

### C44: "What Could Go Wrong" Risk Analysis

- **Implementation breakdown**:
  - New service `src/services/risk_engine.py` (risk scoring + plain-language generation): 3-4h
  - Risk data computation: revenue concentration (top customer %), debt ratio trend, income volatility, event keyword frequency from `adaptive_engine.py`: 3-4h
  - Risk scoring model: heuristic 1-5 scale per dimension with clear thresholds: 2h
  - Plain-language risk descriptions using `analogy_engine.py` patterns: 2-3h
  - UI section in `business_card.py`: risk cards with severity badges (🟢🟡🔴), expandable details: 2-3h
  - Historical evidence lookup: integrate with `events.yaml` for "has this risk materialized before?": 1-2h
  - L0 + L1 verification: 1h
- **Total estimate**: 14-20h (implementation) + 3-4h (testing) = **17-24h**
- **Technical risks**:
  - **Risk scoring subjectivity**: The biggest risk is that scores feel arbitrary. Need clear, documented thresholds (e.g., "debt_ratio > 60% = high risk"). Risk: **HIGH**.
  - **Data availability**: Customer concentration data is NOT in FinMind — it requires manual curation from annual reports. For top 20 stocks only, this is ~2h of data entry. For 1,800 stocks, it's impossible. Risk: **HIGH** (scope limitation).
  - **Tone calibration**: Risk analysis must feel educational ("historian" positioning), not like a "sell signal". Wording matters enormously. Risk: **MEDIUM**.
  - **R1 dependency**: Risk scoring uses debt_ratio, gross_margin, ROE — all currently duplicated across files. Without R1, C44 will add a 5th copy of the same logic. Risk: **HIGH** (architecture debt accumulation).
- **Dependencies**:
  - **R1 (financial_metrics extraction)**: **P0 BLOCKER**. C44 computes debt_ratio, gross_margin, and ROE volatility. Without R1, this adds to the duplication problem. Strongly recommend doing R1 (2.5-4h) before or alongside C44.
  - **adaptive_engine.py**: For event keyword analysis and news sentiment. Already exists.
  - **analogy_engine.py**: For plain-language risk descriptions. Already exists.
  - **events.yaml**: For historical evidence lookup. Already exists.
  - **Manual data curation**: Customer concentration data for top 20 stocks (~2h, one-time effort).
- **Testing effort**: 3-4h
  - Risk scoring function unit tests (pure functions)
  - Threshold boundary tests (e.g., debt_ratio = 59% vs 60%)
  - L0/L1 for new service + business card integration
  - Tone review (non-technical: does it feel educational or alarmist?)
- **Realistic for sprint capacity?**: **BARELY for Sprint 3**. The handoff allocates 10-14h for C44 in Sprint 3, but my estimate is 17-24h. The 10-14h figure likely assumes a reduced scope (top 20 stocks only, 3 risk dimensions instead of 5). **Recommendation**: Reduce scope to MVP — 3 risk dimensions (financial health, revenue concentration, event frequency) for top 20 stocks only. This brings it to ~12-14h, fitting Sprint 3. Full C44 can be a v2 enhancement.

---

### C46: "Moat" Analysis — Competitive Advantage Assessment

- **Implementation breakdown**:
  - New service `src/services/moat_engine.py` (moat scoring + description generation): 3-4h
  - Moat dimension computation: gross margin stability (5-year trend), market share proxy, ROE vs industry, switching cost proxy, brand strength proxy: 3-4h
  - Moat scoring model: 5 dimensions × 1-5 scale = composite moat score (wide/narrow/none): 2-3h
  - Plain-language moat descriptions using `analogy_engine.py` patterns: 2-3h
  - Manual curation: moat data for top 20 stocks (technology leadership, brand, cost advantage, etc.): 3-4h
  - UI section in `business_card.py`: moat type badges, strength indicator, historical evidence cards: 2-3h
  - Radar chart overlay (reuse C43's radar/snowflake pattern): 1-2h
  - L0 + L1 verification: 1h
- **Total estimate**: 17-24h (implementation) + 3-4h (testing) = **20-28h**
- **Technical risks**:
  - **Moat scoring is inherently subjective**: Unlike P/E or ROE, there's no standard formula for "moat width". The scoring model will need clear documentation and stakeholder alignment. Risk: **HIGH**.
  - **Data availability**: Many moat dimensions (brand strength, switching costs, network effects) are qualitative. We can proxy some (gross margin stability → pricing power, ROE vs industry → competitive advantage), but others require manual curation. Risk: **HIGH**.
  - **Manual curation bottleneck**: Top 20 stocks × 5 moat dimensions = 100 data points to research and enter. At ~2 min each = ~3.5h. This is the single largest time sink. Risk: **MEDIUM** (predictable but tedious).
  - **R1 dependency**: Moat scoring uses gross_margin, ROE, revenue_yoy — same duplicated calculations. Risk: **HIGH** (same as C44).
  - **Radar chart reuse**: C43's snowflake/radar chart may need modification for moat dimensions. Verify the chart component is reusable. Risk: **LOW**.
- **Dependencies**:
  - **R1 (financial_metrics extraction)**: **P0 BLOCKER** for same reasons as C44. Moat scoring needs consistent financial calculations.
  - **analogy_engine.py**: For moat descriptions. Already exists.
  - **peer_comparison.py / INDUSTRY_BENCHMARKS**: For industry comparison data. Already exists (but see D6 — hardcoded in Python, not YAML).
  - **C43 (Snowflake)**: Radar chart pattern from C43 is reusable. If C43's radar implementation is clean, C46 saves ~2h.
  - **Manual data curation**: 3-4h for top 20 stocks' moat data.
- **Testing effort**: 3-4h
  - Moat scoring function unit tests
  - Threshold boundary tests
  - L0/L1 for new service + business card integration
  - Data validation: ensure manual curation data loads correctly
- **Realistic for sprint capacity?**: **NO for Sprint 3** (already full). **TIGHT for Sprint 4**. The handoff plan shows Sprint 4 with C36 (8-9h) + C42 (16-24h) + C46 (12-16h) = 36-49h. At my revised estimates (C42: 19-24h, C46: 20-28h, C36: 8-10h), Sprint 4 would be 47-62h — **over capacity**. **Recommendation**: Defer C46 to Sprint 5, or reduce C42 scope to MVP (presets only, ~16h) to fit C46 in Sprint 4.

---

### C47: Financial Education Academy / Structured Learning Path

- **Implementation breakdown**:
  - New page file `src/pages/academy.py` (curriculum layout, lesson viewer, progress tracking): 4-5h
  - Data layer: YAML schema for lessons (title, concept, analogy, example stock, quiz) + 10-15 lesson files: 4-6h
  - Content creation: writing 10-15 lessons with real TW stock examples, analogies, and quiz questions: 8-12h
  - Progress tracking: `st.session_state` integration for completed lessons, quiz scores, progress bar: 2-3h
  - Quiz interactivity: radio buttons, answer feedback, score display: 2-3h
  - Reuse `analogy_engine.py` for concept explanations: 1-2h
  - UI polish: lesson cards, difficulty badges, completion checkmarks, responsive layout: 2-3h
  - L0 + L1 verification: 1h
- **Total estimate**: 24-35h (implementation) + 4-6h (testing) = **28-41h**
- **Technical risks**:
  - **Content creation is 40% of total effort**: This is not a coding risk — it's a content production risk. Writing 10-15 high-quality lessons with accurate financial explanations, appropriate analogies, and meaningful quiz questions is a significant writing task. Risk: **HIGH**.
  - **YAML schema design**: Getting the lesson schema right upfront is critical. Changing the schema after 10 lessons are written means reformatting all of them. Risk: **MEDIUM**.
  - **Mobile responsiveness**: Long-form text content with embedded charts needs careful mobile layout. Risk: **LOW** (Streamlit handles most of this).
  - **Progress persistence**: `st.session_state` is session-only. Users lose progress on page refresh. For an education platform, this is a UX problem. Risk: **MEDIUM** (consider file-based progress storage).
- **Dependencies**:
  - **analogy_engine.py**: For concept explanations. Already exists.
  - **company_facts.yaml**: Proven YAML data pattern. Academy lessons follow the same pattern.
  - **No dependency on R1**: Academy is content-driven, not calculation-driven.
  - **No dependency on other C4x features**: Academy is independently buildable.
  - **Content dependency**: Lessons need real TW stock examples. Requires research time.
- **Testing effort**: 4-6h
  - YAML schema validation tests
  - Lesson content loading tests
  - Progress tracking logic tests
  - L0/L1 for new page
  - Content review (non-technical: are lessons accurate and educational?)
- **Realistic for sprint capacity?**: **NO for Sprints 3 or 4**. At 28-41h, C47 is essentially a sprint-sized feature on its own. The handoff plan correctly places it in Sprint 5 with 60h capacity. **Strong recommendation**: Split C47 into phases:
  - **Phase 1 (Sprint 5, ~20h)**: 8-10 lessons, basic quiz, no progress tracking. MVP to validate the concept.
  - **Phase 2 (Post-Sprint 5, ~15h)**: Remaining lessons, progress tracking, advanced quiz features.
  This reduces Sprint 5 risk and gets user feedback earlier.

---

### Sprint Capacity Analysis

#### Current Sprint 3 Allocation (from handoff)

| Item | Hours | Status |
|------|-------|--------|
| C41: Read Next Recommendations | 6.5h | Planned |
| C38: Compare Stories Phase 1 | 8-10h | Planned |
| C44: Risk Analysis | 10-14h | Planned |
| R5: Migrate hardcoded data to YAML | 4-6h | Planned |
| **Total** | **28.5-36.5h** | **Fits in ~40h** |

**Assessment**: Sprint 3 is **tight but feasible** IF C44 is scoped to MVP (3 risk dimensions, top 20 stocks, ~12-14h). If C44 expands to full scope (5 dimensions, all stocks), Sprint 3 is **over capacity by 4-8h**.

#### Projected Sprint 4 Allocation

| Item | Hours | Status |
|------|-------|--------|
| C36: Visual Revenue Tree | 8-10h | Planned |
| C42: Stock Screener | 19-24h | Planned |
| C46: Moat Analysis | 20-28h | Planned |
| **Total** | **47-62h** | **OVER CAPACITY** |

**Assessment**: Sprint 4 as planned is **significantly over capacity** (47-62h vs ~40h). Even at the low end (47h), it exceeds capacity by 17%. At the high end (62h), it's 55% over.

**Options to fix Sprint 4**:
1. **Defer C46 to Sprint 5**: Sprint 4 = C36 (9h) + C42 (22h) = 31h ✅
2. **Reduce C42 to MVP**: Sprint 4 = C36 (9h) + C42-MVP (16h) + C46 (22h) = 47h — still tight
3. **Defer C36**: Sprint 4 = C42 (22h) + C46 (22h) = 44h — still over

**Recommendation**: Option 1 — defer C46 to Sprint 5. C42 is higher priority (P1, transforms product from lookup to discovery) and C36 is nearly done (data curation for 8 stocks already exists).

#### Projected Sprint 5 Allocation

| Item | Hours | Status |
|------|-------|--------|
| C47: Education Academy Phase 1 | 20h | Planned |
| C46: Moat Analysis (deferred) | 22h | Deferred from S4 |
| Buffer / Polish | 18h | — |
| **Total** | **60h** | **Fits** |

**Assessment**: Sprint 5 with C47 Phase 1 + C46 = 42h + 18h buffer = 60h. Feasible.

---

### Recommendations

#### Immediate (Before Sprint 3)

1. **Verify R3 (batch API) status**: If R3 was NOT done during Sprint 2, C42 will be unusably slow. Check if `category_browser.py` still uses sequential API calls. If so, do R3 (3-5h) as the first Sprint 3 task.

2. **Do R1 (financial_metrics extraction) before C44**: C44 is in Sprint 3 and needs consistent financial calculations. R1 is 2.5-4h and eliminates duplication across 4+ files. **This is the single highest-impact debt item for Sprint 3.** Without it, C44 will add a 5th copy of the same gross_margin/debt_ratio/ROE logic.

3. **Scope C44 to MVP for Sprint 3**: 3 risk dimensions (financial health, revenue concentration, event frequency), top 20 stocks only, template-based descriptions. This keeps C44 at ~12-14h and fits Sprint 3. Full C44 (5 dimensions, all stocks) can be a v2.

#### Sprint 4 Planning

4. **Defer C46 to Sprint 5**: Sprint 4 cannot fit C36 + C42 + C46. C42 is higher priority (P1, discovery engine). C46 moves to Sprint 5 alongside C47 Phase 1.

5. **Start C42 data investigation early**: Before Sprint 4 begins, verify that FinMind's `get_stock_info()` returns enough fields for screening (ROE, P/E, dividend yield, revenue growth). If not, identify which additional FinMind endpoints are needed and test their rate limits.

#### Sprint 5 Planning

6. **Split C47 into two phases**: Phase 1 (Sprint 5, ~20h) = 8-10 lessons, basic quiz, no progress tracking. Phase 2 (post-Sprint 5, ~15h) = remaining lessons + progress tracking. This reduces risk and gets user feedback earlier.

7. **Design C47 YAML schema before writing content**: Spend 1-2h designing and validating the lesson YAML schema before writing any content. Changing the schema after 10 lessons are written is expensive.

#### Architecture Debt

8. **R1 is now critical**: With C37, C39, C43, and C45 all implemented, financial metric duplication has likely grown. R1 (extract `financial_metrics.py`) should be done **before or during Sprint 3** — it's a force multiplier for C44, C46, and all future features that compute financial ratios.

9. **R5 (YAML migration) is in Sprint 3**: Good — this aligns with C41 (needs `relationships.yaml`) and C46 (needs moat data in YAML). Ensure R5 is done before C46 starts.

#### Risk Summary

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| C44 scope creep in Sprint 3 | High | Sprint 3 overrun | Strict MVP scope: 3 dimensions, top 20 stocks |
| R1 not done before C44/C46 | High | 5th copy of financial logic | Make R1 first task of Sprint 3 |
| C42 FinMind rate limits | High | Screener unusably slow | Verify R3 status; add retry logic |
| Sprint 4 overcapacity | Certain | Features cut or delayed | Defer C46 to Sprint 5 |
| C47 content creation bottleneck | High | 40% of effort is writing | Split into phases; start with 8 lessons |
| C46 moat scoring subjectivity | High | Scores feel arbitrary | Document rubric; use simple 1-5 scale |

---

*Created: 2026-06-16*
*Role: Developer*
*Review cycle: Round 10*
*Confidence level: High (based on Sprint 2 delivery review, codebase analysis, and Round 9 estimate validation)*
*Key change from Round 9: Estimates adjusted post-Sprint 2 based on actual codebase state. C44 estimate increased (10-14h → 17-24h) due to R1 dependency. C42 estimate refined (22-34h → 19-24h) based on proven category_browser pattern. Sprint 4 identified as over-capacity; C46 deferral recommended.*
