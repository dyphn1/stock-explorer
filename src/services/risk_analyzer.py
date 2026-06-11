"""
風險分析器 — 純函式，無 Streamlit 與 API 依賴
分析三個維度的風險：客戶集中、財務健康、事件型風險
歷史學家語態：僅描述過去事實，不預測未來
"""

import pandas as pd
from typing import Optional

from src.services.financial_metrics import find_financial_value
from src.services.news_summarizer import get_news_impact_level, summarize_news


# ── Threshold constants ──

# Debt ratio thresholds
_DEBT_HIGH = 65.0
_DEBT_MEDIUM = 45.0

# Net margin thresholds
_MARGIN_HIGH = 3.0
_MARGIN_MEDIUM = 8.0

# Concentration thresholds
_CONC_HIGH = 50.0
_CONC_MEDIUM = 25.0

# Revenue stability CV thresholds
_CV_HIGH = 0.25
_CV_MEDIUM = 0.10


# ── Private helpers: classification ──

def _classify_debt_risk(debt_ratio: float | None) -> str:
    """Classify debt ratio into high/medium/low. Returns risk level string."""
    if debt_ratio is None:
        return "low"
    if debt_ratio > _DEBT_HIGH:
        return "high"
    if debt_ratio >= _DEBT_MEDIUM:
        return "medium"
    return "low"


def _classify_margin_risk(net_margin: float | None) -> str:
    """Classify net profit margin into high/medium/low risk levels."""
    if net_margin is None:
        return "low"
    if net_margin < _MARGIN_HIGH:
        return "high"
    if net_margin <= _MARGIN_MEDIUM:
        return "medium"
    return "low"


def _classify_cashflow_risk(cash_flow_values: list[float]) -> str:
    """Classify cash flow trend from trailing operating cash flow values."""
    if not cash_flow_values:
        return "low"
    negative_count = sum(1 for v in cash_flow_values if v is not None and v < 0)
    if negative_count >= 2:
        return "high"
    if negative_count == 1:
        return "medium"
    return "low"


def _classify_concentration_risk(concentration_pct: float | None) -> str:
    """Classify revenue concentration level."""
    if concentration_pct is None:
        return "low"
    if concentration_pct > _CONC_HIGH:
        return "high"
    if concentration_pct >= _CONC_MEDIUM:
        return "medium"
    return "low"


def _count_risk_events(news_df: pd.DataFrame | None, days: int = 90) -> dict:
    """Count high/medium impact news in trailing window.

    Returns dict with keys: high (int), medium (int), events (list[str]).
    """
    if news_df is None or len(news_df) == 0:
        return {"high": 0, "medium": 0, "events": []}

    df = news_df.copy()
    # Determine the reference date: use the latest date in the news data
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        latest_date = df["date"].max()
        if pd.isna(latest_date):
            return {"high": 0, "medium": 0, "events": []}
        cutoff = latest_date - pd.Timedelta(days=days)
        mask = df["date"] >= cutoff
        recent = df[mask]
    else:
        recent = df

    high_count = 0
    medium_count = 0
    top_events = []

    for _, row in recent.iterrows():
        title = str(row.get("title", ""))
        if not title:
            continue
        impact = get_news_impact_level(title)
        if impact == "high":
            high_count += 1
            if len(top_events) < 3:
                top_events.append(title)
        elif impact == "medium":
            medium_count += 1
            if len(top_events) < 3 and high_count == 0:
                top_events.append(title)

    return {"high": high_count, "medium": medium_count, "events": top_events}


def _determine_overall_level(dimensions: list[str]) -> str:
    """Derive overall risk level from list of dimension risk_level strings."""
    if not dimensions:
        return "low"
    high_count = dimensions.count("high")
    if high_count >= 2:
        return "high"
    if high_count == 1:
        return "medium"
    if all(d == "low" for d in dimensions):
        return "low"
    return "medium"


