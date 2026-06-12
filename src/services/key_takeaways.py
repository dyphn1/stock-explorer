"""
重點摘要（Key Takeaways）模組
精選 + 自動生成重點摘要
"""

from src.services.analogy_engine import get_one_liner

# Curated key takeaways for top 20 stocks (by stock_id)
_KEY_TAKEAWAYS: dict[str, list[str]] = {
    "2330": [
        "全球晶圓代工龍頭，市佔率超過 55%，技術領先優勢明顯",
        "先進製程（5nm/3nm）持續滿載，是蘋果、輝達等巨頭的唯一選擇",
        "護城河極深：高資本支出門檻讓競爭者難以追上",
        "長期受惠於 AI、HPC、電動車等結構性成長趨勢",
    ],
    "2317": [
        "全球最大的電子代工帝國，iPhone 主要組裝廠",
        "營收規模巨大但毛利率偏低（約 5-6%），靠量取勝",
        "積極佈局電動車、伺服器、機器人等新領域",
        "風險：過度依賴蘋果訂單，地緣政治影響產能配置",
    ],
    "2454": [
        "手機晶片設計龍頭，聯發科天系列在 Android 陣營市佔率第一",
        "輕資產模式（無晶圓廠），毛利率高達 45% 以上",
        "積極拓展車用、AIoT、Wi-Fi 7 等新市場",
        "與高通競爭激烈，但性價比優勢在中低階市場明顯",
    ],
    "2308": [
        "電源供應器隱形冠軍，從消費電子到資料中心都有佈局",
        "毛利率穩定在 25-30%，獲利能力優於同業",
        "受惠於 AI 伺服器電源需求爆發，成長動能強勁",
        "產品線多元，分散單一客戶風險",
    ],
    "2881": [
        "台灣最大泛公股金控之一，旗下涵蓋銀行、證券、壽險",
        "獲利穩健，配息大方，是存股族熱門選擇",
        "房貸比重較高，需留意房地產市場波動風險",
        "數位金融轉型積極，但進展相對民營金控緩慢",
    ],
    "1101": [
        "台灣最老牌水泥廠，深耕市場超過 70 年",
        "水泥產業景氣與公共建設高度相關",
        "多角化經營（電力、化工、運輸）降低單一產業風險",
        "獲利穩定但成長性有限，適合保守型投資人",
    ],
    "2002": [
        "台灣鋼鐵業龍頭，產品線完整（鋼筋、型鋼、鋼板）",
        "鋼鐵景氣循環明顯，獲利波動較大",
        "積極發展高附加價值產品（汽車板、電磁鋼片）",
        "受惠於公共建設與製造業回溫",
    ],
    "1301": [
        "台灣最大塑膠集團，產品遍及民生與工業用途",
        "上游原料（乙烯）價格波動影響獲利甚鉅",
        "兩岸佈局完整，但中國市場競爭加劇",
        "朝高值化、環保材料方向轉型",
    ],
    "2357": [
        "華碩品牌價值高，ROG 電競系列在全球市佔率領先",
        "PC 產業成熟，但電競與創作者市場仍有成長空間",
        "AI PC 換機潮是未來重要成長動能",
        "伺服器業務快速成長，成為第二成長曲線",
    ],
    "2382": [
        "全球最大筆記型電腦代工廠，蘋果 MacBook 主要製造商",
        "積極轉型伺服器/雲端業務，AI 伺服器訂單暢旺",
        "毛利率約 3-4%，靠規模經濟維持獲利",
        "風險：筆電市場飽和，成長依賴伺服器業務",
    ],
    "2886": [
        "台灣最大公股金控，外匯業務市場領導者",
        "海外據點最多，跨境金融業務是核心優勢",
        "獲利穩健，殖利率約 3-4%，適合存股",
        "公股背景讓其經營相對保守穩健",
    ],
    "2891": [
        "台灣最大民營金控，信用卡與消費金融領導品牌",
        "中信銀行是台灣最大的信用卡發卡行",
        "海外佈局積極，尤其在中國和東南亞",
        "數位金融發展領先同業，Bank 3.0 佈局完整",
    ],
    "1216": [
        "統一集團橫跨食品、零售、物流的綜合企業集團",
        "統一超商（7-11）是台灣最大的便利商店網絡",
        "多角化經營穩定，現金流充沛",
        "東南亞和中國市場是未來成長重點",
    ],
    "2912": [
        "台灣便利商店龍頭，市佔率超過 50%",
        "據點密度全球最高（平均每 500 公尺一家）",
        "從零售延伸到物流、金融、電商等生態系",
        "單店營收成長趨緩，但多元服務提升客單價",
    ],
    "2303": [
        "台灣第二大晶圓代工廠，專注成熟製程",
        "成熟製程（28nm 以上）需求穩定，車用、IoT 是主力",
        "與台積電互補，不直接競爭先進製程",
        "產能利用率是觀察營運的關鍵指標",
    ],
    "2345": [
        "網路交換器大廠，資料中心關鍵設備供應商",
        "受惠於 AI 資料中心建置潮，400G/800G 交換器需求爆發",
        "白牌交換器趨勢有利於獨立供應商",
        "客戶涵蓋全球主要雲端服務業者",
    ],
    "3008": [
        "手機鏡頭霸主，全球市佔率超過 30%",
        "技術門檻高，鏡片數持續增加（7P→8P）提升單價",
        "蘋果和 Android 陣營雙引擎驅動",
        "風險：中國競爭者（舜宇、瑞聲）持續追趕",
    ],
    "2412": [
        "台灣最大電信業者，行動用戶數超過 1,000 萬",
        "電信產業穩定，現金流充沛，配息大方",
        "5G 資費提升 ARPU，但資本支出也增加",
        "積極發展企業客戶和數位加值服務",
    ],
    "3711": [
        "全球最大封裝測試廠，與台積電緊密合作",
        "先進封裝（CoWoS、InFO）是 AI 晶片關鍵製程",
        "受惠於 AI 晶片封裝需求爆發，產能供不應求",
        "資本支出持續增加以滿足客戶需求",
    ],
    "2324": [
        "全球第二大筆記型電腦代工廠，戴爾、惠普主要夥伴",
        "積極拓展伺服器業務，降低對筆電依賴",
        "毛利率偏低，靠規模和效率維持競爭力",
        "越南、墨西哥等海外產能佈局分散風險",
    ],
}


