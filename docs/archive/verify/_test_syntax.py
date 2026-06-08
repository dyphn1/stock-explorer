import py_compile
import os
import sys

page_dir = os.path.join(os.path.dirname(__file__), "src", "pages")
page_files = [
    "router.py",
    "business_card.py",
    "operation_checkup.py",
    "financial_health.py",
    "peer_comparison.py",
    "group_structure.py",
    "__init__.py",
    "_router_base.py",
]

all_ok = True
for f in page_files:
    path = os.path.join(page_dir, f)
    try:
        py_compile.compile(path, doraise=True)
        print(f"  OK: {f}")
    except py_compile.PyCompileError as e:
        print(f"  FAIL: {f} - {e}")
        all_ok = False

if all_ok:
    print("\nAll page files compile successfully!")
else:
    print("\nSome files have syntax errors!")
    sys.exit(1)
