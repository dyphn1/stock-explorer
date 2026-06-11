# Challenger Discussion — Round 11

## 2026-06-18 Challenge Process — Round 11 New Feature Evaluation (C48-C54)

---

## Team Preliminary Decision

### Consensus Summary

All three roles (Architect, Designer, Developer) independently converged on the same priority ordering:

**Tier 1 (Sprint 4 — Recommended):**
1. **C51: Sector Heatmap** — Highest impact, introduces market-level data flow, all competitors have it
2. **C48: Company Story Card** — Replaces/enhances C37, low risk, high polish
3. **C53: Social Sharing (Phase 1: URL)** — Lowest effort, leverages existing infrastructure

**Tier 2 (Sprint 5 — Recommended):**
4. **C49: Daily Market Pulse** — Creates daily engagement loop, shares data pipeline with C51
5. **C52: Quiz Mode** — Natural companion to C47 education, content creation is the bottleneck
6. **C53: Social Sharing (Phase 2: Image)** — HTML-to-image is hard but valuable for growth

**Tier 3 (Sprint 5+ — Deferred):**
7. **C50: Learning Progress Tracker** — Requires persistence layer + user identity (not feasible)
8. **C54: Video/Audio Explanation** — Requires LLM integration + TTS pipeline (not feasible)

### Role Opinions Summary

| Role | Top Priority | Key Concern | Direction Preferred |
|------|-------------|-------------|-------------------|
| **Architect** | C51 (Sector Heatmap) | Market-level data infrastructure doesn't exist; R3 is critical enabler | Direction A: Quick Wins + Visual Impact |
| **Designer** | C48 (replace C37) + C49 (Daily Pulse) | Page overload if C48 added alongside C37; daily retention is #1 gap | Direction A: Story First |
| **Developer** | C51 + C48 + C53(Phase 1) | R3 blocker for C51; content creation bottleneck for C52 | Direction A: Quick Wins + Visual Impact |

### Total Effort Estimate
- Sprint 4 features: 24-33h (C51 12-16h + C48 10-14h + C53-1 2-3h)
- Sprint 5 features: 26-47h (C49 14-20h + C52 12-18h + C53-2 5-9h)
- Deferred: 46-69h (C50 16-24h + C54 30-45h)
- **Content creation additional**: 20-35h (quiz questions + story elements)

---

## Round 1: Feature Direction Challenge

### Challenger Questions: Feature Direction

#### Challenge 1.1: C48 replaces C37 — is this the right call?
**Context**: Designer recommends C48 *replaces* C37 to avoid page overload. Architect says C48 is feasible but needs "positioning clarity." Developer notes C48 rendering would push business_card.py past 550 lines.

**Team Response**:
- **Architect**: C48 should REPLACE C37, not be added alongside. Both serve the same "summary" purpose. C48 is the visual-first evolution of C37. Adding both creates redundancy and page bloat. The replacement approach is architecturally cleaner — one summary section, not two.
- **Designer**: C48 should REPLACE C37. The current C37 uses a standard blue info card (violating D-016 hero card spec). C48 uses the orange/amber hero card style that was always intended for C37. This simultaneously implements C48 AND fixes D-016. Two birds, one stone.
- **Developer**: Replacement is cleaner. We remove the C37 code path (section at lines 140-152 in business_card.py) and replace with C48's visual story card. Net code change is small (+~50 lines for visual metrics layout, -~15 lines from C37 removal). Must ensure `generate_key_takeaways()` function calls are removed.

**✅ ACCEPTED**: C48 replaces C37. This resolves page overload risk AND fixes D-016.

#### Challenge 1.2: Market-level data — is this the right architectural direction?
**Context**: C49 and C51 both need market-level data aggregation. The current architecture is entirely single-stock. Adding a `market_data.py` service is a new architectural pattern.

