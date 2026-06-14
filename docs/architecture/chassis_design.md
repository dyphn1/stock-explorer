# Plugin-based Chassis 架構設計文件

> 撰寫日期：2026-06-14
> 基於掃描結果：router.py 有 274 行，其中 26 個 `if page ==` + 9 個 `elif page ==`，共 33 個條件分支

---

## 1. 問題摘要

### 1.1 router.py 的 if-elif 問題

```python
# 目前 router.py 的結構（簡化）：
def load_and_render_page(client, stock_id):
    page = st.session_state.get("page", "名片")
    
    # ── 17 個「不需要 stock_id」的頁面 ──
    if page == "分類瀏覽":
        _render_navbar_minimal(page)
        _render_category_browser(client)
        return
    if page == "ETF 專區":
        ...
        return
    # ... 還有 15 個
    
    # ── 需要 stock_id 的頁面 ──
    data = get_stock_data(client, stock_id)
    if data is None:
        st.error(f"找不到股票代號 {stock_id}")
        return
    
    # ── 16 個「需要 stock_id」的頁面 ──
    if page == "名片":
        _render_business_card(data, client)
    elif page == "營運健檢":
        _render_operation_checkup(data)
    elif page == "財務體質":
        _render_financial_health(data)
    # ... 還有 13 個
```

**問題：**
1. 新增一個頁面需要修改 3 個地方：import、page name list、if-elif 分支
2. 頁面名稱在 3 個地方重複定義（navbar list × 2 + if-elif）
3. 無法獨立開發/測試單個 feature
4. 無法動態啟用/停用 feature

### 1.2 目錄結構問題

```
src/
├── main.py                    # 入口（sidebar + search + welcome）
├── data/
│   ├── finmind_client.py      # API client
│   └── batch_api.py           # 批次 API
├── pages/
│   ├── router.py              # 274 行 if-elif 路由器
│   ├── _router_base.py        # 共享工具（data fetch + UI helpers）
│   ├── url_sync.py            # URL ↔ session sync
│   ├── business_card/         # 名片（已拆分為 sub-modules）
│   │   ├── __init__.py
│   │   ├── _main.py
│   │   ├── _helpers.py
│   │   ├── _expert_analysis.py
│   │   ├── _historical_scenarios.py
│   │   ├── _sections.py
│   │   ├── _study_log.py
│   │   └── _sections/         # 7 個 section 檔案
│   ├── operation_checkup.py   # 營運健檢（單檔 200+ 行）
│   ├── financial_health.py    # 財務體質（單檔 300+ 行）
│   ├── peer_comparison.py     # 同業比較（單檔 400+ 行）
│   ├── group_structure.py     # 集團架構
│   ├── category_browser.py    # 分類瀏覽
│   ├── etf_browser.py         # ETF 瀏覽器
│   ├── etf_detail.py          # ETF 詳細
│   ├── watchlist_page.py      # 我的關注
│   ├── event_dashboard.py     # 事件儀表板
│   ├── notification_center.py # 通知中心
│   ├── settings.py            # 設定
│   ├── investment_memo.py     # 投資備忘錄
│   ├── financial_wellness.py  # 理財健康檢查
│   ├── comprehension_check.py # 理解力測驗
│   ├── market_event_case_study.py
│   ├── stock_screener.py      # 股票探索
│   ├── first_visit_guide.py   # 新手導覽
│   ├── company_timeline.py    # 公司時間軸
│   ├── story_timeline.py      # 故事時間軸
│   ├── compare_stories.py     # 同業比較故事
│   ├── moat_comparison.py     # 護城河比較
│   ├── revenue_tree.py        # 營收結構樹
│   ├── sector_heatmap.py      # 產業熱力圖
│   ├── academy.py             # 學習學院
│   ├── case_study_library.py  # 歷史案例庫
│   ├── investor_story_feed.py # 每日故事
│   └── timeline_controls.py   # 時間軸控制
└── services/
    ├── dividend_analyzer.py
    ├── financial_metrics.py
    ├── chart.py / chart_stock.py / chart_market.py
    ├── adaptive_engine.py
    ├── delta_engine.py
    ├── health_scoring.py
    ├── moat_analyzer.py
    ├── revenue_analyzer.py
    ├── risk_analyzer.py
    ├── analogy_engine.py
    ├── metric_explainer.py
    ├── glossary_service.py
    ├── settings_service.py
    ├── watchlist.py
    ├── validation.py
    ├── ...（共 47 個 service 檔案）
    └── llm/
        ├── base.py
        ├── factory.py
        └── template_provider.py
```

