"""
資料模型定義
統一管理所有資料結構
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class CompanyCard:
    """公司名片資料"""
    stock_id: str
    stock_name: str
    industry: str
    one_liner: str  # 一句話定位
    latest_price: float = 0.0
    price_change: float = 0.0
    price_date: str = ""
    market_cap: Optional[float] = None  # 市值（需要付費 API，可能為 None）
    latest_revenue: Optional[float] = None  # 最近月營收
    revenue_yoy: Optional[float] = None  # 營收年增率
    gross_margin: Optional[float] = None  # 毛利率
    operating_margin: Optional[float] = None  # 營業利益率
    net_margin: Optional[float] = None  # 淨利率
    roe: Optional[float] = None  # ROE
    per: Optional[float] = None
    pbr: Optional[float] = None
    dividend_yield: Optional[float] = None
    recent_news_title: str = ""
    recent_news_date: str = ""
    recent_news_summary: str = ""


@dataclass
class RevenueBreakdown:
    """營收組成"""
    period: str  # 期間
    total_revenue: float
    items: list = field(default_factory=list)  # [{"name": "手機晶片", "value": 40.0, "description": "..."}]


@dataclass
class FinancialSummary:
    """財務摘要"""
    period: str
    revenue: float = 0.0
    gross_profit: float = 0.0
    operating_income: float = 0.0
    net_income: float = 0.0
    eps: float = 0.0
    total_assets: float = 0.0
    total_liabilities: float = 0.0
    equity: float = 0.0
    operating_cash_flow: float = 0.0
    free_cash_flow: float = 0.0


@dataclass
class PeerComparison:
    """同業比較"""
    target_stock_id: str
    target_name: str
    benchmark_stock_id: str
    benchmark_name: str
    metrics: dict = field(default_factory=dict)
    # 例如 {"revenue": {"target": 100, "benchmark": 200, "unit": "億"}}


@dataclass
class GroupStructure:
    """集團架構"""
    parent_stock_id: str
    parent_name: str
    subsidiaries: list = field(default_factory=list)
    # [{"stock_id": "...", "name": "...", "holding_ratio": 50.0, "business": "..."}]


@dataclass
class AnalysisResult:
    """分析結果（LLM 生成）"""
    section: str  # 分析區塊
    content: str  # 白話解釋內容
    data_source: str  # 數據來源
    generated_at: str = ""  # 生成時間
