# UX 改進路線圖

> **來源**: `docs/decisions/ux_improvements.md` (2026-06-08)
> **狀態**: 待實作 | **優先級**: P0-P2

---

## P0 — 立即修復（Crash / 嚴重 Bug）

| ID | 問題 | 說明 | 影響檔案 |
|----|------|------|----------|
| UX-08 | DuplicateWidgetID crash | 事件儀表板按鈕 key 重複導致頁面崩潰 | `event_dashboard.py` |

**修復方式**: 使用 `enumerate` index 確保 key 唯一性：`f"evt_{stock_id}_{idx}"`

---

## P1 — Sprint 1（低工作量，高影響）

| ID | 問題 | 說明 | 影響檔案 |
|----|------|------|----------|
| UX-05 | ROE 年化不準確 | 季節性產業用 `*4` 年化失真，改用 TTM | `financial_health.py`, `peer_comparison.py` |
| UX-07 | 關注列表無視覺反饋 | 加入/移除關注後無 toast 提示 | `business_card.py`, `watchlist_page.py` |
| UX-11 | 快取永不清理 | `.cache/` 目錄無限增長 | `finmind_client.py` |
| UX-14 | 關注列表並發寫入 | 多 session 同時寫入 watchlist.yaml 可能損壞 | `watchlist.py` |

---

## P2 — Sprint 2（中工作量，核心 UX）

| ID | 問題 | 說明 | 影響檔案 |
|----|------|------|----------|
| UX-01 | 中文搜尋不支援 | 搜尋框只比對 stock_id，無法搜「台積電」 | `main.py`, `finmind_client.py` |
| UX-02 | 頁面切換無載入指示 | 切換頁面時空白無 spinner | `router.py`, `_router_base.py` |
| UX-04 | 單一期間圖表為空 | 數據不足時圖表空白，應降級顯示 | `chart.py` |
| UX-06 | 同業比較無候補 | 無標竿公司時顯示死頁，應自動選同產業最大 | `peer_comparison.py` |
| UX-09 | 時間軸篩選靜默失敗 | filter_by_timeline 異常時無錯誤提示 | `_router_base.py` |
| UX-13 | 深色模式對比不足 | Plotly 圖表標籤在深色模式不可讀 | `chart.py` |

---

## P3 — Sprint 3（高工作量，架構級）

| ID | 問題 | 說明 | 影響檔案 |
|----|------|------|----------|
| UX-03 | 瀏覽器返回按鈕 | 使用 `st.query_params` 同步 URL | `main.py`, `router.py`, 所有頁面 |
| UX-10 | API 速率限制無警告 | 快速切換股票時無 rate limit 提示 | `finmind_client.py`, `_router_base.py` |
| UX-12 | 小螢幕佈局崩潰 | 6-column 佈局在窄螢幕上擁擠 | `router.py`, `category_browser.py`, `etf_browser.py` |

---

## 側邊欄改進項目

> **來源**: `docs/decisions/sidebar_gap_analysis.md` + `docs/decisions/sidebar_research.md`

### P0 — 側邊欄 Bug

| ID | 問題 | 說明 |
|----|------|------|
| SB-04 | 側邊欄收合後無法再展開 | `initial_sidebar_state="auto"` 導致 |

### P1 — 側邊欄核心功能

| ID | 問題 | 說明 |
|----|------|------|
| SB-01 | Watchlist 無內聯數據 | 側邊欄應直接顯示價格、漲跌幅 |
| SB-02 | 無法多清單管理 | 目前只有一個「我的關注」 |
| SB-03 | 無市場總覽 | 側邊欄底部應顯示大盤指數 |
| SB-05 | 分類瀏覽入口 | 側邊欄缺少分類瀏覽快捷入口 |
| SB-06 | 最近瀏覽記錄 | 無法快速回到之前看過的股票 |
| SB-07 | 側邊欄寬度可調整 | 固定寬度對不同螢幕不友善 |
| SB-08 | 圖示+標籤導航 | 目前只有文字按鈕，缺乏視覺層次 |

### P2 — 側邊欄加分功能

| ID | 問題 | 說明 |
|----|------|------|
| SB-09 | Hover 預覽 | hover 股票顯示 mini chart tooltip |
| SB-10 | 拖曳排序 | watchlist 可拖曳排序 |
| SB-11 | 右鍵選單 | 右鍵股票可加入警示、移除等 |
| SB-12 | 通知 badge | 事件儀表板有新事件時顯示紅點 |
| SB-13 | 資料更新時間 | 顯示最後更新時間 |

---

## 設計審查待修復項目

> **來源**: `docs/decisions/design_comparison_review.md` + `design_comparison_review_round5.md`

### 色彩系統違規

| ID | 問題 | 影響檔案 |
|----|------|----------|
| DC-006 | 使用 `#F39C12`（非系統色） | `financial_health.py` |
| DC-013 | 使用 `#2E86C1`/`#1B4F72`/`#8E44AD`（非系統色） | `etf_browser.py`, `watchlist_page.py` |
| DC-chart | Plotly 圖表使用非系統色 | `chart.py` |

### 元件不一致

| ID | 問題 | 影響檔案 |
|----|------|----------|
| DC-001 | Watchlist 按鈕放在 Zone A | `business_card.py` |
| DC-004 | 自定義 gradient 未使用共享元件 | `operation_checkup.py` |
| DC-009 | 自定義 health assessment card | `financial_health.py` |
| DC-011 | 使用 `st.metric()` 而非 `_白话_card()` | `peer_comparison.py` |
| DC-025 | Raw flexbox HTML 而非 `_白话_card()` | `watchlist_page.py` |
| DC-027 | 自定義 gradient banner | `event_dashboard.py` |
| DC-028 | 內聯 HTML 硬編碼 border color | `watchlist_page.py` |

### 佈局問題

| ID | 問題 | 影響檔案 |
|----|------|----------|
| DC-003 | `_info_card()` 文字過長 | `operation_checkup.py` |
| DC-007 | 財務體質頁文字過多 | `financial_health.py` |
| DC-008 | 圖表比例不足 60% | `financial_health.py` |
| DC-010 | 同業比較分析文字過長 | `peer_comparison.py` |
| DC-015 | 6-column ETF 佈局 | `etf_browser.py` |
| DC-019 | 6-column 分類佈局 | `category_browser.py` |
| DC-020 | `label_visibility="collapsed"` 無障礙問題 | `category_browser.py` |
| DC-022 | severity badge 只有 emoji 無文字 | `event_dashboard.py` |