---

## 2. 目標架構

### 2.1 概念圖

```
┌─────────────────────────────────────────────────────────┐
│                    main.py (Entry)                       │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Chassis (src/core/chassis.py)        │   │
│  │                                                    │   │
│  │  ┌─────────┐  ┌──────────┐  ┌─────────────────┐ │   │
│  │  │Registry │  │ Lifecycle│  │ State Management│ │   │
│  │  │         │  │ Manager  │  │                 │ │   │
│  │  └────┬────┘  └──────────┘  └─────────────────┘ │   │
│  │       │                                           │   │
│  │  ┌────┴──────────────────────────────────────┐   │   │
│  │  │           Plugin Protocol                  │   │   │
│  │  │  name, icon, render(), requires_stock_id   │   │   │
│  │  └────┬──────────┬──────────┬──────────┬─────┘   │   │
│  └───────┼──────────┼──────────┼──────────┼─────────┘   │
│          │          │          │          │               │
│     ┌────┴───┐ ┌───┴────┐ ┌──┴─────┐ ┌──┴──────┐      │
│     │Plugin A│ │Plugin B│ │Plugin C│ │Plugin D │      │
│     │名片    │ │ETF專區 │ │分類瀏覽│ │設定     │      │
│     └────────┘ └────────┘ └────────┘ └─────────┘      │
└─────────────────────────────────────────────────────────┘
```

### 2.2 目標目錄結構

```
src/
├── core/                        # ← 新增：核心框架層
│   ├── __init__.py
│   ├── chassis.py               # Chassis 主類（PluginRegistry + LifecycleManager）
│   ├── plugin_protocol.py       # Plugin 介面定義（Protocol class）
│   ├── i18n.py                  # i18n 模組
│   ├── state.py                 # 狀態管理（session_state 封裝）
│   └── di.py                    # 依賴注入容器
│
├── data/                        # 資料存取層（不變）
│   ├── finmind_client.py
│   └── batch_api.py
│
├── services/                    # 業務邏輯層（不變，但會減少）
│   ├── dividend_analyzer.py
│   ├── financial_metrics.py
│   ├── chart_stock.py
│   ├── chart_market.py
│   ├── adaptive_engine.py
│   ├── delta_engine.py
│   ├── health_scoring.py
│   ├── moat_analyzer.py
│   ├── revenue_analyzer.py
│   ├── risk_analyzer.py
│   ├── analogy_engine.py
│   ├── metric_explainer.py
│   ├── glossary_service.py
│   ├── settings_service.py
│   ├── watchlist.py
│   ├── validation.py
│   └── llm/
│       ├── base.py
│       ├── factory.py
│       └── template_provider.py
│
├── plugins/                     # ← 新增：Plugin 模組（取代 pages/ 的大部分功能）
│   ├── __init__.py              # 自動掃描 + 註冊所有 plugin
│   ├── _base.py                 # BasePlugin 抽象類
│   ├── _registry.py             # Plugin registry（內部使用）
│   │
│   ├── business_card/           # 名片 plugin
│   │   ├── __init__.py          # 導出 plugin class
│   │   ├── plugin.py            # BusinessCardPlugin(BasePlugin)
│   │   ├── _main.py             # 原有渲染邏輯
│   │   ├── _helpers.py
│   │   ├── _expert_analysis.py
│   │   ├── _historical_scenarios.py
│   │   ├── _sections.py
│   │   ├── _study_log.py
│   │   └── _sections/
│   │       ├── __init__.py
│   │       ├── _detail.py
│   │       ├── _financial.py
│   │       ├── _health.py
│   │       ├── _historical_pattern.py
│   │       ├── _moat.py
│   │       ├── _story.py
│   │       └── _summary.py
│   │
│   ├── operation_checkup/       # 營運健檢 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── financial_health/        # 財務體質 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── peer_comparison/         # 同業比較 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── group_structure/         # 集團架構 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── revenue_tree/            # 營收結構樹 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── compare_stories/         # 同業比較故事 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── moat_comparison/         # 護城河比較 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── company_timeline/        # 公司時間軸 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── story_timeline/          # 故事時間軸 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── etf_detail/              # ETF 詳細 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── category_browser/        # 分類瀏覽 plugin（不需要 stock_id）
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── etf_browser/             # ETF 瀏覽器 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── watchlist/               # 我的關注 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── event_dashboard/         # 事件儀表板 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── notification_center/     # 通知中心 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── investment_memo/         # 投資備忘錄 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── financial_wellness/      # 理財健康檢查 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── comprehension_check/     # 理解力測驗 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── market_event_case_study/ # 案例研究 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── stock_screener/          # 股票探索 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── first_visit_guide/       # 新手導覽 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── investor_story_feed/     # 每日故事 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── academy/                 # 學習學院 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── case_study_library/      # 歷史案例庫 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   ├── sector_heatmap/          # 產業熱力圖 plugin
│   │   ├── __init__.py
│   │   └── plugin.py
│   │
│   └── settings/                # 設定 plugin
│       ├── __init__.py
│       └── plugin.py
│
├── ui/                          # ← 新增：共享 UI 元件層
│   ├── __init__.py
│   ├── components.py            # 共用 UI 元件（card, badge, tooltip）
│   ├── navbar.py                # 頂部導航列
│   ├── sidebar.py               # 側邊欄
│   └── fab.py                   # Floating Action Button
│
└── main.py                      # 入口（大幅簡化）
```

