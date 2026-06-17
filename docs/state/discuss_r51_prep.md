# Sprint 25 Day 2 Discussion Brief — C209 Integration

**Date**: 2026-06-17  
**Author**: PM (pre-discussion prep for Round 51)  
**Sprint**: Sprint 25 — Day 2 of 3  
**Task**: Integrate `_source_section()` into 3 target pages  

---

## 1) Sprint 25 Day 2 Scope

### Objective
Integrate the C209 `_source_section()` component (created Day 1, commit `8ed9a97`) into the three highest-priority pages:

| Priority | Page | Rationale |
|----------|------|-----------|
| 1 | `daily_market.py` | Data freshness is critical for market data — users need to know if they're seeing live or stale prices |
| 2 | `business_card/_main.py` | Highest traffic page; users see price, financials, news, group data — source transparency adds trust |
| 3 | `event_dashboard.py` | Already has a partial freshness UI (`_render_freshness_indicator()`); C209 replaces the ad-hoc approach with the standardized component |

### What's Already Done
- `_source_section()` component created in `src/pages/_router_base.py` (lines 568–619)
- i18n keys added to both `locales/en.yaml` and `locales/zh-TW.yaml` under `source_section.*`
- Component signature: `_source_section(sources: list[dict], last_updated: str, *, freshness_indicator: bool = True)`
- Each source dict has keys: `label`, `api`, `time`
- Freshness indicator: 🟢 (<1h), 🟡 (<24h), 🔴 (>24h)

### What Each Page Needs
1. Import `_source_section` from `src.pages._router_base`
2. Build a `sources` list describing the APIs/data sources used on that page
3. Determine the `last_updated` timestamp
4. Call `_source_section(sources, last_updated)` at the bottom of the page content, before the disclaimer

### Estimated Effort
| Page | Estimated Time |
|------|---------------|
| `daily_market.py` | 30–45 min |
| `business_card/_main.py` | 30–45 min |
| `event_dashboard.py` | 20–30 min |
| **Total** | **1.5–2h** |

---

## 2) Per-Page Integration Plan

### 2A. `daily_market.py` — Daily Market Dashboard

**File**: `src/pages/daily_market.py`  
**Entry point**: `_render_daily_market(client)` (line 15)

**Data Sources Used**:
| Source | Service Function | API/Data |
|--------|-----------------|----------|
| Stock info list | `get_all_stock_info(client)` | FinMind `TaiwanStockInfo` |
| Batch price summaries | `get_all_summaries(client, all_stock_info)` | FinMind `TaiwanStockPrice` (batch) |
| Sector classification | `get_sector_stocks(all_stock_info)` | Derived from `TaiwanStockInfo` |
| Market events | `get_all_recent_events(days=1, limit=5)` | Local `data/events.yaml` (no external API) |

**All routed through**: `get_sector_grid_data(client)` (from `src.services.market_data`)

**Proposed Source Dict**:
```python
sources = [
    {"label": t("daily_market.sources.stock_info"), "api": "FinMind", "time": now_str},
    {"label": t("daily_market.sources.price_summary"), "api": "FinMind", "time": now_str},
    {"label": t("daily_market.sources.sector_data"), "api": "FinMind", "time": now_str},
    {"label": t("daily_market.sources.events"), "api": t("daily_market.sources.local_db"), "time": now_str},
]
```

**`last_updated` source**: `datetime.now().strftime("%Y-%m-%d %H:%M")` — the page already has a `_render_freshness()` function (line 68) that computes dates from data. The `_source_section` call should use the same timestamp. Recommendation: compute `last_updated` once at the top of `_render_daily_market` and pass it to both `_render_freshness` and `_source_section`.

**Placement**: After the disclaimer (line 65), before function end. Alternatively, replace the existing `_render_freshness()` call entirely and let `_source_section` handle both freshness and source transparency. **Recommendation**: Remove the standalone `_render_freshness()` call and rely on `_source_section()` for both.

**Existing freshness UI**: The page already shows a freshness caption at line 88:
```python
st.caption(f"{status} ｜ {t('daily_market.last_updated', time=now_str)}")
```
This is a candidate for removal if `_source_section` handles it.

**Key Decision Needed**: Remove or keep the existing `_render_freshness()` caption?  
→ **Recommendation**: Remove it. `_source_section` already shows freshness via the colored dot indicator. Keeping both creates redundancy.

---

### 2B. `business_card/_main.py` — Company Overview (Highest Traffic)

**File**: `src/pages/business_card/_main.py`  
**Entry point**: `_render_business_card(data: dict, client)` (line 191)

