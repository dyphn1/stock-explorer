"""Business card section: health and risk sections."""
import streamlit as st
from src.services.chart import create_health_snowflake
from src.services.health_scoring import compute_health_scores, get_health_summary
from src.services.risk_analyzer import assess_risk
from src.pages._router_base import _info_card, _explain_button, _mini_score_card
from src.pages.business_card._helpers import (
    get_health_dimension_explanation,
    _render_risk_dimension,
    _get_health_metric_values,
)

# 產業標竿對應表（產業 → 標竿公司）
INDUSTRY_BENCHMARKS = {
    "半導體業": ("2330", "台積電"),
    "電子工業": ("2317", "鴻海"),
    "金融保險": ("2881", "富邦金"),
    "電腦及週邊設備業": ("2382", "廣達"),
    "生技醫療業": ("1598", "岱宇"),
    "觀光餐旅": ("2707", "晶華"),
    "電機機械": ("1590", "亞德客"),
    "建材營造": ("2542", "興富發"),
    "化學工業": ("1301", "台塑"),
    "通信網路業": ("4904", "遠傳"),
    "電子零組件業": ("2308", "台達電"),
    "鋼鐵工業": ("2002", "中鋼"),
    "水泥工業": ("1101", "台泥"),
    "塑膠工業": ("1301", "台塑"),
    "紡織纖維": ("1402", "遠東新"),
    "食品工業": ("1216", "統一"),
    "汽車工業": ("2207", "和泰車"),
    "航運業": ("2633", "台灣高鐵"),
    "光電業": ("3008", "大立光"),
    "其他電子業": ("2357", "華碩"),
    "油電燃氣業": ("9904", "大潤發"),
    "貿易百貨": ("2912", "統一超商"),
    "橡膠工業": ("2105", "正新"),
    "造紙工業": ("1907", "永豐餘"),
    "玻璃陶瓷": ("1802", "台玻"),
    "運動休閒": ("9910", "豐泰"),
    "居家生活": ("9945", "潤泰新"),
    "其他": ("2330", "台積電"),
}


def _fetch_benchmark_health_scores(client, industry: str, stock_id: str):
    """
    Fetch health scores for the industry benchmark company.

    Returns a dict of dimension → score (0-100), or None if unavailable.
    """
    if not industry or industry not in INDUSTRY_BENCHMARKS:
        return None

    bench_id, bench_name = INDUSTRY_BENCHMARKS[industry]

    # Don't benchmark against self
    if bench_id == stock_id:
        return None

    try:
        bench_per_pbr = client.get_latest_per_pbr(bench_id)
        bench_financial = client.get_financial_statement(bench_id)
        bench_balance = client.get_balance_sheet(bench_id)
        bench_revenue = client.get_monthly_revenue(bench_id)

        # Build extra_metrics dict from financial/balance data
        bench_extra = {}

        # Extract key metrics from financial statement
        rev_col = None
        gp_col = None
        op_col = None
        ni_col = None
        latest = None
        if bench_financial is not None and len(bench_financial) > 0:
            def _find_col(df, keywords):
                for col in df.columns:
                    for kw in keywords:
                        if kw in str(col):
                            return col
                return None

            # Gross margin
            rev_col = _find_col(bench_financial, ["營業收入", "Revenue", "revenue"])
            gp_col = _find_col(bench_financial, ["營業毛利", "Gross_Profit", "gross_profit"])
            op_col = _find_col(bench_financial, ["營業利益", "Operating_Income", "operating_income"])
            ni_col = _find_col(bench_financial, ["淨利", "Net_Income", "net_income"])

            latest = bench_financial.iloc[-1]
            if rev_col and gp_col:
                rev = latest.get(rev_col)
                gp = latest.get(gp_col)
                if rev and gp and float(rev) > 0:
                    bench_extra["gross_margin"] = float(gp) / float(rev) * 100

            if rev_col and ni_col:
                rev = latest.get(rev_col)
                ni = latest.get(ni_col)
                if rev and ni and float(rev) > 0:
                    bench_extra["net_margin"] = float(ni) / float(rev) * 100

            # Revenue YoY
            try:
                if rev_col and len(bench_financial) >= 2:
                    curr_rev = float(latest[rev_col]) if latest.get(rev_col) else None
                    prev_rev = float(bench_financial.iloc[-2][rev_col]) if bench_financial.iloc[-2].get(rev_col) else None
                    if curr_rev and prev_rev and prev_rev > 0:
                        bench_extra["revenue_yoy"] = (curr_rev - prev_rev) / abs(prev_rev) * 100
            except Exception:
                pass
        else:
            latest = None

        # Debt ratio from balance sheet
        if bench_balance is not None and len(bench_balance) > 0:
            def _find_bal_col(df, keywords):
                for col in df.columns:
                    for kw in keywords:
                        if kw in str(col):
                            return col
                return None

            debt_col = _find_bal_col(bench_balance, ["負債總計", "Total_Liabilities", "total_liabilities"])
            asset_col = _find_bal_col(bench_balance, ["資產總計", "Total_Assets", "total_assets"])
            current_asset_col = _find_bal_col(bench_balance, ["流動資產", "Current_Assets", "current_assets"])
            current_liab_col = _find_bal_col(bench_balance, ["流動負債", "Current_Liabilities", "current_liabilities"])
            equity_col = _find_bal_col(bench_balance, ["權益總計", "Total_Equity", "total_equity"])

            bal_latest = bench_balance.iloc[-1]

            if debt_col and asset_col:
                debt = bal_latest.get(debt_col)
                asset = bal_latest.get(asset_col)
                if debt and asset and float(asset) > 0:
                    bench_extra["debt_ratio"] = float(debt) / float(asset) * 100

            if current_asset_col and current_liab_col:
                ca = bal_latest.get(current_asset_col)
                cl = bal_latest.get(current_liab_col)
                if ca and cl and float(cl) > 0:
                    bench_extra["current_ratio"] = float(ca) / float(cl)

            # ROE: Net Income / Equity
            if equity_col and ni_col:
                try:
                    ni_val = latest.get(ni_col) if bench_financial is not None and len(bench_financial) > 0 else None
                    eq_val = bal_latest.get(equity_col)
                    if ni_val and eq_val and float(eq_val) > 0:
                        bench_extra["roe"] = float(ni_val) / float(eq_val) * 100
                except Exception:
                    pass

        scores = compute_health_scores(
            extra_metrics=bench_extra,
            latest_per_pbr=bench_per_pbr,
            financial_df=bench_financial,
            monthly_revenue=bench_revenue,
        )
        return scores if scores else None

    except Exception:
        return None