---

## 3. Plugin Protocol 設計

### 3.1 plugin_protocol.py

```python
"""
src/core/plugin_protocol.py
Plugin 介面定義。所有 plugin 必須實作此 Protocol。
"""
from __future__ import annotations

from typing import Protocol, Optional
from dataclasses import dataclass, field


class Plugin(Protocol):
    """所有 feature plugin 必須實作的介面。"""

    # ── 元資料 ──────────────────────────────────
    @property
    def name(self) -> str:
        """Plugin 唯一識別名稱（對應 session_state['page']）。"""
        ...

    @property
    def icon(self) -> str:
        """圖示（emoji 或 icon name）。"""
        ...

    @property
    def requires_stock_id(self) -> bool:
        """是否需要 stock_id 才能渲染。
        - True: 股票相關頁面（名片、營運健檢...）
        - False: 全域頁面（分類瀏覽、設定...）
        """
        ...

    @property
    def category(self) -> str:
        """分類：'stock'（股票頁）或 'global'（全域頁）。"""
        ...

    @property
    def order(self) -> int:
        """排序權重（越小越前面）。"""
        ...

    # ── 生命週期 ────────────────────────────────
    def render(self, context: PluginContext) -> None:
        """渲染 plugin 內容。
        
        context 包含所有需要的依賴：
        - context.client: FinMindClient
        - context.stock_id: Optional[str]
        - context.data: Optional[dict]  (已預載的股票資料)
        - context.session_state: Streamlit session_state
        """
        ...


@dataclass
class PluginContext:
    """傳遞給 plugin render() 的上下文物件。"""
    client: object                    # FinMindClient
    stock_id: Optional[str] = None
    data: Optional[dict] = None      # 預載的股票資料（requires_stock_id=True 時有值）
    session_state: dict = field(default_factory=dict)  # st.session_state proxy
```

### 3.2 BasePlugin 抽象類

```python
"""
src/plugins/_base.py
BasePlugin：提供共通功能的抽象基底類。
"""
from __future__ import annotations

import streamlit as st
from abc import ABC, abstractmethod
from src.core.plugin_protocol import Plugin, PluginContext


class BasePlugin(ABC, Plugin):
    """所有 plugin 的基底類。子類只需實作必要方法。"""

    # 子類可覆寫
    requires_stock_id: bool = True
    category: str = "stock"
    order: int = 100
    icon: str = "📄"

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    def render(self, context: PluginContext) -> None:
        """預設渲染流程：show loading → call _render_content()。"""
        try:
            self._render_content(context)
        except Exception as e:
            st.error(f"⚠️ {self.name} 載入失敗：{str(e)}")
            # 不 crash 整個 app，只顯示 localized error

    @abstractmethod
    def _render_content(self, context: PluginContext) -> None:
        """子類實作實際渲染邏輯。"""
        ...


class StockPlugin(BasePlugin):
    """需要 stock_id 的 plugin 基底類。"""
    requires_stock_id: True
    category: str = "stock"


class GlobalPlugin(BasePlugin):
    """不需要 stock_id 的 plugin 基底類。"""
    requires_stock_id: False
    category: str = "global"
```

