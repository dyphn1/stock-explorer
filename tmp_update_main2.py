import sys

def main():
    with open('src/main.py', 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # 1. Fix expander labels
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('with st.expander(') and '🔥 熱門股票' in stripped:
            # Replace the line
            # Keep the original indentation (leading spaces)
            indent = len(line) - len(line.lstrip())
            lines[i] = line[:indent] + 'with st.expander(f\"🔥 {t(\\\"main.sidebar.hot_stocks\\\")}\", expanded=False):\n'
        elif stripped.startswith('with st.expander(') and '🏷️ 熱門 ETF' in stripped:
            indent = len(line) - len(line.lstrip())
            lines[i] = line[:indent] + 'with st.expander(f\"🏷️ {t(\\\"main.sidebar.hot_etfs\\\")}\", expanded=False):\n'

    # 2. Fix disclaimer block
    for i, line in enumerate(lines):
        if line.strip().startswith('st.markdown(\"\"\"'):
            start = i
            for j in range(i, len(lines)):
                if '\"\"\", unsafe_allow_html=True' in lines[j]:
                    end = j
                    break
            # Replace the block
            lines[start:end+1] = ['    st.markdown(t(\"main.disclaimer\"), unsafe_allow_html=True)\n']
            break

    # 3. Fix home page block (welcome page)
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