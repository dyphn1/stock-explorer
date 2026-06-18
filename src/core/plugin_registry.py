"""
src/core/plugin_registry.py
Plugin Registry — 自動掃描、註冊、路由所有 Plugin。

職責：
1. 自動掃描 src/plugins/ 目錄，發現所有 Plugin 子類
2. 維護 plugin key → plugin instance 的映射
3. 提供按 category 分組的插件列表（用於導航渲染）
4. 根據 page_key 查找並調用對應 plugin 的 render() 方法

設計要點：
- 使用 importlib 自動掃描，無需手動註冊
- 支持熱重啟（Streamlit rerun 時重新掃描）
- 向後兼容：現有的 src/pages/*.py 可通過 Adapter 模式接入
- discover() 使用「記錄並跳過」策略：單個壞掉的 plugin 不影響其他 plugin

使用方式：
    registry = PluginRegistry()
    registry.discover()  # 掃描 src/plugins/
    plugin = registry.get("business_card")
    plugin.render(ctx)
"""

from __future__ import annotations

import importlib
import importlib.util
import inspect
import logging
import pkgutil
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from src.core.plugin_protocol import (
    BasePlugin,
    PluginMetadata,
    PluginProtocol,
    PluginRenderContext,
    PluginCategory,
)

if TYPE_CHECKING:
    from src.data.finmind_client import FinMindClient

logger = logging.getLogger(__name__)


# ── Plugin Registration Error ────────────────────────────

class PluginError(Exception):
    """Plugin 相關錯誤的基類。"""
    pass


class PluginNotFoundError(PluginError):
    """找不到指定 key 的 plugin。"""
    pass


class PluginRegistrationError(PluginError):
    """Plugin 註冊失敗。"""
    pass


# ── Plugin Registry ──────────────────────────────────────

