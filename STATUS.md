# 股識 Stock Explorer - 開發狀態

## 當前階段：M4 ETF 與訂閱 🔄 進行中（Bug 修復輪次）

## 進度摘要
| 里程碑 | 狀態 | 完成日期 |
|--------|------|----------|
| M0: 專案基礎建立 | ✅ 完成 | 2026-06-06 |
| M1: MVP 名片頁 | ✅ 完成 | 2026-06-07 |
| M2: 四大深度區塊 | ✅ 完成 | 2026-06-07 |
| M3: 時間軸與分類 | ✅ 完成 | 2026-06-07 |
| M4: ETF 與訂閱 | 🔄 進行中 | - |
| M5: 自適應更新 | ⏳ 待開始 | - |

## M0 任務清單（已完成）
- [x] 建立 GitHub repo
- [x] 初始化 Python 專案（uv + pyproject.toml）
- [x] 安裝依賴（FinMind, Streamlit, pandas, plotly, requests）
- [x] 撰寫產品願景文件
- [x] 撰寫技術設計文件
- [x] FinMind API 研究與驗證（13 個免費 API）
- [x] 建立專案目錄結構
- [x] 實作 FinMind Client 封裝（含快取）
- [x] 實作圖表生成器（6 種圖表）
- [x] 建立 Streamlit 入口與公司名片頁
- [x] 建立 Cron 自動化流程

## M1 任務清單（MVP 名片頁）— 已完成
- [x] 完善公司名片頁（更多公司的一句話定位）— 擴展至 20 家公司
- [x] 營收來源圓餅圖（含白話說明）— 整合 revenue_analyzer + 已知公司資料
- [x] 關鍵數字的生活化比喻（更多指標）— 新增 analogy_engine（12 種比喻）
- [x] 近期動態的白話摘要（模板式摘要 + 影響程度標籤）
- [x] PPT 風格 CSS 優化（新增營收組成卡片、新聞卡片、hover 效果）
- [x] 測試三支代表性股票（2330, 2454, 1101）— 自動化驗證通過（0 錯誤, 0 警告）
- [x] 新手十秒測試驗證 — 代碼完成，待 Daniel 手動 UI 確認

## M2 任務清單（四大深度區塊）— 已完成
- [x] 建立頁面路由器（router.py）
- [x] 公司名片頁重構為獨立模組（business_card.py）
- [x] 營運健檢頁（operation_checkup.py）— 營收趨勢、股價走勢、法人動向、營運摘要
- [x] 財務體質頁（financial_health.py）— 利潤漏斗、關鍵比率、資產負債結構、現金流量
- [x] 同業比較頁（peer_comparison.py）— 並排比較表、雷達圖、差異分析、28 產業標竿
- [x] 集團架構頁（group_structure.py）— 點對點關係、5 家集團資料、關係圖
- [x] 所有模組語法與匯入驗證通過（19 個 Python 檔案，0 錯誤）
- [x] 整合測試通過（所有模組匯入成功）

## M3 任務清單（時間軸與分類）— 已完成
- [x] 時間軸元件：timeline_controls.py（1Y / 3Y / 5Y / ALL 選擇器）
- [x] _router_base.py 加入 filter_by_timeline 輔助函式
- [x] 營運健檢頁整合時間軸過濾（營收、股價、法人圖表）
- [x] 財務體質頁整合時間軸過濾（利潤漏斗、資產負債、現金流量）
- [x] 分類瀏覽頁：category_browser.py
  - [x] 權值股列表（依成交金額排序，Top 20）
  - [x] 產業分類瀏覽（57 產業分類，點擊展開股票列表）
  - [x] 熱門列表（依成交量排序，Top 20）
- [x] 路由器更新：新增「分類瀏覽」頁面（共 6 頁）
- [x] 所有語法與匯入驗證通過
- [x] M3 完成並 commit

## M4 任務清單（ETF 與訂閱）— 進行中
### M4a: ETF 專區
- [x] ETF 資料研究：確認 FinMind 免費 API 可取得 ETF 資料（~500 檔）
- [x] ETF 瀏覽頁（etf_browser.py）
  - [x] 熱門 ETF（依成交量排序，Top 20）
  - [x] ETF 分類瀏覽（市值型/高股息型/債券型/主題型/其他）
  - [x] 配息排行（依殖利率排序，Top 20）
