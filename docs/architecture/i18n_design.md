# i18n 架構設計文件

> 撰寫日期：2026-06-14
> 基於掃描結果：src/ 內 93 個 .py 檔案，共發現 **3,146 個** hardcoded 中文字串

---

## 1. 問題摘要

| 維度 | 數據 |
|---|---|
| 掃描檔案數 | 93 個 .py（src/ 全部） |
| Hardcoded 中文字串 | **3,146 個** |
| Hardcoded 英文字串（UI label）| ~200+ 個（division name, page name, status text） |
| 分佈 | pages/ 43 個檔案（最多）、services/ 47 個、data/ 2 個、main.py |

---

## 2. 架構設計

### 2.1 模組結構

```
src/core/i18n.py              # i18n 核心模組（唯一出入口）
locales/
├── zh-TW.yaml                # 繁體中文（預設）
└── en.yaml                   # 英文
```

**不使用資料夾分類（如 `locales/zh-TW/ui.yaml`）**——3,146 個字串看起來很多，但分檔案會增加查找成本。Daniel 偏好精簡，單一檔案 per locale 是最簡單的方案。未來如果真的超過 500 行再拆分。

### 2.2 src/core/i18n.py 設計

```python
"""
src/core/i18n.py
最簡 i18n 模組：讀取 YAML locale 檔，提供 t() 函數。
"""
from __future__ import annotations

import os
import yaml
import streamlit as st
from pathlib import Path

_LOCALE_DIR = Path(__file__).resolve().parent.parent.parent / "locales"

_locale_cache: dict[str, dict] = {}

def _load_locale(lang: str) -> dict:
    """載入指定語言的 YAML 檔案。"""
    if lang not in _locale_cache:
        path = _LOCALE_DIR / f"{lang}.yaml"
        if not path.exists():
            #  fallback 到 zh-TW
            path = _LOCALE_DIR / "zh-TW.yaml"
        with open(path, encoding="utf-8") as f:
            _locale_cache[lang] = yaml.safe_load(f) or {}
    return _locale_cache[lang]

def t(key: str, **kwargs) -> str:
    """
    翻譯函數。
    
    Usage:
        t("page.title")                    # "股識 Stock Explorer"
        t("metric.revenue_yoy", value=25)  # "營收年增率 {value}%"
        t("error.not_found", sid="9999")   # "找不到股票代號 9999"
    
    YAML 結構使用 dot-notation key，例如：
        page: { title: "股識 Stock Explorer" }
    key "page.title" → data["page"]["title"]
    
    ✨ 如果 key 找不到，回傳 key 本身（不 crash）。
    這在開發中很重要——可以看到哪個 key 還沒翻譯。
    """
    lang = st.session_state.get("lang", "zh-TW")
    data = _load_locale(lang)
    
    # 支援 nested key: "page.title" → data["page"]["title"]
    node = data
    for part in key.split("."):
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return key  # key not found → return key text
    
    text = str(node)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text

def get_available_locales() -> list[dict]:
    """回傳可用語言列表。"""
    return [
        {"code": "zh-TW", "name": "繁體中文", "label": "🇹🇼 繁體中文"},
        {"code": "en", "name": "English", "label": "🇺🇸 English"},
    ]

def set_lang(lang: str):
    """設定語言並清除快取觸發重新翻譯。"""
    st.session_state["lang"] = lang
    _locale_cache.clear()
```

**設計決策說明：**

| 決策 | 理由 |
|---|---|
| YAML 而非 JSON | 支援註解、多行字串（`\|`）、可讀性高 |
| Dot-notation key | `t("page.title")` 比 `t("page")["title"]` 簡潔，也避免嵌套 dict import |
| 單一檔案 per locale | 精簡原則。未來字串超過 500 行再考慮拆分 |
| key not found 回傳 key | 開發友好，不會因為缺翻譯而 crash session |
| `st.session_state["lang"]` 儲存語言 | Streamlit 原生整合，不需要額外 cookie/session 管理 |
| 快取機制 | `_locale_cache` 避免每次呼叫 t() 都重讀檔案 |

