# Welcome Page Audit — 2026-06-24

## Screenshots
- `welcome_full.png` — Full page (1280x900)
- `welcome_viewport.png` — Viewport only

## Rendered Structure

### Sidebar (custom activity bar)
```
📊 股識 Stock Explorer
▸ 📇 基本資料       ← active, hardcoded Chinese
  📂 分類瀏覽
  🏷️ ETF 專區
  ⭐ 關注列表
  🔔 事件儀表板
  📈 今日市場動態
  ⚙️ 設定
  🔥 熱門股票 (expander)
  🏷️ 熱門 ETF (expander)
  ⚠️ 本工具僅供認識公司使用...
```

Before the custom bar, Streamlit's default sidebar nav shows raw page keys (`main`, `academy`, ...).

### Main Content
```
📊 股識
認識一家公司，從這裡開始
💡 在側邊欄輸入股票名稱或代號開始使用
```

### Search Bar (top of main area)
```
placeholder: 例如：台積電 或 2330
aria-label: 輸入股票名稱
position: y=113
```

## Changes Applied (2026-06-24)

| # | Fix | Files |
|---|-----|-------|
| 1 | ✅ business_card 改用 `t('page.business_card')`（「名片」），不再硬編碼「基本資料」 | `activity_bar.py` |
| 5 | ✅ 側邊欄改為自訂收合：icon+文字 ↔ icon-only + hover tooltip | `activity_bar.py`, `layout.py` |
| — | ✅ 移除 Navbar 28 項 radio group（重複） | `navbar.py` |
| — | ✅ 簡化 FAB（僅保留，不再由 layout 自動載入） | `app_controller.py` |
| — | ✅ 側邊欄加入「◂/▸」收合按鈕，切換顯示模式 | `activity_bar.py` |
| — | ✅ 新增 `sidebar.toggle` locale key | `locales/en.yaml`, `zh-TW.yaml` |
| — | ✅ Streamlit 預設側邊導覽移除（CSS + JS MutationObserver） | `layout.py` |
| — | ✅ 新增可串接 Page Object Model 測試 | `tests/pages/*`, `tests/test_welcome_page.py` |

## Remaining Issues

| # | Severity | Issue | Location |
|---|----------|-------|----------|
| 2 | 🐛 Bug | quick_hint 寫「側邊欄」但搜尋框在頂部 | `welcome_page.py` + `locales/*.yaml` |
| 3 | 🧹 Cleanup | `lead2` 已定義但從未渲染 | `welcome_page.py` |
| 4 | 🧹 Cleanup | 歡迎頁無語言切換器 | `welcome_page.py` |
| 6 | 🎨 Style | 歡迎頁用 raw `st.markdown`，無卡片容器 | `welcome_page.py` |
| 7 | 🧹 Cleanup | `en.yaml` 有殘留 `test_key` | `en.yaml:311` |
| 8 | 🐛 Bug | `key_takeaways.2330.X` raw i18n keys visible on stock detail page | business card |

## Current Sidebar Design

### Expanded (default)
```
📊 股識 Stock Explorer   [◂]
━━━━━━━━━━━━━━━━━
📇 名片                 ← active with ▸
📂 分類瀏覽
🏷️ ETF 專區
⭐ 關注列表
🔔 事件儀表板
📈 今日市場動態
⚙️ 設定
━━━━━━━━━━━━━━━━━
🔥 熱門股票 (expander)
🏷️ 熱門 ETF (expander)
━━━━━━━━━━━━━━━━━
⚠️ 本工具僅供認識公司使用...
```

### Collapsed (icon-only)
```
📊
[▸]
━━━
📇  (hover → "名片")
📂  (hover → "分類瀏覽")
🏷️  (hover → "ETF 專區")
⭐  (hover → "關注列表")
🔔  (hover → "事件儀表板")
📈  (hover → "今日市場動態")
⚙️  (hover → "設定")
━━━
(無 hot stocks/ETF/disclaimer)
```

## Color Scheme
