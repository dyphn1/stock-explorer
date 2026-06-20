import sys

def main():
    with open('src/main.py', 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # 1. Replace nav_items tuple lines (lines 225-234 inclusive, 0-index)
    new_tuples = [
        '        (\"📊\", t(\"main.sidebar.nav_home\"), \"sidebar_nav_home\"),\n',
        '        (\"🗺️\", t(\"main.sidebar.nav_sector\"), \"sidebar_nav_sector\"),\n',
        '        (\"📈\", t(\"main.sidebar.nav_category\"), \"sidebar_nav_category\"),\n',
        '        (\"🏷️\", t(\"main.sidebar.nav_etf\"), \"sidebar_nav_etf\"),\n',
        '        (\"📋\", t(\"main.sidebar.nav_watchlist\"), \"sidebar_nav_watchlist\"),\n',
        '        (\"🔔\", t(\"main.sidebar.nav_events\"), \"sidebar_nav_events\"),\n',
        '        (\"🔔\", t(\"main.sidebar.nav_notifications\"), \"sidebar_nav_notifications\"),\n',
        '        (\"📝\", t(\"main.sidebar.nav_memo\"), \"sidebar_nav_memo\"),\n',
        '        (\"💰\", t(\"main.sidebar.nav_wellness\"), \"sidebar_nav_wellness\"),\n',
        '        (\"🔎\", t(\"main.sidebar.nav_screener\"), \"sidebar_nav_screener\"),\n',
    ]
    lines[225:235] = new_tuples

    # 2. Replace expander labels
    for i, line in enumerate(lines):
        if line.strip() == '    with st.expander(\"🔥 熱門股票\", expanded=False):':
            lines[i] = '    with st.expander(f\"🔥 {t(\\\"main.sidebar.hot_stocks\\\")}\", expanded=False):\n'
        elif line.strip() == '    with st.expander(\"🏷️ 熱門 ETF\", expanded=False):':
            lines[i] = '    with st.expander(f\"🏷️ {t(\\\"main.sidebar.hot_etfs\\\")}\", expanded=False):\n'

    # 3. Replace disclaimer block
    for i, line in enumerate(lines):
        if line.strip().startswith('st.markdown(\"\"\"'):
            start = i
            for j in range(i, len(lines)):
                if '\"\"\", unsafe_allow_html=True' in lines[j]:
                    end = j
                    break
            lines[start:end+1] = ['    st.markdown(t(\"main.disclaimer\"), unsafe_allow_html=True)\n']
            break

    # 4. Replace search selectbox label
    for i, line in enumerate(lines):
        if 'st.sidebar.selectbox' in line and '找到多筆符合的股票：' in line:
            lines[i] = line.replace('\"找到多筆符合的股票：\"', 't(\"main.search.multiple_results\")')
            break

    # 5. Replace error message
    for i, line in enumerate(lines):
        if 'st.sidebar.error' in line and '找不到符合的股票' in line:
            lines[i] = line.replace('\"找不到符合的股票\"', 't(\"main.search.not_found\")')
            break

    # 6. Replace home page strings
    # We'll replace the welcome page block by finding the st.markdown for the welcome page.
    for i, line in enumerate(lines):
        if line.strip().startswith('st.markdown(\"\"\"') and '<div style=\"text-align:center;padding:4rem 2rem;\">' in line:
            start = i
            for j in range(i, len(lines)):
                if '\"\"\", unsafe_allow_html=True' in lines[j]:
                    end = j
                    break
            # Build new welcome block
            new_block = '''    st.markdown(\"\"\"\n    <div style=\"text-align:center;padding:4rem 2rem;\">\n        <h1>📊 {t(\"main.home.title\")}</h1>\n        <p style=\"font-size:1.3rem;color:#7F8C8D;margin-top:1rem;\">{t(\"main.home.lead1\")}</p>\n        <p style=\"font-size:1rem;color:#7F8C8D;margin-top:2rem;\">\n            {t(\"main.home.lead2\")}\n        </p>\n    </div>\n    \"\"\", unsafe_allow_html=True)\n'''
            lines[start:end+1] = [new_block]
            break

    with open('src/main.py', 'w') as f:
        f.write(''.join(lines))

if __name__ == '__main__':
    main()