# 股識 Stock Explorer — 架構定義

> 這是一份「開發前必須遵循」的架構分層規範。所有新功能必須依照本文件的分層與資料流開發。

---

## 一、分層架構

```
┌─────────────────────────────────────────────────────┐
│  展示層 (View)                                      │
│  src/pages/*.py                                     │
│  職責：純渲染，接收 data dict，產生 Streamlit UI     │
│  禁止：直接呼叫 FinMind API、直接讀寫 file/cache     │
├─────────────────────────────────────────────────────┤
│  路由層 (Router)                                    │
│  src/pages/router.py                                │
│  職責：管理 session_state、選擇 View、協調資料載入    │
│  禁止：直接產生 UI 元件、直接打 API                  │
├─────────────────────────────────────────────────────┤
│  業務邏輯層 (Service)                               │
│  src/services/*.py                                  │
│  職責：計算指標、生成圖表、白話轉譯、資料分析         │
│  禁止：使用任何 Streamlit API、直接讀寫 cache        │
├─────────────────────────────────────────────────────┤
│  資料層 (Model/Data)                                │
│  src/data/*.py                                      │
│  職責：FinMind API 封裝、快取管理、資料模型           │
│  禁止：使用任何 Streamlit API、包含業務邏輯          │
└─────────────────────────────────────────────────────┘
```

---

## 二、各層職責明確定義

### 2.1 資料層 — `src/data/`

**檔案**：
- `finmind_client.py`：FinMind API 封裝，含快取
- `models.py`：資料型別定義（若需要）

**職責**：
- 打 FinMind API
- 管理本地檔案快取（讀、寫、TTL 失效）
- 回傳 pandas DataFrame 或 dict

**介面規範**：
```python
# ✅ 正確：回傳 DataFrame
def get_daily_price(self, stock_id: str) -> pd.DataFrame:
    ...

# ✅ 正確：回傳 None 表示無資料（不拋異常）
def get_latest_price(self, stock_id: str) -> dict | None:
    ...

# ❌ 錯誤：在資料層決定是否顯示 spinner
# ❌ 錯誤：在資料層做「取 200 筆後排序取前 20」这种混有業務邏輯的操作
```

**禁止**：
- 不可 import streamlit
- 不可包含排序、篩選前 N 筆等業務邏輯（除非是 API 本身參數）
- 不可在資料層做 progress bar 操作

### 2.2 業務邏輯層 — `src/services/`

**檔案**：
- `chart.py`：Plotly 圖表生成函式庫（純輸入 data → 輸出 fig）
- `analogy_engine.py`：白話轉譯引擎（數值 → 生活化比喻）
- `revenue_analyzer.py`：營收分析（營收資料 → 分析結果）
- `news_summarizer.py`：新聞摘要（新聞列表 → 摘要文字）
- `adaptive_engine.py`：事件偵測、新鮮度檢查

**職責**：
- 接收 DataFrame/dict，回傳計算結果或圖表物件
- 所有圖表在這一層生成
- 所有數值計算在這一層完成

**介面規範**：
```python
# ✅ 正確：純函數，輸入 data → 輸出 fig
def create_revenue_trend_chart(revenue_df: pd.DataFrame) -> go.Figure:
    ...

# ✅ 正確：純函數，輸入數值 → 輸出文字
def get_gross_margin_analogy(margin: float) -> str:
    ...

# ❌ 錯誤：在 service 層用 st.plotly_chart()
# ❌ 錯誤：在 service 層用 st.spinner()
```

**禁止**：
- 不可 import streamlit
- 不可直接呼叫 FinMind API（必須透過 data layer）
- 不可有 side effect（寫檔、寫 cache 等）

### 2.3 路由層 — `src/pages/router.py`

**職責**：
- 讀取 `session_state["page"]` 決定顯示哪個 View
- 讀取 `session_state["stock_id"]` 決定顯示哪支股票
- 呼叫 `_router_base.get_stock_data()` 統一載入資料
- 管理「不需要特定股票的頁面」（分類瀏覽、ETF 專區、我的關注、事件儀表板）
- 處理頁面切換時的 loading 狀態

**資料流**：
```
session_state["stock_id"]
    ↓
router.load_and_render_page(client, stock_id)
    ↓
_router_base.get_stock_data(client, stock_id)  ← 統一入口
    ↓
檢查 get_stock_data 內部並行/分批邏輯
    ↓
FinMindClient → 快取 → 回傳 data dict
    ↓
交給對應的 View function
```

**規範**：
- Router 是唯一可以決定「什麼時候載入什麼資料」的地方
- 不可在 View 層重複載入已經在 router 層載好的資料
- 必須在頁面切換時顯示 `st.spinner`

### 2.4 展示層 — `src/pages/*.py`

**檔案**（每個檔案對應一個頁面）：
- `business_card.py`：公司名片
- `operation_checkup.py`：營運健檢
- `financial_health.py`：財務體質
- `peer_comparison.py`：同業比較
- `group_structure.py`：集團架構
- `category_browser.py`：分類瀏覽
- `etf_browser.py`：ETF 專區
- `etf_detail.py`：ETF 詳細
- `watchlist_page.py`：我的關注
- `event_dashboard.py`：事件儀表板

