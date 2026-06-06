"""
新聞白話摘要器
將財新聞標題轉化為新手能理解的白話摘要
使用模板方法（不依賴 LLM），確保穩定性和速度
"""

import re
from typing import Optional


# 常見事件類型的白話解釋模板
NEWS_TEMPLATES = {
    # 財務相關
    "財報": {
        "keywords": ["財報", "營收", "獲利", "eps", "每股盈餘"],
        "template": "{company} 公布了最新成绩单：{rephrase}。对投资人来说，这代表 {implication}。",
    },
    "股利": {
        "keywords": ["股利", "配息", "除權息", "現金股利", "股票股利"],
        "template": "{company} 宣布了股利政策：{rephrase}。如果你持有这家公司的股票，{implication}。",
    },
    "增資": {
        "keywords": ["增資", "現增", "發行", "可轉債", "cb"],
        "template": "{company} 计划募资：{rephrase}。增資代表公司需要更多资金，{implication}。",
    },
    # 營運相關
    "擴廠": {
        "keywords": ["擴廠", "投資", "設廠", "資本支出", "capex", "新建"],
        "template": "{company} 要扩大规模了：{rephrase}。这表示公司看好未来需求，{implication}。",
    },
    "訂單": {
        "keywords": ["訂單", "接單", "簽約", "合作", "客戶"],
        "template": "{company} 拿到了新订单：{rephrase}。新订单代表公司未来收入有保障，{implication}。",
    },
    "漲價": {
        "keywords": ["漲價", "調漲", "價格"],
        "template": "{company} 要涨价了：{rephrase}。涨价可能代表市场需求好，{implication}。",
    },
    # 人事相關
    "經營權": {
        "keywords": ["經營權", "董監", "董事會", "股東會", "改選"],
        "template": "{company} 有经营权异动的消息：{rephrase}。经营权的稳定度会影响公司发展方向，{implication}。",
    },
    # 產品相關
    "新產品": {
        "keywords": ["新產品", "推出", "發布", "上市", "量產"],
        "template": "{company} 推出了新产品：{rephrase}。新产品代表公司在创新，{implication}。",
    },
    # 法律與風險
    "訴訟": {
        "keywords": ["訴訟", "官司", "專利", "侵權"],
        "template": "{company} 有法律相关消息：{rephrase}。法律争议可能影响公司声誉和财务状况，{implication}。",
    },
    # 評價相關
    "評等": {
        "keywords": ["評等", "升", "降", "目標價", "買進", "賣出"],
        "template": "法人对 {company} 的评价有变化：{rephrase}。法人评等变化会影响市场信心，{implication}。",
    },
}


def summarize_news(title: str, company_name: str = "這家公司") -> str:
    """
    將新聞標題轉化為白話摘要
    返回: 白話摘要字串（1-2 句話）
    """
    if not title or not title.strip():
        return f"近期沒有關於 {company_name} 的重大新聞。"

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

    return config["template"].format(
        company=company_name,
        rephrase=rephrase,
        implication=implication,
    )


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
    implications = {
        "財報": "可以關注公司賺錢能力有沒有變化",
        "股利": "可以注意配息金額是否符合預期",
        "增資": "短期可能稀釋每股盈餘，但長期要看資金用途",
        "擴廠": "短期會增加支出，長期可能帶來更多收入",
        "訂單": "代表公司產品有市場需求",
        "漲價": "可能提升毛利率，但也要看客戶是否接受",
        "經營權": "經營團隊的穩定度會影響公司策略",
        "新產品": "代表公司持續創新，但新產品能否成功還需觀察",
        "訴訟": "需要關注訴訟結果對公司的影響",
        "評等": "可以參考法人的看法，但最終還是要看公司基本面",
    }
    return implications.get(category, "值得持續關注")


def _generic_summary(title: str, company_name: str) -> str:
    """通用摘要（當無法匹配特定模板時）"""
    simplified = _simplify_title(title)
    return f"{company_name} 有最新消息：{simplified}。建議關注後續發展對公司的影響。"


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
