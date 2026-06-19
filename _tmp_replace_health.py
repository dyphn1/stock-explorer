import re

path = "src/pages/business_card/_sections/_health.py"
with open(path, "r") as f:
    content = f.read()

# 1. Section title
content = content.replace(
    '_section_title_with_read_time("🏥 公司健康狀況", health_summary_text)',
    '_section_title_with_read_time(t("business_card.health.section_title"), health_summary_text)'
)

# 2. Metric value unit
content = content.replace(
    'metric_value=f"{score:.0f} 分"',
    'metric_value=f"{score:.0f} {t(\'unit.point\')}"'
)

# 3. Source label
content = content.replace(
    'source_label="📊 系統估算"',
    'source_label=t("business_card.health.source_estimated")'
)

# 4. Confidence note
content = content.replace(
    'st.caption(f"{_confidence_badge(0.9)} · 信心指標反映資料完整度，非AI預測確定性")',
    'st.caption(f"{_confidence_badge(0.9)} · {t(\'business_card.health.confidence_note\')}")'
)

# 5. Risk analysis expander title
content = content.replace(
    'with st.expander("⚠️ 風險分析 — 什麼可能出問題？", expanded=False):',
    'with st.expander(t("business_card.health.risk_analysis_title"), expanded=False):'
)

with open(path, "w") as f:
    f.write(content)

print("Replacements done")

# Verify
with open(path, "r") as f:
    new_content = f.read()

remaining_cn_in_ui = []
for i, line in enumerate(new_content.split('\n'), 1):
    s = line.strip()
    if s.startswith('#') or s.startswith('"""') or "'''" in s:
        continue
    if "t('" in line or 't("' in line:
        continue
    matches = re.findall(r'''[\"'][^\"']*[\u4e00-\u9fff]+[^\"']*[\"']''', line)
    matches = [m for m in matches if '{{' not in m]
    if matches:
        remaining_cn_in_ui.append((i, line.strip()[:80]))

if remaining_cn_in_ui:
    print(f"WARNING: {len(remaining_cn_in_ui)} Chinese strings still remain:")
    for ln, txt in remaining_cn_in_ui:
        print(f"  L{ln}: {txt}")
else:
    print("SUCCESS: No Chinese UI strings remain")
