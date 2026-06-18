# ADR-004: Plugin Chassis 架構

## 狀態
規劃中 → **已核准（待實施）**

## 日期
2026-06-14 → **更新：2026-06-18**

---

## 背景

`src/pages/router.py` 目前有 **355 行**，包含 **33 個 if-elif 分支**。新增一個頁面需要修改 **3 個地方**：

1. 新增 `import` 語句
2. 在 `PAGE_KEYS` 列表中添加 key
3. 在 `load_and_render_page()` 中添加 if-elif 分支

這嚴重違反了**開放-封閉原則（Open-Closed Principle）**：對擴展開放，但對修改不封閉。

此外，當前架構存在以下問題：
- 所有頁面函數集中在 `src/pages/` 目錄，難以區分「需要股票數據的頁面」和「獨立頁面」
- 導航渲染邏輯（`_render_navbar`、`_render_navbar_minimal`）與路由邏輯耦合
- 無法動態啟用/停用頁面（feature flag）
- 新增頁面時容易遺漏某處修改，導致運行時錯誤

---

## 決策

將每個頁面設計為獨立 **Plugin**，遵循統一協議，核心框架自動掃描、註冊、路由。

**核心原則：新增頁面 = 新增一個 plugin 目錄，零修改路由邏輯。**

---

## 目標架構

```
src/
├── core/                           # 核心框架層
│   ├── i18n.py                     # i18n 模組（已有）
│   ├── plugin_protocol.py          # Plugin 介面定義（新增）
│   └── plugin_registry.py          # Plugin 註冊表（新增）
│
├── plugins/                        # Plugin 目錄（新增，取代 pages/ 的路由功能）
│   ├── __init__.py                 # 套件標記
│   ├── business_card/              # 公司名片
│   │   ├── plugin.py               # BusinessCardPlugin(BasePlugin)
│   │   └── ...                     # 原有渲染邏輯（從 pages/ 遷移）
│   ├── operation_checkup/          # 營運健檢
│   │   └── plugin.py
│   ├── financial_health/           # 財務體質
│   │   └── plugin.py
│   ├── category_browser/           # 分類瀏覽（獨立頁面，不需要 stock_id）
│   │   └── plugin.py
│   └── ...                         # 其他頁面
│
├── pages/                          # 視圖層（逐步遷移）
│   ├── router.py                   # 頁面路由器（重構為使用 PluginRegistry）
│   ├── _router_base.py             # 共享工具（保留）
│   ├── url_sync.py                 # URL ↔ session 同步（保留）
│   └── *.py                        # 原有頁面文件（遷移完成後移除）
│
├── services/                       # 業務邏輯層（不變）
└── data/                           # 數據層（不變）
```

---

## Plugin Protocol 設計

### PluginMetadata（元數據）

```python
@dataclass(frozen=True)
class PluginMetadata:
    key: str                    # 唯一標識符（對應 i18n key: page.<key>）
    icon: str                   # 圖示（emoji）
    requires_stock_id: bool     # 是否需要股票代號
    requires_data: bool         # 是否需要預載 data dict
    category: str               # 分類：analysis | browse | tool | learn | system
    order: int                  # 排序權重（越小越靠前）
    enabled: bool               # 是否啟用（feature flag）
```

### PluginRenderContext（渲染上下文）

```python
@dataclass
class PluginRenderContext:
    page_key: str
    data: dict | None           # 預載的股票數據
    client: FinMindClient
    stock_id: str | None
```

### BasePlugin（抽象基類）

```python
class BasePlugin(ABC):
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata: ...

    @abstractmethod
    def render(self, ctx: PluginRenderContext) -> None: ...

    def can_render(self, ctx: PluginRenderContext) -> bool:
        """默認實現：檢查 stock_id / data 是否滿足要求"""
        ...
```

### 分類常量

| Category | 說明 | 示例頁面 |
|----------|------|----------|
| `analysis` | 股票分析類 | 名片、營運健檢、財務體質、同業比較 |
| `browse` | 瀏覽類 | 分類瀏覽、ETF 專區、產業熱力圖 |
| `tool` | 工具類 | 股票探索、投資備忘錄、理財健康檢查 |
| `learn` | 學習類 | 學習學院、案例研究、理解力測驗 |
| `system` | 系統類 | 設定、通知中心、事件儀表板 |

---

## PluginRegistry 設計

### 自動掃描策略

```
PluginRegistry.discover()
    → 遍歷 src/plugins/ 下的所有子目錄
    → 每個子目錄中查找 plugin.py
    → 導入模塊，查找所有 BasePlugin 子類
    → 實例化並註冊到 _plugins: dict[str, BasePlugin]
```

### 核心 API