---

## 4. Chassis 設計

### 4.1 chassis.py

```python
"""
src/core/chassis.py
核心框架：PluginRegistry + LifecycleManager + StateManager

Daniel 偏好精簡，所以 Chassis 是一個整合入口，
內部包含 registry、lifecycle、state 三個子系統。
"""
from __future__ import annotations

import streamlit as st
import importlib
import pkgutil
from pathlib import Path
from typing import Optional

from src.core.plugin_protocol import Plugin, PluginContext


class PluginRegistry:
    """Plugin 註冊中心。支援動態載入、註冊、註銷。"""

    def __init__(self):
        self._plugins: dict[str, Plugin] = {}
        self._load_errors: list[str] = []

    def register(self, plugin: Plugin) -> None:
        """註冊一個 plugin。"""
        if plugin.name in self._plugins:
            raise ValueError(f"Plugin '{plugin.name}' 已存在")
        self._plugins[plugin.name] = plugin

    def unregister(self, name: str) -> None:
        """註銷一個 plugin。"""
        self._plugins.pop(name, None)

    def get(self, name: str) -> Optional[Plugin]:
        """取得 plugin。"""
        return self._plugins.get(name)

    def get_all(self) -> list[Plugin]:
        """取得所有已註冊 plugin（依 order 排序）。"""
        return sorted(self._plugins.values(), key=lambda p: p.order)

    def get_stock_plugins(self) -> list[Plugin]:
        """取得需要 stock_id 的 plugin。"""
        return [p for p in self.get_all() if p.requires_stock_id]

    def get_global_plugins(self) -> list[Plugin]:
        """取得不需要 stock_id 的 plugin。"""
        return [p for p in self.get_all() if not p.requires_stock_id]

    def auto_discover(self, package_name: str = "src.plugins") -> int:
        """
        自動掃描 package 下的所有子模組，
        找到有 register(registry) 呼叫的 plugin.py 並載入。
        
        回傳成功載入的 plugin 數量。
        """
        count = 0
        try:
            package = importlib.import_module(package_name)
            package_path = Path(package.__file__).parent
        except ImportError as e:
            self._load_errors.append(f"無法載入 package {package_name}: {e}")
            return 0

        for finder, module_name, is_pkg in pkgutil.walk_packages(
            str(package_path), prefix=f"{package_name}."
        ):
            if module_name.endswith(".plugin"):
                try:
                    mod = importlib.import_module(module_name)
                    # 每個 plugin.py 應在 module level 呼叫 register()
                    # 或由 chassis 顯式呼叫
                    if hasattr(mod, "register_plugin"):
                        mod.register_plugin(self)
                        count += 1
                except Exception as e:
                    self._load_errors.append(f"載入 {module_name} 失敗: {e}")

        return count

    @property
    def load_errors(self) -> list[str]:
        return list(self._load_errors)


class Chassis:
    """
    核心框架整合入口。
    
    Usage:
        chassis = Chassis()
        chassis.discover_plugins()    # 自動掃描 + 註冊
        chassis.render_current_page() # 渲染當前頁面
    """

    def __init__(self):
        self.registry = PluginRegistry()
        self._client = None

    def discover_plugins(self) -> int:
        """自動掃描並註冊所有 plugin。"""
        return self.registry.auto_discover("src.plugins")

    def set_client(self, client) -> None:
        """注入 FinMindClient。"""
        self._client = client

    def get_current_page(self) -> str:
        """取得當前頁面名稱。"""
        return st.session_state.get("page", self._default_page)

    @property
    def _default_page(self) -> str:
        """預設頁面（第一個 stock plugin）。"""
        stock_plugins = self.registry.get_stock_plugins()
        return stock_plugins[0].name if stock_plugins else ""

    def render_current_page(self, stock_id: Optional[str] = None) -> None:
        """
        渲染當前頁面。
        這是 main.py 唯一需要呼叫的渲染方法。
        """
        page_name = self.get_current_page()
        plugin = self.registry.get(page_name)

        if plugin is None:
            st.error(f"頁面 '{page_name}' 不存在")
            return

        # 建立 context
        context = PluginContext(
            client=self._client,
            stock_id=stock_id,
            session_state=dict(st.session_state),
        )

        # 如果需要 stock_id 但沒提供，顯示歡迎頁
        if plugin.requires_stock_id and not stock_id:
            self._render_welcome()
            return

        # 如果需要 stock_id，預載資料
        if plugin.requires_stock_id and stock_id:
            from src.pages._router_base import get_stock_data
            with st.spinner("載入股票資料..."):
                context.data = get_stock_data(self._client, stock_id)
            if context.data is None:
                st.error(f"找不到股票代號 {stock_id}")
                return

        # 渲染 plugin
        plugin.render(context)

    def _render_welcome(self) -> None:
        """歡迎頁面（沒有選股時）。"""
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;">
            <h1>📊 股識</h1>
            <p style="font-size:1.3rem;color:#7F8C8D;margin-top:1rem;">
                認識一家公司，從這裡開始
            </p>
        </div>
        """, unsafe_allow_html=True)

    def get_nav_items(self) -> list[tuple[str, str, str]]:
        """
        取得 sidebar 導航項目。
        Returns: [(icon, label, page_name), ...]
        """
        items = []
        for p in self.registry.get_all():
            items.append((p.icon, p.name, p.name))
        return items
```

