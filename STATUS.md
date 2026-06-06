# 股識 Stock Explorer - 開發狀態

## 當前階段：M1 MVP 名片頁 🔄 進行中

## 進度摘要
| 里程碑 | 狀態 | 完成日期 |
|--------|------|----------|
| M0: 專案基礎建立 | ✅ 完成 | 2026-06-06 |
| M1: MVP 名片頁 | 🔄 進行中 | - |
| M2: 四大深度區塊 | ⏳ 待開始 | - |
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

## M1 任務清單（MVP 名片頁）
- [x] 完善公司名片頁（更多公司的一句話定位）— 擴展至 20 家公司
- [x] 營收來源圓餅圖（含白話說明）— 整合 revenue_analyzer + 已知公司資料
- [x] 關鍵數字的生活化比喻（更多指標）— 新增 analogy_engine（12 種比喻）
- [x] 近期動態的白話摘要（模板式摘要 + 影響程度標籤）
- [x] PPT 風格 CSS 優化（新增營收組成卡片、新聞卡片、hover 效果）
- [ ] 測試三支代表性股票（2330, 2454, 1101）— 待手動驗證
- [ ] 新手十秒測試驗證 — 待 Daniel 確認

## 已完成的工作
- 2026-06-06: 市場調查（現有台股分析網站比較）
- 2026-06-06: 開源專案研究（FinMind, invest-system, taiwan-stock-analysis, CasualMarket）
- 2026-06-06: FinMind API 驗證（13 個免費 API 已測試）
- 2026-06-06: 產品設計文件撰寫
- 2026-06-06: 技術設計文件撰寫
- 2026-06-06: Cron 自動化流程建立（dev-cycle + visual-verify）
- 2026-06-06: M0 專案基礎建立完成並 commit
- 2026-06-07: 實作營收組成分析器（revenue_analyzer.py）
- 2026-06-07: 實作生活化比喻引擎（analogy_engine.py）— 12 種指標比喻
- 2026-06-07: 實作新聞白話摘要器（news_summarizer.py）— 模板式 + 影響程度
- 2026-06-07: 更新 main.py 整合所有新元件
- 2026-06-07: CSS 優化（營收組成卡片、新聞卡片、hover 效果、數據來源標籤）

## 本次開發重點
### 新增檔案
- `src/services/revenue_analyzer.py` — 營收組成分析，含 8 家已知公司資料 + 通用 fallback
- `src/services/analogy_engine.py` — 12 種財務指標的生活化比喻（PER、PBR、殖利率、ROE、負債比、成交量、法人、年增率等）
- `src/services/news_summarizer.py` — 新聞白話摘要，10 種事件模板 + 影響程度判斷

### 更新檔案
- `src/main.py` — 整合營收圓餅圖、白話摘要、生活化比喻、額外財務指標計算
- `src/services/__init__.py` — 匯出新模組

### 功能亮點
1. 營收組成圓餅圖 + 右側白話說明卡片（點擊展開）
2. 關鍵數字卡片自動降級（PER → 毛利率 → ROE，確保總有資料可顯示）
3. 新聞摘要含影響程度標籤（🔴重大 / 🟡注意 / 🟢參考）
4. 毛利率、負債比、營收年增率自動從財報計算
5. 一句話定位擴展至 20 家台灣知名公司

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
1. 手動測試三支代表性股票（2330, 2454, 1101）— 需要 Daniel 啟動 Streamlit 驗證
2. 收集方向性反饋
3. 確認 M1 完成後進入 M2（四大深度區塊）

---
*最後更新：2026-06-07 08:00*
