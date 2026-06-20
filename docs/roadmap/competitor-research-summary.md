# Competitor Research Summary

> **Source**: `docs/decisions/competitor_research.md` (R1-R5)
> **Research Rounds**: 5 rounds, covering 40+ competitor platforms
> **Date**: 2026-06-09 ~ 2026-06-12

---

## Competitor Overview

### Taiwanese Platforms

| Platform | Positioning | Target Users | Difference from Stock Explorer |
|----------|-------------|--------------|-------------------------------|
| **StatementDog (Cai Bao Gou)** | Financial statement analysis expert | Intermediate investors | Data-intensive, lacks plain-language explanations |
| **GoodInfo** | Portal site | All investors | Traditional portal style |
| **CMoney** | Investment decision platform | Active investors | App-style, feature-complete |
| **WantGoo** | Community + data | Short-to-medium-term traders | Forum + basic charts |
| **Yahoo Finance Taiwan** | Portal site | All investors | International, shallow Taiwan data |
| **Anue (Ju Heng)** | News + data | All investors | News-oriented |
| **TEJ** | Professional data | Institutional investors | Paid, professional |
| **JZ Invest** | Investment tools | Intermediate investors | Technical analysis-oriented |

### International Platforms

| Platform | Positioning | Highlights |
|----------|-------------|------------|
| **Investopedia** | Financial education | Glossary + tutorials |
| **Stockopedia** | Stock analysis | Multi-factor scoring |
| **Simply Wall St** | Visual analysis | Snowflake charts |
| **Finviz** | Screener | Powerful screening + heatmap |
| **Kavout** | AI stock scoring | AI-native |
| **TipRanks** | AI + analyst consensus | Community + AI |
| **Moomoo/Futubull** | AI education | 2025 new features |

---

## Key Findings

### 1. White Space
- **Beginner education focus**: No platform focuses on "helping beginners understand in 10 seconds"
- **Story-driven analysis**: Most platforms provide data but lack narrative
- **Adaptive framework**: No platform automatically adjusts analysis perspective based on company type
- **Plain-language translation**: StatementDog has it but doesn't do it thoroughly enough

### 2. Competitor Trends (2025-2026)
- **AI-Native analysis**: Kavout, TipRanks, Yahoo Finance AI Reports
- **Micro-learning**: Taster.finance, Sensical (bite-sized financial education)
- **Mobile-first**: Bottom-sheet, card-stack, swipe UX
- **Progressive disclosure**: Default shows only one number + one sentence, click to expand
- **Dark mode**: All platforms support it, WCAG AA contrast ratio

### 3. Feature Gaps (What Stock Explorer is Missing)

| Feature | Competitor Reference | Priority |
|---------|---------------------|----------|
| Clickable Glossary | Investopedia | P1 |
| Reading time indicator | Medium | P2 |
| Confidence indicator | TipRanks | P1 |
| Industry heatmap | Finviz | P2 |
| Today's market overview | Yahoo Finance | P2 |
| Story arc detection | StockStory | P2 |
| Ex-dividend calendar | GoodInfo | P1 |
| Beginner onboarding flow | Acorns/Stash | P1 |
| Light/dark theme | All platforms | P1 |
| Responsive layout | All platforms | P1 |

---

## Core Competitive Advantages

Stock Explorer's differentiated positioning:
1. **Historian positioning**: No investment advice, only storytelling
2. **PPT style**: One key point per page, image-driven
3. **10-second test**: Beginner-friendly core design principle
4. **Benchmark-oriented comparison**: Compare against industry leaders, not averages
5. **Free and open source**: All competitors are paid or ad-supported
