# discuss_r48_architect.md — Sprint 23 Architecture Analysis

**Date**: 2026-06-17
**Author**: System Architect (Round 48)
**Sprint**: Sprint 23 — C202 (MUST) + C199 (SHOULD) + C200 (COULD)
**Context**: Post-i18n refactoring (commit 7bcbc00)

---

## 1. Executive Summary

| Feature | Feasibility | Risk | Recommendation |
|---------|------------|------|----------------|
| **C202** Story Arc Labels | ✅ HIGH — service exists, integration incomplete | Low | Proceed; needs i18n wrapping |
| **C199** Bear vs Bull Debate Cards | ✅ MEDIUM — no service exists, but patterns are clear | Medium | Proceed with Tone QA gate |
| **C200** What If Calculator | ✅ MEDIUM-HIGH — C74 foundation exists (320 lines) | Medium-High | Proceed with Week 1 gate |

**Critical Blocker**: Dual locale directory conflict (`locales/` vs `src/core/locales/`) must be resolved before any i18n-dependent feature ships. The `i18n.py` code points to `locales/` (old, 225 lines) but commit 7bcbc00 created `src/core/locales/` (new, 130 lines, different schema). These are **incompatible** — the new directory is a subset with a different key structure.

---

## 2. i18n Conflict Analysis

### 2.1 The Dual Locale Directory Problem

**Root cause**: Commit 7bcbc00 created `src/core/locales/` with new YAML files but did NOT update `src/core/i18n.py` to point to them.

**Current state**:
- `src/core/i18n.py` line 11: `_LOCALE_DIR = Path(__file__).resolve().parent.parent.parent / "locales"` → resolves to **`locales/`** (project root)
- `locales/zh-TW.yaml`: **225 lines**, full key set (app, page, sidebar, stock, metric, dividend, action, status, timeline, error, validation, result, comparison, financial_statement, notification, memo, disclaimer, unit)
- `locales/en.yaml`: **216 lines**, full English translations
- `src/core/locales/zh-TW.yaml`: **130 lines**, subset (financial_wellness, unit, dividend, roe, format, business_card only)
- `src/core/locales/en.yaml`: **135 lines**, subset (same scope, English)

**Key structural difference**: The new `src/core/locales/` files have a **different schema** — they use top-level keys like `business_card`, `financial_wellness`, `dividend`, `roe`, `format` instead of the canonical `page`, `sidebar`, `metric`, etc. This appears to be a migration-in-progress that was never completed.

**Impact**: All `t()` calls in the codebase reference keys from the OLD `locales/` schema (e.g., `t("page.business_card")`, `t("status.loading")`). The new `src/core/locales/` files don't contain these keys at all. If someone switches `i18n.py` to point at `src/core/locales/`, **every translation will fall back to raw keys**.

### 2.2 Recommended Resolution

**Option A (Recommended): Keep `locales/` as canonical, delete `src/core/locales/`**

1. Delete `src/core/locales/` directory entirely
2. Keep `locales/zh-TW.yaml` and `locales/en.yaml` as the single source of truth
3. Add missing Sprint 23 keys (story_arc, debate, scenario) to both files
4. Rationale: Minimal disruption, all existing `t()` calls work as-is

**Option B: Migrate to `src/core/locales/` (higher effort)**

1. Merge all keys from `locales/` into `src/core/locales/` with consistent schema
2. Update `i18n.py` `_LOCALE_DIR` to point to `src/core/locales/`
3. Rationale: Co-locating locale files with i18n.py is cleaner long-term, but requires updating 24 files that were modified in commit 7bcbc00

**Recommendation: Option A**. The i18n refactoring is "complete" per the commit message. Don't reopen that can of worms. Just add the new keys needed for Sprint 23.

### 2.3 Missing i18n Keys for Sprint 23

The following keys need to be added to **both** `locales/zh-TW.yaml` and `locales/en.yaml`:

