# Stock Explorer (股識) — 專案文件索引

> **版本**: v0.1.0 | **更新日期**: 2026-06-17
> **定位**: 面向新手投資人的台灣個股故事化分析工具

---

## 📖 文件導覽

| 文件 | 說明 | 適合對象 |
|------|------|----------|
| [`01-product-vision.md`](./01-product-vision.md) | 產品願景、目標用戶、核心價值 | 所有人 |
| [`02-architecture.md`](./02-architecture.md) | 系統架構、分層設計、數據流 | 開發者、架構師 |
| [`03-design-system.md`](./03-design-system.md) | 設計系統、UI 規範、佈局規則 | 開發者、設計師 |
| [`04-tech-stack.md`](./04-tech-stack.md) | 技術選型、依賴清單、API 說明 | 開發者 |
| [`05-roadmap.md`](./05-roadmap.md) | 開發路線圖、里程碑、當前狀態 | PM、所有人 |
| [`06-development-guide.md`](./06-development-guide.md) | 開發指南、環境設置、編碼規範 | 開發者 |

## 📋 其他文件

| 目錄 | 說明 |
|------|------|
| [`../adr/`](../adr/) | 架構決策記錄 (ADR) |
| [`../roadmap/`](../roadmap/) | 詳細路線圖與功能清單 |
| [`../dev-guide/`](../dev-guide/) | 開發指南與工作流程 |
| [`../roles/`](../roles/) | AI Agent 角色定義 |
| [`../state/`](../state/) | 當前問題與狀態追蹤 |

---

## ⚠️ 文件慣例

1. **所有文件以 Markdown 撰寫**，使用 UTF-8 編碼
2. **中英文混排**：產品名稱使用中文（股識），技術術語保留英文
3. **決策記錄**：任何重大技術或產品決策必須寫入 `docs/adr/`
4. **狀態同步**：每次 Sprint 結束時更新 `05-roadmap.md` 和 `docs/state/`
