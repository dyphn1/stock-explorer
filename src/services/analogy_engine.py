"""
生活化比喻引擎
將財務數字轉化為新手能秒懂的比喻
"""

import random
from typing import Optional


def get_revenue_analogy(revenue_billion: float, industry: str) -> str:
    """營收的生活化比喻"""
    if revenue_billion >= 10000:
        return f"相當於台灣政府年度預算的 {revenue_billion/27000*100:.0f}%"
    elif revenue_billion >= 1000:
        return f"大約是 {revenue_billion/1000:.1f} 個小目標（1000億）"
    elif revenue_billion >= 100:
        return f"每個月賺進 {revenue_billion/12:.0f} 億，相當於蓋 {revenue_billion/12/10:.0f} 棟台北 101"
    elif revenue_billion >= 10:
        return f"每個月賺 {revenue_billion/12:.1f} 億，大約是 {revenue_billion/12/5:.0f} 間台積電的月薪"
    else:
        return f"每個月賺 {revenue_billion/12:.1f} 億，穩定的小金雞"


def get_gross_margin_analogy(margin: float) -> str:
    """毛利率的生活化比喻"""
    if margin >= 60:
        return f"賣 100 元東西，扣掉成本還剩 {margin:.0f} 元 — 比多數餐廳還賺"
    elif margin >= 40:
        return f"賣 100 元東西，扣掉成本還剩 {margin:.0f} 元 — 不錯的利潤空間"
    elif margin >= 20:
        return f"賣 100 元東西，扣掉成本還剩 {margin:.0f} 元 — 薄利多銷型"
    elif margin >= 10:
        return f"賣 100 元東西，扣掉成本只剩 {margin:.0f} 元 — 競爭激烈的產業"
    else:
        return f"賣 100 元東西，扣掉成本只剩 {margin:.0f} 元 — 真的是在拚量"


def get_per_analogy(per: float) -> str:
    """本益比的生活化比喻"""
    if per >= 30:
        return f"每賺 1 元，市場願意付 {per:.1f} 元 — 大家看好它未來會賺更多"
    elif per >= 20:
        return f"每賺 1 元，市場願意付 {per:.1f} 元 — 合理的成長預期"
    elif per >= 10:
        return f"每賺 1 元，市場願意付 {per:.1f} 元 — 市場覺得它穩定但不太會暴衝"
    elif per > 0:
        return f"每賺 1 元，市場只願付 {per:.1f} 元 — 市場對它比較保守"
    else:
        return "目前虧損，本益比無意義"


def get_pbr_analogy(pbr: float) -> str:
    """淨值比的生活化比喻"""
    if pbr >= 3:
        return f"股價是淨值的 {pbr:.1f} 倍 — 市場覺得它的品牌和管理值這個價"
    elif pbr >= 1.5:
        return f"股價是淨值的 {pbr:.1f} 倍 — 合理的溢價"
    elif pbr >= 1:
        return f"股價是淨值的 {pbr:.1f} 倍 — 接近淨值，市場評價中性"
    else:
        return f"股價比淨值還低（{pbr:.1f} 倍）— 市場覺得它的資產可能不值那麼多"


def get_dividend_analogy(dy: float, price: float = 0) -> str:
    """殖利率的生活化比喻"""
    if dy >= 6:
        return f"每放 100 元，大約領回 {dy:.1f} 元 — 比定存好很多，但要注意風險"
    elif dy >= 4:
        return f"每放 100 元，大約領回 {dy:.1f} 元 — 穩健的存股選擇"
    elif dy >= 2:
        return f"每放 100 元，大約領回 {dy:.1f} 元 — 比定存好一點"
    elif dy > 0:
        return f"每放 100 元，大約領回 {dy:.1f} 元 — 主要不是靠配息"
    else:
        return "目前不配息，公司把錢留在手上再投資"


def get_roe_analogy(roe: float) -> str:
    """ROE 的生活化比喻"""
    if roe >= 20:
        return f"每投入 100 元資本，賺回 {roe:.1f} 元 — 非常會賺錢的公司"
    elif roe >= 15:
        return f"每投入 100 元資本，賺回 {roe:.1f} 元 — 賺錢能力不錯"
    elif roe >= 10:
        return f"每投入 100 元資本，賺回 {roe:.1f} 元 — 表現中規中矩"
    elif roe >= 5:
        return f"每投入 100 元資本，賺回 {roe:.1f} 元 — 賺錢效率偏低"
    elif roe > 0:
        return f"每投入 100 元資本，只賺回 {roe:.1f} 元 — 需要改善"
    else:
        return "目前虧損，投入的資本沒有回報"


