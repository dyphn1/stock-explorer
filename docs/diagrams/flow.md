# Stock Explorer — PM Flow Diagrams

> This file contains Mermaid visualizations of all PM workflows.
> AGENTS.md references this file as a visual reference.

---

## Diagram 1: PM Decision Flow After Cron Session Wake-up

```mermaid
flowchart TD
    START([PM awakened by cron]) --> READ_STATE[Step 0: Read state<br/>STATUS.md + handoff.md<br/>current_problems.md + pending_review.md]

    READ_STATE --> CHECK_TODO{Determine current<br/>highest priority task}

    CHECK_TODO -->|P0: Refactor + UX Bug| TODO_REFACTOR[TODO: Refactor/Fix]
    CHECK_TODO -->|P1: New Feature| TODO_FEATURE[TODO: New Feature Development]
    CHECK_TODO -->|P2: Verification/Testing| TODO_VERIFY[TODO: Verification]
    CHECK_TODO -->|P3: Research/Discussion| TODO_RESEARCH[TODO: Competitor Research]
    CHECK_TODO -->|No tasks| SILENT([SILENT end])

    TODO_REFACTOR --> GATE1{ Gate Check 1<br/>Design complete?}
    TODO_FEATURE --> GATE1
    TODO_VERIFY --> GATE2{ Gate Check 2<br/>Implementation complete?}
    TODO_RESEARCH --> GATE3{Gate Check 3<br/>Verification passed?}

    GATE1 -->|NOT PASSED| BACK1[Roll back to previous TODO<br/>Specify improvement requirements]
    BACK1 --> CHECK_TODO
    GATE1 -->|PASSED| NEXT1[Advance to next TODO]
    NEXT1 --> GATE2

    GATE2 -->|NOT PASSED| BACK2[Roll back to TODO 2<br/>Specify key issues]
    BACK2 --> TODO_FEATURE
    GATE2 -->|PASSED| NEXT2[Advance to next TODO]
    NEXT2 --> GATE3

    GATE3 -->|NOT PASSED| BACK3[Roll back to TODO 2]
    BACK3 --> TODO_FEATURE
    GATE3 -->|PASSED| TODO4[TODO 4: Release<br/>PM does it personally]

    TODO4 --> COMMIT[git commit + push<br/>Update state files]
    COMMIT --> END([Session ended])
```

---

## Diagram 2: TODO 1 — Refactor/Bug Fix

```mermaid
flowchart TD
    START([TODO 1 Start]) --> READ[PM reads current_problems.md<br/>Confirm issue scope and files]

    READ --> DELEGATE1[delegate_task → Architect<br/>Feasibility analysis + technical solution<br/>model: nemotron-3]
    READ --> DELEGATE2[delegate_task → Challenger<br/>3-round challenge of plan<br/>model: gpt-oss-120b]

    DELEGATE1 --> GATE1{<br/>Gate 1: Design complete?}
    DELEGATE2 --> GATE1

    GATE1 -->|NOT PASSED<br/>Design incomplete| BACK[Re-dispatch<br/>Specify deficiencies]
    BACK --> READ

    GATE1 -->|PASSED<br/>Design approved| TODO2[Advance to TODO 2<br/>Begin implementation]

    style GATE1 fill:#f9e79f,stroke:#d4ac0d
```

**Participants:** Architect (`nemotron-3`) + Challenger (`gpt-oss-120b`)
**Completion criteria:** Technical analysis/ADR exists + Challenger passes 3 rounds

---

## Diagram 3: TODO 2 — New Feature Development (New Feature / UI)

```mermaid
flowchart TD
    START([TODO 2 Start]) --> READ[PM reads design deliverables<br/>HTML prototype + technical analysis]

    READ --> DELEGATE_UX[delegate_task → UX Designer<br/>Create HTML prototype<br/>model: gemma-4]
    READ --> DELEGATE_ARCH[delegate_task → Architect<br/>Technical feasibility analysis<br/>model: nemotron-3]

    DELEGATE_UX --> GATE1{<br/>Gate 1: Design complete?}
    DELEGATE_ARCH --> GATE1

    GATE1 -->|NOT PASSED| BACK1[Re-dispatch]
    BACK1 --> READ

    GATE1 -->|PASSED| DELEGATE_SEC[delegate_task → Security Architect<br/>Threat modeling + security review<br/>model: nemotron-3]

    DELEGATE_SEC --> GATE2{<br/>Gate 2: Security passed?}

    GATE2 -->|NOT PASSED| BACK2[Roll back to Phase 1<br/>Architect revises]
    BACK2 --> READ

    GATE2 -->|PASSED| DELEGATE_DEV[delegate_task → Developer<br/>Implementation + L0/L1 verification<br/>model: owl-alpha]

    DELEGATE_DEV --> GATE3{<br/>Gate 3: Implementation complete?}

    GATE3 -->|NOT PASSED<br/>L0/L1 failed| BACK3[Roll back to Developer<br/>Specify test failures]
    BACK3 --> DELEGATE_DEV

    GATE3 -->|PASSED| TODO3[Advance to TODO 3<br/>Begin verification]

    style GATE1 fill:#f9e79f,stroke:#d4ac0d
    style GATE2 fill:#f9e79f,stroke:#d4ac0d
    style GATE3 fill:#f9e79f,stroke:#d4ac0d
```

**Participants:** UX Designer (`gemma-4`) + Architect (`nemotron-3`) + Security (`nemotron-3`) + Developer (`owl-alpha`)
**Completion criteria:** HTML prototype exists + Security pass + L0/L1 all pass + git commit

---

## Diagram 4: TODO 3 — Verification (Verify / Test)

