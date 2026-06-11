# D24: business_card.py Sub-Directory Extraction Plan

> **Status**: Ready for implementation
> **Created**: 2026-06-12
> **Author**: System Architect
> **Priority**: CRITICAL — Must be FIRST task of Sprint 4

---

## 1. Problem Statement

`src/pages/business_card.py` is **561 lines** and contains **11 distinct rendering sections** plus shared helpers. The file grew from ~337 lines (Round 9) to 561 lines after C37 (Key Takeaways), C39 (Recent Deltas), C43 (Health Snowflake), C44 (Risk Analysis), and C41 (Read Next). Two more features are planned for Sprint 4:

- **C38** (Compare Stories): ~50 lines
- **C48** (Company Story Card): ~70 lines

Without D24, the file will reach **~681 lines**, making it the largest page file and hardest to navigate.

### Current Line Budget

| Section | Lines | % of file |
|---------|-------|-----------|
| Imports + module helpers | 1–83 | 15% |
| `_render_business_card()` signature + data extraction | 84–95 | 2% |
| Header (watchlist buttons, popup) | 96–181 | 15% |
| Key Takeaways (C37) | 183–195 | 2% |
| Recent Deltas (C39) | 197–217 | 4% |
| Health Snowflake (C43) | 219–254 | 6% |
| Risk Analysis (C44) | 256–274 | 3% |
| One-liner + Company Facts | 276–290 | 3% |
| Key Metrics Triple Cards | 292–321 | 5% |
| Dividend Story | 324–431 | 19% |
| Revenue Breakdown (pie chart) | 434–448 | 3% |
| Revenue Trend | 451–457 | 1% |
| Valuation Band | 460–480 | 4% |
| Recent News | 484–499 | 3% |
| Read Next (C41) | 501–556 | 10% |
| Footer (Disclaimer) | 558–561 | 1% |
| **Total** | **561** | **100%** |

---

## 2. Target Directory Structure

```
src/pages/business_card/
    __init__.py       # Re-exports _render_business_card (backward compat)
    _main.py          # Orchestrator: _render_business_card() + data extraction
    _sections.py      # 14 section rendering functions
    _helpers.py       # Shared helpers: get_health_dimension_explanation, _RISK_BADGES, _RISK_COLORS, _render_risk_dimension
```

**Total: 4 files** (replacing 1 file of 561 lines)

---

## 3. File-by-File Specification

### 3.1 `src/pages/business_card/__init__.py`

**Purpose**: Preserve backward compatibility with `from src.pages.business_card import _render_business_card` (router.py line 14).

**Content**:
```python
"""Business card page — sub-directory extraction (D24)."""
from src.pages.business_card._main import _render_business_card

__all__ = ["_render_business_card"]
```

**Size**: ~5 lines

**Rationale**: The router.py import `from src.pages.business_card import _render_business_card` must continue to work. When Python imports `src.pages.business_card`, it executes `src/pages/business_card/__init__.py`. By re-exporting from `_main.py`, the public API is preserved exactly.

---

### 3.2 `src/pages/business_card/_helpers.py`

**Purpose**: Shared helper functions and constants used by multiple sections.

**Source**: Lines 43–83 of current `business_card.py`

**Contents**:

| Item | Source Lines | Type | Used By |
|------|-------------|------|---------|
| `get_health_dimension_explanation(dim_name, score)` | 43–50 | Function | `_render_health()` in `_sections.py` |
| `_RISK_BADGES` | 53–57 | Dict constant | `_render_risk_dimension()` |
| `_RISK_COLORS` | 59–63 | Dict constant | `_render_risk_dimension()` |
| `_render_risk_dimension(dim, stock_name)` | 66–83 | Function | `_render_risk()` in `_sections.py` |

**Imports needed**:
```python
import streamlit as st
```

**Size**: ~40 lines

---

### 3.3 `src/pages/business_card/_main.py`

**Purpose**: Orchestrator function that extracts data from the `data` dict and delegates to section renderers.

**Source**: Lines 84–95 (signature + data extraction) + section dispatch logic

**Contents**:

