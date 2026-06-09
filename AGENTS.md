---
name: "stock-explorer-agents"
description: "AGENTS.md for Stock Explorer (股識). Provides AI agents with precise architecture, commands, conventions, and domain knowledge."
---

# Stock Explorer AI Developer Guide

> A Streamlit-based web application using Python and the FinMind API to provide plain-language, PPT-style educational dashboards for Taiwanese stocks. Designed for novices, it translates complex financial data into understandable stories without offering stock-picking advice.

---

## Team Roles & Collaboration

### Role Definitions

| Role | Type | Model | Responsibility |
|------|------|-------|-----------------|
| **Daniel (Client)** | Human | — | End-user, UX quality judgment, final decision on UI/visual/info architecture |
| **Product Manager** | Main agent | `owl-alpha` | [Product Manager role](docs/roles/pm.md) |
| **System Architect** | sub-agent | `nemotron-120b` | [System Architect role](docs/roles/architect.md) |
| **Developer** | sub-agent | `owl-alpha` | [Developer role](docs/roles/developer.md) |
| **Design Reviewer** | sub-agent | `gemma-31b` | [Design Reviewer role](docs/roles/designer.md) |
| **QA Engineer** | sub-agent | `gemma-31b` | [QA Engineer role](docs/roles/qa.md) |
| **Challenger** | sub-agent | `gpt-oss-120b` | [Challenger role](docs/roles/challenger.md) |

> **Detailed role cards:** See `docs/workflow/ROLE_CARDS.md` for full role definitions, responsibilities per theme, and work guidelines.

### Development Cycle

```
Design > Analyze > Reflect > Synthesize > Redesign → loop until no gaps remain, then implement
```

### Workflow (per cron trigger)

**Cron Theme Rotation** (every 3 cycles):
1. **🔧 開發** — Fix bugs, implement features. Workflow: `docs/workflow/dev.md`
2. **💡 討論** — Feature planning, future direction. Workflow: `docs/workflow/discuss.md`
3. **🔍 檢討** — Gap analysis, optimization, **competitor research**. Workflow: `docs/workflow/review.md`

**State Handoff Mechanism:**
All state is stored in project files — NOT in the cron prompt. Each cron run:
1. PM reads state from `STATUS.md`, `docs/status/issues.md`, `docs/status/pending_review.md`, `docs/status/current_problems.md`
2. PM reads the corresponding workflow file (`docs/workflow/{dev,discuss,review}.md`)
3. PM reads `docs/workflow/ROLE_CARDS.md` to understand each role's responsibilities
4. PM spawns sub-agents with role-specific context
5. Team discusses → Challenger challenges (3 rounds) → PM synthesizes → Developer implements
6. Results written back to state files
7. Cron prompt stays stable — only the project state changes

**Team Discussion + Challenge Flow:**
```
Cron initiates theme
    ↓
PM reads state files + workflow file + role cards
    ↓
PM spawns sub-agents (Architect, Developer, Designer, QA) with role context
    ↓
Sub-agents analyze & report (parallel)
    ↓
PM synthesizes → forms "team preliminary decision"
    ↓
PM spawns Challenger with the preliminary decision
    ↓
Round 1: Challenger questions → Team responds
Round 2: Challenger questions → Team responds  
Round 3: Challenger questions → Team responds
    ↓
Challenger confirms alignment
    ↓
PM delegates work to Developer
    ↓
Developer implements → Verification → State files updated
```

**Competitor Research** (every 3rd cycle — 檢討 theme):
- QA Engineer researches competitor products on the web
- Compares features with Stock Explorer
- Writes findings to `docs/research/competitor_research.md`
- New feature ideas → `docs/status/issues.md` (tagged `source: competitor research`)

### Model Assignment

**Available models** (all via `provider: openrouter`):

| Model | Size | Strength |
|-------|------|----------|
| `openrouter/owl-alpha` | — | Default, balanced reasoning |
| `openrouter/google/gemma-4-31b-it:free` | 31B | **Vision** (screenshot analysis), strong reasoning |
| `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | 120B | **Large context**, complex codebases |
| `openrouter/meta-llama/llama-3.2-3b-instruct:free` | 3B | **Fast**, simple tasks, web extraction |
| `openrouter/nvidia/nemotron-3-nano-30b-a3b:free` | 30B | **Compression**, summarization |

**Do NOT use:**
- `custom/gemma4:e4b` (local ollama) — too weak for real work, only for trivial tasks
- `grok-4.20-reasoning` — not configured

**Role → Model mapping:**

| Role | Model | Why |
|------|-------|-----|
| **Product Manager** | `openrouter/owl-alpha` | Default, strong planning & reasoning |
| **System Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | 120B for deep analysis of large codebases |
| **Developer** | `openrouter/owl-alpha` or `openrouter/google/gemma-4-31b-it:free` | Code generation; use gemma for complex refactors |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | **Vision** for visual inspection + strong reasoning |
| **QA Engineer (Visual)** | `openrouter/google/gemma-4-31b-it:free` | **Vision** for screenshot analysis |
| **QA Engineer (Quick check)** | `openrouter/meta-llama/llama-3.2-3b-instruct:free` | Fast pass for simple verifications |

**Usage in `delegate_task`:**
```python
# Vision task (screenshot analysis, visual QA):
delegate_task(
    goal="Analyze screenshots for visual issues",
    model="openrouter/google/gemma-4-31b-it:free",
    provider="openrouter",
    role="leaf",
    toolsets=["vision", "file"],
    ...
)

# Deep architecture analysis (large codebase):
delegate_task(
    goal="Analyze architecture issues across the full codebase",
    model="openrouter/nvidia/nemotron-3-super-120b-a12b:free",
    provider="openrouter",
    role="leaf",
    toolsets=["terminal", "file"],
    ...
)