```yaml
# ── Story Arc Labels (C202) ──
story_arc:
  growth: "成長期"
  decline: "調整期"
  volatile: "震盪期"
  recovery: "復甦期"
  growth_desc: "過去6個月營收與市場評價偏向正面，整體趨勢向上"
  decline_desc: "過去6個月面臨較多負面事件，市場信心有所回落"
  volatile_desc: "過去6個月正負事件交織，市場看法分歧"
  recovery_desc: "調整後出現正面訊號，市場情緒逐步回暖"
  legend_title: "故事弧線圖例"
  period_label: "此區間共 {count} 個事件"
  section_title: "故事弧線"
  section_desc: "自動偵測公司故事的主要階段，幫助理解長期趨勢與轉折"

# ── Debate Cards (C199) ──
debate:
  title: "多方 vs 空方"
  bull_case: "多方論點"
  bear_case: "空方論點"
  evidence_balance: "證據平衡"
  more_bull: "多方證據較多"
  more_bear: "空方證據較多"
  balanced: "雙方證據相當"
  disclaimer: "以上論點由系統自動整理，僅供參考，不構成投資建議。"
  auto_generated_label: "自動產生"

# ── What If Calculator (C200) ──
scenario:
  title: "如果當時投資了？"
  input_label: "投資日期"
  amount_label: "投資金額"
  result_label: "至今價值"
  return_label: "報酬率"
  dividend_label: "含股息"
  disclaimer: "⚠️ 歷史情境為假設性試算，僅供教育用途，不構成投資建議。過去績效不代表未來表現。"
  no_data: "無法取得該日期的資料"
  before_ipos: "所選日期早於公司上市日期"
  featured_scenarios: "精選情境"
  custom_scenario: "自訂情境"
```

---

## 3. Feature-by-Feature Analysis

### 3.1 C202 — Story Arc Labels (MUST)

**Current state**:
- ✅ `src/services/story_arc_detector.py` exists (211 lines) — pure Python, no Streamlit imports
- ✅ `src/data/yaml/story_arcs.yaml` exists (38 lines) — arc label templates
- ✅ Integrated into `src/pages/story_timeline.py` (lines 196-204 call `detect_arcs()` and `_render_arc_badge()`)
- ❌ **i18n NOT applied**: All UI strings in `story_timeline.py` are hardcoded Chinese:
  - Line 74: `"📊 故事弧線圖例"`
  - Line 150: `f"📅 故事時間軸 — {display_name}"`
  - Line 152: `"*公司完整的故事時間軸：營收異動、新聞事件、歷史轉折與案例研究*"`
  - Line 160: `"時間範圍"`
  - Line 173: `f"載入時間軸時發生錯誤：{exc}"`
  - Line 179: `"目前沒有足夠的時間軸內容"`
  - Line 199: `"📈 故事弧線"`
  - Line 200: `"*自動偵測公司故事的主要階段，幫助理解長期趨勢與轉折*"`
  - Line 217: `"圖例說明"`
  - Line 220-224: Severity legend labels (🔴 重大事件, 🟡 重要事件, 🟢 參考事件)
  - Line 234-236: Disclaimer text
  - Arc badge labels in `_render_arc_badge()`: hardcoded `"📅 {bucket_start} ～ {bucket_end}"`, `"📌 此區間共 **{count}** 個事件"`
  - Arc type labels in `story_arc_detector.py`: hardcoded `"成長期"`, `"調整期"`, `"震盪期"`, `"復甦期"` and their descriptions
- ❌ Arc type labels in `story_arc_detector.py` are hardcoded as Python constants (lines 30-33) and in `_ARC_DESCRIPTIONS` dict (lines 42-47) — should reference i18n keys instead

