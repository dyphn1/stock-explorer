import re
import sys

def find_chinese_strings(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Patterns to ignore: comments and docstrings
    # We'll keep track of whether we are inside a triple quoted string
    in_docstring = False
    docstring_quote = None
    
    # We'll also skip the ETF_CATEGORY_KEYWORDS dictionary (lines 180-211)
    # Note: line numbers are 1-indexed
    skip_start = 180
    skip_end = 211
    
    for i, line in enumerate(lines, start=1):
        # Skip lines in the ETF_CATEGORY_KEYWORDS dictionary
        if skip_start <= i <= skip_end:
            continue
        
        # Remove trailing newline
        original_line = line.rstrip()
        line_stripped = original_line.strip()
        
        # Skip empty lines
        if not line_stripped:
            continue
            
        # Handle docstrings
        if not in_docstring:
            # Check for start of docstring
            if line_stripped.startswith('\"\"\"') or line_stripped.startswith("'''"):
                in_docstring = True
                docstring_quote = line_stripped[:3]
                # Check if it ends on the same line
                if line_stripped.count(docstring_quote) >= 2:
                    in_docstring = False
                    docstring_quote = None
                continue
        else:
            # We are inside a docstring
            if docstring_quote in line:
                # Check if it ends on this line
                parts = line.split(docstring_quote)
                if len(parts) >= 2:
                    in_docstring = False
                    docstring_quote = None
            continue
        
        # Skip comments
        if line_stripped.startswith('#'):
            continue
        
        # Now, we are in code. Look for string literals that contain Chinese and are not inside t() calls.
        # We'll look for both single and double quoted strings.
        # This regex matches a string literal (single or double quoted) that does not contain escaped quotes of the same type.
        # It's not perfect but works for simple cases.
        pattern = r'''(?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')'''
        matches = re.findall(pattern, line)
        for match in matches:
            # Check if the string contains Chinese characters
            if re.search(r'[\u4e00-\u9fff]', match):
                # Check if this string is inside a t() call on the same line
                # We'll look for t('...') or t("...") that contains this string.
                # If the string is the argument of t, then we skip.
                # We'll check if the string is preceded by t( and the opening quote is after t( and the closing quote is before the closing )
                # This is getting complex. Let's do a simple check: if the line contains t(' followed by the string without quotes or t(\" followed by the string without quotes.
                # Remove the quotes from the match
                inner = match[1:-1]  # remove the first and last character (the quotes)
                # Check for t('inner') or t("inner")
                if re.search(r't\(\'.*' + re.escape(inner) + r'\'\)', line) or re.search(r't\(\".*' + re.escape(inner) + r'\"\)', line):
                    continue
                # Also check for t( inner ) with spaces? We'll assume the string is exactly the argument.
                # If we didn't skip, then we found a hardcoded Chinese string that is not in t()
                print(f"Line {i}: {original_line}")
                print(f"  Found string: {match}")
                print()

if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'src/pages/etf_browser.py'
    find_chinese_strings(filename)
