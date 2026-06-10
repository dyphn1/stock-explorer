# Stock Explorer Product Vision

## Core Positioning
**Historian, not a stock picker**
- Do not say buy or sell; only explain what has happened to the company over time.
- Help users move from "I don't understand" to "I know what this company does."
- Focus on the company itself, not short-term price movement.

## Product Name
- **Name**: 股識
- **English**: Stock Explorer
- **Tagline**: Start by understanding the company

## Target Users
- Beginner investors who want to understand the market but feel overwhelmed by jargon.
- Curious observers who want to know how companies around them make money.
- Long-term investors who want to understand changes in the companies they hold.
- Not for short-term traders or people chasing quick profits.

## Market Pain Points
1. **Information overload but insufficient understanding**: Tools like Cat Dog Finance (財報狗) provide massive amounts of data but lack plain-language explanations.
2. **Fragmented understanding**: Users need to piece together a complete company picture from multiple websites.
3. **Hindsight bias**: Most analytical tools explain the past but don't help users understand future variables.
4. **Lack of narrative**: Piles of data without context, making it hard to build memorable insights.
5. **Tool-oriented rather than education-oriented**: Focus is on "what to buy" instead of "what this company is."

## Core Value Proposition

### 1. Story first, data second
- Each analysis point opens with a real-world relatable example.
- For example: instead of saying "gross margin of 66%," say "for every 100 dollars of goods sold, 66 dollars remain after costs."
- All conclusions must be traceable to public data sources.

### 2. PPT-style presentation
- Images lead, text supports (one key point per page).
- Avoid dense walls of text; use charts, icons, and short slogans.

### 3. Adaptive and self-evolving
- Content updates as the company changes.
- Major events drive updates: acquisitions, mergers, significant losses trigger content regeneration.
- Adapts to different company types: conglomerates vs. single entities use different analytical frameworks.

### 4. Point-to-point knowledge construction
- For conglomerate structures: no org charts; instead use parent-to-subsidiary point-to-point mapping.
- Each relationship includes business dealings, ownership percentage, and synergy explanations.
- Progressive drill-down: show primary relationships first, secondary ones only on deeper exploration.

### 5. Benchmark-oriented analysis
- Don't ask "Is this company good?"; ask "How does this company differ from the industry's #1 player?"
- All comparisons are benchmarked against the industry leader.
- Difference analysis must provide specific reasons.

## Product Architecture

### Layer 1: Company Card Page (MVP Core)
- One-sentence positioning
- Revenue source pie chart (each slice with a plain-language explanation)
- Recent major event summary in plain language
- Navigation to four deep-dive sections

### Layer 2: Four Deep-Dive Sections
1. **Operations Health Check**: How does it make money? How stable is it? How has it changed over time?
2. **Financial Condition**: How much does it earn? How much does it spend? How much is left?
3. **Peer Comparison**: How does it differ from the industry's #1 player? Illustrated with real examples.
4. **Conglomerate Structure**: Parent-subsidiary relationships (point-to-point)

### Layer 3: Auxiliary Features
- Timeline configuration: defaults to 3 years, freely adjustable
- Categorized browsing: weighted stocks, industry categories, popular lists
- ETF section: treated equally, from holdings to featured strategies
- Subscription system: fully config-driven

## Tech Stack Selection
1. **Data layer**: FinMind (50+ financial datasets, updated daily)
2. **Processing layer**: Python (data cleaning, feature engineering)
3. **Explanation layer**: LLM (plain-language translation only) + templates
4. **Visualization layer**: Plotly (interactive charts) + custom CSS (PPT-style)
5. **Presentation layer**: Streamlit (rapid iteration)
6. **Caching layer**: Local file cache + invalidation mechanism

## Development Philosophy
### Iterative cycle over waterfall
- Design > Analysis > Reflection > Synthesis > Redesign
- After each feature implementation, verify: does it genuinely help beginners understand better?
- Refuse to implement all features at once.

### Verification principles
- Every explanation must pass the "ten-second test": a beginner can restate the core concept within ten seconds.
- All data must cite its source to avoid a black-box feel.
- Willing to sacrifice completeness for clarity.

## Milestones
| Milestone | Content | Verification Standard |
|-----------|---------|----------|
| M0 | Project foundation setup | Environment runs |
| M1 | MVP card page | Beginner ten-second restatement accuracy > 80% |
| M2 | Four deep-dive sections | Can answer "What has this company been up to recently?" |
| M3 | Timeline & categorization | Users can independently explore across dimensions |
| M4 | ETF & subscriptions | Users proactively set preferences and receive notifications |
| M5 | Adaptive updates | Content updated within 24 hours of a major event |

## Risks & Countermeasures
| Risk | Countermeasure |
|------|-------|
| LLM generates false facts | LLM limited to plain-language translation; facts come from structured data |
| Scope creep | Strict milestone verification enforcement |
| Delayed data updates | FinMind updates daily; major events can be user-reported as triggers |
| Users still want buy/sell advice | Clear product positioning: "This is not a stock-picking tool" |
| Conglomerate complexity spiraling out of control | Phase one only handles holdings >50% or revenue contribution >10% |

---
*Last updated: 2026-06-06*
