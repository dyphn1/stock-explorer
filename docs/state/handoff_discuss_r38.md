# Handoff – Discussion (Round 38)

## Summary
- **Topic**: Discussion (💡) — Round 38, Sprint 18 Planning
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer (via research), Challenger
- **Sprint**: Sprint 18 (follows Sprint 17 completion: C14 + C134 + C07 + D-101)

---

## 1. Sprint 18 Features Under Discussion

| ID | Feature | Priority | PM Est | Dev Est | Architect Direction |
|----|---------|----------|---------|---------|-------------------|
| C139 | "Explain This Number" One-Click Metric Explainer | P1 | 8-12h | 10-15h | Popover-first, extend `_render_metric_popover()` to 5-7 business card metrics |
| C141 | Confidence/Source Badge on Explanations | P2 | 3-4h | 2-4h (bundled) | `ExplanationResponse.source` already exists; render as `st.caption()` |
| C143 | Implication Sentence on Delta Cards | P2 | 4-6h | 7-10h | Extend `DeltaExplanationProvider`; replace (not supplement) existing explanation on card |

---

## 2. Idea Proposals

| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| C139 | "Explain This Number" — 💡 button → popover with TemplateExplanationProvider | Developer | ✅ Accepted |
| C141 | Source badge (`📊 系統估算` / `📊 FinMind`) on all explanations | Developer | ✅ Accepted (bundled) |
| C143 | "如果你正在觀察這家公司，[factual past-tense]" on delta cards | Developer | ✅ Accepted with prerequisites |
| D-097 | Thread industry context through `ExplanationRequest.context` (prerequisite) | Developer | ✅ Accepted as Sprint 18 first task |

---

## 3. Decisions Made

### Architecture Decision: Popover-First (Direction A)
- Extend existing `_render_metric_popover()` pattern rather than building new infrastructure
- New `src/services/metric_explainer.py` convenience function composing existing `TemplateExplanationProvider` + `metric_education.py`
- Zero new protocol changes required for C139/C141
- C143 adds `implication: str = ""` to `ExplanationResponse` (backward-compatible default)

### Design Decisions
- C139: `st.popover()` with `💡` trigger button, subtle styling (0.8rem, no border, light gray)
- C141: `st.caption()` at 0.7rem gray — no new component, merged into C139/C143 implementation
- C143: Implication sentence REPLACES existing explanation on delta cards (not supplements); existing explanation moves to 💡 popover
- C143: Uses `_白话_card()` with `label="觀察重點"`, analogy field for implication sentence