---

## 5. Plugin 實作範例

### 5.1 business_card/plugin.py

```python
"""
src/plugins/business_card/plugin.py
名片 plugin：註冊到 chassis，不需要修改 router.py。
"""
from src.plugins._base import StockPlugin
from src.core.plugin_protocol import PluginContext


class BusinessCardPlugin(StockPlugin):
    name = "名片"
    icon = "📊"
    order = 10

    def _render_content(self, context: PluginContext) -> None:
        from src.plugins.business_card._main import render_business_card
        render_business_card(context.data, context.client)


# ── 註冊函數（由 chassis.auto_discover 呼叫）──
def register_plugin(registry) -> None:
    registry.register(BusinessCardPlugin())
```

### 5.2 settings/plugin.py

```python
"""
src/plugins/settings/plugin.py
設定 plugin：全域頁面，不需要 stock_id。
"""
from src.plugins._base import GlobalPlugin
from src.core.plugin_protocol import PluginContext


class SettingsPlugin(GlobalPlugin):
    name = "設定"
    icon = "⚙️"
    order = 999  # 最後
    category = "global"

    def _render_content(self, context: PluginContext) -> None:
        from src.pages.settings import render_settings_page
        render_settings_page()


def register_plugin(registry) -> None:
    registry.register(SettingsPlugin())
```

### 5.3 category_browser/plugin.py

```python
"""
src/plugins/category_browser/plugin.py
分類瀏覽 plugin：全域頁面。
"""
from src.plugins._base import GlobalPlugin
from src.core.plugin_protocol import PluginContext


class CategoryBrowserPlugin(GlobalPlugin):
    name = "分類瀏覽"
    icon = "📈"
    order = 30
    category = "global"

    def _render_content(self, context: PluginContext) -> None:
        from src.pages.category_browser import _render_category_browser
        _render_category_browser(context.client)


def register_plugin(registry) -> None:
    registry.register(CategoryBrowserPlugin())
```

---

## 6. main.py 簡化後的樣子

```python
"""
股識 Stock Explorer
Streamlit 入口 — Plugin-based Chassis 版本
"""
import sys
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import streamlit as st
from src.core.chassis import Chassis
from src.data.finmind_client import FinMindClient
from src.services.validation import validate_stock_id

# ── 頁面設定 ──────────────────────────────────────────
st.set_page_config(
    page_title="股識 Stock Explorer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────
# ...（不變）

# ── 初始化 Chassis ────────────────────────────────────
@st.cache_resource
def get_chassis() -> Chassis:
    chassis = Chassis()
    count = chassis.discover_plugins()
    if chassis.registry.load_errors:
        for err in chassis.registry.load_errors:
            st.toast(f"⚠️ Plugin load error: {err}")
    return chassis

@st.cache_resource
def get_client() -> FinMindClient:
    return FinMindClient(cache_dir=".cache")

chassis = get_chassis()
client = get_client()
chassis.set_client(client)

# ── Sidebar ───────────────────────────────────────────
# 使用 chassis.get_nav_items() 動態生成導航
with st.sidebar:
    st.markdown("## 🔍 股識")
    st.markdown("*認識一家公司，從這裡開始*")
    st.markdown("---")
    
    search_input = st.text_input(
        "搜尋股票",
        placeholder="例如：2330 或 台積電",
        label_visibility="collapsed",
        key="sidebar_search",
    )
    
    st.markdown("---")
    st.markdown("### 頁面導航")
    
    # 動態從 registry 取得導航項目
    for icon, label, page_name in chassis.get_nav_items():
        if st.button(f"{icon} {label}", key=f"nav_{page_name}", use_container_width=True):
            st.session_state["page"] = page_name
            st.rerun()
    
    # ... 熱門股票/ETF、disclaimer 等

# ── 主內容 ────────────────────────────────────────────
stock_id = _resolve_stock_id(search_input, client)  # 提取為 helper
chassis.render_current_page(stock_id)
```

