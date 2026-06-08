---
name: "stock-explorer-agents"
description: "AGENTS.md for Stock Explorer (股識). Provides AI agents with precise architecture, commands, conventions, and domain knowledge."
---

# 股識 Stock Explorer - AI Developer Guide

> A Streamlit-based web application using Python and the FinMind API to provide plain-language, PPT-style educational dashboards for Taiwanese stocks. Designed for novices, it translates complex financial data into understandable stories without offering stock-picking advice.

---

## 團隊角色與協作流程

### 角色定義

| 角色 | 類型 | 職責 | 決策範圍 |
|------|------|------|----------|
| **Daniel（客戶端）** | 人類 | 最終使用者，體驗品質判斷 | UI/視覺/資訊架構的最終決策 |
| **產品經理** | 主 agent | 全局規劃、優先級排序、里程碑管理、協調團隊 | 任務分派、進度管理、跨模組一致性、反思調整規劃 |
| **系統架構師** | sub-agent | 分層架構、資料流、錯誤處理規範、跨模組整合 | 技術方案、架構調整 |
| **開發者** | sub-agent | 寫 code、import 檢查、commit | 實現細節、技術選型 |
| **QA 工程師** | script | 功能驗證（import、渲染、煙測） | 品質把關、問題回報 |
| **設計評審** | sub-agent | 體驗品質、主題一致性、code review | 設計與實作的對齊 |

### 協作原則

1. **功能 bug → 自動修復，不找 Daniel**（import error、runtime error、空白頁面）
2. **體驗品質 → 寫入 PENDING_REVIEW.md 請 Daniel 確認**（視覺美感、資訊架構、白話品質、直覺性）
3. **全局反思優先**：每次開發前反思全局狀態，檢查跨模組一致性
4. **驗證用 script**：機械性驗證用 script；需要推理的用 sub-agent
5. **團隊參與設計**：PM 協調多個 sub-agent 從各自角色角度討論，不是 PM 一人全包
6. **角色定義要記錄在專案上**：團隊角色、協作流程寫入 AGENTS.md，不能只靠 prompt 臨時定義

### 開發流程

```
設計 > 分析 > 反思 > 歸納整理 > 重新設計 → 循環到沒缺口才實作
```

### 工作流（每次 cron 觸發）

```
全局反思 → Bug 修復 → 新功能開發 → Code Review → 反思與調整 → 更新報告
```

1. **全局反思**：讀 STATUS.md + ISSUES.md + PENDING_REVIEW.md，判斷當前狀態
2. **Bug 修復**：如果有未修復 bug → 修復 sub-agent → verify script → 清除 bug
3. **新功能開發**：如果無 bug → 開發 sub-agent → verify script → 標記完成
4. **Code Review**：code review sub-agent 檢查品質、一致性、主題對齊
5. **反思與調整**：綜合驗證 + 評審結果，決定是否需要修復或調整規劃
6. **Daniel 確認**：如果涉及體驗品質問題 → 寫入 PENDING_REVIEW.md

### 驗證方式

驗證 script 位於專案根目錄，分三層：

| 層級 | 檔案 | 內容 | 耗時 |
|------|------|------|------|
| Layer 0 | `_verify_layer0.py` | 語法 + import + key 唯一性 + 分層架構 | < 5s |
| Layer 1 | `_verify_layer1.py` | AppTest 所有頁面渲染測試 | < 30s |
| Layer 2 | `_verify_layer2.py` | Playwright 側邊欄 + 頁面切換 + console error | < 120s |
| 全流程 | `_verify_all.py` | 依序執行 L0 → L1 → L2，產出報告 | < 5min |

執行方式：`uv run python _verify_all.py --skip-l2`（L2 需要 Playwright）

> Playwright 安裝：`uv add playwright && uv run playwright install chromium`

### 設計規範文件

