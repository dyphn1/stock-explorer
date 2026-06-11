## Friday, June 19, 2026 Technical Analysis — Round 14 Discussion

### Competitive Landscape Summary

Based on the Round 14 competitor research (8 new competitors analyzed) and cumulative insights across all 14 rounds, Stock Explorer's positioning as a "Beginner Education (Historian)" tool continues to be validated while specific execution gaps become clearer. The Round 14 research highlights:

**Key Competitive Insights from Round 14:**

1. **Dhan's "Read More, Trade Less"** — Stock Explorer's "historian, not stock picker" positioning is no longer unique globally. Dhan (India) has staked its entire brand on the same philosophy. This validates the positioning but also means Stock Explorer must execute it better than a well-funded Indian competitor. Dhan's specific patterns worth adopting:
   - "Why This Matters" conclusion section on every analysis
   - "Read Time" / "Depth" labels on all content
   - Reading-first, trading-second navigation hierarchy

2. **Atom Finance's "Company Narratives"** — AI-generated plain-language company summaries are the closest global analog to Stock Explorer's business card page. The fact that a US competitor is doing essentially the same thing validates the approach urgently — we need to ship C48 before this becomes table stakes internationally.

3. **Groww's "Whys" inline explanations** — Every financial metric on Groww has an AI-generated hover explanation. Our planned C33 (Glossary) and C56 (Explain This Metric) must reach this level of integration (inline, not separated) to remain competitive.

4. **Toss Securities' "Stock Stories"** — The 30-second stock explanation concept appears across multiple Asian competitors (Toss, Stake, Atom Finance). This is C48's core concept and it is fully validated. Effort should be at the low end (8-12h).

5. **Moomoo's "Market Heatmap with Education"** — Sector heatmaps with plain-language explanations are now a proven pattern. C51's technical approach (Plotly treemap) is sound but must include narrative explanations to differentiate.

**Competitor Validation Matrix for Sprint 4 Features:**

| Sprint 4 Feature | Competitors with Equivalent | Validation Level | Risk if Delayed |
|---|---|---|---|
| C38 Compare Stories | Atom Finance (Compare), Seeking Alpha (Side-by-side) | 🟡 Medium — structured comparison exists but narrative comparison is rare | Medium — no TW competitor has narrative comparison yet |
| C51 Sector Heatmap | StockEdge, Moomoo, 永豐金證券 | 🔴 High — proven pattern across 4+ competitors in 3 markets | Medium — we have unique "with education" angle |
| C48 Company Story Card | Dhan, Atom Finance, Toss, Stake | 🔴 High — core concept validated across 4 competitors in 4 markets | 🔴 High — Atom Finance is doing exactly this |
| C53-1 Social Sharing URL | TradingView, Plotch.ai, Stake | 🟡 Medium — sharing is table stakes but our narrative cards are unique | Low — quick win, no dependency |
| R3 Batch API | (Performance infrastructure) | N/A — internal optimization | Low — enables C51 |
| D16 Split analogy_engine.py | (Technical debt) | N/A — unblocks C48 | 🔴 High — C48's story_composer.py depends on stable interfaces |

---

### Direction A: C48 Company Story Card — 30-Second Visual Summary (Sprint 4)

**Description**: A hero card at the top of each company page showing the one-liner, 3 most notable metrics with plain-language explanations, and a rotating "Did You Know?" fact. This is the "ten-second test" made real — a beginner can understand the company in 30 seconds, then choose to dive deeper.

**Technical Approach**:

```
┌─────────────────────────────────────────────────────┐
│  Data Layer (unchanged)                              │
│  FinMind API → existing data dict                    │
├─────────────────────────────────────────────────────┤
│  Service Layer (new)                                 │
│  src/services/story_composer.py                      │
│  - compose_story_card(data_dict) -> StoryCard        │
│  - select_top_metrics(data_dict, n=3) -> list        │
│  - get_fact(stock_id, rotation_key) -> str           │
│  Imports from: analogy_engine.py,                    │
│    company_facts.py, financial_metrics.py            │
│  NOTE: D16 (split analogy_engine.py) must complete   │
│  first to stabilize the import interface             │
├─────────────────────────────────────────────────────┤
│  Router Layer (unchanged)                            │
│  story_composer as optional addition to data dict    │
│  or separate service call from page                  │
├─────────────────────────────────────────────────────┤
│  View Layer                                          │
│  src/pages/business_card/__init__.py or _main.py     │
│  - render_story_card(story: StoryCard)               │
│  - Uses existing _info_card() / _白话_card() for     │
│    metric rendering                                  │
│  - PPT-style card layout (custom CSS)                │
└─────────────────────────────────────────────────────┘
```

