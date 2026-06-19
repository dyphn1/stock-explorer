"""
Compare Stories (同業比較故事) 模組
生成公司與同業的敘事式比較（C38 Phase 1）

使用比喻引擎（analogy_engine）和重點摘要（key_takeaways）產生白話比較文本。
不使用 LLM，完全基於結構化數據與模板。
"""

from __future__ import annotations

from typing import Optional

import pandas as pd

from src.core.i18n import t
from src.services.analogy_engine import (
    get_one_liner,
    get_per_analogy,
    get_dividend_analogy,
    get_gross_margin_analogy,
    get_revenue_analogy,
    get_yoy_analogy,
    get_roe_analogy,
    get_pbr_analogy,
)
from src.services.key_takeaways import generate_key_takeaways


# ── Peer lookup ────────────────────────────────────────────

def _find_peers(
    stock_id: str,
    industry: str,
    all_stock_info: pd.DataFrame,
    max_peers: int = 3,
) -> list[dict]:
    """從全量股票資訊中找出同產業的同業（排除自己）。

    Returns:
        list of dict，每個 dict 包含 stock_id, stock_name, industry_category
    """
    if all_stock_info is None or len(all_stock_info) == 0:
        return []
    if not industry or industry == "未知":
        return []

    mask = (
        (all_stock_info["industry_category"] == industry)
        & (all_stock_info["stock_id"] != stock_id)
    )
    peers_df = mask_any(all_stock_info, mask)
    if peers_df is None or len(peers_df) == 0:
        return []

    peers_df = peers_df.sort_values("stock_id").head(max_peers)
    return [
        {
            "stock_id": str(row["stock_id"]),
            "stock_name": row["stock_name"],
            "industry": row.get("industry_category", industry),
        }
        for _, row in peers_df.iterrows()
    ]


def mask_any(df: pd.DataFrame, mask: pd.Series) -> pd.DataFrame:
    """安全地套用 mask，避免型別錯誤。"""
    try:
        result = df[mask]
        if isinstance(result, pd.DataFrame):
            return result.copy()
        return df.iloc[:0]
    except Exception:
        return df.iloc[:0]


# ── Narrative comparison generators ────────────────────────

def _compare_metric_story(
    label: str,
    self_value: Optional[float],
    peer_value: Optional[float],
    fmt: str = "{:.1f}",
    unit: str = "",
    higher_is_better: bool = True,
) -> Optional[str]:
    """比較單一指標，產生一句白話描述。

    Returns:
        比較描述字串，或 None（當兩邊都無資料時）
    """
    if self_value is None and peer_value is None:
        return None

    if self_value is not None and peer_value is not None:
        diff = self_value - peer_value
        abs_diff = abs(diff)
        self_str = fmt.format(self_value)
        peer_str = fmt.format(peer_value)

        if abs_diff < 0.5:
            return t('comparison.metric.close', label=label, self_str=self_str, peer_str=peer_str, unit=unit)

        if diff > 0:
            direction = t('comparison.higher')
            better = t('comparison.advantage') if higher_is_better else t('comparison.valuation_higher')
        else:
            direction = t('comparison.lower')
            better = t('comparison.disadvantage') if higher_is_better else t('comparison.valuation_lower')

        return t('comparison.metric.diff', label=label, self_str=self_str, unit=unit, direction=direction, peer_str=peer_str, better=better)

    # 只有一邊有資料
    if self_value is not None:
        return t('comparison.metric.self_only', label=label, value=fmt.format(self_value), unit=unit)
    return None