### Scope Decisions
- C139 scope: **Business card page only** (5-7 metrics), NOT all 15+ metrics across all pages
- C141 scope: Bundled with C139/C143, not a standalone task
- C143 scope: 3 delta metric types (月營收, 股價, 營收年增率) × direction
- Sprint 18 total: **22-31h** (revised from initial 20-28h after Challenger's math correction)

### Execution Order (revised after Challenger Round 2)
1. **D-097 fix** (1-2h) — Thread industry context through `ExplanationRequest.context` to `TemplateExplanationProvider`
2. **C139** (10-14h) — Explain This Number on business card page
3. **C141** (2-3h, bundled) — Source badges added during C139/C143 implementation
4. **Tone QA automation** (2-3h) — `tests/test_tone_qa.py` in CI
5. **C143** (7-9h) — Implication sentences on delta cards

---

## 4. 🔥 Three-Round Challenge (Round 38)

### Round 1: Feature Direction Challenge
**Challenger**: Is C139 building on existing `_render_metric_popover()` or creating something new? The designer claims "15+ metrics with zero explanation UI" but `_render_metric_popover()` already exists for 6 metrics.

**Team Response**: C139 extends the popover pattern to metrics that currently use `_白话_card()` without any popover. The existing `_render_metric_popover()` in `_financial.py` is tightly coupled to that section's specific layout. C139 creates a lighter-weight, reusable `_explain_button()` helper in `_router_base.py` that works across all sections. Specific metrics getting 💡 for Sprint 18: business card _summary.py top-3 metrics, _health.py dimension cards, _story.py delta cards, _moat.py dimension cards (5-7 total).

**Verdict**: ✅ Feature directions confirmed authentic. C139 extends existing pattern; C141/C143 leverage existing infrastructure.

### Round 2: Priority Challenge
**Challenger**: D-097 is scheduled mid-sprint but is a prerequisite for C143. If D-097 is delayed, C143 is blocked. Also, C143 estimate ranges from 4-6h (dev) to 7-13h (team) — which is correct?

**Team Response**: D-097 moved to be FIRST task in sprint. C143 estimate reconciled at 7-10h (includes content creation for implication templates, which dev estimate excluded). Tone QA is a one-time 2-3h CI pipeline addition.

**Verdict**: ✅ Priority order revised to D-097-first. Estimates reconciled. Sprint total revised to 22-31h.

### Round 3: Goal Alignment Challenge
**Challenger**: (a) Sprint math doesn't add up (stated 20-28h vs actual 22-31h). (b) Tone QA blocklist incomplete — misses advisory phrases like "值得關注," "表現優於預期." (c) C143 card design might create overload. (d) C139 scope discrepancy ("5-7 metrics" vs "6-8 locations").

**Team Response**: (a) Revised total: 22-31h acknowledged. (b) Blocklist expanded to: 建議, 應該, 買, 賣, 推薦, 進場, 出場, 值得關注, 需要密切關注, 值得持續追蹤, 表現優於預期. (c) C143 implication sentence REPLACES existing explanation on card (not supplements); existing explanation moves to popover. (d) C139 scope confirmed as 5-7 metrics ALL on business card page.

**Verdict**: ✅ CONFIRMED with 6 binding conditions (see below).

---

## 5. Final Challenger Verdict: ✅ CONFIRMED with 6 Conditions

### Binding Conditions
1. **D-097 must be FIRST task** (not C139) — unblocks both C139 template quality and C143 industry context.
2. **Sprint total is 22-31h** (not 20-28h) — if capped at 28h, reduce C143 or C139 scope.
3. **Tone QA blocklist expanded** to cover advisory phrases. `tests/test_tone_qa.py` must be in CI and passing before C143 merge.
4. **C143 implication sentence REPLACES existing explanation** on delta cards (not supplements). Existing explanation moves to 💡 popover.
5. **C139 scope precisely defined** as a written spec before implementation: exact 5-7 metrics, reuse vs new pattern per metric, metric→template_key mapping.
6. **`ExplanationResponse` protocol change** (`implication: str = ""`) must be architect-reviewed and tested for backward compatibility before implementation.

---

## 6. Action Items

| Item ID | Description | Owner | Due Date | Priority |
|---------|-------------|-------|----------|----------|
| R38-DES1 | Fix D-097: Thread industry context through `ExplanationRequest.context` | Developer | Sprint 18 Day 1 | 🔴 FIRST |
| R38-DEV1 | Create `src/services/metric_explainer.py` with metric→key mapping | Developer | Sprint 18 | 🔴 P1 |
| R38-DEV2 | Create `_explain_button()` helper in `_router_base.py` | Developer | Sprint 18 | 🔴 P1 |
| R38-DEV3 | Wire 💡 buttons to 5-7 business card page metrics | Developer | Sprint 18 | 🔴 P1 |
| R38-DEV4 | Add source badge rendering to all explanation UI | Developer | Sprint 18 | 🟡 P2 (bundled) |
| R38-DEV5 | Extend `ExplanationResponse` with `implication: str = ""` | Developer | Sprint 18 | 🟡 P2 |
| R38-DEV6 | Write implication templates for 3 delta metric types × directions | Developer | Sprint 18 | 🟡 P2 |
| R38-DEV7 | Create `tests/test_tone_qa.py` with expanded blocklist | Developer/QA | Sprint 18 | 🔴 Before C143 merge |
| R38-QA1 | All C143 content must pass tone QA blocklist before merge | QA | Sprint 18 | 🔴 Required |
| R38-ARCH1 | Architect review of `ExplanationResponse` protocol change | Architect | Before C143 dev | 🟡 Required |

---

## 7. Consolidated Team Consensus

All roles agree:
- **Architect**: Direction A (Popover-First) is lowest risk, fastest delivery. Zero new infrastructure.
- **Designer**: C139 (9/10) is highest UX impact. C143 (8/10) is high impact but needs tone gate. C141 (7/10) is trust signal, merge into other tasks.
- **Developer**: 22-31h total with D-097 first. C139: 10-14h, C141: 2-3h bundled, C143: 7-9h, D-097: 1-2h, Tone QA: 2-3h.
- **Challenger**: CONFIRMED with 6 conditions after 3 rigorous rounds.

---

## Next Cycle Handoff
💡 Discussion Round 38 Complete (Sprint 18: C139 + C141 + C143, D-097, Tone QA) → 🔍 Review Round 38 → 🔧 Development Round 39 (Sprint 18 execution)

Reference `docs/design/designer_review_sprint18.md` for full design review.
Reference `docs/state/handoff_discuss_r38.md` for this discussion's complete record.
