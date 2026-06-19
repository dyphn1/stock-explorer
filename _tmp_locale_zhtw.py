# Insert health keys into zh-TW.yaml after business_card: section
with open("locales/zh-TW.yaml", "r") as f:
    lines = f.readlines()

# Find line with top-level "business_card:" (L730)
insert_idx = None
for i, line in enumerate(lines):
    if line.strip() == "business_card:" and not line.startswith(' ') and not line.startswith('\t'):
        # Find next top-level key (not indented)
        for j in range(i+1, len(lines)):
            if lines[j] and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                insert_idx = j
                break
        break

if insert_idx is None:
    insert_idx = len(lines)

health_keys = """  health:
    section_title: 公司健康狀況
    source_estimated: 📊 系統估算
    confidence_note: 信心指標反映資料完整度，非AI預測確定性
    risk_analysis_title: ⚠️ 風險分析 — 什麼可能出問題？

"""

lines.insert(insert_idx, health_keys)

with open("locales/zh-TW.yaml", "w") as f:
    f.writelines(lines)

print(f"Inserted health keys at line {insert_idx}")

# Now add unit.point to zh-TW.yaml
with open("locales/zh-TW.yaml", "r") as f:
    lines = f.readlines()

added_point = False
for i, line in enumerate(lines):
    if line.strip() == "unit:":
        # Check if point already exists
        point_exists = False
        for j in range(i+1, len(lines)):
            if not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                break
            if "point:" in lines[j]:
                point_exists = True
                break
        if not point_exists:
            lines.insert(i+1, "  point: 分\n")
            added_point = True
        break

if added_point:
    with open("locales/zh-TW.yaml", "w") as f:
        f.writelines(lines)
    print("Added unit.point to zh-TW.yaml")
else:
    print("unit.point already exists or unit: not found in zh-TW.yaml")