class PluginRegistry:
    """Plugin 註冊表 — 自動掃描、註冊、路由。

    Attributes:
        _plugins: key → plugin instance 的映射
        _scanned: 是否已完成掃描

    使用方式：
        registry = PluginRegistry()
        registry.discover()  # 自動掃描 src/plugins/
        # 或
        registry.register(MyPlugin())  # 手動註冊
    """

    def __init__(self, plugin_dir: str | Path | None = None):
        """初始化註冊表。

        Args:
            plugin_dir: 插件目錄路徑。默認為 src/plugins/
        """
        self._plugins: dict[str, BasePlugin] = {}
        self._scanned: bool = False
        self._plugin_dir = Path(plugin_dir) if plugin_dir else self._default_plugin_dir()

    @staticmethod
    def _default_plugin_dir() -> Path:
        """返回默認插件目錄路徑。"""
        return Path(__file__).resolve().parent.parent / "plugins"

    # ── Discovery ─────────────────────────────────────────

    def discover(self) -> int:
        """自動掃描插件目錄，註冊所有發現的 Plugin。

        掃描策略（「記錄並跳過」）：
        1. 遍歷 plugin_dir 下的所有子目錄
        2. 每個子目錄中查找 plugin.py 模塊
        3. 導入模塊，查找所有 BasePlugin 子類
        4. 實例化並註冊
        5. 任何單個 plugin 載入失敗只記錄錯誤，不影響其他 plugin

        Returns:
            新註冊的插件數量。
        """
        if self._scanned:
            logger.debug("PluginRegistry already scanned, skipping discovery.")
            return 0

        count = 0
        plugin_dir = self._plugin_dir

        if not plugin_dir.exists():
            logger.warning("Plugin directory does not exist: %s", plugin_dir)
            self._scanned = True
            return 0

        # SEC-004: Do NOT manipulate sys.path — spec_from_file_location
        # works with explicit paths and doesn't require sys.path entries.
        # Inserting plugin_dir.parent into sys.path enables module shadowing.

        for item in sorted(plugin_dir.iterdir()):
            if not item.is_dir():
                continue
            if item.name.startswith("_"):
                continue

            # SEC-002: Validate directory name matches plugin key pattern
            import re as _re
            if not _re.match(r'^[a-z][a-z0-9_]{0,63}$', item.name):
                logger.warning(
                    "Skipping plugin directory '%s': name does not match ^[a-z][a-z0-9_]{0,63}$",
                    item.name,
                )
                continue

            # SEC-002: Ensure resolved path is within plugin_dir (prevent path traversal)
            try:
                resolved = item.resolve()
                if not str(resolved).startswith(str(plugin_dir.resolve())):
                    logger.warning(
                        "Skipping plugin directory '%s': resolved path escapes plugin_dir",
                        item.name,
                    )
                    continue
            except (OSError, ValueError) as path_err:
                logger.warning(
                    "Skipping plugin directory '%s': path resolution failed: %s",
                    item.name,
                    path_err,
                )
                continue

            plugin_file = item / "plugin.py"
            if not plugin_file.exists():
                logger.debug("Skipping %s: no plugin.py found", item.name)
                continue

            try:
                module = self._import_plugin_module(item.name, plugin_file)
                plugin_classes = self._find_plugin_classes(module)
                for cls in plugin_classes:
                    instance = cls()
                    self._register(instance)
                    count += 1
                # Also check for module-level plugin instances (e.g. LegacyPageAdapter)
                instance_count = self._find_plugin_instances(module)
                count += instance_count
            except Exception as exc:
                # 「記錄並跳過」策略：單個壞掉的 plugin 不影響其他 plugin
                logger.error(
                    "Failed to load plugin from %s: %s — skipping.",
                    item.name,
                    exc,
                    exc_info=True,
                )

        self._scanned = True
        logger.info("PluginRegistry: discovered %d plugins.", count)
        return count

    def _import_plugin_module(self, name: str, path: Path):
        """導入插件模塊。

        Args:
            name: 插件目錄名稱（用作模塊名）。
            path: plugin.py 文件路徑。

        Returns:
            導入的模塊對象。
        """
        module_name = f"src.plugins.{name}.plugin"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create module spec for {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def _find_plugin_classes(self, module) -> list[type[BasePlugin]]:
        """在模塊中查找所有 BasePlugin 子類。

        只返回在該模塊中定義的類（通過檢查 __module__ 屬性），
        避免將從其他模塊導入的類（如 LegacyPageAdapter）誤認為 plugin。

        Args:
            module: 要搜索的模塊。

        Returns:
            BasePlugin 子類列表。
        """
        classes = []
        module_name = getattr(module, "__name__", "")
        for attr_name in dir(module):
            if attr_name.startswith("_"):
                continue
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, BasePlugin)
                and attr is not BasePlugin
                and getattr(attr, "__module__", "") == module_name
            ):
                classes.append(attr)
        return classes

    def _find_plugin_instances(self, module) -> int:
        """在模塊中查找 module-level BasePlugin 實例（非類）。

        用於支持 LegacyPageAdapter 實例直接定義在 plugin.py 模塊層面的模式。
        跳過已通過 _find_plugin_classes 註冊的實例（避免重複註冊）。

        Args:
            module: 要搜索的模塊。

        Returns:
            新註冊的實例數量。
        """
        count = 0
        for attr_name in dir(module):
            if attr_name.startswith("_"):
                continue
            if attr_name[0].isupper():
                # Skip classes (handled by _find_plugin_classes)
                continue
            attr = getattr(module, attr_name)
            if isinstance(attr, BasePlugin) and not isinstance(attr, type):
                try:
                    self._register(attr)
                    count += 1
                except PluginRegistrationError:
                    # Already registered by _find_plugin_classes — skip
                    logger.debug(
                        "Plugin instance '%s' already registered, skipping.",
                        attr_name,
                    )
        return count

    # ── Registration ──────────────────────────────────────

    def register(self, plugin: BasePlugin) -> None:
        """手動註冊一個 plugin 實例。

        Args:
            plugin: 要註冊的 plugin 實例。

        Raises:
            PluginRegistrationError: key 已存在或 plugin 無效。
        """
        self._register(plugin)

    def _register(self, plugin: BasePlugin) -> None:
        """內部註冊邏輯。"""
        key = plugin.metadata.key
        if key in self._plugins:
            raise PluginRegistrationError(
                f"Plugin key '{key}' is already registered by {self._plugins[key]!r}"
            )
        self._plugins[key] = plugin
        logger.debug("Registered plugin: %s", plugin)

    # ── Lookup ────────────────────────────────────────────

    def get(self, key: str) -> BasePlugin:
        """根據 key 查找 plugin。

        Args:
            key: 插件 key。

        Returns:
            對應的 plugin 實例。

        Raises:
            PluginNotFoundError: 找不到對應的 plugin。
        """
        if key not in self._plugins:
            raise PluginNotFoundError(f"No plugin registered for key: {key!r}")
        return self._plugins[key]

    def has(self, key: str) -> bool:
        """檢查是否存在指定 key 的 plugin。"""
        return key in self._plugins

    @property
    def all_plugins(self) -> list[BasePlugin]:
        """返回所有已註冊的 plugin 列表（按 category + order + key 排序）。

        排序使用三個鍵確保穩定性：
        1. category（分類）
        2. order（權重）
        3. key（字母順序，確保相同 category+order 的插件順序穩定）
        """
        return sorted(
            self._plugins.values(),
            key=lambda p: (p.metadata.category, p.metadata.order, p.metadata.key),
        )

    def get_by_category(self, category: str) -> list[BasePlugin]:
        """返回指定分類的 plugin 列表。"""
        return [
            p for p in self.all_plugins
            if p.metadata.category == category and p.metadata.enabled
        ]

    @property
    def all_keys(self) -> list[str]:
        """返回所有已註冊的 plugin key 列表。"""
        return [p.metadata.key for p in self.all_plugins if p.metadata.enabled]

    def __len__(self) -> int:
        return len(self._plugins)

    def __repr__(self) -> str:
        return f"<PluginRegistry plugins={list(self._plugins.keys())}>"


