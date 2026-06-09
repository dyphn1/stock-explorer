"""
同業比較頁 — M2 第三頁
目標：跟產業第一名差在哪？
"""

import streamlit as st
import pandas as pd
from src.data.finmind_client import FinMindClient
from src.services.chart import create_comparison_radar
from src.services.analogy_engine import (
    get_gross_margin_analogy,
    get_roe_analogy,
    get_per_analogy,
)
from src.pages._router_base import _section_title, _info_card, _find_financial_value


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


@st.cache_data(ttl=3600)
def _find_fallback_benchmark(industry: str, stock_id: str):
    """Find the largest company in the same industry as a fallback benchmark."""
    try:
        client = FinMindClient()
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
    st.warning(f"找不到「{industry}」的同業標竿公司，以下僅顯示 {stock_name} 的指標")
    # Show the target company's key metrics in a simple table/card
    metrics = {}
    if data.get("latest_per_pbr") is not None and not data["latest_per_pbr"].empty:
        latest = data["latest_per_pbr"].iloc[-1]
        metrics["本益比"] = latest.get("PE_ratio", "—")
        metrics["股價淨值比"] = latest.get("PB_ratio", "—")
        metrics["殖利率"] = latest.get("dividend_yield", "—")
    if data.get("financial") is not None and not data["financial"].empty:
        latest_fs = data["financial"].iloc[-1]
        # extract whatever fields are available
        for field, label in [("net_profit_margin", "淨利率"), ("ROE", "ROE")]:
            if field in latest_fs:
                metrics[label] = latest_fs[field]

    if metrics:
        for label, value in metrics.items():
            st.metric(label, value)
    else:
        st.info("目前無法取得此公司的指標資料")
    st.caption(f"💡 如需同業比較，請在側邊欄切換到其他具有標竿公司的產業")


