# C201 今日市場動態 (Daily Market Dashboard) — Architecture Design

> **Feature Code**: C201
> **Page Key**: `daily_market`
> **Positioning**: Historian, not stock picker — tells the "story of today's market" in plain language
> **Author**: System Architect
> **Date**: 2026-06-17

---

## 1. Problem Statement

Users need a quick, narrative-driven overview of what happened in the Taiwan stock market today. Not a stock picker, not a heatmap — a **plain-language story** that answers: "What moved the market today, and why should I care?"

The existing sector heatmap (C51) shows *what* sectors moved but doesn't explain *why* or *so what*. C201 fills that gap with narrative context.

---

## 2. Data Sources

All data comes from **free FinMind APIs** via the existing `FinMindClient` + `BatchAPI` + `market_data` service layer.

| Section | API | Client Method | Notes |
|---|---|---|---|
| **Market overview** (TAIEX index) | `taiwan_stock_daily` | `client.get_daily_price("TAIEX", ...)` | Use index proxy `TAIEX` or `0000` if available; fallback to computing from all stock summaries |
| **Sector performance** | `taiwan_stock_info` + `taiwan_stock_daily` | Via `market_data.get_sector_grid_data()` | Reuse existing service — already fetches all stock info + batch summaries + computes sector metrics |
| **Top gainers/losers** | `taiwan_stock_daily` | Via `BatchAPI.get_watchlist_summaries()` | Sort all stocks by `change` field |
| **Advance/decline ratio** | Computed from summaries | `compute_sector_metrics()` output | Count up/down/flat across all stocks |
| **Volume analysis** | `taiwan_stock_daily` | `get_latest_price()` per stock | Sum `volume` across all stocks; compare to 5-day average |
| **Key events** | `taiwan_stock_news` + `config/events.yaml` | `get_all_recent_events()` from adaptive_engine | Reuse M5 event detection; filter for market-level events (earnings, dividend announcements, institutional shifts) |
| **Data freshness** | Computed | Reuse `check_data_freshness()` pattern | Show last update timestamp from most recent API call |

### 2.1 API Call Budget

| API Call | Frequency | Cache TTL |
|---|---|---|
| `taiwan_stock_info` (all) | Once per page load | 24h (shared cache) |
| `taiwan_stock_daily` (batch via BatchAPI) | Once per page load | 24h (shared cache) |
| `taiwan_stock_news` (market-level) | Once per page load | 1h |
| `config/events.yaml` | Once per page load | In-memory cache |

**Total: ~2-3 unique API calls** (stock info cached globally, daily prices cached per stock, news cached short-term). Well within free tier limits.

---

## 3. Page Structure & Layout

### 3.1 Layout (Top to Bottom)

```
┌─────────────────────────────────────────────────────┐
│  _render_navbar_minimal("daily_market")             │
├─────────────────────────────────────────────────────┤
│  📰 今日市場動態                                      │
│  ─────────────────────────────────────────────────  │
│  [Data freshness indicator: 🟢 即時 | 2026-06-17 14:30] │
├─────────────────────────────────────────────────────┤
│  SECTION 1: 市場總覽 (Market Overview)                │
│  ┌─────────────────────────────────────────────────┐│
│  │ _summary_card() — One plain-language paragraph   ││
│  │ "今天台股收在 XX,XXX 點，漲/跌 X.X%..."          ││
│  └─────────────────────────────────────────────────┘│
├─────────────────────────────────────────────────────┤
│  SECTION 2: 市場情緒 (Market Sentiment)               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │_白话_card│ │_白话_card│ │_白话_card│ │_白话_  │ │
│  │ 漲跌比   │ │ 成交量   │ │ 市場溫度 │ │ card  │ │
│  │ 3:1 偏多 │ │ 2,500億  │ │ 🟡 中性  │ │ ...   │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
├─────────────────────────────────────────────────────┤
│  SECTION 3: 板塊動態 (Sector Performance Strip)       │
│  🔥 半導體 +2.3%  🏦 金融 -0.8%  📱 電子 +1.1% ...  │
│  (Horizontal scrollable chips/cards — top 6 sectors) │
├─────────────────────────────────────────────────────┤
│  SECTION 4: 漲跌幅排行 (Top Movers)                   │
│  ┌────────────────────┐ ┌────────────────────┐      │
│  │ 🔴 漲幅 Top 5      │ │ 🟢 跌幅 Top 5      │      │
│  │ #1 台積電 +3.2%    │ │ #1 XX股 -5.1%      │      │
│  │ #2 聯發科 +2.8%    │ │ #2 XX股 -4.2%      │      │
│  │ ...                │ │ ...                │      │
│  └────────────────────┘ └────────────────────┘      │
├─────────────────────────────────────────────────────┤
│  SECTION 5: 重要事件 (Key Events)                     │
│  ┌─────────────────────────────────────────────────┐│
│  │ _info_card() — "台積電法說會優於預期..."         ││
│  │ _info_card() — "外資買超 120 億元..."           ││
│  └─────────────────────────────────────────────────┘│
│  (Only shown if events exist; max 3-5 events)        │
├─────────────────────────────────────────────────────┤
│  ⚠️ 免責聲明                                          │
└─────────────────────────────────────────────────────┘
```