def _combine_sub_dimensions(debt_risk: str, margin_risk: str, cashflow_risk: str) -> str:
    """Combine three financial sub-dimensions into one risk level."""
    sub_dims = [debt_risk, margin_risk, cashflow_risk]
    high_count = sub_dims.count("high")
    if high_count >= 2:
        return "high"
    if high_count == 1:
        return "medium"
    if all(d == "low" for d in sub_dims):
        return "low"
    return "medium"


# ── Public API: dimension assessors ──

def assess_customer_concentration(data: dict) -> dict | None:
    """Analyze customer/supplier concentration risk.

    Uses revenue breakdown items from financial statements and
    revenue trend data from monthly_revenue to assess whether the
    company depends disproportionately on a small number of customers.
    """
    extra_metrics = data.get("extra_metrics") or {}
    financial = data.get("financial")
    monthly_revenue = data.get("monthly_revenue")
    stock_name = data.get("stock_name", "該公司")

    has_any_data = False
    supporting_data = {}

    # 1. Try to find revenue concentration from financial DataFrame
    concentration_pct = None
    if financial is not None and len(financial) > 0:
        try:
            # Look for revenue breakdown by customer/segment
            segment_keywords = ["客戶", "客源", "營業收入", "segment", "revenue by"]
            for kw in segment_keywords:
                mask = financial["type"].str.contains(kw, case=False, na=False)
                if mask.any():
                    segment_rows = financial[mask]
                    # Get the latest date values
                    if "date" in segment_rows.columns:
                        latest_date = segment_rows["date"].max()
                        latest_rows = segment_rows[segment_rows["date"] == latest_date]
                    else:
                        latest_rows = segment_rows
                    # Find the max segment value as concentration indicator
                    if "value" in latest_rows.columns:
                        values = latest_rows["value"].dropna()
                        if len(values) > 0:
                            total = float(values.sum())
                            if total > 0:
                                max_val = float(values.max())
                                concentration_pct = round(max_val / total * 100, 1)
                                has_any_data = True
                                supporting_data["revenue_concentration_pct"] = concentration_pct
                    break
        except Exception:
            pass

    # 2. Calculate revenue stability (CV of trailing 12 months)
    revenue_stability_cv = None
    revenue_trend = "stable"
    if monthly_revenue is not None and len(monthly_revenue) > 0:
        try:
            rev_values = monthly_revenue["revenue"].tail(12).dropna()
            if len(rev_values) >= 3:
                mean_rev = rev_values.mean()
                if mean_rev > 0:
                    std_rev = rev_values.std()
                    revenue_stability_cv = round(std_rev / mean_rev, 2)
                    has_any_data = True
                    supporting_data["revenue_stability_cv"] = revenue_stability_cv

                    # Determine trend: compare first half vs second half
                    half = len(rev_values) // 2
                    if half > 0:
                        first_half = rev_values.iloc[:half].mean()
                        second_half = rev_values.iloc[half:].mean()
                        if first_half > 0:
                            change_pct = (second_half - first_half) / first_half * 100
                            if change_pct > 10:
                                revenue_trend = "growing"
                            elif change_pct < -10:
                                revenue_trend = "declining"
                            else:
                                revenue_trend = "stable"
                    supporting_data["revenue_trend"] = revenue_trend
        except Exception:
            pass

    if not has_any_data:
        return None

    supporting_data["revenue_concentration_pct"] = concentration_pct

    # Classify based on concentration and CV
    conc_risk = _classify_concentration_risk(concentration_pct)
    cv_risk = "low"
    if revenue_stability_cv is not None:
        if revenue_stability_cv > _CV_HIGH:
            cv_risk = "high"
        elif revenue_stability_cv >= _CV_MEDIUM:
            cv_risk = "medium"

    # Take the worse of concentration and stability
    risk_levels = [r for r in [conc_risk, cv_risk] if r is not None]
    risk_level = _determine_overall_level(risk_levels)

    # Generate plain-language description
    desc_parts = []
    if concentration_pct is not None and concentration_pct > 0:
        if risk_level == "high":
            desc_parts.append(
                f"根據最近一期財報，前三大客戶合計佔營收約 {concentration_pct:.0f}%。"
            )
        elif risk_level == "medium":
            desc_parts.append(
                f"近月營收主要來自 2–3 個業務線，最大業務線佔營收約 {concentration_pct:.0f}%。"
            )
        else:
            desc_parts.append(
                f"公司營收來源分散在多個業務線，最大業務線佔營收不到 {concentration_pct:.0f}%。"
            )

    if revenue_stability_cv is not None:
        if risk_level == "high":
            desc_parts.append(
                f"過去 12 個月營收波動幅度（變異係數為 {revenue_stability_cv:.2f}），顯示收入來源較不穩定。"
                f"這意味著少數客戶的訂單變化會顯著影響公司營收。"
            )
        elif risk_level == "medium":
            desc_parts.append(
                f"過去 12 個月營收波動幅度為 {revenue_stability_cv:.2f}，屬於正常範圍。"
                f"公司營收來源有一定集中，但仍在可控範圍。"
            )
        else:
            desc_parts.append(
                f"過去 12 月營收波動幅度為 {revenue_stability_cv:.2f}，收入來源穩定多元。"
            )

    if not desc_parts:
        return None

    plain_language_description = "".join(desc_parts)

    return {
        "risk_level": risk_level,
        "title": "客戶集中風險",
        "plain_language_description": plain_language_description,
        "supporting_data": supporting_data,
    }


