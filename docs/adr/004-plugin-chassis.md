# ADR-004: Plugin Chassis 架構

## 狀態
規劃中

## 日期
2026-06-14

## 背景

`router.py` 目前有 274 行，包含 33 個 if-elif 分支。新增一個頁面需要修改 3 個地方：import、page name list、if-elif 分支。這違反了開放-封閉原則。

## 決策

將每個頁面設計為獨立 **Plugin**，遵循統一協議，核心框架自動掃描、註冊、路由。

## 目標架構

```
src/
├── core/
│   ├── chassis.py          # Chassis 主類（PluginRegistry + LifecycleManager）
│   ├── plugin_protocol.py  # Plugin 介面定義
│   └── di.py               # 依賴注入容器
│
├── plugins/                # 取代 pages/ 的大部分功能
│   ├── __init__.py         # 自動掃描 + 註冊所有 plugin
│   ├── _base.py            # BasePlugin 抽象類
│   ├── business_card/
│   │   ├── plugin.py       # BusinessCardPlugin(BasePlugin)
│   │   └── ...             # 原有渲染邏輯
│   ├── operation_checkup/
│   ├── financial_health/
│   └── ...
```

## Plugin Protocol

```python
class BasePlugin(Protocol):
    name: str           # 頁面名稱（用於導航）
    icon: str           # 圖示
    requires_stock_id: bool  # 是否需要股票代號
    
    def render(self, data: dict, client: FinMindClient) -> None:
        """渲染頁面內容"""
        ...
```

## 理由

1. **開放-封閉原則**：新增功能不需修改現有程式碼
2. **獨立開發**：每個 plugin 可獨立開發/測試
3. **動態啟用/停用**：不需修改路由邏輯

## 實施計畫

1. 定義 `PluginProtocol` 和 `BasePlugin`
2. 建立 `PluginRegistry`（自動掃描 `src/plugins/`）
3. 重構 `router.py` 使用 registry
4. 逐頁遷移至 plugin 格式

## 後果

- ✅ 新增/移除功能 = 註冊/取消註冊 plugin
- ✅ 可獨立開發/測試單一 feature
- ⚠️ 需要一次性重構成本
- ⚠️ 團隊需要理解 plugin 概念