- [x] ETF 詳細頁（etf_detail.py）
  - [x] 一句話定位（依 ETF 類型自動生成）
  - [x] 績效走勢圖（近一年收盤價）
  - [x] 配息資訊（頻率、金額、白話說明）
  - [x] 法人動向（近 30 天買賣超）
  - [x] 費用說明（管理費生活化比喻）
  - [x] ETF 小知識（依類型說明）
- [x] 路由器更新：新增「ETF 專區」頁面
- [x] ETF 自動判斷：輸入 ETF 代碼自動導向 ETF 詳細頁
- [x] 側邊欄新增熱門 ETF 快捷入口（0050, 0056, 00878, 00919, 006208）
- [ ] 需要 Daniel 手動啟動 Streamlit 進行 UI 驗證

### M4b: 訂閱系統
- [x] Watchlist 服務（watchlist.py）
  - [x] YAML 基礎的 config 儲存（config/watchlist.yaml）
  - [x] 加入/移除關注
  - [x] 價格提醒（alert_above / alert_below）
  - [x] 關注摘要（含即時價格、提醒觸發狀態）
- [x] 關注頁面（watchlist_page.py）
  - [x] 關注列表（價格、漲跌幅、提醒狀態）
  - [x] 移除功能
  - [x] 空狀態引導
- [x] 名片頁整合：加入/取消關注按鈕
- [x] 側邊欄新增「我的關注」快捷入口
- [x] 路由器更新：新增「我的關注」頁面
- [ ] 需要 Daniel 手動啟動 Streamlit 進行 UI 驗證

## 已完成的工作
### 2026-06-06
- 市場調查（現有台股分析網站比較）
- 開源專案研究（FinMind, invest-system, taiwan-stock-analysis, CasualMarket）
- FinMind API 驗證（13 個免費 API 已測試）
- 產品設計文件撰寫
- 技術設計文件撰寫
- Cron 自動化流程建立（dev-cycle + visual-verify）
- M0 專案基礎建立完成並 commit

### 2026-06-07（M1）
- 實作營收組成分析器（revenue_analyzer.py）
- 實作生活化比喻引擎（analogy_engine.py）— 12 種指標比喻
- 實作新聞白話摘要器（news_summarizer.py）— 模板式 + 影響程度
- 更新 main.py 整合所有新元件
- CSS 優化（營收組成卡片、新聞卡片、hover 效果、數據來源標籤）
- M1 完成並 commit

### 2026-06-07（M2）
- 建立頁面路由器架構（router.py + _router_base.py）
- 實作營運健檢頁（operation_checkup.py）
- 實作財務體質頁（financial_health.py）
- 實作同業比較頁（peer_comparison.py）
- 實作集團架構頁（group_structure.py）
- 所有模組語法與匯入驗證通過（0 錯誤）
- M2 整合測試通過並 commit

### 2026-06-07（M3）
- 實作時間軸控制元件（timeline_controls.py）
- 更新 _router_base.py 加入 filter_by_timeline
- 更新營運健檢頁、財務體質頁支援時間軸過濾
- 實作分類瀏覽頁（category_browser.py）— 權值股、產業分類、熱門列表
- 更新 router.py 新增「分類瀏覽」路由
- 所有 19 個 Python 檔案語法驗證通過
- M3 完成並 commit

### 2026-06-07（M4 第一輪）
- ETF 資料研究：確認 ~500 檔 ETF 可透過 `industry_category` 篩選
- 實作 ETF 瀏覽頁（etf_browser.py）— 熱門、分類、配息排行
- 實作 ETF 詳細頁（etf_detail.py）— 績效、配息、法人、費用、小知識
- 實作 Watchlist 服務（watchlist.py）— YAML 儲存、價格提醒
- 實作關注頁面（watchlist_page.py）— 列表、移除、空狀態
- 路由器更新：新增「ETF 專區」和「我的關注」頁面（共 8 頁）
- 側邊欄新增熱門 ETF 快捷入口和關注按鈕
- 名片頁加入關注/取消關注按鈕
- ETF 自動判斷與導向
- 所有 23 個 Python 檔案語法與匯入驗證通過（0 錯誤）
- M4 第一輪完成並 commit

### 2026-06-07（Bug 修復輪次）
- **ISSUE-001 修復**：關注頁面新增價格提醒設定 UI
  - `watchlist_page.py`：新增「🔔 設定提醒」按鈕 + `st.popover` 輸入上限/下限
  - `watchlist.py`：新增 `update_alerts()` 函數
