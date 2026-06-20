# Current Problems — Stock Explorer (股識)

> **上次更新**: 2026-06-20
> **維護者**: PM Agent

---

## 格式說明

每筆問題記錄使用以下格式：

```
## [ID] [標題]
- **嚴重度**: P0/P1/P2
- **類型**: Bug / Tech Debt / Security / UX / Performance
- **報告者**: [角色]
- **日期**: [日期]
- **描述**: [問題描述]
- **影響檔案**: [相關檔案]
- **狀態**: Open / In Progress / Fixed / Verified
- **解決方案**: [修復方式，若已修復]
```

---

## P0 — 緊急（需在 1 個 sprint 內修復）

### TD-02: i18n 全面化
- **嚴重度**: P0 (Tech Debt)
- **類型**: Tech Debt / i18n
- **報告者**: QA Agent
- **日期**: 2026-06-18
- **描述**: 掃描發現 2,877 行 hardcoded 中文字串未使用 `t()` 函數。影響國際化支援。Phase 1 已完成前 5 大頁面遷移（~300 字串），Phase 2 已遷移 `src/main.py`（入口檔案）+ 約 8 個服務層檔案，剩餘大量 `src/services/` 檔案約 2,200 行字串待處理（多為 docstring 和內部字串）。
- **影響檔案**: 全域（主要為 `src/main.py` 及 `src/services/` 下的服務檔案）
- **狀態**: In Progress (Phase 1 完成, main.py 完成, locale keys 修復完成)
- **解決方案**: 逐頁將 hardcoded 字串替換為 `t()` 呼叫，在 locale YAML 檔中新增對應 key。Phase 1 完成：etf_browser, financial_health, group_structure, peer_comparison, etf_detail。main.py 完成（1d59af1）。locale keys 修復完成（3ebca99）— daily_market.* 和 validation.error.* 已加入。剩餘 27 個 pre-existing 測試失敗（非 i18n 相關）。

## P1 — 高優先（需在 2 個 sprint 內修復）

### TD-03: API 快取修復
- **嚴重度**: P1
- **類型**: Tech Debt / 效能
- **報告者**: 路線圖
- **日期**: 2026-06-18
- **描述**: `get_stock_info` 每次全表拉取，未使用快取。切換股票時重複呼叫浪費 API quota。
- **影響檔案**: `src/pages/_router_base.py`, `src/data/finmind_client.py`
- **狀態**: Fixed
- **解決方案**: 2320ce0 — `get_stock_info` 加入 `@lru_cache(maxsize=128)`，避免重複 API 呼叫。698/699 測試通過。

### TD-06: 色彩系統統一
- **嚴重度**: P1
- **類型**: Tech Debt / 設計系統
- **報告者**: Design Reviewer
- **日期**: 2026-06-18
- **描述**: 多處使用非設計系統色（如 `#F39C12`、`#2E86C1`、`#8E44AD`），違反設計系統規範。
- **影響檔案**: 全域（已修復）
- **狀態**: Fixed
- **解決方案**: b53546d 修復 8 個檔案（pages + story_timeline），6d8d691 修復剩餘 7 個檔案（sector_heatmap, business_card sections/helpers, timeline_service, financial_wellness_service）。所有 src/ 檔案已統一使用標準色彩 token。

### TD-07: 元件一致性
- **嚴重度**: P1
- **類型**: Tech Debt / 設計系統
- **報告者**: Design Reviewer
- **日期**: 2026-06-18
- **描述**: 部分頁面使用 `st.metric()` 或 raw HTML 而非 `_白话_card()`，導致視覺不一致。
- **影響檔案**: `src/pages/peer_comparison.py`, `src/pages/watchlist_page.py`
- **狀態**: Fixed
- **解決方案**: b53546d 已將 peer_comparison.py 中的 st.metric() 替換為 _白话_card()。驗證 src/ 下無 bare st.metric() 呼叫。

---

## P2 — 中優先（可排入未來 sprint）

### UX-01: 中文搜尋不支援
- **嚴重度**: P2
- **類型**: UX / 功能
- **報告者**: UX 改進路線圖
- **日期**: 2026-06-18
- **描述**: 搜尋框只比對 stock_id，無法搜尋「台積電」等中文股名。
- **影響檔案**: `src/main.py`, `src/data/finmind_client.py`
- **狀態**: Open
- **解決方案**: 加入中文股名對照表，支援模糊搜尋。

### UX-02: 頁面切換無載入指示
- **嚴重度**: P2
- **類型**: UX / 視覺反饋
- **報告者**: UX 改進路線圖
- **日期**: 2026-06-18
- **描述**: 切換頁面時空白無 spinner（部分頁面已有，但非全面）。
- **影響檔案**: `src/pages/router.py`
- **狀態**: Open
- **解決方案**: 加入全域 loading spinner。

### UX-14: 關注列表並發寫入
- **嚴重度**: P2
- **類型**: Bug / 資料完整性
- **報告者**: UX 改進路線圖
- **日期**: 2026-06-18
- **描述**: 多 session 同時寫入 watchlist.yaml 可能損壞檔案。
- **影響檔案**: `src/services/watchlist.py`
- **狀態**: Open
- **解決方案**: 加入 filelock 並發控制。

---

## 已完成問題

| ID | 標題 | 完成日期 | 說明 |
|----|------|----------|------|
| TD-01 | Plugin Chassis 重構 | 2026-06-18 | Phase 1+2 完成，24 個頁面全部遷移至 PluginRegistry |
| TD-02 Phase 1 | i18n 全面化 — 前 5 頁 | 2026-06-18 | etf_browser, financial_health, group_structure, peer_comparison, etf_detail 已遷移 |
| C170 | 可點擊 Glossary | 2026-06-17 | `glossary_service.py` + `_glossary_tooltip()` 已全面使用 |
| C188 | 為什麼漲跌？ | 2026-06-17 | `stock_movement_explainer.py` + `_why_moved.py` 已實作 |
| C204 | 信心指標 | 2026-06-17 | `_confidence_badge()` 已在多頁使用 |
| C205 | 閱讀時間指示器 | 2026-06-17 | `_section_title_with_read_time()` 已實作 |
| D-125 | chart_stock.py 拆分 | 2026-06-17 | 已拆分至 chart_stock_financial/health/valuation.py |
| TD-04 | business_card.py 拆分 | 2026-06-17 | 已拆分至 business_card/ 子目錄 |
| UX-05 | ROE TTM 修正 | 2026-06-18 | `roe_calculator.py` 已實作 TTM，`financial_health.py` + `peer_comparison.py` 已正確使用 |
|| UX-07 | 關注列表視覺反饋 | 2026-06-18 | `_summary_hero.py` + `watchlist_page.py` 已有 `st.toast()` |
|| TD-06 | 色彩系統統一 | 2026-06-20 | 所有 src/ 檔案已統一使用標準色彩 token（b53546d + 6d8d691） |
|| TD-07 | 元件一致性 | 2026-06-20 | 無 bare st.metric() 呼叫，全部使用 _白话_card()（b53546d） |