**What's needed**:
1. Wrap all hardcoded strings in `story_timeline.py` with `t()` calls
2. Refactor `story_arc_detector.py` to accept arc labels from i18n (or at minimum, make the descriptions use `t()`)
3. Add missing keys to `locales/zh-TW.yaml` and `locales/en.yaml`
4. Add `"story_arc"` to the `PAGE_KEYS` list in `router.py` if arc labels need a dedicated page (currently they're embedded in `full_story_timeline` page)

**Updated effort estimate**: 9-14h → **10-16h** (added 1-2h for i18n wrapping that was missed in the original estimate)

**Architecture assessment**: The service layer is well-designed. `story_arc_detector.py` is a pure Python module with no Streamlit dependencies, good TypedDict typing, and clean separation. The integration into `story_timeline.py` follows the existing pattern. The only gap is the i18n wrapping.

### 3.2 C199 — Bear vs Bull Debate Cards (SHOULD)

**Current state**:
- ❌ `src/services/debate_engine.py` does **NOT exist**
- ❌ No debate-related code anywhere in the codebase
- ❌ No `debate_templates.yaml` exists
- This is a **greenfield feature**

**Recommended architecture**:

```
src/services/debate_engine.py          # Pure Python service (~150-200 lines)
src/data/yaml/debate_templates.yaml    # Evidence templates per metric (~100-150 lines)
src/pages/debate_cards.py              # Streamlit page renderer (~200-250 lines)
```

**Service design** (`debate_engine.py`):
```python
class DebatePoint(TypedDict):
    side: str          # "bull" or "bear"
    metric: str        # e.g., "roe", "revenue_yoy"
    value: float       # actual value
    peer_avg: float    # industry average
    argument: str      # generated argument text
    icon: str          # emoji
    strength: float    # 0.0-1.0 evidence strength

def generate_debate(data: dict, extra_metrics: dict) -> list[DebatePoint]:
    """Generate bull/bear arguments from stock data.
    
    Rules-based approach (no LLM):
    - Compare each metric vs industry average
    - Generate bull argument if metric > peer_avg
    - Generate bear argument if metric < peer_avg
    - Strength based on magnitude of difference
    - Max 6 points per side, min 1 per side
    """
```

**Page design** (`debate_cards.py`):
- Two-column layout: bull (left, green-tinted) vs bear (right, red-tinted)
- Each column shows 3-6 argument cards with metric name, value, and plain-language argument
- Evidence balance indicator at top (e.g., "🟢 多方證據較多" / "🔴 空方證據較多" / "🟡 雙方證據相當")
- Four-safeguard pattern (per A47-05):
  1. Disclaimer at bottom
  2. "自動產生" label on each card
  3. Data-driven points only (no speculation)
  4. Banned word list enforcement

**Router integration**: Add to `router.py`:
```python
from src.pages.debate_cards import render_debate_cards_page
# Add "debate_cards" to PAGE_KEYS
# Add elif branch in load_and_render_page()
```

**Updated effort estimate**: 10-16h → **12-18h** (added 2h for four-safeguard pattern implementation and Tone QA compliance)

**Risk**: Medium. The four-safeguard pattern and Tone QA gate are the main risks. The technical implementation is straightforward — it's a rules-based comparison engine, no LLM needed.

### 3.3 C200 — What If Calculator (COULD)

**Current state**:
- ✅ `src/pages/business_card/_historical_scenarios.py` exists (320 lines) — C74 implementation
- ✅ `src/data/yaml/historical_scenarios.yaml` exists — curated scenarios
- ❌ `src/services/scenario_calculator.py` does **NOT exist**
- ❌ No interactive calculator service exists
- The existing C74 is **curated/static** — pre-written scenarios for 10 major TW stocks
- C200 requires **interactive/generalized** — any date, any amount, any stock

**Recommended architecture**:

Extend C74 rather than replace it. The existing `_historical_scenarios.py` becomes the "Featured Scenarios" section, and a new `scenario_calculator.py` service adds the "Custom Scenario" calculator.

```
src/services/scenario_calculator.py                    # New: pure Python calculator (~150-200 lines)
src/pages/business_card/_historical_scenarios.py      # Modified: add custom calculator section
```

**Service design** (`scenario_calculator.py`):
```python
class ScenarioResult(TypedDict):
    start_date: str
    end_date: str
    start_price: float
    end_price: float
    shares: float           # shares bought with input amount
    total_return: float     # percentage
    absolute_return: float  # dollar amount
    dividend_income: float  # accumulated dividends
    annualized_return: float
    is_estimated: bool      # True if end_date is in the future or data incomplete

def calculate_scenario(
    stock_id: str,
    start_date: str,
    investment_amount: float,
    include_dividends: bool = True,
    client: FinMindClient | None = None,
) -> ScenarioResult:
    """Calculate what-if investment scenario.
    
    Pure calculation — no LLM.
    Uses FinMindClient for historical price and dividend data.
    Handles edge cases: pre-IPO dates, missing data, future dates.
    """
```

**Integration approach**: Add a new expander section "自訂情境" in `_historical_scenarios.py` below the existing curated scenarios. This keeps the curated content (which has been tone-tested) while adding the interactive calculator.

**Week 1 gate criteria** (from A47-07):
1. FinMind API caching validated — `get_daily_price()` and `get_dividend()` must use cache
2. Historian framing passes tone QA — no FOMO language, proper disclaimers

**Updated effort estimate**: 12-17h → **10-15h** (reduced because C74 foundation is solid — 320 lines of working code with `_scenario_card`, `_section_header`, `_historian_disclaimer` helpers already available)

**Risk**: Medium-High. The main risks are:
1. FinMind API rate limits for historical price data (mitigated by caching)
2. Edge cases: pre-IPO dates, stocks with missing data, future dates
3. Tone QA: must use historian framing, no FOMO language

---

## 4. Updated Sprint 23 Plan

| Priority | Feature | Effort | Risk | Go/No-Go Gate |
|----------|---------|--------|------|----------------|
| MUST | C202 Story Arc Labels | 10-16h | Low | Quality check on 3 test stocks (TSMC, 鴻海, 緯穎) + i18n wrapping complete |
| SHOULD | C199 Bear vs Bull Debate Cards | 12-18h | Medium | Tone QA gate — 2 revision max, then defer |
| COULD | C200 What If Calculator | 10-15h | Medium-High | Week 1: FinMind API caching + historian framing |
| **Total** | | **32-49h** | | |

### Implementation Order (unchanged)
1. **Week 1**: C202 (Story Arc) — quick win, lowest risk, but must include i18n wrapping
2. **Week 1-2**: C199 (Debate Cards) — parallel with C202 UI phase
3. **Week 2-3**: C200 (What If Calculator) — only if Week 1 gate passes

---

## 5. Blocking Issues

### 5.1 CRITICAL: Dual Locale Directory Conflict

**Issue**: `i18n.py` points to `locales/` but commit 7bcbc00 created `src/core/locales/` with an incompatible schema.

**Impact**: If not resolved, any new i18n keys added for Sprint 23 will be added to the wrong file, or the wrong file will be loaded at runtime.

**Resolution required before**: Any Sprint 23 feature that adds i18n keys.

**Recommended action**: Delete `src/core/locales/` directory. Keep `locales/` as canonical. Add Sprint 23 keys to `locales/zh-TW.yaml` and `locales/en.yaml`.

### 5.2 HIGH: story_timeline.py i18n Not Applied

**Issue**: The i18n refactoring (commit 7bcbc00) added `story_arc_detector.py` and integrated it into `story_timeline.py`, but the UI strings in `story_timeline.py` are NOT wrapped in `t()` calls — they're hardcoded Chinese.

**Impact**: C202 will ship with untranslatable strings, breaking the i18n contract for the `full_story_timeline` page.

**Resolution required before**: C202 ships.

### 5.3 MEDIUM: No debate_engine.py Exists

**Issue**: C199 is greenfield — no service, no templates, no page.

**Impact**: Higher implementation risk than C202 or C200.

**Mitigation**: The four-safeguard pattern and Tone QA gate (A47-05) must be implemented. Consider deferring to Sprint 24 if Tone QA fails twice.

### 5.4 LOW: _router_base.py Growth

**Issue**: `_router_base.py` is 579 lines. Adding more UI helpers will increase it further.

**Mitigation**: Monitor file size. If it exceeds 600 lines after Sprint 23, extract UI helpers to a separate `src/pages/_ui_helpers.py` module.

---

## 6. File Inventory

### Files that exist
| File | Lines | Status |
|------|-------|--------|
| `src/services/story_arc_detector.py` | 211 | ✅ Complete, needs i18n |
| `src/data/yaml/story_arcs.yaml` | 38 | ✅ Complete |
| `src/pages/story_timeline.py` | 236 | ⚠️ Needs i18n wrapping |
| `src/pages/business_card/_historical_scenarios.py` | 320 | ✅ C74 foundation |
| `src/data/yaml/historical_scenarios.yaml` | ~100 | ✅ C74 data |
| `src/pages/router.py` | 349 | ✅ Ready for new pages |
| `src/pages/_router_base.py` | 579 | ⚠️ Monitor size |
| `src/core/i18n.py` | 101 | ✅ Complete |
| `locales/zh-TW.yaml` | 225 | ✅ Canonical (add Sprint 23 keys) |
| `locales/en.yaml` | 216 | ✅ Canonical (add Sprint 23 keys) |

### Files that do NOT exist (need to be created)
| File | Estimated Lines | Purpose |
|------|----------------|---------|
| `src/services/debate_engine.py` | 150-200 | C199 debate logic |
| `src/data/yaml/debate_templates.yaml` | 100-150 | C199 evidence templates |
| `src/pages/debate_cards.py` | 200-250 | C199 page renderer |
| `src/services/scenario_calculator.py` | 150-200 | C200 calculator logic |

### Files that should be deleted
| File | Reason |
|------|--------|
| `src/core/locales/` (directory) | Incompatible schema, not used by i18n.py |

---

## 7. Key Architectural Decisions

1. **C202 arc labels stay in `story_timeline.py`** — no separate page needed; they're rendered inline at transition points
2. **C199 is a new page** (`debate_cards.py`) — it's a standalone feature that needs its own page key in the router
3. **C200 extends C74** — add "Custom Scenario" expander to existing `_historical_scenarios.py`, don't replace curated content
4. **All three features are stock-specific pages** — they need stock data, so they go through the `get_stock_data()` path in `router.py`
5. **No LLM dependency for any feature** — all three are rules-based, keeping complexity and cost low
6. **`locales/` is canonical** — delete `src/core/locales/` to avoid confusion

---

## 8. Test Plan

1. **C202**: Test arc detection on TSMC (2330), 鴻海 (2317), 緯穎 (6669) with 1Y/3Y/5Y lookback
2. **C199**: Tone QA review of all generated arguments — check against banned word list
3. **C200**: Test edge cases — pre-IPO date, future date, stock with no dividend data, API rate limit
4. **i18n**: Switch language to EN and verify all new strings render correctly

---

*Created: 2026-06-17 by System Architect*
*References: docs/architecture/i18n_integration.md, docs/state/handoff_discuss_r47.md, docs/architecture/discuss_r47_architect.md*
