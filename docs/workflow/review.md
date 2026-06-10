# 🔍 Review Workflow (REVIEW WORKFLOW)

> When the current theme is "Review" (determined from `docs/state/handoff.md`), the PM follows this workflow.

---

## Review Theme Objectives
- Examine product gaps
- Optimize existing features
- **Competitor Research**: Search the web for similar products and compare feature gaps
- Generate new feature suggestions

---

## Flowchart (Complete)

```mermaid
flowchart TD
    A([🔍 Review Theme Start]) --> B[PM reads docs/state/handoff.md]
    B --> C[PM reads docs/state/current_problems.md]
    C --> D[PM reads docs/decisions/competitor_research.md]
    
    D --> E[PM calls all sub-agents in parallel]
    
    E --> F[Architect reviews architecture debt]
    E --> G[Design Reviewer compares competitor designs]
    E --> H[QA Engineer searches the web for competitors]
    E --> I[Developer estimates optimization costs]
    
    F --> J[PM consolidates all findings]
    G --> J
    H --> J
    I --> J
    
    J --> K[PM forms "Review Report"]
    K --> L[New features → ISSUES.md]
    K --> M[Design improvements → CURRENT_PROBLEMS.md]
    K --> N[Technical debt → TECH_DEBT.md]
    
    L --> O[PM calls Challenger]
    M --> O
    N --> O
    
    O --> P{Challenger Round 1}
    
    P --> Q1[Challenger questions: Are these really gaps?]
    Q1 --> R1[Team responds]
    R1 --> S1{Challenger Round 2}
    
    S1 --> Q2[Challenger questions: Is the priority correct?]
    Q2 --> R2[Team responds]
    R2 --> S2{Challenger Round 3}
    
    S2 --> Q3[Challenger questions: Goal alignment?]
    Q3 --> R3[Team final response]
    R3 --> T{Challenger confirms?}
    
    T -- No --> U[Team re-discusses]
    U --> J
    
    T -- Yes --> V[PM updates all status files]
    V --> W[PM writes to CHALLENGE_LOG.md]
    W --> X[PM reports to Daniel]
    X --> Z([End])
```

---

## Three-Round Challenge Process (Detailed)

### Round 1: Gap Authenticity Challenge
```
Challenger asks:
- Are these "feature gaps" really gaps? Or do we simply not need them?
- Just because competitors have it doesn't mean we should too. Why should we build it?
- Are there things "competitors don't have but we should"?

Team responds:
- QA supplements competitor research details
- Designer supplements UX analysis
- Architect supplements technical feasibility
```

### Round 2: Priority Challenge
```
Challenger asks:
- Are the priorities for these new features correct?
- What should be done first? Why?
- Is there more important technical debt to address first?

Team responds:
- PM responds based on STATUS.md priorities
- Developer supplements cost analysis
```

### Round 3: Goal Alignment Challenge
```
Challenger asks:
- Does this optimization direction align with the product vision?
- Are there any contradictions?
- What are the risks?

Team responds:
- Final confirmation or plan revision
```

---

## PM Tasks (Detailed)

### Step 1: Read Status
```
1. docs/state/handoff.md → Find the 🔍 Review section to restore context
2. docs/state/current_problems.md → Understand known issues
3. docs/decisions/competitor_research.md → Understand previous competitor research results
4. docs/state/tech_debt.md → Understand technical debt
```

### Step 2: Call Sub-agents in Parallel
```
Call simultaneously (parallel):
- Architect: Review architecture debt, propose refactoring suggestions
- Design Reviewer: Compare competitor designs, propose design improvements
- QA Engineer: Search the web for competitors, compare feature gaps
- Developer: Estimate optimization costs
```

### Step 3: Consolidate Review Report
```
After collecting all sub-agent input:
1. Organize feature gap list
2. Organize design improvement suggestions
3. Organize technical debt priorities
4. Form the "Review Report"
```

### Step 4: Challenge Phase
```
1. Call Challenger, provide the "Review Report"
2. Conduct at least 3 rounds of challenges
3. Record challenge content and team responses for each round
4. Cannot proceed until Challenger confirms
```

### Step 5: Write to Files
```
1. New features → docs/state/issues.md (tag: source: competitor research)
2. Design improvements → docs/state/current_problems.md
3. Technical debt → docs/state/tech_debt.md
4. Challenge records → docs/logs/challenge_log.md
5. Append to docs/state/handoff.md
```

---

## Sub-agent Tasks

### QA Engineer 🧪 (Competitor Research Lead)
1. **Search the web** for competitor information (Yahoo Finance, TradingView, Finviz, StatementDog, GoodInfo, CMoney, etc.)
2. Compare feature gaps with Stock Explorer
3. Write to `docs/decisions/competitor_research.md`
4. New feature suggestions → `docs/status/issues.md`

### Architect 🏗️
1. Read `docs/status/tech_debt.md`
2. Review architecture debt
3. Propose refactoring suggestions
4. Analyze performance bottlenecks

### Design Reviewer 🎨
1. Compare competitor designs
2. Propose design improvement plans
3. Review whether DESIGN_SYSTEM.md needs updating

### Developer 💻
1. Estimate implementation cost for each optimization
2. Provide time estimates
3. Analyze technical risks

### Challenger 🔥
1. **Challenge** the authenticity of feature gaps
2. **Challenge** whether priorities are correct
3. **Challenge** alignment with product goals
4. Confirm only after at least 3 rounds of challenges

---

## Competitor Research Checklist

QA Engineer must research the following competitors during the review theme:

| Competitor | URL | Research Focus |
|------------|-----|----------------|
| Yahoo Finance | finance.yahoo.com | Overview, navigation, watchlist |
| TradingView | tradingview.com | Charts, technical analysis, community |
| Finviz | finviz.com | Screeners, heatmap |
| StatementDog | statementdog.com | Plain-language explanations, educational content |
| GoodInfo | goodinfo.tw | Ex-dividend, fundamentals |
| CMoney | cmoney.tw | App ecosystem, AI stock picking |
| WantGoo | wantgoo.com | Market temperature, PPT export |

---

## Status Update

PM must append to `docs/state/handoff.md` under the 🔍 Review section:

```markdown
## 🔍 Review Log - YYYY-MM-DD
- **Competitor Research**: QA Engineer completed [N] competitor analyses
- **Feature Gaps**: [N] new feature suggestions
- **Design Improvements**: [N] improvement suggestions
- **Technical Debt**: [N] items pending
- **Challenger Challenges**: [3-round summary]
- **Pending Daniel Decision**: [Items written to PENDING_REVIEW.md]
```

---

## Step 6: Write Handoff File

After completing the review cycle, PM **MUST** append to `docs/state/handoff.md` under the 🔍 Review section:

```markdown
# Handoff – Review

## Summary
- **Topic**: Review (🔍)
- **Date**: `YYYY-MM-DD`
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger

## Competitor Research Findings
| Platform | Feature Gap | Suggested Improvement |
|----------|-------------|-----------------------|
|          |             |                       |

## Decisions Made
- Bullet points summarizing architectural refinements, technical debt reductions, and UX improvements identified during the review.

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
|         |             |       |          |

## Next Cycle Handoff
Reference the appropriate `handoff_*.md` for the next theme.
```

**RULES:**
- Fill in ALL tables — do not leave them empty
- Include git commit hash in the Summary for Completed Items
- If no items were completed, write "No items completed this cycle"
- This file is the **primary state handoff** for the next cron run

---

*Last updated: 2026-06-10*
