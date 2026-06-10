# Design Review Report

> Reviewer: Design Reviewer sub-agent
> Date: 2026-06-08
> Documents reviewed: `docs/strategy/product_vision.md`, `docs/design/design_system.md`, `docs/design/architecture_fixes.md`, `docs/design/ux_improvements.md`

---

## Summary

Both proposal documents are **high quality** and demonstrate deep understanding of the codebase. The architect and UX agent identified largely the same set of problems from different angles, which increases confidence in the findings. All proposals align with the core product vision of "Be a historian, not a stock picker" — none introduce stock-picking features or violate the 10-second test principle.

**Key verdict**: Approve all proposals for implementation. The consolidated roadmap below merges overlapping proposals and resolves 6 conflicts/gaps between the two documents.

**Overall quality assessment:**
- Architecture fixes: Technically sound, well-prioritized, correct root cause analysis
- UX improvements: Strong user empathy, good alignment with design system, accurate severity ratings
- Both docs correctly reference DESIGN_SYSTEM.md patterns (color system, PPT style, error handling rules)

---

## Conflicts & Issues

### Conflict 1: ROE Annualization — Duplicate Proposal, Different Approaches
- **ARCH_FIXES Issue 7** proposes TTM (trailing twelve months) with fallback to quarterly ROE labeled "(單季)" when < 4 quarters available.
- **UX Issue 5** also proposes TTM but additionally suggests a `seasonal_industries` list and industry-specific warning labels.
- **Resolution**: Merge. Use the arch proposal as the algorithmic base, and add the UX proposal's seasonal industry note as the display-layer enhancement. Both are correct; the UX proposal adds a beginner-friendly layer on top of the arch fix.

### Conflict 2: Watchlist Race Conditions — Different Locking Libraries
- **ARCH_FIXES Issue 8** proposes a custom `FileLockManager` using `fcntl.flock()` (Unix-only) with atomic writes via `os.replace()`.
- **UX Issue 14** proposes the `filelock` pip package (cross-platform) with backup via `shutil.copy2`.
- **Resolution**: Prefer `filelock` package — it is cross-platform (Windows compatibility noted in the arch doc), tested, and immediately available via `uv add filelock`. The atomic write pattern from the arch proposal should be layered on top. The `fcntl`-only approach is fragile if the app is ever deployed on Windows.

### Conflict 3: API Rate Limit Handling — Layer Disagreement
- **ARCH_FIXES Issue 6** proposes a custom `FinMindRateLimitError` exception class at the data layer, caught at the UI layer.
- **UX Issue 10** proposes a `_consecutive_failures` counter with a threshold-based warning, plus request debouncing and a sidebar status indicator.
- **Resolution**: Merge both. The custom exception (arch) handles the immediate detection; the consecutive-failure counter (UX) handles the case where FinMind returns empty DataFrames instead of raising errors. Both are needed. The sidebar status indicator is a nice UX addition.

### Conflict 4: Chinese Name Search — Overlapping Scope
- **ARCH_FIXES Issue 1** proposes `search_stocks()` in `finmind_client.py` with full-list caching.
- **ARCH_FIXES Issue 3** proposes using `search_stocks()` in the sidebar.
- **UX Issue 1** proposes a similar `search_stock()` method but in the client class with a different method name and additional fuzzy matching.
- **Resolution**: Consolidate into a single `search_stocks()` method (plural, as in arch) that supports exact + partial matching. The arch doc already implies this. The UX proposal's fuzzy matching (partial for inputs ≥ 2 chars) should be the matching strategy. The arch proposal's `_fetch_all_stock_info()` is the correct caching approach.

### Conflict 5: DuplicateWidgetID — Trivial Fix, Same Solution
- **ARCH_FIXES Issue 4** recommends `enumerate` index (Option A).
- **UX Issue 8** recommends index + date in the key.
- **Resolution**: Use the arch proposal's Option A (`f"evt_{stock_id}_{idx}"`) — it is simpler and deterministic. Adding the date (UX proposal) adds no value if the index is already unique within the page render. Both agree this is a P0 one-line fix.

### Conflict 6: Timeline Filter — Same Root Cause, Different Error Messages
- **ARCH_FIXES Issue 10** proposes narrow exception handling + `st.warning` for errors + `st.info` for empty results.
- **UX Issue 9** proposes the same, plus a debug caption showing the active date range and a "Reset to ALL" button.
- **Resolution**: Merge. The arch fix handles the technical correction; the UX proposal adds useful display enhancements (caption, reset button). Both are needed for a complete fix.

