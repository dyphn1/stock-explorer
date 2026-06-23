# UX: Missing images and placeholder text on screen

**Date**: 2026-06-23
**Reporter**: Daniel

## What's the problem?

Multiple parts of the screen fail to render images or display readable text:

1. **Fake chart placeholder** (`src/main.py:382`) — Tab 2 shows literal text `[ Plotly Line Chart: Monthly Revenue Trend ]` inside a dashed-border box instead of an actual Plotly chart.

2. **No images anywhere** — Zero `st.image()` or `<img>` tags in the entire app. Company logos, icons, and visual aids are completely absent.

3. **Empty charts on missing data** — 6 chart functions return blank Plotly figures with only text annotation when data is unavailable (e.g., "no_revenue_data").

4. **49 unsafe HTML blocks** — Raw `st.markdown(..., unsafe_allow_html=True)` across 16 files; broken HTML could silently hide content.

5. **Split HTML structure** — `calculator_card.py:103` sends `</div>` as a separate `st.markdown()` call, making rendering fragile.

## Expected behavior

- Charts should render actual Plotly charts (not text placeholders)
- Company logos / images should load properly or show a graceful fallback
- Empty/no-data states should show user-friendly messages, not blank chart areas
- All HTML components should render reliably without breaking layout

## Context

The UX improvement roadmap (`docs/roadmap/ux-improvements.md`) has been documented but most items remain unaddressed:
- UX-02 (Loading indicator) — complete
- UX-07 (Watchlist feedback) — complete
- Most other UX items (UX-01, UX-03, UX-04, UX-05, UX-06, UX-09, UX-10, UX-12, UX-13, UX-14) — not started
- All P0-P3 sidebar improvements (SB-01~13) — not started
- Design review fixes (DC-001~DC-028) — most not started
- No automated UI visual regression testing exists

Sprint 23 UX prototype (`docs/sprints/sprint-23-ux-prototype.md`) proposed tabbed layout + navigation header removal, but the chart placeholder implementation was left as fake text instead of a real chart.
