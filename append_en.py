import sys

def append_main_section(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Ensure content ends with newline
    if not content.endswith('\n'):
        content += '\n'
    
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
    new_content = content + addition
    with open(filepath, 'w') as f:
        f.write(new_content)

if __name__ == '__main__':
    append_main_section('/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales/en.yaml')
    print('Appended to en.yaml')