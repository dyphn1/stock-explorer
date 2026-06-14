## Developer Cost Estimates — Round 38

> **Developer**: Developer Agent
> **Date**: 2026-06-14
> **Scope**: Sprint 18 validation (C139 + C141 + C143 + D-097 + Tone QA), new feature pipeline (C147, C149, C152), debt items (D-074, D-103)
> **Context**: Sprint 17 COMPLETE. Architecture 🟢 HEALTHY (44 services, 0 god modules). Design Grade A (5th consecutive).

---

### Sprint 18 Validation

| Item | PM Estimate | Dev Estimate | Verdict | Key Adjustment |
|------|------------|--------------|---------|----------------|
| **D-097** (Industry Context) | 1-2h | **1.5h** | ✅ Agree | Thread `industry` from `ExplanationRequest.context` into `TemplateExplanationProvider.explain()`. Add `industry` key to `_resolve_direction()` context-aware branching. Small change — 2 files: `template_provider.py` (+15 lines), `delta_engine.py` call site (+2 lines). |
| **C139** (Explain This Number) | 8-12h | **10-13h** | ✅ Agree | Extend existing `_render_metric_popover()` pattern. Create `_explain_button()` helper in `_router_base.py` (~40 lines). Wire into `_summary.py` top-3 metrics (3 locations), `_health.py` dimension cards (2 locations), `_story.py` delta cards (1 location). Each location: add `💡` button → `st.popover()` with `TemplateExplanationProvider` output. Reuses `metric_education.get_metric_explanation()` + `glossary_service` already wired. |
| **C141** (Source Badge) | 3-4h (bundled) | **2h** (bundled with C139) | ✅ Agree | `ExplanationResponse.source` already exists. Add `st.caption()` with `📊 系統估算` / `📊 FinMind` below each explanation text. Zero new components. Add during C139 implementation at each popover location. |
| **Tone QA Automation** | 2-3h | **2.5h** | ✅ Agree | Create `tests/test_tone_qa.py` with blocklist: 建議, 應該, 買, 賣, 推薦, 進場, 出場, 值得關注, 需要密切關注, 值得持續追蹤, 表現優於預期. Scan all template strings in `delta_explanation_provider.py` and `template_provider.py`. Add CI step to `pyproject.toml` or Makefile. **Prerequisite**: Must audit and fix existing blocklist violations first (see Risks). |
| **C143** (Implication Sentence) | 4-6h | **7-9h** | ✅ Agree | (1) Add `implication: str = ""` field to `ExplanationResponse` (backward-compatible). (2) Add 6 implication templates to `DeltaExplanationProvider` (3 metrics × 2 directions). (3) Replace delta card explanation with implication sentence; move existing explanation to 💡 popover. (4) Content creation: each implication must pass tone blocklist — budget 2h for writing + review. (5) Wire `_白话_card(label="觀察重點", ...)` with implication in analogy field. |
| **Total** | 22-31h | **23-28.5h** | ✅ Within range | Dev estimate lands at the lower-middle of PM range. Main variance: C139 at 10-13h (PM: 8-12h) due to 5-7 UI wiring locations; C143 at 7-9h (PM: 4-6h) due to content creation overhead. |

---

### New Feature Pipeline

| ID | Feature | Range | Confidence | Risk |
|----|---------|-------|------------|------|
| **C147** | Historical Event Pattern — "When This Happened Before, Here's What Followed" | **14-18h** | 🟡 Medium | **High complexity**: Requires new service module (`historical_event_pattern.py`) that queries historical delta events for the same stock, identifies recurring patterns, and generates narrative. Needs: (1) historical delta storage/retrieval (currently deltas are computed on-the-fly, not stored), (2) pattern matching logic (same metric, similar magnitude, time-proximity), (3) template-based "what followed" narrative generation. **Architecture risk**: May require new data layer (event history table) or caching layer. Recommend spike (2h) before committing to full implementation. |
| **C149** | "So What?" Implication Box — Dedicated Visual Implication UI | **10-14h** | 🟢 High | **Medium complexity**: New shared component `_implication_box()` in `_router_base.py` with amber background (`#FFF8E1`), `💡 這代表什麼?` header, 14px implication text, expand for detail. Wire into 3-4 page locations. Design spec already documented in review38_design.md. Reuses C143 implication content. Lower risk than C147 because it's a presentation-layer change on top of existing content. |
| **C152** | Multi-Factor Event Narratives — One Story, All Factors Combined | **16-20h** | 🟡 Medium | **Highest complexity**: Requires new `narrative_engine.py` service that takes multiple delta events (revenue + price + margin) and generates a single coherent narrative. Needs: (1) event correlation logic (same time window, same stock), (2) narrative template system with multiple factor slots, (3) tone QA for combined narratives, (4) integration with `delta_engine.py` output. **Dependency**: Builds on C147's historical pattern infrastructure. Recommend C147 → C152 sequencing. |

---

### Debt Items

