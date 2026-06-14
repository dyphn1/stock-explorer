# Challenge Log — C163 (Learn First Gate) + C40 (Beginner/Expert Mode)

**Date**: 2026-06-14  
**Challenger**: Challenger (openrouter/openai/gpt-oss-120b:free)  
**Theme**: Challenge of Team Preliminary Decision — Option A: Unified Beginner Experience System  
**Context**: Sprint 20 — C167 complete (~14h), C163 + C40 pending. Sprint capacity: 30-42h.

---

## Round 1 — Feature Direction Challenge

### Team Proposal
The team recommends **Option A: Unified Beginner Experience System**:
- C163 and C40 share `user_experience_level` session state ("beginner"/"expert")
- C163: Full-page 4-lesson gate replacing C103, soft gate with skip
- C40: Sidebar toggle (Zone B), affects all stock pages with per-page beginner mode specs
- New `experience_service.py` for pure functions
- Total effort: 18-24h + 5-7h prerequisites
- Implementation order: C163 first, then C40

### Challenge

**1. Premise Challenge — Is a shared state really the right abstraction?**

The team assumes C163 (temporal gate — first visit) and C40 (persistent toggle — always available) should share a single `user_experience_level` state. But these serve fundamentally different purposes:
- C163 is about **onboarding** — did the user complete the introductory lessons?
- C40 is about **content complexity** — how much detail should be shown right now?

Conflating these creates a hidden coupling: if a user completes the C163 gate (setting `first_visit_dismissed = True`) but then toggles to expert mode, the system must reconcile two different signals. The Architect's Option A says the gate sets the initial value of `user_experience_level`, but the Designer says the gate uses `first_visit_dismissed` while the toggle uses `user_experience_level`. **These are contradictory session state models.** The Architect's diagram shows 3 levels (beginner/intermediate/expert) but the Designer's spec only uses 2 (新手/進階). Which is it?

**2. Alternatives Challenge — Was Option B dismissed too quickly?**

Option B (Minimal Viable Implementation) was rejected for being "too minimal" and creating "technical debt." But consider:
- Sprint 20 has 16-28h remaining. Option A is 18-24h. That leaves **zero buffer** — any scope discovery pushes into Sprint 21.
- The Architect admits Option A's "broader scope" affects multiple pages: "Each page needs to check `is_beginner_mode()` and conditionally render sections." This is the highest-risk part of the implementation.
- Option B's C40 scope (business card only) could be **expanded incrementally** in Sprint 21, treating beginner mode as a rolling feature. This aligns with the product vision's "Iterative cycle over waterfall" principle.

**Why was incremental expansion rejected in favor of a big-bang 5-page beginner mode?** The team has Sprint 21 already planned (C152 + C170 + D-120). A big-bang approach to C40 in Sprint 20 risks cascading into Sprint 21, displacing C152 (called "non-negotiable" in the Sprint 21 plan).

**3. Risk Challenge — The prerequisite dependency chain is fragile.**

The 5-7h of prerequisites (P1: per-page spec, P2: lesson content) are described as "can be done in parallel." But:
- P1 (per-page beginner mode spec) is a **prerequisite for C40 implementation** — the developer can't implement beginner mode without knowing what to show/hide per page.
- P2 (gateway lesson content) is a **prerequisite for C163** — the developer can't finalize the gate without content.
- Both are assigned to PM/Designer, who are also responsible for C170 glossary content, C152 narrative templates, and C152 historian synthesis boundary document — all flagged as "start NOW" in Sprint 21 planning.

**The PM/Designer has 4 parallel content workstreams during Sprint 20.** What happens if P1 or P2 slips? The developer is blocked, and Sprint 20 overflows.

**4. Consistency Challenge — Architect and Designer disagree on session state granularity.**

- **Architect** (Option A, line 38): `user_experience_level` with values `"beginner" | "intermediate" | "expert"` — three levels.
- **Designer** (C40 spec, line 161): `st.radio` with two options: "🌱 新手模式" / "🔬 進階模式" — two levels.

This is a direct contradiction. Three levels require different UI treatment than two levels. A radio with 3 options is cluttered; a toggle only works for 2. The team must resolve this before implementation.

**5. Scope Challenge — Is Sprint 20 the right sprint for this?**

The product vision's verification principle states: "After each feature implementation, verify: does it genuinely help beginners understand better?" C163 + C40 are the **most user-facing features** in the sprint — they define the first impression of the entire product. Rushing them into a sprint that's already 14h consumed (C167) with no buffer seems risky. The team should consider: **what if C163 + C40 were Sprint 21's primary features instead of C152?** C152 could shift to Sprint 22. This would give the beginner experience the attention it deserves.