```python
"""Business card main orchestrator."""
import streamlit as st
import pandas as pd
from datetime import datetime, date

# Service imports (same as current business_card.py lines 9-40)
from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart, create_health_snowflake
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner, get_per_analogy, get_dividend_analogy,
    get_gross_margin_analogy, get_revenue_analogy, get_yoy_analogy,
    get_roe_analogy, get_pbr_analogy,
    generate_key_takeaways, compute_recent_deltas, compute_health_scores,
    get_health_summary,
)
from src.services.risk_analyzer import assess_risk
from src.services.dividend_analyzer import extract_dividend_summary
from src.services.news_summarizer import summarize_news, get_news_impact_level
from src.services.company_facts import get_company_facts
from src.services.watchlist import (
    is_in_watchlist, is_in_any_list, get_lists_for_stock,
    add_to_watchlist, remove_from_all_lists, remove_from_watchlist,
    create_list, list_names,
)
from src.pages._router_base import _白话_card, _info_card, _summary_card
from src.pages.url_sync import navigate_to

# Sub-section imports
from src.pages.business_card._sections import (
    _render_header,
    _render_takeaways,
    _render_deltas,
    _render_health,
    _render_risk,
    _render_one_liner,
    _render_key_metrics,
    _render_dividend,
    _render_revenue_breakdown,
    _render_revenue_trend,
    _render_valuation,
    _render_news,
    _render_read_next,
    _render_footer,
)


def _render_business_card(data: dict, client):
    """公司名片主頁（M1）— orchestrator"""
    # ── Data extraction (lines 86-94) ──
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    latest_price = data["latest_price"]
    latest_per_pbr = data["latest_per_pbr"]
    monthly_revenue = data["monthly_revenue"]
    financial = data["financial"]
    news = data["news"]
    extra_metrics = data["extra_metrics"]

    # ── Section dispatch ──
    _render_header(data, client)
    _render_takeaways(data, client)
    _render_deltas(data, client)
    _render_health(data, client)
    _render_risk(data, client)
    _render_one_liner(data, client)
    _render_key_metrics(data, client)
    _render_dividend(data, client)
    _render_revenue_breakdown(data, client)
    _render_revenue_trend(data, client)
    _render_valuation(data, client)
    _render_news(data, client)
    _render_read_next(data, client)
    _render_footer(data, client)
```

**Size**: ~60 lines

**Key Design Decision**: The orchestrator extracts all data variables from the `data` dict and passes the full `data` dict to each section function. Each section extracts only what it needs. This avoids a parameter explosion (14 functions × 8+ params = 112 parameters) while keeping the `data` dict as the single source of truth.

**Alternative considered**: Passing individual variables as parameters to each section. Rejected because:
1. The `data` dict already contains everything needed
2. Future sections (C38, C48) may need additional fields — no signature changes needed
3. Consistent with the existing `_render_business_card(data, client)` signature

---

### 3.4 `src/pages/business_card/_sections.py`

**Purpose**: All 14 section rendering functions, each taking `(data, client)` as parameters.

**Size**: ~450 lines total (same rendering logic, just reorganized)

#### Function Inventory

| # | Function | Source Lines | Lines | Description |
|---|----------|-------------|-------|-------------|
| 1 | `_render_header()` | 96–181 | ~86 | Watchlist header with stock name, price, watchlist buttons + popup |
| 2 | `_render_takeaways()` | 183–195 | ~13 | C37 Key Takeaways via `generate_key_takeaways()` |
| 3 | `_render_deltas()` | 197–217 | ~21 | C39 Recent Deltas via `compute_recent_deltas()` |
| 4 | `_render_health()` | 219–254 | ~36 | C43 Health Snowflake chart + 5-dimension score cards + summary |
| 5 | `_render_risk()` | 256–274 | ~19 | C44 Risk Analysis with expandable dimensions |
| 6 | `_render_one_liner()` | 276–290 | ~15 | One-liner + rotating company facts tip card |
| 7 | `_render_key_metrics()` | 292–321 | ~30 | Triple cards: PER/gross margin, revenue/ROE, dividend yield/PBR |
| 8 | `_render_dividend()` | 324–431 | ~108 | Dividend story: countdown, summary, mini-cards, expandable history table |
| 9 | `_render_revenue_breakdown()` | 434–448 | ~15 | Revenue pie chart + plain-language descriptions |
| 10 | `_render_revenue_trend()` | 451–457 | ~7 | Revenue trend chart or "no data" message |
| 11 | `_render_valuation()` | 460–480 | ~21 | Valuation band chart + interpretation card |
| 12 | `_render_news()` | 484–499 | ~16 | Recent news with impact level badges |
| 13 | `_render_read_next()` | 501–556 | ~56 | C41 Read Next: peer stocks + curated fun facts |
| 14 | `_render_footer()` | 558–561 | ~4 | Disclaimer |

**Imports needed**:
```python
import streamlit as st
import pandas as pd
from datetime import datetime, date

from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart, create_health_snowflake
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_one_liner, get_per_analogy, get_dividend_analogy,
    get_gross_margin_analogy, get_revenue_analogy, get_yoy_analogy,
    get_roe_analogy, get_pbr_analogy,
    generate_key_takeaways, compute_recent_deltas, compute_health_scores,
    get_health_summary,
)
from src.services.risk_analyzer import assess_risk
from src.services.dividend_analyzer import extract_dividend_summary
from src.services.news_summarizer import summarize_news, get_news_impact_level
from src.services.company_facts import get_company_facts
from src.services.watchlist import (
    is_in_watchlist, is_in_any_list, get_lists_for_stock,
    add_to_watchlist, remove_from_all_lists, remove_from_watchlist,
    create_list, list_names,
)
from src.pages._router_base import _白话_card, _info_card, _summary_card
from src.pages.url_sync import navigate_to
from src.pages.business_card._helpers import (
    get_health_dimension_explanation,
    _render_risk_dimension,
)
```

