"""Fix sys.path in all page modules so 'src' is importable when run as Streamlit pages."""
import os
import re

PAGES_DIR = "/Users/daniel.chang/Desktop/GitHub/stock-explorer/src/pages"
PATH_FIX_LINES = [
    "import sys as _sys",
    "import os as _os",
    "_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))))",
    "",
]

for fname in sorted(os.listdir(PAGES_DIR)):
    if not fname.endswith(".py") or fname == "__init__.py":
        continue
    fpath = os.path.join(PAGES_DIR, fname)
    with open(fpath, "r") as f:
        content = f.read()

    # Skip if already fixed
    if "_sys.path.insert" in content:
        print(f"  SKIP {fname} (already fixed)")
        continue

    # Find the position after the docstring closing """
    match = re.match(r'(""".*?"""|\'\'\'.*?\'\'\')\s*\n', content, re.DOTALL)
    if match:
        insert_pos = match.end()
        new_content = content[:insert_pos] + "\n" + "\n".join(PATH_FIX_LINES) + "\n" + content[insert_pos:]
        with open(fpath, "w") as f:
            f.write(new_content)
        print(f"  FIXED {fname}")
    else:
        print(f"  WARN {fname}: no docstring found, skipping")

print("Done!")
