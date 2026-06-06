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
