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
  --fab-bg: rgba(120,120,128,0.25);
  --fab-bg-hover: rgba(120,120,128,0.35);
  --fab-bg-active: rgba(120,120,128,0.45);
  --fab-border: rgba(120,120,128,0.3);
  --fab-icon: #555;
  --fab-shadow: rgba(0,0,0,0.12);
  --fab-menu-bg: #FFFFFF;
  --fab-menu-shadow: rgba(0,0,0,0.15);
  --fab-text: #1C1C1E;
  --fab-hover-bg: #F2F2F7;
  --fab-divider: #E5E5EA;
}}

@media (prefers-color-scheme: dark) {{
  :root {{
    --fab-bg: rgba(120,120,128,0.3);
    --fab-bg-hover: rgba(120,120,128,0.4);
    --fab-bg-active: rgba(120,120,128,0.5);
    --fab-border: rgba(120,120,128,0.4);
    --fab-icon: #ccc;
    --fab-shadow: rgba(0,0,0,0.3);
    --fab-menu-bg: #1C1C1E;
    --fab-menu-shadow: rgba(0,0,0,0.4);
    --fab-text: #F2F2F7;
    --fab-hover-bg: #2C2C2E;
    --fab-divider: #38383A;
  }}
}}

/* ── Floating button (Apple Assistive Touch-style) ── */
#fabBtn {{
  position: fixed;
  z-index: 999;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: var(--fab-bg);
  border: 1px solid var(--fab-border);
  box-shadow: 0 2px 8px var(--fab-shadow);
  color: var(--fab-icon);
  font-size: 22px;
  cursor: grab;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: background 0.2s ease, transform 0.1s ease;
  user-select: none;
  -webkit-user-select: none;
  touch-action: none;
  outline: none;
  line-height: 1;
}}
#fabBtn:hover {{ background: var(--fab-bg-hover); }}
#fabBtn:active {{ cursor: grabbing; transform: scale(1.08); }}
#fabBtn.dragging {{ cursor: grabbing; transform: scale(1.12); background: var(--fab-bg-active); transition: none; }}
#fabBtn.open {{ background: var(--fab-bg-active); }}

/* ── Menu ── */
.fab-menu-container {{
  position: fixed;
  z-index: 998;
  display: none;
}}
.fab-menu-container.show {{ display: block; }}
#fabMenu {{
  background: var(--fab-menu-bg);
  border-radius: 16px;
  box-shadow: 0 8px 30px var(--fab-menu-shadow);
  padding: 6px;
  min-width: 210px;
  max-height: 60vh;
  overflow-y: auto;
  opacity: 0;
  transform: translateY(10px) scale(0.95);
  transition: opacity 0.15s ease, transform 0.15s ease;
}}
#fabMenu.show {{
  opacity: 1;
  transform: translateY(0) scale(1);
}}

.fab-menu-item {{
  padding: 10px 16px;
  cursor: pointer;
  border-radius: 10px;
  font-size: 14px;
  color: var(--fab-text);
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  transition: background 0.15s;
  outline: none;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
}}
.fab-menu-item:hover {{ background: var(--fab-hover-bg); text-decoration: none; color: var(--fab-text); }}
.fab-menu-item:focus-visible {{ outline: 2px solid #007AFF; outline-offset: -2px; }}

.fab-divider {{ height: 1px; background: var(--fab-divider); margin: 4px 12px; }}

#fabOverlay {{
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 997;
}}
#fabOverlay.show {{ display: block; }}

@media (max-width: 480px) {{
  #fabBtn {{ width: 44px; height: 44px; font-size: 18px; }}
  #fabMenu {{ min-width: 180px; }}
}}
</style>

<div id="fabOverlay" onclick="closeFabMenu()" role="presentation"></div>
<div class="fab-menu-container" id="fabMenuContainer">
  <div id="fabMenu" role="menu" aria-label="Page navigation">
    {menu_html}
  </div>
</div>
<button id="fabBtn" aria-label="Menu">⊞</button>