---

## 7. 遷移路徑

### Phase 1：建立核心框架
1. 建立 `src/core/plugin_protocol.py`
2. 建立 `src/core/chassis.py`（PluginRegistry + Chassis）
3. 建立 `src/plugins/_base.py`（BasePlugin, StockPlugin, GlobalPlugin）
4. 建立 `src/plugins/__init__.py`

### Phase 2：逐頁遷移（每次 1-2 個 plugin）
1. 建立 `src/plugins/<name>/plugin.py`
2. 將原有 `_render_<name>()` 函數包裝進 Plugin class
3. 在 `plugin.py` 中實作 `register_plugin(registry)`
4. 測試：確認 `chassis.discover_plugins()` 能找到並正確渲染
5. 從 `router.py` 移除對應的 if-elif 分支

### Phase 3：清理
1. 當所有頁面都遷移完畢後，刪除 `router.py`
2. 將 `pages/` 中已遷移的檔案標記為 deprecated
3. 保留 `_router_base.py` 的 helper 函數（供 plugins 使用）

### Phase 4：FAB 整合
1. 根據 design_review_round18 的設計，實作 FAB component
2. stock plugin 的導航改為透過 FAB 而非 navbar
3. global plugin 的導航保留在 sidebar

---

## 8. 設計決策說明

| 決策 | 理由 |
|---|---|
| Protocol + ABC 並用 | Protocol 提供 structural typing（不需繼承），ABC 提供預設實作。plugin 可選繼承 BasePlugin 或直接實作 Protocol |
| `register_plugin()` 函數 | 每個 plugin.py 暴露 `register_plugin(registry)` 函數，由 `auto_discover` 顯式呼叫。比 module-level side effect 更清晰 |
| `PluginContext` dataclass | 避免 plugin 直接依賴 `st.session_state`（可測試），也避免參數列表過長 |
| 保留 `_router_base.py` | helper 函數（`_section_title`, `_explain_button`, `_白话_card` 等）被大量 plugin 共用，不需要搬動 |
| 不引入第三方 plugin 框架 | Daniel 偏好精簡。pluggy / stevedore 等框架過度設計，手寫 registry 更輕量 |
| `requires_stock_id` flag | 區分兩種頁面類型，影響：(1) 是否需要預載股票資料 (2) 是否在 FAB 中顯示 (3) 是否需要 navbar |
| `order` 屬性 | 控制 sidebar/navbar 排序，避免硬編碼順序 |
| 錯誤隔離 | `BasePlugin.render()` 包 try-except，單個 plugin 失敗不影響整個 app |

---

## 9. 與 i18n 的整合

Plugin 架構和 i18n 架構是正交的：

```python
# plugin.py 中使用 i18n
from src.core.i18n import t

class BusinessCardPlugin(StockPlugin):
    name: t("page.business_card")  # ❌ 不行！name 必須是常數
    
    # ✅ 正確：name 用英文 key，顯示時用 t()
    name = "business_card"  # 內部 key
    
    # 在 sidebar 中：
    # t(f"page.{plugin.name}") → "名片"
```

**修正方案**：Plugin `name` 使用英文 key（如 `"business_card"`），UI 顯示時用 `t(f"page.{name}")` 翻譯。

---

*本文檔基於 2026-06-14 掃描 stock-explorer/src/*.py 的实际结果撰寫*