```python
registry = PluginRegistry()
registry.discover()                          # 自動掃描，返回新註冊數量
registry.get("business_card")                # 根據 key 查找 plugin
registry.has("business_card")                # 檢查是否存在
registry.all_keys                            # 所有已註冊的 key 列表
registry.all_plugins                         # 所有 plugin（按 category + order 排序）
registry.get_by_category("analysis")         # 按分類獲取
```

### LegacyPageAdapter（向後兼容）

在遷移過渡期，可將現有的 `_render_*` 函數包裝為 Plugin，無需立即重構：

```python
adapter = LegacyPageAdapter(
    key="business_card",
    icon="🏢",
    category=PluginCategory.ANALYSIS,
    render_fn=_render_business_card,
    order=10,
)
registry.register(adapter)
```

---

## 重構後的 router.py

重構後的 `load_and_render_page()` 偽代碼：

```python
def load_and_render_page(client: FinMindClient, stock_id: str):
    page_key = st.session_state.get("page_key", "business_card")

    # 從 registry 查找 plugin
    plugin = registry.get(page_key)

    # 構建渲染上下文
    ctx = PluginRenderContext(
        page_key=page_key,
        data=None,
        client=client,
        stock_id=stock_id,
    )

    # 獨立頁面（不需要 stock_id）：直接渲染
    if not plugin.metadata.requires_stock_id:
        _render_navbar_minimal(page_key)
        plugin.render(ctx)
        return

    # 需要 stock_id 的頁面：載入數據
    with st.spinner(t("status.loading_stock")):
        data = get_stock_data(client, stock_id)
    if data is None:
        st.error(t("error.not_found", sid=stock_id))
        return

    # M5 事件偵測（保持不變）
    _run_event_detection(stock_id, data)

    # ETF 導向 ETF 詳細頁（保持不變）
    if _is_etf(stock_id, data):
        _render_navbar(data, page_key)
        registry.get("etf_detail").render(ctx)
        return

    # 渲染導航列 + 頁面
    _render_navbar(data, page_key)
    ctx.data = data
    plugin.render(ctx)
```

---

## 遷移計畫

### 階段 0：基礎骨架（TD-01a）✅ 當前
**目標**：建立 Plugin Protocol 和 Registry 骨架，不遷移任何頁面。

- [x] 建立 `src/core/plugin_protocol.py`
- [x] 建立 `src/core/plugin_registry.py`
- [x] 建立 `src/plugins/__init__.py`
- [ ] 更新 `docs/adr/004-plugin-chassis.md`（本文檔）

**風險**：無。不影響現有功能。

### 階段 1：向後兼容層（TD-01b）
**目標**：使用 `LegacyPageAdapter` 將現有頁面包裝為 Plugin，驗證 Registry 功能。

遷移順序（低風險優先）：
1. `category_browser` — 獨立頁面，不需要 stock_id
2. `settings` — 系統頁面，無數據依賴
3. `event_dashboard` — 獨立頁面
4. `notification_center` — 獨立頁面
5. `daily_market` — 獨立頁面

**驗證標準**：
- 所有 5 個頁面通過 `LegacyPageAdapter` 註冊後，導航和渲染正常
- 原有 `router.py` 的 if-elif 分支可被 registry 查找替代

### 階段 2：核心分析頁面遷移（TD-01c）
**目標**：遷移核心股票分析頁面到 `src/plugins/` 目錄。

遷移順序（按使用頻率）：
1. `business_card` — 最高頻，作為標杆
2. `operation_checkup`
3. `financial_health`
4. `peer_comparison`
5. `group_structure`
6. `story_timeline`
7. `full_story_timeline`
8. `revenue_tree`
9. `compare_stories`
10. `moat_comparison`
11. `debate_cards`

**每個頁面的遷移步驟**：
1. 在 `src/plugins/<name>/` 建立 `plugin.py`
2. 繼承 `BasePlugin`，定義 `metadata`
3. 將原有 `_render_*` 函數的邏輯移入 `render()` 方法
4. 更新 `router.py` 使用 `registry.get(name).render(ctx)`
5. 運行測試驗證

### 階段 3：瀏覽/工具/學習頁面遷移（TD-01d）
**目標**：遷移剩餘頁面。

遷移順序：
1. `etf_section` / `etf_browser`
2. `watchlist`
3. `investment_memo`
4. `financial_wellness`
5. `stock_screener`
6. `case_study` / `market_event_case_study`
7. `comprehension_check`
8. `academy`
9. `case_study_library`
10. `first_visit_guide`
11. `learn_first_gate`
12. `daily_story` / `investor_story_feed`
13. `sector_heatmap`

### 階段 4：清理（TD-01e）
**目標**：移除舊代碼，完成重構。

