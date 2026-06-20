# Product Vision — Stock Explorer (股識)

> **Core Positioning**: A historian, not a stock picker. We don't call buys or sells — we tell the story of "what happened to this company over the years."

---

## 1. Product Overview

| Property | Value |
|----------|-------|
| **Chinese Name** | 股識 |
| **English Name** | Stock Explorer |
| **Tagline** | Get to know a company, starting here |
| **Version** | v0.1.0 (MVP) |
| **License** | MIT License |
| **Repository** | GitHub — stock-explorer |

---

## 2. Target Users

### Primary Users
- **Beginner investors**: People who want to understand the market but are intimidated by jargon
- **Curious observers**: People who want to know how companies around them make money
- **Long-term holders**: Investors who want to understand changes in the companies they hold

### Non-Target Users
- Short-term traders or those chasing quick profits
- Professional traders who need real-time quotes or technical analysis

---

## 3. Market Pain Points

| # | Pain Point | Shortcoming of Existing Tools |
|---|------------|-------------------------------|
| 1 | Information overload but insufficient understanding | Tools like StatementDog provide lots of data but lack plain-language explanations |
| 2 | Fragmented understanding | Users need to piece together a company's full picture from multiple sites |
| 3 | Lack of narrative | Piles of data without context, hard to form memorable insights |
| 4 | Tool-oriented rather than education-oriented | Focus is on "what to buy" rather than "what kind of company is this" |
| 5 | Rear-view mirror bias | Most tools explain the past but don't help understand future variables |

---

## 4. Core Value Proposition

### 4.1 Story First, Data Second
- Every analysis point starts with a real-world understandable example
- For example: instead of saying "gross margin 66%", say "for every 100 dollars of goods sold, 66 dollars remain after costs"
- All conclusions must be traceable to public data sources

### 4.2 PPT-Style Presentation
- Image-driven, text-assisted (one key point per page)
- Avoid dense text walls; use charts, icons, short taglines

### 4.3 Adaptive and Self-Evolving
- Content updates as the company changes
- Major events (acquisitions, mergers, significant losses) trigger content regeneration
- Different company types (group vs. single entity) use different analysis frameworks

### 4.4 Point-to-Point Knowledge Building
- Group structure: use parent company → subsidiary point-to-point mapping instead of org charts
- Each relationship includes business dealings, ownership percentage, synergy explanation
- Progressive depth: show primary relationships first, secondary relationships only on deeper exploration

### 4.5 Benchmark-Oriented Analysis
- Don't ask "is this company good?", ask "how does this company differ from the industry leader?"
- All comparisons use the industry leader as the benchmark
- Difference analysis must provide specific reasons

---

## 5. Design Principles

### 5.1 10-Second Test
> A beginner must be able to understand and restate the core concept of a page within 10 seconds.

### 5.2 Design Decision Priority
```
Correctness > Clarity > Completeness > Aesthetics
```
Better to show less than to show incorrect or confusing content.

### 5.3 Safety Boundaries
- **No investment advice**: Only explain the company's past and present
- **Transparent data sources**: All data must be annotated with its source
- **LLM safety**: LLM is only used to translate financial terms into plain language; factual derivation or stock recommendations are prohibited

---

## 6. Feature Architecture

### Layer 1: Business Card Page (MVP Core)
- One-line positioning
- Revenue breakdown pie chart (each slice with plain-language explanation)
- Plain-language summary of recent major events
- Navigation to four deep-dive sections

### Layer 2: Four Deep-Dive Sections
1. **Operations Checkup**: How does it make money? Is revenue stable? Historical changes?
2. **Financial Health**: How much does it earn? How much does it spend? How much is left?
3. **Peer Comparison**: How does it differ from the industry leader? Explained with real examples
4. **Group Structure**: Parent company → subsidiary relationships (point-to-point)

### Layer 3: Supporting Features
- Timeline: Default 3 years, freely adjustable
- Category browser: Blue-chip stocks, industry categories, hot lists
- ETF section: Listed alongside individual stocks, from holdings to strategy explanation
- Watchlist: Config-based, supports price alerts
- Event dashboard: Adaptive updates, major event notifications

---

## 7. Competitor Differentiation

| Dimension | StatementDog | GoodInfo | CMoney | **Stock Explorer** |
|-----------|-------------|----------|--------|-------------------|
| **Positioning** | Financial statement analysis expert | Portal site | Investment decision platform | **Beginner education-oriented** |
| **UI Style** | Data-dense tables | Traditional portal | App-style | **PPT-style** |
| **Plain-language** | Partial | None | Yes (key summaries) | **Core feature** |
| **Target Users** | Intermediate investors | All investors | Active investors | **Beginner investors** |
| **Pricing** | Free + paid membership | Free (ads) | Free + subscription | **Free and open source** |