def _build_peer_narrative(
    self_data: dict,
    peer_data: dict,
    self_metrics: dict,
    peer_metrics: dict,
    self_per_pbr: dict | None,
    peer_per_pbr: dict | None,
) -> list[str]:
    """建立兩家公司的敘事比較段落。

    Returns:
        比較文本行列表（3-5 句）
    """
    lines: list[str] = []
    stock_name = self_data["stock_name"]
    peer_name = peer_data["stock_name"]

    # 1. 營收規模比較
    self_rev = _latest_revenue_billion(self_metrics)
    peer_rev = _latest_revenue_billion(peer_metrics)
    rev_story = _compare_metric_story(
        "月營收", self_rev, peer_rev, fmt="{:,.0f}", unit=" 億"
    )
    if rev_story:
        if self_rev and peer_rev:
            if self_rev > peer_rev * 1.5:
                lines.append(
                    t('comparison.revenue.larger', stock_name=stock_name, peer_name=peer_name, rev_desc=revs_desc(self_rev, peer_rev))
                )
            elif peer_rev > self_rev * 1.5:
                lines.append(
                    t('comparison.revenue.smaller', stock_name=stock_name, peer_name=peer_name, rev_desc=revs_desc(self_rev, peer_rev))
                )
            else:
                lines.append(t('comparison.revenue.similar', rev_story=rev_story))
        else:
            lines.append(f"📏 {rev_story}")

    # 2. 毛利率比較
    self_gm = self_metrics.get("gross_margin")
    peer_gm = peer_metrics.get("gross_margin")
    if self_gm is not None and peer_gm is not None:
        if self_gm > peer_gm + 5:
            lines.append(
                t('comparison.gross_margin.higher', stock_name=stock_name, self_gm=self_gm, peer_name=peer_name, peer_gm=peer_gm, analogy=get_gross_margin_analogy(self_gm))
            )
        elif peer_gm > self_gm + 5:
            lines.append(
                t('comparison.gross_margin.lower', stock_name=stock_name, self_gm=self_gm, peer_name=peer_name, peer_gm=peer_gm, analogy=get_gross_margin_analogy(self_gm))
            )
        else:
            lines.append(t('comparison.gross_margin.similar', self_gm=self_gm, peer_gm=peer_gm))

    # 3. 獲利能力（ROE）
    self_roe = self_metrics.get("roe")
    peer_roe = peer_metrics.get("roe")
    roe_story = _compare_metric_story(
        "ROE", self_roe, peer_roe, fmt="{:.1f}", unit="%"
    )
    if roe_story:
        lines.append(f"📈 {roe_story}")

    # 4. 估值（PER）
    self_per = self_per_pbr.get("PER") if self_per_pbr else None
    peer_per = peer_per_pbr.get("PER") if peer_per_pbr else None
    if self_per is not None and peer_per is not None and self_per > 0 and peer_per > 0:
        if self_per > peer_per * 1.3:
            lines.append(
                t('comparison.per.higher', stock_name=stock_name, self_per=self_per, peer_name=peer_name, peer_per=peer_per)
            )
        elif peer_per > self_per * 1.3:
            lines.append(
                t('comparison.per.lower', stock_name=stock_name, self_per=self_per, peer_name=peer_name, peer_per=peer_per)
            )
        else:
            lines.append(t('comparison.per.similar', self_per=self_per, peer_per=peer_per))

    # 5. 殖利率
    self_dy = self_per_pbr.get("dividend_yield") if self_per_pbr else None
    peer_dy = peer_per_pbr.get("dividend_yield") if peer_per_pbr else None
    if self_dy is not None and peer_dy is not None:
        if self_dy > peer_dy + 1:
            lines.append(
                t('comparison.dividend_yield.higher', stock_name=stock_name, self_dy=self_dy, peer_name=peer_name, peer_dy=peer_dy)
            )
        elif peer_dy > self_dy + 1:
            lines.append(
                t('comparison.dividend_yield.lower', stock_name=stock_name, self_dy=self_dy, peer_name=peer_name, peer_dy=peer_dy)
            )
        elif self_dy > 0:
            lines.append(t('comparison.dividend_yield.similar', self_dy=self_dy, peer_dy=peer_dy))

    # 確保至少回傳 1 行
    if not lines:
        lines.append(t('comparison.no_difference', stock_name=stock_name, peer_name=peer_name))

    return lines[:5]