**Option A1: Thin Service + Thin View (Recommended)**
- `story_composer.py` is a pure function (data_dict → StoryCard dict)
- View renders using existing UI components
- **Pros**: Clean separation, testable, follows existing patterns exactly
- **Cons**: Limited interactivity (static card)
- **Effort**: 10-12h (8h service + 4h view)

**Option A2: Rich Service + Interactive View**
- `story_composer.py` includes metric selection algorithm (what's "most notable"?)
- View includes expandable sections, hover tooltips, "Tell Me More" buttons
- **Pros**: Richer experience, more engaging, closer to Dhan/Atom Finance implementations
- **Cons**: More complex, adds session state for rotation/interaction, higher risk
- **Effort**: 14-18h

**Recommendation**: **Option A1** — Ship the thin version in Sprint 4. The priority is getting C48 out before international competitors make it table stakes. Option A2 can be a Sprint 5 enhancement after D16 stabilizes the import interfaces and D24's extraction makes the view layer more manageable.

**Dependencies**: D16 (must complete first — story_composer imports from analogy_engine.py), D24 (already done ✅)

---

### Direction B: C51 Sector Heatmap — Visual Market Overview (Sprint 4)

**Description**: A visual, color-coded grid of TW sectors showing relative performance. Click on a sector → see top companies with plain-language explanations. This is Stock Explorer's first market-level feature (not company-level), which introduces architectural novelty.

**Technical Approach**:

```
┌─────────────────────────────────────────────────────┐
│  Data Layer (new pattern)                            │
│  src/data/finmind_client.py                          │
│  - get_sector_performance() -> DataFrame             │
│  - get_sector_companies(sector_id) -> list           │
│  NOTE: This is a new DATA FLOW pattern — market-wide │
│  → aggregate → visualize (not stock_id → data dict) │
├─────────────────────────────────────────────────────┤
│  Service Layer (new)                                 │
│  src/services/market_data.py (addresses D25)         │
│  - get_sector_heatmap_data() -> HeatmapData          │
│  - get_sector_story(sector_id) -> SectorStory        │
│  - get_top_companies(sector_id, n=5) -> list         │
│  Imports from: analogy_engine.py, sector data YAML   │
├─────────────────────────────────────────────────────┤
│  Router Layer (new pattern)                          │
│  market-level page bypasses stock_id pattern         │
│  Separate router flow: sector_page.py directly calls │
│  market_data.py (no stock_id → data dict)            │
├─────────────────────────────────────────────────────┤
│  View Layer (new page)                               │
│  src/pages/sector_page.py                            │
│  - Plotly treemap or heatmap visualization           │
│  - Click-through to sector detail with narratives    │
│  - Plain-language sector explanations                │
└─────────────────────────────────────────────────────┘
```

**Option B1: Plotly Treemap (Recommended)**
- Use `plotly.express.treemap` for the visualization
- Color by performance (green/red), size by market cap
- **Pros**: Fewer lines than `go.Sunburst`, good mobile responsiveness, click-through support
- **Cons**: Less visually distinctive than a custom heatmap
- **Effort**: 12-14h

**Option B2: Plotly Heatmap Grid**
- Custom heatmap with sector labels
- More "at a glance" readable but less information-dense
- **Pros**: Closer to StockEdge/Moomoo patterns, visually cleaner
- **Cons**: Harder to show within-sector company breakdown
- **Effort**: 14-16h

**Option C: Custom HTML Grid**
- Pure HTML/CSS grid with embedded sparklines
- Maximum visual control but maximum maintenance burden
- **Pros**: Unique look, full PPT-style design integration
- **Cons**: 20-25h effort, hard to maintain, breaks with data changes
- **Effort**: 20-25h (NOT recommended for Sprint 4)

**Recommendation**: **Option B1 (Plotly Treemap)** — It's the fastest path to a working sector heatmap that differentiates through plain-language explanations (which StockEdge and Moomoo lack). The narrative layer (SectorStory) is where Stock Explorer's value lies, not the visualization itself.

**Critical prerequisite**: R3 (Batch API) must complete before C51 to avoid sequential API calls for 200+ stocks across sectors.

**Dependencies**: R3 (Batch API minimal), D25 (market_data.py — can be created as part of C51), new sector data YAML

---

### Direction C: C38 Compare Stories Phase 1 — Side-by-Side Narrative Comparison (Sprint 3/4)

**Description**: A new tab on the peer comparison page showing two companies' narratives side-by-side. Not just metrics comparison ("TSMC ROE: 25%, UMC ROE: 15%") but story comparison ("TSMC makes cutting-edge chips for Apple; UMC makes mature chips for IoT devices"). Phase 1 uses structured data only (no LLM).

**Technical Approach**:

```
┌─────────────────────────────────────────────────────┐
│  Data Layer (unchanged)                              │
│  FinMind API → existing _get_benchmark_data()       │
│  Already loads two companies' data                   │
├─────────────────────────────────────────────────────┤
│  Service Layer (new)                                 │
│  src/services/narrative_comparator.py                │
│  - compare_stories(stock_a_data, stock_b_data)       │
│    -> ComparisonResult                               │
│  - compare_dimension(dim_name, a_val, b_val) -> str  │
│  - generate_narrative_diff(metric, a_val, b_val,     │
│    analogy_a, analogy_b) -> str                      │
│  Imports from: analogy_engine.py, financial_metrics  │
├─────────────────────────────────────────────────────┤
│  Router Layer (unchanged)                            │
│  peer_comparison.py already loads two stocks         │
│  narrative_comparator receives data from existing    │
│  _get_benchmark_data() flow                          │
├─────────────────────────────────────────────────────┤
│  View Layer (extension)                              │
│  src/pages/peer_comparison.py (new tab)              │
│  - "故事比較" tab next to "指標比較" tab             │
│  - Side-by-side narrative cards                      │
│  - Plain-language comparison bullet points           │
└─────────────────────────────────────────────────────┘
```

**Option C1: Narrative卡片 Side-by-Side (Recommended)**
- Two columns, each showing a company's one-liner, key analogies, and a "story summary" generated from templates
- Bottom section: dimension-by-dimension comparison (Profitability, Growth, etc.) with narrative differences
- **Pros**: Clean, follows existing card patterns, implementable in 10-12h
- **Cons**: May feel like "reading two business cards side by side" rather than true comparison narrative

**Option C2: Single Narrative Comparison**
- One integrated narrative: "TSMC and UMC are both semiconductor foundries, but their stories differ in three key ways..."
- Uses template-based generation with both companies' data
- **Pros**: True narrative comparison, more valuable to users, closer to Stocksera/Seeking Alpha vision
- **Cons**: Template complexity grows combinatorially, harder to make readable, 14-16h

**Option C3: Structured Comparison with Narrative Annotations**
- Structured metric comparison (existing) + narrative annotations per metric
- Each dimension gets: metric comparison (numbers) + 1-sentence narrative explanation
- **Pros**: Leverages existing structure, adds narrative layer incrementally, lowest risk
- **Cons**: Less visually compelling, more cluttered

**Recommendation**: **Option C1** for Phase 1. It's independently valuable, low risk, and creates the rendering infrastructure that Option C2 can later enhance. The key insight from competitor research is that NO TW competitor has narrative comparison at all — even side-by-side cards are a differentiator. Option C2 (true narrative comparison) should be Phase 2 (Sprint 6+), possibly with LLM integration.

**Dependencies**: D16 (imports analogy_engine.py), R1 (financial_metrics.py — done ✅)

---

### Sprint 4 Architecture Sequence Assessment

The current Sprint 4 plan is: **D16 → R3 → C38 → C51 → C48 → C53-1**

**Assessment**: ✅ **Architecturally sound**, with specific observations:

| Step | Architectural Risk | Notes |
|------|-------------------|-------|
| **D16** (Split analogy_engine.py) | 🟡 Medium | Must complete before C48 and C38. 850 lines across 6 responsibilities. R1 unblocks it. |
| **R3** (Batch API) | 🟢 Low | 1-2h, isolated change. Enables C51 performance. |
| **C38** (Compare Stories P1) | 🟡 Medium | Depends on D16. Creates `narrative_comparator.py`. Clean service layer addition. |
| **C51** (Sector Heatmap) | 🟡 Medium | Depends on R3. Creates `market_data.py` (D25). New router flow (market-level, not stock-level). |
| **C48** (Company Story Card) | 🟢 Low | Depends on D16 + D24. Creates `story_composer.py`. Pure service + thin view. |
| **C53-1** (Social Sharing URL) | 🟢 Low | Quick win. Streamlit's built-in URL params + minimal view layer change. |

**No circular dependencies detected.** The critical path is: D16 → C38 and D16 → C48. R3 → C51.

**Recommended sequencing adjustment**: The current plan lists C38 before C51 before C48. However, C48 has the highest competitive urgency (Atom Finance is doing it now) and lowest technical risk. Consider: D16 → R3 → **C48** → C51 → C38 → C53-1. This ships the highest-urgency feature (C48) earlier without breaking any dependency constraints.

---

### New Architecture Debt Identified

**D34: `market_data.py` creates a new architectural pattern (market-level data flow)**
- **Severity**: 🟡 Medium
- **Description**: All existing service-layer code assumes a `stock_id → data dict` pattern. C51's `market_data.py` introduces a market-wide → aggregate → visualize flow. This is architecturally distinct and needs clear separation from the stock-level flow.
- **Recommended Action**: Document the two data flow patterns in `docs/architecture/architectural_patterns.md`. Ensure market-level services never import from stock-level services (and vice versa) to maintain clean separation.

**D35: `story_composer.py` depends on post-D16 import interfaces**
- **Severity**: 🟡 Medium (becomes 🔴 High if D16 slips)
- **Description**: `story_composer.py` will import analogy functions from the post-split `analogy_engine.py`. If D16 slips or the split changes interfaces, C48 is blocked.
- **Recommended Action**: Define the public API surface for `analogy_engine.py` early in D16. Write down what `story_composer.py` needs from each split module before starting the split. This way, D16 can split with C48's requirements in mind.

**D36: `sector_page.py` is a new page type that bypasses `_router_base.py`**
- **Severity**: 🟢 Low
- **Description**: The sector page doesn't follow the `stock_id → data dict → page render` pattern. It's a standalone page with its own data flow.
- **Recommended Action**: Acceptable for now. If more market-level pages are added (e.g., C49 Daily Market Pulse), consider extracting a `market_page_base.py` to share the market-level data loading pattern.

---

### Competitor Gap Analysis: What's Still Missing

After 14 rounds of competitor research, the following gaps remain unaddressed by Stock Explorer:

| Gap | Competitors with It | Our Status | Priority | Suggested Action |
|-----|-------------------|-----------|----------|-----------------|
| **"Why This Matters" conclusions** | Dhan, Finimize, TipRanks | ❌ Not built | P1 | Add to Sprint 5 for business_card.py |
| **Read Time / Depth labels** | Dhan, Trading 212 | ❌ Not built | P2 | Quick addition to existing UI |
| **Inline metric explanations ("Whys")** | Groww, Robinhood, 永豐金證券 | ⚠️ C56 planned (Sprint 5) | P1 | Accelerate C56; make inline, not separate |
| **Daily engagement loop** | Finimize, TradingView, Kabu.com | ❌ Not built | P1 | C49 or C64 — create daily reason to return |
| **Portfolio simulation** | Groww (Vola), Investopedia, Webull | ❌ Not built | P2 | Consider for Sprint 6+ |
| **Super Investor tracking** | Dhan, TipRanks | ❌ Not built | P2 | Interesting historian angle: "What smart investors read" |
| **Company Filing Explorer** | Atom Finance | ❌ Not built | P2 | C65 — high effort (16-24h) but unique differentiator |
| **Risk Profile Quiz** | Smart FOLIO, Syfe, 玉山證券 | ❌ Not built | P1 | C66 — low effort (6-10h), enhances C58 |

---

### Recommendation

For Round 14 discussion, the team should prioritize **Direction A: C48 Company Story Card** as the primary Sprint 4 feature after D16/R3. The competitive analysis shows that Dhan, Atom Finance, Toss Securities, and Stake are all converging on the same "30-second stock story" concept. Stock Explorer must ship C48 in Sprint 4 (not later) to maintain differentiation. Direction B (C51 Sector Heatmap) should follow as the market-level expansion. Direction C (C38 Compare Stories) can complete in parallel if capacity allows.

**Suggested Discussion Points:**
1. **Prioritize C48 over C51**: Ship the Company Story Card first (highest competitive urgency, lowest technical risk after D16). Sector Heatmap creates new architecture (market_data.py) and needs more careful design.
2. **Define D16 public API before splitting**: Document what story_composer.py and narrative_comparator.py need from analogy_engine.py before splitting. This prevents interface mismatches.
3. **Start C56 content creation now**: The Groww "Whys" feature proves that inline metric explanations must be comprehensive. C56 (Sprint 5) needs 3-5h of content creation for metric explanations. Starting now spreads the load.
4. **Add "Why This Matters" section**: Dhan makes this look essential. It's a low-effort addition (2-3h) to the business card page that significantly improves the user experience.
5. **Consider C64 (Daily Market Quiz) for Sprint 5**: Kabu.com and Toss Securities prove that daily gamified engagement drives retention. It's low effort (8-12h) and creates a daily engagement loop that Stock Explorer currently lacks.

---
*Created: 2026-06-19*
*Maintainer: System Architect*
*Next review: After Sprint 4 feature implementation (C48 + C51)*