**Team Response**:
- **Architect**: This is the most important architectural decision in this batch. The `market_data.py` service introduces a new data flow pattern: `market → aggregate → visualize`. This is fundamentally different from the existing `stock_id → data dict` pattern. It's a natural and necessary evolution — the product can't stay single-stock forever. The key design decisions are: (a) batch API calls (R3 dependency), (b) caching strategy (market data changes daily, not per-interaction), (c) sector classification mapping (YAML).
- **Designer**: From a UX perspective, market-level views are table stakes. Every competitor has them. Users who come from StockEdge or Moomoo expect sector heatmaps. The question isn't whether to add this — it's how to make it educational rather than just data-dense. The "why" plain-language explanations are the differentiator.
- **Developer**: The `market_data.py` module is the right approach. Shared infrastructure between C49 and C51. The estimated 3-4h for this module is realistic — it's a new file with batch-fetch + aggregate functions. The risky part is the FinMind API market-level endpoints that haven't been tested. Need to validate data availability before committing to the full feature.

**✅ ACCEPTED**: `market_data.py` is the right architectural direction. Proceed with shared infrastructure for C49 + C51.

#### Challenge 1.3: C52 Quiz — is content creation effort justified?
**Context**: C52 engineering is 12-18h, but content creation is 10-15h for 50-100 questions. Is this the best use of content creation time vs. other features?

**Team Response**:
- **Architect**: Quiz mode is architecturally simple (YAML question bank + session-state quiz flow). The content creation effort is real but spread over time — you don't need 100 questions at launch. 20 questions for MVP is sufficient. The feature's value is in the *mechanism* (quiz as active learning), not the volume.
- **Designer**: Quizzes are the missing piece for the education loop. C47 teaches, C52 tests, C50 tracks. Without C52, C47 is passive reading. I recommend starting with 10-20 high-quality questions rather than 100 mediocre ones. Quality over quantity.
- **Developer**: Agree with starting small. 20 questions × 15 min each = 5h content creation, not 10-15h. The engineering (quiz state machine + rendering) is the more predictable cost. Phase 2 (dynamic question generation from real data) is where the real engineering challenge lies, but that's Sprint 5+.

**✅ ACCEPTED**: C52 should launch with 20-question MVP, expand over time. Content creation scoped to 5h for MVP.

---

## Round 2: Priority Challenge

### Challenger Questions: Priority

#### Challenge 2.1: C51 vs C48 — which is truly higher priority?
**Context**: Architect ranks C51 first, Designer ranks C48 first. The Developer agrees with Architect. Is C51 really higher priority than C48?

**Team Response**:
- **Architect**: C51 is higher priority because it introduces new infrastructure (`market_data.py`) that takes longer to validate. C48 is composition of existing features — it can be built quickly once the infrastructure is in place. Also, C51 is the feature most competitors have and our product lacks. C48 replaces an existing feature (C37), so it's an enhancement, not a gap.
- **Designer**: I rank C48 first because it directly fixes D-016 (missing hero card style) and improves the most-viewed page (business card). But I agree C51 should be built in the same sprint. The ordering within Sprint 4 doesn't matter — what matters is they both ship.
- **Developer**: C51 first because of R3 dependency. If R3 isn't done, C51 is blocked. C48 depends on D16, which is a Sprint 3 task. In practice, C51 and C48 can be developed in parallel if R3 and D16 are done.

**✅ ACCEPTED**: C51 is first priority (introduces new infrastructure), C48 is second (replaces existing feature). Both ship in Sprint 4. Order within sprint is flexible.

#### Challenge 2.2: C49 (Daily Pulse) for Sprint 5 — correct timing?
**Context**: C49 shares infrastructure with C51. Some might argue it should ship alongside C51 in Sprint 4. Is Sprint 5 the right call?

**Team Response**:
- **Architect**: Sprint 5 is correct. C49 adds scheduling complexity (daily refresh), market commentary generation, and a new page — on top of the `market_data.py` that C51 builds. Trying to do both C51 and C49 in Sprint 4 would overload the sprint (C51 12-16h + C49 14-20h + C48 10-14h = 36-50h, leaving no buffer). C49 benefits from C51's stable `market_data.py`.
- **Designer**: The daily pulse is a retention feature, not a core analysis feature. It's important but not urgent. Sprint 5 gives time to design the page properly and test the daily refresh mechanism.
- **Developer**: Agree with Sprint 5. C49 reuses `market_data.py` from C51, so the data layer is ready. The remaining work (page layout, commentary templates, caching strategy) is 14-20h — a full sprint feature.