### 3.2 Section Details

#### Section 1: 市場總覽 (Market Overview)
- **Component**: `_summary_card()` (reuse from `_router_base.py`)
- **Content**: One paragraph, plain language, generated from data
- **Generation logic** (template-based, no LLM):
  ```python
  # Pseudo-template:
  "今日台股{market_direction}，收在 {close:,.0f} 點，{change_verb} {abs_change:,.0f} 點（{pct_change:+.2f}%）。
   成交金額約 {volume:,.0f} 億元，{volume_comment}。
   {sector_summary}。"
  ```
- **i18n**: Template string from locale file with `{placeholders}`

#### Section 2: 市場情緒 (Market Sentiment)
- **Components**: 4× `_白话_card()` in `st.columns(4)`
- **Metrics**:
  - 漲跌比 (advance/decline ratio): e.g., "3:1 偏多"
  - 成交量 vs 5日均量: e.g., "2,500 億（高於均量）"
  - 市場溫度: 🟢偏多 / 🟡中性 / 🔴偏空 (based on AD ratio + volume)
  - 上漲家數 / 下跌家數

#### Section 3: 板塊動態 (Sector Performance Strip)
- **Component**: Custom horizontal chip row (Streamlit `st.columns()` or `st.pills()` style)
- **Data**: Top 6 sectors by absolute avg change
- **Display**: Sector name + color-coded change % + emoji
- **Reuse**: `market_data.compute_sector_metrics()` output

#### Section 4: 漲跌幅排行 (Top Movers)
- **Component**: Two-column layout, 5 rows each
- **Data**: Sort all stocks by `change` field from `summary_map`
- **Display**: Rank, name, ID, change %, sector, price
- **Reuse**: Same pattern as `sector_heatmap._render_mover_row()`

#### Section 5: 重要事件 (Key Events)
- **Component**: `_info_card()` per event
- **Data**: `get_all_recent_events(days=1, limit=5)` from adaptive_engine
- **Filter**: Only market-level events (earnings, dividend, institutional)
- **Fallback**: "今日無重大市場事件" if empty

#### Data Freshness Indicator
- **Component**: `st.caption()` with emoji status
- **Logic**: Check `summary_map` timestamps; if latest price date == today → 🟢即時, else → 🟡延遲
- **Position**: Top of page, below title

---

## 4. File Changes

### 4.1 New Files

| File | Purpose |
|---|---|
| `src/pages/daily_market.py` | Main page module — `_render_daily_market(client)` + helper functions |

### 4.2 Modified Files

