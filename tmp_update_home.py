import sys

def main():
    with open('src/main.py', 'r') as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # Fix home page block (welcome page)
    for i, line in enumerate(lines):
        if line.strip().startswith('st.markdown(\"\"\"'):
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