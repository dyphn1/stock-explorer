# Review Round 39 — QA Competitor Research Report (Consolidated)

> **Date**: 2026-06-14
> **Round**: 39 (Sprint 18 Post-Mortem + Sprint 19 Planning)
> **Author**: QA Engineer
> **Status**: COMPLETE

---

## Executive Summary

This is Review Round 39's consolidated QA competitor research deliverable, covering both Round 13 and Round 14 research. It provides a comprehensive analysis of the competitive landscape following Sprint 18's delivery of C139 (Explain This Number), C141 (Source Badge), C143 (Implication Sentence), C149 (So What? Box), D-097 (Tone QA), and Tone QA automation.

**Key Sprint 18 Achievement**: Stock Explorer simultaneously closed 5 major competitive gaps — no other TW platform offers the combination of tap-to-explain metrics, source transparency, implication sentences, dedicated "So What?" visual pattern, and systematic tone QA.

**Key Round 39 Finding**: Moomoo's April 2026 launch of "API Skills" marks the beginning of "agentic investing" — AI-powered natural language stock analysis. This makes C162 (AI Strategy Agent) a competitive necessity, not a nice-to-have. Combined with C167 (AI Screener Explanations), these would extend Stock Explorer's historian positioning into territory no TW competitor currently occupies.

---

## Competitors Analyzed (Round 14 — Review Round 39, Continued)

6 new competitors analyzed in this round:

| # | Competitor | Region | Relevance | Key Finding |
|---|-----------|--------|-----------|-------------|
| 1 | **Moomoo** | SG/Global | 🔴 High | Launched "API Skills" (April 2026) — AI-powered natural language trading strategy execution |
| 2 | **Webull** | US/Global | 🔴 High | "Learn first" positioning, paper trading, removed $25K PDT minimum (June 2026) |
| 3 | **Tastytrade** | US | 🔴 High | Most comprehensive free education library among US brokers |
| 4 | **TradingView** | Global | 🟡 Medium | "Ideas" feature — community-driven implication sharing |
| 5 | **StockEdge** | India | 🟡 Medium | Screening + education combined in single flow |
| 6 | **Zerodha Varsity** | India | 🟡 Medium | Gold standard for structured, progressive finance education |

### Competitors Analyzed Across All Rounds (Cumulative)

**116+ unique competitors** analyzed across Rounds 1-14, spanning:
- **TW Market**: StatementDog, GoodInfo, CMoney, WantGoo, 財報狗, JZ Invest, 鉅亨網, TEJ, Yahoo奇摩股市, 群益, 元大證券, 永豐金證券, 玉山證券, Haya Finance, Edgestock, Tietr
- **US/Global**: Public.com, Seeking Alpha, Koyfin, Finary, Stocksera, The Motley Fool, NerdWallet, Investopedia, Morningstar, TradingView, TipRanks, Finimize, Tickeron, Khan Academy, Stake, Moomoo, eToro, Webull, Robinhood, Spiking, Copilot Money, Datawallet, Visual Capitalist, FinChat, Kavout, Stockstory, Inderes, OpenBB, Luca AI, Bonsai, Stocked AI, Kasisto, Rogo, Tastytrade
- **Asia (ex-TW)**: Naver Finance (Korea), Kabutan (Japan), 雪球/Xueqiu (China), Zerodha Varsity (India), StockEdge (India), Gotrade (Singapore), Neon (Brazil)
- **Europe**: Freetrade (UK), Trade Republic (Germany), Revolut (UK/EU)

---

## Sprint 18 Competitive Impact Assessment

### Gaps CLOSED by Sprint 18 (5 Features)

| Feature | Sprint 18 Delivery | Competitors Who Had It | Status |
|---------|-------------------|----------------------|--------|
| Tap-to-Explain Metrics | C139 (Explain This Number) | Revolut, Ticker.ai, Luca AI | ✅ CLOSED |
| Source Transparency | C141 (Source Badge) | Luca AI | ✅ CLOSED |
| Implication Sentences | C143 (Implication Sentence) | Stockstory, Spiking, Inderes | ✅ CLOSED |
| "So What?" Visual Pattern | C149 (So What? Box) | Stockstory, Bonsai | ✅ CLOSED |
| Tone Consistency | D-097 (Tone QA) | Finimize (partial) | ✅ CLOSED |

### Gaps That Remain OPEN After Sprint 18