---

## Round 2 — Priority Challenge

### Team Response (Synthesized from Architect + Designer documents)

The team would likely respond:
1. **Session state granularity**: The Designer's 2-level radio is the correct target. The Architect's 3-level model was an initial exploration; the Designer refined it to 2 levels based on competitor research (Sharesies uses 3 levels but NerdWallet uses 2, and 2 is simpler for TW users). The shared state should use `"beginner" | "expert"` only.
2. **Option B rejection stands**: Incremental expansion creates an inconsistent experience — beginners would see simplified business card but full complexity on operation checkup. This is worse than no beginner mode at all.
3. **Prerequisites are manageable**: P1 (per-page spec) is 2-3h of content design, not coding. The Designer already produced a detailed per-page spec in the design document (lines 169-219). P1 is effectively **already done**. P2 (lesson content) can use placeholder text for initial implementation.
4. **Sprint 20 is the right time**: C163 + C40 are foundational features that C170 (Tappable Glossary) and C152 (Narrative Explanations) depend on. Delaying them delays the entire beginner experience pipeline.

### Re-Challenge

**1. P1 is NOT "effectively done" — it's a design spec, not a technical spec.**

The Designer's per-page spec (lines 169-219) is a **content design** document. It says things like "Revenue Trend: ✅ Shown" and "Volume Analysis: ❌ Hidden." But it doesn't specify:
- Which Streamlit components map to which sections?
- What's the expander label text in Chinese?
- What's the fallback if a section doesn't have data?
- How does the beginner mode banner interact with existing page headers?

The Architect's P1 says "2-3h (content design, **not coding**). Should be done by PM/Designer **before Sprint 20 coding begins**." But Sprint 20 coding has already begun (C167 is done). **If P1 isn't truly done, the developer will be making content decisions during implementation, which is exactly the inconsistency risk the team is trying to avoid.**

**2. The "C170 depends on C163/C40" argument is backwards.**

The team says C163/C40 must come first because C170 depends on them. But looking at the Sprint 21 plan:
- C170 (Tappable Glossary) uses `_glossary_tooltip()` from `_router_base.py` — it's a **content layer** feature, not dependent on experience level.
- The Architect notes C170 "auto-shows glossary tooltips on first occurrence of financial terms" in beginner mode. But this is an **enhancement**, not a dependency. C170 works fine without C40 — it just shows tooltips for all users.

**The dependency chain is weaker than claimed.** C170 can be implemented independently. C152 doesn't depend on C163/C40 at all. The argument for doing C163/C40 in Sprint 20 first is primarily about user experience sequencing, not technical dependency.

**3. What happens if only C163 is done?**

The team's implementation order is C163 first (8-10h), then C40 (8-10h). If C163 is completed but C40 runs out of sprint budget:
- Users get a 4-lesson onboarding gate → then see the full expert-level complexity on every page.
- The gate teaches P/E and ROE → but the pages show debt analysis, cash flow, institutional flow with no simplification.
- **This is the worst possible outcome**: the gate sets expectations of simplicity, then the product delivers complexity. It's like a "beginner" ski lesson that ends at the top of an expert run.

**The team needs an explicit cut-line rule**: if C40 can't be completed, should C163 also be deferred? Or should C163 ship alone with a "beginner mode coming soon" banner?

**4. Sprint 21 displacement risk is real and underweighted.**

The Sprint 21 plan (from handoff_discuss_r42.md) allocates 38-52h against a 30-42h capacity. It's already **overcommitted by 8-10h** before accounting for any C163/C40 carry-over. The Challenger Condition #4 from Round 41 states: "If either [C163 or C40] carries over, it displaces the lowest-priority Sprint 21 item (C172 stretch first, then C170). C152 is non-negotiable."

But displacing C170 means the glossary content being created in parallel during Sprint 20 is wasted. And C170 is the highest impact/effort feature in Sprint 21. **The team is betting Sprint 20 won't overflow while simultaneously planning a Sprint 21 that's already over capacity.**

**5. The "intermediate" level ghost.**

Even after the team's response narrowing to 2 levels, the Architect's code structure (Option A, line 38) still defines 3 levels. If `experience_service.py` is written with 3-level logic but the UI only exposes 2, that's dead code and confusion. If it's written with 2 levels but the service interface accepts 3, that's a future-proofing trap. **The team must explicitly decide: 2 levels or 3, and document it in the service interface.**

---

## Round 3 — Goal Alignment Challenge

### Final Proposal (Team's refined position after Rounds 1-2)

