# Competitor Research — Round 18

> **Date**: 2026-06-12
> **Author**: PM (synthesized from Rounds 1-17 + Sprint 6 delivery assessment)
> **Purpose**: Assess competitive landscape after Sprint 6 delivery (C83, C85, C02)

---

## Competitive Position After Sprint 6

Sprint 6 delivered C83 (Investment Memo), C85 (Financial Wellness Check), C02 (Notification Center). These address 3 major competitive gaps:

| Gap | Previous Status | After Sprint 6 |
|-----|---------------|----------------|
| **Notifications** | ❌ Not built | ✅ C02 delivered — severity badges, per-stock grouping, settings |
| **Structured Reflection Tools** | ❌ Not built | ✅ C83 Investment Memo — unique in TW market |
| **Financial Wellness / Behavioral Finance** | ❌ Not built | ✅ C85 quiz — no TW or international competitor has this |

## Remaining Competitive Gaps (Not Addressed by Sprint 6)

Based on Rounds 1-17 research (12+ competitors) + current landscape:

| Feature | Competitors Have | Our Status | Priority | Effort |
|---------|-----------------|------------|----------|--------|
| **C42 Stock Screener** | 財報狗 (#1 feature), Stockopedia, Simply Wall St | ❌ Not built | P1 | 16-24h |
| **C36 Visual Revenue Tree** | Public.com, Koyfin | ❌ Pie chart only | P2 | 10-14h |
| **C37 Key Takeaways** | Seeking Alpha, Public.com | ✅ Partially (C37 exists) | — | Done |
| **C39 Recent Changes** | Koyfin, Finary | ✅ Partially (C39 exists) | — | Done |
| **C34 Story Timeline** | Stocksera (unique diff) | ❌ Not built | P2 | 18-24h |
| **C40 Beginner/Expert Toggle** | Sharesies, NerdWallet | ❌ Not built | P2 | 10-14h |
| **C47 Learning Path** | CMoney, Investopedia Academy | ❌ Not built | P2 | 20-30h |
| **Market Thermometer** | WantGoo, CMoney | ❌ Not built | P1 | 10-12h |

## Table Stakes vs Differentiators (Updated 2026)

**Becoming Table Stakes** (expected in any stock tool):
- ✅ Real-time price display (we have via FinMind)
- ✅ Basic financial metrics (we have)
- ✅ Charts (revenue, valuation — we have)
- ❌ Notifications (C02 now delivered — parity achieved)
- ❌ Watchlist (we have basic, but no health dashboard)

**Our Sustained Differentiators**:
- Plain-language explanations (unique in TW market)
- PPT-style presentation (unique design approach)
- Point-to-point group structure (more detailed than competitors)
- Investment Memo (C83 — no competitor has structured reflection tool)
- Financial Wellness Check (C85 — no competitor has behavioral finance quiz)
- Snowflake Health Visualization (C43 — unique 5-dimension with benchmark)

## Key Competitor Insights (From Rounds 13-17)

### Emerging Trend: Narrative-First Platforms
Stocksera, Public.com, and Seeking Alpha are all adding narrative features. Stocksera has a dedicated "Story" tab per stock. This validates our "historian" positioning — the market is moving toward narrative.

### Emerging Trend: AI-Powered Education
Multiple platforms (Koyfin metric descriptions, Simply Wall St infographics, Investopedia Academy) are investing in AI-generated explanations. Our analogy engine is a strong foundation but needs LLM integration (D5 debt) to stay competitive.

### Emerging Trend: Progressive Disclosure as Standard
Sharesies (complexity levels), NerdWallet (simple view), Robinhood (minimalist default) — progressive disclosure is becoming standard. Our "progressive drill-down" principle needs explicit UI support (C40 Beginner/Expert toggle).

## Sprint 7+ Feature Priorities (Competitive Perspective)

1. **C84 (Market Event Case Study)** — No competitor has interactive historical events. Unique historian differentiator. **Priority: Sprint 7 main feature.**

2. **C42 (Stock Screener / Discovery Engine)** — 財報狗's #1 feature. Needed for user acquisition. **Priority: Sprint 8 (after C84).**

3. **C93 (Dividend Income Calendar)** — Conditional on positioning as intermediate feature. **Priority: Sprint 8.**

4. **C94 (Earnings Story)** — Conditional on historical framing + disclaimers. M5 engine already detects events. **Priority: Sprint 8.**

---

*Note: Full competitor profiles for 12+ platforms are documented in docs/research/competitor_research.md (Rounds 1-13).*
