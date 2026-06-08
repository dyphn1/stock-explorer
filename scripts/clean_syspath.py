import re
import sys

files = sys.argv[1:]

for fpath in files:
    with open(fpath) as f:
        content = f.read()
    
    old_content = content
    
    # Remove the sys.path insertion block that was added after module docstring
    content = re.sub(
        r'\n+import sys as _sys\nimport os as _os\n_sys\.path\.insert\(_?0, _os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.abspath\(__file__\)\)\)\)\)',
        '',
        content
    )
    
    if content != old_content:
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"Cleaned: {fpath}")
    else:
        print(f"No change: {fpath}")