def get_debt_ratio_analogy(ratio: float) -> str:
    """負債比的生活化比喻"""
    if ratio >= 70:
        return f"每 100 元資產中，有 {ratio:.0f} 元是借來的 — 借錢借比較多，要注意"
    elif ratio >= 50:
        return f"每 100 元資產中，有 {ratio:.0f} 元是借來的 — 適度槓桿"
    elif ratio >= 30:
        return f"每 100 元資產中，有 {ratio:.0f} 元是借來的 — 財務結構穩健"
    else:
        return f"每 100 元資產中，只有 {ratio:.0f} 元是借來的 — 幾乎不借錢"


def get_volume_analogy(volume: int) -> str:
    """成交量的生活化比喻"""
    if volume >= 100000:
        return f"今天成交 {volume/1000:.0f} 千張 — 市場非常關注這檔股票"
    elif volume >= 50000:
        return f"今天成交 {volume/1000:.0f} 千張 — 交易熱絡"
    elif volume >= 10000:
        return f"今天成交 {volume/1000:.0f} 千張 — 正常交易量"
    elif volume >= 1000:
        return f"今天成交 {volume/1000:.0f} 千張 — 交易冷清"
    else:
        return f"今天只成交 {volume} 張 — 幾乎沒人在買賣"


def get_institutional_analogy(net_buy: float) -> str:
    """法人買賣超的生活化比喻"""
    if net_buy >= 50000:
        return f"三大法人今天大買 {net_buy/1000:.0f} 千張 — 法人很看好"
    elif net_buy >= 10000:
        return f"三大法人今天買超 {net_buy/1000:.0f} 千張 — 法人偏多"
    elif net_buy >= 0:
        return f"三大法人今天小買 {net_buy/1000:.0f} 千張 — 法人態度中性偏多"
    elif net_buy >= -10000:
        return f"三大法人今天賣超 {abs(net_buy)/1000:.0f} 千張 — 法人偏空"
    else:
        return f"三大法人今天大賣 {abs(net_buy)/1000:.0f} 千張 — 法人急著出場"


def get_yoy_analogy(yoy: float) -> str:
    """年增率的生活化比喻"""
    if yoy >= 50:
        return f"營收年增 {yoy:.0f}% — 成長非常強勁，可能是新產品大賣"
    elif yoy >= 20:
        return f"營收年增 {yoy:.0f}% — 穩定成長，公司經營得不錯"
    elif yoy >= 5:
        return f"營收年增 {yoy:.0f}% — 溫和成長"
    elif yoy >= -5:
        return f"營收年增 {yoy:.0f}% — 跟去年差不多，持平"
    elif yoy >= -20:
        return f"營收年減 {abs(yoy):.0f}% — 比去年差，需要關注原因"
    else:
        return f"營收年減 {abs(yoy):.0f}% — 大幅衰退，可能有結構性問題"