def _render_peer_comparison(data: dict, client):
    """同業比較主頁"""
    stock_id = data["stock_id"]
    stock_name = data["stock_name"]
    industry = data["industry"]
    extra_metrics = data["extra_metrics"]
    latest_per_pbr = data["latest_per_pbr"]
    financial = data["financial"]
    balance_sheet = data["balance_sheet"]

    st.markdown(f"## ⚖️ 同業比較 — {stock_name}")
    st.markdown(f"*跟產業第一名差在哪？*")
    st.markdown("---")

    # 決定標竿公司
    benchmark_id, benchmark_name = INDUSTRY_BENCHMARKS.get(industry, (None, None))
    is_fallback = False

    if benchmark_id is None:
        with st.spinner("正在尋找同業標竿..."):
            fallback = _find_fallback_benchmark(industry, stock_id)
        if fallback:
            benchmark_id, benchmark_name = fallback
            is_fallback = True
        else:
            _render_single_company_view(data, stock_name, industry)
            return

    if is_fallback:
        st.info("此產業無預設標竿，已自動選取同業最大公司作為基準")

    # 避免自己跟自己比
    if benchmark_id == stock_id:
        st.info(f"💡 {stock_name} 就是 {industry} 的產業標竿！")
        _info_card("標竿地位", f"{stock_name} 是 {industry} 的領導者，可以跟其他產業的標竿比較看看。", "🏆")
        return

    st.markdown(f"**產業：{industry}**　｜　**標竿：{benchmark_name}（{benchmark_id}）**")

    # 載入標竿公司資料
    with st.spinner(f"正在載入標竿公司 {benchmark_name} 的資料..."):
        bench_data = _get_benchmark_data(client, benchmark_id)

    if bench_data is None:
        st.error(f"無法載入標竿公司 {benchmark_name} 的資料，以下僅顯示 {stock_name} 的指標")
        _render_single_company_view(data, stock_name, industry)
        return

    st.markdown("---")

    # ── 1. 並排比較表 ────────────────────────────────
    _section_title("並排比較：數字差多少？")

    # 收集比較指標
    metrics = _collect_comparison_metrics(data, bench_data)

    if metrics:
        # 建立比較表格
        comparison_rows = []
        for metric_name, (target_val, bench_val) in metrics.items():
            diff = target_val - bench_val
            diff_pct = (diff / bench_val * 100) if bench_val != 0 else 0
            comparison_rows.append({
                "指標": metric_name,
                f"{stock_name}": f"{target_val:.1f}",
                f"{benchmark_name}": f"{bench_val:.1f}",
                "差距": f"{diff:+.1f} ({diff_pct:+.0f}%)",
            })

        comp_df = pd.DataFrame(comparison_rows)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        # 白話解讀
        _render_metric_analysis(metrics, stock_name, benchmark_name, industry)
    else:
        st.info("目前沒有足夠的比較資料")

    st.markdown("---")

    # ── 2. 雷達圖 ────────────────────────────────────
    _section_title("雷達圖：多維度比較")

    radar_metrics = _prepare_radar_data(data, bench_data)
    if radar_metrics:
        fig = create_comparison_radar(radar_metrics, stock_name, benchmark_name)
        st.plotly_chart(fig, use_container_width=True)
        _info_card("雷達圖解讀",
                   f"藍色區域是 {stock_name}，紅色區域是 {benchmark_name}（標竿）。"
                   "面積越大代表該指標表現越好。如果藍色完全被紅色覆蓋，代表標竿公司在所有面向都領先。",
                   "🎯")
    else:
        st.info("目前沒有足夠的雷達圖資料")

    st.markdown("---")

    # ── 3. 差異分析 ──────────────────────────────────
    _section_title("差異分析：為什麼差這麼多？")

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
                revenue = _find_financial_value(latest, ["營業收入", "收入", "Revenue", "revenue"])
                gross_profit = _find_financial_value(latest, ["營業毛利", "毛利", "Gross Profit", "gross_profit"])
                net_income = _find_financial_value(latest, ["淨利", "本期淨利", "Net Income", "net_income"])
                if revenue and revenue > 0:
                    if gross_profit:
                        bench_metrics["gross_margin"] = round(gross_profit / revenue * 100, 1)
                    if net_income:
                        bench_metrics["net_margin"] = round(net_income / revenue * 100, 1)
            except Exception:
                pass

        if bench_balance is not None and len(bench_balance) > 0:
            try:
                latest_date = bench_balance["date"].max()
                latest = bench_balance[bench_balance["date"] == latest_date]
                total_assets = _find_financial_value(latest, ["資產總計", "總資產", "Total Assets", "total_assets"])
                total_equity = _find_financial_value(latest, ["權益總計", "股東權益", "Total Equity", "total_equity"])
                net_income = 0
                if bench_financial is not None and len(bench_financial) > 0:
                    fi_latest = bench_financial[bench_financial["date"] == bench_financial["date"].max()]
                    net_income = _find_financial_value(fi_latest, ["淨利", "本期淨利", "Net Income", "net_income"])
                if net_income and total_equity and total_equity > 0:
                    bench_metrics["roe"] = round(net_income * 4 / total_equity * 100, 1)
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
        metrics["毛利率 (%)"] = (target_em["gross_margin"], bench_em["gross_margin"])

    # 淨利率
    if target_em.get("net_margin") and bench_em.get("net_margin"):
        metrics["淨利率 (%)"] = (target_em["net_margin"], bench_em["net_margin"])

    # ROE
    if target_em.get("roe") and bench_em.get("roe"):
        metrics["ROE (%)"] = (target_em["roe"], bench_em["roe"])

    # PER
    if target_per.get("PER") and bench_per.get("PER"):
        metrics["本益比"] = (target_per["PER"], bench_per["PER"])

    # 殖利率
    if target_per.get("dividend_yield") and bench_per.get("dividend_yield"):
        metrics["殖利率 (%)"] = (target_per["dividend_yield"], bench_per["dividend_yield"])

    # PBR
    if target_per.get("PBR") and bench_per.get("PBR"):
        metrics["淨值比"] = (target_per["PBR"], bench_per["PBR"])

    # 營收年增率
    if target_em.get("revenue_yoy") and bench_em.get("revenue_yoy"):
        metrics["營收年增率 (%)"] = (target_em["revenue_yoy"], bench_em["revenue_yoy"])

    # 負債比
    if target_em.get("debt_ratio") and bench_em.get("debt_ratio"):
        metrics["負債比 (%)"] = (target_em["debt_ratio"], bench_em["debt_ratio"])

    return metrics


