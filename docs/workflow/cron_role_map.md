# Stock Explorer - Cron Role Map

## Cron Theme Rotation

| Cycle | Theme | Description |
|-------|-------|-------------|
| 1 | 🔧 Development | Fix bugs and implement features |
| 2 | 💡 Discussion | Feature planning and future direction |
| 3 | 🔍 Review | Gap analysis, product optimization, competitor research |

---

## Roles

| Role | Model | Responsibility |
|------|-------|----------------|
| **Cron** | - | Start the theme and wake up the team |
| **PM** | owl-alpha | Coordinate, synthesize, and assign work |
| **Architect** | nemotron-120b | Architecture analysis and technical proposals |
| **Developer** | owl-alpha | Implementation and bug fixes |
| **Design Reviewer** | gemma-31b | Visual/UX review |
| **QA Engineer** | gemma-31b | Verification, competitor research |
| **Challenger** | gpt-oss-120b:free | Question, counter-prove, ensure goal alignment |

---

## Challenge Process (MANDATORY)

**Every important decision must go through at least 3 rounds of challenge:**

```
Round 1: Team proposes a plan
    ↓
Challenger questions (Why? Are there alternatives? What are the risks?)
    ↓
Round 2: Team responds to questions, revises the plan
    ↓
Challenger questions again (Loopholes? Contradictions?)
    ↓
Round 3: Team gives final response
    ↓
Challenger confirms: goals are aligned → Approved
```

**Goal:** Not to oppose for the sake of opposing, but to ensure every decision can withstand scrutiny through the challenge process.

---

## Each Role's Responsibilities per Cron

### 1. Cron (Initiator)
- Reads `docs/state/handoff.md` to determine the theme for this cycle
- Wakes up the Main Agent (PM)
- Appends the current theme to `docs/state/handoff.md`

### 2. Main Agent / PM (Coordinator)
- Reads `docs/state/handoff.md`, `docs/state/issues.md`, `docs/state/pending_review.md`
- Initiates team discussion (standup)
- Synthesizes input from all roles
- Decisions can only be confirmed after **at least 3 rounds of challenges**
- Writes back to status files

### 3. System Architect
- **Development theme:** Analyze technical feasibility, propose architecture plans
- **Discussion theme:** Evaluate technical impact of new features
- **Review theme:** Examine technical debt, propose refactoring recommendations

### 4. Developer
- **Development theme:** Implement features, fix bugs
- **Discussion theme:** Estimate implementation cost, provide time estimates
- **Review theme:** Refactor code, optimize performance

### 5. Design Reviewer
- **Development theme:** Review UI/UX implementation
- **Discussion theme:** Provide design direction recommendations
- **Review theme:** Compare competitor designs, propose improvements

### 6. QA Engineer
- **Development theme:** Execute verification (L0/L1/L2)
- **Discussion theme:** Evaluate testing strategy
- **Review theme:** Run competitor comparison and write to `docs/research/competitor_research.md`

### 7. Challenger ⭐ NEW
- **All themes:** Listen to team discussions, question every decision
- Require at least 3 rounds of challenges before confirming any decision
- Ensure team goal alignment
- Key questions:
  - Does this plan actually solve the problem?
  - Is there a simpler/better alternative?
  - What are the risks? Anything missing?
  - Are there contradictions between roles' opinions?

---

## State Handoff Mechanism

### Status Files (all kept within the project)

| File | Purpose | When Updated |
|------|---------|--------------|
| `docs/state/handoff.md` | Single source of truth: all cycle records | Every cron run ends |
| `docs/state/issues.md` | Known bugs and follow-up items | When new issues are found |
| `docs/state/pending_review.md` | Items waiting for Daniel's decision | When human judgment is needed |
| `docs/state/current_problems.md` | All known problems, including non-bugs | During review themes |
| `docs/decisions/competitor_research.md` | Competitor research report | During review themes |
| `docs/logs/challenge_log.md` | Challenger's challenge records | Whenever a challenge occurs |

### Handoff Flow

```
Cron initiates theme
    ↓
PM reads docs/state/handoff.md + issues.md + pending_review.md
    ↓
PM initiates team discussion (delegate_task to Architect, Developer, Designer, QA)
    ↓
Each role returns opinions/results
    ↓
PM synthesizes → proposes a plan
    ↓
Challenger questions (Round 1)
    ↓
PM coordinates team response → revised plan
    ↓
Challenger questions (Round 2)
    ↓
PM coordinates team response → final plan
    ↓
Challenger questions (Round 3)
    ↓
Challenger confirms: goals are aligned
    ↓
PM assigns work to Developer
    ↓
Developer implements → verifies → commits
    ↓
PM appends to docs/state/handoff.md + updates issues.md
    ↓
Done
```

---

## Basic Info

**Available models (all via `provider: openrouter`):**

| Model | Role(s) |
|-------|---------|
| `openrouter/owl-alpha` | PM, Developer |
| `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | Architect |
| `openrouter/google/gemma-4-31b-it:free` | Design Reviewer, QA Engineer |
| `openrouter/openai/gpt-oss-120b:free` | **Challenger** |

---

*Last updated: 2026-06-09*
