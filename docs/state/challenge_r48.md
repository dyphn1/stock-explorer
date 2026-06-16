# Challenge – Round 48 (Sprint 23 Pre-Development)

**Date**: 2026-06-17
**Author**: Challenger (Round 48)
**Sprint**: Sprint 23 — C202 (MUST) + C199 (SHOULD) + C200 (COULD)
**Context**: Post-i18n refactoring (commit 7bcbc00), 458 tests passing

---

## Executive Verdict

**⚠️ CONDITIONAL ALIGNED** — Sprint 23 can proceed, but **three critical blockers must be resolved before any feature ships**, and the effort estimate needs a floor adjustment.

---

## 1. Critical Blocker: Dual Locale Directory Conflict

**Severity**: 🔴 CRITICAL — Must be resolved before Sprint 23 development begins.

**The problem**: There are two incompatible locale directories in the codebase:

| Directory | Lines (zh-TW) | Schema | Used by `i18n.py`? |
|-----------|---------------|--------|---------------------|
| `locales/` (project root) | 225 | `app`, `page`, `metric`, `status`, `unit`, etc. | ✅ YES — `i18n.py` line 11 points here |
| `src/core/locales/` (new in 7bcbc00) | 130 | `financial_wellness`, `business_card`, `dividend`, `roe`, etc. | ❌ NO — orphaned |

These schemas are **incompatible**. The `src/core/locales/` files use top-level keys like `business_card.simple_mode.health_title` that don't exist in the canonical `locales/` files, and vice versa. Commit 7bcbc00 created the new directory but never updated `i18n.py` to point to it, making the new directory dead code.

