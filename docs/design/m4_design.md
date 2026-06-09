# Stock Explorer M4 Design Document

## M4a: ETF Section

### Design Principles
- Treat ETFs the same as individual stocks; they are not a side feature.
- Move from "what does this ETF hold" to "why would someone buy this ETF".
- Explain ETF strategies in plain language so beginners can understand the differences.

### 頁面結構
1. **ETF 名片頁**（與個股名片並列）
   - 一句話定位：「這檔 ETF 在追蹤什麼」
   - 前十大持股圓餅圖（FinMind 無持股 API，改用「ETF 基本資料」呈現）
   - 績效走勢（與追蹤指數比較，目前只有 ETF 自身價格）
   - 配息資訊（白話說明配息頻率和金額）
   - 費用說明（管理費的生活化比喻）

2. **ETF 分類瀏覽**
   - 市值型（0050, 006208）
   - 高股息型（0056, 00878, 00919）
   - 債券型（00679B, 00720B）
   - 主題型（電動車、AI、半導體等）
   - 槓桿/反向型

3. **ETF 比較工具**
   - 兩檔 ETF 並排比較（費用、規模、配息、績效）
   - 差異白話說明

### 資料策略
- 使用 `industry_category` 包含 "ETF" 來篩選
- 使用 `taiwan_stock_daily` 取得價格
- 使用 `taiwan_stock_dividend` 取得配息
- 使用 `taiwan_stock_institutional_investors` 取得法人動向
- 持股資料：FinMind 付費 API 無，改用「ETF 公開說明書」靜態資料或省略

### 實作順序
1. 先完成 ETF 篩選和基本資料取得
2. ETF 名片頁（簡化版）
3. ETF 分類瀏覽
4. ETF 比較工具

## M4b: 訂閱系統

### 設計原則
- 全 config 化，不需資料庫
- 使用者可以「關注」股票/ETF
- 側邊欄顯示關注列表
- 每次啟動時顯示關注股票的摘要

### 資料結構
```yaml
# config/watchlist.yaml
watchlist:
  - stock_id: "2330"
    name: "台積電"
    type: "stock"
    added_date: "2026-06-07"
    alert_price_above: 1000
    alert_price_below: 800
  - stock_id: "0050"
    name: "元大台灣50"
    type: "etf"
    added_date: "2026-06-07"
```

### 功能
1. 加入/移除關注
2. 設定價格提醒（可選）
3. 側邊欄顯示關注列表（含即時價格）
4. 關注頁面摘要（價格變動、新聞）

### 實作順序
1. Watchlist config 管理（讀寫 YAML）
2. 側邊欄整合關注列表
3. 價格提醒邏輯
4. 關注摘要頁面

---
*建立日期：2026-06-07*
