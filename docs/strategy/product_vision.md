# Stock Explorer Product Vision

## Core Positioning
**Historian, not a stock picker**
- Do not say buy or sell; only explain what has happened to the company over time.
- Help users move from "I don't understand" to "I know what this company does."
- Focus on the company itself, not short-term price movement.

## Product Name
- **Name**: 股識
- **English**: Stock Explorer
- **Tagline**: Start by understanding the company

## Target Users
- Beginner investors who want to understand the market but feel overwhelmed by jargon.
- Curious observers who want to know how companies around them make money.
- Long-term investors who want to understand changes in the companies they hold.
- Not for short-term traders or people chasing quick profits.

## Market Pain Points
1. **資訊過載但理解不足**：財報狗等工具提供海量數據但缺乏白話解釋
2. **碎片化認知**：需要從多個網站拼湊公司完整畫面
3. **事後諸葛**：多分析工具解釋過去但不幫助理解未來變數
4. **缺乏故事性**：數據堆砌而無脈絡，難以建立記憶點
5. **工具導向而非教育導向**：焦點在「該買什麼」而不是「這家公司是什麼」

## 核心價值主張

### 1. 故事優先，數據為輔
- 每個分析點以一個生活化案例開場
- 例如：不說「毛利率 66%」，而說「賣 100 元東西，扣掉成本還剩 66 元」
- 所有結論必須可追溯到公開數據來源

### 2. PPT 風格呈現
- 圖片為主，文字為輔（一頁一個重點）
- 避免密集文字牆，使用圖表、圖示、簡短標語

### 3. 自適應與自我進化
- 內容隨公司變化而更新
- 重大事件驅動更新：收購、合併、重大虧損等觸發內容重生
- 適應不同公司類型：集團與單一公司使用不同分析框架

### 4. 點對點認知建構
- 集團架構不做組織圖，做「母公司 → 子公司」的點對點說明
- 每個關係附帶業務往來、持股比例、協同效應說明
- 逐步挖掘：先看主要關係，深入時才顯示次要關係

### 5. 標竿導向分析
- 不問「這家公司好不好」，而問「這家公司跟產業第一名差在哪」
- 所有比較以產業標竿為基準
- 差異分析必須給出具體原因

## 產品架構

### 第一層：公司名片頁（MVP 核心）
- 一句話定位
- 收入來源圓餅圖（每塊附白話說明）
- 最近一則重大事件白話摘要
- 導航至四大深度區塊

### 第二層：四大深度區塊
1. **營運健檢**：靠什麼賺錢？穩不穩？隨時間怎麼變？
2. **財務體質**：賺多少？花多少？剩多少？
3. **同業比較**：跟產業第一名差在哪？用實際案例說明
4. **集團架構**：母子公司關係（點對點）

### 第三層：輔助功能
- 時間軸配置：預設 3 年，可自由調整
- 分類瀏覽：權值股、產業分類、熱門列表
- ETF 專區：同等對待，從持倉到特色策略
- 訂閱系統：全 config 化

## 技術選型
1. **資料層**：FinMind（50+ 金融資料集，每日更新）
2. **處理層**：Python（資料清理、特徵工程）
3. **解釋層**：LLM（僅限白話轉譯）+ 模板
4. **視覺層**：Plotly（互動圖表）+ 自定義 CSS（PPT 風格）
5. **展示層**：Streamlit（快速迭代）
6. **快取層**：本地檔案快取 + 失效機制

## 開發哲學
### 反覆循環而非瀑布式
- 設計 > 分析 > 反思 > 歸納整理 > 重新設計
- 每個功能實作後必須驗證：對新手是否真的更易理解？
- 拒絕一次性實作全部功能

### 驗證原則
- 每個解釋必須過「十秒測試」：新手看十秒後能複述核心概念
- 所有數據標明來源，避免黑箱感
- 願意犧牲完整性以求清晰度

## 里程碑
| 里程碑 | 內容 | 驗證標準 |
|--------|------|----------|
| M0 | 專案基礎建立 | 環境可跑 |
| M1 | MVP 名片頁 | 新手十秒複述正確率 > 80% |
| M2 | 四大深度區塊 | 能回答「這家公司最近在幹嘛？」 |
| M3 | 時間軸與分類 | 使用者能自主探索不同維度 |
| M4 | ETF 與訂閱 | 使用者主動設定並收到通知 |
| M5 | 自適應更新 | 重大事件後 24 小時內內容更新 |

## 風險與對策
| 風險 | 對策 |
|------|------|
| LLM 生成不實事實 | LLM 限於白話轉譯，事實來自結構化數據 |
| 開發範圍蔓延 | 嚴格執行里程碑驗證 |
| 資料更新延遲 | FinMind 每日更新；重大事件由使用者回報觸發 |
| 使用者仍想要買賣建議 | 明確產品定位：「這不是選股工具」 |
| 集團架構複雜度失控 | 第一階段只處理持股 > 50% 或營收貢獻 > 10% |

---
*最後更新：2026-06-06*