**Risk**: If Sprint 23 developers add i18n keys to the wrong directory, translations will silently fail at runtime (the `t()` function falls back to returning the raw key, so there's no crash — just untranslated Chinese strings).

**Challenger's demand**: **Pick one directory and delete the other BEFORE Sprint 23 coding starts.** The Architect recommends keeping `locales/` and deleting `src/core/locales/`. The Challenger agrees — Option A is the only safe choice. Migrating (Option B) would require re-auditing every `t()` call in the codebase, which is a separate sprint's work.

**❓ Question 1**: Has the team formally decided to delete `src/core/locales/`? Who is responsible for this cleanup, and will it be done before or during Sprint 23? "During" is not acceptable — it must be "before" to avoid confusion.

---

## 2. Critical Blocker: C202 Is NOT i18n-Compliant

**Severity**: 🔴 CRITICAL — C202 cannot ship as-is.

**The problem**: `story_timeline.py` contains at least **15 hardcoded Chinese strings** that are not wrapped in `t()` calls. Specifically:

| Line | Hardcoded String | Should Be |
|------|-----------------|-----------|
| 74 | `"📊 故事弧線圖例"` | `t("story_arc.legend_title")` |
| 150 | `f"📅 故事時間軸 — {display_name}"` | `t("story_arc.page_title", name=display_name)` |
| 152 | `"*公司完整的故事時間軸：營收異動、新聞事件、歷史轉折與案例研究*"` | `t("story_arc.page_desc")` |
| 160 | `"時間範圍"` | `t("timeline.range_label")` |
| 173 | `f"載入時間軸時發生錯誤：{exc}"` | `t("timeline.load_error", error=exc)` |
| 179 | `"目前沒有足夠的時間軸內容"` | `t("timeline.empty_title")` |
| 199 | `"📈 故事弧線"` | `t("story_arc.section_title")` |
| 200 | `"*自動偵測公司故事的主要階段，幫助理解長期趨勢與轉折*"` | `t("story_arc.section_desc")` |
| 217 | `"圖例說明"` | `t("timeline.legend_title")` |
| 220-224 | Severity legend labels | `t("timeline.severity.high")`, etc. |
| 234-236 | Disclaimer text | `t("disclaimer.historical")` |

Additionally, `story_arc_detector.py` has **hardcoded Chinese constants** (lines 30-33) and a hardcoded `_ARC_DESCRIPTIONS` dict (lines 42-47) that feed directly into the UI. These are the arc labels: `"成長期"`, `"調整期"`, `"震盪期"`, `"復甦期"`. Even though this is a "service layer" module, its output is rendered directly in the UI.

**The `story_arcs.yaml` file** (38 lines) duplicates these same Chinese strings — but it's also an i18n-unaware YAML file sitting in `src/data/yaml/`, not in the locale system.

**❓ Question 2**: Should `story_arc_detector.py` be refactored to return translation keys instead of Chinese text, wrapping to `t()` at the page level? Or should the service layer call `t()` directly? The current approach — returning raw Chinese from the service layer — breaks the i18n contract and makes the `full_story_timeline` page untranslatable.

**❓ Question 3**: Is the `story_arcs.yaml` file redundant now that we have locale YAML files? Should it be merged into `locales/zh-TW.yaml` under a `story_arc:` namespace, or is it serving a different purpose (e.g., thresholds/configuration vs. display text)? The Challenger believes it's a config file that should NOT contain display strings.

**Effort impact**: The Architect added +1-2h for i18n wrapping (10-16h range). The Challenger believes this is **underestimated** — refactoring `story_arc_detector.py` to separate display text from detection logic, adding all new keys to both locale files, and testing in English mode is more like **3-4h**. This brings C202 to **11-18h**.

---

## 3. Feasibility Concern: C199 Is Full Greenfield

**Severity**: 🟡 MEDIUM — The plan underestimates the greenfield scope.

**The plan says** (line 98 of handoff_discuss_r47.md): *"All three features are independent of Sprint 21/22 work — no blocking dependencies."*

**The reality**: C199 has zero existing code. The plan estimates 10-16h (Architect says 12-18h). Let's inventory what needs to be created from scratch:

| Component | Estimated Lines | Dependencies |
|-----------|----------------|--------------|
| `src/services/debate_engine.py` | 150-200 | `financial_metrics.py`, `risk_analyzer.py` |
| `src/data/yaml/debate_templates.yaml` | 100-150 | PM content review |
| `src/pages/debate_cards.py` | 200-250 | `router.py` modification, `_router_base.py` helpers |
| Four-safeguard pattern | +2-3h | PM + Designer Tone QA |
| Banned word list | +20 entries | PM |
| i18n keys for all UI strings | +1-2h | Both locale files |
| L0 unit tests | 2-3h | Threshold branches, missing data, balance |

**Total realistic estimate**: 14-22h, not 12-18h. The upper bound exceeds the original 16h estimate by 6h.

**❓ Question 4**: The four-safeguard pattern (disclaimer, "自動產生" label, data-driven points, banned word list) is listed as a separate action item (A47-05) with Designer + PM ownership. Has this pattern been designed yet? If not, the developer cannot start C199 implementation — the safeguards affect the data model (e.g., `DebatePoint` needs a `source_type` field for the "自動產生" label, a `confidence` field for evidence strength, and banned word filtering on the `argument` field).

**❓ Question 5**: The plan says C199 can run "parallel with C202 UI phase." But if the four-safeguard pattern isn't defined, C199 can't start at all. Should we formally add a **pre-sprint dependency**: "A47-05 must be complete before C199 service development begins"?

---

## 4. Feasibility Concern: C200 Depends on FinMind API Behavior

**Severity**: 🟡 MEDIUM — The Week 1 gate may be harder than expected.

**The plan assumes**: Existing C74 code (320 lines) provides a solid foundation.

**The reality**: C74 is a **static, curated** page. It has hardcoded scenarios for 10 stocks. C200 requires:
- `FinMindClient.get_daily_price()` for arbitrary date ranges
- `FinMindClient.get_dividend()` for the same stock
- Real-time calculation of shares, returns, CAGR
- Handling edge cases: pre-IPO, non-trading dates, split-adjusted prices

The existing C74 `_historical_scenarios.py` doesn't call `get_daily_price()` — it displays pre-computed scenarios. The helpers (`_scenario_card`, `_section_header`, `_historian_disclaimer`) are UI-only. The actual calculation logic doesn't exist.

**❓ Question 6**: Has anyone tested `FinMindClient.get_daily_price()` with a 5+ year date range to verify it returns complete data? If the API paginates or truncates results, the calculator will silently produce wrong numbers. The Week 1 gate should include a **data completeness verification**: fetch 5 years of daily data for TSMC and verify no gaps > 5 trading days.

**❓ Question 7**: The C74 page is 320 lines. Adding an interactive calculator section (date input, amount slider, results display, chart with buy-date line) could push it to 450+ lines. The Architect flagged `_router_base.py` growth as LOW risk — isn't `_historical_scenarios.py` growth also a concern? Should we pre-emptively create a `_scenario_calculator.py` UI helper module?

**Effort impact**: The Architect actually *reduced* the estimate to 10-15h from 12-17h. The Challenger disagrees — the Week 1 gate work (API validation + caching + historian framing) is **not** implementation effort, it's **risk reduction effort**. If the gate fails, all subsequent effort is wasted. Realistically, C200 is still 12-17h, and the Week 1 gate adds 2-3h of validation work. The reduced estimate is false precision.

---

## 5. Cumulative Sprint Load: 31-47h Is No Longer Valid

**Original estimate** (handoff_discuss_r47.md, line 31):
| Feature | Original | Revised (Architect) | Revised (Challenger) |
|---------|----------|---------------------|---------------------|
| C202 | 9-14h | 10-16h | 11-18h |
| C199 | 10-16h | 12-18h | 14-22h |
| C200 | 12-17h | 10-15h | 12-17h (+2-3h gate) |
| **Total** | **31-47h** | **32-49h** | **37-57h** (+2-3h gate) |

**The Challenger's floor estimate is 37h** (if everything goes right), and the ceiling is **59h** (if Week 1 gate work is included). This is significantly above the original 31-47h range.

**❓ Question 8**: The sprint has implicit capacity constraints. If the real estimate is 37-59h instead of 31-47h, does the team have capacity for all three features? Should C200 be **pre-committed to deferral** — i.e., only start C200 if C202 and C199 together take < 30h? The current plan already has a Week 1 go/no-go gate for C200, but the Challenger recommends making the **deferral criteria explicit and numeric**.

---

## 6. Hard Questions That Must Be Answered Before Sprint 23 Begins

These are not suggestions. These are **preconditions** that the Challenger requires to be resolved before approving Sprint 23 development.

### Must Answer (Blocking)

| # | Question | Owner | Deadline |
|---|----------|-------|----------|
| Q1 | Which locale directory is canonical? Delete the other one. | Developer | Before Sprint 23 Day 1 |
| Q2 | How will `story_arc_detector.py` output be i18n-wrapped? Keys or direct `t()`? | Architect + Developer | Before Sprint 23 Day 1 |
| Q3 | Is `story_arcs.yaml` config or display text? If display text, merge into locale files. | PM + Developer | Before Sprint 23 Day 1 |
| Q4 | Is the four-safeguard pattern (A47-05) designed? C199 service cannot start without it. | Designer + PM | Before C199 development |
| Q5 | Has `get_daily_price()` been tested with 5Y date ranges? | Developer | Sprint 23 Week 1 Gate |

### Should Answer (Strongly Recommended)

| # | Question | Owner | Deadline |
|---|----------|-------|----------|
| Q6 | What numeric criteria trigger C200 deferral to Sprint 24? | PM | Before Sprint 23 Day 1 |
| Q7 | Should `_historical_scenarios.py` be split before adding calculator UI? | Architect | Before C200 development |
| Q8 | Is the 37-59h revised estimate acceptable sprint capacity? | PM | Before Sprint 23 Day 1 |
| Q9 | How should arc type descriptions be sourced — from locale YAML or from `story_arcs.yaml`? One must be canonical. | Architect + PM | Before Sprint 23 Day 1 |

---

## 7. Summary of Findings

### What's Solid
- ✅ `story_arc_detector.py` is well-designed: pure Python, clean TypedDict types, good algorithm
- ✅ 327 lines of unit tests for `story_arc_detector.py` — thorough coverage
- ✅ C74 `_historical_scenarios.py` exists (320 lines) with reusable UI helpers
- ✅ `i18n.py` module works correctly (loads YAML, resolves nested keys, handles fallback)
- ✅ Locale files `locales/zh-TW.yaml` (225 lines) and `locales/en.yaml` (216 lines) are complete and canonical

### What's Broken
- 🔴 Dual locale directory conflict — `src/core/locales/` is dead code with incompatible schema
- 🔴 `story_timeline.py` has 15+ hardcoded Chinese strings not wrapped in `t()`
- 🔴 `story_arc_detector.py` returns hardcoded Chinese text from the service layer

### What's Missing
- 🟡 `debate_engine.py` — full greenfield, 5 files/modules to create
- 🟡 `scenario_calculator.py` — greenfield service on top of existing C74
- 🟡 Four-safeguard pattern for C199 — not yet designed
- 🟡 `debate_templates.yaml` — content not yet created
- 🟡 All i18n keys for Sprint 23 features — not yet added to locale files

### What Needs Re-Estimating
- 🟡 Total sprint load is 37-59h, not 31-47h (+20-25% over original)
- 🟡 C199 is 14-22h, not 10-16h (+37-50% over original)
- 🟡 C202 is 11-18h, not 9-14h (+22-29% over original)

---

## 8. Challenger Recommendations

1. **Before Sprint 23 coding starts**: Resolve Q1-Q3 (locale conflict, i18n strategy, story_arcs.yaml). Estimated time: 2-3h.

2. **Before C199 development starts**: Resolve Q4 (four-safeguard pattern). This is a hard dependency.

3. **Set explicit deferral criteria for C200**: e.g., "If C202 + C199 combined exceed 30h, C200 is automatically deferred to Sprint 24."

4. **Add +2-3h to the Sprint 23 plan for the Week 1 gate work** (FinMind API validation + historian framing validation). This is currently unaccounted for in the 31-47h estimate.

5. **Delete `src/core/locales/` immediately** — it's a trap for any developer who doesn't read `i18n.py` line 11.

6. **Standardize the i18n approach for service-layer modules**: Either services return keys and pages call `t()`, or services call `t()` directly. Document the decision. Currently `story_arc_detector.py` does neither — it returns raw Chinese.

---

*Created: 2026-06-17 by Challenger*
*References: docs/state/handoff_discuss_r47.md, docs/architecture/discuss_r48_architect.md, docs/architecture/i18n_integration.md*
