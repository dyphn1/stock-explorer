# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡) — Sprint 16b Planning
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger

## Idea Proposals
|| Idea ID | Description | Owner | Status ||
||---------|-------------|-------|--------||
|| C28 | Company Story Timeline — compose-and-enrich pipeline merging events + case studies + milestones | Architect | Accepted (MVP: events + case studies) ||
|| C07 | Customizable Event Thresholds — UI for customizing risk/notification sensitivity | Developer | Accepted (partial: settings skeleton in Sprint 16b) ||
|| D5 | LLM Abstraction Layer — protocol-based explanation provider (interface + template fallback) | Developer | Accepted (to unblock C134) ||
|| C134 | AI-Generated Change Explanations | Developer | Deferred (requires D5 LLM layer) ||
|| C02 | Notification System | Developer | Already Done (discovered during analysis) ||
|| C39 | What Changed Recently Delta Card | Developer | Already Done (discovered during analysis) ||

## Decisions Made
- **Sprint 16b Primary**: C28 Full Story Timeline (MVP: events + case studies only, milestones as stretch goal)
- **Sprint 16b Parallel**: C07 Custom Thresholds (settings skeleton, 4h started) + D5 LLM Abstraction Layer (3-4h)
- **Sprint 17**: C07 Custom Thresholds (remaining 8-12h) + C134 Change Explanations (20-26h)
- **Already Complete**: C02 Notifications and C39 What Changed Recently (0h needed)
- **Total Sprint 16b Effort**: 35-51h (revised from 42-56h)
- **Risk Mitigation**: Data seeding (top 10 case studies), empty state handling, basic explanation templates via D5

## Action Items
|| Item ID | Description | Owner | Due Date ||
||---------|-------------|-------|----------||
|| A1 | Implement C28 Story Timeline MVP: compose-and-enrich pipeline (events + case studies) | Developer | Sprint 16b ||
|| A2 | Add horizontal scrollable timeline UI in dedicated "Story" tab | Developer/Designer | Sprint 16b ||
|| A3 | Begin C07 threshold UI skeleton (settings page) | Developer | Sprint 16b (4h) ||
|| A4 | Build D5 LLM Abstraction Layer: ExplanationProvider protocol + TemplateExplanationProvider fallback | Developer | Sprint 16b (3-4h) ||
|| A5 | Seed case studies for top 10 stocks by market cap | Developer | Sprint 16b ||
|| A6 | Implement empty state guidance for sparse timelines | Developer/Designer | Sprint 16b ||
|| A7 | Use D5 to generate basic explanation templates for event types | Developer | Sprint 16b ||
|| A8 | Complete remaining C07 threshold customization UI | Developer | Sprint 17 ||
|| A9 | Implement C134 Change Explanations using LLM abstraction layer | Developer | Sprint 17 ||

## Next Cycle Handoff
Reference `docs/state/handoff_discuss_r35.md` for Sprint 16b planning and execution.