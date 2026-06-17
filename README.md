# 股識 Stock Explorer

> 認識一家公司，從這裡開始。不是股評家，是歷史學家。不喊買進賣出，只說「這家公司這些年發生了什麼事」。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 快速開始

### 環境需求
- Python 3.11+

### 安裝與啟動
```bash
# Clone
git clone https://github.com/your-username/stock-explorer.git
cd stock-explorer

# 虛擬環境
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# 安裝
pip install -e .

# 啟動
streamlit run src/main.py
```

---

## 文件導覽

| 文件 | 說明 |
|------|------|
| [`docs/overview/00-index.md`](docs/overview/00-index.md) | 📖 文件索引與導覽 |
| [`docs/overview/01-product-vision.md`](docs/overview/01-product-vision.md) | 🎯 產品願景與目標用戶 |
| [`docs/overview/02-architecture.md`](docs/overview/02-architecture.md) | 🏗️ 系統架構與分層設計 |
| [`docs/overview/03-design-system.md`](docs/overview/03-design-system.md) | 🎨 設計系統與 UI 規範 |
| [`docs/overview/04-tech-stack.md`](docs/overview/04-tech-stack.md) | 🔧 技術選型與依賴 |
| [`docs/overview/05-roadmap.md`](docs/overview/05-roadmap.md) | 🗺️ 開發路線圖 |
| [`docs/overview/06-development-guide.md`](docs/overview/06-development-guide.md) | 📝 開發指南 |
| [`docs/adr/`](docs/adr/) | 📋 架構決策記錄 (ADR) |
| [`AGENTS.md`](AGENTS.md) | 🤖 AI Agent 團隊路由 |

---

## 核心概念

| 術語 | 定義 |
|------|------|
| **FinMind** | 主要數據來源，提供 50+ 台灣股票數據集，每日更新 |
| **十秒測試** | 核心 UX 原則：新手必須能在 10 秒內理解並複述一頁的核心概念 |
| **PPT 風格** | 設計哲學：圖表主導、比喻輔助、最小化文字 |
| **分層架構** | 嚴格四層：Data → Service → Router → Presentation |

---

## 功能特色

### 1. 公司名片頁
一句話定位、營收來源圓餅圖、關鍵數字生活化比喻、近期動態白話摘要

### 2. 營運健檢
營收趨勢、股價走勢、法人動向、營運摘要

### 3. 財務體質
利潤漏斗、關鍵比率、資產負債結構、現金流量

### 4. 同業比較
與產業龍頭的並排比較、雷達圖、差異分析

### 5. 集團架構
母公司→子公司點對點關係圖

### 6. ETF 專區
ETF 瀏覽、詳細頁、配息排行

### 7. 關注列表
YAML 基礎的價格提醒與關注管理

### 8. 事件儀表板
自適應更新、重大事件通知

---

## 安全與隱私

- **數據本地化**：執行在本機，數據從 FinMind 取得後快取於本地
- **LLM 安全**：LLM 僅用於翻譯財務術語為白話文，不做投資建議
- **免責聲明**：本工具不構成任何投資建議

---

## 貢獻

歡迎開 Issue 或提交 PR。開發前請先閱讀 [`docs/overview/06-development-guide.md`](docs/overview/06-development-guide.md)。

---

## 授權

[MIT License](LICENSE)