| File | Change |
|---|---|
| `src/pages/router.py` | Add `"daily_market"` to `PAGE_KEYS` list; add import + `if page_key == "daily_market"` branch in `load_and_render_page()` |
| `locales/zh-TW.yaml` | Add `page.daily_market: "今日市場動態"` + all new i18n keys (see §5) |
| `locales/en.yaml` | Add `page.daily_market: "Daily Market"` + all new English i18n keys |
| `src/pages/url_sync.py` | Add `"今日市場動態"` to `VALID_PAGES` set |

### 4.3 Reused Files (No Changes)

| File | What's Reused |
|---|---|
| `src/pages/_router_base.py` | `_白话_card()`, `_info_card()`, `_summary_card()`, `_section_title()` |
| `src/services/market_data.py` | `get_sector_grid_data()`, `compute_sector_metrics()`, `get_all_summaries()` |
| `src/data/batch_api.py` | `BatchAPI.get_watchlist_summaries()` |
| `src/services/adaptive_engine.py` | `get_all_recent_events()`, `check_data_freshness()` |
| `src/data/finmind_client.py` | All existing client methods (no new methods needed) |

---

## 5. i18n Keys

### 5.1 Page Key (in `page:` section)

```yaml
# zh-TW.yaml
page:
  daily_market: "今日市場動態"   # already exists? NO — new key

# en.yaml
page:
  daily_market: "Daily Market"
```

### 5.2 New Section Keys (new `daily_market:` section)

```yaml
# zh-TW.yaml
daily_market:
  title: "今日市場動態"
  subtitle: "今天台股發生了什麼事"
  last_updated: "最後更新：{time}"
  freshness_fresh: "🟢 即時"
  freshness_stale: "🟡 延遲"
  freshness_unknown: "⚪ 未知"

  overview:
    title: "📰 市場總覽"
    template_bull: "今日台股走強，收在 {close:,.0f} 點，上漲 {abs_change:,.0f} 點（{pct_change:+.2f}%）。成交金額約 {volume:,.0f} 億元，{volume_comment}。{sector_summary}。"
    template_bear: "今日台股走弱，收在 {close:,.0f} 點，下跌 {abs_change:,.0f} 點（{pct_change:+.2f}%）。成交金額約 {volume:,.0f} 億元，{volume_comment}。{sector_summary}。"
    template_flat: "今日台股持平，收在 {close:,.0f} 點，小漲 {abs_change:,.0f} 點（{pct_change:+.2f}%）。成交金額約 {volume:,.0f} 億元，{volume_comment}。{sector_summary}。"
    volume_above: "高於均量"
    volume_below: "低於均量"
    volume_normal: "與均量相當"
    sector_lead_up: "以 {sector} 板塊漲幅最大（{pct:+.2f}%）"
    sector_lead_down: "以 {sector} 板塊跌幅最大（{pct:+.2f}%）"

  sentiment:
    title: "🌡️ 市場情緒"
    ad_ratio: "漲跌比"
    ad_ratio_value: "{up}:{down}"
    volume: "成交量"
    volume_unit: "億元"
    mood: "市場溫度"
    mood_bullish: "🟢 偏多"
    mood_neutral: "🟡 中性"
    mood_bearish: "🔴 偏空"
    up_count: "上漲家數"
    down_count: "下跌家數"

  sectors:
    title: "🏭 板塊動態"
    top_n: "前 {n} 板塊"

  movers:
    title: "🔥 漲跌幅排行"
    gainers: "🔴 漲幅排行"
    losers: "🟢 跌幅排行"
    rank: "#{rank}"
    price: "NT${price}"

  events:
    title: "📋 重要事件"
    empty: "今日無重大市場事件"

  disclaimer: "⚠️ 本頁面僅供認識市場使用，不構成任何投資建議。"
```

