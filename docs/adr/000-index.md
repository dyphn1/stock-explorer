# 架構決策記錄 (ADR) 索引

> **說明**: 本目錄記錄所有重大技術與產品決策。每個 ADR 包含：背景、決策、後果、替代方案。

---

## 決策清單

| ID | 標題 | 狀態 | 日期 |
|----|------|------|------|
| [ADR-001](./001-streamlit-as-frontend.md) | 選擇 Streamlit 作為前端框架 | 已接受 | 2026-06-06 |
| [ADR-002](./002-finmind-as-data-source.md) | 選擇 FinMind 作為主要數據來源 | 已接受 | 2026-06-06 |
| [ADR-003](./003-layered-architecture.md) | 採用嚴格分層架構 | 已接受 | 2026-06-07 |
| [ADR-004](./004-plugin-chassis.md) | Plugin Chassis 架構 | ✅ 完成（Phase 1+2） | 2026-06-18 |
| [ADR-005](./005-i18n-yaml.md) | i18n 使用 YAML 單一檔案 per locale | 已接受 | 2026-06-14 |
| [ADR-006](./006-browser-back-button.md) | 瀏覽器返回按鈕支援 | 已接受 | 2026-06-12 |
| [ADR-007](./007-llm-safety-boundary.md) | LLM 安全邊界：只翻譯不推導 | 已接受 | 2026-06-07 |
| [ADR-008](./008-yaml-config-driven.md) | 全 Config 驅動設計 | 已接受 | 2026-06-07 |
| [ADR-009](./009-layout-restructure.md) | 佈局重構：兩層導航架構 | 規劃中 | 2026-06-14 |
| [ADR-010](./010-ppt-style-design.md) | PPT 風格設計原則 | 已接受 | 2026-06-08 |

---

## ADR 狀態定義

| 狀態 | 說明 |
|------|------|
| **提案中** | 尚未決定的決策 |
| **已接受** | 已採納並實施中 |
| **已取代** | 被更新的 ADR 取代 |
| **已棄用** | 不再適用 |
| **規劃中** | 已決定方向但尚未實施 |
