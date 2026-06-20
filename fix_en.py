import sys

def fix_en_yaml(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Keep only the first 46 lines (original content)
    # Actually we need to keep until the line before the first malformed main section.
    # Let's find the line that starts with 'main:' (the first occurrence)
    # and discard from there.
    # But we know the original ended at line 46 (previous_year_same_period).
    # We'll just keep lines up to index 45 (0-index) inclusive? Let's compute.
    # We'll read the file and find the index of the line that starts with 'main:' (the malformed one).
    # There may be two 'main:' lines now.
    # We'll keep everything before the first 'main:' line.
    new_lines = []
    for line in lines:
        if line.strip().startswith('main:'):
            break
        new_lines.append(line)
    # Now new_lines contains the original content up to but not including the first main line.
    # Ensure it ends with newline.
    if new_lines and not new_lines[-1].endswith('\n'):
        new_lines[-1] += '\n'
    
    # Append the correct main section
    addition = '''main:
  sidebar:
    nav_home: "Home"
    nav_sector: "Sector Heatmap"
    nav_category: "Category Browse"
    nav_etf: "ETF Zone"
    nav_watchlist: "Watchlist"
    nav_events: "Events Dashboard"
    nav_notifications: "Notifications"
    nav_memo: "Investment Memo"
    nav_wellness: "Financial Wellness Check"
    nav_screener: "Stock Screener"
    hot_stocks: "Hot Stocks"
    hot_etfs: "Hot ETFs"
  search:
    multiple_results: "Multiple matching stocks found:"
    not_found: "No matching stocks found"
  home:
    title: "Stock Explorer"
    lead1: "Get to know a company, start here"
    lead2: "Enter a stock code or name in the left sidebar to begin getting to know a company"
  disclaimer: "⚠️ This tool is for company education only,<br>does not constitute any investment advice.<br>Investing involves risk, please assess on your own."
'''
    new_lines.append(addition)
    
    with open(filepath, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    fix_en_yaml('/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales/en.yaml')
    print('Fixed en.yaml')