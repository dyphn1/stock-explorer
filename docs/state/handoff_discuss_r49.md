# Handoff – Discussion Round 49

## Summary
- **Topic**: 💡 Discussion (Round 49 — 2026-06-17)
- **Participants**: Product Manager, System Architect, Challenger
- **Sprint Status**: Sprint 23 ✅ COMPLETE → Sprint 24 (C201) ready for implementation
- **Challenger Verdict**: ✅ ALIGNED — All Round 48 blockers resolved, C201 ready, C203/C209 decisions made

---

## Sprint 23 — FINAL VERIFICATION ✅

All 5 Round 48 blocking questions confirmed RESOLVED in codebase:

| # | Question | Status | Evidence |
|---|----------|--------|----------|
| Q1 | `src/core/locales/` deleted? | ✅ | Directory confirmed gone |
| Q2 | `story_arc_detector.py` returns keys? | ✅ | Returns `growth`/`decline`/`volatile`/`recovery`, not Chinese |
| Q3 | `story_arcs.yaml` removed? | ✅ | File deleted; all strings in locale YAML |
| Q4 | Four-safeguard pattern in `debate_cards.py`? | ✅ | All 4 safeguards present (disclaimer, auto-generated label, data-driven points, banned word filter) |
| Q5 | FinMind API validated? | ✅ | 484 lines of tests with mock data; all 122 Sprint 23 tests passing |

### Sprint 23 Shipped Features

| Feature | Files | Tests | Status |
|---------|-------|-------|--------|
| C202 Story Arc Labels | `story_arc_detector.py` (228 lines) | 327 lines | ✅ Complete |
| C199 Bear vs Bull Debate Cards | `debate_engine.py` (196 lines), `debate_cards.py` (201 lines) | 388 lines | ✅ Complete |
| C200 What If Calculator | `scenario_calculator.py` (374 lines) | 484 lines | ✅ Complete |

**Total new code**: ~998 lines | **Total new tests**: ~1,199 lines | **All 545 tests**: ✅ PASSING

---

## C201 Open Questions — RESOLVED

| # | Question | Resolution |
|---|----------|------------|
| 1 | TAIEX data source | **Use average change proxy** — compute market-level stats from all stock summaries (already implemented in design). Remove the `close=total_stocks * 100` placeholder. Show `% change` and `avg change` instead of absolute index value. |
| 2 | Volume baseline | **Simplify to absolute volume** — show total market volume in 億元. Remove `volume_above`/`volume_below`/`volume_normal` comparison keys. Replace with single `volume_total` key. |
| 3 | Event filtering | **Post-filter by event type** — filter `get_all_recent_events()` results to market-relevant types only: `earnings`, `dividend`, `institutional`, `market_news`. Skip per-stock operational events. |

---

## C203/C209 Evaluation — DECISIONS

### C203 Supply Chain Visual Map → REDEFINED

**Decision**: Redefine as **"Company Ecosystem Cards" v1** for Sprint 25.

**Rationale**: True supply chain data (customer-supplier relationships) requires paid FinMind API or manual curation at 2-4h per stock. The 36-50h original estimate is too large for a single feature. Existing `group_structures.yaml` has parent-subsidiary data for ~12 stocks.

**Scope for v1**:
- Show key relationships as cards (not network graph) for top 15-20 stocks
- Use existing `group_structures.yaml` + manually curated data from annual reports
- No network visualization — simple card-based layout
- **Revised estimate**: 12-15h (data curation + page + tests)

**Deferred**: Full network graph visualization (D3.js/Plotly force-directed layout) — requires dedicated sprint.

### C209 Source Transparency Layer → REDESIGNED

**Decision**: Implement as **collapsible "資料來源" section** per page (Option A).

**Rationale**: Inline citations on every metric would clutter the PPT-style layout and misalign with historian positioning. M5's `check_data_freshness()` already provides per-page freshness indicators (80% of value). A collapsible section adds the remaining 20% with minimal UI impact.

**Scope**:
- Add collapsible "資料來源" expander at bottom of each data-heavy page
- Show: data source name (e.g., "FinMind API"), last fetch timestamp, cache status
- **Revised estimate**: 4-6h (reuse existing provenance data from M5)

---