<script>
(function(){{
var btn = document.getElementById('fabBtn');
var menu = document.getElementById('fabMenu');
var overlay = document.getElementById('fabOverlay');
var menuContainer = document.getElementById('fabMenuContainer');

var STORAGE_KEY = 'fab_position';
var DEFAULT_X = window.innerWidth - 80;
var DEFAULT_Y = window.innerHeight - 100;
var isDragging = false;
var isOpen = false;
var startX, startY, origX, origY;
var dragThreshold = 5;

function getSidebarWidth() {{
  var s = document.querySelector('section[data-testid="stSidebar"]');
  return s ? s.offsetWidth : 0;
}}

function clampPos(x, y) {{
  var sw = getSidebarWidth();
  var bw = btn.offsetWidth || 50;
  var bh = btn.offsetHeight || 50;
  var maxX = window.innerWidth - bw - 8;
  var minX = sw + 8;
  var minY = 60;
  var maxY = window.innerHeight - bh - 20;
  return {{
    x: Math.max(minX, Math.min(maxX, x)),
    y: Math.max(minY, Math.min(maxY, y))
  }};
}}

function loadPos() {{
  try {{
    var saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {{
      var p = JSON.parse(saved);
      return clampPos(p.x, p.y);
    }}
  }} catch(e) {{}}
  return clampPos(DEFAULT_X, DEFAULT_Y);
}}

function savePos(x, y) {{
  try {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify({{x:x, y:y}}));
  }} catch(e) {{}}
}}

function setPos(x, y) {{
  btn.style.left = x + 'px';
  btn.style.top = y + 'px';
  btn.style.right = 'auto';
  btn.style.bottom = 'auto';
}}

function positionMenu() {{
  var bx = parseInt(btn.style.left) || DEFAULT_X;
  var by = parseInt(btn.style.top) || DEFAULT_Y;
  var mw = 210;
  var mh = menu.scrollHeight || 300;
  var mx = bx + 25 - mw/2;
  var my = by - mh - 12;
  if (my < 8) my = by + 56;
  if (mx < 8) mx = 8;
  if (mx + mw > window.innerWidth - 8) mx = window.innerWidth - mw - 8;
  menuContainer.style.left = mx + 'px';
  menuContainer.style.top = my + 'px';
}}

function toggleFabMenu(e) {{
  if (e) {{ e.stopPropagation(); }}
  isOpen = !isOpen;
  menu.classList.toggle('show', isOpen);
  overlay.classList.toggle('show', isOpen);
  btn.classList.toggle('open', isOpen);
  btn.setAttribute('aria-label', isOpen ? 'Close menu' : 'Menu');
  if (isOpen) positionMenu();
}}

function closeFabMenu() {{
  isOpen = false;
  menu.classList.remove('show');
  overlay.classList.remove('show');
  btn.classList.remove('open');
  btn.setAttribute('aria-label', 'Menu');
}}

// ── Init position ──
var p = loadPos();
setPos(p.x, p.y);

// ── Mouse drag ──
btn.addEventListener('mousedown', function(e) {{
  isDragging = false;
  startX = e.clientX;
  startY = e.clientY;
  origX = parseInt(btn.style.left);
  origY = parseInt(btn.style.top);
  document.addEventListener('mousemove', onMouseMove);
  document.addEventListener('mouseup', onMouseUp);
}});

function onMouseMove(e) {{
  var dx = e.clientX - startX;
  var dy = e.clientY - startY;
  if (!isDragging && (Math.abs(dx) > dragThreshold || Math.abs(dy) > dragThreshold)) {{
    isDragging = true;
    btn.classList.add('dragging');
  }}
  if (isDragging) {{
    var np = clampPos(origX + dx, origY + dy);
    setPos(np.x, np.y);
  }}
}}

function onMouseUp(e) {{
  document.removeEventListener('mousemove', onMouseMove);
  document.removeEventListener('mouseup', onMouseUp);
  btn.classList.remove('dragging');
  if (isDragging) {{
    var np = clampPos(
      parseInt(btn.style.left) || origX,
      parseInt(btn.style.top) || origY
    );
    setPos(np.x, np.y);
    savePos(np.x, np.y);
    isDragging = false;
  }} else {{
    toggleFabMenu(e);
  }}
}}

// ── Touch drag ──
btn.addEventListener('touchstart', function(e) {{
  isDragging = false;
  var t = e.touches[0];
  startX = t.clientX;
  startY = t.clientY;
  origX = parseInt(btn.style.left);
  origY = parseInt(btn.style.top);
  document.addEventListener('touchmove', onTouchMove, {{passive: false}});
  document.addEventListener('touchend', onTouchEnd);
}}, {{passive: true}});

function onTouchMove(e) {{
  e.preventDefault();
  var t = e.touches[0];
  var dx = t.clientX - startX;
  var dy = t.clientY - startY;
  if (!isDragging && (Math.abs(dx) > dragThreshold || Math.abs(dy) > dragThreshold)) {{
    isDragging = true;
    btn.classList.add('dragging');
  }}
  if (isDragging) {{
    var np = clampPos(origX + dx, origY + dy);
    setPos(np.x, np.y);
  }}
}}

function onTouchEnd(e) {{
  document.removeEventListener('touchmove', onTouchMove);
  document.removeEventListener('touchend', onTouchEnd);
  btn.classList.remove('dragging');
  if (isDragging) {{
    var np = clampPos(
      parseInt(btn.style.left) || origX,
      parseInt(btn.style.top) || origY
    );
    setPos(np.x, np.y);
    savePos(np.x, np.y);
    isDragging = false;
  }} else {{
    toggleFabMenu(e);
  }}
}}

// ── Escape key ──
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape') closeFabMenu();
}});

// ── Reposition on resize ──
window.addEventListener('resize', function() {{
  var p = loadPos();
  setPos(p.x, p.y);
}});
}})();
</script>
""")