**Function signatures** (all follow the same pattern):

```python
def _render_header(data: dict, client) -> None:
    """Watchlist header with stock name, price, watchlist buttons."""

def _render_takeaways(data: dict, client) -> None:
    """C37 Key Takeaways section."""

# ... etc for all 14 functions
```

---

## 4. Data Flow

```
router.py
  │
  ├── from src.pages.business_card import _render_business_card
  │         │
  │         └── __init__.py ──re-exports──> _main.py::_render_business_card
  │
  └── _render_business_card(data, client)
            │
            ├── extracts: stock_id, stock_name, industry, latest_price,
            │            latest_per_pbr, monthly_revenue, financial,
            │            news, extra_metrics
            │
            ├── delegates to _sections.py functions (each receives data + client):
            │     ├── _render_header(data, client)
            │     ├── _render_takeaways(data, client)
            │     ├── _render_deltas(data, client)
            │     ├── _render_health(data, client)  ──uses──> _helpers.py
            │     ├── _render_risk(data, client)    ──uses──> _helpers.py
            │     ├── _render_one_liner(data, client)
            │     ├── _render_key_metrics(data, client)
            │     ├── _render_dividend(data, client)
            │     ├── _render_revenue_breakdown(data, client)
            │     ├── _render_revenue_trend(data, client)
            │     ├── _render_valuation(data, client)
            │     ├── _render_news(data, client)
            │     ├── _render_read_next(data, client)
            │     └── _render_footer(data, client)
            │
            └── each section extracts what it needs from data dict
```

---

## 5. Dependency Analysis

### 5.1 What `_sections.py` needs from `_helpers.py`

| Helper | Used by Section | Why |
|--------|----------------|-----|
| `get_health_dimension_explanation()` | `_render_health()` | Line 246: renders plain-language score explanation |
| `_render_risk_dimension()` | `_render_risk()` | Line 274: renders each risk dimension card |
| `_RISK_BADGES` | `_render_risk_dimension()` | Line 68: looks up badge text by risk level |
| `_RISK_COLORS` | `_render_risk_dimension()` | Line 69: looks up color by risk level |

### 5.2 What each section needs from the `data` dict

| Section | data keys used |
|---------|---------------|
| `_render_header` | `stock_id`, `stock_name`, `industry`, `latest_price` |
| `_render_takeaways` | `stock_id`, `stock_name`, `industry`, `extra_metrics`, `latest_per_pbr`, `monthly_revenue`, `financial` |
| `_render_deltas` | `extra_metrics`, `monthly_revenue`, `daily_price`, `latest_per_pbr` |
| `_render_health` | `extra_metrics`, `latest_per_pbr`, `financial`, `monthly_revenue` |
| `_render_risk` | (entire `data` dict — passed to `assess_risk(data)`) |
| `_render_one_liner` | `stock_id`, `stock_name`, `industry` |
| `_render_key_metrics` | `latest_per_pbr`, `extra_metrics`, `monthly_revenue` |
| `_render_dividend` | `latest_price`, `dividend` |
| `_render_revenue_breakdown` | `financial`, `stock_id`, `industry` |
| `_render_revenue_trend` | `monthly_revenue`, `stock_name` |
| `_render_valuation` | `daily_price`, `financial`, `latest_per_pbr`, `stock_id`, `stock_name` |
| `_render_news` | `news`, `stock_name` |
| `_render_read_next` | `industry`, `stock_id`, `stock_name` |
| `_render_footer` | (none — static text) |

### 5.3 What each section needs from `client`

| Section | Uses `client`? | How |
|---------|---------------|-----|
| `_render_header` | No | Watchlist functions are direct imports |
| `_render_takeaways` | No | Service functions only |
| `_render_deltas` | No | Service functions only |
| `_render_health` | No | Service functions only |
| `_render_risk` | No | `assess_risk(data)` only |
| `_render_one_liner` | No | Service functions only |
| `_render_key_metrics` | No | Service functions only |
| `_render_dividend` | No | Service functions only |
| `_render_revenue_breakdown` | No | Service functions only |
| `_render_revenue_trend` | No | Service functions only |
| `_render_valuation` | No | Service functions only |
| `_render_news` | No | Service functions only |
| `_render_read_next` | **Yes** | `client.get_stock_info()` for peer stocks |
| `_render_footer` | No | Static text |

**Note**: Only `_render_read_next()` uses the `client` parameter. However, all sections receive it for consistency and future-proofing (e.g., C38 Compare Stories may need `client` to load peer company data).