```yaml
# en.yaml
daily_market:
  title: "Daily Market"
  subtitle: "What happened in the Taiwan market today"
  last_updated: "Last updated: {time}"
  freshness_fresh: "🟢 Live"
  freshness_stale: "🟡 Delayed"
  freshness_unknown: "⚪ Unknown"

  overview:
    title: "📰 Market Overview"
    template_bull: "The Taiwan market closed at {close:,.0f}, up {abs_change:,.0f} pts ({pct_change:+.2f}%). Trading volume was approximately {volume:,.0f} hundred million, {volume_comment}. {sector_summary}."
    template_bear: "The Taiwan market closed at {close:,.0f}, down {abs_change:,.0f} pts ({pct_change:+.2f}%). Trading volume was approximately {volume:,.0f} hundred million, {volume_comment}. {sector_summary}."
    template_flat: "The Taiwan market closed flat at {close:,.0f}, up slightly {abs_change:,.0f} pts ({pct_change:+.2f}%). Trading volume was approximately {volume:,.0f} hundred million, {volume_comment}. {sector_summary}."
    volume_above: "above average"
    volume_below: "below average"
    volume_normal: "in line with average"
    sector_lead_up: "{sector} led gains (+{pct:+.2f}%)"
    sector_lead_down: "{sector} led losses ({pct:+.2f}%)"

  sentiment:
    title: "🌡️ Market Sentiment"
    ad_ratio: "A/D Ratio"
    ad_ratio_value: "{up}:{down}"
    volume: "Volume"
    volume_unit: "100M TWD"
    mood: "Market Mood"
    mood_bullish: "🟢 Bullish"
    mood_neutral: "🟡 Neutral"
    mood_bearish: "🔴 Bearish"
    up_count: "Advancers"
    down_count: "Decliners"

  sectors:
    title: "🏭 Sector Performance"
    top_n: "Top {n} Sectors"

  movers:
    title: "🔥 Top Movers"
    gainers: "🔴 Top Gainers"
    losers: "🟢 Top Losers"
    rank: "#{rank}"
    price: "NT${price}"

  events:
    title: "📋 Key Events"
    empty: "No major market events today"

  disclaimer: "⚠️ This page is for educational purposes only and does not constitute investment advice."
```

**Total new i18n keys: ~50** (25 per locale)

---

## 6. Implementation Details

### 6.1 Page Module: `src/pages/daily_market.py`