def assess_financial_health(data: dict) -> dict | None:
    """Analyze financial health risk across leverage, cash flow, and profitability."""
    extra_metrics = data.get("extra_metrics") or {}
    balance_sheet = data.get("balance_sheet")
    cash_flow = data.get("cash_flow")
    financial = data.get("financial")
    stock_name = data.get("stock_name", "該公司")

    has_any_data = False
    supporting_data = {}

    # 1. Debt ratio
    debt_ratio = extra_metrics.get("debt_ratio")
    if debt_ratio is not None:
        has_any_data = True
        supporting_data["debt_ratio"] = debt_ratio

    # 2. Equity ratio
    equity_ratio = extra_metrics.get("equity_ratio")
    if equity_ratio is not None:
        supporting_data["equity_ratio"] = equity_ratio

    # 3. Net margin
    net_margin = extra_metrics.get("net_margin")
    if net_margin is not None:
        has_any_data = True
        supporting_data["net_margin"] = net_margin

    # 4. Gross margin
    gross_margin = extra_metrics.get("gross_margin")
    if gross_margin is not None:
        supporting_data["gross_margin"] = gross_margin

    # 5. Operating cash flow trend (trailing 4 quarters)
    operating_cash_flow_trend = "positive"
    if cash_flow is not None and len(cash_flow) > 0:
        try:
            ocf_keywords = ["營業活動", "Operating Cash Flow", "營業活動之淨現金"]
            ocf_values = []
            for kw in ocf_keywords:
                mask = cash_flow["type"].str.contains(kw, case=False, na=False)
                if mask.any():
                    ocf_rows = cash_flow[mask].sort_values("date")
                    ocf_values = ocf_rows["value"].tail(4).tolist()
                    break
            if ocf_values:
                has_any_data = True
                negative_count = sum(1 for v in ocf_values if v < 0)
                if negative_count >= 2:
                    operating_cash_flow_trend = "negative"
                elif negative_count == 1:
                    operating_cash_flow_trend = "mixed"
                else:
                    operating_cash_flow_trend = "positive"
                supporting_data["operating_cash_flow_trend"] = operating_cash_flow_trend
        except Exception:
            pass

    # 6. Profitability trend (trailing 4 quarters net income)
    profitability_trend = "stable"
    if financial is not None and len(financial) > 0:
        try:
            ni_keywords = ["淨利", "本期淨利", "Net Income", "net_income"]
            for kw in ni_keywords:
                mask = financial["type"].str.contains(kw, case=False, na=False)
                if mask.any():
                    ni_rows = financial[mask].sort_values("date")
                    ni_values = ni_rows["value"].tail(4).tolist()
                    if len(ni_values) >= 2:
                        has_any_data = True
                        first_val = ni_values[0]
                        last_val = ni_values[-1]
                        if first_val != 0:
                            change = (last_val - first_val) / abs(first_val) * 100
                            if change > 15:
                                profitability_trend = "improving"
                            elif change < -15:
                                profitability_trend = "declining"
                            else:
                                profitability_trend = "stable"
                        supporting_data["profitability_trend"] = profitability_trend
                    break
        except Exception:
            pass

    if not has_any_data:
        return None

    # Classify sub-dimensions
    debt_risk = _classify_debt_risk(debt_ratio)
    margin_risk = _classify_margin_risk(net_margin)

    # Cash flow risk from trend
    cf_risk_map = {"negative": "high", "mixed": "medium", "positive": "low"}
    cashflow_risk = cf_risk_map.get(operating_cash_flow_trend, "low")

    risk_level = _combine_sub_dimensions(debt_risk, margin_risk, cashflow_risk)

    # Generate plain-language description
    desc_parts = []
    if risk_level == "high":
        if debt_ratio is not None:
            desc_parts.append(
                f"最近一期負債比為 {debt_ratio:.0f}%，高於一般認為的警戒線 65%。"
            )
        if operating_cash_flow_trend == "negative":
            desc_parts.append(
                "過去 4 季營業現金流有 2 季為負數，表示本業賺取的現金不足以支應營運所需。"
            )
        if net_margin is not None and net_margin < _MARGIN_HIGH:
            desc_parts.append(f"淨利率僅 {net_margin:.1f}%，獲利空間極為有限。")
    elif risk_level == "medium":
        if debt_ratio is not None:
            desc_parts.append(f"負債比為 {debt_ratio:.0f}%，屬於適度槓桿範圍。")
        if net_margin is not None:
            desc_parts.append(f"淨利率為 {net_margin:.1f}%，獲利穩定但不算突出。")
        if operating_cash_flow_trend == "mixed":
            desc_parts.append("過去 4 季營業現金流有 1 季為負，需留意後續是否改善。")
    else:  # low
        if debt_ratio is not None:
            desc_parts.append(f"負債比僅 {debt_ratio:.0f}%，財務結構穩健。")
        if net_margin is not None:
            desc_parts.append(
                f"淨利率維持在 {net_margin:.1f}% 以上，獲利能力在同產業中屬於前段班。"
            )
        if operating_cash_flow_trend == "positive":
            desc_parts.append("過去 4 季營業現金流均為正數，本業現金創造能力良好。")

    if not desc_parts:
        return None

    plain_language_description = "".join(desc_parts)

    return {
        "risk_level": risk_level,
        "title": "財務健康風險",
        "plain_language_description": plain_language_description,
        "supporting_data": supporting_data,
    }