**✅ ACCEPTED**: C49 in Sprint 5 is correct. C51 must ship first to provide the data layer.

#### Challenge 2.3: C53 Phase 1 (URL sharing) — worth doing?
**Context**: URL sharing is the simplest form of social sharing — just a link. Does this provide meaningful value?

**Team Response**:
- **Architect**: URL sharing alone is low value. Users can already copy the browser URL. The value of C53 is in the shareable IMAGE card — a visual representation of the company that's worth sharing. However, image generation is hard (HTML-to-image fragility). Phase 1 URL sharing is a good way to validate the feature concept before investing in image generation.
- **Designer**: URL sharing alone adds a "copy link" button, which is a UX improvement (users don't have to manually select the URL). But the real value is the image card. I recommend doing both Phase 1 (URL) and Phase 2 (image) in sequence — URL in Sprint 4 as a quick win, image in Sprint 5 as the real feature.
- **Developer**: URL sharing is 2-3h and leverages existing `url_sync.py`. It's a no-brainer quick win. Image generation (5-9h) is the real effort and should be Phase 2.

**✅ ACCEPTED**: C53 Phase 1 (URL) in Sprint 4 as quick win; Phase 2 (image) in Sprint 5.

---

## Round 3: Goal Alignment Challenge

### Challenger Questions: Goal Alignment

#### Challenge 3.1: Does this plan align with the "historian" positioning?
**Context**: Stock Explorer's core positioning is "historian, not a stock picker." Do market-level features (C49, C51) align with this positioning, or do they turn Stock Explorer into a trading tool?

**Team Response**:
- **Architect**: Market-level data aligns with "historian" if used to explain, not to pick. The historian explains what happened in the market, not what to buy. C49 should say "Today, semiconductors rose 3% because of TSMC earnings" — factual, educational. C51 should show sector performance with plain-language explanations — benchmark-oriented, not predictive.
- **Designer**: This is a critical alignment concern. The historian positioning means we must be careful with the framing of C49 and C51. They should be "market education tools" not "market timing tools." The tone should always be factual: "This is what happened" not "This is what will happen." I recommend explicit tone guidelines for these features.
- **Developer**: The data doesn't care about positioning — it's the presentation that matters. C49's templates should use "過去發生" (happened in the past) language. C51's sector labels should explain "why" not "what's hot." The architecture supports this — we control the templates and descriptions.

**✅ ACCEPTED**: C49 and C51 align with historian positioning IF tone guidelines are enforced. **Action item**: Add tone guidelines for market-level features: use "過去發生" language, factual not predictive, explain not recommend.

#### Challenge 3.2: Are we spreading too thin?
**Context**: Sprint 4 plan includes C51 (12-16h) + C48 (10-14h) + C53-1 (2-3h) = 24-33h. Sprint 3 is already full (C44, C41, C38, R1, D16). Are we trying to do too much?

**Team Response**:
- **Architect**: Sprint 4 is at 24-33h out of ~40h capacity. This leaves 7-16h for bug fixes, R3 (if not done in Sprint 3), and buffer. This is a reasonable load. The key risk is R3 — if R3 isn't done in Sprint 3, it becomes Sprint 4's first task, consuming 2-3h of the buffer. Still manageable.
- **Designer**: I'm comfortable with Sprint 4's load. The three features (C51, C48, C53-1) don't touch the same pages (C51 is a new page, C48 replaces C37, C53 is a button), so there's minimal integration risk. My concern is the design system — if D-016 hero card style isn't defined before C48 implementation starts, we'll get inconsistencies.
- **Developer**: Sprint 4 is manageable IF Sprint 3 delivers R3, R1, and D16 as planned. If any of those slip, Sprint 4's features are at risk. Recommendation: treat R3 and D16 as hard prerequisites for Sprint 4. If they're not done, defer C51 to Sprint 5 and keep C48 (lower dependency risk).

**✅ ACCEPTED**: Sprint 4 load is manageable. **Action item**: Define R3 and D16 as hard prerequisites for Sprint 4. If they slip, defer C51 and keep C48 + C53-1.

#### Challenge 3.3: C50 and C54 — should they remain in the backlog or be explicitly excluded?
**Context**: Both C50 and C54 have critical infrastructure blockers (persistence layer, LLM integration). They're deferred to Sprint 5+. Should they stay in the backlog as future features or be explicitly excluded from the near-term roadmap?

**Team Response**:
- **Architect**: They should stay in the backlog as P2 features with explicit blocker documentation. C50 blocks on D22 (persistence layer) and C54 blocks on R7 (LLM abstraction). When those infrastructure projects are scheduled, C50 and C54 become feasible. No point excluding them — they're valuable features, just not feasible yet.
- **Designer**: Agree. The education features (C50, C54) are the long-term differentiator. They should stay visible in the backlog so the team remembers they're coming. But they should be clearly marked as "infrastructure-dependent" so no one tries to build them prematurely.
- **Developer**: Keep them in backlog with clear blocker labels. A lightweight version of C50 ("pages visited" tracker using `session_state`) could be built without persistence infrastructure, but it provides minimal value. Better to wait.

**✅ ACCEPTED**: C50 and C54 remain in backlog as infrastructure-dependent features. No lightweight shortcuts.

---

## Final PM Decision (Challenger ✅ Confirmed)

### Sprint Plan

| Sprint | Features | Est. Hours | Prerequisites | Competitor Insight Addressed |
|--------|----------|------------|---------------|------------------------------|
| **3** (in progress) | C44 + C41 + C38 + R1 + D16 | 33-50h | — | #1 Story first, #3 Adaptive |
| **4** | C51 + C48 + C53(Phase 1) | 24-33h | R3, D16 | #4 Visual-first, #6 Mobile awareness |
| **5** | C49 + C52 + C53(Phase 2) | 33-47h | C51's market_data.py | #3 Daily engagement, #5 Assessment |
| **5+** | C50 + C54 | 46-69h | D22, R7 | #2 Structured education |

### Feature Directions Confirmed

**Direction A ("Quick Wins + Visual Impact") adopted with modifications:**

1. **C48 replaces C37** (not alongside) — fixes D-016 hero card style simultaneously
2. **C51 first** in Sprint 4 — introduces `market_data.py` for shared infrastructure
3. **C49 after C51** — reuses `market_data.py`, adds scheduling complexity
4. **C52 scoped to 20-question MVP** — reduces content creation from 10-15h to 5h
5. **C53 in two phases** — URL first (2-3h), image second (5-9h)
6. **C50 and C54 deferred** — remain in backlog with infrastructure blockers documented

### New Tone Guidelines for Market-Level Features
- Use "過去發生" / "歷史證據" / "觀察指標" language (same as C44 risk analysis)
- Never "可能發生" / "預測" / "建議買入"
- Frame as "market education" not "market timing"
- All market commentary must cite specific data sources

### New Architecture Decisions
- **market_data.py**: New service for market-level data aggregation (shared by C49, C51)
- **story_composer.py**: New service for composing company stories from existing data (C48)
- **export_service.py**: New utility for HTML-to-image rendering (shared by C48, C53)
- **sector_mapping.yaml**: New YAML data file for sector classifications
- **quiz_questions.yaml**: New YAML data file for quiz question bank

### Items Added to Pending Review (for Daniel)
None — all decisions are within team authority. Existing pending items remain:
1. C34 vs C46 priority for Sprint 5
2. C47 Phase 1 scope (5 vs 10 lessons)
3. Business Card Page IA: "above the fold" definition

### New Architecture Debt from This Discussion
- D23: Tone guidelines needed for market-level features (C49, C51) — P2
- D24: business_card.py will grow further with C48 — consider extracting to sub-directory — P2

---

*Challenger confirmed alignment after 3 rounds of challenge. All roles agree on feature directions, priorities, and deferrals. No contradictions remain.*
*Created: 2026-06-18*
*Maintainer: Product Manager (with Challenger)*
