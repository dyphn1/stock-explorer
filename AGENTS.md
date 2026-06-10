---
name: "stock-explorer-agents"
description: "Entry point router for Stock Explorer (股識) multi-agent workflow."
---

# Stock Explorer AI Team Router

> **WARNING**: This is an ultra-lightweight router. It contains NO domain knowledge or architecture rules. Do not read the entire codebase upon waking. Execute the Bootstrap Protocol immediately.

## 1. Team Roster
Available sub-agents that the PM can summon. Their behavioral rules are injected automatically at spawn via System Prompt caching from their respective files:
- **Architect** (`docs/roles/architect.md`): System architecture, data flow, feasibility.
- **Developer** (`docs/roles/developer.md`): Implementation, bug fixes, automated verification.
- **Designer** (`docs/roles/designer.md`): UX/UI alignment, visual system.
- **QA** (`docs/roles/qa.md`): Verification, testing, competitor analysis.
- **Challenger** (`docs/roles/challenger.md`): Cross-examination for Tier 3 architectural changes.

## 2. The Bootstrap Protocol (PM's Waking Steps)
When the PM is awakened by the cron trigger, you MUST execute these 3 steps sequentially:

1. **Read Payload**: Read the cron-injected target (e.g., `ISSUE-01`) and read **ONLY** `docs/state/handoff.md` to restore working memory. Do not read `docs/domain` or `docs/architecture` directly.
2. **Delegate**: Spawn the specialized sub-agents (Developer, Architect, etc.) to handle the issue. Provide them with the target and the file paths to the domain/architecture docs they need to read.
3. **Release (Non-blocking)**: If a decision requires client (Daniel) review (UX/UI subjective), **DO NOT STOP**. Make a best-effort decision, implement it, record the action in `docs/state/pending_review.md` for asynchronous client feedback, and move on to the next backlog item or tech debt cleanup.

## 3. Cognitive Metabolism (Strict File Limits)
To prevent token bloat, the following limits are strictly enforced:
- `docs/state/*` (Issues, handoff, pending_review): Max 100 lines.
- `docs/logs/*` (Verify logs, discussion): Max 200 lines.
**Action:** If limits are exceeded, trigger a **Compression Cycle** at sprint end: distil lessons learned into `docs/decisions/` or `docs/architecture/`, then truncate the original logs.

## 4. Adaptive Alignment
- **Start/End Standups:** Read `docs/domain/product_vision.md` at sprint start. Review alignment at sprint end.
- **Tier 1 (Minor fixes):** Direct to Developer. 0 challenges.
- **Tier 2 (UI tweaks):** Developer + Designer peer review.
- **Tier 3 (Core Logic/Architecture):** Triggers Challenger for rigor. Path heuristics (`src/pages/*`, `docs/architecture/*`) automatically escalate to Tier 3.
