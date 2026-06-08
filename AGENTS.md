---
name: "stock-explorer-agents"
description: "AGENTS.md for Stock Explorer (股識). Provides AI agents with precise architecture, commands, conventions, and domain knowledge."
---

# 股識 Stock Explorer - AI Developer Guide

> A Streamlit-based web application using Python and the FinMind API to provide plain-language, PPT-style educational dashboards for Taiwanese stocks. Designed for novices, it translates complex financial data into understandable stories without offering stock-picking advice.

---

## Team Roles & Collaboration

### Role Definitions

| Role | Type | Responsibility | Decision Scope |
|------|------|---------------|----------------|
| **Daniel (Client)** | Human | End-user, UX quality judgment | Final decision on UI/visual/info architecture |
| **Product Manager** | Main agent | Global planning, prioritization, milestone management, team coordination | Task assignment, progress tracking, cross-module consistency, reflection & plan adjustment |
| **System Architect** | sub-agent | Layered architecture, data flow, error handling, cross-module integration | Technical solutions, architecture changes |
| **Developer** | sub-agent | Write code, import checks, git commits | Implementation details, tech stack choices |
| **QA Engineer** | script + vision agent | Functional verification (import, rendering, smoke test) + screenshot analysis | Quality gate, issue reporting |
| **Design Reviewer** | sub-agent | UX quality, theme alignment, code review, visual inspection | Design-implementation alignment |

### Model Assignment

**Current environment**: `openrouter/owl-alpha` is the only configured model. All sub-agents use it.

**When multiple models are available** (configured in `config.yaml`), the PM should assign the appropriate model to each sub-agent via the `model` parameter in `delegate_task`:

| Role | Preferred Model | Reason |
|------|----------------|--------|
| Product Manager | `claude-sonnet-4` or equivalent | Strong reasoning, multi-step planning |
| System Architect | `claude-sonnet-4` or equivalent | Deep technical analysis |
| Developer | `claude-sonnet-4` or `gpt-4o` | Code generation strength |
| QA Engineer (Visual) | `gpt-4o` or `claude-sonnet-4` | Vision capabilities for screenshot analysis |
| Design Reviewer | `claude-sonnet-4` | Design reasoning + vision |

**Key principle**: Each role should use its ideal model, not a single model for everything. When only one model is available, all roles use it.

### Verification Strategy (Updated 2026-06-08)

**Screenshot-based visual verification is now the primary QA method.**

1. **Layer 0** (static): `_verify_layer0.py` — syntax, import, key uniqueness
2. **Layer 1** (rendering): `_verify_layer1.py` — AppTest page rendering
3. **Layer 2** (interaction): `_verify_layer2.py` — Playwright interaction testing
4. **Layer 3** (visual/UX): **Screenshot + Vision Agent** — capture screenshots at key interaction points, analyze with vision model for layout issues, contrast problems, broken elements

**Screenshot verification flow:**
```bash
# 1. Start Streamlit
uv run streamlit run src/main.py --server.port 8501 --server.headless true &

# 2. Capture screenshots at key pages
uv run python scripts/capture_screenshots.py

# 3. Analyze with vision agent
# (PM delegates to QA Engineer role with vision model)
```

**What to check in screenshots:**
- Layout breaks (overlapping elements, misaligned columns)
- Color contrast (text readable against background)
- Missing elements (buttons, charts, text that should be present)
- Visual consistency (fonts, spacing, colors match DESIGN_SYSTEM)
- Loading states (spinners appear during data loading)
- Error states (error messages are user-friendly)

### Collaboration Principles

1. **Functional bugs → auto-fix, don't bother Daniel** (import errors, runtime errors, blank pages)
2. **UX quality → write to PENDING_REVIEW.md for Daniel's confirmation** (visual aesthetics, info architecture, plain-language quality, intuitiveness)
3. **Global reflection first**: reflect on global state before each development, check cross-module consistency
4. **Verification via script**: mechanical verification via script; reasoning-heavy tasks via sub-agents
5. **Team involvement in design**: PM facilitates multi-sub-agent discussion from each role's perspective — not PM doing everything alone
6. **Roles documented in project**: team roles and collaboration flow must be written in AGENTS.md, not defined ad-hoc in prompts

### Development Cycle

```
Design > Analyze > Reflect > Synthesize > Redesign → loop until no gaps remain, then implement
```

### Workflow (per cron trigger)

```
Global Reflection → Bug Fix → New Feature Development → Code Review → Reflection & Adjustment → Update Report
```

1. **Global Reflection**: Read STATUS.md + ISSUES.md + PENDING_REVIEW.md, assess current state
2. **Bug Fix**: If unresolved bugs → fix sub-agent → verify script → clear bug entry
3. **New Feature Development**: If no bugs → dev sub-agent → verify script → mark complete
4. **Code Review**: Code review sub-agent checks quality, consistency, theme alignment
5. **Reflection & Adjustment**: Synthesize verification + review results, decide if fixes or plan adjustments needed
6. **Daniel Confirmation**: If UX quality issue → write to PENDING_REVIEW.md (UX issues only, not functional bugs)

### Verification (Layered)

| Layer | File | Scope | Duration |
|-------|------|-------|----------|
| Layer 0 | `_verify_layer0.py` | Syntax + import + key uniqueness + architecture compliance | < 5s |
| Layer 1 | `_verify_layer1.py` | AppTest page rendering (all pages, no exceptions) | < 30s |
| Layer 2 | `_verify_layer2.py` | Playwright interaction (sidebar, page switching, console errors) | < 120s |
| Full | `_verify_all.py` | Run L0 → L1 → L2 sequentially, generate report | < 5min |

Run: `uv run python _verify_all.py --skip-l2` (L2 requires Playwright)

> Install Playwright: `uv add playwright && uv run playwright install chromium`

### Design & Planning Documents

| File | Content |
|------|---------|
| `docs/DESIGN_SYSTEM.md` | Design system (layout, colors, components, interaction, PPT style) |
| `docs/ARCHITECTURE.md` | Architecture (layers, data flow, error handling) |
| `docs/CURRENT_PROBLEMS.md` | Known issues (including Daniel's manual UI/UX findings) |
| `docs/PENDING_REVIEW.md` | UX quality issues pending Daniel's confirmation |
| `docs/PRODUCT_VISION.md` | Product vision, core philosophy, milestones |
| `docs/TECHNICAL_DESIGN.md` | Technical design, API research, page specs |

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
