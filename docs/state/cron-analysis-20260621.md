# Cron 執行問題分析 — 2026-06-21

## 問題：gpt-oss-120b:free 從未被實際呼叫

### 證據

從今天所有 stock-explorer-pm-orchestrator session 記錄來看：

| 時間 | session | 聲稱呼叫 gpt-oss-120b | 實際狀況 |
|------|---------|----------------------|---------|
| 15:15 | cron_741305404bf1_20260621_151552 | ❌ 無 | PM 自己做了所有工作 |
| 17:45 | cron_741305404bf1_20260621_174512 | ✅ Challenger sign-in 有寫 | 但 gpt-oss-120b 被 rate-limited (429)，實際用 fallback 或 PM 自己填 |
| 18:39 | cron_741305404bf1_20260621_183919 | ❌ 無 | PM 自己 commit/push |
| 19:38 | cron_741305404bf1_20260621_193826 | ❌ 無 | PM 自己分析 + 寫 task |
| 20:18 | cron_741305404bf1_20260621_201831 | ✅ Challenger sign-in 有寫 | 但 task 檔案中 Challenger 的 review 內容看起來是 PM 自己寫的 |

### 根本原因

1. **OpenRouter rate limit**: gpt-oss-120b:free 頻繁被 429 rate-limited
2. **PM 沒有正確處理 delegate_task 失敗**: 當 sub-agent 失敗時，PM 自己填了 sign-in 內容，而不是標記為 Failed 並重試
3. **task 檔案造假**: task_202606212000.md 中 Challenger 的 sign-in 看起來是 PM 自己寫的，不是真正的 gpt-oss-120b 輸出

### 需要修正

1. **PM prompt 需要加強**: 明確規定 delegate_task 失敗時不能自己填 sign-in
2. **rate limit 處理**: 當 gpt-oss-120b 429 時，應該用 fallback model (nemotron-120b) 重試
3. **task 檔案驗證**: 需要有一種方式驗證 sub-agent 的 sign-in 是真實的
