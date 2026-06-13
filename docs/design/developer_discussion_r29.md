## 2026-06-13 Developer Estimate — Sprint 14 Feature Candidates

### Implementation Estimates

#### C47 Education Academy
- Service layer: 12-18h (new modules: learning_path.py service, potential extensions to quiz_engine.py/glossary_service.py)
- View layer: 8-12h (new pages: education_academy.py; potential modifications to router.py for navbar entry)
- Data/curation: 8-12h (content: lessons.yaml with 5-8 lessons MVP, each requiring TW stock examples, explanations, quiz questions)
- Integration: 5h
- TOTAL: 33-42h
- Risks: Content creation is 40% of effort (bottleneck); scope creep risk (must cap at 5-8 lessons MVP); progress persistence (session_state ephemeral); card-count constraint for lesson cards
- Dependencies: Soft dependency on glossary_service.py (term definitions) and quiz_engine.py (lesson quizzes); no hard dependencies

#### C40 Mode Toggle
- Service layer: 0h (no new modules needed)
- View layer: 0h (already implemented in _main.py lines 199-208)
- Data/curation: 0h
- Integration: 0h
- TOTAL: 0h (feature already complete as C105)
- Risks: None (feature is complete and working)
- Dependencies: None
- Note: If propagating "simple mode" to ALL pages (peer comparison, financial health, etc.), additional work: ~4-6h to add simple_mode checks to other page render functions.

#### C123 Revenue Geography
- Service layer: 8-12h (new modules: revenue_geography.py service)
- View layer: 2-4h (new sections: modifications to revenue_tree.py or business_card.py revenue section)
- Data/curation: 8-12h (content: manual curation of revenue_geography.yaml for TW stocks; requires research as FinMind lacks this data)
- Integration: 2-4h
- TOTAL: 20-32h
- Risks: 🔴 CRITICAL: No FinMind data source for geographic revenue breakdown; manual curation creates high maintenance burden; content creation for plain-language explanations; data staleness (geographic shifts annually)
- Dependencies: C36 Revenue Tree (complete) — natural extension but not blocked by it

#### C125 Segment Profitability
- Service layer: 4-8h (new modules: extensions to revenue_analyzer.py for segment margin analysis)
- View layer: 2-4h (new sections: modifications to revenue_tree.py for segment margin tab/toggle)
- Data/curation: 4-6h (content: manual curation of segment_margins.yaml for available stocks; research required as FinMind data is inconsistent)
- Integration: 2-4h
- TOTAL: 12-22h
- Risks: 🟡 Data availability: FinMind's financial statements have segment-level data for SOME companies only (large conglomerates); content curation for ~10-15 stocks; maintenance burden as margins change quarterly; card-count constraint (mitigated by extending existing treemap)
- Dependencies: C36 Revenue Tree (complete) — extends it naturally; C123 (Revenue Geography) is NOT a dependency (segment vs geographic)

#### C126 Moat Comparison
- Service layer: 2-4h (new modules: potential extensions to moat_analyzer.py for comparison logic)
- View layer: 6-10h (new sections: tab addition to peer_comparison.py or new comparison page)
- Data/curation: 4-6h (content: plain-language comparison explanations for 10-15 stock pairs; reuse moat_data.yaml which is already comparison-ready)
- Integration: 2-4h
- TOTAL: 14-24h
- Risks: Low risk (all data exists, service layer exists); content creation for comparison explanations; card-count constraint for side-by-side comparison; peer selection logic (can reuse INDUSTRY_BENCHMARKS)
- Dependencies: ✅ C46 complete (Sprint 13b); ✅ moat_data.yaml has 20 stocks with scores; ✅ peer_comparison.py has industry benchmark mapping

### Combined Sprint Options
#### Option A: C47 only (MVP)
- Total: 33-42h
- Feasibility: ⚠️ BORDERLINE — Exceeds typical 26-38h sprint budget; content creation bottleneck makes this risky for a single-feature sprint

#### Option B: C123 + C125 + C126
- Total: 46-78h
- Feasibility: ❌ NOT FEASIBLE — Significantly exceeds sprint budget; C123 is blocked by data availability

#### Option C: C126 + C40 propagation + C47 spike (MVP prototype)
- Total: 28-40h
- Feasibility: ✅ FEASIBLE — Within 26-38h buffer; delivers immediate value, completes existing work, validates education infrastructure

#### Option D: C126 + C125 (limited scope)
- Total: 18-32h
- Feasibility: ✅ FEASIBLE — Within budget; creates "deep analysis" suite but misses education opportunity

### Recommendation
**Select Option C: C126 Moat Comparison + C40 Mode Toggle Propagation + C47 Education Academy Spike**

**Rationale:**
1. **C126 Moat Comparison** (14-24h): Highest feasibility, lowest risk. All infrastructure built (C46 complete, moat_data.yaml ready). Directly supports "benchmark-oriented analysis" core value. View-layer addition only.
2. **C40 Mode Toggle Propagation** (4-6h): Completes existing C105 implementation across all pages. Small effort, high polish impact. Uses proven session_state pattern.
3. **C47 Education Academy Spike** (10-12h): Build 3-5 lesson prototype to validate architecture (lessons.yaml schema, learning_path.py service, education_academy.py page) without over-committing on content creation. Establishes foundation for future expansion.

**Total Effort: 28-40h** — within normal sprint capacity (26-38h buffer), leaving room for bug fixes and technical debt items.

**Defer to Sprint 15+:**
- **C123 Revenue Geography**: Blocked by lack of FinMind data source. Requires either new API or significant manual curation budget.
- **C125 Segment Profitability**: Feasible but lower priority than education features. Pair with C123 in future "Revenue Deep Dive" sprint.
- **C47 Full Academy**: After spike validates architecture in Sprint 14.

This approach balances immediate user value (C126), completion of existing work (C40), and strategic infrastructure investment (C47 spike) while respecting the 40% content creation budget constraint.