```mermaid
flowchart TD
    START([TODO 3 Start]) --> READ[PM confirms implementation complete<br/>git diff --stat + L0 pass]

    READ --> DELEGATE_QA[delegate_task → QA<br/>L0 + L1 + L2 testing<br/>model: gemma-4]
    READ --> DELEGATE_SEC[delegate_task → Security<br/>Code audit<br/>model: nemotron-3]
    READ --> DELEGATE_REVIEW[delegate_task → Design Reviewer<br/>Visual vs prototype<br/>model: gemma-4]

    DELEGATE_QA --> GATE{<br/>Gate: All passed?}
    DELEGATE_SEC --> GATE
    DELEGATE_REVIEW --> GATE

    GATE -->|NOT PASSED<br/>P0 issues| BACK[Roll back to TODO 2<br/>Specify fix priorities]
    BACK --> START

    GATE -->|PASSED<br/>All pass| TODO4[Advance to TODO 4<br/>Release]

    style GATE fill:#f9e79f,stroke:#d4ac0d
```

**Participants:** QA (`gemma-4`) + Security (`nemotron-3`) + Design Reviewer (`gemma-4`)
**Completion criteria:** L0 + L1 + L2 all pass + no security critical issues + no P0 visual deviations

---

## Diagram 5: TODO 4 — Release (PM Does It Personally)

```mermaid
flowchart TD
    START([TODO 4 Start]) --> PM1[Update docs/state/handoff.md<br/>Session summary]
    PM1 --> PM2[Update docs/state/current_problems.md<br/>Mark resolved]
    PM2 --> PM3[Update docs/state/pending_review.md<br/>Clear reviewed items]
    PM3 --> PM4[Update docs/overview/05-roadmap.md<br/>Mark features complete]
    PM4 --> PM5[git add -A<br/>git commit -m "type: summary"<br/>git push]
    PM5 --> END([✅ Task complete])

    style PM5 fill:#d5f5e3,stroke:#27ae60
```

**Only PM does this personally, no sub-agents.**

---

## Diagram 6: Research/Discussion (Research / Discuss)

```mermaid
flowchart TD
    START([Research/Discussion Start]) --> READ[PM defines research scope<br/>Competitor analysis or next steps]

    READ --> DELEGATE_QA[delegate_task → QA<br/>Competitor research<br/>model: gemma-4]
    READ --> DELEGATE_ARCH[delegate_task → Architect<br/>Feasibility assessment<br/>model: nemotron-3]
    READ --> DELEGATE_UX[delegate_task → UX Designer<br/>UX recommendations<br/>model: gemma-4]

    DELEGATE_QA --> GATE1{<br/>Gate 1: Research complete?}
    DELEGATE_ARCH --> GATE1
    DELEGATE_UX --> GATE1

    GATE1 -->|NOT PASSED| BACK[Re-dispatch]
    BACK --> READ

    GATE1 -->|PASSED| SYNTHESIZE[PM synthesizes results<br/>→ Draft]

    SYNTHESIZE --> DELEGATE_CHAL[delegate_task → Challenger<br/>3-round challenge<br/>model: gpt-oss-120b]

    DELEGATE_CHAL --> GATE2{<br/>Gate 2: Challenge passed?}

    GATE2 -->|NOT PASSED| REVISE[Revise draft]
    REVISE --> SYNTHESIZE

    GATE2 -->|PASSED| DOC[PM writes ADR<br/>Updates roadmap<br/>Creates handoff]
    DOC --> COMMIT[git commit + push]
    COMMIT --> END([✅ Complete])

    style GATE1 fill:#f9e79f,stroke:#d4ac0d
    style GATE2 fill:#f9e79f,stroke:#d4ac0d
```

---

## Diagram 7: Optimization (Design Review Fixes)

```mermaid
flowchart TD
    START([Optimization task start]) --> READ[PM reads design review report<br/>Lists items to fix]

    READ --> CLASSIFY{Issue classification}

    CLASSIFY -->|Color/Component violations| DELEGATE_DEV[delegate_task → Developer<br/>Fix to design system colors<br/>model: owl-alpha]
    CLASSIFY -->|Layout/Responsive| DELEGATE_UX[delegate_task → UX Designer<br/>Update prototype<br/>model: gemma-4]
    CLASSIFY -->|Interaction/Flow| DELEGATE_UX

    DELEGATE_DEV --> GATE{<br/>Gate: Fix complete?}
    DELEGATE_UX --> GATE

    GATE -->|NOT PASSED| BACK[Re-do]
    BACK --> READ

    GATE -->|PASSED| VERIFY[PM runs L0 verification<br/>Confirm no regression]
    VERIFY --> COMMIT[git commit + push]
    COMMIT --> END([✅ Complete])

    style GATE fill:#f9e79f,stroke:#d4ac0d
```

---

## Role and Model Reference Table

| Role | Model | Primary TODO Participation |
|------|-------|---------------------------|
| **PM** | `openrouter/owl-alpha` | TODO 4 (personal) + all Gate Checks |
| **Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | TODO 1, 2, 6 |
| **Security Architect** | `openrouter/nvidia/nemotron-3-super-120b-a12b:free` | TODO 2, 3 |
| **UX Designer** | `openrouter/google/gemma-4-31b-it:free` | TODO 2, 6, 7 |
| **Developer** | `openrouter/owl-alpha` | TODO 1, 2, 7 |
| **Design Reviewer** | `openrouter/google/gemma-4-31b-it:free` | TODO 3 |
| **QA** | `openrouter/google/gemma-4-31b-it:free` | TODO 3, 6 |
| **Challenger** | `openrouter/openai/gpt-oss-120b:free` | TODO 1, 6 |
