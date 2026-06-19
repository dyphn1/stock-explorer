import pathlib

p = pathlib.Path("src/services/metric_education.py")
orig_lines = p.read_text().splitlines()

# Find the line index where the import block ends (the line after get_yoy_analogy)
# We'll just rebuild the file from scratch using the known structure.
new_lines = []
new_lines.append('"""')
new_lines.append('Metric Education Service')
new_lines.append('將財務指標轉化為新手能秒懂的解釋 + 比喻')
new_lines.append('No Streamlit imports — pure data service.')
new_lines.append('"""')
new_lines.append('')
new_lines.append('from src.services.analogy_engine import (')
new_lines.append('    get_roe_analogy,')
new_lines.append('    get_gross_margin_analogy,')
new_lines.append('    get_per_analogy,')
new_lines.append('    get_pbr_analogy,')
new_lines.append('    get_dividend_analogy,')
new_lines.append('    get_debt_ratio_analogy,')
new_lines.append('    get_yoy_analogy,')
new_lines.append(')')
new_lines.append('')
new_lines.append('from src.core.i18n import t')
new_lines.append('')
new_lines.append('# ── Metric registry ──────────────────────────────────────')
# Now find the rest of the file starting from the line that contains '# Each entry:'
for i, line in enumerate(orig_lines):
    if line.startswith('# Each entry:'):
        # from this line onward
        rest = orig_lines[i:]
        break
else:
    # fallback: find line that starts with '_METRIC_REGISTRY'
    for i, line in enumerate(orig_lines):
        if line.startswith('_METRIC_REGISTRY'):
            rest = orig_lines[i:]
            break
    else:
        rest = []
new_lines.extend(rest)
p.write_text("\n".join(new_lines))