## Sprint 24 — FINAL PLAN

### Week 1-2: C201 Implementation (MUST)

| Step | File | Change | Hours |
|------|------|--------|-------|
| 1 | `src/pages/daily_market.py` | CREATE — new page with 6 section renderers | 3-4 |
| 2 | `src/pages/router.py` | Add route + import | 0.5 |
| 3 | `locales/zh-TW.yaml` + `locales/en.yaml` | Add ~40 i18n keys (reduced from 50 after volume simplification) | 1.5 |
| 4 | `src/pages/url_sync.py` | Add to VALID_PAGES | 0.25 |
| 5 | Testing | Verify all 5 sections render; i18n; freshness indicator | 1-2 |
| **Total** | | | **6-8h** |

**Resolved design changes** (from open questions):
- Remove TAIEX placeholder — use avg change % as primary metric
- Simplify volume to absolute total (億元)
- Post-filter events by market-relevant types only

### Week 3: C201 Testing + Bug Fixes
- All 5 sections verified with real FinMind data
- Edge cases handled (empty data, API errors, stale cache)
- 545+ tests still green

### Week 4: C206 Stretch Goal (if C201 ships early)
- Recurring Investment Education content
- 6-8h, pure educational content, no new data sources
- Add to `academy.py` or as new lesson

### Sprint 25 (Provisional)
1. **C203** Company Ecosystem Cards v1 (12-15h)
2. **C209** Collapsible source section (4-6h)
3. **C200** follow-ups (if deferred from Sprint 23 — already complete)

---

## Low-Priority Cleanup Items (Sprint 24, if time permits)

| Issue | Severity | Effort | Recommendation |
|-------|----------|--------|----------------|
| `validate_debate_text()` naming | 🟢 Low | 5 min | Rename to `contains_banned_words()` |
| Timeline strings in `scenario:` namespace | 🟢 Low | 15 min | Move to `timeline:` namespace |
| Dead `calculate_scenario` import in `_historical_scenarios.py` | 🟢 Low | 5 min | Remove if unused |

---

## Action Items

| Item ID | Description | Owner | Sprint | Status |
|---------|-------------|-------|--------|--------|
| A49-01 | Create `src/pages/daily_market.py` | Developer | Sprint 24 | ⏳ Pending |
| A49-02 | Add daily_market route to router.py | Developer | Sprint 24 | ⏳ Pending |
| A49-03 | Add C201 i18n keys (~40 keys) to locale files | Developer | Sprint 24 | ⏳ Pending |
| A49-04 | Fix TAIEX placeholder — use avg change proxy | Developer | Sprint 24 | ⏳ Pending |
| A49-05 | Simplify volume to absolute total | Developer | Sprint 24 | ⏳ Pending |
| A49-06 | Post-filter events by market-relevant types | Developer | Sprint 24 | ⏳ Pending |
| A49-07 | Rename `validate_debate_text()` → `contains_banned_words()` | Developer | Sprint 24 | ⏳ Pending |
| A49-08 | Move timeline strings to `timeline:` namespace | Developer | Sprint 24 | ⏳ Pending |
| A49-09 | Remove dead import in `_historical_scenarios.py` | Developer | Sprint 24 | ⏳ Pending |
| A49-10 | Evaluate C206 for Sprint 24 stretch | PM | Sprint 24 | ⏳ Pending |

---

## Key Architectural Decisions (Updated)

1. **C201 uses avg change % proxy** — no TAIEX absolute value needed
2. **Volume simplified to absolute total** — no 5-day average comparison
3. **Events post-filtered by type** — market-relevant only
4. **C203 redefined as "Company Ecosystem Cards" v1** — card-based, not network graph
5. **C209 redesigned as collapsible source section** — not inline citations
6. **All Sprint 23 features verified complete** — 545 tests green

---

## Documentation Created
- `docs/architecture/discuss_r49_architect.md` — Full architecture analysis
- `docs/state/challenge_r49.md` — 3-round challenge with 9 questions
- `docs/state/handoff_discuss_r49.md` — This document

---

*Created: 2026-06-17 by PM*
*Source: docs/architecture/discuss_r49_architect.md, docs/state/challenge_r49.md, docs/state/handoff_discuss_r48.md*