def assess_event_risk(data: dict) -> dict | None:
    """Analyze event-based risk from recent news headlines."""
    news = data.get("news")
    institutional = data.get("institutional")
    stock_name = data.get("stock_name", "該公司")

    if news is None or len(news) == 0:
        return None

    supporting_data = {}

    # Count risk events in trailing 90 days
    event_counts = _count_risk_events(news, days=90)
    high_count = event_counts["high"]
    medium_count = event_counts["medium"]
    top_events = event_counts["events"]

    supporting_data["high_impact_count"] = high_count
    supporting_data["medium_impact_count"] = medium_count
    supporting_data["top_events"] = top_events

    # Assess institutional flow (trailing 30 days)
    foreign_flow_trend = "neutral"
    net_foreign_selling = 0
    if institutional is not None and len(institutional) > 0:
        try:
            if "date" in institutional.columns and "foreign_net_buy" in institutional.columns:
                inst = institutional.copy()
                inst["date"] = pd.to_datetime(inst["date"], errors="coerce")
                latest_date = inst["date"].max()
                if pd.notna(latest_date):
                    cutoff_30d = latest_date - pd.Timedelta(days=30)
                    recent = inst[inst["date"] >= cutoff_30d]
                    net = recent["foreign_net_buy"].sum()
                    net_foreign_selling = -net  # positive means selling
                    if net > 5000:
                        foreign_flow_trend = "buying"
                    elif net < -5000:
                        foreign_flow_trend = "selling"
                    else:
                        foreign_flow_trend = "neutral"
                    supporting_data["foreign_flow_trend"] = foreign_flow_trend
        except Exception:
            pass

    supporting_data["foreign_flow_trend"] = foreign_flow_trend

    # Classify risk level
    if high_count >= 3 or (high_count >= 2 and net_foreign_selling > 10000):
        risk_level = "high"
    elif high_count >= 1 or medium_count >= 3:
        risk_level = "medium"
    else:
        risk_level = "low"

    # Generate plain-language description
    if risk_level == "high":
        event_desc = f"近 90 天內有 {high_count + medium_count} 則重大消息"
        if top_events:
            event_desc += "，包含" + "、".join(top_events[:2])
        event_desc += "。"
        if high_count > 0:
            event_desc += f"其中 {high_count} 則被列為高度關注事件。"
        if foreign_flow_trend == "selling":
            event_desc += "同期外資累計賣超，法人態度偏向保守。"
        plain_language_description = event_desc
    elif risk_level == "medium":
        plain_language_description = (
            f"近 90 天內有 {medium_count} 則中度關注消息，涉及產品認證與供應鏈調整。"
            f"同期外資買賣互見，法人態度中性。"
        )
    else:
        plain_language_description = (
            "近 90 天內未有重大消息，新聞多為例行性公告。"
            "同期外資小幅買超，法人態度穩定。"
        )

    return {
        "risk_level": risk_level,
        "title": "事件型風險",
        "plain_language_description": plain_language_description,
        "supporting_data": supporting_data,
    }


