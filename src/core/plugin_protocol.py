"""
src/core/plugin_protocol.py
Plugin Protocol 定義 — 所有頁面 Plugin 必須實現的介面。

此模組定義了 Plugin Chassis 的核心協議：
- PluginMetadata: 插件元數據
- PluginRenderContext: 渲染上下文（data dict + client + page_key + session_state）
- RenderMiddleware: 渲染中介層協議（用於 cross-cutting concerns）
- PluginProtocol: Python Protocol class（靜態結構檢查用）
- BasePlugin: 抽象基類（運行時繼承用，提供默認行為）

設計原則：
1. Protocol 用於靜態類型檢查（mypy / IDE）
2. BasePlugin 用於運行時繼承（提供默認實現，子類只需 override 必要方法）
3. 兩者接口一致，開發者可任選其一
4. session_state 通過 PluginRenderContext 暴露，plugin 不直接訪問 st.session_state
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from src.data.finmind_client import FinMindClient

logger = logging.getLogger(__name__)


# ── Plugin Metadata ──────────────────────────────────────

@dataclass(frozen=True)
class PluginMetadata:
    """插件元數據 — 描述插件的基本屬性。

    Attributes:
        key: 唯一標識符（對應 session_state['page_key'] 和 i18n key）
        icon: 圖示（emoji 或 icon name）
        requires_stock_id: 是否需要股票代號才能渲染
        requires_data: 是否需要預載的 data dict（False = 獨立頁面如 category_browser）
        category: 插件分類（用於導航分組：'analysis' | 'browse' | 'tool' | 'learn' | 'system'）
        order: 排序權重（越小越靠前）
        enabled: 是否啟用（False = 註冊但不顯示在導航）
    """
    key: str
    icon: str = "📄"
    requires_stock_id: bool = True
    requires_data: bool = True
    category: str = "analysis"
    order: int = 100
    enabled: bool = True

    def __post_init__(self):
        """Validate key format: lowercase letters, digits, underscores only."""
        import re
        if not re.match(r'^[a-z][a-z0-9_]{0,63}$', self.key):
            raise ValueError(
                f"PluginMetadata.key must match ^[a-z][a-z0-9_]{{0,63}}$, got: {self.key!r}"
            )


# ── Render Context ───────────────────────────────────────

@dataclass
class PluginRenderContext:
    """傳遞給插件 render() 方法的上下文。

    Attributes:
        page_key: 當前頁面 key
        data: 預載的股票數據 dict（requires_data=False 的插件可能為 None）
        client: FinMindClient 實例
        stock_id: 當前股票代號（可能為 None）
        session_state: 只讀引用到 Streamlit session_state（由框架注入）

    session_state 策略：
        - Plugin 通過 ctx.session_state 讀取 session 中的唯讀數據（如 page_key、stock_id）
        - Plugin 通過 ctx.set_state(key, value) 寫入需要在 session 中持久化的狀態
        - Plugin **不應**直接訪問 st.session_state，保持與框架解耦
        - session_state 在大多數情況下為 None（測試時），plugin 需處理此情況
    """
    page_key: str
    data: dict | None
    client: "FinMindClient"
    stock_id: str | None = None
    session_state: Any = None  # 只讀引用（通常為 st.session_state 或 None）

    def set_state(self, key: str, value: Any) -> None:
        """將狀態寫入 session_state（如果可用）。

        此方法是 plugin 與 session_state 互動的唯一推薦方式。
        如果 session_state 為 None（例如測試環境），此方法為 no-op。

        Args:
            key: session_state 中的鍵名
            value: 要存儲的值
        """
        if self.session_state is not None:
            try:
                self.session_state[key] = value
            except Exception:
                logger.warning(
                    "Failed to set session_state[%r] — "
                    "session_state may be read-only or unavailable.",
                    key,
                    exc_info=True,
                )


# ── Render Middleware Protocol ──────────────────────────

@runtime_checkable
class RenderMiddleware(Protocol):
    """渲染中介層協議 — 用於 cross-cutting concerns。

    中介層在 plugin render() 前後執行，可實現：
    - ETF 檢測與重導向
    - M5 事件偵測
    - 性能監控 / 日誌記錄
    - 權限檢查

    使用方式：
        class ETFDetectionMiddleware:
            def before_render(self, ctx: PluginRenderContext, plugin: PluginProtocol) -> bool:
                # 返回 False 中斷渲染（例如已重導向到 ETF 頁面）
                ...

            def after_render(self, ctx: PluginRenderContext, plugin: PluginProtocol) -> None:
                ...

    注意：
    - before_render 返回 False 表示「已處理，跳過 plugin.render()」
    - 多個中介層按註冊順序執行
    - 中介層例外會被記錄但不中斷渲染（fail-open 策略）
    """

    def before_render(self, ctx: PluginRenderContext, plugin: "PluginProtocol") -> bool:
        """在 plugin render() 之前執行。

        Args:
            ctx: 渲染上下文
            plugin: 將要渲染的 plugin

        Returns:
            True 繼續渲染，False 跳過 plugin.render()
        """
        ...

    def after_render(self, ctx: PluginRenderContext, plugin: "PluginProtocol") -> None:
        """在 plugin render() 之後執行。

        Args:
            ctx: 渲染上下文
            plugin: 已渲染的 plugin
        """
        ...


# ── Plugin Protocol (靜態檢查用) ─────────────────────────

@runtime_checkable
class PluginProtocol(Protocol):
    """Plugin 協議 — 用於靜態類型檢查。

    任何實現了以下屬性和方法的對象都符合此協議：
    - metadata: PluginMetadata
    - render(ctx: PluginRenderContext) -> None

    使用 @runtime_checkable 允許運行時 isinstance() 檢查。
    """

    @property
    def metadata(self) -> PluginMetadata:
        """插件元數據。"""
        ...

    def render(self, ctx: PluginRenderContext) -> None:
        """渲染插件內容。

        Args:
            ctx: 渲染上下文，包含 data、client、page_key 等。
        """
        ...

    def can_render(self, ctx: PluginRenderContext) -> bool:
        """檢查當前上下文是否允許渲染。

        默認實現：如果 requires_stock_id=True 但 stock_id 為 None，返回 False。
        子類可擴展此方法實現更複雜的條件判斷。

        Args:
            ctx: 渲染上下文。

        Returns:
            True 如果可以渲染，False 否則。
        """
        ...


# ── BasePlugin (運行時繼承用) ────────────────────────────

class BasePlugin(ABC):
    """Plugin 抽象基類 — 提供默認實現，子類只需 override 必要方法。

    使用方式：
        class BusinessCardPlugin(BasePlugin):
            metadata = PluginMetadata(key="business_card", icon="🏢", category="analysis", order=10)

            def render(self, ctx: PluginRenderContext) -> None:
                # 原有 _render_business_card(data, client) 的邏輯
                ...

    注意：
    - 子類必須定義 metadata 類屬性
    - 子類必須實現 render() 方法
    - can_render() 有默認實現，可選擇性 override
    """

    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """插件元數據。子類必須定義。"""
        ...

    @abstractmethod
    def render(self, ctx: PluginRenderContext) -> None:
        """渲染插件內容。子類必須實現。"""
        ...

    def can_render(self, ctx: PluginRenderContext) -> bool:
        """檢查當前上下文是否允許渲染。默認實現。"""
        if self.metadata.requires_stock_id and not ctx.stock_id:
            return False
        if self.metadata.requires_data and ctx.data is None:
            return False
        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} key={self.metadata.key!r}>"


# ── Plugin Category Constants ────────────────────────────

class PluginCategory:
    """插件分類常量。"""
    ANALYSIS = "analysis"       # 分析類頁面（名片、財務體質等）
    BROWSE = "browse"           # 瀏覽類頁面（分類瀏覽、ETF 專區等）
    TOOL = "tool"               # 工具類頁面（股票探索、投資備忘錄等）
    LEARN = "learn"             # 學習類頁面（學習學院、案例研究等）
    SYSTEM = "system"           # 系統類頁面（設定、通知中心等）
