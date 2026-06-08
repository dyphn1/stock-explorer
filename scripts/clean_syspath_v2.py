import re
import sys

files = sys.argv[1:]

for fpath in files:
    with open(fpath) as f:
        content = f.read()
    
    old_content = content
    
    # Remove the sys.path insertion blocks with varying formats
    patterns = [
        # main.py style (2 dirname levels)
        r'\nimport sys as _sys\nimport os as _os\n_sys\.path\.insert\(0, _os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.abspath\(__file__\)\)\)\)\n',
        # pages style (3 dirname levels)
        r'\nimport sys as _sys\nimport os as _os\n_sys\.path\.insert\(0, _os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.abspath\(__file__\)\)\)\)\)\n',
        # With leading newlines
        r'\n+import sys as _sys\nimport os as _os\n_sys\.path\.insert\(_?0, _os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.abspath\(__file__\)\)\)\)\)\n+',
        r'\n+import sys as _sys\nimport os as _os\n_sys\.path\.insert\(_?0, _os\.path\.dirname\(_os\.path\.dirname\(_os\.path\.abspath\(__file__\)\)\)\n+',
    ]
    
    for pat in patterns:
        content = re.sub(pat, '\n', content)
    
    # Clean up triple blank lines
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != old_content:
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"Cleaned: {fpath}")
    else:
        print(f"No change: {fpath}")