```python
"""
C201 今日市場動態 — Daily Market Dashboard
Narrative-driven market overview: what happened in the Taiwan market today.
"""

import streamlit as st
import numpy as np
from datetime import datetime
from src.pages._router_base import _白话_card, _info_card, _summary_card, _section_title
from src.core.i18n import t
from src.services.market_data import (
    get_sector_grid_data,
    get_all_stock_info,
    get_sector_stocks,
)
from src.services.adaptive_engine import get_all_recent_events


def _render_daily_market(client):
    """Daily Market Dashboard — main entry point."""
    st.markdown(f"## 📰 {t('daily_market.title')}")
    st.markdown(f"*{t('daily_market.subtitle')}*")
    st.markdown("---\n")

    # ── Load all market data via existing service ──
    with st.spinner(t("status.loading_page")):
        try:
            grid_data = get_sector_grid_data(client)
        except Exception as e:
            st.error(f"無法載入市場資料：{e}")
            return

    all_stock_info = grid_data["all_stock_info"]
    sector_metrics = grid_data["sector_metrics"]
    summary_map = grid_data["summary_map"]
    sector_stocks = grid_data["sector_stocks"]

    if not summary_map:
        st.warning("目前無市場資料可顯示。")
        return

    # ── Data freshness ──
    _render_freshness(summary_map)

    # ── Section 1: Market Overview ──
    _render_overview(summary_map, sector_metrics)

    st.markdown("---\n")

    # ── Section 2: Market Sentiment ──
    _render_sentiment(summary_map)

    st.markdown("---\n")

    # ── Section 3: Sector Performance Strip ──
    _render_sector_strip(sector_metrics)

    st.markdown("---\n")

    # ── Section 4: Top Movers ──
    _render_top_movers(summary_map, sector_stocks)

    st.markdown("---\n")

    # ── Section 5: Key Events ──
    _render_key_events()

    # ── Disclaimer ──
    st.caption(t("daily_market.disclaimer"))


def _render_freshness(summary_map: dict):
    """Show data freshness caption."""
    # Find the most recent date across all stock summaries
    latest_date = None
    for s in summary_map.values():
        price = s.get("latest_price")
        if price:
            d = str(price)[:10] if isinstance(price, str) else None
            if d and (latest_date is None or d > latest_date):
                latest_date = d

    today = datetime.now().strftime("%Y-%m-%d")
    if latest_date == today:
        status = t("daily_market.freshness_fresh")
    elif latest_date:
        status = t("daily_market.freshness_stale")
    else:
        status = t("daily_market.freshness_unknown")

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.caption(f"{status} ｜ {t('daily_market.last_updated', time=now_str)}")


def _render_overview(summary_map: dict, sector_metrics: dict):
    """Section 1: One-paragraph market overview."""
    _section_title(t("daily_market.overview.title"))

    all_changes = [s["change"] for s in summary_map.values() if s.get("change") is not None]
    if not all_changes:
        _summary_card(t("daily_market.overview.title"), "無資料")
        return

    # Compute market-level stats
    avg_change = float(np.mean(all_changes))
    up_count = sum(1 for c in all_changes if c > 0)
    down_count = sum(1 for c in all_changes if c < 0)
    total_stocks = len(all_changes)

    # Find leading/lagging sectors
    if sector_metrics:
        sorted_sectors = sorted(sector_metrics.items(), key=lambda x: x[1]["avg_change"], reverse=True)
        lead_sector = sorted_sectors[0]
        lag_sector = sorted_sectors[-1]
        sector_summary = t(
            "daily_market.overview.sector_lead_up",
            sector=lead_sector[0],
            pct=lead_sector[1]["avg_change"],
        )
    else:
        sector_summary = ""

    # Estimate total volume (sum of all stock volumes)
    total_volume = 0
    for s in summary_map.values():
        lp = s.get("latest_price")
        if isinstance(lp, (int, float)) and lp > 0:
            total_volume += lp
    total_volume_billions = total_volume / 1e8  # Convert to 億元

    # Pick template based on direction
    if avg_change > 0.5:
        template_key = "daily_market.overview.template_bull"
    elif avg_change < -0.5:
        template_key = "daily_market.overview.template_bear"
    else:
        template_key = "daily_market.overview.template_flat"

    # Volume comment
    volume_comment = t("daily_market.overview.volume_normal")  # Simplified; could compare to MA

    overview_text = t(
        template_key,
        close=total_stocks * 100,  # Placeholder — real TAIEX value from index data
        abs_change=abs(avg_change),
        pct_change=avg_change,
        volume=total_volume_billions,
        volume_comment=volume_comment,
        sector_summary=sector_summary,
    )

    _summary_card(t("daily_market.overview.title"), overview_text)


def _render_sentiment(summary_map: dict):
    """Section 2: Market sentiment indicators."""
    _section_title(t("daily_market.sentiment.title"))

    all_changes = [s["change"] for s in summary_map.values() if s.get("change") is not None]
    if not all_changes:
        st.info("無情緒指標資料。")
        return

    up_count = sum(1 for c in all_changes if c > 0)
    down_count = sum(1 for c in all_changes if c < 0)
    flat_count = len(all_changes) - up_count - down_count

    # Market mood
    ad_ratio = up_count / max(down_count, 1)
    if ad_ratio >= 2.0:
        mood = t("daily_market.sentiment.mood_bullish")
    elif ad_ratio >= 0.8:
        mood = t("daily_market.sentiment.mood_neutral")
    else:
        mood = t("daily_market.sentiment.mood_bearish")

    # Total volume
    total_volume = sum(
        s.get("latest_price", 0) or 0
        for s in summary_map.values()
    )
    volume_display = f"{total_volume / 1e8:,.0f} {t('daily_market.sentiment.volume_unit')}"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        _白话_card(
            t("daily_market.sentiment.ad_ratio"),
            t("daily_market.sentiment.ad_ratio_value", up=up_count, down=down_count),
            f"⚪ 平盤 {flat_count}",
        )
    with col2:
        _白话_card(
            t("daily_market.sentiment.volume"),
            volume_display,
            "",
        )
    with col3:
        _白话_card(
            t("daily_market.sentiment.mood"),
            mood,
            f"漲跌比 {ad_ratio:.1f}",
        )
    with col4:
        _白话_card(
            t("daily_market.sentiment.up_count"),
            str(up_count),
            t("daily_market.sentiment.down_count") + f" {down_count}",
        )


def _render_sector_strip(sector_metrics: dict):
    """Section 3: Horizontal sector performance strip."""
    _section_title(t("daily_market.sectors.title"))

    if not sector_metrics:
        st.info("無板塊資料。")
        return

    # Sort by avg change, take top 6
    sorted_sectors = sorted(
        sector_metrics.items(),
        key=lambda x: x[1]["avg_change"],
        reverse=True,
    )[:6]

    cols = st.columns(len(sorted_sectors))
    for i, (sector, metrics) in enumerate(sorted_sectors):
        chg = metrics["avg_change"]
        sign = "+" if chg > 0 else ""
        color = "#E74C3C" if chg > 0 else ("#27AE60" if chg < 0 else "#7F8C8D")
        with cols[i]:
            st.markdown(f"""
            <div style="background:#F8F9FA;border-radius:10px;padding:0.8rem;text-align:center;border-top:3px solid {color};">
                <div style="font-size:0.8rem;color:#7F8C8D;">{sector}</div>
                <div style="font-size:1.3rem;font-weight:700;color:{color};">{sign}{chg:.2f}%</div>
                <div style="font-size:0.7rem;color:#7F8C8D;">🔴{metrics['up']} 🟢{metrics['down']}</div>
            </div>
            """, unsafe_allow_html=True)


def _render_top_movers(summary_map: dict, sector_stocks: dict):
    """Section 4: Top 5 gainers and losers."""
    _section_title(t("daily_market.movers.title"))

    # Build reverse mapping: stock_id -> sector
    stock_sector = {}
    for sector, sids in sector_stocks.items():
        for sid in sids:
            stock_sector[sid] = sector

    # Sort all stocks by change
    all_stocks = [
        {**s, "sector": stock_sector.get(s["stock_id"], "")}
        for s in summary_map.values()
        if s.get("change") is not None
    ]
    all_stocks.sort(key=lambda x: x["change"], reverse=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {t('daily_market.movers.gainers')}")
        for rank, s in enumerate(all_stocks[:5], 1):
            _render_mover_row(rank, s, True)

    with col2:
        st.markdown(f"#### {t('daily_market.movers.losers')}")
        for rank, s in enumerate(reversed(all_stocks[-5:]), 1):
            _render_mover_row(rank, s, False)


def _render_mover_row(rank: int, s: dict, is_gainer: bool):
    """Render a single mover row."""
    sign = "+" if s["change"] > 0 else ""
    color = "#E74C3C" if is_gainer else "#27AE60"
    c1, c2 = st.columns([3, 1])
    with c1:
        st.text(f"{t('daily_market.movers.rank', rank=rank)} {s.get('stock_name', s['stock_id'])} ({s['stock_id']})")
    with c2:
        st.markdown(f"<span style='color:{color};font-weight:700;'>{sign}{s['change']:.2f}%</span>", unsafe_allow_html=True)
    st.caption(f"{s.get('sector', '')} ｜ {t('daily_market.movers.price', price=s.get('latest_price', '—'))}")
    st.write("")


def _render_key_events():
    """Section 5: Key market events from adaptive engine."""
    _section_title(t("daily_market.events.title"))

    try:
        events = get_all_recent_events(days=1, limit=5)
    except Exception:
        events = []

    if not events:
        st.info(t("daily_market.events.empty"))
        return

    for event in events[:5]:
        event_title = event.get("title", event.get("event_type", ""))
        event_desc = event.get("description", event.get("implication", ""))
        _info_card(event_title, event_desc)
```

