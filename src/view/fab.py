import streamlit as st


def render_fab(stock_id: str, menu_items: list[dict]):
    if not menu_items:
        return
    menu_html = ""
    for i, item in enumerate(menu_items):
        if item.get("divider"):
            menu_html += '<div class="fab-divider" role="separator"></div>'
        else:
            href = item["href"].format(stock_id=stock_id)
            label = item["label"]
            menu_html += f'<a class="fab-menu-item" href="{href}" role="menuitem">{item["icon"]} {label}</a>'

    st.html(f"""
<style>
:root {{
  --fab-bg: #007AFF;
  --fab-shadow: rgba(0,122,255,0.3);
  --fab-hover-shadow: rgba(0,122,255,0.4);
  --fab-menu-bg: #FFFFFF;
  --fab-menu-shadow: rgba(0,0,0,0.15);
  --fab-text: #1C1C1E;
  --fab-hover-bg: #F2F2F7;
  --fab-divider: #E5E5EA;
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    --fab-bg: #0A84FF;
    --fab-shadow: rgba(10,132,255,0.3);
    --fab-hover-shadow: rgba(10,132,255,0.4);
    --fab-menu-bg: #1C1C1E;
    --fab-menu-shadow: rgba(0,0,0,0.4);
    --fab-text: #F2F2F7;
    --fab-hover-bg: #2C2C2E;
    --fab-divider: #38383A;
  }}
}}

.fab-container {{
  position: fixed; bottom: 24px; right: 24px; z-index: 999;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}}

.fab-button {{
  width: 56px; height: 56px; border-radius: 50%; background: var(--fab-bg);
  color: white; border: none; box-shadow: 0 4px 16px var(--fab-shadow);
  font-size: 28px; cursor: pointer; display: flex; align-items: center;
  justify-content: center; transition: transform 0.2s ease, box-shadow 0.2s ease;
  line-height: 1; outline: none;
}}
.fab-button:hover {{ transform: scale(1.08); box-shadow: 0 6px 20px var(--fab-hover-shadow); }}
.fab-button:active {{ transform: scale(0.95); }}
.fab-button:focus-visible {{ outline: 3px solid var(--fab-bg); outline-offset: 3px; }}

.fab-menu {{
  display: none; position: absolute; bottom: 70px; right: 0;
  background: var(--fab-menu-bg); border-radius: 16px;
  box-shadow: 0 8px 30px var(--fab-menu-shadow);
  padding: 6px; min-width: 210px; max-height: 60vh; overflow-y: auto;
  opacity: 0; transform: translateY(10px) scale(0.95);
  transition: opacity 0.15s ease, transform 0.15s ease;
}}
.fab-menu.show {{
  display: block; opacity: 1; transform: translateY(0) scale(1);
}}

.fab-menu-item {{
  padding: 10px 16px; cursor: pointer; border-radius: 10px; font-size: 14px;
  color: var(--fab-text); display: flex; align-items: center; gap: 10px;
  text-decoration: none; transition: background 0.15s; outline: none;
}}
.fab-menu-item:hover {{ background: var(--fab-hover-bg); text-decoration: none; color: var(--fab-text); }}
.fab-menu-item:focus-visible {{ outline: 2px solid var(--fab-bg); outline-offset: -2px; }}

.fab-divider {{ height: 1px; background: var(--fab-divider); margin: 4px 12px; }}

.fab-overlay {{
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 998;
}}
.fab-overlay.show {{ display: block; }}

@media (max-width: 480px) {{
  .fab-container {{ bottom: 16px; right: 16px; }}
  .fab-button {{ width: 48px; height: 48px; font-size: 24px; }}
  .fab-menu {{ min-width: 180px; right: 0; bottom: 60px; }}
}}
</style>
<div class="fab-overlay" id="fabOverlay" onclick="closeFabMenu()" role="presentation"></div>
<div class="fab-container">
  <div class="fab-menu" id="fabMenu" role="menu" aria-label="Page navigation">
    {menu_html}
  </div>
  <button class="fab-button" id="fabBtn" onclick="toggleFabMenu()" aria-label="Open page navigation menu" aria-expanded="false">+</button>
</div>
<script>
function toggleFabMenu(){{
  var m=document.getElementById('fabMenu'),o=document.getElementById('fabOverlay'),b=document.getElementById('fabBtn');
  var isOpen=m.classList.contains('show');
  m.classList.toggle('show');o.classList.toggle('show');
  b.textContent=isOpen?'+':'×';
  b.setAttribute('aria-label', isOpen?'Open page navigation menu':'Close page navigation menu');
  b.setAttribute('aria-expanded', String(!isOpen));
}}
function closeFabMenu(){{
  var m=document.getElementById('fabMenu'),o=document.getElementById('fabOverlay'),b=document.getElementById('fabBtn');
  m.classList.remove('show');o.classList.remove('show');
  b.textContent='+';
  b.setAttribute('aria-label','Open page navigation menu');
  b.setAttribute('aria-expanded','false');
}}
document.addEventListener('keydown',function(e){{
  if(e.key==='Escape'){{closeFabMenu();}}
}});
</script>
""")