| ID | Description | Estimate | Priority |
|----|-------------|----------|----------|
| **D-074** | filelock fix — Add `filelock>=3.0.0` to `pyproject.toml` or mock in `conftest.py` | **0.25h** | 🔴 Sprint 18 Day 1 — blocks all tests |
| **D-103** | DeltaExplanationProvider tests — 179-line module, 3 template dicts × 2 directions × 3 thresholds + generic fallback | **1.5h** | 🟡 Sprint 18 early — prerequisite for C139/C143 |
| **D-104** | settings_service tests — 16-line module, `get_threshold()` function | **0.25h** | 🟢 Deferrable — trivial |
| **D-107** | Extract shared benchmark function (summary.py → shared service) | **1.5h** | 🟡 Sprint 19 — alongside D-105 YAML migration |
| **D-111** | Remove dead code `self._template_provider.is_available()` call (line 169) | **0.1h** | 🟢 Quick fix alongside D-103 |

---

### Critical Risks

1. **🔴 Tone blocklist violations in existing templates BLOCK C143 and Tone QA**
   - `delta_explanation_provider.py` line 30: `"值得關注後續動能"` — contains blocklist term `值得關注`
   - `delta_explanation_provider.py` line 31: `"表現優於預期"` — contains blocklist term `表現優於預期`
   - `delta_explanation_provider.py` line 35: `"需要密切關注"` — contains blocklist term `需要密切關注`
   - **Impact**: If Tone QA CI is implemented first, these existing templates will immediately fail. If C143 ships first without fixing these, the implication sentences will contain blocked phrases. **Must fix templates before either C143 or Tone QA ships.** Budget 1-2h for template audit + rewrite. This is a hidden dependency that makes D-097 → Tone QA → C143 the critical path.

2. **🟡 C139 scope: 5-7 metrics across multiple section files creates wiring complexity**
   - The existing `_render_metric_popover()` in `_financial.py` is tightly coupled to that section's layout (uses `st.columns([5, 1])` with `_白话_card`). C139 must wire into `_summary.py` (top-3 metrics), `_health.py` (dimension cards), and `_story.py` (delta cards) — each with different card rendering patterns. The `_explain_button()` helper must be flexible enough to work inside `_白话_card()`, `_info_card()`, and standalone column layouts. **Mitigation**: Build `_explain_button()` as a pure function accepting `key` and `content` params, not coupled to any card type.

3. **🟡 C147 (Historical Event Pattern) requires architectural spike before commitment**
   - Current `delta_engine.py` computes deltas on-the-fly from API data — there is no historical event store. C147 needs to query "when did this same pattern happen before?" which requires either: (a) a new `event_history.yaml` or SQLite table populated on each stock view, or (b) re-computing deltas from full historical data on each request (expensive). Option (a) adds infrastructure; option (b) adds latency. **Recommendation**: 2h spike to evaluate feasibility before committing to the 14-18h range.

4. **🟢 D-074 filelock regression persistence (3+ sprints)**
   - Low effort (0.25h) but has persisted since Round 26. The fix is trivial (add `filelock` to `pyproject.toml` or mock in `conftest.py`). However, every sprint that defers it means 2 test files fail at collection time, reducing confidence in CI. **Recommendation**: Fix on Sprint 18 Day 1, no exceptions.

---

### Sprint 18 Execution Order (Recommended)

| Order | Task | Estimate | Dependencies |
|-------|------|----------|-------------|
| 1 | **D-074** filelock fix | 0.25h | None |
| 2 | **D-103** DeltaExplanationProvider tests | 1.5h | D-074 |
| 3 | **D-097** Industry context threading | 1.5h | D-103 (verify protocol works) |
| 4 | **Template audit + rewrite** (tone blocklist) | 1.5h | D-097 (templates must be clean before C143) |
| 5 | **C139** Explain This Number | 10-13h | D-097, template audit |
| 6 | **C141** Source Badge (bundled) | 2h | During C139 |
| 7 | **Tone QA Automation** | 2.5h | Template audit complete |
| 8 | **C143** Implication Sentence | 7-9h | C139, template audit, Tone QA |
| | **Total** | **23-28.5h** | |

---

### Summary

- **Sprint 18 total**: **23-28.5h** (within PM range of 22-31h)
- **Critical path**: D-074 → D-103 → D-097 → Template Audit → C139+C141 → Tone QA → C143
- **Biggest risk**: Tone blocklist violations in existing templates (3 violations in `delta_explanation_provider.py`) must be fixed before C143 or Tone QA. This is a hidden 1.5h task not explicitly in the sprint plan.
- **Pipeline**: C147 (14-18h) recommended for Sprint 19 with a 2h spike first. C149 (10-14h) and C152 (16-20h) for Sprint 19-20.
- **Debt**: D-074 (0.25h) is Day 1 mandatory. D-103 (1.5h) is early-sprint recommended. D-104 (0.25h) is deferrable.

*Created: 2026-06-14 (Round 38)*
*Reviewer: Developer Agent*
*Next: Development Round 39 (Sprint 18 execution)*
