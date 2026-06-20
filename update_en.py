import sys

def update_yaml(filepath, new_section_dict, lang):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Ensure file ends with newline
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'
    
    # Convert dict to YAML lines at the top level
    # We'll just dump as simple key-value under a top-level key 'main'
    # Since the existing file has top-level keys screener and delta, we'll add main after them.
    # We'll generate YAML lines for the new section.
    import yaml
    # But we don't have yaml installed? We can dump manually.
    # We'll do a simple manual construction for our known structure.
    # We'll add a blank line then 'main:' then indent each subkey.
    new_lines = []
    new_lines.append('\n')
    new_lines.append('main:\n')
    # Process the dict recursively
    def dict_to_yaml_lines(d, indent):
        lines = []
        for key, value in d.items():
            if isinstance(value, dict):
                lines.append(' ' * indent + f'{key}:\n')
                lines.extend(dict_to_yaml_lines(value, indent+2))
            else:
                # For string values, we need to escape newlines and special chars? We'll just quote if needed.
                # For simplicity, we'll represent the string as is, and if it contains newline, we'll use block scalar.
                if '\n' in value:
                    # Use block scalar literal style
                    lines.append(' ' * indent + f'{key}: |\\n')
                    for line in value.splitlines(keepends=True):
                        lines.append(' ' * (indent+2) + line)
                else:
                    # If string contains special YAML characters, we'll quote.
                    # We'll just always quote with double quotes and escape existing quotes.
                    # Replace double quotes with \\\" and backslashes with \\\\.
                    escaped = value.replace('\\', '\\\\').replace('\"', '\\\"')
                    lines.append(' ' * indent + f'{key}: \"{escaped}\"\\n')
        return lines
    
    new_lines.extend(dict_to_yaml_lines(new_section_dict, 2))
    
    with open(filepath, 'w') as f:
        f.writelines(lines + new_lines)

if __name__ == '__main__':
    # Define the new section for English
    new_section = {
        'sidebar': {
            'nav_home': 'Home',
            'nav_sector': 'Sector Heatmap',
            'nav_category': 'Category Browse',
            'nav_etf': 'ETF Zone',
            'nav_watchlist': 'Watchlist',
            'nav_events': 'Events Dashboard',
            'nav_notifications': 'Notifications',
            'nav_memo': 'Investment Memo',
            'nav_wellness': 'Financial Wellness Check',
            'nav_screener': 'Stock Screener',
            'hot_stocks': 'Hot Stocks',
            'hot_etfs': 'Hot ETFs'
        },
        'search': {
            'multiple_results': 'Multiple matching stocks found:',
            'not_found': 'No matching stocks found'
        },
        'home': {
            'title': 'Stock Explorer',
            'lead1': 'Get to know a company, start here',
            'lead2': 'Enter a stock code or name in the left sidebar to begin getting to know a company'
        },
        'disclaimer': '⚠️ This tool is for company education only,<br>does not constitute any investment advice.<br>Investing involves risk, please assess on your own.'
    }
    update_yaml('/Users/daniel.chang/Desktop/GitHub/stock-explorer/locales/en.yaml', new_section, 'en')
    print('Updated en.yaml')