"""
新聞白話摘要器
將財新聞標題轉化為新手能理解的白話摘要
使用模板方法（不依賴 LLM），確保穩定性和速度
"""

import re
from typing import Optional
from src.core.i18n import t


# 常見事件類型的白話解釋模板
NEWS_TEMPLATES = {
    # 財務相關
    "財報": {
        "keywords": ["財報", "營收", "獲利", "eps", "每股盈餘"],
        "message_key": "news_summarizer_template_financial_report",
    },
    "股利": {
        "keywords": ["股利", "配息", "除權息", "現金股利", "股票股利"],
        "message_key": "news_summarizer_template_dividend",
    },
    "增資": {
        "keywords": ["增資", "現增", "發行", "可轉債", "cb"],
        "message_key": "news_summarizer_template_capital_increase",
    },
    # 營運相關
    "擴廠": {
        "keywords": ["擴廠", "投資", "設廠", "資本支出", "capex", "新建"],
        "message_key": "news_summarizer_template_factory_expansion",
    },
    "訂單": {
        "keywords": ["訂單", "接單", "簽約", "合作", "客戶"],
        "message_key": "news_summarizer_template_order",
    },
    "漲價": {
        "keywords": ["漲價", "調漲", "價格"],
        "message_key": "news_summarizer_template_price_increase",
    },
    # 人事相關
    "經營權": {
        "keywords": ["經營權", "董監", "董事會", "股東會", "改選"],
        "message_key": "news_summarizer_template_management_rights",
    },
    # 產品相關
    "新產品": {
        "keywords": ["新產品", "推出", "發布", "上市", "量產"],
        "message_key": "news_summarizer_template_new_product",
    },
    # 法律與風險
    "訴訟": {
        "keywords": ["訴訟", "官司", "專利", "侵權"],
        "message_key": "news_summarizer_template_lawsuit",
    },
    # 評價相關
    "評等": {
        "keywords": ["評等", "升", "降", "目標價", "買進", "賣出"],
        "message_key": "news_summarizer_template_rating",
    },
}


def summarize_news(title: str, company_name: str = "這家公司") -> str:
    """
    將新聞標題轉化為白話摘要
    返回: 白話摘要字串（1-2 句話）
    """
    if not title or not title.strip():
        return t("news_summarizer_no_news", company_name=company_name)

    title = title.strip()

    # 嘗試匹配模板
    for category, config in NEWS_TEMPLATES.items():
        if _match_keywords(title, config["keywords"]):
            return _apply_template(category, title, company_name, config)

    # fallback: 通用摘要
    return _generic_summary(title, company_name)


def _match_keywords(title: str, keywords: list) -> bool:
    """檢查標題是否包含關鍵字"""
    title_lower = title.lower()
    return any(kw.lower() in title_lower for kw in keywords)


def _apply_template(category: str, title: str, company_name: str, config: dict) -> str:
    """套用模板生成摘要"""
    rephrase = _simplify_title(title)
    implication = _get_implication(category)

    return t(config["message_key"], company=company_name, rephrase=rephrase, implication=implication)


def _simplify_title(title: str) -> str:
    """將專業標題簡化"""
    # 移除不必要的括號內容
    title = re.sub(r'[（(][^）)]*[）)]', '', title)
    # 簡化常見用語
    replacements = {
        "年增": "比去年同期成長",
        "年減": "比去年同期減少",
        "季增": "比上一季成長",
        "季減": "比上一季減少",
        "月增": "比上個月成長",
        "月減": "比上個月減少",
        "EPS": "每股盈餘",
        "ROE": "股東權益報酬率",
        "YoY": "比去年同期",
        "QoQ": "比上一季",
        "MoM": "比上個月",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title.strip()


def _get_implication(category: str) -> str:
    """根據事件類型給出影響說明"""
    implication_keys = {
        "財報": "news_summarizer_implication_financial_report",
        "股利": "news_summarizer_implication_dividend",
        "增資": "news_summarizer_implication_capital_increase",
        "擴廠": "news_summarizer_implication_factory_expansion",
        "訂單": "news_summarizer_implication_order",
        "漲價": "news_summarizer_implication_price_increase",
        "經營權": "news_summarizer_implication_management_rights",
        "新產品": "news_summarizer_implication_new_product",
        "訴訟": "news_summarizer_implication_lawsuit",
        "評等": "news_summarizer_implication_rating",
    }
    key = implication_keys.get(category)
    if key:
        return t(key)
    return t("news_summarizer_implication_default")
def _generic_summary(title: str, company_name: str) -> str:
    """通用摘要（當無法匹配特定模板時）"""
    simplified = _simplify_title(title)
    return t("news_summarizer_generic_summary", company_name=company_name, simplified=simplified)
def get_news_impact_level(title: str) -> str:
    """
    判斷新聞影響程度
    返回: "high" | "medium" | "low"
    """
    high_impact_keywords = ["財報", "營收", "獲利", "虧損", "股利", "經營權", "合併", "收購"]
    medium_impact_keywords = ["訂單", "投資", "擴廠", "新產品", "合作", "簽約"]

    title_lower = title.lower()
    if any(kw in title_lower for kw in high_impact_keywords):
        return "high"
    elif any(kw in title_lower for kw in medium_impact_keywords):
        return "medium"
    return "low"