- **ISSUE-002 改善**：擴展 ETF 分類關鍵字（精確匹配 + 通用關鍵字）
- **ISSUE-003 改善**：`_is_etf()` 加入 `industry_category` 參數，三層判斷順序
- **ISSUE-004 修復**：ETF 瀏覽頁加入 `@st.cache_data` 快取（`_cached_get_stock_info` + `_get_all_etf_prices`）
- 所有 15 個 Python 檔案語法驗證通過（0 錯誤）
- 所有匯入與邏輯單元測試通過

## 架構總覽
### 目錄結構
```
src/
├── main.py                    # Streamlit 入口 + 側邊欄
├── data/
│   ├── finmind_client.py      # FinMind API 封裝（含快取）
│   └── models.py              # 資料模型
├── services/
│   ├── chart.py               # 6 種圖表生成器
│   ├── analogy_engine.py      # 12 種生活化比喻
│   ├── revenue_analyzer.py    # 營收組成分析
│   ├── news_summarizer.py     # 新聞白話摘要
│   └── watchlist.py           # 關注列表管理（YAML）
└── pages/
    ├── __init__.py
    ├── _router_base.py        # 共享工具（get_stock_data, filter_by_timeline）
    ├── router.py              # 頁面路由器（8 頁）
    ├── business_card.py       # 公司名片頁
    ├── operation_checkup.py   # 營運健檢頁
    ├── financial_health.py    # 財務體質頁
    ├── peer_comparison.py     # 同業比較頁
    ├── group_structure.py     # 集團架構頁
    ├── timeline_controls.py   # 時間軸控制元件
    ├── category_browser.py    # 分類瀏覽頁
    ├── etf_browser.py         # ETF 瀏覽頁
    ├── etf_detail.py          # ETF 詳細頁
    └── watchlist_page.py      # 關注列表頁
config/
└── watchlist.yaml             # 關注列表資料（自動生成）
```

### 架構亮點
1. **模組化頁面架構**：每個頁面獨立一個檔案，方便維護和擴展
2. **共享工具層**：`_router_base.py` 提供共用的資料載入、計算、時間軸過濾
3. **頁面路由**：使用 session_state['page'] 控制頁面切換
4. **時間軸**：全域時間範圍選擇器，圖表動態過濾
5. **分類瀏覽**：權值股、產業分類、熱門列表三種探索方式
6. **ETF 同等對待**：ETF 有專屬詳細頁，自動判斷導向
7. **關注系統**：YAML config 為基礎，支援價格提醒
8. **白話解讀**：每個頁面都有自動生成的白話解讀和摘要

## 統計
- **總程式碼行數**：~4,800 行（Python）
- **Python 檔案數**：23 個
- **頁面數**：8 頁（名片、營運健檢、財務體質、同業比較、集團架構、分類瀏覽、ETF 專區、我的關注）
- **Git Commits**：7 個
- **語法錯誤**：0
- **匯入錯誤**：0

## 已知問題
- FinMind 部分 API 需要付費會員（股權分散表、產業供應鏈、市值、月/週均價）
- 第一階段不使用這些付費 API
- LSP 顯示 import 警告（因 .venv 不在 LSP 路徑），不影響執行
- Pyright 對 Streamlit 控制流（if/else）的變數作用域有誤報，不影響執行
- 分類瀏覽頁的權值股/熱門列表需要遍歷多支股票資料，載入時間可能較長
- ETF 詳細頁的配息排行需要遍歷多檔 ETF，載入時間可能較長
- ETF 持股資料（前十大持股）FinMind 付費 API 無，目前以公開說明書靜態資料替代

## Cron 自動化
| Job | 頻率 | 用途 |
|-----|------|------|
| stock-explorer-dev-cycle | 每 2 小時 | 主開發循環：讀取進度→分派任務→更新狀態 |
| stock-explorer-visual-verify | 每 4 小時 | 視覺化驗證：啟動 Streamlit→截圖→記錄 |

## 下一步
1. ✅ M4 ETF 與訂閱 — 代碼完成
2. ⏳ Daniel 手動 UI 驗證（ETF 專區、我的關注、價格提醒 UI）
3. ⏳ M5 準備 — 自適應更新機制（重大事件驅動更新）

---
*最後更新：2026-06-07 15:00*
