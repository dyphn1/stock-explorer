# Stream Explorer UI/UX Issues
**Date**: 2026-06-21
**Source**: Daniel (Discord)
**Priority**: P0 — Blocks basic usage

## Issues

### 1. 大量 string 沒有印出來
- `t()` 找不到 key 時回傳 key 本身，導致介面顯示 raw key 而非翻譯
- **Root cause**: 7 個 locale keys 缺失
- **Status**: 已修復 ✅ (補齊 app.title, main.sidebar.*, main.welcome.subtitle)

### 2. 畫面只有一張卡片，需要大量下滑
- 改善計劃尚未執行
- **Action needed**: UX redesign — 減少不必要的垂直滾動

### 3. main.sidebar.navigation_header 無用
- 不能點、沒有功能
- **Action needed**: 砍掉整個 navigation_header 區塊

### 4. ETF 功能與股票功能相同
- ETF 跟股票性質不同，不應該有一樣的功能
- **Action needed**: 重新設計 ETF 區塊

### 5. UI/UX 應提升為 P0
- 缺乏基本自動化測試
- **Action needed**: 
  - UI/UX 設為 P0
  - 加入自動化測試（不只測 logic，也要測畫面 render）

### 6. 每次執行角色最少要有兩次質疑者
- 目前 Challenger 只有 1 個
- **Action needed**: 每次 cron 執行至少要 Challenger 質疑 2 次以上

### 7. 畫面行為驗證 — 需要 Playwright 自動化測試
- 目前只有 unit test，沒有畫面層級的自動化驗證
- **Action needed**: 
  - 導入 Playwright（或類似工具）做 headless browser 測試
  - 驗證關鍵 UI 元素是否有正確渲染（不只是測邏輯）
  - 截圖比對：預期畫面 vs 實際畫面
  - 驗證 t() 翻譯是否正確顯示（不是顯示 raw key）
  - 驗證互動行為（按鈕點擊、頁面切換等）

## Acceptance Criteria
- [ ] 所有 t() key 都存在，介面不再顯示 raw key
- [ ] 主畫面不用滾動就能看完所有卡片
- [ ] navigation_header 已移除
- [ ] ETF 頁面有獨立功能設計
- [ ] UI/UX 自動化測試已加入
- [ ] 每次 cron 有 ≥2 次質疑
- [ ] Playwright 畫面驗證測試已加入