### 6.2 Router Changes

In `router.py`:
1. Add `"daily_market"` to `PAGE_KEYS` list
2. Add import: `from src.pages.daily_market import _render_daily_market`
3. Add branch in `load_and_render_page()`:
   ```python
   if page_key == "daily_market":
       _render_navbar_minimal(page_key)
       with st.spinner(t("status.loading_page")):
           _render_daily_market(client)
       return
   ```

### 6.3 URL Sync Changes

In `url_sync.py`, add `"今日市場動態"` to `VALID_PAGES` set.

---

## 7. Effort Estimate

| Task | Hours |
|---|---|
| `src/pages/daily_market.py` (new page module) | 3-4 |
| Router + URL sync modifications | 0.5 |
| i18n keys (zh-TW + en, ~50 keys) | 1.5 |
| Testing & refinement | 1-2 |
| **Total** | **6-8 hours** |

---

## 8. Alternative Approaches

### Alternative A: Lightweight — Summary Cards Only (No Batch Fetch)

**Description**: Instead of fetching all stock summaries via BatchAPI, use only the TAIEX index data + a small set of representative stocks (e.g., top 20 by market cap).

**Pros**:
- Faster page load (fewer API calls)
- Simpler code
- Lower API usage

**Cons**:
- Incomplete market picture (misses small/mid-cap movements)
- Can't compute accurate advance/decline ratio
- Sector coverage may be incomplete
- Doesn't align with "historian" positioning — feels shallow

