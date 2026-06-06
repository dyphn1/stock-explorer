"""M2 驗證腳本 — 確認所有新模組可正確載入"""
import ast
import sys

files = [
    'src/pages/__init__.py',
    'src/pages/_router_base.py',
    'src/pages/router.py',
    'src/pages/business_card.py',
    'src/pages/operation_checkup.py',
    'src/pages/financial_health.py',
    'src/pages/peer_comparison.py',
    'src/pages/group_structure.py',
    'src/main.py',
]

print('=== Syntax Check ===')
all_ok = True
for f in files:
    try:
        with open(f) as fh:
            ast.parse(fh.read())
        print(f'  OK: {f}')
    except SyntaxError as e:
        print(f'  FAIL: {f}: {e}')
        all_ok = False

if not all_ok:
    sys.exit(1)

print()
print('=== Import Check ===')
from src.pages._router_base import get_stock_data, _calc_extra_metrics, _find_financial_value
print('  OK: _router_base')

from src.pages.router import load_and_render_page
print('  OK: router')

from src.pages.business_card import _render_business_card
print('  OK: business_card')

from src.pages.operation_checkup import _render_operation_checkup
print('  OK: operation_checkup')

from src.pages.financial_health import _render_financial_health
print('  OK: financial_health')

from src.pages.peer_comparison import _render_peer_comparison, INDUSTRY_BENCHMARKS
print(f'  OK: peer_comparison ({len(INDUSTRY_BENCHMARKS)} industries)')

from src.pages.group_structure import _render_group_structure, KNOWN_GROUP_STRUCTURES
print(f'  OK: group_structure ({len(KNOWN_GROUP_STRUCTURES)} groups)')

print()
print('=== ALL M2 CHECKS PASSED ===')
