# Security Review Report — TD-01 Plugin Chassis

**Review Date**: 2026-06-18
**Reviewer**: Security Architect (Hermes Agent)
**Scope**: TD-01 Plugin Chassis Refactoring — `plugin_protocol.py`, `plugin_registry.py`, `adr/004-plugin-chassis.md`
**Related ADRs**: ADR-004 (Plugin Chassis), ADR-007 (LLM Safety Boundary)

---

## Executive Summary

The Plugin Chassis design is **architecturally sound** and introduces a clean separation of concerns. However, the security review identified **6 findings** — 2 High, 3 Medium, and 1 Info — that must be addressed before production deployment.

The most critical concerns are around the **automatic code execution via `discover()`** (arbitrary code execution if the plugins directory is compromised) and the **absence of plugin key validation** (enabling path traversal and injection vectors). The design's trust model implicitly assumes that anyone with write access to `src/plugins/` is trusted to execute arbitrary Python code — this assumption must be explicitly documented and enforced.

The Plugin Chassis is **compatible with ADR-007's LLM safety boundary** and does not weaken it, provided the `RenderMiddleware` protocol is used for cross-cutting LLM output validation.

**Overall Verdict**: ⚠️ **PASS with conditions** — All High and Medium findings must be remediated before TD-01b (LegacyPageAdapter integration) proceeds.

---

## Findings

### SEC-001: Automatic Code Execution via `discover()`

- **Severity**: **High**
- **Category**: Code Execution / Supply Chain
- **Description**:

  `PluginRegistry.discover()` (lines 99–158 of `plugin_registry.py`) uses `importlib.util.spec_from_file_location()` + `spec.loader.exec_module()` to dynamically load every `plugin.py` found under `src/plugins/<name>/`. This is **arbitrary code execution by design** — any Python code in a discovered `plugin.py` runs with the full privileges of the application process at import time.

  The current code has **zero validation** of what it imports:
  - No cryptographic signature or hash verification of plugin files
  - No sandboxing or restricted execution environment
  - No allowlist of permitted module imports within plugins
  - No check that the loaded class actually implements `BasePlugin` beyond `_find_plugin_classes()` filtering (which only checks `issubclass(attr, BasePlugin)` — a malicious class could still pass this check while executing arbitrary code in `__init__` or at module level)

  **Attack scenario**: An attacker who gains write access to the `src/plugins/` directory (via a separate vulnerability, misconfigured CI/CD, or a malicious dependency) can place a file `src/plugins/evil/plugin.py` that executes arbitrary code — exfiltrates data, modifies other plugins, opens a reverse shell, etc. The `discover()` method will happily load it on the next Streamlit rerun.

  Additionally, `_import_plugin_module()` (line 175) registers the module in `sys.modules`, meaning a malicious plugin could **monkey-patch** any previously loaded module, including `BasePlugin` itself or the registry.

- **Recommendation**:
  1. **Document the trust model explicitly**: Write access to `src/plugins/` = code execution. This must be protected with the same rigor as the application source code (code review, CI/CD gating, file integrity monitoring).
  2. **Add a plugin manifest with hash verification**: Require each plugin directory to contain a `plugin.yaml` manifest with a SHA-256 hash of `plugin.py`. Verify the hash at discovery time against a known-good list stored in the repository.
  3. **Restrict `sys.path` manipulation**: The current code inserts `plugin_dir.parent` into `sys.path` (line 127). This is unnecessary when using `importlib.util.spec_from_file_location()` with an explicit path, and it could allow a malicious plugin directory name to shadow standard library modules. Remove this `sys.path` manipulation.
  4. **Consider a plugin signing mechanism** for future external plugin support.

---

### SEC-002: Plugin Key Validation Absent — Path Traversal and Injection Risk