# ── Legacy Adapter (向後兼容) ───────────────────────────

class LegacyPageAdapter(BasePlugin):
    """將現有的 src/pages/*.py 渲染函數包裝為 Plugin。

    用途：在遷移過渡期，無需立即重構所有頁面，
    可通過此 Adapter 將現有的 _render_* 函數包裝為 Plugin。

    支持的 render_fn 簽名（在 __init__ 時通過 inspect.signature 驗證）：
    1. (data, client) → None        # 需要 data 的頁面
    2. (client) → None              # 不需要 data 的頁面
    3. (data) → None                # 只需要 data 的頁面
    4. () → None                    # 獨立頁面，不需要任何參數（如 settings）

    使用方式：
        adapter = LegacyPageAdapter(
            key="business_card",
            icon="🏢",
            category=PluginCategory.ANALYSIS,
            render_fn=_render_business_card,
            requires_data=True,
        )
        registry.register(adapter)
    """

    # 支持的簽名模式（參數名不重要，只檢查數量和類型註解）
    _SUPPORTED_SIGNATURES = [
        # (data, client) — 需要 data 的頁面
        {"min_params": 2, "max_params": 2, "name": "(data, client)"},
        # (client,) — 不需要 data 的頁面
        {"min_params": 1, "max_params": 1, "name": "(client)"},
        # (data,) — 只需要 data 的頁面
        {"min_params": 1, "max_params": 1, "name": "(data)"},
        # () — 獨立頁面，不需要任何參數（如 settings）
        {"min_params": 0, "max_params": 0, "name": "()"},
    ]

    def __init__(
        self,
        key: str,
        icon: str,
        category: str,
        render_fn,
        requires_stock_id: bool = True,
        requires_data: bool = True,
        order: int = 100,
    ):
        self._metadata = PluginMetadata(
            key=key,
            icon=icon,
            requires_stock_id=requires_stock_id,
            requires_data=requires_data,
            category=category,
            order=order,
        )
        self._render_fn = render_fn
        self._validate_signature()

    def _validate_signature(self) -> None:
        """在 __init__ 時驗證 render_fn 的簽名。

        通過 inspect.signature 檢查參數數量，確保 render() 時能正確調用。
        不依賴運行時檢查，錯誤在構造時即被捕獲。

        Raises:
            TypeError: render_fn 的簽名不受支持。
        """
        sig = inspect.signature(self._render_fn)
        params = [
            p for p in sig.parameters.values()
            if p.kind in (
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.POSITIONAL_ONLY,
            )
        ]
        num_params = len(params)

        # Check if matches any supported signature
        if num_params == 2:
            self._signature_type = "data_client"
        elif num_params == 1:
            # 判斷是 (client) 還是 (data)
            # 通過參數名或 requires_data 推斷
            param_name = params[0].name.lower() if params else ""
            if self._metadata.requires_data:
                self._signature_type = "data_only"
            elif param_name in ("client",):
                self._signature_type = "client_only"
            else:
                # 默認：如果 requires_data=True 但只有 1 個參數，視為 data_only
                # 否則視為 client_only
                self._signature_type = "data_only" if self._metadata.requires_data else "client_only"
        elif num_params == 0:
            self._signature_type = "none"
        else:
            supported = ", ".join(s["name"] for s in self._SUPPORTED_SIGNATURES)
            raise TypeError(
                f"LegacyPageAdapter: render_fn has {num_params} parameters, "
                f"but only {supported} are supported. "
                f"Got signature: {sig}"
            )

        logger.debug(
            "LegacyPageAdapter[%s]: validated signature as %s",
            self._metadata.key,
            self._signature_type,
        )

    @property
    def metadata(self) -> PluginMetadata:
        return self._metadata

    def render(self, ctx: PluginRenderContext) -> None:
        """調用原有的渲染函數，根據簽名類型傳遞正確參數。"""
        if self._signature_type == "data_client":
            if ctx.data is not None:
                self._render_fn(ctx.data, ctx.client)
            else:
                logger.warning(
                    "Plugin '%s' requires data but ctx.data is None — skipping render.",
                    self._metadata.key,
                )
        elif self._signature_type == "client_only":
            self._render_fn(ctx.client)
        elif self._signature_type == "data_only":
            if ctx.data is not None:
                self._render_fn(ctx.data)
            else:
                logger.warning(
                    "Plugin '%s' requires data but ctx.data is None — skipping render.",
                    self._metadata.key,
                )
        elif self._signature_type == "none":
            self._render_fn()
