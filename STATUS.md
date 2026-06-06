# 股識 Stock Explorer - 開發狀態

## 當前階段：M2 四大深度區塊 🔄 進行中

## 進度摘要
| 里程碑 | 狀態 | 完成日期 |
|--------|------|----------|
| M0: 專案基礎建立 | ✅ 完成 | 2026-06-06 |
| M1: MVP 名片頁 | ✅ 完成 | 2026-06-07 |
| M2: 四大深度區塊 | 🔄 進行中 | - |
| M3: 時間軸與分類 | ⏳ 待開始 | - |
| M4: ETF 與訂閱 | ⏳ 待開始 | - |
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

## M2 任務清單（四大深度區塊）
- [x] 建立頁面路由器（router.py）
- [x] 公司名片頁重構為獨立模組（business_card.py）
- [x] 營運健檢頁（operation_checkup.py）— 營收趨勢、股價走勢、法人動向、營運摘要
- [x] 財務體質頁（financial_health.py）— 利潤漏斗、關鍵比率、資產負債結構、現金流量
- [x] 同業比較頁（peer_comparison.py）— 並排比較表、雷達圖、差異分析、28 產業標竿
- [x] 集團架構頁（group_structure.py）— 點對點關係、5 家集團資料、關係圖
- [x] 所有模組語法與匯入驗證通過
- [ ] 整合測試（啟動 Streamlit 驗證所有頁面）— 待 Daniel 手動確認

## 已完成的工作
### 2026-06-06
- 市場調查（現有台股分析網站比較）
- 開源專案研究（FinMind, invest-system, taiwan-stock-analysis, CasualMarket）
- FinMind API 驗證（13 個免費 API 已測試）
- 產品設計文件撰寫
- 技術設計文件撰寫
- Cron 自動化流程建立（dev-cycle + visual-verify）
- M0 專案基礎建立完成並 commit

### 2026-06-07
- 實作營收組成分析器（revenue_analyzer.py）
- 實作生活化比喻引擎（analogy_engine.py）— 12 種指標比喻
- 實作新聞白話摘要器（news_summarizer.py）— 模板式 + 影響程度
- 更新 main.py 整合所有新元件
- CSS 優化（營收組成卡片、新聞卡片、hover 效果、數據來源標籤）
- M1 完成並 commit

### 2026-06-07（M2 第一輪）
- 建立頁面路由器架構（router.py + _router_base.py）
- 重構 main.py 為模組化架構
- 實作營運健檢頁（operation_checkup.py）
  - 營收趨勢圖 + 年增率白話解讀
  - 股價走勢圖（K線 + 成交量）
  - 三大法人買賣超圖 + 動向總結
  - 營運摘要卡片
- 實作財務體質頁（financial_health.py）
  - 利潤漏斗圖（營收→毛利→營業利益→淨利）
  - 關鍵財務比率三連卡（毛利率、ROE、負債比、PER、殖利率）
  - 資產負債結構解讀 + 財務體質評估
  - 現金流量解讀（營業/投資/籌資活動）
- 實作同業比較頁（peer_comparison.py）
  - 28 產業標竿對應表
  - 並排比較表（差距百分比）
  - 雷達圖（多維度正規化比較）
  - 差異分析白話解讀
- 實作集團架構頁（group_structure.py）
  - 5 家集團資料（台積電、鴻海、富邦金、台塑、台泥）
  - 點對點關係卡片（持股比例、營收貢獻、業務說明）
  - 集團關係長條圖
  - 集團策略解讀
- 所有模組語法與匯入驗證通過（0 錯誤）

## 本次開發重點（M2）
### 新增檔案
- `src/pages/__init__.py` — 頁面模組初始化
- `src/pages/_router_base.py` — 路由器共享工具（get_stock_data、calc_extra_metrics 等）
- `src/pages/router.py` — 頁面路由器（根據 session_state['page'] 渲染對應頁面）
- `src/pages/business_card.py` — 公司名片頁（從 main.py 重構）
- `src/pages/operation_checkup.py` — 營運健檢頁
- `src/pages/financial_health.py` — 財務體質頁
- `src/pages/peer_comparison.py` — 同業比較頁
- `src/pages/group_structure.py` — 集團架構頁

### 更新檔案
- `src/main.py` — 重構為模組化架構，使用路由器

### 架構亮點
1. **模組化頁面架構**：每個頁面獨立一個檔案，方便維護和擴展
2. **共享工具層**：`_router_base.py` 提供共用的資料載入和計算函式
3. **頁面路由**：使用 session_state['page'] 控制頁面切換
4. **導航列**：頂部導航列在所有頁面間保持一致
5. **白話解讀**：每個頁面都有自動生成的白話解讀和摘要

## 已知問題
- FinMind 部分 API 需要付費會員（股權分散表、產業供應鏈、市值、月/週均價）
- 第一階段不使用這些付費 API
- LSP 顯示 import 警告（因 .venv 不在 LSP 路徑），不影響執行
- Pyright 對 Streamlit 控制流（if/else）的變數作用域有誤報，不影響執行

## Cron 自動化
| Job | 頻率 | 用途 |
|-----|------|------|
| stock-explorer-dev-cycle | 每 2 小時 | 主開發循環：讀取進度→分派任務→更新狀態 |
| stock-explorer-visual-verify | 每 4 小時 | 視覺化驗證：啟動 Streamlit→截圖→記錄 |

## 下一步
1. 手動測試所有頁面（名片、營運健檢、財務體質、同業比較、集團架構）— 需要 Daniel 啟動 Streamlit 驗證
2. 收集方向性反饋
3. 確認 M2 完成後進入 M3（時間軸與分類）

---
*最後更新：2026-06-07 10:00*