---

## 3. Locale 檔案格式設計

### 3.1 zh-TW.yaml 頂層結構

```yaml
# zh-TW.yaml — 繁體中文
# 本檔案包含所有 UI 顯示文字
# 規則：用詞統一、專業、不口語化

# ── App 全域 ──────────────────────────────────
app:
  title: "股識 Stock Explorer"
  subtitle: "認識一家公司，從這裡開始"
  search_placeholder: "例如：2330 或 台積電"
  search_label: "搜尋股票"
  loading: "載入中..."

# ── 頁面名稱（sidebar + navbar）──────────────
page:
  business_card: "名片"
  operation_checkup: "營運健檢"
  financial_health: "財務體質"
  peer_comparison: "同業比較"
  group_structure: "集團架構"
  category_browser: "分類瀏覽"
  etf_section: "ETF 專區"
  watchlist: "我的關注"
  event_dashboard: "事件儀表板"
  notification_center: "通知中心"
  investment_memo: "投資備忘錄"
  financial_wellness: "理財健康檢查"
  stock_screener: "股票探索"
  settings: "設定"
  sector_heatmap: "產業熱力圖"
  case_study: "案例研究"
  comprehension_check: "理解力測驗"
  academy: "學習學院"
  case_study_library: "歷史案例庫"
  first_visit_guide: "新手導覽"
  story_timeline: "故事時間軸"
  full_story_timeline: "完整故事時間軸"
  daily_story: "每日故事"
  revenue_tree: "營收結構樹"
  compare_stories: "同業比較故事"
  moat_comparison: "護城河比較"

# ── Sidebar 元素 ────────────────────────────
sidebar:
  hot_stocks: "🔥 熱門股票"
  hot_etfs: "🏷️ 熱門 ETF"
  disclaimer: "⚠️ 本工具僅供認識公司使用，不構成任何投資建議。<br>投資有風險，請自行評估。"

# ── 股票資訊標籤 ──────────────────────────────
stock:
  code: "代號"
  name: "名稱"
  industry: "產業"
  price: "股價"
  change: "漲跌"
  not_found: "找不到股票代號 {sid}"
  search_multiple: "找到多筆符合的股票："
  no_match: "找不到符合的股票"

# ── 財務指標名稱 ──────────────────────────────
metric:
  revenue: "營業收入"
  revenue_yoy: "營收年增率"
  revenue_monthly: "月營收"
  gross_margin: "毛利率"
  operating_margin: "營業利益率"
  net_margin: "淨利率"
  roe: "股東權益報酬率 (ROE)"
  per: "本益比 (PER)"
  pbr: "淨值比 (PBR)"
  dividend_yield: "殖利率"
  debt_ratio: "負債比"
  current_ratio: "流動比"
  eps: "每股盈餘 (EPS)"
  total_assets: "總資產"
  total_liabilities: "總負債"
  total_equity: "股東權益"
  operating_cash_flow: "營業現金流"
  investing_cash_flow: "投資現金流"
  financing_cash_flow: "籌資現金流"
  fcf: "自由現金流"

# ── 股利相關 ──────────────────────────────────
dividend:
  status_paid: "✓ 已發放"
  status_pending: "⏳ 待發放"
  status_unpaid: "⏳ 待發放"
  frequency_quarterly: "季配"
  frequency_annual: "年配"
  frequency_irregular: "不規則"
  no_record: "此公司暂無除權息紀錄"
  no_record_recent: "此公司近五年無配息紀錄"
  cash_dividend: "現金股利"
  stock_dividend: "股票股利"
  total_dividend: "合計股利"
  ex_date_label: "除息日"
  pay_date_label: "發放日"
  year: "年度"
  historical_record: "歷史除權息紀錄"
  latest_quarter: "最近一季"
  estimated_annual: "預估全年配息"
  dividend_yield_label: "殖利率"
  summary: "配息摘要"
  detail_expand: "📋 展開查看歷史除權息紀錄"

# ── 按鈕與操作 ────────────────────────────────
action:
  submit: "提交答案"
  retry: "重新測驗"
  reset: "重設"
  save: "儲存"
  cancel: "取消"
  back: "返回"
  go_to_detail: "前往下一課"
  review: "複習"
  start: "開始"
  share: "分享"
  copy_link: "複製分享連結"
  next_page: "下一頁"
  prev_page: "上一頁"

# ── 狀態訊息 ──────────────────────────────────
status:
  loading: "載入中..."
  loading_stock: "載入股票資料..."
  loading_page: "載入頁面..."
  checking_events: "🔍 檢查近期事件..."
  rate_limited: "⚠️ API 速率限制已達上限，部分資料可能無法載入。請稍後再試。"
  rate_limited_short: "⚠️ FinMind API 暫時受限，資料可能不完整。請稍後再試。"
  data_missing: "暫無資料"
  no_revenue_data: "暫無營收資料"
  no_price_data: "暫無股價資料"
  no_institutional_data: "暫無法人資料"
  no_peer_data: "目前沒有找到同產業的同業可比較"

# ── 時間軸 ────────────────────────────────────
timeline:
  label_1y: "1 年"
  label_3y: "3 年"
  label_5y: "5 年"
  label_all: "全部"
  filter_failed: "⚠️ 時間軸過濾失敗，已顯示全部資料"
  no_data_in_range: "📌 此時間範圍內無資料，已切換至全部資料"

# ── 錯誤訊息 ──────────────────────────────────
error:
  not_found: "找不到股票代號 {sid}"
  no_data: "無法取得資料"
  no_answer: "找不到測驗答案，請重新開始"
  no_course: "找不到課程內容"
  no_list_name: "請輸入清單名稱"
  list_exists: "清單名稱已存在或建立失敗"
  remove_failed: "移除失敗"
  settings_saved: "✅ 設定已儲存"
  api_error: "❌ API 錯誤：{message}"

# ── 結果/回饋 ─────────────────────────────────
result:
  score: "答對題數"
  accuracy: "正確率"
  excellent: "表現優異，在同產業中屬於前段班"
  good: "表現穩定，有改善空間"
  needs_attention: "需要留意，可能拖累整體表現"
  correct: "✅ 答對"
  wrong: "❌ 答錯"

# ── 配對/比較 ─────────────────────────────────
comparison:
  vs: "vs."
  industry_avg: "同業平均"
  rank: "排名"
  stronger: "優於同業"
  weaker: "落後同業"
  similar: "與同業相當"

# ── 財報科目 ──────────────────────────────────
financial_statement:
  revenue: "營業收入"
  gross_profit: "營業毛利"
  operating_income: "營業利益"
  net_income: "淨利"
  total_assets: "資產總計"
  total_liabilities: "負債總計"
  current_assets: "流動資產"
  current_liabilities: "流動負債"
  total_equity: "權益總計"

# ── 通知中心 ─────────────────────────────────
notification:
  title: "通知中心"
  subtitle: "追蹤你關注股票的重要事件與異動"
  mark_all_read: "已將所有通知標記為已讀"
  no_notification: "目前沒有通知"

# ── 投資備忘錄 ────────────────────────────────
memo:
  title: "投資備忘錄"
  add: "新增備忘"
  edit: "編輯備忘"
  delete: "刪除備忘"
  empty: "目前沒有任何備忘"

# ── 免責聲明 ─────────────────────────────────
disclaimer:
  general: "⚠️ 本工具僅供認識公司使用，所有數據來自公開資訊觀測站與 FinMind。不構成任何投資建議。投資有風險，請自行評估。"
  expert: "⚠️ 專家分析由 AI 輔助整理，僅供參考，不構成投資建議。"
  historical: "⚠️ 歷史情境為假設性試算，僅供教育用途，不構成投資建議。過去績效不代表未來表現。"
  feedback_positive: "感謝你的正面回饋！👍"
  feedback_negative: "感謝你的回饋，我們會持續改進！👎"
```

