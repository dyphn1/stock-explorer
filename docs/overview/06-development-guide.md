# 開發指南 — Stock Explorer

> **適用對象**: 開發者、AI Agent | **上次更新**: 2026-06-17

---

## 1. 環境設置

### 1.1 前置需求
- Python 3.11+
- Git
- （可選）uv 套件管理器

### 1.2 安裝步驟
```bash
# 1. Clone
git clone https://github.com/your-username/stock-explorer.git
cd stock-explorer

# 2. 建立虛擬環境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 3. 安裝依賴
pip install -e .

# 4. 啟動開發伺服器
streamlit run src/main.py
```

### 1.3 驗證環境
```bash
# 執行測試
uv run pytest

# 驗證語法
uv run python -c "import src; print('OK')"
```

---

## 2. 分層架構規範

### 2.1 嚴格分層
```
Presentation (src/pages/) → Routing (src/pages/router.py) → Services (src/services/) → Data (src/data/)
```

### 2.2 各層職責與禁止事項

#### Data Layer (`src/data/`)
```python
# ✅ 正確：返回 DataFrame
def get_daily_price(self, stock_id: str) -> pd.DataFrame: ...

# ✅ 正確：返回 None 表示無數據（不拋異常）
def get_latest_price(self, stock_id: str) -> dict | None: ...

# ❌ 錯誤：在 data layer 決定是否顯示 spinner
# ❌ 錯誤：在 data layer 做業務邏輯（如排序、取 top N）
```
- **禁止**：import streamlit、包含業務邏輯

#### Service Layer (`src/services/`)
```python
# ✅ 正確：純函數，輸入數據 → 輸出圖表
def create_revenue_trend_chart(revenue_df: pd.DataFrame) -> go.Figure: ...

# ✅ 正確：純函數，輸入值 → 輸出文字
def get_gross_margin_analogy(margin: float) -> str: ...

# ❌ 錯誤：在 service layer 使用 st.plotly_chart()
# ❌ 錯誤：在 service layer 直接呼叫 FinMind API
```
- **禁止**：import streamlit、直接呼叫 API、有 side effects

#### Routing Layer (`src/pages/router.py`)
- 唯一決定「何時載入什麼數據」的地方
- 管理頁面切換的 loading state
- **禁止**：直接產生 UI 元件

#### Presentation Layer (`src/pages/*.py`)
```python
# ✅ 正確：View 接收 data dict，呼叫 service 生成圖表
def _render_business_card(data: dict, client: FinMindClient):
    st.markdown(f"## {data['stock_name']}")
    fig = create_revenue_pie_chart(data["monthly_revenue"])
    st.plotly_chart(fig)

# ❌ 錯誤：在 View 重新載入 router 已載入的數據
# ❌ 錯誤：在 View 做複雜數值計算
```
- **禁止**：直接讀寫快取、複雜計算、業務邏輯

---

## 3. 編碼規範

### 3.1 命名慣例
- **檔案**：`snake_case.py`（如 `business_card.py`）
- **函數**：`snake_case`（如 `get_revenue_data`）
- **類**：`PascalCase`（如 `FinMindClient`）
- **常數**：`UPPER_SNAKE_CASE`（如 `MAX_RETRIES`）
- **i18n key**：`dot.notation`（如 `pages.business_card.title`）

### 3.2 字串處理
```python
# ✅ 正確：使用 i18n
from src.core.i18n import t
st.markdown(t("pages.business_card.title"))

# ❌ 錯誤：hardcoded 中文
st.markdown("公司名片")
```

### 3.3 錯誤處理
```python
# ✅ 正確：優雅降級
data = client.get_daily_price(stock_id)
if data is None or len(data) == 0:
    st.warning(t("errors.no_data"))
    return

# ❌ 錯誤：讓異常崩潰整個頁面
data = client.get_daily_price(stock_id)  # 可能拋異常
```

### 3.4 快取使用
```python
# ✅ 正確：透過 FinMindClient（內建快取）
client = FinMindClient()
data = client.get_daily_price(stock_id)

# ❌ 錯誤：直接讀寫 .cache/ 目錄
with open(".cache/some_file.json") as f: ...
```

---

## 4. 新增頁面流程

### 4.1 目前流程（需修改 3 處）
1. 在 `src/pages/` 建立新頁面檔案
2. 在 `src/pages/router.py` 新增 import
3. 在 `src/pages/router.py` 新增 if-elif 分支

### 4.2 目標流程（Plugin Chassis）
1. 在 `src/plugins/` 建立新 plugin
2. 繼承 `BasePlugin`，實作 `render()` 方法
3. 自動掃描註冊，**零修改路由邏輯**

---

## 5. 測試規範

### 5.1 測試分層
| 層級 | 檢查內容 | 通過標準 |
|------|----------|----------|
| **L0** | 語法、import、key 唯一性 | 必須在 commit 前通過 |
| **L1** | 頁面渲染（所有頁面不崩潰） | 必須在 handoff 前通過 |
| **L2** | 互動（按鈕、導航、表單） | 必須在 release 前通過 |
| **L3** | 視覺/UX（截圖分析） | Designer 審核 |

### 5.2 執行測試
```bash
# 全部測試
uv run pytest

# 特定檔案
uv run pytest tests/test_business_logic.py

# 特定標記
uv run pytest -m tone
```

---

## 6. Git 規範

### 6.1 Commit 風格
遵循 Angular-style Conventional Commits：
```
feat: add revenue pie chart to business card
fix: resolve cache invalidation in get_daily_price
refactor: extract business_card.py into sub-directory
docs: update architecture overview
test: add unit tests for analogy_engine
```

### 6.2 分支策略
- `main`：穩定版本
- `feature/Cxxx-<name>`：新功能
- `fix/Dxxx-<name>`：修復
- `refactor/TDxxx-<name>`：重構

---

## 7. AI Agent 協作規範

### 7.1 角色分工
| 角色 | 職責 | 模型 |
|------|------|------|
| **PM** | 協調、整合、分配工作 | owl-alpha |
| **Architect** | 架構分析、技術方案 | nemotron-3-super-120b |
| **Developer** | 實作、修復、重構 | owl-alpha |
| **Designer** | UX/UI 審核、視覺系統 | gemma-4-31b-it |
| **QA** | 驗證、測試、競品分析 | gemma-4-31b-it |
| **Challenger** | 交叉檢驗決策 | gpt-oss-120b |

### 7.2 工作流程
1. **PM** 讀取 `STATUS.md` 和 `docs/state/handoff.md`
2. **PM** 分派任務給各角色
3. **Architect** 分析技術可行性
4. **Developer** 實作
5. **QA** 驗證
6. **Challenger** 挑戰決策（3 輪）
7. **PM** 整合結果

### 7.3 文件限制
- `docs/state/*`：最多 100 行
- `docs/logs/*`：最多 200 行
- 超過時觸發 **Compression Cycle**：提煉至 `docs/adr/` 或 `docs/overview/`，然後截斷