# Standard development task:
delegate_task(
    goal="Implement a specific fix",
    model="openrouter/owl-alpha",
    provider="openrouter",
    role="leaf",
    toolsets=["terminal", "file"],
    ...
)

# Quick verification / simple task:
delegate_task(
    goal="Run quick verification check",
    model="openrouter/meta-llama/llama-3.2-3b-instruct:free",
    provider="openrouter",
    role="leaf",
    toolsets=["terminal", "file"],
    ...
)
```

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
2. **UX quality -> write to `docs/status/pending_review.md` for Daniel's confirmation** (visual aesthetics, info architecture, plain-language quality, intuitiveness)
3. **Global reflection first**: reflect on global state before each development, check cross-module consistency
4. **Verification via script**: mechanical verification via script; reasoning-heavy tasks via sub-agents
5. **Team involvement in design**: PM facilitates multi-sub-agent discussion from each role's perspective — not PM doing everything alone
6. **Roles documented in project**: team roles and collaboration flow must be written in AGENTS.md, not defined ad-hoc in prompts
7. **Proactive team discussion (CRITICAL)**: Even with no bugs and no new features, the team MUST actively discuss and improve the product. The PM should rotate through discussion topics each cycle: Architecture Review, Code Quality Review, UX/Visual Review, New Feature Exploration. Never let the team go idle — a mature team continuously improves through internal discussion.
8. **Delegate reasoning, retain coordination**: PM should ONLY do mechanical work (read status files, run verification scripts, git commit). All reasoning tasks (code analysis, architecture review, design critique, visual inspection) MUST be delegated to the appropriate sub-agent role with the appropriate model.
9. **Challenger mandatory (CRITICAL)**: Every important decision MUST go through at least 3 rounds of challenge by the Challenger role. The Challenger listens to all team discussions, questions each decision, and ensures team alignment. No decision is final until the Challenger confirms consistency. Model: `gpt-oss-120b:free`.

### Development Cycle

```
Design > Analyze > Reflect > Synthesize > Redesign → loop until no gaps remain, then implement
```

### Workflow (per cron trigger)

**Cron Theme Rotation** (every 3 cycles):
1. **🔧 開發** — Fix bugs, implement features
2. **💡 討論** — Feature planning, future direction
3. **🔍 檢討** — Gap analysis, optimization, **competitor research**

**State Handoff Mechanism:**
All state is stored in project files — NOT in cron prompts. Each cron run:
1. Reads state from `STATUS.md`, `docs/status/issues.md`, `docs/status/pending_review.md`, `docs/status/current_problems.md`
2. PM coordinates team discussion (mandatory — never skip)
3. Sub-agents do reasoning work (never PM alone)
4. Results written back to state files
5. Cron prompt stays stable — only the project state changes

**Team Discussion Flow:**
```
Cron initiates theme → PM reads state → PM spawns sub-agents →
Sub-agents analyze & report → PM synthesizes → PM delegates work →
Developer implements → Verification → State files updated
```

**Competitor Research** (every 3rd cycle — 檢討 theme):
- QA Engineer researches competitor products on the web
- Compares features with Stock Explorer
- Writes findings to `docs/research/competitor_research.md`
- New feature ideas -> `docs/status/issues.md` (tagged `source: competitor research`)

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
| `docs/design/design_system.md` | Design system (layout, colors, components, interaction, PPT style) |
| `docs/design/architecture.md` | Architecture (layers, data flow, error handling) |
| `docs/status/current_problems.md` | Known issues (including Daniel's manual UI/UX findings) |
| `docs/status/pending_review.md` | UX quality issues pending Daniel's confirmation |
| `docs/strategy/product_vision.md` | Product vision, core philosophy, milestones |
| `docs/design/technical_design.md` | Technical design, API research, page specs |
| `memories/index.md` | Memory structure overview (session, repo, user scopes) |

### Memories & State Persistence

The project uses a **`memories/`** directory to store structured markdown files that act as a lightweight, file‑based memory store for sub-agents. This keeps all state version‑controlled alongside the code.

**Directory Layout:**
```
memories/
│   index.md          # Overview of the memory structure
│
├── session/          # Temporary notes for the current cron cycle
│   └── plan.md       # High‑level plan for the current round (PM)
│
├── repo/             # Repository‑scoped facts (architecture, design system, conventions)
│   └── architecture.md
│
└── user/             # Persistent user preferences and long‑term insights
    └── preferences.md
```

**How Sub‑Agents Use It:**
- **Read** – Before performing any task, an agent reads the relevant markdown files (e.g., the PM reads `memories/session/plan.md` to know the current objectives).
- **Write** – When a decision should survive beyond the current run, the agent writes to `memories/repo/` (e.g., the Architect updates `memories/repo/architecture.md`).
- **Update** – For transient information that only lives for the current cycle, agents update files under `memories/session/`.

**PM Responsibility:** The PM creates/updates `memories/session/plan.md` at the start of each cron run and commits any changes to the `memories/` directory together with the rest of the project.

## Tech Stack & Architecture

- **Frontend/Backend**: Python 3.11+, Streamlit
- **Visualization**: Plotly + custom CSS (PPT style)
- **Data Source**: FinMind API (50+ datasets, daily updates)
- **LLM Integration**: Restricted strictly to plain-language translation/summarization, not fact interpretation

```
config/
  watchlist.yaml
docs/
  design/
    m4_design.md
    design_system.md
    technical_design.md
    ...
  strategy/
    product_vision.md
  status/
    issues.md
    pending_review.md
    current_problems.md
  research/
    competitor_research.md
  workflow/
    main.md
    dev.md
    discuss.md
    review.md
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