def _latest_revenue_billion(metrics: dict) -> Optional[float]:
    """從 extra_metrics 取得最近月營收（億）。"""
    rev = metrics.get("latest_revenue_billion")
    if rev is not None:
        return float(rev)
    return None


def revs_desc(self_rev: float, peer_rev: float) -> str:
    """產生營收規模比較描述。"""
    if peer_rev <= 0:
        return ""
    ratio = self_rev / peer_rev
    if ratio >= 2:
        return t('comparison.revs_ratio.double', ratio=ratio)
    elif ratio >= 1.2:
        return t('comparison.revs_ratio.slightly_larger', ratio=ratio)
    elif ratio >= 0.8:
        return t('comparison.revs_ratio.similar')
    elif ratio >= 0.5:
        return t('comparison.revs_ratio.percent', ratio=ratio)
    else:
        return t('comparison.revs_ratio.only_percent', ratio=ratio)


# ── Public API ─────────────────────────────────────────────

def generate_compare_stories(
    stock_id: str,
    stock_name: str,
    industry: str,
    extra_metrics: dict,
    latest_per_pbr: dict | None,
    monthly_revenue,
    financial_df,
    all_stock_info: pd.DataFrame,
    peer_cache: dict[str, dict] | None = None,
) -> list[dict]:
    """生成同業比較故事（C38 Phase 1）。

    找出 2-3 家同業，為每個同業生成敘事式比較。

    Args:
        stock_id: 當前股票代號
        stock_name: 當前股票名稱
        industry: 產業分類
        extra_metrics: 當前股票的財務指標
        latest_per_pbr: 當前股票的 PER/PBR/殖利率
        monthly_revenue: 當前股票的月營收 DataFrame
        financial_df: 當前股票的財務報表 DataFrame
        all_stock_info: 全量股票資訊（用來找同業）
        peer_cache: 同業資料快取 {stock_id: data_dict}，避免重複載入

    Returns:
        list of dict，每個 dict 包含：
            peer_id, peer_name, narrative_lines (list[str])
    """
    peers = _find_peers(stock_id, industry, all_stock_info, max_peers=3)
    if not peers:
        return []

    # 將當前股票的月營收（億）注入 extra_metrics
    if monthly_revenue is not None and len(monthly_revenue) > 0:
        extra_metrics["latest_revenue_billion"] = (
            float(monthly_revenue.iloc[-1]["revenue"]) / 1e8
        )

    self_data = {"stock_id": stock_id, "stock_name": stock_name}
    results: list[dict] = []

    for peer in peers:
        peer_id = peer["stock_id"]
        peer_name = peer["stock_name"]

        # 嘗試從快取取得同業資料
        if peer_cache and peer_id in peer_cache:
            peer_full = peer_cache[peer_id]
            peer_metrics = peer_full.get("extra_metrics", {})
            peer_per_pbr = peer_full.get("latest_per_pbr")
            peer_revenue = peer_full.get("monthly_revenue")
            peer_financial = peer_full.get("financial")
        else:
            # 沒有快取時，使用精簡版同業資料（只有基本資訊）
            # 在 Phase 1 中，同業的詳細財務資料透過 all_stock_info 取得
            peer_metrics = {}
            peer_per_pbr = None
            peer_revenue = None
            peer_financial = None

        # 將同業月營收注入
        if peer_revenue is not None and len(peer_revenue) > 0:
            peer_metrics["latest_revenue_billion"] = (
                float(peer_revenue.iloc[-1]["revenue"]) / 1e8
            )

        narrative_lines = _build_peer_narrative(
            self_data=self_data,
            peer_data=peer,
            self_metrics=extra_metrics,
            peer_metrics=peer_metrics,
            self_per_pbr=latest_per_pbr,
            peer_per_pbr=peer_per_pbr,
        )

        results.append({
            "peer_id": peer_id,
            "peer_name": peer_name,
            "narrative_lines": narrative_lines,
        })

    return results
