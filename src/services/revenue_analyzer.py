"""
營收組成分析器
從損益表解析營收來源組成，用於生成圓餅圖
"""

from typing import Optional
import pandas as pd
from src.core.i18n import t

# 已知公司的營收組成（當 FinMind 無法提供細項時使用）
# 這些是公開資訊，來自各公司財報
KNOWN_COMPANY_REVENUE = {
    "2330": {  # 台積電
        "3奈米": {"value": 30, "description": "最新製程，蘋果、高通等大客戶搶著用"},
        "5奈米": {"value": 25, "description": "成熟先進製程，用於手機和電腦晶片"},
        "7奈米": {"value": 15, "description": "用於中階手機和電玩晶片"},
        "成熟製程": {"value": 20, "description": "28奈米以上，用於汽車、家電等"},
        "其他": {"value": 10, "description": "封裝測試、光罩等周邊服務"},
    },
    "2317": {  # 鴻海
        "消費電子(iPhone)": {"value": 50, "description": "幫蘋果組裝 iPhone 等消費電子產品"},
        "雲端伺服器": {"value": 20, "description": "幫品牌客戶製造雲端伺服器"},
        "元件": {"value": 15, "description": "連接器、機殼等元件"},
        "其他": {"value": 15, "description": "電動車、數位健康等新事業"},
    },
    "2454": {  # 聯發科
        "手機晶片": {"value": 55, "description": "智慧型手機 SoC 晶片，賣給各手機品牌"},
        "智慧終端": {"value": 25, "description": "智慧電視、WiFi、藍牙等晶片"},
        "電源管理": {"value": 10, "description": "各種電子產品的電源管理晶片"},
        "其他": {"value": 10, "description": "ASIC 客製化晶片等"},
    },
    "2308": {  # 台達電
        "電源供應器": {"value": 35, "description": "從手機充電器到資料中心電源"},
        "基礎設施": {"value": 25, "description": "電動車充電樁、通訊基礎建設"},
        "自動化": {"value": 20, "description": "工業自動化設備和機器人"},
        "風扇與散熱": {"value": 10, "description": "伺服器和電腦散熱風扇"},
        "其他": {"value": 10, "description": "視訊顯示、網通設備等"},
    },
    "2881": {  # 富邦金
        "富邦人壽": {"value": 45, "description": "人壽保險業務，保費收入為主"},
        "台北富邦銀行": {"value": 30, "description": "商業銀行存放款、信用卡業務"},
        "富邦證券": {"value": 15, "description": "證券經紀、承銷業務"},
        "其他": {"value": 10, "description": "富邦產險、富邦創投等"},
    },
    "1101": {  # 台泥
        "水泥": {"value": 50, "description": "建築用水泥，蓋房子和公共工程的基本材料"},
        "電力": {"value": 20, "description": "水泥廠的餘熱發電和綠能發電"},
        "廢棄物處理": {"value": 15, "description": "幫工廠處理垃圾和廢棄物"},
        "其他": {"value": 15, "description": "預拌混凝土、環保材料等"},
    },
    "2002": {  # 中鋼
        "條鋼": {"value": 30, "description": "鋼筋、型鋼等建築用鋼材"},
        "熱軋": {"value": 25, "description": "熱軋鋼捲，用於汽車、家電"},
        "冷軋": {"value": 20, "description": "冷軋鋼片，表面品質較佳"},
        "其他": {"value": 25, "description": "棒線、電磁鋼片等特殊鋼材"},
    },
    "1301": {  # 台塑
        "塑膠": {"value": 40, "description": "PVC、PE 等塑膠原料"},
        "石油化工": {"value": 30, "description": "乙烯、丙烯等化工原料"},
        "纖維": {"value": 15, "description": "紡織纖維和布匹"},
        "其他": {"value": 15, "description": "電子材料、醫療用品等"},
    },
}


def analyze_revenue_breakdown(financial_df: pd.DataFrame, stock_id: str, industry: str) -> list:
    """
    分析營收組成
    返回: [{"name": "...", "value": 百分比, "description": "..."}]
    """
    # 優先使用已知資料
    if stock_id in KNOWN_COMPANY_REVENUE:
        return [
            {"name": k, "value": v["value"], "description": v["description"]}
            for k, v in KNOWN_COMPANY_REVENUE[stock_id].items()
        ]

    # 嘗試從損益表解析
    breakdown = _parse_financial_for_segments(financial_df, industry)
    if breakdown:
        return breakdown

    # fallback: 回傳通用結構
    return _create_generic_breakdown(industry)


def _parse_financial_for_segments(financial_df: pd.DataFrame, industry: str) -> list:
    """從損益表中解析業務分類"""
    if financial_df is None or len(financial_df) == 0:
        return []

    # 檢查是否有業務分類欄位
    if "type" in financial_df.columns:
        types = financial_df["type"].unique()
        # 如果有明確的業務分類
        segment_keywords = ["部門", "事業", "業務", "產品", "segment", "business"]
        if any(k in str(t).lower() for t in types for k in segment_keywords):
            latest_date = financial_df["date"].max()
            latest = financial_df[financial_df["date"] == latest_date]
            items = []
            for _, row in latest.iterrows():
                if pd.notna(row.get("value")) and row["value"] > 0:
                    items.append({
                        "name": str(row["type"]),
                        "value": float(row["value"]),
                        "description": _auto_describe_segment(str(row["type"])),
                    })
            if items:
                # 正規化為百分比
                total = sum(i["value"] for i in items)
                for item in items:
                    item["value"] = round(item["value"] / total * 100, 1)
                return items

    return []


def _auto_describe_segment(segment_name: str) -> str:
    """自動生成業務線描述"""
    segment_map = {
        "晶圓代工": "revenue_analyzer_auto_describe_wafer_foundry",
        "IC設計": "revenue_analyzer_auto_describe_ic_design",
        "封裝測試": "revenue_analyzer_auto_describe_packaging_testing",
        "代工製造": "revenue_analyzer_auto_describe_contract_manufacturing",
        "消費電子": "revenue_analyzer_auto_describe_consumer_electronics",
        "銀行": "revenue_analyzer_auto_describe_bank",
        "保險": "revenue_analyzer_auto_describe_insurance",
        "證券": "revenue_analyzer_auto_describe_securities",
        "水泥": "revenue_analyzer_auto_describe_cement",
        "藥物": "revenue_analyzer_auto_describe_pharmaceuticals",
        "醫療器材": "revenue_analyzer_auto_describe_medical_equipment",
    }
    for key, locale_key in segment_map.items():
        if key in segment_name:
            return t(locale_key)
    return t("revenue_analyzer_auto_describe_fallback", segment=segment_name)
def _create_generic_breakdown(industry: str) -> list:
    """建立通用的營收組成（當沒有詳細資料時）"""
    return [
        {"name": t("revenue_analyzer_generic_breakdown_primary_business"), "value": 70.0, "description": t("revenue_analyzer_generic_breakdown_primary_business_description", industry=industry)},
        {"name": t("revenue_analyzer_generic_breakdown_other_investments"), "value": 15.0, "description": t("revenue_analyzer_generic_breakdown_other_investments_description")},
        {"name": t("revenue_analyzer_generic_breakdown_new_business"), "value": 15.0, "description": t("revenue_analyzer_generic_breakdown_new_business_description")},
    ]