### Gap 1: No Cross-Reference Between Docs
Neither document references the other. The architect was unaware of the UX findings and vice versa. This led to duplicated ROE and race condition proposals. **Recommendation**: In the development workflow, always review both architecture and UX proposals together before implementation.

### Gap 2: Missing Proposal — Sidebar Search UX for `search_stocks()` Results
The arch proposal adds `search_stocks()` but doesn't specify how multi-match results are displayed in the sidebar. The UX proposal (Issue 1) specifies a dropdown but doesn't mention the multi-result case. The sidebar search UI needs a defined behavior for: (a) no match → error, (b) single match → navigate directly, (c) multiple matches → show dropdown. **This is implicitly handled by the combined proposals but should be made explicit in implementation.**

### Gap 3: Missing Proposal — Cache Key Fix Has User-Facing Impact
The cache key fix (ARCH Issue 2) will reduce API calls dramatically, which directly solves UX Issue 10 (rate limits). However, neither document makes this connection explicit. **Implementing the cache key fix may reduce the urgency of UX Issue 10** — the rate limit warning may rarely trigger once caching works correctly.

### Gap 4: Issue Severity Inconsistency for ETF Classification
- **ARCH_FIXES Issue 5** (ETF determination): Ranked P1.
- This issue has no UX counterpart but directly affects the ETF Zone page (3rd layer feature). However, **for beginners exploring ETFs** (a stated user persona), misclassification means they see the wrong analysis framework. This should arguably be P0 for M4 milestone readiness. Keeping at P1 is acceptable since M4 hasn't been reached yet.

### Gap 5: PPT Style Chart Proportions Not Addressed in Chart Fallback Proposals
UX Issue 4 (single-period charts) proposes fallback to bar/line charts but doesn't address whether the fallback still meets the "> 60% chart area" requirement from DESIGN_SYSTEM Section 5.3. **Implementation note**: When showing a single-period bar chart, it should use `fig.update_layout(height=...)` to maintain proportional screen usage.

---

## Consolidated Implementation Roadmap