def _prepare_radar_data(data: dict, bench_data: dict) -> dict:
    """準備雷達圖資料（正規化到 0-100）"""
    metrics = _collect_comparison_metrics(data, bench_data)
    if not metrics:
        return {}

    radar = {}
    for name, (target_val, bench_val) in metrics.items():
        # 對於「越低越好」的指標（PER、PBR、負債比），反轉
        reverse = name in ["本益比", "淨值比", "負債比 (%)"]
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

    if "毛利率 (%)" in metrics:
        target_gm, bench_gm = metrics["毛利率 (%)"]
        diff = target_gm - bench_gm
        if abs(diff) < 5:
            analysis_parts.append(f"• 毛利率跟標竿差不多（差距 {abs(diff):.1f}%），代表兩家公司的產品利潤空間接近。")
        elif diff > 0:
            analysis_parts.append(f"• 毛利率比標竿高 {diff:.1f}%，代表 {stock_name} 的產品或服務利潤空間更大。")
        else:
            analysis_parts.append(f"• 毛利率比標竿低 {abs(diff):.1f}%，可能是產品定位不同或成本控制較弱。")

    if "ROE (%)" in metrics:
        target_roe, bench_roe = metrics["ROE (%)"]
        diff = target_roe - bench_roe
        if abs(diff) < 3:
            analysis_parts.append(f"• ROE 跟標竿接近（差距 {abs(diff):.1f}%），股東報酬率相當。")
        elif diff > 0:
            analysis_parts.append(f"• ROE 比標竿高 {diff:.1f}%，代表 {stock_name} 幫股東賺錢的效率更好。")
        else:
            analysis_parts.append(f"• ROE 比標竿低 {abs(diff):.1f}%，可能是資本運用效率較差。")

    if "本益比" in metrics:
        target_per, bench_per = metrics["本益比"]
        if target_per > bench_per * 1.3:
            analysis_parts.append(f"• 本益比（{target_per:.1f}）明顯高於標竿（{bench_per:.1f}），市場對 {stock_name} 的成長預期較高。")
        elif target_per < bench_per * 0.7:
            analysis_parts.append(f"• 本益比（{target_per:.1f}）低於標竿（{bench_per:.1f}），市場對 {stock_name} 的評價較保守。")
        else:
            analysis_parts.append(f"• 本益比跟標竿接近，市場評價相當。")

    if analysis_parts:
        _info_card("指標差異解讀", "\n".join(analysis_parts), "🔍")


def _render_difference_analysis(metrics: dict, stock_name: str, benchmark_name: str, industry: str):
    """差異分析總結"""
    if not metrics:
        st.info("目前沒有足夠資料進行差異分析")
        return

    # 計算領先和落後的指標數
    leading = 0
    trailing = 0
    for name, (target_val, bench_val) in metrics.items():
        reverse = name in ["本益比", "淨值比", "負債比 (%)"]
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
        st.info("無法進行比較")
        return

    st.markdown(f"**{stock_name} 在 {total} 項指標中：**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"✅ **領先 {leading} 項**")
    with col2:
        st.markdown(f"⚠️ **落後 {trailing} 項**")

    # 總結
    if leading > trailing:
        _info_card("總結",
                   f"{stock_name} 在多數指標上領先 {benchmark_name}。"
                   f"這代表 {stock_name} 在 {industry} 中表現優異。"
                   f"不過，單一指標不代表全部，建議搭配其他面向一起看。",
                   "🏆")
    elif leading == trailing:
        _info_card("總結",
                   f"{stock_name} 和 {benchmark_name} 各有勝負，實力相當。"
                   f"可以關注兩家公司在不同面向的差異。",
                   "⚖️")
    else:
        _info_card("總結",
                   f"{stock_name} 在多數指標上落後 {benchmark_name}。"
                   f"這不代表 {stock_name} 不好，而是標竿公司在這些面向表現更強。"
                   f"可以關注 {stock_name} 是否有其他獨特優勢。",
                   "📊")
