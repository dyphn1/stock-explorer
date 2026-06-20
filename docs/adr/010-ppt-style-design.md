# ADR-010: PPT-Style Design Principles

## Status
Accepted

## Date
2026-06-08

## Background

Stock Explorer's target users are beginner investors. Traditional stock tools with data-dense tables and heavy text are not beginner-friendly.

## Decision

Adopt **PPT style** as the core design principle:

1. **One key point per page**: Each page conveys only one core message
2. **Visual-first, text-supporting**: Charts occupy > 60% of page area
3. **Ten-second test**: A beginner can restate the core concept within 10 seconds
4. **Progressive disclosure**: Only key data shown by default, details on demand

## Specific Guidelines

### Layout
- Each page has at most 1 primary chart
- Above the chart: a one-line title
- Below the chart: plain-language explanation + real-life analogy
- No stacking 3+ charts on a single page

### Data Cards
- Each card: title + large-font data + plain-language explanation
- Maximum 4 cards per row (desktop)
- Use `_plain_language_card()` shared component

### Text Limits
- Card description text ≤ 200 characters
- Analysis text ≤ 400 characters
- When exceeded, use `st.expander` to collapse

## Rationale

1. **Beginner-friendly**: Reduces cognitive load
2. **Memorability**: One key point per page is easier to remember
3. **Differentiation**: Creates distinction from data-dense tools like StatementDog

## Consequences

- ✅ Easier for beginners to understand
- ✅ Cleaner pages
- ⚠️ Strict enforcement required, otherwise easy to regress to data-dense style
- ⚠️ Some pages need to be rewritten to comply with guidelines
