# ADR-008: 全 Config 驅動設計

## 狀態
已接受

## 日期
2026-06-07

## 背景

Stock Explorer 需要支援關注列表、事件記錄、學習課程等功能。這些數據需要持久化，但 MVP 階段不適合引入資料庫。

## 決策

使用 **YAML 文件**作為配置和數據儲存，實現全 config 驅動設計。

## 配置檔案清單

| 檔案 | 用途 |
|------|------|
| `config/watchlist.yaml` | 關注列表、價格提醒 |
| `config/events.yaml` | 事件記錄 |
| `config/quiz.yaml` | 理解力測驗題目 |
| `config/lessons/` | 學習學院課程內容 |
| `config/comprehension_quiz.yaml` | 理解力測驗中繼資料 |

## 理由

1. **零依賴**：不需要資料庫
2. **人類可讀**：Daniel 可以直接編輯
3. **版本控制**：YAML 檔案可納入 Git
4. **AI Agent 友好**：易於讀寫

## 替代方案

| 方案 | 不選原因 |
|------|----------|
| SQLite | MVP 階段過度設計 |
| JSON | 不支援註解，可讀性較差 |
| 資料庫（PostgreSQL） | 部署複雜度高 |

## 後果

- ✅ 零成本持久化
- ✅ 易於備份和版本控制
- ⚠️ 並發寫入需要 filelock
- ⚠️ 大量數據時效能較差（目前可接受）