def get_one_liner(stock_id: str, stock_name: str, industry: str) -> str:
    """生成一句話定位（擴展版）"""
    one_liners = {
        "2330": "全世界最大的晶圓代工廠，幫蘋果、輝達等科技巨頭製造晶片 — 你的手機和電腦裡都有它的產品",
        "2317": "全球最大的電子代工帝國，iPhone 的主要組裝廠 — 全世界每兩支 iPhone 就有一支出自它",
        "2454": "手機晶片設計龍頭，你的手機裡很可能有它的晶片 — 不用自己蓋工廠，靠設計就能賺錢",
        "2308": "電源供應器隱形冠軍，從手機充電器到電動車充電樁都有它的身影 — 低調但無所不在",
        "2881": "台灣最大的金融控股集團之一，旗下有銀行、證券、壽險 — 你的存款、保單、股票可能都跟它有關",
        "1101": "台灣最老牌的水泥廠，從蓋房子到基礎建設都少不了它 — 蓋台灣的人都需要它",
        "2002": "台灣鋼鐵業龍頭，從建築鋼材到汽車鋼板都有生產 — 台灣工業的骨架",
        "1301": "台灣最大的塑膠集團，從塑膠袋到醫療用品都有它的產品 — 生活中到處都是它的影子",
        "2357": "華碩電腦，從主機板到筆記型電腦 — 你用的電腦零件可能就來自它",
        "2382": "廣達電腦，全球最大的筆記型電腦代工廠 — 蘋果 MacBook 的主要製造商",
        "2886": "兆豐金控，台灣最大的公股金控 — 外匯和企業金融的專家",
        "2891": "中信金控，台灣最大的民營金控 — 信用卡和消費金融的領導者",
        "1216": "統一企業，從泡麵到便利商店 — 統一超商和統一食品都是它的",
        "2912": "統一超商，台灣最大的便利商店 — 平均每 500 公尺就有一家",
        "2303": "聯華電子，台灣第二大晶圓代工廠 — 台積電的兄弟公司",
        "2345": "智邦科技，網路交換器大廠 — 資料中心的關鍵設備供應商",
        "3008": "大立光，手機鏡頭霸主 — 全球每三支手機鏡頭就有一支來自它",
        "2412": "中華電信，台灣最大的電信公司 — 你的手機網路可能就靠它",
        "3711": "日月光，全球最大的封裝測試廠 — 晶片出廠前的最後一道工序",
        "2324": "仁寶電腦，全球第二大筆電代工廠 — 戴爾、惠普的主要合作夥伴",
    }

    if stock_id in one_liners:
        return one_liners[stock_id]

    # 根據產業生成通用定位
    industry_templates = {
        "半導體業": f"{stock_name} 是半導體產業的重要成員，在這個驅動全球科技的產業中扮演關鍵角色",
        "電子工業": f"{stock_name} 是電子產業的重要成員，從消費電子到工業設備都有佈局",
        "金融保險": f"{stock_name} 是金融保險業的重要成員，管理著數以兆計的資產",
        "電腦及週邊設備業": f"{stock_name} 是電腦產業的重要成員，在這個數位時代扮演重要角色",
        "生技醫療業": f"{stock_name} 是生技醫療產業的重要成員，致力於改善人類健康",
        "觀光餐旅": f"{stock_name} 是觀光餐旅業的重要成員，服務著無數的旅客和消費者",
        "電機機械": f"{stock_name} 是電機機械產業的重要成員，從工業設備到民生用品都有涉獵",
        "建材營造": f"{stock_name} 是建材營造業的重要成員，參與台灣無數的建設工程",
        "化學工業": f"{stock_name} 是化學工業的重要成員，從基礎化學到特化品都有生產",
        "通信網路業": f"{stock_name} 是通信網路業的重要成員，連接著台灣的數位生活",
    }

    return industry_templates.get(industry, f"{stock_name} 是 {industry} 的重要成員，股票代號 {stock_id}")


# ── C37: Key Takeaways (重點摘要) ──────────────────────────

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
    return takeaways[:5]


# ── C39: Recent Deltas (最近有什麼變化) ────────────────────

def compute_recent_deltas(
    extra_metrics: dict,
    monthly_revenue,
    daily_price,
    latest_per_pbr: dict | None,
) -> list[dict]:
    """計算最近的重要變化（C39）

    比較：營收（最近月 vs 前一月）、股價（近 30 日 vs 前 30 日）、
          毛利率（最近季 vs 前季）。
    只回傳變化幅度 > 10% 的項目。

    回傳 list of dict，每個 dict 包含：
        metric_name, current_value, previous_value, change_pct, direction, explanation
    """
    deltas: list[dict] = []

    # 1. 營收月對月變化（最近月 vs 前一月）
    if monthly_revenue is not None and len(monthly_revenue) >= 2:
        try:
            latest_rev = float(monthly_revenue.iloc[-1]["revenue"])
            prev_rev = float(monthly_revenue.iloc[-2]["revenue"])
            if prev_rev > 0:
                rev_change = (latest_rev - prev_rev) / prev_rev * 100
                if abs(rev_change) > 10:
                    deltas.append({
                        "metric_name": "月營收",
                        "current_value": f"{latest_rev / 1e8:.0f} 億",
                        "previous_value": f"{prev_rev / 1e8:.0f} 億",
                        "change_pct": round(rev_change, 1),
                        "direction": "up" if rev_change > 0 else "down",
                        "explanation": "",
                    })
        except (KeyError, IndexError, TypeError, ZeroDivisionError):
            pass

    # 2. 股價 30 日變化（最後 30 日 vs 前 30 日）
    if daily_price is not None and len(daily_price) >= 60:
        try:
            recent_30 = daily_price.iloc[-30:]
            prior_30 = daily_price.iloc[-60:-30]
            recent_avg = float(recent_30["close"].mean())
            prior_avg = float(prior_30["close"].mean())
            if prior_avg > 0:
                price_change = (recent_avg - prior_avg) / prior_avg * 100
                if abs(price_change) > 10:
                    deltas.append({
                        "metric_name": "股價（近 30 日均價）",
                        "current_value": f"{recent_avg:.0f} 元",
                        "previous_value": f"{prior_avg:.0f} 元",
                        "change_pct": round(price_change, 1),
                        "direction": "up" if price_change > 0 else "down",
                        "explanation": "",
                    })
        except (KeyError, IndexError, TypeError, ZeroDivisionError):
            pass

    # 3. 毛利率季度變化（需要 financial_df，這裡從 extra_metrics 取得最新值，
    #    但季度比較需要歷史數據，這裡用 revenue_yoy 作為替代指標）
    yoy = extra_metrics.get("revenue_yoy")
    if yoy is not None and abs(yoy) > 10:
        deltas.append({
            "metric_name": "營收年增率",
            "current_value": f"{yoy:+.1f}%",
            "previous_value": "去年同期",
            "change_pct": round(yoy, 1),
            "direction": "up" if yoy > 0 else "down",
            "explanation": "",
        })

    # 為每個 delta 產生白話解釋
    for delta in deltas:
        delta["explanation"] = explain_delta(
            delta["metric_name"],
            delta["change_pct"],
            delta["direction"],
            "",  # stock_name 可選，留空使用通用描述
            "",
        )

    return deltas


