import re
import ast

def replace_t(match):
    return "'KEY'"

with open('src/pages/etf_browser.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Extract lines 180 to 211 (1-indexed, so index 179 to 211 inclusive)
dict_lines = lines[179:212]  # indices 179 to 211 inclusive

# Join the lines
dict_str = ''.join(dict_lines)

# Replace t('...') and t("...") with 'KEY'
pattern = r'''t\((?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')\)'''
dict_str = re.sub(pattern, replace_t, dict_str)

# Now, extract the dictionary part after the equals sign
if '=' in dict_str:
    dict_part = dict_str.split('=', 1)[1].strip()
else:
    dict_part = dict_str

# Parse the dictionary
try:
    dictionary = ast.literal_eval(dict_part)
    total_strings = 0
    for key, value in dictionary.items():
        if isinstance(value, list):
            total_strings += len(value)
    print(f"Total strings in dictionary values: {total_strings}")
except Exception as e:
    print(f"Error parsing dictionary: {e}")
    print("Dictionary string:")
    print(dict_str)