"""One-time migration: update locale YAML files for expert_analysis i18n."""
import yaml
from pathlib import Path

LOCALES = Path('/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales')

# ── 1. Fix en.yaml: merge duplicate expert_analysis blocks, add stock_name ──

en_path = LOCALES / 'en.yaml'
with open(en_path, 'r') as f:
    en_text = f.read()

# The first expert_analysis block (line ~1430) is a subset of the second (line ~1646).
# YAML: second block overrides first. We need to:
#   a) Remove the first block entirely
#   b) Add stock_name keys to the second block

# Parse: find the first "expert_analysis:" that is NOT the one with full content.
# Strategy: load YAML, then manipulate the dict.

en_data = yaml.safe_load(en_text)

# Add stock_name to each stock section in expert_analysis
stock_names_en = {
    "tsmc": "TSMC",
    "foxconn": "Foxconn",
    "mediatek": "MediaTek",
    "delta": "Delta Electronics",
    "fubon_finance": "Fubon Financial",
    "cathay_finance": "Cathay Financial",
    "formosa_plastics": "Formosa Plastics",
    "china_steel": "China Steel",
    "quanta": "Quanta Computer",
    "largan": "Largan Precision",
}

ea = en_data.get("expert_analysis", {})
for stock_key, name in stock_names_en.items():
    if stock_key in ea and isinstance(ea[stock_key], dict):
        ea[stock_key]["stock_name"] = name

# Now we need to write back. But the file has TWO expert_analysis keys in raw text.
# YAML spec: duplicate keys → last one wins. So loading gives us the right data.
# We need to rewrite the file cleanly.

# However, we must preserve comments and formatting. Let's use a different approach:
# Remove the first expert_analysis block from the raw text, then dump the second
# block with the updated stock_name keys.

# Find the first expert_analysis block (the short one) and remove it.
# It starts with "expert_analysis:\n  title: ..." and ends before "watchlist:"
lines = en_text.split('\n')

# Find the first "expert_analysis:" line
first_ea_start = None
first_ea_end = None
for i, line in enumerate(lines):
    if line.strip() == 'expert_analysis:' and first_ea_start is None:
        first_ea_start = i
    elif first_ea_start is not None and first_ea_end is None:
        # Find where the next top-level key starts (no leading space)
        if line and not line.startswith(' ') and not line.startswith('#'):
            first_ea_end = i
            break

print(f"en.yaml: first expert_analysis block at lines {first_ea_start+1}-{first_ea_end}")

# Remove lines from first_ea_start to first_ea_end (exclusive)
new_lines = lines[:first_ea_start] + lines[first_ea_end:]
en_text_cleaned = '\n'.join(new_lines)

# Now reload and add stock_name to the remaining block
en_data = yaml.safe_load(en_text_cleaned)
ea = en_data["expert_analysis"]
for stock_key, name in stock_names_en.items():
    if stock_key in ea and isinstance(ea[stock_key], dict):
        ea[stock_key]["stock_name"] = name

# But we can't just yaml.dump because it would lose comments and formatting.
# Instead, let's manually insert stock_name into the raw text.
# The second expert_analysis block is now the only one. Let's find it and
# add stock_name entries.

# Actually, let's use a hybrid approach: remove the first block, then manually
# add stock_name to the second block in the raw text.

# Find the position of each stock section in the remaining text
for stock_key, name in stock_names_en.items():
    # Find the line with "  tsmc:" (or similar) and add stock_name after the last key
    # We need to insert "    stock_name: \"TSMC\"" before the next stock or end of block
    pass

# This is getting complex. Let's use a simpler approach: just do string replacement
# on the cleaned text.

# For each stock, find the pattern like "  tsmc:\n    global_leader:" and add stock_name
# Actually, let's add stock_name as the first key in each stock section.

for stock_key, name in stock_names_en.items():
    # Find "  tsmc:\n" and insert "    stock_name: "TSMC"\n" after it
    old = f"  {stock_key}:\n"
    new = f"  {stock_key}:\n    stock_name: \"{name}\"\n"
    en_text_cleaned = en_text_cleaned.replace(old, new)

with open(en_path, 'w') as f:
    f.write(en_text_cleaned)

print("en.yaml updated")

# ── 2. Fix zh-TW.yaml: add full expert_analysis content + stock_name ──

zh_path = LOCALES / 'zh-TW.yaml'
with open(zh_path, 'r') as f:
    zh_text = f.read()

zh_data = yaml.safe_load(zh_text)

stock_names_zh = {
    "tsmc": "台積電",
    "foxconn": "鴻海",
    "mediatek": "聯發科",
    "delta": "台達電",
    "fubon_finance": "富邦金",
    "cathay_finance": "國泰金",
    "formosa_plastics": "台塑",
    "china_steel": "中鋼",
    "quanta": "廣達",
    "largan": "大立光",
}