- **Severity**: **High**
- **Category**: Input Validation / Injection
- **Description**:

  The `PluginMetadata.key` field is a free-form string with **no validation** anywhere in the codebase:
  - `PluginMetadata` is a frozen dataclass with no `__post_init__` validation
  - `PluginRegistry._register()` (line 214) only checks for key uniqueness
  - `PluginRegistry.get()` (line 226) uses the key directly as a dict lookup

  The key is used in multiple security-sensitive contexts:
  1. **Module naming**: `_import_plugin_module()` constructs `module_name = f"src.plugins.{name}.plugin"` where `name` comes from the **directory name**, not the key. However, the key is used for lookup in `registry.get(page_key)` where `page_key` comes from `st.session_state["page_key"]` — which is set from URL query parameters via `url_sync.py`.
  2. **Session state**: The key is stored in `session_state["page_key"]` and used to look up plugins. A crafted key could cause a `PluginNotFoundError` (minor DoS), but more critically, the key flows into i18n lookups like `t(f"page.{key}")` in `router.py`.
  3. **Future URL routing**: ADR-004 Phase 4 plans to use `registry.all_keys` for `VALID_PAGES` replacement, meaning keys will directly control URL-routable endpoints.

  **Attack scenarios**:
  - **Path traversal via directory name**: If an attacker can create a directory like `src/plugins/../../../etc/` (or `src/plugins/__import__/`) the `discover()` method's `item / "plugin.py"` path construction could resolve to unexpected locations. While `pathlib.Path` mitigates basic `../` traversal, the lack of a canonical path check is a gap.
  - **Key collision / shadowing**: A plugin with key `"__init__"` or `"__pycache__"` could cause confusing behavior or shadow Python internals.
  - **Format string injection**: If keys are ever used in f-strings that evaluate expressions (not currently the case, but a latent risk).

- **Recommendation**:
  1. **Add key format validation** in `PluginMetadata.__post_init__` (requires removing `frozen=True` or using `__post_init__` with `object.__setattr__`):
     ```python
     import re
     _KEY_PATTERN = re.compile(r'^[a-z][a-z0-9_]{0,63}$')
     ```
     Reject keys with uppercase, hyphens, dots, slashes, or leading underscores.
  2. **Validate directory names** in `discover()` — check that `item.name` matches the same pattern and resolve to a canonical path within `plugin_dir`.
  3. **Sanitize the `page_key` from session_state** before using it in `registry.get()` — validate against `registry.all_keys` before lookup.

---

### SEC-003: `session_state` Passed as Mutable Reference — Data Isolation Weakness

- **Severity**: **Medium**
- **Category**: Data Isolation / Information Disclosure
- **Description**:

  `PluginRenderContext.session_state` (line 79 of `plugin_protocol.py`) is documented as a "只讀引用" (read-only reference) but is actually a **mutable reference** to `st.session_state`. There is no enforcement of read-only access:

  ```python
  session_state: Any = None  # 只讀引用（通常為 st.session_state 或 None）
  ```

  The documentation says "Plugin **不應**直接訪問 st.session_state" (line 72), but this is a **convention, not a control**. Any plugin can:
  - Read all session state data from other plugins (cross-plugin data leakage)
  - Modify or delete session state keys belonging to other plugins or the framework
  - Inject malicious session state keys that affect framework behavior (e.g., setting `page_key` to a crafted value)

  The `set_state()` method (line 81) is provided as the "only recommended way" to write state, but nothing prevents direct `ctx.session_state["key"] = value` access.

  **Impact**: In a multi-plugin environment, a buggy or malicious plugin could:
  - Read sensitive data from other plugins' session state
  - Corrupt another plugin's state by overwriting shared keys
  - Cause framework errors by modifying `page_key` or `stock_id` mid-render

- **Recommendation**:
  1. **Wrap session_state in a read-only proxy** that raises `AttributeError` on `__setitem__` and `__delitem__`:
     ```python
     class ReadOnlyState:
         def __init__(self, state):
             self._state = state
         def __getitem__(self, key):
             return self._state[key]
         def __contains__(self, key):
             return key in self._state
         def get(self, key, default=None):
             return self._state.get(key, default)
         def keys(self):
             return self._state.keys()
         def __setitem__(self, key, value):
             raise AttributeError("Use ctx.set_state() to write state")
     ```
  2. **Namespace plugin session state**: Instead of sharing the global `st.session_state`, give each plugin its own namespace (e.g., `session_state[f"plugin.{key}."]`) to prevent cross-plugin key collisions.
  3. **Document the session state contract** in `BasePlugin` with clear examples of allowed vs. prohibited patterns.