The team refines Option A with the following clarifications:
1. **Session state**: 2 levels only (`"beginner" | "expert"`). The Architect's 3-level model is dropped. `experience_service.py` uses 2-level logic.
2. **P1 prerequisite**: The Designer's per-page spec (design doc lines 169-219) is sufficient for implementation. No additional technical spec needed. The developer consults the Designer for ambiguities during implementation.
3. **P2 prerequisite**: C163 ships with placeholder content if lesson content isn't ready. Content is updated in Sprint 21.
4. **Cut-line rule**: If C163 is done but C40 is not, C40 carries over to Sprint 21 and displaces C172 (stretch). C170 is NOT displaced. C163 ships alone with a "新手模式即將推出" (Beginner Mode coming soon) banner on stock pages.
5. **Sprint 21 overflow**: The team acknowledges Sprint 21 is overcommitted. If C40 carries over, Sprint 21 becomes: D-120(pre) + C170 + C40(carry) + C152 + C172(stretch). C152 scope reduces to 5 templates (12-15h) to accommodate.

### Confirmation

**✅ ALIGNED — with 3 binding conditions.**

The direction is sound. C163 + C40 as a unified beginner experience system aligns with:
- **Product vision**: "Historian, not a stock picker" — the gate teaches understanding, not action. Beginner mode reduces jargon overload.
- **Design principles**: "Ten-second test" — each gate lesson is one key point. "Progressive drill-down" — beginner mode shows essentials first.
- **Competitor validation**: Webull (learn first), NerdWallet (simple view), Sharesies (complexity levels) all validate the approach.
- **Core values**: "Story first" — gate uses narrative format. "Adaptive" — mode toggle adapts to user preference.

**The 3 binding conditions for alignment:**

1. **Session state must be 2 levels, not 3.** The `experience_service.py` interface must explicitly define only `"beginner" | "expert"`. No `intermediate` value, no 3-level enum, no future-proofing trap. If the team wants 3 levels later, that's a new feature (C122 Adaptive Learning).

2. **C163-alone shipping is acceptable but requires a "coming soon" indicator.** If C40 doesn't fit in Sprint 20, C163 ships with a visible but non-intrusive indicator on stock pages: "🌱 新手模式開發中 — 目前顯示完整內容" (Beginner Mode in development — showing full content). This manages user expectations and avoids the "gate promises simplicity, pages deliver complexity" trap.

3. **Sprint 21 must have a hard cut-line before coding begins.** Before Sprint 21 development starts, the PM must define: if C40 carries over, C152 templates are capped at 5 (not 8), and C172 is dropped entirely. This is non-negotiable — Sprint 21 is already overcommitted without carry-over.

### Remaining Observations (Non-Blocking)

- **C103 removal timing**: The team says C103 is removed "as part of C163 implementation." But if C163 ships without C40, the old C103 is gone and there's no beginner mode. This is acceptable given the "coming soon" indicator, but the team should verify no other code references `first_visit_guide.py` or the "新手導覽" page entry.
- **URL sync compatibility**: The Architect notes the gate is a page (not router interception), so `navigate_to()` handles URL sync. But the gate is the **default landing page** for first-time users. What URL does a first-time user see? If they bookmark the gate, will they see it again on return visit (after `first_visit_dismissed = True`)? The router must redirect away from the gate for returning users.
- **Mobile testing**: The Designer flags mobile responsiveness as P2 risk. The 26-tab navbar is already problematic on mobile. Adding a 4-lesson gate on mobile needs explicit testing. This should be a QA acceptance criterion, not a post-ship fix.

---

## Challenge Summary

| Round | Focus | Key Finding | Resolution |
|-------|-------|-------------|------------|
| 1 | Feature Direction | Session state granularity conflict (2 vs 3 levels); Option B dismissed too quickly; prerequisite dependency chain fragile; Sprint 20 timing questionable | Team clarifies 2 levels; P1 considered done by Designer's spec; Sprint 20 timing accepted |
| 2 | Priority | P1 is design spec not technical spec; dependency chain weaker than claimed; C163-alone is worst outcome; Sprint 21 already overcommitted | Cut-line rule added; C163-alone shipping with "coming soon" banner; Sprint 21 hard cut-line required |
| 3 | Goal Alignment | Direction is sound and aligns with product vision | ✅ ALIGNED with 3 binding conditions |

**Final Verdict**: ✅ **ALIGNED** — Option A is the right direction. The 3 binding conditions (2-level state, C163-alone shipping indicator, Sprint 21 hard cut-line) must be documented as part of the implementation plan before coding begins.

---

*Challenger: Challenger (openrouter/openai/gpt-oss-120b:free)*  
*Date: 2026-06-14*  
*Status: Challenge complete — alignment confirmed with conditions*  
*Next step: PM to document the 3 binding conditions in the Sprint 20 implementation plan*
