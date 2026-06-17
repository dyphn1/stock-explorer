# ADR-003: 採用嚴格分層架構

## 狀態
已接受

## 日期
2026-06-07

## 背景

初始開發採用「code-first」方式，導致程式碼混雜了數據存取、業務邏輯和 UI 渲染，難以維護和測試。

## 決策

採用**嚴格四層架構**，每層有明確職責和禁止事項。

## 架構定義

```
Presentation Layer (src/pages/)
    ↕ 只依賴
Routing Layer (src/pages/router.py)
    ↕ 只依賴
Business Logic Layer (src/services/)
    ↕ 只依賴
Data Layer (src/data/)
```

## 各層職責

### Data Layer (`src/data/`)
- **職責**：FinMind API 封裝、快取管理
- **返回**：pandas DataFrame 或 dict
- **禁止**：import streamlit、包含業務邏輯

### Business Logic Layer (`src/services/`)
- **職責**：計算指標、生成圖表、白話翻譯
- **返回**：計算結果或圖表物件
- **禁止**：import streamlit、直接呼叫 API、有 side effects

### Routing Layer (`src/pages/router.py`)
- **職責**：管理 session_state、選擇 View、協調數據載入
- **禁止**：直接產生 UI 元件

### Presentation Layer (`src/pages/*.py`)
- **職責**：純渲染，接收 data dict，產生 Streamlit UI
- **禁止**：直接呼叫 API、直接讀寫快取、複雜計算

## 理由

1. **可測試性**：每層可獨立測試
2. **可維護性**：修改一層不影響其他層
3. **AI Agent 友好**：明確的邊界讓 AI 知道每個檔案該放在哪裡

## 後果

- ✅ 程式碼有明確歸屬
- ✅ 可獨立測試每層
- ⚠️ 初期開發速度較慢（需要遵循分層）
- ⚠️ 需要嚴格執行，否則容易退化
