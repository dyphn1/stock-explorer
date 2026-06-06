# 股識 Stock Explorer - 開發狀態

## 當前階段：M0 專案基礎建立

## 進度摘要
| 里程碑 | 狀態 | 完成日期 |
|--------|------|----------|
| M0: 專案基礎建立 | 🔄 進行中 | - |
| M1: MVP 名片頁 | ⏳ 待開始 | - |
| M2: 四大深度區塊 | ⏳ 待開始 | - |
| M3: 時間軸與分類 | ⏳ 待開始 | - |
| M4: ETF 與訂閱 | ⏳ 待開始 | - |
| M5: 自適應更新 | ⏳ 待開始 | - |

## M0 任務清單
- [x] 建立 GitHub repo
- [x] 初始化 Python 專案（uv + pyproject.toml）
- [x] 安裝依賴（FinMind, Streamlit, pandas, plotly, requests）
- [x] 撰寫產品願景文件
- [x] 撰寫技術設計文件
- [x] FinMind API 研究與驗證
- [ ] 建立專案目錄結構
- [ ] 實作 FinMind Client 封裝
- [ ] 實作快取機制
- [ ] 建立 Streamlit 入口

## 已完成的工作
- 2026-06-06: 市場調查（現有台股分析網站比較）
- 2026-06-06: 開源專案研究（FinMind, invest-system, taiwan-stock-analysis, CasualMarket）
- 2026-06-06: FinMind API 驗證（13 個免費 API 已測試）
- 2026-06-06: 產品設計文件撰寫
- 2026-06-06: 技術設計文件撰寫
- 2026-06-06: Cron 自動化流程建立

## 已知問題
- FinMind 部分 API 需要付費會員（股權分散表、產業供應鏈、市值、月/週均價）
- 第一階段不使用這些付費 API

## 下一步
1. 建立專案目錄結構
2. 實作 FinMind Client 封裝
3. 實作快取機制
4. 建立 Streamlit 入口
5. 開始 M1：MVP 名片頁

---
*最後更新：2026-06-06 22:41*