| Priority | Issue | Source Doc | Effort | Impact |
|----------|-------|------------|--------|--------|
| **P0** | DuplicateWidgetID crash in event dashboard | ARCHIssue 4 + UX Issue 8 | **Trivial** — 1 line change | Prevents page crash in production. Use `enumerate` index for unique keys. |
| **P0** | API abuse in `get_stock_info` — full list per stock | ARCH Issue 1 + UX Issue 1 | **Medium** — new method + refactor callers | Eliminates root cause of rate limiting. Enables Chinese name search. Single full-list cache shared across all lookups. |
| **P0** | Daily cache invalidation — `end_date` in cache key | ARCH Issue 2 | **Low** — remove param from key generation | Cache TTL actually works. Fixes rate limit trigger (enables UX Issue 10 fix). Bounded disk usage. |
| **P0** | Race conditions in YAML file operations | ARCH Issue 8 + UX Issue 14 | **Medium** — new `filelock` utility + refactor | Prevents data loss under concurrent access. Use `filelock` package (cross-platform) + atomic writes. Apply to watchlist and events YAML. |
| **P1** | Crude ROE annualization — quarterly × 4 misleading | ARCH Issue 7 + UX Issue 5 | **Medium** — TTM calculation + seasonal note | Fixes wildly inaccurate ROE for seasonal businesses. Follows "Correctness > Clarity" principle. Merge TTM algorithm (arch) + seasonal industry label (UX). |
| **P1** | No loading indicator on page switch | UX Issue 2 | **Low** — wrap with `st.spinner` | Meets DESIGN_SYSTEM 4.1 requirement. Prevents duplicate clicks from confused users. Essential for the 10-second test (users need feedback within 0.5s). |
| **P1** | ETF determination missing `industry_category` param | ARCH Issue 5 | **Low** — pass param or fetch internally | Correct ETF classification → correct analysis framework. Needed for M4 ETF Zone milestone. |
| **P1** | Unhandled API rate limit — silent failures | ARCH Issue 6 + UX Issue 10 (merged) | **Medium** — exception class + failure counter + UI | Custom `FinMindRateLimitError` + consecutive failure detection + warning UI. Sidebar rate status indicator (UX enhancement). Lower urgency if P0 cache fix works well. |
| **P1** | Watchlist add/remove — no visual feedback | UX Issue 7 | **Low** — `st.toast()` or `st.success()` | Fundamental UX principle: action confirmation. Low effort, high trust impact. |
| **P1** | Peer comparison dead-end for non-benchmark stocks | UX Issue 6 | **Medium** — fallback benchmark selection | Prevents empty pages for less popular stocks. Auto-select market cap leader in same industry. Always show at least single-company data. |
| **P1** | Timeline filter silent failure | ARCH Issue 10 + UX Issue 9 (merged) | **Low** — narrow exceptions + warning UI + caption | Merge: narrow exception handling (arch) + date range caption + reset button (UX). Prevents user confusion about filter state. |
| **P1** | Single-period data shows empty charts | UX Issue 4 | **Medium** — fallback chart types | Violates PPT-style >60% chart area rule. Show bar/line fallback with contextual note. |
| **P1** | No name/keyword search in sidebar | ARCH Issue 3 (uses ARCH Issue 1's `search_stocks`) | **Low** — already covered by P0 Issue 1 | Enables "TSMC" search. Define 3-state UI: no match → error, single → navigate, multiple → dropdown. |
| **P2** | Browser back button doesn't work | UX Issue 3 | **High** — `st.query_params` integration | Known Streamlit limitation. Use `st.query_params` for URL-based state. Important for power users but not blocking MVP. |
| **P2** | Layout breaks on small screens | UX Issue 12 | **High** — CSS media queries + responsive columns | Important for tablet/laptop users. Use CSS media queries + `st.tabs()` fallback for navbar. Test at 375/768/1024/1440px. |
| **P2** | Dark mode chart label contrast | UX Issue 13 | **Medium** — shared `CHART_TEMPLATE` | Create shared Plotly layout template with DESIGN_SYSTEM colors. Test in both light and dark mode. |
| **P2** | Cache directory grows unbounded | UX Issue 11 (ARCH Issue 2 partially covers) | **Low** — cleanup on init | Already partially addressed by ARCH Issue 2's `_cleanup_cache()`. Add LRU eviction and sidebar stats as polish. |
| **P2** | Fragile column name access in event detection | ARCH Issue 9 | **Medium** — `column_map.py` utility | Defensive coding against FinMind schema changes. Lower priority since it hasn't broken yet. |

---

## Recommendations

### For the PM

1. **Start with the 4 P0 items this sprint.** They are independent and can be parallelized:
   - DuplicateWidgetID (1 line, any dev can do it)
   - Cache key fix (single file change)
   - API abuse fix + search (one sub-agent, two birds)
   - YAML locking (one sub-agent, new utility file)

2. **Merge the overlapping proposals before assigning work.** Specifically:
   - ROE annualization: one implementation, two display enhancements
   - Rate limit handling: data-layer exception + UX-layer counter/indicator
   - Timeline filter: technical fix + UX enhancements in one PR
   - File locking: use `filelock` package, not raw `fcntl`

3. **The cache key fix (P0) may defang the rate limit issue (P1).** After implementing the cache fix, monitor whether rate limits still occur. If not, the rate limit warning UI (UX Issue 10) can be deprioritized to P2.

4. **Chinese name search is a first-impression issue.** The sidebar placeholder promises it, but it doesn't work. This is the very first interaction for many Taiwanese users. Implement it as part of the P0 API abuse fix (they share the same `search_stocks()` method).

5. **Watchlist feedback (UX Issue 7) is a 15-minute fix with outsized trust impact.** Do it alongside the YAML locking fix since both touch `watchlist.py`.

6. **Don't defer the loading indicator (UX Issue 2).** It's low effort and directly required by DESIGN_SYSTEM 4.1. Users staring at a blank screen for 5-15 seconds will abandon the app before the 10-second test even begins.

7. **For the responsive layout issue (UX Issue 12),** consider whether Streamlit's built-in `st.tabs()` could replace the 9-button navbar entirely. This would solve both the narrow-screen wrapping issue and simplify the navigation code. This is a design decision for Daniel to confirm — write to PENDING_REVIEW.md.

8. **Validate the seasonal industry list with Daniel** before implementing UX Issue 5's seasonal note. The list of "known seasonal industries" is a product decision, not a technical one.

9. **Add cross-referencing to the development workflow.** Before any future architecture or UX review, the reviewer should read both proposal documents to avoid duplicate proposals and identify synergies.

### Implementation Sequencing Note

The recommended order within each priority band:
- **P0 band**: Issue 4 (trivial win) → Issue 2 (unblocks cache) → Issue 1 (enables search + fixes rate limits) → Issue 8 (data integrity)
- **P1 band**: Issue 7 (ROE, foundational correctness) → Issue 2 (loading, immediate UX) → Issue 5 (ETF, M4 prep) → Issue 14 (watchlist feedback) → Issue 10 (rate limit UI) → Issue 3 (search UI) → Issue 9 (timeline) → Issue 6 (peer comparison) → Issue 4 (chart fallbacks)

---

*This review was produced by cross-referencing all four project documents. All proposals are approved for implementation with the noted merges and resolutions.*