**Data Sources Used** (all from `get_stock_data()` in `_router_base.py`):
| Source | API | Data |
|--------|-----|-------|
| Stock info | `client.get_stock_info()` | FinMind `TaiwanStockInfo` |
| Latest price | `client.get_latest_price()` | FinMind `TaiwanStockPrice` |
| PER/PBR | `client.get_latest_per_pbr()` | FinMind `TaiwanStockPER` |
| Monthly revenue | `client.get_monthly_revenue()` | FinMind `TaiwanStockMonthRevenue` |
| Financial statement | `client.get_financial_statement()` | FinMind `TaiwanStockFinancialStatement` |
| News | `client.get_news()` | FinMind `TaiwanStockNews` |
| Institutional investors | `client.get_institutional_investors()` | FinMind `TaiwanStockInstitutionalInvestors` |
| Balance sheet | `client.get_balance_sheet()` | FinMind `TaiwanStockBalanceSheet` |
| Cash flow | `client.get_cash_flow()` | FinMind `TaiwanStockCashFlow` |
| Dividends | `client.get_dividend()` | FinMind `TaiwanStockDividend` |
| Group/group structure | `data["stock_info"]` column | FinMind (via `get_stock_info`) |
| Events | `get_all_recent_events()` / `get_events_for_stock()` | Local `data/events.yaml` |
| Revenue tree | `analyze_revenue_breakdown()` | Derived from financial data |
| Price charts | `create_revenue_trend_chart()`, etc. | Derived from price/monthly revenue data |

**Proposed Source Dict** (grouped for readability):
```python
sources = [
    {"label": t("business_card.sources.stock_info"),    "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.price"),          "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.per_pbr"),        "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.revenue"),        "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.financial"),      "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.dividend"),       "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.news"),           "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.institutional"),  "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.balance_sheet"),  "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.cash_flow"),      "api": "FinMind", "time": now_str},
]
```

**`last_updated` source**: The `data` dict is loaded via `get_stock_data()` which fetches in real-time. Use `datetime.now().strftime("%Y-%m-%d %H:%M")` at render time. For accuracy, could store a `_fetch_time` in `data` during `get_stock_data()`.

**Placement**: At the end of `_render_business_card()`, after `_render_footer()` (line 327), before the function returns. This keeps the source section below all content but above nothing — it's the last thing users see.

**Special consideration**: The business card page has 10+ FinMind endpoints. Listing all 10 may be verbose.  
→ **Key Decision Needed**: List all 10 sources individually, or group them?  
→ **Recommendation**: Group into 4–5 logical groups (Price/Valuation, Financials, News/Events, Corporate Data). This follows the component's `label` key design — each entry can be a broader category.

**Alternative grouped approach**:
```python
sources = [
    {"label": t("business_card.sources.price_valuation"),  "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.financial_revenue"), "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.dividend"),          "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.news_institutional"), "api": "FinMind", "time": now_str},
    {"label": t("business_card.sources.corporate"),         "api": "FinMind", "time": now_str},
]
```

---

### 2C. `event_dashboard.py` — Event Dashboard

**File**: `src/pages/event_dashboard.py`  
**Entry point**: `_render_event_dashboard(client)` (line 59)

**Data Sources Used**:
| Source | Service Function | API/Data |
|--------|-----------------|----------|
| All recent events (30 days) | `get_all_recent_events(days=30, limit=50)` | Local `data/events.yaml` |
| Stock-specific events | `get_events_for_stock()` | Local `data/events.yaml` |
| Event interpretation | `get_interpretation()` | Local config (`event_interpretation_templates.yaml`) |
| Data freshness check | `check_data_freshness()` | Derived from `data` dict |

**Proposed Source Dict**:
```python
sources = [
    {"label": t("event_dashboard.sources.events"),    "api": t("event_dashboard.sources.local_db"), "time": now_str},
    {"label": t("event_dashboard.sources.interpretation"), "api": t("event_dashboard.sources.templates"), "time": now_str},
]
```

**`last_updated` source**: The events are stored locally. Use `"N/A"` or the file modification time of `data/events.yaml`.  
→ **Recommendation**: Use `datetime.now().strftime("%Y-%m-%d %H:%M")` for when the page was rendered, since the events themselves are loaded from a local file that's updated on each stock page visit.

**Placement**: After the "關於事件儀表板" info section (line 154), before the function returns. The existing `_render_freshness_indicator()` function (line 157) is defined but **not called** from `_render_event_dashboard()`. This is dead code.  
→ **Key Decision Needed**: Remove the unused `_render_freshness_indicator()` function entirely, or integrate it into `_source_section`?  
→ **Recommendation**: Remove `_render_freshness_indicator()` — `_source_section` with `freshness_indicator=True` subsumes its functionality.

**Special consideration**: Event data comes from a local YAML file, not FinMind. The `api` field should reflect this (e.g., "本地事件資料庫" / "Local Event DB"). The `_source_section` component doesn't hardcode "FinMind" — it reads whatever string is in the `api` field, so this works naturally.