---

### SEC-004: `sys.path` Manipulation and Module Name Collision

- **Severity**: **Medium**
- **Category**: Code Injection / Module Shadowing
- **Description**:

  In `PluginRegistry.discover()` (lines 125–127):

  ```python
  plugin_parent = str(plugin_dir.parent)
  if plugin_parent not in sys.path:
      sys.path.insert(0, plugin_parent)
  ```

  This inserts the **parent of the plugins directory** (i.e., `src/`) at position 0 in `sys.path`. Combined with the module name construction `f"src.plugins.{name}.plugin"`, this creates a dangerous interaction:

  1. **Module shadowing**: By inserting `src/` at `sys.path[0]`, any module name starting with `src.` could shadow or be shadowed by real packages. If a plugin directory is named `os` or `sys`, the module name `src.os.plugin` could interfere with Python's standard library resolution.
  2. **Persistent `sys.path` pollution**: The `sys.path` modification is permanent for the process lifetime. If `discover()` is called multiple times (the `_scanned` flag prevents re-scanning, but this could be reset), the path keeps growing.
  3. **Interaction with `sys.modules`**: Line 175 (`sys.modules[module_name] = module`) registers the module globally. If a plugin is removed from the filesystem but remains in `sys.modules`, stale code persists. There's no cleanup mechanism.

  Furthermore, the `_default_plugin_dir()` method uses `Path(__file__).resolve().parent.parent / "plugins"` — this is relative to the **installed location** of `plugin_registry.py`, not the project root. If the package is installed system-wide or in a virtual environment, the resolved path may point to an unexpected location.

- **Recommendation**:
  1. **Remove the `sys.path` manipulation entirely** — `importlib.util.spec_from_file_location()` does not require the target directory to be in `sys.path` when an explicit file path is provided.
  2. **Add module cleanup** to `discover()` — remove stale plugin modules from `sys.modules` when their directories no longer exist.
  3. **Validate the resolved `plugin_dir`** is within the expected project directory (use `Path.cwd()` or an explicit project root marker like `pyproject.toml`).

---

### SEC-005: LegacyPageAdapter Render Function Fallback Logic — Unexpected Behavior

- **Severity**: **Medium**
- **Category**: Logic Error / Denial of Service
- **Description**:

  `LegacyPageAdapter.render()` (lines 386–400 of `plugin_registry.py`) contains fallback logic that calls the wrong function signature when expected data is missing:

  ```python
  elif self._signature_type == "data_client":
      if ctx.data is not None:
          self._render_fn(ctx.data, ctx.client)
      else:
          # data 為 None 但簽名需要 data — 嘗試用 client 單參數調用
          self._render_fn(ctx.client)  # ← Calls with 1 arg, but signature expects 2
  ```

  When `ctx.data` is `None` for a `data_client` signature, the code falls back to calling `self._render_fn(ctx.client)` — passing a `FinMindClient` object as the first positional argument where the original function expects a `data` dict. This will cause a **runtime TypeError** or, worse, silent data corruption if the render function doesn't validate its inputs.

  Similar issues exist in the `data_only` branch (line 397–400) where `ctx.client` is passed when `ctx.data` is `None`.

  **Impact**: During the migration transition period (TD-01b), if a `LegacyPageAdapter`-wrapped page is rendered without the expected data (e.g., due to a race condition or misconfiguration), the application will crash with an unhandled exception.

- **Recommendation**:
  1. **Fail explicitly** when required data is missing instead of calling with wrong argument types:
     ```python
     if ctx.data is None:
         logger.warning("Plugin %s requires data but ctx.data is None", self._metadata.key)
         st.warning("Data not available for this page.")
         return
     ```
  2. **Add input validation** in the `render()` method to verify argument types before calling the legacy function.
  3. **Add unit tests** for all fallback paths in `LegacyPageAdapter.render()`.

---

### SEC-006: LLM Safety Boundary Compatibility — Positive Finding with Minor Gap