| Gap | ID | Priority | Competitor With This Feature |
|-----|-----|----------|------------------------------|
| AI Natural Language Strategies | C162 | P1 | Moomoo API Skills |
| Learn First Gate | C163 | P2 | Webull Learn |
| Community Implications | C164 | P2 | TradingView Ideas |
| Varsity Mode (Progressive Learning) | C165 | P2 | Zerodha Varsity |
| Paper Trading Integration | C166 | P2 | Webull, Moomoo |
| AI-Powered Stock Screener | C167 | P1 | StockEdge, Moomoo |
| Video Education Library | C168 | P2 | Tastytrade |
| Robo-Advisory with Explanations | C169 | P2 | Webull Advisors |
| Historical Event Patterns | C147/C156 | P1 | Spiking, Quiver Quantitative |
| Multi-Factor Event Narratives | C152/C158 | P1 | Public.com, Copilot Money |
| One-Paragraph Company Story | C153/C155 | P2 | Bonsai, Copilot Money |
| Screening + Explanation | C154 | P1 | Stocked AI, StonkGrid |
| Implication Confidence | C157 | P2 | Inderes, Morningstar |
| Adaptive Complexity | C159/C161 | P2 | Finimize, Stash, Revolut |
| User Annotations | C160 | P2 | 元大證券, Tastytrade |

---

## New Feature Gaps Identified (C162-C169)

### P1 Features (Next Sprint Priority)

| ID | Name | Effort | Source | Description |
|----|------|--------|--------|-------------|
| **C162** | AI Strategy Agent | 20-30h | Moomoo API Skills | Natural language stock analysis actions; conversational unification of all explanation features |
| **C167** | AI Screener Explanations | 14-18h | StockEdge, Moomoo | Plain-language stock screener with outcome narratives; transforms data into story |

### P2 Features (Short-Term Priority)

| ID | Name | Effort | Source | Description |
|----|------|--------|--------|-------------|
| **C163** | Learn First Gate | 8-12h | Webull Learn | Educational onboarding before viewing stock data |
| **C164** | Community Implications | 14-20h | TradingView Ideas | User-generated implication sentences on company pages |
| **C165** | Varsity Mode | 16-24h | Zerodha Varsity | Structured progressive learning path with certificates |
| **C166** | Paper Trading Mode | 16-24h | Webull, Moomoo | Simulated portfolio with real data and explanations |
| **C168** | Video Explanation Library | 20-30h | Tastytrade | Bite-sized videos embedded alongside stock data |
| **C169** | Robo-Advisory with Explanations | 18-24h | Webull Advisors | AI portfolio recommendations with plain-language reasoning |

---

## Key Insights (8 Bullet Points)

1. **"Agentic Investing" is the next frontier** — Moomoo's April 2026 launch of API Skills marks the shift from "explaining data" to "acting on natural language queries." C162 (AI Strategy Agent) would bridge this gap for Stock Explorer.

2. **"Learn First" is becoming table stakes** — Webull's "Get educated before you start trading" positioning, Tastytrade's education-first model, and Zerodha Varsity's education-only platform all validate that beginners expect education before data.

3. **Community-driven interpretation is the missing social layer** — TradingView's "Ideas" feature proves users want to share interpretations. C164 (Community Implications) would add a social layer on top of C143's algorithmic implications.

4. **Paper trading is expected by beginners — but none explain the simulation** — Webull and Moomoo both offer paper trading, but none explain WHY the portfolio changed. C166 would be unique: every simulated trade includes a plain-language explanation.

5. **Structured curriculum > scattered lessons** — Zerodha Varsity's progressive approach (Beginner → Intermediate → Advanced) is the gold standard. C165 (Varsity Mode) would organize all C47 content into a unified curriculum.

6. **Video education is expected but none integrate it with data** — Tastytrade has the best video education library, but it's separate from stock data. C168 would embed videos alongside relevant stock data.

7. **Robo-advisory without explanations is a missed opportunity** — Webull Advisors offers robo-advisory but doesn't explain WHY. C169 would combine robo-advisory with plain-language historical context.

8. **TW market has no "agentic" platform** — Moomoo's API Skills is US-focused. No TW platform offers natural language stock screening with explanations. C162 would be a unique differentiator.

---

## Sprint 19 Recommendations

### Top 3 Priorities for Sprint 19

1. **C167 (AI Screener Explanations)** — P1, 14-18h. Combines C42+C154 into a single narrative screening experience. StockEdge proves demand. Transforms Stock Explorer from "lookup tool" to "discovery and learn" platform.

2. **C162 (AI Strategy Agent)** — P1, 20-30h. Moomoo's April 2026 launch of API Skills makes this time-sensitive. No TW competitor has this. The conversational unification of all explanation features.

3. **C163 (Learn First Gate)** — P2, 8-12h. Low effort, high impact for beginner onboarding. Webull proves the "learn first" positioning.

### Cumulative Totals

| Metric | Count |
|--------|-------|
| Competitors analyzed | 116+ |
| Total feature gaps (C01-C169) | 169 |
| Sprint 18 gaps closed | 5 |
| New gaps identified (C162-C169) | 8 |
| P1 gaps remaining | 14+ |

---

## Files Modified

1. **docs/research/competitor_research.md** — Appended Round 14 section (C162-C169)
2. **docs/status/issues.md** — Added C162-C169 feature gap items
3. **docs/research/review39_qa.md** — This consolidated summary report

---

*End of Review Round 39 QA Competitor Research Report (Consolidated)*
