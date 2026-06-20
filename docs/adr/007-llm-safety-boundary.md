# ADR-007: LLM Safety Boundary — Translate Only, No Inference

## Status
Accepted

## Date
2026-06-07

## Background

Stock Explorer uses LLMs to translate financial terminology into plain language. However, LLMs may produce inaccurate information or give investment advice, which violates the product positioning.

## Decision

LLMs are limited to **translating financial terminology into plain language**. Strictly prohibited from:
1. Making factual inferences (e.g., predicting future revenue)
2. Giving stock recommendations (buy/sell)
3. Generating content that cannot be traced back to raw data

## Implementation

1. **Template-first**: Pre-defined templates are preferred, LLM is only used as fallback
2. **Output validation**: LLM output must pass tone blocklist scanning
3. **Disclaimer**: "This tool does not constitute investment advice" displayed at the bottom of all pages

```python
# ✅ Correct: Translate terminology
explain_gross_margin(0.66) → "For every 100 dollars of goods sold, 66 dollars remain after costs"

# ❌ Wrong: Predict future
predict_future("This company will rise next year") → Prohibited

# ❌ Wrong: Investment advice
recommend("Recommend buying") → Prohibited
```

## Rationale

1. **Product positioning**: Historian, not stock critic
2. **Legal risk**: Investment advice requires relevant licenses
3. **User trust**: Incorrect AI advice harms user interests

## Consequences

- ✅ Aligned with product positioning
- ✅ Reduced legal risk
- ⚠️ LLM capabilities limited, more templates needed to supplement