### 3.2 en.yaml 對應結構

```yaml
# en.yaml — English
#對應 zh-TW.yaml 的 key 結構，值改為英文

app:
  title: "Stock Explorer"
  subtitle: "Understanding a company starts here"
  search_placeholder: "e.g., 2330 or TSMC"
  search_label: "Search"
  loading: "Loading..."

page:
  business_card: "Overview"
  operation_checkup: "Operations"
  financial_health: "Financial Health"
  peer_comparison: "Peer Comparison"
  group_structure: "Corporate Structure"
  # ... 其餘對應

stock:
  not_found: "Stock ID {sid} not found"
  search_multiple: "Multiple stocks found:"
  # ...

metric:
  revenue: "Revenue"
  revenue_yoy: "YoY Revenue Growth"
  # ...

# ... 完整 zh-TW.yaml 的所有 key，值改為英文
```

---

## 4. Hardcoded 字串分類與對應 key 數量估計

| 分類 | 估計數量 | 說明 | key prefix |
|---|---|---|---|
| **Page labels** | 36 | 頁面名稱（sidebar 10 + navbar 26） | `page.*` |
| **Metric labels** | 40+ | 財務指標名稱（revenue, ROE, PER...） | `metric.*` |
| **Sidebar 元素** | 8 | 熱門股票/ETF 名稱 + disclaimer | `sidebar.*` |
| **Stock info** | 6 | 代號/名稱/產業相關 tag | `stock.*` |
| **Dividend 相關** | 18 | 配息狀態/頻率/發放日 | `dividend.*` |
| **Financial statement** | 12 | 損益表/BS 科目 | `financial_statement.*` |
| **Buttons / Actions** | 15 | 提交/儲存/取消等 | `action.*` |
| **Status / Loading** | 10 | spinner text, status info | `status.*` |
| **Error messages** | 12 | error/warning text | `error.*` |
| **Disclaimer** | 4 | 各類型免責聲明 | `disclaimer.*` |
| **Chart labels** | 30+ | 圖表 axis label, hover text | `chart.*` |
| **Comparison text** | 8 | vs, stronger/weaker | `comparison.*` |
| **Result/Feedback** | 8 | 測驗結果, 回饋語 | `result.*` |
| **Expert analysis** | 50+ | 每檔股票的專家分析文字（11 檔） | `expert.*` |
| **Historical scenarios** | 60+ | 歷史情境分析文字（11 檔 × 3 情境） | `scenario.*` |
| **Industry classification** | 40+ | 產業分類對照表 | 進入 `page.*` 或独立 `industry.*` |
| **Notification text** | 6 | 通知中心 UI | `notification.*` |
| **Glossary entries** | 30+ | 名詞解釋/比喻/例子 | `glossary.*` |
| **Unit labels** | 10 | 億/萬/張/元/% 組合 | formatter function, not i18n key |
| **HTML/CSS 內文字** | 5+ | 內嵌在 st.markdown HTML 中 | 視情況提取或不提取 |

