"""
同業比較頁 — M2 第三頁
目標：跟產業第一名差在哪？
"""

import streamlit as st
import pandas as pd
from src.core.i18n import t
from src.data.finmind_client import FinMindClient
from src.services.chart import create_comparison_radar
from src.services.analogy_engine import (
    get_gross_margin_analogy,
    get_roe_analogy,
    get_per_analogy,
)
from src.pages._router_base import _section_title, _info_card, _白话_card
from src.services.financial_metrics import find_financial_value
from src.services.benchmarks import get_industry_benchmarks
from src.services.roe_calculator import calc_roe_ttm

# Re-export INDUSTRY_BENCHMARKS for backward compatibility
INDUSTRY_BENCHMARKS = get_industry_benchmarks()


def _find_fallback_benchmark(industry: str, stock_id: str):
    """Find the largest company in the same industry as a fallback benchmark."""
    try:
        client = FinMindClient(cache_dir=".cache")
        all_stocks = client.get_stock_info()  # cached full-universe call
        if all_stocks is None or all_stocks.empty:
            return None
        # Filter same industry, Exclude self
        peers = all_stocks[
            (all_stocks["industry_category"] == industry) &
            (all_stocks["stock_id"] != stock_id)
        ]
        if peers.empty:
            return None
        # Sort by stock_id ascending (proxy for market establishment)
        peers = peers.sort_values("stock_id")
        best = peers.iloc[0]
        return (best["stock_id"], best["stock_name"])
    except Exception:
        return None


def _render_single_company_view(data: dict, stock_name: str, industry: str):
    """Show single-company data when no benchmark is available."""
    st.warning(t("peer.comparison.no_benchmark", industry=industry, stock_name=stock_name))
    # Show the target company's key metrics in a simple table/card
    metrics = {}
    if data.get("latest_per_pbr") is not None and not data["latest_per_pbr"].empty:
        latest = data["latest_per_pbr"].iloc[-1]
        metrics[t("peer.comparison.metric.pe")] = latest.get("PE_ratio", "—")
        metrics[t("peer.comparison.metric.pb")] = latest.get("PB_ratio", "—")
        metrics[t("peer.comparison.metric.dividend_yield")] = latest.get("dividend_yield", "—")
    if data.get("financial") is not None and not data["financial"].empty:
        latest_fs = data["financial"].iloc[-1]
        # extract whatever fields are available
        for field, label_key in [("net_profit_margin", "peer.comparison.metric.net_margin"), ("ROE", "peer.comparison.metric.roe")]:
            if field in latest_fs:
                metrics[t(label_key)] = latest_fs[field]

    if metrics:
        cols = st.columns(min(len(metrics), 4))
        for i, (label, value) in enumerate(metrics.items()):
            with cols[i % 4]:
                _白话_card(label, str(value), "")
    else:
        st.info(t("peer.comparison.no_metrics"))
    st.caption(t("peer.comparison.switch_industry"))


