---
name: "stock-explorer-agents"
description: "AGENTS.md for Stock Explorer (股識). Provides AI agents with precise architecture, commands, conventions, and domain knowledge."
---

# 股識 Stock Explorer - AI Developer Guide

> A Streamlit-based web application using Python and the FinMind API to provide plain-language, PPT-style educational dashboards for Taiwanese stocks. Designed for novices, it translates complex financial data into understandable stories without offering stock-picking advice.

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
