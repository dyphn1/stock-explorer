# 股識 Stock Explorer

> 認識一家公司，從這裡開始。不是股評家，是歷史學家。不喊買進賣出，只說「這家公司這些年發生了什麼事」。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

股識 (Stock Explorer) is a tool designed to help novice and curious investors understand Taiwanese companies through a plain-language, PPT-style, story-first approach. Instead of raw numbers and stock recommendations, it provides a historical and operational overview using the FinMind API and LLMs to explain the "how" and "why" behind a business's operations, financial health, peer comparisons, and group structures.

---

## Getting Started

### Prerequisites
- Python 3.11+
- FinMind API (for extensive queries, though some core endpoints are free)
- `.env` file containing any required secrets

### Installation / Deployment
```bash
# Clone the repository
git clone https://github.com/your-username/stock-explorer.git
cd stock-explorer

# Create a virtual environment to avoid polluting the global Python environment
python -m venv .venv

# Activate the virtual environment (Windows)
.venv\Scripts\activate
# Activate the virtual environment (macOS/Linux)
# source .venv/bin/activate

# Install dependencies in editable mode
pip install -e .
```

### Initial Configuration
Copy `.env.example` to `.env` (if provided) and fill in your keys.

Start the Streamlit application:
```bash
streamlit run src/main.py
```

---

## Core Workflow & Features

### 1. Company Business Card
An at-a-glance dashboard that provides a one-line summary, a pie chart of revenue sources (with plain-language explanations), and highlights of recent significant events.

### 2. Operational Checkup
Explores the core of the business: how the company makes money, the stability of its income, and historical comparisons.

### 3. Financial Health
Breaks down complex financial statements into relatable concepts: how much the company earns, how much it spends, and what is left over.

### 4. Peer Comparison & Group Structure
Benchmarks the company against industry leaders using practical analogies and maps out parent-subsidiary relationships in an intuitive node structure.

---

## Concepts & Glossary

| Term | Definition |
|---|---|
| `FinMind` | The primary data source, an API providing 50+ financial datasets for Taiwanese stocks, updated daily. |
| `10-Second Test` | The core UX principle: A beginner must be able to understand and summarize a page's core concept within 10 seconds. |
| `PPT Style` | The design philosophy emphasizing charts, analogies, and minimal text, rather than dense data tables. |

---

## Security & Privacy

- **Data Locality:** Execution happens locally. Data is fetched from FinMind and cached via local file storage mechanisms.
- **LLM Safety:** Any integrated Large Language Models are strictly confined to translating financial jargon into plain text. They are intentionally prohibited from making factual derivations or stock recommendations.

---

## FAQ & Limitations

- **Q: Does this tool tell me what to buy?**
  - **A:** No. Stock Explorer acts purely as a "historian." It explains the company's past and present business operations.
- **Known Limitation:** Currently operates as an MVP focused on analyzing a single stock profile across 5 core views.

---

## Support & Community

- Need help? Open an [Issue](https://github.com/your-username/stock-explorer/issues).

---

## For Developers

Want to build `Stock Explorer` from source or contribute? 
Please see our [Contributing Guide](CONTRIBUTING.md) (if available) and the AI instructions in [`AGENTS.md`](AGENTS.md).