- [ ] 移除 `router.py` 中所有 if-elif 分支
- [ ] 移除 `router.py` 中所有 import（改為 registry 自動發現）
- [ ] 移除 `PAGE_KEYS` 列表（改為 `registry.all_keys`）
- [ ] 移除 `src/pages/` 中已遷移的 `.py` 文件
- [ ] 更新 `url_sync.py` 的 `VALID_PAGES`（改為從 registry 動態獲取）
- [ ] 更新 `main.py` 的 sidebar nav_items（改為從 registry 動態獲取）
- [ ] 全面測試

---

## 頁面分類與排序

| Key | Category | Order | requires_stock_id | requires_data | Icon |
|-----|----------|-------|-------------------|---------------|------|
| business_card | analysis | 10 | ✅ | ✅ | 🏢 |
| operation_checkup | analysis | 20 | ✅ | ✅ | 🔧 |
| financial_health | analysis | 30 | ✅ | ✅ | 💪 |
| peer_comparison | analysis | 40 | ✅ | ✅ | 👥 |
| group_structure | analysis | 50 | ✅ | ✅ | 🏗️ |
| story_timeline | analysis | 60 | ✅ | ✅ | 📅 |
| full_story_timeline | analysis | 65 | ✅ | ✅ | 📆 |
| revenue_tree | analysis | 70 | ✅ | ✅ | 🌳 |
| compare_stories | analysis | 80 | ✅ | ✅ | 📖 |
| moat_comparison | analysis | 90 | ✅ | ✅ | 🏰 |
| debate_cards | analysis | 100 | ✅ | ✅ | 🃏 |
| category_browser | browse | 10 | ❌ | ❌ | 🗺️ |
| etf_section | browse | 20 | ❌ | ❌ | 🏷️ |
| sector_heatmap | browse | 30 | ❌ | ❌ | 🔥 |
| daily_market | browse | 40 | ❌ | ❌ | 📈 |
| watchlist | tool | 10 | ❌ | ❌ | 📋 |
| investment_memo | tool | 20 | ❌ | ❌ | 📝 |
| financial_wellness | tool | 30 | ❌ | ❌ | 💰 |
| stock_screener | tool | 40 | ❌ | ❌ | 🔎 |
| case_study | learn | 10 | ❌ | ❌ | 📚 |
| comprehension_check | learn | 20 | ❌ | ❌ | ✅ |
| academy | learn | 30 | ❌ | ❌ | 🎓 |
| case_study_library | learn | 40 | ❌ | ❌ | 📖 |
| first_visit_guide | learn | 50 | ❌ | ❌ | 👋 |
| learn_first_gate | learn | 60 | ❌ | ❌ | 🚪 |
| daily_story | learn | 70 | ❌ | ❌ | 📰 |
| event_dashboard | system | 10 | ❌ | ❌ | 📊 |
| notification_center | system | 20 | ❌ | ❌ | 🔔 |
| settings | system | 30 | ❌ | ❌ | ⚙️ |

---

## 理由

1. **開放-封閉原則**：新增功能不需修改現有程式碼，只需新增 plugin 目錄
2. **獨立開發**：每個 plugin 可獨立開發/測試，降低耦合
3. **動態啟用/停用**：通過 `metadata.enabled` 實現 feature flag
4. **漸進式遷移**：`LegacyPageAdapter` 允許逐步遷移，降低風險
5. **類型安全**：`PluginProtocol` + `BasePlugin` 提供靜態和運行時雙重檢查
6. **自動發現**：無需手動註冊，減少遺漏風險

## 後果

### 正面
- ✅ 新增/移除功能 = 新增/移除 plugin 目錄，零修改路由邏輯
- ✅ 可獨立開發/測試單一 feature
- ✅ 動態啟用/停用 feature（通過 `enabled` 屬性）
- ✅ 頁面元數據集中管理（icon、order、category）
- ✅ 導航自動從 registry 生成，消除 `PAGE_KEYS` 與路由不同步的風險

### 風險與緩解
- ⚠️ **一次性重構成本**：緩解：分 5 個階段漸進遷移，每階段可獨立驗證
- ⚠️ **團隊需要理解 plugin 概念**：緩解：提供清晰的文檔和 `LegacyPageAdapter` 示例
- ⚠️ **Streamlit session_state 與 Plugin 生命週期耦合**：緩解：`PluginRenderContext` 封裝所有狀態，plugin 不直接訪問 session_state
- ⚠️ **自動掃描可能導入不需要的模塊**：緩解：只掃描 `src/plugins/` 目錄，每個 plugin 必須有 `plugin.py`

---

## 相關文件

- `src/core/plugin_protocol.py` — Plugin Protocol 定義
- `src/core/plugin_registry.py` — Plugin Registry 實現
- `src/plugins/__init__.py` — Plugin 目錄標記
- `src/pages/router.py` — 待重構的路由器
- `docs/overview/02-architecture.md` — 系統架構文件
- `docs/overview/06-development-guide.md` — 開發指南