# Content for zh-TW
zh_content = {
    "tsmc": {
        "stock_name": "台積電",
        "global_leader": "**全球半導體龍頭**：台積電在先進製程（7nm以下）市占率超過90%，是Apple、NVIDIA、AMD等科技巨頭的核心供應商。",
        "growth": "**成長動能**：AI與HPC（高效能運算）需求持續強勁，CoWoS先進封裝產能供不應收，預期2025-2026年營收維持雙位數成長。",
        "risk": "**風險提示**：海外擴張（美國、日本）涉及巨額資本支出，折舊成本上升可能短期壓縮毛利率，地緣政治風險亦需持續關注。",
    },
    "foxconn": {
        "stock_name": "鴻海",
        "ems_leader": "**EMS龍頭**：鴻海是全球最大的電子代工製造商，主要客戶包括Apple、Dell、HP等國際品牌。",
        "transformation": "**加速轉型**：積極拓展AI伺服器、電動車（MIH平台）及半導體業務，AI伺服器業務受惠於資料中心擴建需求。",
        "risk": "**風險提示**：傳統消費電子代工競爭激烈、毛利偏低，轉型成果仍需時間驗證。",
    },
    "mediatek": {
        "stock_name": "聯發科",
        "ic_leader": "**IC設計龍頭**：聯發科是全球主要智慧型手機晶片供應商之一，其Dimensity 5G系列在旗艦及中階市場均有斬獲。",
        "ai_edge": "**AI邊緣運算**：積極拓展AI PC與車用晶片市場，與NVIDIA合作的車用晶片方案備受矚目。",
        "risk": "**風險提示**：智慧型手機市場復甦不均，且來自Qualcomm的競爭壓力持續。",
    },
    "delta": {
        "stock_name": "台達電",
        "power_expert": "**電源管理專家**：台達電是全球電源與散熱管理解決方案的領導者，涵蓋資料中心、電動車充電及工業自動化。",
        "esg": "**ESG先驱**：積極投入節能減碳，資料中心電源與散熱需求受惠於AI基礎建設浪潮。",
        "risk": "**風險提示**：原物料價格波動及供應鏈管理是主要挑戰。",
    },
    "fubon_finance": {
        "stock_name": "富邦金",
        "financial_giant": "**金融控股巨頭**：富邦金是台灣最大的金融控股公司之一，涵蓋銀行、壽險及證券業務。",
        "profit_stable": "**穩定獲利**：受惠於升息循環與資本市場復甦，壽險利差損失壓力緩解，銀行端利息收入成長。",
        "risk": "**風險提示**：金融市場波動及匯率風險需持續關注。",
    },
    "cathay_finance": {
        "stock_name": "國泰金",
        "financial_duo": "**金融雙雄之一**：國泰金是台灣最大的金融控股公司，國泰人壽為全台最大壽險，國泰世華銀行為領先商業銀行。",
        "digital_transform": "**數位轉型**：積極推動數位金融服務，行動銀行及線上保險平台用戶持續成長。",
        "risk": "**風險提示**：壽險業面臨IFRS 17會計準則轉換挑戰，資本市場波動影響投資收益。",
    },
    "formosa_plastics": {
        "stock_name": "台塑",
        "petro_leader": "**石化產業龍頭**：台塑是全球重要的石化生產商，產品涵蓋PVC、PE、PP等通用塑膠及化學品。",
        "transformation": "**轉型策略**：積極發展綠能、半導體材料及高階應用材料，降低對傳統石化循環的依賴。",
        "risk": "**風險提示**：全球石化產能過剩壓力持續，中國競爭者擴張加劇競爭。",
    },
    "china_steel": {
        "stock_name": "中鋼",
        "steel_leader": "**鋼鐵產業龍頭**：中鋼是台灣最大的鋼鐵製造商，產品廣泛應用於建築、機械及汽車工業。",
        "green_transform": "**綠色轉型**：積極推動減碳製程並開發高附加值鋼品。",
        "risk": "**風險提示**：鋼鐵週期明顯，中國鋼鐵傾銷壓力及原物料價格波動是主要風險。",
    },
    "quanta": {
        "stock_name": "廣達",
        "server_leader": "**伺服器代工龍頭**：廣達是全球最大的筆記型電腦代工廠，也是AI伺服器的主要供應商。",
        "ai_server": "**AI伺服器爆發**：受惠於CSP（雲端服務供應商）資本支出擴張，AI伺服器營收占比快速提升。",
        "risk": "**風險提示**：PC/NB市場需求疲弱，AI伺服器訂單能見度雖高但競爭加劇。",
    },
    "largan": {
        "stock_name": "大立光",
        "optical_leader": "**光學鏡頭龍頭**：大立光是全球智慧型手機光學鏡頭的領導者，技術壁壘高，客戶包括Apple、Samsung、華為。",
        "tech_lead": "**技術領先**：在潛望式鏡頭、自由曲面鏡頭等先進光學技術保持領先，持續受惠於多鏡頭趨勢。",
        "risk": "**風險提示**：智慧型手機市場成長放緩，中國競爭者（舜宇、AAC）持續追趕。",
    },
}

ea_zh = zh_data.get("expert_analysis", {})
for stock_key, content in zh_content.items():
    ea_zh[stock_key] = content

# Now write back to zh-TW.yaml. The current file has:
# expert_analysis:
#   title: "..."
#   coming_soon: "..."
#
# We need to add the stock blocks after coming_soon.
# Let's do this by finding the right insertion point.

# Find "coming_soon:" line and insert after it
zh_lines = zh_text.split('\n')
new_zh_lines = []
inserted = False
for i, line in enumerate(zh_lines):
    new_zh_lines.append(line)
    if not inserted and line.strip().startswith('coming_soon:'):
        # Insert all stock blocks after this line
        for stock_key, content in zh_content.items():
            new_zh_lines.append(f"  {stock_key}:")
            for k, v in content.items():
                # Escape any double quotes in the value
                v_escaped = v.replace('"', '\\"')
                new_zh_lines.append(f"    {k}: \"{v_escaped}\"")
        inserted = True

zh_text_new = '\n'.join(new_zh_lines)

with open(zh_path, 'w') as f:
    f.write(zh_text_new)

print("zh-TW.yaml updated")
print("Done!")
