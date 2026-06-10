# Stock Explorer Pending Daniel Review

> Items here require human judgment and cannot be auto-resolved by agents.

## 🎨 Design Decisions (Resolved)
- #1 Navbar: ✅ `st.radio(horizontal=True)` — implemented 2026-06-09
- #2 Seasonal Industry List: Deferred — needs Daniel input on industry list
- #3 ETF Classification Severity: Kept P1 — fix after P0 band

## 🔴 Positioning Decision (Resolved)
- #4 Portfolio P&L: ❌ CANCELLED — positioning violation ("historian, not stock picker")

## 📋 Roadmap Approval
- #5 Revised Roadmap (Round 4): Superseded by Round 7 plan below
- #6 business_card.py P0 Regression: ✅ Fixed — restored to 462 lines

## 🔴 Awaiting Daniel's Decision

### 7. C14 Health Score: Scope Decision
- **Option A: Health Score Badge** (5h) — Simple 0-100 score with color coding on business_card.py
- **Option B: Full 5-Axis Radar** (18h) — Profitability/Growth/Financial Health/Dividend/Stability
- **Challenger recommendation**: Option A given C+ design grade
- **Status**: Badge approved for Sprint 4. Radar deferred to post-MVP.

### 8. Revised Roadmap Approval (Round 7)
- **Plan**: 5-sprint roadmap, ~73h base → ~109h with 50% buffer
- **Sprint 0**: Design Quality + Quick wins (2.7h)
- **Sprint 1**: C28 Spike + LLM Architecture (5h)
- **Sprint 2**: D02 Notifications + C31 Daily Company Story (15h)
- **Sprint 3**: C28 Company Story Timeline (20h)
- **Sprint 4**: C07 Custom Thresholds + C14 Health Badge (17h)
- **Sprint 5**: C29 Explain Any Metric (10h)
- **Decision needed**: Approve this roadmap?

### 9. Category Browser + Group Structure Redesign
- Both pages at grade D (lowest). Need structural redesign, not just polish.
- **Recommendation**: Defer to post-MVP, after design system is better enforced.
- **Decision needed**: Include now or defer?

### 10. C31 Content Strategy
- C31 reframed from "Daily Financial Challenge" to "Daily Company Story" (narrative-driven).
- **Options**: A) Manual curation B) Template + FinMind data C) LLM-generated
- **Decision needed**: Which approach, or hybrid?

### 11. NEW-G18: events.yaml Schema Extension
- C28 needs richer event data (related_metrics, price_at_event, narrative_category).
- **Effort**: 2-3h. Must be done before C28 Sprint 3.
- **Decision needed**: Approve schema extension?

### 12. NEW-G19: User Preference/State Storage Abstraction
- C31, C07, D02 all need per-user persistent state. Currently scattered across YAML files.
- **Effort**: 2-3h. Should be done before Sprint 3.
- **Decision needed**: Approve abstraction layer?

### 13. NEW-G20: analogy_engine.py Coverage Gap
- 8 metrics covered, 30+ needed for C29.
- **Effort**: 4-6h. Must be done before C29 Sprint 5.
- **Decision needed**: Approve coverage expansion?

---
*Updated: 2026-06-13 by PM after discussion round 7 + challenger 3-round challenge*
