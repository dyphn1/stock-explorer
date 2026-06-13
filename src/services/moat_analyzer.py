"""
Moat Analysis Service (C46 + C124)
Evaluates competitive advantage using 5-dimension scoring + moat type classification.
"""
from pathlib import Path
import yaml

_MODULE_DIR = Path(__file__).resolve().parent
_DATA_FILE = _MODULE_DIR.parent / "data" / "moat_data.yaml"

_cache: dict | None = None


def _load_data() -> dict:
    global _cache
    if _cache is None:
        if not _DATA_FILE.exists():
            raw: dict = {}
        else:
            with open(_DATA_FILE, "r", encoding="utf-8") as f:
                raw = yaml.safe_load(f) or {}
        _cache = raw
    return _cache


def load_moat_data(stock_id: str) -> dict | None:
    """Load moat data for a stock from YAML."""
    data = _load_data()
    entry = data.get(stock_id)
    if entry is None:
        return None
    return dict(entry)


def get_moat_summary(
    stock_id: str,
    extra_metrics: dict,
    latest_per_pbr: dict | None,
    financial_df,
    monthly_revenue,
) -> dict:
    """
    Return moat summary for a stock.

    Returns dict with:
        - moat_type: str (護城河類型)
        - moat_score: float (0-100)
        - dimensions: dict of 5 dimension scores
        - evidence: list of evidence strings
        - moat_type_description: str
        - has_data: bool
    """
    yaml_data = load_moat_data(stock_id)
    if yaml_data:
        # Use curated YAML data
        dimensions = yaml_data.get("dimensions", {})
        return {
            "moat_type": yaml_data.get("moat_type", "無明顯護城河"),
            "moat_score": yaml_data.get("moat_score", 0),
            "dimensions": {
                "品牌力": dimensions.get("品牌力", 0),
                "成本優勢": dimensions.get("成本優勢", 0),
                "網路效應": dimensions.get("網路效應", 0),
                "轉換成本": dimensions.get("轉換成本", 0),
                "規模經濟": dimensions.get("規模經濟", 0),
            },
            "evidence": yaml_data.get("evidence", []),
            "moat_type_description": yaml_data.get("moat_type_description", ""),
            "has_data": True,
        }

    # Template scoring for non-curated stocks
    dimensions = compute_moat_dimensions(extra_metrics, latest_per_pbr, financial_df, monthly_revenue)
    moat_type, moat_type_desc = _classify_moat_type(dimensions)
    avg_score = sum(dimensions.values()) / len(dimensions) if dimensions else 0

    return {
        "moat_type": moat_type,
        "moat_score": round(avg_score, 1),
        "dimensions": dimensions,
        "evidence": [f"系統自動評分：{moat_type}"],
        "moat_type_description": moat_type_desc,
        "has_data": avg_score > 0,
    }


def compute_moat_dimensions(
    extra_metrics: dict,
    latest_per_pbr: dict | None,
    financial_df,
    monthly_revenue,
) -> dict:
    """
    Compute 5 moat dimensions from available financial data.

    Returns dict with keys: 品牌力, 成本優勢, 網路效應, 轉換成本, 規模經濟
    Each scored 0-100.
    """
    # 品牌力 (Brand): gross margin stability + level
    gross_margin = extra_metrics.get("gross_margin")
    if gross_margin is not None:
        brand_score = min(100, max(0, gross_margin * 1.5))  # 67% gm -> 100
    else:
        brand_score = 30

    # 成本優勢 (Cost): gross margin + operating efficiency proxy
    if gross_margin is not None:
        cost_score = min(100, max(0, gross_margin * 1.3))
    else:
        cost_score = 25

    # 網路效應 (Network): revenue growth consistency
    revenue_yoy = extra_metrics.get("revenue_yoy")
    if revenue_yoy is not None:
        network_score = min(100, max(0, 50 + revenue_yoy * 1.5))
    else:
        network_score = 35

    # 轉換成本 (Switching): revenue stability (low CV = high switching cost)
    switching_score = 50
    if monthly_revenue is not None and len(monthly_revenue) >= 12:
        try:
            recent_12 = monthly_revenue.tail(12)["revenue"]
            mean_val = recent_12.mean()
            if mean_val > 0:
                cv = recent_12.std() / mean_val
                switching_score = min(100, max(0, 100 - cv * 200))
        except Exception:
            pass

    # 規模經濟 (Scale): revenue scale + market position proxy
    roe = extra_metrics.get("roe")
    if roe is not None and gross_margin is not None:
        scale_score = min(100, max(0, (roe + gross_margin) / 2))
    else:
        scale_score = 40

    return {
        "品牌力": round(brand_score, 1),
        "成本優勢": round(cost_score, 1),
        "網路效應": round(network_score, 1),
        "轉換成本": round(switching_score, 1),
        "規模經濟": round(scale_score, 1),
    }


def _classify_moat_type(dimensions: dict) -> tuple:
    """Classify moat type based on highest-scoring dimension."""
    if not dimensions:
        return "無明顯護城河", "目前各項護城河指標分數均偏低，尚未形成明顯競爭優勢"

    max_dim = max(dimensions, key=lambda k: dimensions[k])
    max_score = dimensions[max_dim]

    descriptions = {
        "品牌力": ("品牌護城河", "公司擁有強勁的品牌定價能力，客戶願意為品牌支付溢價"),
        "成本優勢": ("成本護城河", "公司在生產或營運成本上具有結構性優勢，競爭對手難以複製"),
        "網路效應": ("網路效應護城河", "平台或產品的價值隨用戶增長而提升，形成正向循環"),
        "轉換成本": ("轉換成本護城河", "客戶轉換至高競爭對手的成本高，形成自然鎖定"),
        "規模經濟": ("規模經濟護城河", "公司因規模龐大而享有單位成本優勢，新進入者難以競爭"),
    }

    if max_score < 40:
        return "無明顯護城河", "目前各項護城河指標分數均偏低，尚未形成明顯競爭優勢"

    return descriptions.get(max_dim, ("無明顯護城河", ""))