def _render_peer_comparison(data: dict, client):
    """同業比較主頁"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    balance_sheet = data["balance_sheet"]

    st.markdown(t("peer.comparison.title", stock_name=stock_name))
    st.markdown(t("peer.comparison.subtitle"))
    st.markdown("---")

    # 決定標竿公司
    benchmark_id, benchmark_name = INDUSTRY_BENCHMARKS.get(industry, (None, None))
    is_fallback = False

    if benchmark_id is None:
        with st.spinner(t("peer.comparison.searching_benchmark")):
            fallback = _find_fallback_benchmark(industry, stock_id)
        if fallback:
            benchmark_id, benchmark_name = fallback
            is_fallback = True
        else:
            _render_single_company_view(data, stock_name, industry)
            return

    if is_fallback:
        st.info(t("peer.comparison.fallback_benchmark"))

    # 避免自己跟自己比
    if benchmark_id == stock_id:
        st.info(t("peer.comparison.is_benchmark", stock_name=stock_name, industry=industry))
        _info_card(t("peer.comparison.benchmark_status"),
                   t("peer.comparison.benchmark_status_desc", stock_name=stock_name, industry=industry),
                   "🏆")
        return

    st.markdown(t("peer.comparison.industry_benchmark", industry=industry, benchmark_name=benchmark_name, benchmark_id=benchmark_id))

    # 載入標竿公司資料
    with st.spinner(t("peer.comparison.loading_benchmark", benchmark_name=benchmark_name)):
        bench_data = _get_benchmark_data(client, benchmark_id)

    if bench_data is None:
        st.error(t("peer.comparison.load_failed", benchmark_name=benchmark_name, stock_name=stock_name))
        _render_single_company_view(data, stock_name, industry)
        return

    st.markdown("---")

    # ── 1. 並排比較表 ────────────────────────────────
    _section_title(t("peer.comparison.side_by_side"))

    # 收集比較指標
    metrics = _collect_comparison_metrics(data, bench_data)

    if metrics:
        # 建立比較表格
        comparison_rows = []
        for metric_name, (target_val, bench_val) in metrics.items():
            diff = target_val - bench_val
            diff_pct = (diff / bench_val * 100) if bench_val != 0 else 0
            comparison_rows.append({
                t("peer.comparison.col_metric"): metric_name,
                f"{stock_name}": f"{target_val:.1f}",
                f"{benchmark_name}": f"{bench_val:.1f}",
                t("peer.comparison.col_diff"): f"{diff:+.1f} ({diff_pct:+.0f}%)",
            })

        comp_df = pd.DataFrame(comparison_rows)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        # 白話解讀
        _render_metric_analysis(metrics, stock_name, benchmark_name, industry)
    else:
        st.info(t("peer.comparison.no_comparison_data"))

    st.markdown("---")

    # ── 2. 雷達圖 ────────────────────────────────────
    _section_title(t("peer.comparison.radar_chart"))

    radar_metrics = _prepare_radar_data(data, bench_data)
    if radar_metrics:
        fig = create_comparison_radar(radar_metrics, stock_name, benchmark_name)
        st.plotly_chart(fig, use_container_width=True)
        _info_card(t("peer.comparison.radar_guide_title"),
                   t("peer.comparison.radar_guide", stock_name=stock_name, benchmark_name=benchmark_name),
                   "🎯")
    else:
        st.info(t("peer.comparison.no_radar_data"))

    st.markdown("---")

    # ── 3. 差異分析 ──────────────────────────────────
    _section_title(t("peer.comparison.diff_analysis"))

    _render_difference_analysis(metrics, stock_name, benchmark_name, industry)


def _get_benchmark_data(client, benchmark_id: str) -> dict:
    """取得標竿公司的關鍵數據"""
    try:
        stock_info = client.get_stock_info(benchmark_id)
        if len(stock_info) == 0:
            return None

        bench_name = stock_info.iloc[0]["stock_name"]
        bench_industry = stock_info.iloc[0]["industry_category"]
        bench_per_pbr = client.get_latest_per_pbr(benchmark_id)
        bench_financial = client.get_financial_statement(benchmark_id)
        bench_balance = client.get_balance_sheet(benchmark_id)
        bench_revenue = client.get_monthly_revenue(benchmark_id)

        # 計算額外指標
        bench_metrics = {}
        if bench_financial is not None and len(bench_financial) > 0:
            try:
                latest_date = bench_financial["date"].max()
                latest = bench_financial[bench_financial["date"] == latest_date]
                revenue = find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
                gross_profit = find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
                net_income = find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])
                if revenue and revenue > 0:
                    if gross_profit:
                        bench_metrics["gross_margin"] = round(gross_profit / revenue * 100, 1)
                    if net_income:
                        bench_metrics["net_margin"] = round(net_income / revenue * 100, 1)
            except Exception:
                pass

        if bench_balance is not None and len(bench_balance) > 0:
            try:
                roe_result = calc_roe_ttm(bench_financial, bench_balance)
                if roe_result is not None:
                    bench_metrics["roe"] = roe_result["roe"]
            except Exception:
                pass

        if bench_revenue is not None and len(bench_revenue) > 12:
            try:
                latest_rev = bench_revenue.iloc[-1]["revenue"]
                last_year_rev = bench_revenue.iloc[-13]["revenue"]
                if last_year_rev > 0:
                    bench_metrics["revenue_yoy"] = round((latest_rev - last_year_rev) / last_year_rev * 100, 1)
            except Exception:
                pass

        return {
            "stock_id": benchmark_id,
            "stock_name": bench_name,
            "industry": bench_industry,
            "latest_per_pbr": bench_per_pbr,
            "financial": bench_financial,
            "balance_sheet": bench_balance,
            "extra_metrics": bench_metrics,
        }
    except Exception:
        return None


def _collect_comparison_metrics(data: dict, bench_data: dict) -> dict:
    """收集可比較的指標"""
    metrics = {}
    target_em = data.get("extra_metrics", {})
    bench_em = bench_data.get("extra_metrics", {})
    target_per = data.get("latest_per_pbr", {}) or {}
    bench_per = bench_data.get("latest_per_pbr", {}) or {}

    # 毛利率
    if target_em.get("gross_margin") and bench_em.get("gross_margin"):
        metrics[t("peer.comparison.metric.gross_margin")] = (target_em["gross_margin"], bench_em["gross_margin"])

    # 淨利率
    if target_em.get("net_margin") and bench_em.get("net_margin"):
        metrics[t("peer.comparison.metric.net_margin")] = (target_em["net_margin"], bench_em["net_margin"])

    # ROE
    if target_em.get("roe") and bench_em.get("roe"):
        metrics[t("peer.comparison.metric.roe")] = (target_em["roe"], bench_em["roe"])

    # PER
    if target_per.get("PER") and bench_per.get("PER"):
        metrics[t("peer.comparison.metric.pe")] = (target_per["PER"], bench_per["PER"])

    # 殖利率
    if target_per.get("dividend_yield") and bench_per.get("dividend_yield"):
        metrics[t("peer.comparison.metric.dividend_yield_pct")] = (target_per["dividend_yield"], bench_per["dividend_yield"])

    # PBR
    if target_per.get("PBR") and bench_per.get("PBR"):
        metrics[t("peer.comparison.metric.pb")] = (target_per["PBR"], bench_per["PBR"])

    # 營收年增率
    if target_em.get("revenue_yoy") and bench_em.get("revenue_yoy"):
        metrics[t("peer.comparison.metric.revenue_yoy")] = (target_em["revenue_yoy"], bench_em["revenue_yoy"])

    # 負債比
    if target_em.get("debt_ratio") and bench_em.get("debt_ratio"):
        metrics[t("peer.comparison.metric.debt_ratio")] = (target_em["debt_ratio"], bench_em["debt_ratio"])

    return metrics


def _prepare_radar_data(data: dict, bench_data: dict) -> dict:
    """準備雷達圖資料（正規化到 0-100）"""
    metrics = _collect_comparison_metrics(data, bench_data)
    if not metrics:
        return {}

    radar = {}
    for name, (target_val, bench_val) in metrics.items():
        # 對於「越低越好」的指標（PER、PBR、負債比），反轉
        reverse = name in [t("peer.comparison.metric.pe"), t("peer.comparison.metric.pb"), t("peer.comparison.metric.debt_ratio")]
        max_val = max(abs(target_val), abs(bench_val), 0.1)
        if reverse:
            target_norm = max(0, 100 - abs(target_val) / max_val * 100)
            bench_norm = max(0, 100 - abs(bench_val) / max_val * 100)
        else:
            target_norm = max(0, abs(target_val) / max_val * 100)
            bench_norm = max(0, abs(bench_val) / max_val * 100)
        radar[name] = [round(target_norm, 1), round(bench_norm, 1)]

    return radar


def _render_metric_analysis(metrics: dict, stock_name: str, benchmark_name: str, industry: str):
    """白話解讀各項指標差異"""
    analysis_parts = []

    gross_margin_key = t("peer.comparison.metric.gross_margin")
    roe_key = t("peer.comparison.metric.roe")
    pe_key = t("peer.comparison.metric.pe")

    if gross_margin_key in metrics:
        target_gm, bench_gm = metrics[gross_margin_key]
        diff = target_gm - bench_gm
        if abs(diff) < 5:
            analysis_parts.append(t("peer.comparison.analysis.gross_margin_similar", diff=abs(diff)))
        elif diff > 0:
            analysis_parts.append(t("peer.comparison.analysis.gross_margin_higher", diff=diff, stock_name=stock_name))
        else:
            analysis_parts.append(t("peer.comparison.analysis.gross_margin_lower", diff=abs(diff)))

    if roe_key in metrics:
        target_roe, bench_roe = metrics[roe_key]
        diff = target_roe - bench_roe
        if abs(diff) < 3:
            analysis_parts.append(t("peer.comparison.analysis.roe_similar", diff=abs(diff)))
        elif diff > 0:
            analysis_parts.append(t("peer.comparison.analysis.roe_higher", diff=diff, stock_name=stock_name))
        else:
            analysis_parts.append(t("peer.comparison.analysis.roe_lower", diff=abs(diff)))

    if pe_key in metrics:
        target_per, bench_per = metrics[pe_key]
        if target_per > bench_per * 1.3:
            analysis_parts.append(t("peer.comparison.analysis.per_higher", target_per=target_per, bench_per=bench_per, stock_name=stock_name))
        elif target_per < bench_per * 0.7:
            analysis_parts.append(t("peer.comparison.analysis.per_lower", target_per=target_per, bench_per=bench_per, stock_name=stock_name))
        else:
            analysis_parts.append(t("peer.comparison.analysis.per_similar"))

    if analysis_parts:
        _info_card(t("peer.comparison.analysis.title"), "\n".join(analysis_parts), "🔍")


def _render_difference_analysis(metrics: dict, stock_name: str, benchmark_name: str, industry: str):
    """差異分析總結"""
    if not metrics:
        st.info(t("peer.comparison.diff_no_data"))
        return

    # 計算領先和落後的指標數
    leading = 0
    trailing = 0
    pe_key = t("peer.comparison.metric.pe")
    pb_key = t("peer.comparison.metric.pb")
    debt_key = t("peer.comparison.metric.debt_ratio")
    for name, (target_val, bench_val) in metrics.items():
        reverse = name in [pe_key, pb_key, debt_key]
        if reverse:
            if target_val < bench_val:
                leading += 1
            else:
                trailing += 1
        else:
            if target_val > bench_val:
                leading += 1
            else:
                trailing += 1

    total = leading + trailing
    if total == 0:
        st.info(t("peer.comparison.cannot_compare"))
        return

    st.markdown(t("peer.comparison.summary_header", stock_name=stock_name, total=total))
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(t("peer.comparison.leading_count", leading=leading))
    with col2:
        st.markdown(t("peer.comparison.trailing_count", trailing=trailing))

    # 總結
    if leading > trailing:
        _info_card(t("peer.comparison.summary_title"),
                   t("peer.comparison.summary_leading", stock_name=stock_name, benchmark_name=benchmark_name, industry=industry),
                   "🏆")
    elif leading == trailing:
        _info_card(t("peer.comparison.summary_title"),
                   t("peer.comparison.summary_tied", stock_name=stock_name, benchmark_name=benchmark_name),
                   "⚖️")
    else:
        _info_card(t("peer.comparison.summary_title"),
                   t("peer.comparison.summary_trailing", stock_name=stock_name, benchmark_name=benchmark_name),
                   "📊")
