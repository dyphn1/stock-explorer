import streamlit as st


def render_fab(stock_id: str, menu_items: list[dict]):
    if not menu_items:
        return
    menu_html = ""
    for i, item in enumerate(menu_items):
        if item.get("divider"):
            menu_html += '<div class="fab-divider"></div>'
        else:
            href = item["href"].format(stock_id=stock_id)
            menu_html += f'<a class="fab-menu-item" href="{href}">{item["icon"]} {item["label"]}</a>'

    st.html(f"""
<style>
.fab-container {{
  position: fixed; bottom: 24px; right: 24px; z-index: 999;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}}
.fab-button {{
  width: 56px; height: 56px; border-radius: 50%; background: #007AFF;
  color: white; border: none; box-shadow: 0 4px 16px rgba(0,122,255,0.3);
  font-size: 28px; cursor: pointer; display: flex; align-items: center;
  justify-content: center; transition: transform 0.2s, box-shadow 0.2s; line-height: 1;
}}
.fab-button:hover {{ transform: scale(1.08); box-shadow: 0 6px 20px rgba(0,122,255,0.4); }}
.fab-button:active {{ transform: scale(0.95); }}
.fab-menu {{
  display: none; position: absolute; bottom: 70px; right: 0;
  background: white; border-radius: 16px; box-shadow: 0 8px 30px rgba(0,0,0,0.15);
  padding: 6px; min-width: 210px; max-height: 60vh; overflow-y: auto;
}}
.fab-menu.show {{ display: block; }}
.fab-menu-item {{
  padding: 10px 16px; cursor: pointer; border-radius: 10px; font-size: 14px;
  color: #1C1C1E; display: flex; align-items: center; gap: 10px;
  text-decoration: none; transition: background 0.15s;
}}
.fab-menu-item:hover {{ background: #F2F2F7; text-decoration: none; color: #1C1C1E; }}
.fab-divider {{ height: 1px; background: #E5E5EA; margin: 4px 12px; }}
.fab-overlay {{
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 998;
}}
.fab-overlay.show {{ display: block; }}
</style>
<div class="fab-overlay" id="fabOverlay" onclick="closeFabMenu()"></div>
<div class="fab-container">
  <div class="fab-menu" id="fabMenu">
    {menu_html}
  </div>
  <button class="fab-button" id="fabBtn" onclick="toggleFabMenu()">+</button>
</div>
<script>
function toggleFabMenu(){{
  var m=document.getElementById('fabMenu'),o=document.getElementById('fabOverlay'),b=document.getElementById('fabBtn');
  var isOpen=m.classList.contains('show');
  m.classList.toggle('show');o.classList.toggle('show');
  b.textContent=isOpen?'+':'×';
}}
function closeFabMenu(){{
  document.getElementById('fabMenu').classList.remove('show');
  document.getElementById('fabOverlay').classList.remove('show');
  document.getElementById('fabBtn').textContent='+';
}}
</script>
""")
