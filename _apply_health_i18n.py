"""One-time script to migrate hardcoded Chinese strings in _health.py to t() calls (part 2)."""
with open('src/pages/business_card/_sections/_health.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Line 92: metric_value=f"{score:.0f} 分",
    (
        'metric_value=f"{score:.0f} \u5206}",',
        "metric_value=f\"{score:.0f} {t('unit.point')}\","
    ),
    # Line 104: st.caption(f"{_confidence_badge(0.9)} · 信心指標反映資料完整度，非AI預測確定性")
    (
        'st.caption(f"{_confidence_badge(0.9)} \u00B7 \u4FE1\u5FC3\u6307\u6A19\u53CD\u6620\u8CC7\u6599\u5B8C\u6574\u5EA6\uFF0C\u975EAI\u9810\u6E2C\u78BA\u5B9A\u6027")',
        'st.caption(f"{_confidence_badge(0.9)} \u00B7 {t(\'business_card.health.confidence_note\')}")'
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'  REPLACED: {old[:60]}...')
    else:
        print(f'  NOT FOUND: {old[:60]}...')

with open('src/pages/business_card/_sections/_health.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done.')
