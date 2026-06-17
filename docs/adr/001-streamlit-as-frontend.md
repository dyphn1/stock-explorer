# ADR-001: 選擇 Streamlit 作為前端框架

## 狀態
已接受

## 日期
2026-06-06

## 背景

Stock Explorer 是一個 MVP 階段的工具，需要快速迭代。團隊需要一個能讓 Python 開發者快速構建數據應用的前端框架。

## 決策

選擇 **Streamlit** 作為前端框架。

## 理由

1. **開發速度**：純 Python 開發，無需前端知識，適合快速迭代
2. **數據友好**：原生支援 pandas DataFrame、Plotly 圖表
3. **MVP 定位**：適合單一用戶本地部署，不需要複雜的使用者認證
4. **AI Agent 友好**：Python 程式碼易於 AI Agent 理解和修改

## 替代方案

| 方案 | 優點 | 缺點 | 不選原因 |
|------|------|------|----------|
| React + FastAPI | 完整前後端分離 | 開發成本高、需要前端知識 | MVP 階段過度設計 |
| Gradio | 更輕量 | 客製化能力較弱 | 佈局靈活性不足 |
| Flask + Jinja2 | 完全控制 | 需手寫 HTML/JS | 開發速度慢 |

## 後果

- ✅ 快速交付 MVP
- ✅ 降低 AI Agent 開發門檻
- ⚠️ 多用戶部署受限（Streamlit 設計為單用戶）
- ⚠️ 行動版體驗受限
- ⚠️ 高度客製化 UI 需透過 CSS injection

## 未來考量

若未來需要多用戶部署或行動版，可考慮遷移至 React/Vite + FastAPI。但當前 MVP 階段，Streamlit 是最佳選擇。
