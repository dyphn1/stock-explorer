"""Business card section: financial sections (key metrics, dividend, revenue, valuation)."""
import streamlit as st
import pandas as pd
from datetime import date
from src.services.chart import create_revenue_trend_chart, create_revenue_pie_chart, create_valuation_band_chart
from src.services.revenue_analyzer import analyze_revenue_breakdown
from src.services.analogy_engine import (
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_pbr_analogy,
)
from src.services.dividend_analyzer import extract_dividend_summary
from src.services.metric_education import get_metric_explanation, get_top_metrics_for_education
from src.pages._router_base import _白话_card, _info_card, _glossary_tooltip
from src.services import glossary_service


# Mapping from metric_name to glossary term key for D-079 merged popover
_METRIC_GLOSSARY_MAP: dict[str, str] = {
    "PER": "本益比",
    "gross_margin": "毛利率",
    "revenue_yoy": "營收年增率",
    "ROE": "ROE",
    "dividend_yield": "殖利率",
    "PBR": "淨值比",
}


def _render_metric_popover(label: str, value: str, analogy: str, metric_name: str, metric_value: float, stock_id: str, glossary_service) -> None:
    """Render a 白话_card with a ❓ help button that opens a popover with glossary + metric education."""
    # Unique key for this popover button
    popover_key = f"metric_popover_{metric_name}_{stock_id}"

    # Render the card with an inline help button
    col_card, col_help = st.columns([5, 1])
    with col_card:
        _白话_card(label, value, analogy)
    with col_help:
        with st.popover("❓", key=popover_key, help="點擊了解這個指標"):
            edu = get_metric_explanation(metric_name, metric_value, stock_id)
            glossary_key = _METRIC_GLOSSARY_MAP.get(metric_name)
            glossary_term = glossary_service.get_glossary_term(glossary_key) if glossary_key else None

            st.markdown(f"### 📖 {edu['display_name']} 是什麼？")
            st.markdown(f"**數值：{metric_value:.2f} {edu['unit']}**")
            st.markdown("---")

            # ── Glossary definition (D-079: merged from separate _glossary_tooltip) ──
            if glossary_term:
                st.markdown(f"**📖 名詞解釋**\n\n_{glossary_term.get('plain', '')}_")
                if glossary_term.get("analogy"):
                    st.markdown(f"**🌰 名詞比喻**\n\n{glossary_term['analogy']}")
                if glossary_term.get("example"):
                    st.markdown(f"**📌 例子**\n\n{glossary_term['example']}")
                st.markdown("---")

            st.markdown(f"**💡 白話解釋**\n\n{edu['explanation']}")
            st.markdown(f"**🏠 生活比喻**\n\n{edu['analogy']}")
            direction = "⬆️ 越高越好" if edu["is_higher_better"] else "⬇️ 越低越好"
            st.markdown(f"**📊 方向**\n\n{direction}")
            st.markdown(f"**📚 進階背景**\n\n{edu['historical_context']}")


