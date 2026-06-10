# 💡 Discussion Topic Workflow (DISCUSS WORKFLOW)

> When STATUS.md specifies the topic as "Discussion", the PM follows this workflow.

---

## Discussion Topic Objectives
- Discuss new feature directions
- Evaluate future development roadmap
- Gather input from all roles
- Form team consensus

---

## Flowchart (Complete)

```mermaid
flowchart TD
    A([💡 Discussion Topic Start]) --> B[PM reads STATUS.md]
    B --> C[PM reads all status files]
    C --> D[PM reads COMPETITOR_RESEARCH.md]
    
    D --> E[PM calls Architect]
    E --> F[Architect analyzes technical feasibility]
    F --> G[Architect proposes 2-3 feature directions]
    
    D --> H[PM calls Design Reviewer]
    H --> I[Design Reviewer evaluates UX impact]
    I --> J[Design Reviewer provides design direction]
    
    D --> K[PM calls Developer]
    K --> L[Developer estimates implementation cost]
    L --> M[Developer provides time estimates]
    
    G --> N[PM consolidates all opinions]
    J --> N
    M --> N
    
    N --> O[PM forms "team preliminary decision"]
    O --> P[PM calls Challenger]
    P --> Q{Challenger Round 1}
    
    Q --> R1[Challenger questions: feature direction]
    R1 --> S1[Team responds]
    S1 --> T1{Challenger Round 2}
    
    T1 --> R2[Challenger questions: priority]
    R2 --> S2[Team responds]
    S2 --> T2{Challenger Round 3}
    
    T2 --> R3[Challenger questions: goal alignment]
    R3 --> S3[Team final response]
    S3 --> U{Challenger confirms?}
    
    U -- No --> V[Team re-discusses]
    V --> O
    
    U -- Yes --> W[PM writes PENDING_REVIEW.md]
    W --> X[PM updates STATUS.md]
    X --> Y[PM reports to Daniel]
    Y --> Z([End])
```

---

## Three-Round Challenge Process (Detailed)

### Round 1: Feature Direction Challenge
```
Challenger asks:
- Does this feature direction truly align with the product vision?
- Are there other better directions?
- How do competitors do it? Why are we doing it this way?

Team responds:
- Architect supplements technical analysis
- Design supplements UX analysis
- Developer supplements cost analysis
```

### Round 2: Priority Challenge
```
Challenger asks:
- Is the priority of this feature correct?
- Are there more important things to do first?
- Is this the right time to build this feature?

Team responds:
- PM responds based on STATUS.md priorities
- Each role supplements with opinions
```

### Round 3: Goal Alignment Challenge
```
Challenger asks:
- Does this proposal help achieve the project goals?
- Are there contradictions between the roles' opinions?
- Are there any overlooked risks?

Team responds:
- Final confirmation or revision of the proposal
```

---

## PM Tasks (Detailed)

### Step 1: Read Status
```
1. STATUS.md → Confirm this topic is "Discussion"
2. docs/status/issues.md → Understand current issues
3. docs/status/pending_review.md → Understand pending decisions
4. docs/research/competitor_research.md → Understand competitor trends
5. docs/strategy/product_vision.md → Verify product vision alignment
```

### Step 2: Call Sub-agents (Agile Discussion)
```
Call simultaneously (parallel):
- Architect: Analyze technical feasibility, propose feature directions
- Design Reviewer: Evaluate UX impact, provide design direction
- Developer: Estimate implementation cost
```

### Step 3: Consolidate Decision
```
After collecting all sub-agent opinions:
1. PM forms "team preliminary decision"
2. Record differing opinions from each role
3. Prepare to enter the challenge phase
```

### Step 4: Challenge Phase
```
1. Call Challenger, provide "team preliminary decision"
2. Conduct at least 3 rounds of challenges
3. Record challenge content and team responses for each round
4. Cannot proceed until Challenger confirms
```

### Step 5: Write to Files
```
1. New feature suggestions → docs/status/issues.md (tagged source: team discussion)
2. Items requiring Daniel's decision → docs/status/pending_review.md
3. Update STATUS.md
```

---

## Sub-agent Tasks

### Architect 🏗️
1. Read `docs/design/architecture.md`
2. Read `docs/research/competitor_research.md`
3. Propose 2-3 technically feasible feature directions
4. Analyze the technical impact of each direction
5. Respond to Challenger's challenges

### Design Reviewer 🎨
1. Read `docs/design/design_system.md`
2. Evaluate the UX impact of new features
3. Provide design direction suggestions
4. Reference competitor design patterns
5. Respond to Challenger's challenges

### Developer 💻
1. Estimate the implementation cost of each feature direction
2. Provide time estimates
3. Analyze technical risks
4. Respond to Challenger's challenges

### Challenger 🔥
1. **Listen** to all sub-agent opinions
2. **Challenge** the validity of feature directions
3. **Challenge** whether priorities are correct
4. **Challenge** whether they align with product goals
5. Confirm only after at least 3 rounds of challenges

---

## Status Update

PM must update in STATUS.md:

```markdown
## 💡 Discussion Record - YYYY-MM-DD
- **Topic**: [Discussion topic]
- **Architect suggestion**: [Suggestion content]
- **Designer suggestion**: [Suggestion content]
- **Developer estimate**: [Cost estimate]
- **Challenger challenges**: [3-round summary]
- **Final decision**: [Decision content]
- **Pending Daniel's decision**: [Items written to PENDING_REVIEW.md]
```

---

## Step 6: Write Handoff File

After completing the discussion cycle, PM **MUST** write `docs/status/handoff_discuss.md`:

```markdown
# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡)
- **Date**: `YYYY-MM-DD`
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger

## Idea Proposals
| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
|         |             |       |        |

## Decisions Made
- Bullet points of agreed‑upon feature directions, priorities, and design considerations.

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
