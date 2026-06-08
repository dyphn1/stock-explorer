import sys
import os

files = sys.argv[1:]

# The sys.path hack needed for direct python execution (playwright test)
# src.main.py needs 2 dirname levels, pages need 3
main_hack = """import sys as _sys
import os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
"""

page_hack = """import sys as _sys
import os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))))
"""

for fpath in files:
    with open(fpath) as f:
        content = f.read()
    
    hack = main_hack if fpath == "src/main.py" else page_hack
    
    # Insert hack after the module docstring closing triple quote
    # Find the closing triple quote
    lines = content.split('\n')
    insert_idx = None
    docstring_end = None
    
    # Find end of module docstring
    in_docstring = False
    for i, line in enumerate(lines):
        if line.startswith('\"\"\"') and not in_docstring:
            in_docstring = True
            docstring_end = i
        elif in_docstring and '\"\"\"' in line and i > docstring_end:
            insert_idx = i + 1
            break
    
    if insert_idx and '_sys.path.insert' not in content:
        lines.insert(insert_idx, '')
        lines.insert(insert_idx + 1, hack.rstrip())
        new_content = '\n'.join(lines)
        with open(fpath, 'w') as f:
            f.write(new_content)
        print(f"Restored: {fpath}")
    elif '_sys.path.insert' in content:
        print(f"Already present: {fpath}")
    else:
        print(f"Could not find docstring end: {fpath}")