def _render_key_metrics(data: dict, client) -> None:
    """Triple cards: PER/gross margin, revenue/ROE, dividend yield/PBR."""
    latest_per_pbr = data["latest_per_pbr"]
    extra_metrics = data["extra_metrics"]
    monthly_revenue = data["monthly_revenue"]
    industry = data["industry"]
    stock_id = data["stock_id"]

    # 關鍵數字三連卡
    st.markdown("### 📊 關鍵數字")
    col1, col2, col3 = st.columns(3)

    with col1:
        if latest_per_pbr and latest_per_pbr.get("PER"):
            per = latest_per_pbr["PER"]
            _render_metric_popover(
                "本益比 (PER)", f"{per:.1f}", get_per_analogy(per),
                "PER", per, stock_id, glossary_service,
            )
        elif extra_metrics.get("gross_margin"):
            gm = extra_metrics["gross_margin"]
            _render_metric_popover(
                "毛利率", f"{gm:.1f}%", get_gross_margin_analogy(gm),
                "gross_margin", gm, stock_id, glossary_service,
            )

    with col2:
        if len(monthly_revenue) > 0:
            rev = monthly_revenue.iloc[-1]["revenue"] / 1e8
            yoy = extra_metrics.get("revenue_yoy")
            yoy_analogy = get_yoy_analogy(yoy) if yoy is not None else ""
            _render_metric_popover(
                "最近月營收", f"{rev:,.0f} 億",
                get_revenue_analogy(rev, industry) + (f" ｜ {yoy_analogy}" if yoy_analogy else ""),
                "revenue_yoy", yoy if yoy is not None else 0.0, stock_id, glossary_service,
            )
        elif extra_metrics.get("roe"):
            roe = extra_metrics["roe"]
            _render_metric_popover(
                "ROE", f"{roe:.1f}%", get_roe_analogy(roe),
                "ROE", roe, stock_id, glossary_service,
            )

    with col3:
        if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
            dy = latest_per_pbr["dividend_yield"]
            _render_metric_popover(
                "殖利率", f"{dy:.2f}%", get_dividend_analogy(dy),
                "dividend_yield", dy, stock_id, glossary_service,
            )
        elif latest_per_pbr and latest_per_pbr.get("PBR"):
            pbr = latest_per_pbr["PBR"]
            _render_metric_popover(
                "淨值比 (PBR)", f"{pbr:.2f}", get_pbr_analogy(pbr),
                "PBR", pbr, stock_id, glossary_service,
            )

    st.markdown("---")

    # ── 📚 學更多：Metric Education Expander ──
    top_metrics = get_top_metrics_for_education(data)
    if top_metrics:
        with st.expander("📚 學更多：關鍵指標白話教室", expanded=False):
            st.markdown("*點擊每個指標的 ❓ 按鈕，了解它的意思和背後的故事*")
            st.markdown("")
            for item in top_metrics:
                edu = item["explanation"]
                direction_icon = "⬆️ 越高越好" if edu["is_higher_better"] else "⬇️ 越低越好"
                direction_color = "#27AE60" if edu["is_higher_better"] else "#E74C3C"

                _info_card(
                    f"{edu['display_name']} — {item['value']:.2f} {edu['unit']}",
                    f"**💡 {edu['explanation']}**\n\n"
                    f"**🏠 比喻：** {edu['analogy']}\n\n"
                    f"{direction_icon}\n\n"
                    f"*{edu['historical_context']}*",
                    "📖",
                )
                st.markdown("")


def _render_dividend(data: dict, client) -> None:
    """Dividend story: countdown, summary, mini-cards, expandable history table."""
    latest_price = data["latest_price"]

    # === 💵 配息故事 (Dividend Story) ===
    # Extract current price for yield calculation
    _current_price = None
    if latest_price and latest_price.get("close"):
        _current_price = float(latest_price["close"])

    dividend_data = data.get("dividend") if isinstance(data, dict) else None
    div_summary = extract_dividend_summary(
        dividend_data,
        current_price=_current_price,
    )

    if div_summary["has_data"]:
        # ── Countdown to next ex-dividend date ──
        _today = date.today()
        _next_ex_date = None
        _next_ex_year = None
        for _d in div_summary["yearly_dividends"]:
            _ex = _d.get("ex_date", "")
            if not _ex or _ex == "—":
                continue
            try:
                _ex_dt = pd.Timestamp(_ex).date()
                if _ex_dt >= _today:
                    if _next_ex_date is None or _ex_dt < _next_ex_date:
                        _next_ex_date = _ex_dt
                        _next_ex_year = _d.get("year", "")
            except Exception:
                continue

        if _next_ex_date:
            _days_left = (_next_ex_date - _today).days
            _info_card(
                "除息日倒數",
                f"距離除息日還剩 {_days_left} 天（預計 {_next_ex_date.strftime('%Y/%m/%d')}）",
                "⏳",
            )

        # Plain-language headline (tip card style)
        _info_card("配息摘要", div_summary["plain_summary"], "💵")

        # Three mini-cards
        col1, col2, col3 = st.columns(3)
        with col1:
            _白话_card("最近一季", f"{div_summary['latest_cash_div']:.2f} 元", "每股現金股利")
            _glossary_tooltip("每股盈餘", glossary_service)
        with col2:
            annual_str = f"{div_summary['estimated_annual']:.2f} 元" if div_summary['estimated_annual'] else "—"
            _白话_card("預估全年", annual_str, "預估全年配息")
            _glossary_tooltip("殖利率", glossary_service)
        with col3:
            yield_str = f"{div_summary['estimated_yield']:.2f}%" if div_summary['estimated_yield'] else "—"
            _白话_card("殖利率", yield_str, "年化股利／股價")
            _glossary_tooltip("殖利率", glossary_service)

        # Expandable history table
        with st.expander("📋 展開查看歷史除權息紀錄", expanded=False):
            if div_summary["yearly_dividends"]:
                hist_df = pd.DataFrame(div_summary["yearly_dividends"])
                # Rename columns for display
                display_df = hist_df[["year", "cash_div", "ex_date", "status"]].copy()
                display_df.columns = ["年度", "現金股利", "除息日", "狀態"]
                if "stock_div" in hist_df.columns:
                    display_df["股票股利"] = hist_df["stock_div"]

                # Add ex-date badge column
                _today = date.today()
                _badges = []
                for _, _row in display_df.iterrows():
                    _ex = _row["除息日"]
                    if _ex and _ex != "—":
                        try:
                            _ex_dt = pd.Timestamp(_ex).date()
                            if _ex_dt >= _today:
                                _badges.append(
                                    f'<span style="background:#27AE60;color:#FFFFFF;padding:2px 8px;border-radius:10px;font-size:0.75rem;">即將除息</span>'
                                )
                            else:
                                _badges.append(
                                    f'<span style="background:#3498DB;color:#FFFFFF;padding:2px 8px;border-radius:10px;font-size:0.75rem;">已除息</span>'
                                )
                        except Exception:
                            _badges.append("")
                    else:
                        _badges.append("")
                display_df["除息標記"] = _badges

                # Render as HTML table to support badges
                html_rows = []
                _cols = list(display_df.columns)
                _header = "".join(f'<th style="text-align:left;padding:8px 12px;color:#7F8C8D;font-size:0.85rem;border-bottom:2px solid #BDC3C7;">{c}</th>' for c in _cols)
                html_rows.append(f"<tr>{_header}</tr>")
                for _, _r in display_df.iterrows():
                    _cells = ""
                    for _c in _cols:
                        _val = _r[_c]
                        if _c == "除息標記":
                            _cells += f'<td style="padding:8px 12px;border-bottom:1px solid #F8F9FA;">{_val}</td>'
                        else:
                            _cells += f'<td style="padding:8px 12px;color:#2C3E50;border-bottom:1px solid #F8F9FA;">{_val}</td>'
                    html_rows.append(f"<tr>{_cells}</tr>")
                _table_html = (
                    '<table style="width:100%;border-collapse:collapse;font-size:0.9rem;">'
                    + "".join(html_rows)
                    + "</table>"
                )
                st.markdown(_table_html, unsafe_allow_html=True)
    else:
        # Show a subtle note for stocks without dividends
        _info_card("配息摘要", div_summary["plain_summary"], "💡")

    st.markdown("---")