---

## 6. Implementation Steps

### Step 1: Create the directory
```bash
mkdir -p src/pages/business_card
```

### Step 2: Create `_helpers.py`
- Copy lines 43–83 from `business_card.py`
- Add `import streamlit as st` (needed by `_render_risk_dimension`)
- Add module docstring

### Step 3: Create `_sections.py`
- Add all imports (lines 9–40 from `business_card.py` + import from `_helpers.py`)
- Copy each section's code verbatim into its own function
- Replace variable references: `stock_id` → `data["stock_id"]`, etc.
- Add `(data: dict, client)` signature to each function
- **Do not change any rendering logic**

### Step 4: Create `_main.py`
- Add all imports (same as current `business_card.py` + imports from `_sections.py`)
- Copy the data extraction block (lines 86–94)
- Add delegation calls to all 14 section functions
- Keep the `_render_business_card(data, client)` signature unchanged

### Step 5: Create `__init__.py`
- Add re-export: `from src.pages.business_card._main import _render_business_card`

### Step 6: Delete the old `business_card.py`
```bash
rm src/pages/business_card.py
```

### Step 7: Verify
- Run L0 import check: `python -c "from src.pages.business_card import _render_business_card"`
- Run L1 render check: start the app and navigate to a stock's business card page
- Verify all 14 sections render correctly

---

## 7. Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| Import breakage in router.py | **HIGH** | `__init__.py` re-exports the function; test with L0 check immediately |
| Variable name mismatches in sections | **MEDIUM** | Each section receives the full `data` dict; extract locally. Copy-paste rendering logic verbatim |
| Missing imports in `_sections.py` | **MEDIUM** | All service imports go in `_sections.py`; only `st` + `_helpers` needed in `_main.py` |
| `st.session_state` keys collide | **LOW** | Session state keys use `stock_id` in their names (e.g., `f"show_watchlist_popup_{stock_id}"`); no naming changes needed |
| `client` parameter unused in most functions | **LOW** | Acceptable for interface consistency; `_render_read_next` uses it |

---

## 8. Line Count Budget (Post-Extraction)

| File | Estimated Lines | Notes |
|------|----------------|-------|
| `__init__.py` | ~5 | Re-export only |
| `_helpers.py` | ~40 | 4 items from original lines 43–83 |
| `_main.py` | ~60 | Imports + data extraction + 14 delegation calls |
| `_sections.py` | ~450 | All 14 section functions (same rendering logic) |
| **Total** | **~555** | Same logic, better organization |

**Net change**: 561 → 555 lines (slight reduction from eliminating duplicate import blocks).

---

## 9. Future-Proofing for Sprint 4 Features

### C38: Compare Stories (~50 lines)
- Add `_render_compare_stories(data, client)` to `_sections.py`
- Add delegation call in `_main.py`
- No structural changes needed

### C48: Company Story Card (~70 lines)
- Add `_render_story_card(data, client)` to `_sections.py`
- Add delegation call in `_main.py`
- No structural changes needed

### After both features: `_sections.py` ~570 lines
- Still well within acceptable range for a single file
- If `_sections.py` exceeds ~600 lines, consider splitting into `_sections_1.py` / `_sections_2.py` by category (summary sections vs. chart sections)

---

## 10. Verification Checklist

- [ ] `from src.pages.business_card import _render_business_card` works (L0)
- [ ] All 14 sections render on the business card page (L1)
- [ ] Watchlist add/remove buttons work correctly
- [ ] Watchlist popup (create list + add stock) works
- [ ] Health snowflake chart renders with 5 dimensions
- [ ] Risk analysis expandable sections work
- [ ] Dividend history table with badges renders
- [ ] Read Next peer stock buttons navigate correctly
- [ ] Company facts rotation works
- [ ] No `st.session_state` key collisions
- [ ] No import errors in any other page file

---

## 11. Related Debt Items

| Debt | Relationship to D24 |
|------|---------------------|
| **D19** | Inline HTML in business_card.py — after D24, the dividend table HTML lives in `_sections.py::_render_dividend()`. Still inline but isolated. Address via R9 (ui_components.py) later. |
| **D29** | C41 Read Next inline HTML — after D24, peer stock HTML lives in `_sections.py::_render_read_next()`. Still inline but isolated. |
| **D32** | Presentation helpers in page file — D24 moves `get_health_dimension_explanation()` and `_render_risk_dimension()` to `_helpers.py`. Still not in `ui_components.py` but no longer in a page file. |
| **D33** | C41 page-level data access — after D24, `client.get_stock_info()` call lives in `_render_read_next()`. Still a data access in presentation layer. Address by pre-computing peer data in `_router_base.py`. |

---

*Created: 2026-06-12*
*Status: Ready for implementation*
*Estimated effort: 2-3h*