**預計總 key 數：約 350-400 個 unique keys**
（3,146 個字串實例 → 大量重複 key + HTML fragment）

---

## 5. 遷移策略

### Phase 1：基礎建設
1. 建立 `src/core/i18n.py`
2. 建立 `locales/zh-TW.yaml`（完整覆蓋率）
3. 建立 `locales/en.yaml`（可後續逐步翻譯）
4. 在 `main.py` 中初始化 `session_state["lang"]`（預設 zh-TW）
5. 在 `main.py` sidebar 加入語言切換下拉選單

### Phase 2：核心字串遷移（需要優先處理）
- `main.py` 的 sidebar labels + welcome page（~30 個字串）
- `router.py` 的 page name list（1 個 list → `t()` 包裹）
- `_router_base.py` 的 UI helper（`_section_title`, `_explain_button`）
- 各 `pages/*.py` 的 page title + section header

### Phase 3：深度遷移
- 各 page 的 content 字串
- Expert analysis 文字的遷移（考慮改用 structural data 而非冗長字串）
- Glossary entries
- Chart labels

### Phase 4：英文翻譯

---

## 6. 待討論決策

### 6.1 Expert Analysis 和 Historical Scenarios

目前 `_expert_analysis.py` 和 `_historical_scenarios.py` 包含 11 檔股票的大量文字（每檔 ~15 行專家分析 + 9 個歷史情境）。