def _render_revenue_breakdown(data: dict, client) -> None:
    """Revenue pie chart + plain-language descriptions + glossary tooltips."""
    financial = data["financial"]
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]

    # 營收組成（圓餅圖 + 白話說明）
    st.markdown("### 📊 營收組成")
    st.markdown("*這家公司靠什麼賺錢？*")

    revenue_items = analyze_revenue_breakdown(financial, stock_id, industry)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = create_revenue_pie_chart(revenue_items, f"{stock_name} 營收來源")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        for item in revenue_items:
            _info_card(f"{item['name']} — {item['value']:.0f}%", item['description'], "📊")
            # Glossary tooltip for each revenue source
            _glossary_tooltip(item['name'], glossary_service)

    st.markdown("---")


def _render_revenue_trend(data: dict, client) -> None:
    """Revenue trend chart or 'no data' message."""
    monthly_revenue = data["monthly_revenue"]
    stock_name = data["stock_name"]

    # 營收趨勢圖
    st.markdown("### 📊 營收趨勢")
    if len(monthly_revenue) > 0:
        fig = create_revenue_trend_chart(monthly_revenue, f"{stock_name} 月營收趨勢")
        st.plotly_chart(fig, use_container_width=True)
        # C170: Glossary tooltip for revenue
        _glossary_tooltip("營業收入", glossary_service)
    else:
        st.info("暫無營收資料")

    st.markdown("---")


def _render_valuation(data: dict, client) -> None:
    """Valuation band chart + interpretation card."""
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]

    # 估值區間圖（歷史 P/E 範圍）
    st.markdown("### 📊 估值區間")
    st.markdown("*目前本益比在歷史上的位置*")

    daily_price = data.get("daily_price")
    if daily_price is not None and len(daily_price) > 0 and len(financial) > 0 and latest_per_pbr and latest_per_pbr.get("PER"):
        fig, interp = create_valuation_band_chart(
            stock_id=stock_id,
            stock_name=stock_name,
            daily_price_df=daily_price,
            financial_df=financial,
            latest_per_pbr=latest_per_pbr,
        )
        st.plotly_chart(fig, use_container_width=True)

        # 白話解讀 — use interpretation returned by chart function
        if interp and interp.get("valuation_text"):
            _info_card("估值解讀", interp["valuation_text"], "💡")
        # C170: Glossary tooltip for PER / PBR
        _glossary_tooltip("本益比", glossary_service)
        _glossary_tooltip("淨值比", glossary_service)
    else:
        st.info("暫無足夠資料計算估值區間")

    st.markdown("---")