**Effort**: 3-4 hours

### Alternative B: Heavy — Full Narrative Generation with LLM

**Description**: Use an LLM (e.g., Gemini API) to generate the market overview paragraph and event summaries dynamically.

**Pros**:
- More natural, varied language
- Can synthesize complex multi-factor narratives
- Impressive UX

**Cons**:
- Requires paid API (violates free-only constraint)
- Adds latency (LLM call time)
- Non-deterministic output — harder to test
- Overkill for MVP; can be added later as enhancement

**Effort**: 10-12 hours + ongoing API costs

### Alternative C: Static Report — Pre-computed Daily Snapshot

**Description**: Generate the market report once per day (via cron job), save as JSON, and display the cached version.

**Pros**:
- Instant page load
- No API calls at render time
- Consistent snapshot throughout the day

**Cons**:
- Not real-time — stale during market hours
- Requires cron infrastructure
- Defeats the purpose of "today's market" — users expect live data
- More complex architecture for marginal gain

**Effort**: 8-10 hours

---

## 9. Recommendation

**Recommended: Main approach (§6) — Template-based narrative with full BatchAPI data fetch.**

**Rationale**:
1. **Follows existing patterns**: Reuses `market_data.get_sector_grid_data()`, `BatchAPI`, `_白话_card()`, `_summary_card()`, `_info_card()` — minimal new code
2. **Free-only**: All data from free FinMind APIs, no LLM costs
3. **Real-time**: Live data at page load, not pre-computed
4. **Narrative-driven**: Template-based generation is deterministic, testable, and i18n-friendly — no LLM needed for MVP
5. **PPT-style**: One key point per section, plain language, historian tone
6. **Reasonable effort**: 6-8 hours, single new file + minor modifications

**Future enhancements** (post-MVP):
- Add LLM-generated narrative (Alternative B) as optional enhancement
- Add intraday update button for real-time refresh
- Add historical comparison ("vs last week", "vs last month")
- Add export/share functionality for the daily report

---

## 10. Open Questions

1. **TAIEX index data**: Does FinMind's free tier provide TAIEX index data directly? If not, we compute a proxy from all stock summaries (weighted average). Need to verify.
2. **Volume baseline**: For "volume vs average" comparison, we need 5-day average volume. This requires either (a) storing historical volume data, or (b) simplifying to just show absolute volume. Recommend (b) for MVP.
3. **Event filtering**: The adaptive engine's `get_all_recent_events()` returns per-stock events. We need to filter for market-level events only. May need a new parameter or post-filter logic.
4. **Market hours handling**: Should the page show "market closed" state with yesterday's data? Recommended: yes, with a clear "last trading day" indicator.