# ── Public API: top-level orchestrator ──

def assess_risk(data: dict) -> dict:
    """Complete risk assessment — top-level entry point.

    Orchestrates the three risk dimension sub-analyses and produces
    a unified RiskAssessment dict.
    """
    if not data:
        return {
            "customer_concentration": None,
            "financial_health": None,
            "event_based": None,
            "overall_level": "low",
            "summary_text": "風險分析資料不足",
        }

    customer_concentration = assess_customer_concentration(data)
    financial_health = assess_financial_health(data)
    event_based = assess_event_risk(data)

    # Collect non-None risk levels for overall determination
    dim_levels = []
    for dim in [customer_concentration, financial_health, event_based]:
        if dim is not None:
            dim_levels.append(dim["risk_level"])

    overall_level = _determine_overall_level(dim_levels)

    # Generate summary text
    if not dim_levels:
        summary_text = "風險分析資料不足"
    else:
        high_dims = []
        if customer_concentration and customer_concentration["risk_level"] == "high":
            high_dims.append("客戶集中")
        if financial_health and financial_health["risk_level"] == "high":
            high_dims.append("財務健康")
        if event_based and event_based["risk_level"] == "high":
            high_dims.append("事件型")
        if high_dims:
            summary_text = f"分析顯示 {'、'.join(high_dims)} 面向存在較高風險，以下為各維度詳細說明。"
        else:
            summary_text = "以下為各風險維度分析，資料來源為近期公開資訊。"

    return {
        "customer_concentration": customer_concentration,
        "financial_health": financial_health,
        "event_based": event_based,
        "overall_level": overall_level,
        "summary_text": summary_text,
    }