def generate_key_takeaways(
    stock_id: str,
    stock_name: str,
    industry: str,
    extra_metrics: dict,
    latest_per_pbr: dict | None,
    monthly_revenue,
    financial_df,
) -> list[str]:
    """生成 3-5 條重點摘要（C37）

    優先使用精選內容（curated），若無則根據財務數據自動生成。
    回傳中文（zh-TW）的重點摘要列表。
    """
    # 1. 精選內容優先
    if stock_id in _KEY_TAKEAWAYS:
        return _KEY_TAKEAWAYS[stock_id]

    # 2. 自動生成
    takeaways: list[str] = []

    # 一句話定位作為第一條
    one_liner = get_one_liner(stock_id, stock_name, industry)
    # 取第一句（以 — 或逗號前的部分）
    first_sentence = one_liner.split("—")[0].strip()
    if first_sentence:
        takeaways.append(f"{first_sentence}，是 {industry} 的重要成員")

    # 毛利率
    gm = extra_metrics.get("gross_margin")
    if gm is not None:
        if gm >= 40:
            takeaways.append(f"毛利率 {gm:.1f}%，獲利能力在同產業中屬於前段班")
        elif gm >= 20:
            takeaways.append(f"毛利率 {gm:.1f}%，利潤空間穩定")
        elif gm >= 10:
            takeaways.append(f"毛利率 {gm:.1f}%，屬於薄利多銷的經營模式")
        else:
            takeaways.append(f"毛利率僅 {gm:.1f}%，獲利空間有限，需靠規模取勝")

    # 營收年增率
    yoy = extra_metrics.get("revenue_yoy")
    if yoy is not None:
        if yoy >= 20:
            takeaways.append(f"營收年增 {yoy:.0f}%，成長動能強勁")
        elif yoy >= 5:
            takeaways.append(f"營收年增 {yoy:.0f}%，穩定成長中")
        elif yoy >= -5:
            takeaways.append(f"營收年增 {yoy:.0f}%，與去年持平")
        else:
            takeaways.append(f"營收年減 {abs(yoy):.0f}%，需留意衰退原因")

    # 本益比
    if latest_per_pbr and latest_per_pbr.get("PER"):
        per = latest_per_pbr["PER"]
        if per >= 25:
            takeaways.append(f"本益比 {per:.1f} 倍，市場給予高度成長預期")
        elif per >= 15:
            takeaways.append(f"本益比 {per:.1f} 倍，評價合理")
        elif per > 0:
            takeaways.append(f"本益比 {per:.1f} 倍，市場評價相對保守")
        else:
            takeaways.append("目前處於虧損狀態，本益比無參考意義")

    # 殖利率
    if latest_per_pbr and latest_per_pbr.get("dividend_yield"):
        dy = latest_per_pbr["dividend_yield"]
        if dy >= 5:
            takeaways.append(f"殖利率 {dy:.2f}%，是熱門的存股選擇")
        elif dy >= 3:
            takeaways.append(f"殖利率 {dy:.2f}%，配息穩健")
        elif dy > 0:
            takeaways.append(f"殖利率 {dy:.2f}%，配息較少，成長優先")
        else:
            takeaways.append("目前不配息，公司將盈餘保留再投資")

    # ROE
    roe = extra_metrics.get("roe")
    if roe is not None:
        if roe >= 20:
            takeaways.append(f"ROE {roe:.1f}%，股東報酬率優異")
        elif roe >= 10:
            takeaways.append(f"ROE {roe:.1f}%，資本運用效率良好")
        elif roe > 0:
            takeaways.append(f"ROE {roe:.1f}%，資本運用效率有改善空間")
        else:
            takeaways.append("目前 ROE 為負，公司尚未為股東創造報酬")

    # 負債比
    debt = extra_metrics.get("debt_ratio")
    if debt is not None:
        if debt >= 70:
            takeaways.append(f"負債比 {debt:.0f}%，財務槓桿較高，需留意償債風險")
        elif debt >= 50:
            takeaways.append(f"負債比 {debt:.0f}%，適度運用槓桿")
        else:
            takeaways.append(f"負債比 {debt:.0f}%，財務結構穩健")

    # 最多回傳 5 條
    return takeaways[:3]