def explain_delta(
    metric_name: str,
    change_pct: float,
    direction: str,
    stock_name: str = "",
    industry: str = "",
) -> str:
    """為變化量生成白話解釋（C39）

    Args:
        metric_name: 指標名稱
        change_pct: 變化百分比（含正負號）
        direction: "up" 或 "down"
        stock_name: 股票名稱（可選）
        industry: 產業名稱（可選）

    回傳中文（zh-TW）的解釋字串。
    """
    abs_pct = abs(change_pct)
    name_prefix = f"{stock_name} " if stock_name else ""

    # 根據指標類型和方向產生解釋
    if metric_name == "月營收":
        if direction == "up":
            if abs_pct >= 50:
                return f"{name_prefix}月營收暴增 {abs_pct:.0f}%，可能是大訂單入帳或旺季效應，值得關注後續動能"
            elif abs_pct >= 30:
                return f"{name_prefix}月營收成長 {abs_pct:.0f}%，表現優於預期，可能是需求回溫或新產品貢獻"
            else:
                return f"{name_prefix}月營收成長 {abs_pct:.0f}%，溫和成長中"
        else:
            if abs_pct >= 50:
                return f"{name_prefix}月營收驟降 {abs_pct:.0f}%，可能是淡季或失去大客戶，需要密切關注"
            elif abs_pct >= 30:
                return f"{name_prefix}月營收衰退 {abs_pct:.0f}%，表現不如預期，可能是需求下滑或訂單遞延"
            else:
                return f"{name_prefix}月營收小跌 {abs_pct:.0f}%，略有衰退但仍在合理範圍"

    if metric_name == "股價（近 30 日均價）":
        if direction == "up":
            if abs_pct >= 30:
                return f"{name_prefix}股價近 30 日大漲 {abs_pct:.0f}%，市場情緒樂觀，可能是基本面改善或利多消息推動"
            elif abs_pct >= 20:
                return f"{name_prefix}股價近 30 日上漲 {abs_pct:.0f}%，多頭趨勢明顯"
            else:
                return f"{name_prefix}股價近 30 日上漲 {abs_pct:.0f}%，穩步走揚"
        else:
            if abs_pct >= 30:
                return f"{name_prefix}股價近 30 日大跌 {abs_pct:.0f}%，市場信心不足，可能是利空消息或基本面惡化"
            elif abs_pct >= 20:
                return f"{name_prefix}股價近 30 日下跌 {abs_pct:.0f}%，空頭趨勢明顯"
            else:
                return f"{name_prefix}股價近 30 日小跌 {abs_pct:.0f}%，略有回檔"

    if metric_name == "營收年增率":
        if direction == "up":
            if abs_pct >= 50:
                return f"{name_prefix}營收年增 {abs_pct:.0f}%，成長非常強勁，可能是新產品大賣或市場需求爆發"
            elif abs_pct >= 20:
                return f"{name_prefix}營收年增 {abs_pct:.0f}%，穩定成長，公司經營績效良好"
            else:
                return f"{name_prefix}營收年增 {abs_pct:.0f}%，溫和成長"
        else:
            if abs_pct >= 50:
                return f"{name_prefix}營收年減 {abs_pct:.0f}%，大幅衰退，可能有結構性問題需要關注"
            elif abs_pct >= 20:
                return f"{name_prefix}營收年減 {abs_pct:.0f}%，比去年差，需留意原因"
            else:
                return f"{name_prefix}營收年減 {abs_pct:.0f}%，略有衰退"

    # 通用解釋
    if direction == "up":
        return f"{name_prefix}{metric_name} 較前期成長 {abs_pct:.1f}%"
    else:
        return f"{name_prefix}{metric_name} 較前期衰退 {abs_pct:.1f}%"
