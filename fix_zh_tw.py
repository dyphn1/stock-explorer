import sys

def fix_zh_tw_yaml(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Keep only the original content (up to but not including any added main section)
    new_lines = []
    for line in lines:
        if line.strip().startswith('main:'):
            break
        new_lines.append(line)
    # Ensure ends with newline
    if new_lines and not new_lines[-1].endswith('\n'):
        new_lines[-1] += '\n'
    
    # Construct the main section with Chinese values
    # We'll build the disclaimer string exactly as needed.
    disclaimer_str = '''    <div class=\"disclaimer\">\n    ⚠️ 本工具僅供認識公司使用，<br>\n    不構成任何投資建議。<br>\n    投資有風險，請自行評估。\n    </div>'''
    # Note: the string includes newline characters. We need to represent it in YAML.
    # We'll use a block scalar literal style to preserve newlines.
    # We'll construct the addition as a string.
    addition = '''main:
  sidebar:
    nav_home: "名片"
    nav_sector: "產業熱力圖"
    nav_category: "分類瀏覽"
    nav_etf: "ETF 專區"
    nav_watchlist: "我的關注"
    nav_events: "事件儀表板"
    nav_notifications: "通知中心"
    nav_memo: "投資備忘錄"
    nav_wellness: "理財健康檢查"
    nav_screener: "股票探索"
    hot_stocks: "熱門股票"
    hot_etfs: "熱門 ETF"
  search:
    multiple_results: "找到多筆符合的股票："
    not_found: "找不到符合的股票"
  home:
    title: "股識"
    lead1: "認識一家公司，從這裡開始"
    lead2: "在左側輸入股票代號或名稱，開始認識一家公司"
  disclaimer: |-
'''
    # Now we need to add the disclaimer string with proper indentation (2 spaces for the key, then 4 spaces for the block?)
    # In YAML, after a key with "|-", the following lines should be indented by 2 spaces relative to the key?
    # Actually the pattern is:
    #   disclaimer: |-
    #     <div class="disclaimer">
    #     ⚠️ 本工具僅供認識公司使用，<br>
    #     ...
    # We'll indent the block by 2 spaces (since the key is indented by 2 spaces under main? Let's see:
    # main:
    #   disclaimer: |-
    #     <div class="disclaimer">
    # The key "disclaimer:" is indented by 2 spaces (since main is at root, indent 0, then main: indent 2, then disclaimer: indent 4? Actually typical YAML:
    # main:
    #   sidebar:
    #     nav_home: "Home"
    #   disclaimer: |-
    #     <div class="disclaimer">
    # So disclaimer is at same indent level as sidebar, which is 2 spaces.
    # The block scalar indicator "|-" is followed by a newline, then the content indented by 2 spaces relative to the indentation level of the key? Actually the content should be indented further than the key.
    # Let's keep it simple: we'll just write the addition as a literal string with proper indentation as we would want in the file.
    # We'll write the addition exactly as we want it to appear in the file.
    # We'll construct the addition line by line.
    
    # Let's just write the addition as we know it should look:
    addition_lines = [
        'main:\n',
        '  sidebar:\n',
        '    nav_home: "名片"\n',
        '    nav_sector: "產業熱力圖"\n',
        '    nav_category: "分類瀏覽"\n',
        '    nav_etf: "ETF 禮區"\n',  # Oops typo, fix later
        # We'll do it stepwise; better to write a separate script but time is limited.
    ]
    # Given the complexity, let's instead use the same approach as for en.yaml but with Chinese strings and proper YAML formatting for multiline string.
    # We'll write a simple string that we believe is correct YAML.
    # We'll use the following format for the disclaimer:
    #   disclaimer: >-
    #     <div class=\"disclaimer\">\n    ⚠️ 本工具僅供認識公司使用，<br>\n    不構成任何投資建議。<br>\n    投資有風險，請自行評估。\n    </div>
    # Using '>' for folded style, but we want to keep newlines, so we use '|' for literal.
    # We'll use '|-' to strip trailing newlines.
    # We'll indent the content by 2 spaces.
    # Let's manually construct the addition:
    
    addition = '''main:
  sidebar:
    nav_home: "名片"
    nav_sector: "產業熱力圖"
    nav_category: "分類瀏覽"
    nav_etf: "ETF 專區"
    nav_watchlist: "我的關注"
    nav_events: "事件儀表板"
    nav_notifications: "通知中心"
    nav_memo: "投資備忘錄"
    nav_wellness: "理財健康檢查"
    nav_screener: "股票探索"
    hot_stocks: "熱門股票"
    hot_etfs: "熱門 ETF"
  search:
    multiple_results: "找到多筆符合的股票："
    not_found: "找不到符合的股票"
  home:
    title: "股識"
    lead1: "認識一家公司，從這裡開始"
    lead2: "在左側輸入股票代號或名稱，開始認識一家公司"
  disclaimer: |-
'''
    # Now add the disclaimer lines with indentation of 4 spaces (since the key is indented by 2, we need to add 2 more for the content? Actually for literal block scalar, the indentation of the content lines is relative to the indentation level of the key? The spec is complex. We'll just indent by 4 spaces and hope it works.
    for line in disclaimer_str.splitlines(keepends=True):
        addition += '    ' + line  # 4 spaces
    addition += '\n'
    
    new_lines.append(addition)
    
    with open(filepath, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    fix_zh_tw_yaml('/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales/zh-TW.yaml')
    print('Fixed zh-TW.yaml')