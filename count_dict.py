import ast
import sys

# We'll parse the file and find the ETF_CATEGORY_KEYWORDS dictionary
with open('src/pages/etf_browser.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We'll use a simple approach: find the dictionary and then evaluate it? But it contains t() calls.
# Instead, we can extract the dictionary string and then count the strings in the lists.
# Since the dictionary values are lists of strings, and the keys are t() calls, we can ignore the keys.

# Let's use regex to extract the dictionary content between the curly braces.
# We know the dictionary starts at line 180 and ends at line 211, but let's do it programmatically.

# Find the line that starts with "ETF_CATEGORY_KEYWORDS = {"
lines = content.split('\n')
start_line = None
for i, line in enumerate(lines):
    if line.strip().startswith('ETF_CATEGORY_KEYWORDS = {'):
        start_line = i
        break

if start_line is None:
    print("Dictionary not found")
    sys.exit(1)

# Now, we need to find the matching closing brace.
# We'll keep a count of braces.
brace_count = 0
end_line = None
for i in range(start_line, len(lines)):
    line = lines[i]
    brace_count += line.count('{')
    brace_count -= line.count('}')
    if brace_count == 0 and i > start_line:
        end_line = i
        break

if end_line is None:
    print("Could not find end of dictionary")
    sys.exit(1)

# Extract the dictionary lines
dict_lines = lines[start_line:end_line+1]
dict_content = '\n'.join(dict_lines)

# Now, we want to extract the lists of strings that are the values.
# We can use regex to find all the lists: [ ... ]
# But note: the dictionary values are the lists.
# We'll look for patterns like: [ ... ] inside the dictionary.

# Since the dictionary is not too big, we can use ast.literal_eval if we replace the t() calls with placeholders.
# However, the t() calls are in the keys, and we don't care about the keys for counting strings.

# Let's remove the keys and keep only the values.
# We can split by ',' at the top level? It's complex.

# Instead, let's just count the strings in the values by looking for quoted strings inside the dictionary.
# We'll ignore the keys (which are t() calls) and only look at the values.

# We'll use a simple state machine: we are in a value when we see a '=' and then a '[' until the matching ']'.

# But given the time, let's just count all quoted strings in the dictionary and then subtract the ones in the keys?
# The keys are t() calls, which have strings inside them. We don't want to count those.

# Let's do: find all quoted strings in the dictionary, then subtract the ones that are inside t() calls.

# We'll use regex to find all quoted strings.
import re
pattern = r'''(?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')'''
matches = re.findall(pattern, dict_content)

# Now, we need to exclude the strings that are inside t() calls.
# We can check for each match if it is inside a t('...') or t("...") in the dictionary content.
# We'll create a set of strings that are inside t() calls.
t_strings = set()
# Find all t(...) calls in the dictionary content.
t_pattern = r'''t\((?:\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')\)'''
t_matches = re.findall(t_pattern, dict_content)
for t_match in t_matches:
    # Extract the inner string
    inner = t_match[2:-1]  # remove t( and )
    if inner.startswith('\"') and inner.endswith('\"'):
        inner = inner[1:-1]
    elif inner.startswith(\"'\") and inner.endswith(\"'\"):
        inner = inner[1:-1]
    t_strings.add(inner)

# Now, the strings in matches that are not in t_strings are the ones in the values.
value_strings = []
for match in matches:
    inner = match[1:-1]
    if inner not in t_strings:
        value_strings.append(inner)

print(f"Number of strings in the dictionary values: {len(value_strings)}")
print("Strings:")
for s in value_strings:
    print(f"  {s}")