**問題**：這些文字應該：
- (A) 全部放入 locale yaml → yaml 會很臃腫（但仍有結構）
- (B) 放入獨立的 `data/expert_analysis.yaml` / `data/scenarios.yaml` 資料檔
- (C) 保留在 Python 模組中但用 `t()` 包裹
- (D) 改用結構化 data（欄位：company, strength[], risk[], 再由 template 組合）

**建議**：Option D。

將專家分析改為結構化格式：

```yaml
# data/expert_analysis.yaml
2330:
  title: "TSMC (2330) Expert Insights"
  position: "Global semiconductor foundry leader"
  strengths:
    - "Advanced process (7nm below) market share >90%"
    - "Core supplier to Apple, NVIDIA, AMD"
  risks:
    - "Overseas expansion capex burden"
    - "Geopolitical risks"
  outlook:
    - "AI/HPC demand driving growth"
    - "CoWoS advanced packaging capacity tight"
```

再由 View layer template 組合，支援多語言 template 切換。

### 6.2 Unit/格式化處理

金額單位（億/萬）不適合用 i18n key 處理，建議保持 `format_number()` 工具函式：

```python
def format_amount(value: float) -> str:
    """Format number with appropriate unit."""
    if value >= 1e8:
        return f"{value / 1e8:,.1f} {t('unit.hundred_million')}"  # 億 / billion
    elif value >= 1e4:
        return f"{value / 1e4:,.0f} {t('unit.ten_thousand')}"     # 萬 / million
    else:
        return f"{value:,.0f} {t('unit.yuan')}"                   # 元 / dollar
```

locale yaml 只需提供單位標籤：

```yaml
unit:
  hundred_million: "億"
  ten_thousand: "萬"
  yuan: "元"
  percent: "%"
  shares: "張"
```

---

## 7. 程式碼整合方式

### 6.1 在 main.py 中初始化

```python
# 在 main.py 頂部加入
from src.core.i18n import t, set_lang, get_available_locales

# 初始化語言
if "lang" not in st.session_state:
    st.session_state["lang"] = "zh-TW"
```

### 6.2 在 page 中取代方式

```python
# Before (hardcoded):
st.markdown(f"## 🏥 營運健檢 — {stock_name}")
st.info("暫無營收資料")

# After (i18n):
st.markdown(f"## {t('page.operation_checkup')} — {stock_name}")
st.info(t("status.no_revenue_data"))
```

### 6.3 Page name list 處理

```python
# Before:
nav_items = [
    ("📊", "名片", "sidebar_nav_home"),
    ("🗺️", "產業熱力圖", "sidebar_nav_sector"),
]

# After:
nav_items = [
    ("📊", t("page.business_card"), "sidebar_nav_home"),
    ("🗺️", t("page.sector_heatmap"), "sidebar_nav_sector"),
]
```

---

## 8. Checklist

- [ ] 建立 `src/core/i18n.py`
- [ ] 建立 `locales/zh-TW.yaml`（完整）
- [ ] 建立 `locales/en.yaml`（基本）
- [ ] `main.py` 加入語言初始化 + 選擇器
- [ ] `router.py` page name list 改為 `t()`
- [ ] `_router_base.py` helper 函數 i18n 化
- [ ] 各 page 檔案 title/header i18n 化
- [ ] 各 page 檔案 content/body i18n 化
- [ ] Expert analysis → structured data
- [ ] Historical scenarios → structured data
- [ ] Unit formatter 函數

---

*本文檔基於 2026-06-14 掃描 stock-explorer/src/*.py 的实际结果撰寫*
