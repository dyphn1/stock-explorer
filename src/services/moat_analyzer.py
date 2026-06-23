"""
Moat Analysis Service (C46 + C124)
Evaluates competitive advantage using 5-dimension scoring + moat type classification.
"""
from pathlib import Path
import yaml

from src.core.i18n import t

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
            "moat_type": yaml_data.get("moat_type", t("moat.type.none")),
            "moat_score": yaml_data.get("moat_score", 0),
            "dimensions": {
                t("moat.dimension.brand"): dimensions.get("品牌力", 0),
                t("moat.dimension.cost"): dimensions.get("成本優勢", 0),
                t("moat.dimension.network"): dimensions.get("網路效應", 0),
                t("moat.dimension.switching"): dimensions.get("轉換成本", 0),
                t("moat.dimension.scale"): dimensions.get("規模經濟", 0),
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
        "evidence": [t("moat.evidence.auto_score", moat_type=moat_type)],
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
        t("moat.dimension.brand"): round(brand_score, 1),
        t("moat.dimension.cost"): round(cost_score, 1),
        t("moat.dimension.network"): round(network_score, 1),
        t("moat.dimension.switching"): round(switching_score, 1),
        t("moat.dimension.scale"): round(scale_score, 1),
    }


def _classify_moat_type(dimensions: dict) -> tuple:
    """Classify moat type based on highest-scoring dimension."""
    if not dimensions:
        return t("moat.type.none"), t("moat.description.none")

    max_dim = max(dimensions, key=lambda k: dimensions[k])
    max_score = dimensions[max_dim]

    descriptions = {
        t("moat.dimension.brand"): (t("moat.type.brand"), t("moat.description.brand")),
        t("moat.dimension.cost"): (t("moat.type.cost"), t("moat.description.cost")),
        t("moat.dimension.network"): (t("moat.type.network"), t("moat.description.network")),
        t("moat.dimension.switching"): (t("moat.type.switching"), t("moat.description.switching")),
        t("moat.dimension.scale"): (t("moat.type.scale"), t("moat.description.scale")),
    }

    if max_score < 40:
        return t("moat.type.none"), t("moat.description.none")

    return descriptions.get(max_dim, (t("moat.type.none"), ""))
