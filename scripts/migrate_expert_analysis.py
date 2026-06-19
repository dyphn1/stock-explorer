"""One-time migration script: move hardcoded Chinese stock names to t() calls."""
import re

filepath = 'src/pages/business_card/_expert_analysis.py'

with open(filepath, 'r') as f:
    content = f.read()

# Map stock_id -> locale key prefix (matches the locale YAML keys)
stock_locale_map = {
    "2330": "tsmc",
    "2317": "foxconn",
    "2454": "mediatek",
    "2308": "delta",
    "2881": "fubon_finance",
    "2882": "cathay_finance",
    "1301": "formosa_plastics",
    "2002": "china_steel",
    "2382": "quanta",
    "3045": "largan",
}

for stock_id, locale_key in stock_locale_map.items():
    pattern = rf'(t\("expert_analysis\.title", name="[^"]+", id="{stock_id}"\))'
    replacement = rf't("expert_analysis.title", name=t("expert_analysis.{locale_key}.stock_name"), id="{stock_id}")'
    content = re.sub(pattern, replacement, content)

with open(filepath, 'w') as f:
    f.write(content)

print("Python file updated successfully")

# Verify
with open(filepath, 'r') as f:
    for i, line in enumerate(f.readlines(), 1):
        if 'name=' in line:
            print(f"{i}: {line.rstrip()}")