def _render_health(data: dict, client) -> None:
    """C43 Health Snowflake chart + 5-dimension score cards + summary."""
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    monthly_revenue = data["monthly_revenue"]
    stock_name = data["stock_name"]
    stock_id = data["stock_id"]
    industry = data["industry"]

    # 🏥 公司健康狀況 (C43: Health Snowflake)
    health_scores = compute_health_scores(
        extra_metrics=extra_metrics,
        latest_per_pbr=latest_per_pbr,
        financial_df=financial,
        monthly_revenue=monthly_revenue,
    )
    if health_scores:
        st.markdown("### 🏥 公司健康狀況")

        # ── Fetch benchmark overlay data ──
        benchmark_scores = None
        benchmark_label = "同業平均"
        if industry:
            benchmark_scores = _fetch_benchmark_health_scores(client, industry, stock_id)
            if benchmark_scores:
                # Determine label: use the benchmark company name
                bench_info = INDUSTRY_BENCHMARKS.get(industry)
                if bench_info:
                    _, bench_name = bench_info
                    benchmark_label = f"{bench_name}"

        metric_values = _get_health_metric_values(extra_metrics, latest_per_pbr)
        health_fig = create_health_snowflake(
            stock_name,
            health_scores,
            metric_values=metric_values,
            benchmark_scores=benchmark_scores,
            benchmark_label=benchmark_label,
        )
        st.plotly_chart(health_fig, use_container_width=True)

        # 五維度分數明細
        dim_cols = st.columns(5)
        for i, (dim_name, score) in enumerate(health_scores.items()):
            with dim_cols[i]:
                if score >= 70:
                    indicator = "🟢"
                elif score >= 40:
                    indicator = "🟡"
                else:
                    indicator = "🔴"
                _mini_score_card(f"{indicator} {dim_name}", score)
                explanation = get_health_dimension_explanation(dim_name, score)
                if explanation:
                    st.caption(explanation)
                if dim_name in metric_values and metric_values[dim_name]:
                    metric_text = " · ".join(metric_values[dim_name])
                    st.caption(metric_text)
                _explain_button(
                    metric_name=dim_name,
                    metric_value=f"{score:.0f} 分",
                    key_prefix=f"health_{stock_id}",
                    source_label="📊 系統估算",
                )

        # 白話健康摘要
        health_summary = get_health_summary(health_scores)
        _info_card("健康摘要", health_summary, "🏥")


def _render_risk(data: dict, client) -> None:
    """C44 Risk Analysis with expandable dimensions."""
    stock_name = data["stock_name"]

    # ⚠️ 風險分析 (C44: Risk Analysis)
    risk = assess_risk(data)
    has_risk_dims = any(
        risk.get(dim) is not None
        for dim in ("customer_concentration", "financial_health", "event_based")
    )
    if has_risk_dims:
        with st.expander("⚠️ 風險分析 — 什麼可能出問題？", expanded=False):
            if risk.get("summary_text"):
                st.caption(risk["summary_text"])
            for dim_key in ("customer_concentration", "financial_health", "event_based"):
                dim = risk.get(dim_key)
                if dim is None:
                    continue
                _render_risk_dimension(dim, stock_name)