| 檔案 | 內容 |
|------|------|
| `docs/DESIGN_SYSTEM.md` | 設計系統規範（版面、顏色、元件、互動、PPT 風格） |
| `docs/ARCHITECTURE.md` | 架構定義（分層、資料流、錯誤處理） |
| `docs/CURRENT_PROBLEMS.md` | 目前已知問題（含 Daniel 手動測試的 UI/UX 問題） |
| `docs/PENDING_REVIEW.md` | 待 Daniel 確認的體驗品質問題 |
| `docs/PRODUCT_VISION.md` | 產品願景、核心理念、里程碑 |
| `docs/TECHNICAL_DESIGN.md` | 技術設計、API 研究、頁面詳細設計 |

## Tech Stack & Architecture

- **Frontend/Backend**: Python 3.11+, Streamlit
- **Visualization**: Plotly + custom CSS (PPT style)
- **Data Source**: FinMind API (50+ datasets, daily updates)
- **LLM Integration**: Restricted strictly to plain-language translation/summarization, not fact interpretation

```
config/
  watchlist.yaml
docs/
  M4_DESIGN.md
  PRODUCT_VISION.md
  TECHNICAL_DESIGN.md
  ...
src/
  data/
    finmind_client.py
    models.py
  pages/
    business_card.py
    operation_checkup.py
    financial_health.py
    peer_comparison.py
    ...
  services/
    chart.py
    news_summarizer.py
    ...
  main.py
tests/
```

| Directory | Purpose |
|---|---|
| `src/data/` | FinMind API client and local data models. |
| `src/pages/` | Streamlit pages defining the dashboard views. |
| `src/services/` | Business logic for chart generation, news summarizing, and revenue analysis. |
| `docs/` | Architecture, product vision, and technical design documents. |

## Development Commands

All commands are executed from the repository root unless otherwise noted.

### Setup & Dependencies
```bash
# Create a virtual environment to avoid polluting the global Python environment
python -m venv .venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate
# Activate the virtual environment (macOS/Linux)
# source .venv/bin/activate

# Install the package and its dependencies in editable mode
pip install -e .
```

### Local Development
```bash
# Start the Streamlit server
streamlit run src/main.py
```
- The application runs on: `http://localhost:8501` (default Streamlit port)

### Testing
```bash
# Run pytest for the test suite
pytest
```

## Conventions

- **Package Manager**: Use `pip` in conjunction with `pyproject.toml`.
- **UI Design**: Adhere strictly to the "PPT Style" - image/chart heavy, minimal text walls. One core message per page.
- **Verification Principle**: All UI/UX implementations must pass the "10-second test" (a beginner must be able to comprehend and summarize the page's core point within 10 seconds).
- **LLM Usage**: When integrating AI generation, LLMs are restricted to translating professional financial jargon into analogies/plain text. They must not perform fact derivation or autonomous financial analysis.

## Product Domain Knowledge

- **Company Business Card (公司名片)**: One-line company summary and revenue breakdown. Managed in `src/pages/business_card.py`.
- **Operational Checkup (營運健檢)**: Analyzes how the company makes money and its stability. Managed in `src/pages/operation_checkup.py`.
- **Financial Health (財務體質)**: Translates financials into "how much is earned, spent, and left". Managed in `src/pages/financial_health.py`.
- **Peer Comparison (同業比較)**: Benchmarks the company against industry leaders with analogies. Managed in `src/pages/peer_comparison.py`.

## Do Not Edit

- `.streamlit/secrets.toml` — Ephemeral local secrets for development.
- `__pycache__/` and `*.egg-info/` — Ephemeral Python build output directories.

## System Boundaries & Gotchas

- **FinMind Limits**: Avoid excessive, un-cached calls to FinMind to prevent rate limiting. The system relies on a local file caching mechanism + invalidation.
- **No Stock Picking**: Do not introduce any features that calculate buy/sell signals, target prices, or predictive modeling. The application acts as a "historian", strictly reporting past and present operational state.