---

## 3) i18n Key Requirements

### Already Exist (C209 Day 1)
Both `locales/en.yaml` and `locales/zh-TW.yaml` already have:

```yaml
# zh-TW.yaml (line 560)
source_section:
  title: "📡 資料來源"
  last_updated: "最後更新"
  fresh:
    recent: "1 小時內"
    day: "24 小時內"
    stale: "超過 24 小時"

# en.yaml (line 551)
source_section:
  title: "📡 Data Sources"
  last_updated: "Last Updated"
  fresh:
    recent: "< 1 hour ago"
    day: "< 24 hours ago"
    stale: "> 24 hours ago"
```

### New Keys Needed for Per-Page Source Labels

#### `daily_market` — Add to both locale files:

```yaml
# en.yaml — under daily_market:
  sources:
    stock_info: "Stock Info & Sector Classification"
    price_summary: "Batch Price Summary"
    sector_data: "Sector Aggregation"
    events: "Market Events (Local)"

# zh-TW.yaml — under daily_market:
  sources:
    stock_info: "股票資料與產業分類"
    price_summary: "批次股價摘要"
    sector_data: "板塊數據"
    events: "市場事件（本機）"
```

#### `business_card` — Add new section to both locale files:

```yaml
# en.yaml — new top-level business_card section:
business_card:
  sources:
    price_valuation: "Price & Valuation Data"
    financial_revenue: "Financial Statements & Revenue"
    dividend: "Dividend Data"
    news_institutional: "News & Institutional Investors"
    corporate: "Corporate Data (Balance Sheet, Cash Flow)"

# zh-TW.yaml — new top-level business_card section:
business_card:
  sources:
    price_valuation: "股價與估值資料"
    financial_revenue: "財務報表與營收"
    dividend: "股利資料"
    news_institutional: "新聞與法人動向"
    corporate: "公司資料（資產負債表、現金流量表）"
```

**Note**: Adding a `business_card:` top-level key to the locale files will NOT conflict with the existing `page.business_card: "Overview"` key — they are at different nesting levels. `page.business_card` is under the `page:` namespace; `business_card:` would be a new top-level namespace.

#### `event_dashboard` — Add to both locale files:

```yaml
# en.yaml — new top-level event_dashboard section:
event_dashboard:
  sources:
    events: "Event Records"
    interpretation: "Event Interpretation Templates"
    local_db: "Local Event Database"
    templates: "Template Engine"

# zh-TW.yaml — new top-level event_dashboard section:
event_dashboard:
  sources:
    events: "事件紀錄"
    interpretation: "事件解讀範本"
    local_db: "本機事件資料庫"
    templates: "範本引擎"
```

### Total New i18n Keys

| Page | New Key Groups | Count |
|------|---------------|-------|
| `daily_market` | `daily_market.sources.*` | 4 per locale |
| `business_card` | `business_card.sources.*` | 5 per locale |
| `event_dashboard` | `event_dashboard.sources.*` | 4 per locale |
| **Total** | | **13 per locale (26 total)** |

These are all simple label strings — no template variables needed.

---

## 4) Risk Assessment

### 🟢 Low Risk: `_source_section()` component is well-tested
- Component was created Day 1 with inline empty-sources handling
- Import test passes
- No external dependencies beyond `i18n.t()` and `datetime`

### 🟡 Medium Risk: Business card page is complex (327 lines, 20+ service imports)
- The `_render_business_card()` function has many sections and two modes (beginner/expert)
- Adding an import and a call at the bottom is low-risk, but verifying correct `last_updated` timing requires care
- The business card uses `get_stock_data()` which fetches 10 APIs via ThreadPoolExecutor — determining the "fetch time" for `last_updated` is imprecise (all fetches happen in parallel, but we only know when the page finishes rendering)
- **Mitigation**: Use `datetime.now()` at render time as a pragmatic approximation

### 🟡 Medium Risk: Event dashboard has dead freshness code
- `_render_freshness_indicator()` (line 157) and `_freshness_badge()` (line 34) are defined but never called from `_render_event_dashboard()`
- Adding `_source_section` makes these functions dead code
- **Mitigation**: Mark for removal commit. Don't ship dead code in the same commit as the new feature.

### 🟡 Medium Risk: Many new i18n keys across 2 locale files
- 13 new keys per locale, all under new namespace sections (`business_card:`, `event_dashboard:`, `daily_market.sources:`)
- Risk of inconsistency between en and zh-TW if translated separately
- **Mitigation**: Add keys to both files atomically in the same commit. Use the grouped source approach (5 entries for business_card instead of 10) to minimize translation surface.

### 🟢 Low Risk: daily_market.py already has freshness UI
- Existing `_render_freshness()` shows a caption with freshness status
- Replacing it with `_source_section` removes a standalone function (`_render_freshness` becomes dead code)
- **Mitigation**: Remove `_render_freshness()` in the same commit

