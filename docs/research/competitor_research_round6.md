# Stock Explorer Competitor Research Report — Round 6

**Date:** 2026-06-12
**Author:** QA Engineer (Hermes) — PM-synthesized (QA subagent timed out on web search)
**Round:** 6 — Gap Analysis & Competitive Threat Update
**Previous Rounds:** R1-2 (2026-06-09): 9 TW platforms. R3 (2026-06-10): 13 international. R4 (2026-06-11): 8 new angles. R5 (2026-06-12): 8 emerging trends.

---

## Note

The QA Engineer subagent timed out on web search (600s limit). This report synthesizes existing competitor data from Rounds 1-5 to identify any remaining gaps. No new web research was conducted this round.

---

## Competitive Landscape Summary (Rounds 1-5 Cumulative)

### High Threat Competitors
| Competitor | Threat | Key Overlap with Stock Explorer |
|---|---|---|
| **StockStory** (stockstory.ai) | 🔴 High | AI-generated company narratives + TW coverage + "Turning Points" timeline — directly overlaps "historian" positioning |
| **Stockopedia AI** (2025 relaunch) | 🔴 High | AI metric explanations + TW coverage + learning paths — comprehensive competitor |
| **Moomoo/Futubull** | 🟡 Med-High | AI education + social learning feed + paper trading; broker conflict of interest |

### Medium Threat Competitors
| Competitor | Threat | Key Overlap |
|---|---|---|
| **Sensical** | 🟡 Medium | AI-adaptive learning + Traditional Chinese support |
| **玉山證券** | 🟡 Medium | "Beginner Village" + ESG screener |
| **Finimize** | 🟡 Medium | AI Q&A + structured courses |
| **TW Telegram Bots** | 🟡 Med-High | Messaging-native UX advantage; evolving rapidly |
| **Finqle** | 🟡 Medium | Gamified learning; validates demand for engagement |

### Emerging Trends (from R5)
1. **AI-Generated Company Narratives** — becoming table stakes by 2026
2. **Personalized Learning Paths** — standard feature in financial education
3. **Social + Mobile-First Learning** — TikTok-style feeds, swipe-based UX
4. **ESG Integration** — growing area of beginner interest
5. **AI Q&A as Table Stakes** — users expect natural language questions
6. **Gamification** — "Duolingo for finance" model gaining traction

---

## Feature Gap Analysis (Current vs. Competitors)

### Critical Gaps (No Competitor Does This Well for TW Market)
| Gap | Stock Explorer Status | Closest Competitor | Opportunity |
|---|---|---|---|
| **TW-Specific Company Timeline Narrative** | ❌ Missing (ISSUE-C11, P2, 16-24h) | StockStory (no TW depth) | Unique differentiator |
| **Explainable Health Score** | ❌ Missing (ISSUE-C14, P1/P2, 4-20h) | Stockopedia AI (limited explanations) | Unique differentiator |
| **Guided Learning Path** | ❌ Missing (ISSUE-C19, deferred) | Sensical (no TW companies) | Unique differentiator |

### Standard Gaps (Competitors Have, Stock Explorer Doesn't)
| Gap | Stock Explorer Status | Competitors |
|---|---|---|
| **Push Notifications** | ❌ ISSUE-C02 (P0, 14-18h) | All major competitors |
| **Ex-Dividend Calendar** | ❌ ISSUE-C01 (P0, partial) | GoodInfo, StatementDog |
| **Market Thermometer** | ❌ ISSUE-C04 (P1, 12-16h) | WantGoo, CMoney |
| **PPT Generation** | ❌ ISSUE-C06 (P1, 18-24h) | WantGoo |
| **Custom Event Thresholds** | ❌ ISSUE-C07 (P1, 10-14h) | None (unique opportunity) |
| **AI Q&A** | ❌ ISSUE-C17 (P2, 10-14h) | Stockopedia AI, Finimize |
| **Glossary/Tooltips** | ❌ ISSUE-C12 (P2, 8-12h) | Investopedia |
| **Company Facts** | ❌ ISSUE-C16 (P2, 4-6h) | Stash "Stock Bits" |

---

## New Feature Ideas from Round 6

No new feature ideas were generated this round due to QA subagent timeout. The existing backlog of 17 feature ideas (C01-C19, D01-D03, R5-A through R5-F) remains current.

---

## Key Takeaways for PM

1. **StockStory and Stockopedia AI remain the highest threats** — both have AI-generated narratives + TW coverage. Stock Explorer must accelerate ISSUE-C11 (Company Timeline Narrative) and ISSUE-C14 (Health Score) to defend the "historian" positioning.

2. **AI-generated narratives are becoming table stakes** — by 2026, users expect to see a company story, not just data. Stock Explorer's structured analysis (9 pages) is deeper, but the lack of a narrative entry point is a competitive weakness.

3. **The notification gap (C02) is the most critical P0 gap** — all competitors have push notifications. Stock Explorer's event detection engine has the data but no delivery mechanism. D02 (background worker) is the blocker.

4. **Design grade improved to C** (from C-) — the `_info_card()` border fix (D-059) and business_card.py restoration are confirmed. But 81 total design issues remain.

5. **Tech debt velocity is zero** — 5 consecutive review rounds with zero items resolved. The 19 open tech debt items (~19 hours) need a dedicated cleanup sprint.

---

*This report was synthesized by the PM after the QA Engineer subagent timed out on web search. The next review cycle should re-attempt web research with a narrower scope or longer timeout.*