- **Severity**: **Info**
- **Category**: LLM Safety / ADR-007 Compliance
- **Description**:

  The Plugin Chassis architecture is **compatible with and does not weaken** ADR-007's LLM safety boundary. Key observations:

  ✅ **Positive**: The `RenderMiddleware` protocol (lines 106–149 of `plugin_protocol.py`) provides a natural hook point for LLM output validation middleware. ADR-007's tone blocklist scanning can be implemented as a `RenderMiddleware.before_render()` or `after_render()` check.

  ✅ **Positive**: The `PluginRenderContext` encapsulates all data passed to plugins, preventing plugins from accessing LLM-related session state directly.

  ✅ **Positive**: The `BasePlugin.can_render()` method provides a pre-render gate that can be extended to check LLM safety preconditions.

  ⚠️ **Minor gap**: The current design does not include an explicit **LLM output validation layer** in the plugin rendering pipeline. While the `RenderMiddleware` protocol exists, there is no built-in middleware for ADR-007 compliance. This means LLM safety validation must be implemented separately and **could be omitted** by a developer who is unaware of ADR-007.

  ⚠️ **Minor gap**: The `LegacyPageAdapter` bypasses the `PluginRenderContext` encapsulation for legacy render functions — these functions may directly call LLM services without going through the middleware pipeline.

- **Recommendation**:
  1. **Implement an `LLMSafetyMiddleware`** as a built-in `RenderMiddleware` that enforces ADR-007's tone blocklist on all LLM-generated content before rendering.
  2. **Document the LLM safety requirements** in the Plugin Chassis developer guide — all plugins that use LLM services must go through the middleware pipeline.
  3. **Add a deprecation path** for `LegacyPageAdapter` render functions that call LLM services directly, requiring them to migrate to the middleware-based approach.

---

## Additional Observations

### Positive Security Attributes

1. **Fail-open error handling in `discover()`**: The "log and skip" strategy (line 147–154) ensures a single broken plugin doesn't crash the entire application. This is good resilience.

2. **Directory name filtering**: The `item.name.startswith("_")` check (line 133) correctly skips `__pycache__`, `__init__`, and other private directories.

3. **Sorted iteration**: `sorted(plugin_dir.iterdir())` (line 129) provides deterministic discovery order, reducing the risk of order-dependent bugs.

4. **Frozen `PluginMetadata`**: Using `@dataclass(frozen=True)` prevents plugins from mutating their metadata after registration, which is a good immutability practice.

### Areas Not Covered (Out of Scope)

- **Network security**: The Plugin Chassis does not introduce new network endpoints or API surfaces.
- **Authentication/Authorization**: Stock Explorer is a single-user Streamlit app with no authentication. Plugin-level access control is not applicable in the current architecture.
- **Data at rest**: Plugin files are stored on the local filesystem with standard OS permissions. No encryption at rest is required for this threat model.

---

## Remediation Priority

| Priority | Finding | Effort | Risk if Not Fixed |
|----------|---------|--------|--------------------|
| P0 | SEC-001: Automatic Code Execution | Medium | Arbitrary code execution via plugins directory |
| P0 | SEC-002: Plugin Key Validation | Low | Path traversal, injection, DoS |
| P1 | SEC-003: session_state Isolation | Medium | Cross-plugin data leakage |
| P1 | SEC-004: sys.path Manipulation | Low | Module shadowing, stale code |
| P2 | SEC-005: LegacyPageAdapter Fallback | Low | Runtime crashes during migration |
| P3 | SEC-006: LLM Safety Middleware | Medium | ADR-007 compliance gap |

---

## Overall Verdict

### ⚠️ PASS with conditions

The Plugin Chassis architecture is well-designed and follows good software engineering principles. The security concerns are **manageable** but must be addressed:

**Required before TD-01b (LegacyPageAdapter integration)**:
1. SEC-001: Document the trust model; add plugin hash verification or equivalent
2. SEC-002: Add plugin key format validation
3. SEC-004: Remove `sys.path` manipulation

**Required before TD-01c (core page migration)**:
4. SEC-003: Implement read-only session_state proxy
5. SEC-005: Fix LegacyPageAdapter fallback logic

**Required before production deployment**:
6. SEC-006: Implement LLMSafetyMiddleware

---

*Report generated by Security Architect — Hermes Agent*
*Review based on code as of 2026-06-18*