### 🟡 Medium-risk: i18n key namespace collision
- `business_card:` doesn't exist at top level in locale files — safe to add
- `event_dashboard:` doesn't exist at top level — safe to add  
- `daily_market:` already exists as top level — need to nest `sources:` under it, not create a new top-level key
- **Mitigation**: Verify YAML structure before writing. The existing `daily_market:` key structure ends at line 556 in zh-TW.yaml — adding `sources:` sub-key is safe

---

## 5) Recommended Decisions

### Decision 1: Replace existing freshness UI in `daily_market.py`
**Decision**: Remove `_render_freshness()` call (line 39) and the function itself (lines 68–88). Let `_source_section()` handle both source transparency and freshness indication.

**Rationale**: Having both creates redundancy — two freshness indicators on the same page. The `_source_section` component's colored dot + timestamp is more informative than the existing caption.

### Decision 2: Group business card sources (not 10 individual entries)
**Decision**: Use 5 grouped source entries for business_card instead of listing all 10 FinMind endpoints individually.

**Rationale**: The component renders one `st.caption` per source entry. 10 entries would be verbose and push content below the fold on smaller screens. 5 grouped entries (Price/Valuation, Financials/Revenue, Dividend, News/Institutional, Corporate) match the page's existing section organization.

### Decision 3: Remove dead freshness code from `event_dashboard.py`
**Decision**: Remove `_render_freshness_indicator()` (lines 157–178) and `_freshness_badge()` (lines 34–43) in the same commit as the C209 integration. They are dead code superseded by `_source_section`.

**Rationale**: Don't ship dead code alongside new features. Both functions are unused (grep confirms zero callers).

### Decision 4: Use `datetime.now()` for `last_updated` across all pages
**Decision**: Use `datetime.now().strftime("%Y-%m-%d %H:%M")` as the `last_updated` value for all three pages, rather than trying to determine the actual data fetch time.

**Rationale**: Accurate fetch-time tracking would require changes to `get_stock_data()` and `get_sector_grid_data()` — additive changes that are out of scope for C209 v1. The render-time timestamp is "good enough" for freshness indication (the dot color thresholds are 1h/24h, and page render typically happens within seconds of data fetch).

### Decision 5: Add all i18n keys atomically per page
**Decision**: When integrating each page, simultaneously add the required `sources.*` keys to both `en.yaml` and `zh-TW.yaml` in the same commit.

**Rationale**: Prevents the app from hitting missing-key fallback (which shows the raw key name) if only one locale is updated. The `t()` function returns the key name as fallback — ugly but not a crash.

### Decision 6: Placement — bottom of page, after disclaimer where one exists
**Decision**: Place `_source_section()`:
- `daily_market.py`: After the disclaimer `st.caption()` on line 65 (or replace it if Decision 1 is to remove freshness)
- `business_card/_main.py`: After `_render_footer()` on line 327
- `event_dashboard.py`: After the "關於事件儀表板" info section on line 154

**Rationale**: Progressive disclosure — the source section is supplementary info that should not interrupt the primary content flow. Bottom placement matches the designer's spec for collapsible source sections.

---

## Appendix A: `_source_section()` Signature Reference

```python
def _source_section(
    sources: list[dict],
    last_updated: str,
    *,
    freshness_indicator: bool = True,
) -> None:
```

Each source dict: `{"label": str, "api": str, "time": str}`

Renders: `st.expander("📡 資料來源 / Data Sources", expanded=False)`

Freshness: 🟢 (< 1 hour), 🟡 (< 24 hours), 🔴 (> 24 hours)

## Appendix B: Locale Key Checklist

- [ ] `daily_market.sources.stock_info` — en + zh-TW
- [ ] `daily_market.sources.price_summary` — en + zh-TW
- [ ] `daily_market.sources.sector_data` — en + zh-TW
- [ ] `daily_market.sources.events` — en + zh-TW
- [ ] `business_card.sources.price_valuation` — en + zh-TW
- [ ] `business_card.sources.financial_revenue` — en + zh-TW
- [ ] `business_card.sources.dividend` — en + zh-TW
- [ ] `business_card.sources.news_institutional` — en + zh-TW
- [ ] `business_card.sources.corporate` — en + zh-TW
- [ ] `event_dashboard.sources.events` — en + zh-TW
- [ ] `event_dashboard.sources.interpretation` — en + zh-TW
- [ ] `event_dashboard.sources.local_db` — en + zh-TW
- [ ] `event_dashboard.sources.templates` — en + zh-TW

---

*Prepared: 2026-06-17 for Sprint 25 Day 2 discussion (Round 51)*  
*Component commit: 8ed9a97 | Test baseline: 662 passed, 3.64s*
