# C44: Risk Analysis MVP — Technical Design Document

> **Feature**: "What Could Go Wrong" Risk Analysis Section
> **Tier**: P2 · 12–14h estimated
> **Positioning**: Historian (explain, don't predict) — describe what *has happened*, never advise buy/sell
> **Author**: Architect (System Architect role)
> **Date**: 2026-06-12

---

## 1. Problem Description

### 1.1 What C44 Needs to Accomplish

The Stock Explorer business card page currently answers: *"What does this company do, and how is it doing?"* via C37 (summary), C39 (recent deltas), and C43 (health snowflake). C44 adds the missing question: **"What could go wrong?"**

C44 surfaces historical risk evidence in three dimensions, written in plain language, so that a novice investor can understand risks *the company has already experienced* — without the system ever predicting the future or giving investment advice.

### 1.2 Historian Positioning (解釋過去，不預測未來)

| ✅ Allowed | ❌ Forbidden |
|-----------|-------------|
| "過去三年負債比從 45% 上升到 68%" | "負債比可能持續上升" |
| "前五大客戶佔營收 72%，高於同業平均" | "客戶集中度過高，建議減碼" |
| "近一年內發生 3 次重大組織異動" | "經營層不穩定，前景看淡" |
| "現金流連續兩季為負" | "公司可能面臨資金短缺風險" |

**Key principles:**
- All statements reference historical data only
- No forward-looking language (會、可能、預計、有望)
- No buy/sell/hold recommendations
- Tone: factual, calm, educational — like a historian narrating what happened

### 1.3 MVP Scope (3 Risk Dimensions Only)

| # | Dimension | Data Source | Scope Cap |
|---|-----------|-------------|-----------|
| 1 | Customer Concentration Risk | `monthly_revenue`, `financial`, `extra_metrics` | Revenue concentration, customer dependency |
| 2 | Financial Health Risk | `balance_sheet`, `cash_flow`, `extra_metrics` | Leverage, cash flow, profitability trends |
| 3 | Event-Based Risk | `news`, `institutional` | Recent significant events from news |

Deferred (post-MVP): volatility risk, cyclicality risk, governance risk, supply chain risk.

---

## 2. Proposed Architecture

### 2.1 New Service Module: `src/services/risk_analyzer.py`

A new service module in the **Business Logic Layer** (Service), following the same pattern as `analogy_engine.py` and `news_summarizer.py`.

**Layer placement:**
```
┌─────────────────────────────────────────────────┐
│  View: business_card.py                         │
│  Calls: assess_risk() → renders risk section    │
├─────────────────────────────────────────────────┤
│  ★ Service: risk_analyzer.py (NEW)              │
│  Pure functions — no st.*, no API calls          │
│  Receives data dict fields → returns risk dict   │
├─────────────────────────────────────────────────┤
│  Data: _router_base.py get_stock_data()         │
│  Already provides all required fields in data{}  │
└─────────────────────────────────────────────────┘
```

**Design constraints (per architecture.md):**
- ✅ Pure functions: data in → result out
- ❌ No `import streamlit`
- ❌ No direct FinMind API calls
- ❌ No file I/O, no cache writes
- ❌ No side effects

### 2.2 Data Flow

```
_router_base.get_stock_data()
    → data dict {
        extra_metrics,    # dict: debt_ratio, equity_ratio, gross_margin, etc.
        financial,        # DataFrame: income statement items
        balance_sheet,    # DataFrame: assets/liabilities/equity
        cash_flow,        # DataFrame: operating/investing/financing cash flow
        news,             # DataFrame: title, source, date, ...
        institutional,    # DataFrame: foreign/insider buying
        monthly_revenue,  # DataFrame: monthly revenue history
        stock_id,         # str
        stock_name,       # str
        industry,         # str
    }
        ↓
risk_analyzer.assess_risk(data)
    → RiskAssessment {
        customer_concentration: RiskDimension | None
        financial_health: RiskDimension | None
        event_based: RiskDimension | None
        overall_level: "high" | "medium" | "low"
        summary_text: str   # plain-language 2-3 sentence overview
    }
        ↓
business_card.py _render_risk_section(data)
    → st.expander("⚠️ 風險分析") with RiskDimension cards
```

### 2.3 Output Data Structure

```python
# Each risk dimension produces:
RiskDimension = {
    "risk_level": "high" | "medium" | "low",
    "title": str,                     # e.g. "客戶集中風險"
    "plain_language_description": str, # 1–2 sentences, Chinese, historical language
    "supporting_data": dict,           # Structured evidence for expansion
}

# Top-level output:
RiskAssessment = {
    "customer_concentration": RiskDimension | None,
    "financial_health": RiskDimension | None,
    "event_based": RiskDimension | None,
    "overall_level": "high" | "medium" | "low",
    "summary_text": str,              # Narrative overview for the section header
}
```

### 2.4 Output Structure Rationale

The output is a plain dict (not a dataclass) to stay consistent with existing service patterns (`compute_health_scores()` returns a dict, `summarize_news()` returns a string). The `supporting_data` field is an plain dict keyed by metric name — this lets the View layer decide what to show in the expandable detail area without re-querying anything.

---

## 3. Function Signatures

### 3.1 Public API — 3 Functions

```python
def assess_risk(data: dict) -> dict:
    """
    Complete risk assessment — top-level entry point.

    Orchestrates the three risk dimension sub-analyses and produces
    a unified RiskAssessment dict.

    Args:
        data: The standard data dict from _router_base.get_stock_data(),
              containing keys: extra_metrics, financial, balance_sheet,
              cash_flow, news, institutional, monthly_revenue, stock_id,
              stock_name, industry.

    Returns:
        dict with keys:
            customer_concentration (dict | None): Customer concentration dimension
            financial_health (dict | None): Financial health dimension
            event_based (dict | None): Event-based risk dimension
            overall_level (str): "high" | "medium" | "low"
            summary_text (str): Plain-language 2–3 sentence overall summary
        Each dimension dict has:
            risk_level (str): "high" | "medium" | "low"
            title (str): Dimension title in Chinese
            plain_language_description (str): Historical, factual description
            supporting_data (dict): Evidence details for expandable display
        Returns {"overall_level": "low", "summary_text": "風險分析資料不足", ...}
        with all dimensions None if input data is critically incomplete.
    """
```

```python
def assess_customer_concentration(data: dict) -> dict | None:
    """
    Analyze customer/supplier concentration risk.

    Uses revenue breakdown items from financial statements and
    revenue trend data from monthly_revenue to assess whether the
    company depends disproportionately on a small number of customers.

    Data fields used:
        - financial DataFrame: revenue breakdown by customer/segment type
        - extra_metrics: revenue_yoy (for trend context)
        - monthly_revenue: to assess revenue stability over trailing 12 months

    Returns:
        RiskDimension dict, or None if insufficient data to assess.
        supporting_data includes:
            - revenue_concentration_pct (float | None): top customer/segment %
            - revenue_stability_cv (float | None): coefficient of variation of trailing 12m revenue
            - revenue_trend (str): "growing" | "stable" | "declining"
    """
```

```python
def assess_financial_health(data: dict) -> dict | None:
    """
    Analyze financial health risk across leverage, cash flow, and profitability.

    Data fields used:
        - extra_metrics: debt_ratio, equity_ratio, gross_margin,
          operating_margin, net_margin, revenue_yoy
        - balance_sheet: latest period liability and equity composition
        - cash_flow: trailing 4-quarter operating cash flow trend
        - financial: trailing 4-quarter profitability for trend analysis

    Returns:
        RiskDimension dict, or None if insufficient data.
        supporting_data includes:
            - debt_ratio (float | None)
            - equity_ratio (float | None)
            - gross_margin (float | None)
            - net_margin (float | None)
            - operating_cash_flow_trend (str): "positive" | "mixed" | "negative"
            - profitability_trend (str): "improving" | "stable" | "declining"
    """
```

```python
def assess_event_risk(data: dict) -> dict | None:
    """
    Analyze event-based risk from recent news headlines.

    Data fields used:
        - news: DataFrame with title, source, date columns
        - institutional: foreign investor net buy/sell (trailing 30 days)

    Returns:
        RiskDimension dict, or None if no news data.
        supporting_data includes:
            - high_impact_count (int): number of high-impact news in trailing 90 days
            - medium_impact_count (int): number of medium-impact news
            - top_events (list[str]): top 3 event summaries (plain language)
            - foreign_flow_trend (str): "buying" | "neutral" | "selling"
    """
```

### 3.2 Internal / Private Helpers

These are private (prefixed with `_`) and handle thresholding:

```python
def _classify_debt_risk(debt_ratio: float | None) -> str:
    """Classify debt ratio into high/medium/low. Returns risk level string."""

def _classify_margin_risk(net_margin: float | None) -> str:
    """Classify net profit margin into high/medium/low risk levels."""

def _classify_cashflow_risk(cash_flow_values: list[float]) -> str:
    """Classify cash flow trend from trailing operating cash flow values."""

def _classify_concentration_risk(concentration_pct: float | None) -> str:
    """Classify revenue concentration level."""

def _count_risk_events(news_df, days: int = 90) -> dict:
    """Count high/medium impact news in trailing window. Returns {high, medium, events}."""

def _determine_overall_level(dimensions: list[str]) -> str:
    """Derive overall risk level from list of dimension risk_level strings."""
```

---

## 4. Page Integration Plan

### 4.1 Placement in business_card.py

The risk section should be placed **after the C43 health snowflake section** and **before the 一句話定位 (one-liner)** section. This creates a logical flow:

1. 📋 重點摘要 (C37) — *What is this company?*
2. 🔄 最近變化 (C39) — *What changed recently?*
3. 🏥 健康狀況 (C43) — *How healthy is it?*
4. ⚠️ **風險分析 (C44)** — *What could go wrong?* ← NEW
5. 💡 一句話定位 — *One-line summary*

This positioning keeps the risk section close to the health data it references, while placing it *after* the positive/neutral content and *before* the closing summary.

### 4.2 Expandable Pattern (Progressive Disclosure)

Following the pattern established by the dividend history expander (line 325 of `business_card.py`) and the D-025 expandable card spec:

```python
# In _render_business_card(), after C43 health section:

from src.services.risk_analyzer import assess_risk

# ... after st.markdown("---") following health snowflake ...

risk = assess_risk(data)
if risk["overall_level"] != "low" or any(
    risk.get(dim) for dim in ("customer_concentration", "financial_health", "event_based")
):
    with st.expander("⚠️ 風險分析 — 什麼可能出問題？", expanded=False):
        if risk["summary_text"]:
            st.markdown(
                f"""<div style="color:#7F8C8D;font-size:0.9rem;margin-bottom:0.8rem;">
                {risk["summary_text"]}</div>""",
                unsafe_allow_html=True,
            )

        # Render each non-None dimension
        for dim_key in ("customer_concentration", "financial_health", "event_based"):
            dim = risk.get(dim_key)
            if dim is None:
                continue
            _render_risk_dimension(dim, data["stock_name"])
```

### 4.3 Dimension Card Rendering (View Layer)

A new helper in `business_card.py` renders each dimension using the `_info_card()` / `_summary_card()` pattern with a colour-coded risk badge:

```python
_RISK_BADGES = {
    "high":   "🔴 高風險",
    "medium": "🟡 中風險",
    "low":    "🟢 低風險",
}

_RISK_COLORS = {
    "high":   "#E74C3C",
    "medium": "#F39C12",
    "low":    "#27AE60",
}

def _render_risk_dimension(dim: dict, stock_name: str):
    """Render a single risk dimension as an expandable info card."""
    badge = _RISK_BADGES.get(dim["risk_level"], "⚪ 未知")
    color = _RISK_COLORS.get(dim["risk_level"], "#7F8C8D")

    st.markdown(
        f"""<div style="background:#FFF8F0;border-radius:12px;padding:1.2rem;
        border-left:4px solid {color};margin:0.5rem 0 1rem 0;">
            <div style="font-weight:600;color:#2C3E50;">
                {badge} {dim["title"]}
            </div>
            <div style="font-size:0.9rem;color:#2C3E50;margin-top:0.4rem;
            line-height:1.7;">{dim["plain_language_description"]}</div>
        </div>""",
        unsafe_allow_html=True,
    )
```

### 4.4 Handling Missing Data

Following the architecture's error-handling convention (Service returns `None` → View displays `st.info()` or skips):

- If `assess_risk()` returns no non-None dimensions → **skip the entire section**, no placeholder shown
- If a single dimension is `None` → skip that dimension card, render the others
- If `assess_risk()` returns the fallback dict (all None, overall_level "low") → skip section

This is the safest approach: the risk section adds a disclaimer for stocks *with* visible risks and stays invisible for stocks without, consistent with the historian principle of "only report what the data shows."

### 4.5 No New Component File Needed

The `_render_risk_dimension` helper (~25 lines) and the section-rendering block (~30 lines) can live directly in `business_card.py` as a private function, consistent with how other sections are handled. The heavy lifting (analysis logic) lives in `src/services/risk_analyzer.py`.

If D24 (business_card.py sub-directory extraction) has been completed before this work begins, place the rendering function in `src/pages/business_card/sections/risk.py` instead, per the D24 spec in `tech_debt.md`.

---

## 5. Alternative Approaches

### Option A: New `src/services/risk_analyzer.py` (Recommended ✓)

**Description**: Standalone service module with pure functions, following the same pattern as `news_summarizer.py`.

**Pros:**
- Clean separation of concerns — risk logic is isolated and independently testable
- Follows architecture.md Service Layer conventions exactly
- Easy to extend (new dimensions added as new functions, no existing file changes)
- No side effects: trivially verified no `st.*` imports
- Parallel to `analogy_engine.py` pattern — reviewer familiar with codebase will understand instantly
- Can be unit-tested with fixture DataFrames without any Streamlit context

**Cons:**
- Another file in `src/services/` (minor)
- ~40 lines of import + rendering code still needed in `business_card.py`

**Verdict**: **Recommended.** Cleanest, most maintainable, architecture-compliant.

---

### Option B: Extend `analogy_engine.py` with risk functions

**Description**: Add `assess_risk()` and helpers into the existing 850-line `analogy_engine.py`.

**Pros:**
- No new file created
- `analogy_engine.py` already receives `extra_metrics`, `financial`, `monthly_revenue` as inputs — same data

**Cons:**
- `analogy_engine.py` is already 850 lines and flagged for decomposition (D16, tech_debt.md)
- Mixing analogy-generation with risk-analysis violates single-responsibility
- D16 is planned to *split* `analogy_engine.py` — adding to it now creates merge/conflict work later
- Makes the planned D16 split harder (more code to migrate)
- Reviewer burden: risk logic masked inside analogy logic

**Verdict**: **Not recommended.** Violates D16 intent and SRP. tech_debt.md explicitly calls out this file as overdue for splitting.

---

### Option C: Inline in `business_card.py`

**Description**: Write all risk analysis logic as private functions directly in the View layer.

**Pros:**
- Single file, easy to trace data flow
- No cross-module imports needed
- Fast to implement

**Cons:**
- Violates architecture.md: business logic in View layer
- `business_card.py` is 509 lines; D24 (sub-directory extraction) exists to prevent this growth
- Cannot be unit-tested without Streamlit runtime
- Cannot be reused by other pages (e.g., a future "risk dashboard" view)
- Sets bad precedent: encourages more inline logic

**Verdict**: **Not recommended.** Directly contradicts the 4-layer architecture. tech_debt.md has a specific debt item (D30) flagging this exact problem.

---

## 6. Effort Estimate

| Phase | Task | Hours | Notes |
|-------|------|-------|-------|
| **Service Module** | `risk_analyzer.py`: `assess_customer_concentration()` + helpers | 3.0 | Thresholds + plain-language generation in zh-TW |
| | `assess_financial_health()` + helpers | 3.5 | Most complex: leverage + cashflow + profitability trends |
| | `assess_event_risk()` + helpers | 2.0 | Reuses `get_news_impact_level()` pattern from `news_summarizer` |
| | `assess_risk()` orchestrator + `_determine_overall_level()` | 1.0 | Trivial wiring |
| | Input validation + None-safety for all functions | 1.0 | Every function must handle None/empty DataFrame gracefully |
| **Subtotal Service** | | **10.5** | |
| **Page Integration** | `_render_risk_dimension()` helper | 0.5 | Pure rendering, follows existing `_info_card()` pattern |
| | `st.expander()` block in `_render_business_card()` | 0.5 | ~15 lines, follows dividend expander pattern |
| | Section placement + `from src.services.risk_analyzer import` | 0.3 | Import + placement after C43 |
| | Edge case handling (no data, None dimensions) | 0.5 | Skip logic + test manually with 3+ stocks |
| **Subtotal Page** | | **1.8** | |
| **Testing** | Manual test with 5 stocks (varied industries) | 1.0 | Verify thresholds trigger correctly; read Turkish output aloud |
| | Boundary test: missing `balance_sheet`, missing `news` | 0.5 | Ensure graceful degradation |
| | Read-through for historian tone compliance | 0.5 | Check for any forward-looking language |
| **Subtotal Testing** | | **2.0** | |
| **Contingency** | | **1.5** | Unexpected data shapes, threshold tuning |
| **TOTAL** | | **15.8** | Fits within 12–14h estimate + ~2h buffer |

---

## 7. Risk Analysis Logic — Detail by Dimension

### 7.1 Dimension 1: Customer Concentration Risk (客戶集中風險)

**Data fields used:**

| Field | Source | Purpose |
|-------|--------|---------|
| `financial` DataFrame | `type` contains "營業收入" or segment/customer breakdown rows | Revenue by customer or segment percentage |
| `monthly_revenue` | Trailing 12 months of revenue | Revenue stability (coefficient of variation) |
| `extra_metrics["revenue_yoy"]` | Revenue year-over-year growth | Context: is revenue growing diversified or concentrated? |

**Thresholds:**

| Risk Level | Condition |
|------------|-----------|
| `high` | Top customer/segment > 50% of revenue, OR monthly revenue CV > 0.25 |
| `medium` | Top customer/segment 25–50%, OR monthly revenue CV 0.10–0.25 |
| `low` | Top customer/segment < 25%, AND monthly revenue CV < 0.10 |

**Analysis approach:**
1. Search `financial` DataFrame for revenue breakdown rows (type contains "客戶", "客源", "營業收入" with segment data)
2. Calculate CV of trailing 12-month revenue values
3. Classify based on thresholds above
4. Generate plain-language description referencing actual data values

**Example output text (Chinese):**

*High risk:*
> 根據最近一期財報，前三大客戶合計佔營收約 65%。過去 12 個月營收波動幅度（變異係數）為 0.28，顯示收入来源較不穩定。這意味著少數客戶的訂單變化會顯著影響公司營收。

*Medium risk:*
> 近月營收主要來自 2–3 個業務線，最大業務線佔營收約 35%。過去 12 個月營收波動幅度為 0.15，屬於正常範圍。公司營收來源有一定集中，但仍在可控範圍。

*Low risk:*
> 公司營收來源分散在多個業務線，最大業務線佔營收不到 20%。過去 12 月營收波動幅度為 0.08，收入來源穩定多元。

---

### 7.2 Dimension 2: Financial Health Risk (財務健康風險)

**Data fields used:**

| Field | Source | Purpose |
|-------|--------|---------|
| `extra_metrics["debt_ratio"]` | `balance_sheet`: total liabilities / total assets | Leverage assessment |
| `extra_metrics["equity_ratio"]` | `balance_sheet`: total equity / total assets | Solvency buffer |
| `extra_metrics["gross_margin"]` | `financial`: gross profit / revenue | Core profitability |
| `extra_metrics["net_margin"]` | `financial`: net income / revenue | Bottom-line profitability |
| `cash_flow` DataFrame | Operating cash flow items (type contains "營業活動", "Operating Cash Flow") | Cash generation trend |
| `financial` DataFrame | Net income over trailing 4 quarters | Profitability trend |

**Sub-dimension thresholds and logic:**

**Debt risk:**
| Risk Level | Debt Ratio |
|------------|-----------|
| `high` | > 65% |
| `medium` | 45–65% |
| `low` | < 45% |

**Profitability risk (net margin):**
| Risk Level | Net Margin |
|------------|-----------|
| `high` | < 3% (thin margin) or negative |
| `medium` | 3–8% |
| `low` | > 8% |

**Cash flow risk:**
| Risk Level | Operating Cash Flow Trend |
|------------|--------------------------|
| `high` | 2+ of trailing 4 quarters negative |
| `medium` | 1 of trailing 4 quarters negative |
| `low` | All 4 quarters positive |

**Composite classification:**
- If 2+ sub-dimensions are `high` → overall `high`
- If 1 sub-dimension is `high` → overall `medium`
- If all sub-dimensions are `low` → overall `low`
- Otherwise → `medium`

**Example output text (Chinese):**

*High risk:*
> 最近一期負債比為 72%，高於一般認為的警戒線 65%。過去 4 季營業現金流有 2 季為負數，表示本業賺取的現金不足以支應營運所需。淨利率僅 1.2%，獲利空間極為有限。

*Medium risk:*
> 負債比為 52%，屬於適度槓桿範圍。淨利率為 4.5%，獲利穩定但不算突出。過去 4 季營業現金流有 1 季為負，需留意後續是否改善。

*Low risk:*
> 負債比僅 35%，財務結構穩健。淨利率維持在 12% 以上，獲利能力在同產業中屬於前段班。過去 4 季營業現金流均為正數，本業現金創造能力良好。

---

### 7.3 Dimension 3: Event-Based Risk (事件型風險)

**Data fields used:**

| Field | Source | Purpose |
|-------|--------|---------|
| `news` DataFrame | `title`, `date` columns | Recent significant events via `get_news_impact_level()` |
| `institutional` DataFrame | Foreign investor net buy/sell | Institutional sentiment signal |

**Analysis approach:**
1. Filter `news` to trailing 90 days from latest date in the DataFrame
2. Run each title through existing `get_news_impact_level()` (from `news_summarizer.py`)
3. Count high/medium impact events
4. Summarize top 3 most impactful events using `summarize_news()`
5. Assess institutional flow direction from trailing 30-day net foreign buying

**Thresholds:**

| Risk Level | Condition |
|------------|-----------|
| `high` | 3+ high-impact events in 90 days, OR (2+ high-impact AND net foreign selling > 10,000 张) |
| `medium` | 1–2 high-impact events, OR 3+ medium-impact events |
| `low` | 0 high-impact AND < 3 medium-impact events |

**Example output text (Chinese):**

*High risk:*
> 近 90 天內有 4 則重大消息，包含財報公布、組織異動等 Event。其中 3 則被列為高度關注事件。同期外資累計賣超 25,000 張，法人態度偏向保守。

*Medium risk:*
> 近 90 天內有 2 則中度關注消息，涉及產品認證與供應鏈調整。同期外資買賣互見，法人態度中性。

*Low risk:*
> 近 90 天內未有重大消息，新聞多為例行性公告。同期外資小幅買超，法人態度穩定。

---

## 8. Dependencies and Imports

### 8.1 New imports in `src/services/risk_analyzer.py`

```python
"""風險分析器 — 純函式，無 Streamlit 與 API 依賴"""

import pandas as pd
from typing import Optional

from src.services.financial_metrics import find_financial_value
from src.services.news_summarizer import get_news_impact_level, summarize_news
```

### 8.2 New import in `src/pages/business_card.py`

```python
from src.services.risk_analyzer import assess_risk
```

### 8.3 No changes needed to:
- `_router_base.py` — all required fields already present in data dict
- `financial_metrics.py` — reuse existing helpers
- `news_summarizer.py` — reuse existing `get_news_impact_level()`

---

## 9. Historian Tone Checklist

Before implementation, the Developer must run the following checklist. Every output string in `risk_analyzer.py` must comply:

- [ ] No forward-looking verbs: 會、可能、預計、有望、看起來要
- [ ] No recommendation language: 建議、應該、最好、需要留意（except "需要關注" as a factual observation, never as advice）
- [ ] Every risk statement cites a specific data point with a number
- [ ] Percentages include the base period: "從 45% 上升到 68%" not just "目前是 68%"
- [ ] No comparison to market/index unless explicitly queried — focus on company-internal trends
- [ ] Language meets the 國中國 level target (國中生可讀)

---

## 10. Open Questions for Developer

1. **Revenue breakdown availability**: The `financial` DataFrame may not have per-customer breakdown for most TWSE stocks. If not available, `assess_customer_concentration()` should return `None` gracefully and rely on revenue stability (CV) as the sole signal.

2. **Cash flow column naming**: The `cash_flow` DataFrame column names depend on FinMind's response format. The Developer should inspect a sample response to identify the correct `type` keyword for operating cash flow rows (likely "營業活動之淨現金流入（出）" or similar).

3. **Threshold calibration**: The thresholds in Section 7 are starting estimates. The Developer should test with 5–8 stocks across different industries and adjust thresholds if the distribution feels off (e.g., if 80% of stocks come out as "medium").

4. **D24 sequencing**: If D24 (business_card.py extraction) completes before this work, the rendering function should go in `src/pages/business_card/sections/risk.py` per D24 spec. Check `business_card.py` target structure before implementing.

---

*End of Design Document*