**職責**：
- 接收 `data` dict + `client`（如果需要額外查詢）
- 呼叫 `src/services/` 的函式生成圖表
- 用 Streamlit API 渲染 UI

**規範**：
```python
# ✅ 正確：View 接收 data dict，呼叫 service 生成圖表
def _render_business_card(data: dict, client: FinMindClient):
    st.markdown(f"## {data['stock_name']}")
    fig = create_revenue_pie_chart(data["monthly_revenue"])
    st.plotly_chart(fig)

# ✅ 正確：View 可以在需要時透過 client 額外查詢
# 但僅限於「該頁面專用」的小量查詢，不可重複 _router_base 已載入的全部資料
def _render_peer_comparison(data: dict, client: FinMindClient):
    benchmark_id = get_benchmark(data["industry"])
    benchmark_data = get_stock_data(client, benchmark_id)  # 額外查詢標竿
    ...

# ❌ 錯誤：在 View 中重新載入該頁面已經有的全部資料
# ❌ 錯誤：在 View 中呼叫 client.get_daily_price() 之類的基礎查詢（應在 router/base 統一做）
```

**禁止**：
- 不可直接讀寫 cache file
- 不可做複雜的數值計算（應在 service 層）
- 不可有業務邏輯（如判斷是否是集團企業，應在 service 層）

---

## 三、資料流規範

### 3.1 標準資料流

```
使用者操作（側邊欄 / 頁籤 / 搜尋）
    → st.session_state 更新
    → st.rerun()
    → router.load_and_render_page()
        → _router_base.get_stock_data()（單一入口）
            → FinMindClient（含快取）
            → 回傳 data dict
        → 選擇 View function
            → View 呼叫 services/ 生成圖表
            → View 用 st.* 渲染
```

### 3.2 禁止的反向依賴

```
❌ View → 直接 → Data layer（跳過 service）
❌ Service → 直接 → View（service 不可有 UI）
❌ Data layer → 直接 → View（data 不可有 UI）
❌ View → 寫入 → session_state 以外的狀態（用 st.session_state）
```

### 3.3 資料快取策略

| 資料類型 | 快取 TTL | 更新時機 |
|----------|----------|----------|
| 日收盤價 | 1 天 | 每日收盤後 |
| 月營收 | 1 天 | 每月 10 日後 |
| 財報 | 1 天 | 每季公布後 |
| 公司基本資訊 | 7 天 | 過期後更新 |
| 新聞 | 1 天 | 每日更新 |

**規範**：
- 快取由 `FinMindClient` 統一管理
- 不可在 View 或 Service 層自己做快取
- 不可在 View 層用 `st.cache_data`（會導致 session 間共享難以除錯）

---

## 四、頁面切換機制

### 4.1 State 管理

所有頁面狀態由 `session_state` 管理：

```python
# 全域 state
st.session_state["stock_id"]      # 目前股票代碼
st.session_state["page"]           # 目前頁面名稱
st.session_state["industry_filter"] # 產業篩選（如果使用）

# 頁面內 state（用前綴區分）
st.session_state["peer_benchmark"] # 同業比較的標竿
st.session_state["compare_stocks"] # 比較的股票列表
```

### 4.2 切換流程

```
側邊欄按鈕 / 頁籤按鈕
    → st.session_state["stock_id"] = sid  （如果需要）
    → st.session_state["page"] = page_name
    → st.rerun()  # 觸發整個頁面重繪
```

**原則**：
- 不使用 `st.switch_page()`（它會失去 session_state）
- 不手動清除不需要的 state
- 頁面切換時，router 負責用 `st.spinner` 包裝資料載入

### 4.3 獨立頁面

以下頁面不需要 `stock_id`，由 router 直接導向：
- `分類瀏覽`（`category_browser.py`）
- `ETF 專區`（`etf_browser.py`）
- `我的關注`（`watchlist_page.py`）
- `事件儀表板`（`event_dashboard.py`）

這些頁面自行管理自己的資料載入與 state。

---

## 五、錯誤處理分層

| 層級 | 處理方式 |
|------|----------|
| Data layer | API 失敗時回傳 None 或空 DataFrame，**不拋異常** |
| Service layer | 收到 None/空資料時回傳 None 或空 fig，**不拋異常** |
| View layer | 收到 None 時顯示 `st.info()` 或跳過該區塊，**不 crash** |
| Router layer | `get_stock_data` 回傳 None 時顯示 `st.error()` 並 return |

**原則**：任何層級都不可讓未捕獲的 exception 到達 Streamlit。

---

## 六、開發前架構檢查清單

在寫任何新代码之前：

- [ ] 確認放在正確的層（data / service / page / router）
- [ ] 確認沒有跨越層級直接向 API 或向 Streamlit
- [ ] 確認資料流方向正確（View → Service → Data，不可反向）
- [ ] 確認 error handling 在各層都到位
- [ ] 確認 session_state 管理在 router 或 View 層（不在 Data/Service 層）
- [ ] 確認按鈕 key 唯一
- [ ] 確認頁面切換有 spinner
- [ ] 確認快取由 FinMindClient 統一管理
- [ ] 沒有在 View 層用 `st.cache_data`（全域 cache 會影響其他 session）

---

*建立日期：2026-06-08*
*維護者：主 agent（PM）*
