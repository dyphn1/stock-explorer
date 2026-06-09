# Challenge Log

Record each important decision that goes through the Challenger review process.

## Format

```markdown
## [Date] Theme: [development/discussion/review]

### Round 1
- Plan:
- Challenge:
- Response:

### Round 2
- Revision:
- Challenge:
- Response:

### Round 3
```

---

## [2026-06-09] Theme: Discussion — Feature Roadmap Planning

### Round 1
- **Plan:** Implement 3 P0 features from competitor research in order C01 → C03 → C02
- **Challenge:** C05 violates "historian" positioning; roadmap is competitor-driven not vision-driven; C02 under-prioritized
- **Response:** Downgraded C02 design spike to P1; C03 downgraded to P1

### Round 2
- **Revision:** C02 design spike first, then C03, then C02 implementation
- **Challenge:** C07 is advanced feature not beginner need; C02 should be Phase 1; C06 strategically misranked
- **Response:** C06 moved to Phase 1 as quick win leveraging existing PPT-style CSS

### Round 3
- **Revision:** Phase 1 = C06 + C07, Phase 2 = C02 + C04, Phase 3 = C05 (conditional)
- **Challenge:** Roadmap doesn't advance educational mission; M5 unverified; uv.lock marked done but missing
- **Response:** Added D01 (M5 verification) and D02 (background worker investigation) as prerequisites; C05 made conditional on Daniel's approval

---

## [2026-06-10] Theme: Review — Tech Debt + Design + Cost Estimation

> **Context:** Architect found 13 remaining tech debt items (3 new), Design Reviewer found 26 design issues across 7 categories, Developer estimated 103.4h across 35 items. The Challenger must stress-test all findings against product vision.

### Round 1: Gap Authenticity Challenge

#### Q1: Are the 26 design issues REAL problems or nitpicks? Which actually affect users?

**Challenger's Analysis:**

Of the 26 design issues (DR-01 through DR-08 in the new review), I categorize them by actual user impact:

**REAL problems that hurt beginners (user-facing):**
- **DR-03 (Financial Health text-heavy, C+ grade)** — This is the worst-graded page. The product vision says "PPT-style: one key point per page, image-first" and "charts must occupy >60% of page area." Financial Health has 4 text-heavy sections with only 1 chart. A beginner landing here will see a wall of text — this directly violates the 10-second test. **Verdict: REAL, HIGH impact.**
- **DR-05 (Responsive column layouts break)** — Beginners use phones. If the 6-column layout overflows on a 375px screen, users see broken UI. **Verdict: REAL for mobile users.** However, from STATUS.md it looks like P2-2 responsive work was marked complete — the DR says it's only partially fixed. **Verdict: REAL but scope needs reduction (focus on most-broken pages only).**
- **DR-01 (Color violations in 6 files)** — 10+ instances of non-standard colors. This is a brand consistency issue. For a beginner, inconsistent colors create cognitive load and erode trust. **Verdict: REAL but LOW urgency — fix during normal maintenance cycles.**

**Nitpicks (developer-facing, low user impact):**
- **DR-02 (st.cache_data in View layer)** — This is an architecture purity issue. The code works. Moving caching to the data layer doesn't change what users see. **Verdict: NITPICK. The 30-minute fix is fine but should never be prioritized over user-facing work.**
- **DR-04 (Component inconsistency)** — 4 pages use inline HTML instead of shared `_白话_card()`. Users see cards that look slightly different but still work. **Verdict: NITPICK for now. Should be addressed during the natural evolution of pages, not as a dedicated 2-hour task.**
- **DR-07 (Text alternatives on severity badges)** — WCAG 1.4.1 compliance. Important for accessibility, but this is a Taiwanese beginner stock app, not a government portal. **Verdict: REAL but LOW priority. Fix when touching event_dashboard.py for other reasons.**
- **DR-08 (Chart color standardization)** — `#4A90D9` vs `#3498DB` — users barely notice. **Verdict: NITPICK.**

**Missed issue — the DR didn't mention loading performance adequately:**
- The cost estimation says category browser takes 30-60 seconds on cold cache (HIGH-C01 from tech_debt.md). This is a **P0 user-facing problem**. The DR graded category_browser as "B" but didn't flag the 30-60s load time as a design issue. A beginner waiting 60 seconds for a page that shows a spinner will bounce.

#### Q2: Is the tech debt prioritization correct? Should any P2 items be P0?

**Cross-referencing the Architect's findings with the product vision:**

1. **TD-B01 FinMindRateLimitError silently swallowed (P1, 15min)** — This should be **P0**. Here's why: the product vision says "All data must cite its source to avoid a black-box feel" and "Under no circumstances should Streamlit throw an uncaught exception." When a rate limit error is silently swallowed, the user sees "Data temporarily unavailable" with no explanation. This is a black-box experience. **Upgrade to P0.**

2. **TD-E01 No tests for event detection algorithms (P0, 3h)** — Correctly prioritized as P0. The architect recommends this and I agree — but I'd add that these tests are **prerequisites for every feature that builds on M5** (C02, C07, C04). Without tested foundations, the team is building on sand.

3. **TD-C01 Category browser N+1 (High in tech debt, but NOT in the new design issues)** — The architect flagged this as HIGH priority (30-60s load time). It's missing from the design review entirely. **This should be a P1 item somewhere.**

4. **TD-D01 YAML storage doesn't scale (Medium in tech debt, 4h)** — Currently irrelevant. This is a single-user app. Revisit when multi-user deployment is planned.

5. **TD-C03 ETF dividend ranking (Medium in tech debt, 1.5h)** — 500 sequential calls. This is a real user-facing performance issue but the fix (7-day TTL cache) is straightforward. **Keep at Medium priority.**

**Verdict:** The P2→P0 promotion I'd push is **TD-B01 (rate limit visibility)**. The silently-swallowed error is the single biggest "black box" experience in the app.

#### Q3: Are there things "competitors don't have but we should" that the team missed?

The DR's competitor analysis identified good patterns (card consistency, empty states, loading states). But I see **two strategic gaps**:

1. **No mention of "Story Threads" or "Company Timeline Narratives"** — The product vision says "Story first, data second" and "Lack of narrative: Piles of data without context." The event dashboard (A- grade) is the closest thing, but it's a disconnected list. What's missing is a **narrative timeline** — "Here's what happened to TSMC in the last 3 years, told as a story." This is the #1 thing competitors DON'T have and aligns perfectly with the "historian" positioning. The team has all the data (events, revenue, price) but no narrative thread connecting them.

2. **No mention of "Beginner Glossary" or "Term Tooltip System"** — The design system says "All professional terms must have plain-language translations." But there's no systematic glossary or tooltip system. Beginners encounter terms like "ROE," "P/B ratio," "institutional investors" and have no inline help. This is a unique educational feature that no competitor has done well.

**Neither of these should be added to the current roadmap** — they're future ideas. But the team should be aware that the current roadmap doesn't advance the "story first" core value at all.

#### Q4: Is the 103.4h estimate realistic? What's missing?

**The estimate is optimistic.** Here's what's missing:

1. **No time for Daniel's manual UI verification** — STATUS.md repeatedly says "需要 Daniel 手動啟動 Streamlit 進行 UI驗證." The cost estimation explicitly excludes "extensive QA cycles" but Daniel's manual verification is a hard gate for every visual change. At minimum, add 1-2 hours per design change for Daniel's review cycle.

2. **No time for the "unknown unknowns" of Streamlit** — Streamlit has quirks: `st.cache_data` invalidation, session_state race conditions, widget key collisions. The team has already hit several of these (P0-1 through P0-4 in STATUS.md). Budget 10% contingency for Streamlit-specific debugging.

3. **No time for documentation updates** — The design system, product vision, and architecture docs need updating after every significant change. Budget 30 minutes per feature.

4. **The 72h for new features is underestimated** — NF-C06 (PPT, 20h) and NF-C02 (Notifications, 16h) are both high-risk, high-complexity items. The developer's own confidence interval is ±40% for new features. Realistic range: 72h × 1.4 = **~100h for new features**.

5. **Missing item: C03 Multi-Watchlist status discrepancy** — STATUS.md shows C03 as completed (line 499: "多清單關注系統實作完成"), but issues.md shows it as 📋 Todo. This needs to be reconciled. If it's actually done, that's 3-4h saved. If it's not done, the estimate is missing it.

**Revised estimate: 103.4h → ~130h with realistic buffers (not the 124h with 20% buffer the developer calculated).**

---

### Round 2: Priority Challenge

#### Q1: Should the team focus on design polish (26 issues, 8.3h) or new features (72h)?

**Neither. The team should focus on FOUNDATION first.**

Here's the problem: the current roadmap (Phase 1 = C06 + C07) assumes the M5 event detection works. The architect found **zero tests for event detection algorithms** (TD-E01). The STATUS.md shows M5 as "代碼完成" (code complete) but NOT verified with real FinMind data.

**The risk:** If the team builds C07 (Custom Thresholds) on top of unverified event detection, they may discover mid-implementation that the detection logic has bugs. This would waste 12+ hours of C07 work.

**My recommendation:**
1. **Week 1: Foundation** — D01 (M5 verification, 4h) + TD-E01 (event detection tests, 3h) + Immediate tech debt (1.3h) = **~8 hours**
2. **Week 2: Quick design wins** — DR-03 (Financial Health text reduction, 1.5h) + DR-01 (color violations, 1h) + DR-02 (cache_data in view, 0.5h) = **~3 hours**
3. **Week 3+: Features** — Now build C06, C07, C02, C04 on verified foundations

**The 8.3h of design polish should NOT be done as a separate sprint.** Instead:
- DR-03 (Financial Health) should be done before C06 (PPT Generation), because PPT generation will capture whatever's on the page. If Financial Health is text-heavy, the PPT will be text-heavy too.
- DR-01 (colors) and DR-08 (chart colors) can be batched with any feature work that touches the same files.
- DR-04, DR-05, DR-06, DR-07 are all "nice to have" and should be deferred.

#### Q2: Is the roadmap still correct given the new findings?

**The roadmap needs three adjustments:**

1. **D01 (M5 verification) must be a hard blocker for C07, not just a prerequisite in name.** The current roadmap lists D01 as a prerequisite but doesn't enforce it. Add an explicit gate: "C07 cannot start until D01 produces a verification report showing detection accuracy >80% on 10+ stocks."

2. **C06 (PPT Generation) should be moved AFTER DR-03 (Financial Health text reduction).** The PPT captures page content. If the worst-graded page (Financial Health, C+) is included in the PPT, it will undermine the "PPT-style" brand promise. Fix the page first, then generate the PPT.

3. **DR-03 should be promoted to P0.** Here's why: Financial Health is one of the "Four Deep-Dive Sections" (Layer 2 of the product architecture). It's a core page, not an auxiliary feature. It's graded C+ — the worst of all pages. And it directly violates the product vision's "PPT-style" and "10-second test" requirements. **A beginner's experience of the Financial Health page is a referendum on the entire product.**

#### Q3: Should DR-03 (Financial Health text) be P0 since it's the worst-graded page?

**Yes. Absolutely.** Here's the argument:

1. **Product vision alignment:** The vision says "PPT-style: one key point per page, image-first" and "charts must occupy >60% of page area." Financial Health has 4 sections, mostly text, 1 chart. It's the anti-vision page.

2. **User journey impact:** Financial Health is one of the 4 core deep-dive sections (Layer 2). A beginner who navigates here expects the same quality as the Business Card (B+) or Event Dashboard (A-). Getting a C+ page feels broken by comparison.

3. **Downstream impact on C06:** If PPT generation includes the current Financial Health page, the PPT will have a text-heavy slide that undermines the "PPT-style" brand. Fix the page first.

4. **Cost is low:** 1.5 hours. This is the highest-ROI fix in the entire backlog.

**Recommendation: Promote DR-03 to P0. Do it before C06.**

#### Q4: Is C06 (PPT Generation, 20h) really Phase 1 material or should it wait?

**C06 should wait. Here's why:**

The product vision says "PPT-style presentation" — this refers to the IN-APP presentation, not PPT file generation. The core value is "Help beginners understand companies through visual, plain-language analysis." C06 is a delivery mechanism (export to PPT), not an understanding mechanism.

**Arguments for delaying C06:**
- 20h is the single largest feature cost
- It depends on DI-04 (card standardization, 2h) which isn't done
- It captures page content as-is — if pages are broken, PPT is broken
- No competitor has this as a core feature (玩股網 has basic report generation, not PPT)
- It doesn't advance any of the 5 core values in the product vision

**Arguments for keeping C06 in Phase 1:**
- It's a unique differentiator (no competitor has PPT export)
- It drives organic sharing (users share PPTs → new users)
- It leverages existing PPT-style CSS (low incremental cost)

**My verdict: Move C06 to Phase 2 or 3.** Phase 1 should focus on making the core pages excellent (fix DR-03, verify M5). Phase 2 can add C06 as a "share what you've learned" feature. The 20h is better spent on C02 (Notifications, 16h) which is a P0 gap that all competitors have.

#### Q5: The team found that `uv.lock` was marked done but doesn't exist — are there other "done" items that are actually incomplete?

**Critical finding: `uv.lock` now EXISTS on disk.** The file search confirmed `/Users/daniel.chang/Desktop/GitHub/stock-explorer/uv.lock` exists. The architect's report was written before this was committed. This is a false alarm.

**However, the broader concern is valid. Let me cross-reference STATUS.md claims vs issues.md:**

1. **C03 Multi-Watchlist** — STATUS.md line 499 says "多清單關注系統實作完成 (ISSUE-C03)" ✅ Done. But issues.md line 64 shows C03 as 📋 Todo. **This is a real discrepancy.** The STATUS was updated but issues.md was not. **Action needed: Update issues.md to mark C03 as Done.**

2. **M5 Event Detection** — STATUS.md says "✅ 代碼完成" (code complete). The architect's D01 item says "code-complete but unvalidated in production." **This is accurate — code complete ≠ verified.** The team correctly identified this gap.

3. **D03 Event Retention Policy** — issues.md line 269 shows D03 as ✅ Done. But the architect's review doesn't mention it. **This appears to be genuinely done** (prune_old_events function exists).

4. **TD items marked "Done" in tech_debt.md** — The architect verified 9 items as resolved. I spot-checked a few:
   - Card helpers: The DR found DR-04 (inline HTML cards in 4 pages) still exists. The architect said "all pages import `_section_title`, `_白话_card`, `_info_card` from `_router_base.py`" but the DR found 4 pages still using inline HTML. **This is a partial resolution** — the shared components exist but not all pages use them. The architect's "Done" claim is about the consolidation being available, not about all pages being migrated. **This is technically correct but misleading.**

**Verdict:** The main discrepancy is C03 (done in STATUS, todo in issues.md). The TD "Done" items are technically correct (the underlying issues were resolved) but some pages haven't adopted the shared components yet.

---

### Round 3: Goal Alignment Challenge

#### Q1: Does fixing 26 design issues advance the product vision? Or is it perfectionism?

**It depends on WHICH issues you fix.**

The product vision has 5 core values:
1. Story first, data second
2. PPT-style presentation
3. Adaptive and self-evolving
4. Point-to-point knowledge construction
5. Benchmark-oriented analysis

**Issues that DIRECTLY advance the vision:**
- DR-03 (Financial Health text-heavy) → Advances value #2 (PPT-style)
- DR-01 (Color violations) → Supports value #2 (consistent visual language)
- DR-05 (Responsive layouts) → Supports value #1 (accessible to all beginners)

**Issues that are NEUTRAL to the vision:**
- DR-02 (st.cache_data in View) — architecture purity, no user impact
- DR-04 (Component inconsistency) — maintainability, indirect user impact
- DR-06 (Responsive layouts for narrow screens) — important but low usage (most beginners on desktop)
- DR-07 (Accessibility badges) — important but not vision-critical
- DR-08 (Chart colors) — nitpick

**The team should fix DR-03 and batch DR-01 with other work. Everything else is perfectionism at this stage.**

#### Q2: Is the team spending too much time on infrastructure vs user-facing value?

**Yes, the cost estimation has too much infrastructure.**

Looking at the 103.4h breakdown:
- **Infrastructure (no direct user value):** TD-07 (max_workers config, 0.3h) + TD-10 (data consolidation, 2h) + TD-11 (type checking, 2h) + TD-12 (storage abstraction, 4h) + TD-13 (rate limit global state, 1h) + TD-14 (integration tests, 3h) + TD-15 (pagination, 1h) + TD-16 (last known good, 2h) = **15.3h of infrastructure**
- **User-facing value:** Everything else = **88.1h**

That's 15% of the total budget on infrastructure. For a single-user educational app that's about to validate its core features, this is too much.

**Specific pushback:**
- **TD-11 (type checking, 2h):** The app is 5,300 lines of Python. Adding mypy configuration and fixing type errors across the codebase is a significant time investment for a Streamlit app where most type complexity comes from untyped dicts. **Defer to post-MVP.**
- **TD-12 (storage abstraction, 4h):** The app is single-user. YAML works. SQLite is premature. **Defer to when multi-user deployment is planned.**
- **TD-15 (pagination, 1h):** The category browser already has a progress bar. Pagination is nice but not blocking. **Defer.**

**Recommendation: Cut 7.3h of infrastructure (TD-11, TD-12, TD-15) from the current plan. Reallocate to user-facing features or reduce total estimate to ~96h.**

#### Q3: The "historian not stock picker" positioning — does any proposed feature violate this?

**Two features raise concerns:**

1. **C05 (Portfolio P&L Management)** — Already flagged in the previous discussion round. The challenger's report says it's a positioning violation. I agree. **Even if reframed as "Paper Portfolio for Learning," the moment you show P&L numbers, users will treat it as a portfolio tracker.** The team should either:
   - Drop C05 entirely
   - Reframe as "Watchlist 2.0" — add notes, tags, custom categories (no P&L)

2. **C04 (Market Thermometer)** — This is borderline. A "market temperature" indicator could be interpreted as "is now a good time to buy?" which is a buy/sell signal. **The implementation must be carefully scoped:**
   - ✅ OK: "The market is hot/cold based on trading volume and institutional activity" — this is historical fact
   - ❌ NOT OK: "Now is a good time to buy/sell" — this is a recommendation
   - The current design (🔥 Hot / 😊 Normal / 🥶 Cold) is fine as long as the plain-language explanation stays factual

**C02 (Notifications), C06 (PPT), C07 (Custom Thresholds)** — all aligned with "historian" positioning. They tell users "something happened" not "what to do about it."

#### Q4: What should the team do FIRST in the next sprint? What's the single most impactful thing?

**The single most impactful thing: Verify M5 event detection with real FinMind data (D01, 4h).**

Here's why:

1. **M5 is the foundation for 3 features** (C02, C07, C04). If M5 is broken, all three are wasted effort.
2. **It's the cheapest risk reduction** — 4 hours now potentially saves 42+ hours of building on broken foundations.
3. **It's the only P0 item that's truly a blocker** — everything else can proceed in parallel.
4. **It validates the "adaptive and self-evolving" core value** — the product vision's value #3.

**The next sprint should be:**

| Order | Item | Hours | Why |
|-------|------|-------|-----|
| 1 | D01: M5 Verification | 4h | Unblocks C02, C07, C04 |
| 2 | TD-E01: Event Detection Tests | 3h | Prevents regressions in M5 |
| 3 | TD-B01: Rate Limit Visibility | 0.25h | Biggest "black box" UX issue |
| 4 | DR-03: Financial Health Text Reduction | 1.5h | Worst-graded page, unblocks C06 |
| 5 | TD-01: Commit uv.lock | 0.1h | Reproducibility (already done!) |
| 6 | TD-02: Extract timeline constants | 0.2h | DRY cleanup |
| 7 | TD-03: Add logging to _fetch() | 0.2h | Debuggability |
| 8 | TD-05: Fix st.session_state in tests | 0.5h | Test reliability |
| **Total** | | **~10h** | |

**After this sprint, the team will have:**
- Verified M5 event detection (foundation for 3 features)
- Fixed the worst-designed page (Financial Health)
- Cleaned up all immediate tech debt
- A solid foundation for Phase 1 features (C06, C07)

---

## Challenger's Verdict

### Confirmed Findings

I confirm the following findings from the team's reviews:

1. **Tech debt count (13 remaining)** — Accurate. The architect's verification against source code is thorough.
2. **Design grades (B- overall)** — Fair assessment. The A- for Event Dashboard and C+ for Financial Health are accurate based on the design system criteria.
3. **Cost estimation (103.4h)** — Directionally correct but optimistic. Realistic range: 96-130h depending on which infrastructure items are deferred.
4. **3 new tech debt items** — All valid. TD-E01 (no event detection tests) is the most critical.
5. **uv.lock** — Now exists on disk. The architect's report was written before the file was committed. **False alarm.**

### Findings That Need Adjustment

1. **DR-03 (Financial Health) should be P0, not P1** — It's the worst-graded core page and directly violates the product vision's PPT-style requirement.
2. **TD-B01 (Rate Limit Visibility) should be P0, not P1** — Silently swallowing errors contradicts the "no black box" vision.
3. **C06 (PPT Generation) should be Phase 2 or 3, not Phase 1** — It's a delivery mechanism, not an understanding mechanism. Fix pages first, then export.
4. **C03 (Multi-Watchlist) status discrepancy** — STATUS.md says done, issues.md says todo. Needs reconciliation.
5. **Infrastructure items (TD-11, TD-12, TD-15) should be deferred** — 7.3h of infrastructure work is premature for a single-user app.
6. **Category browser performance (30-60s load) is missing from design review** — This is a P1 user-facing issue that the DR overlooked.

### What Needs to Change

1. **Promote DR-03 and TD-B01 to P0**
2. **Move C06 from Phase 1 to Phase 2 or 3**
3. **Add a hard gate: C07 cannot start until D01 is complete**
4. **Reconcile C03 status between STATUS.md and issues.md**
5. **Defer TD-11 (type checking), TD-12 (storage abstraction), TD-15 (pagination) to post-MVP**
6. **Batch DR-01 (color fixes) with feature work instead of doing it as a separate task**
7. **Add category browser performance optimization to the roadmap** (currently in tech debt but not in design issues or cost estimation's recommended execution order)

---

## Recommended Adjustments

### Revised Priority List

| Priority | Item | Hours | Category |
|----------|------|-------|----------|
| **P0** | D01: M5 Event Detection Verification | 4h | Foundation |
| **P0** | TD-E01: Event Detection Tests | 3h | Quality |
| **P0** | DR-03: Financial Health Text Reduction | 1.5h | Design |
| **P0** | TD-B01: Rate Limit Visibility | 0.25h | UX |
| **P0** | TD-01: Commit uv.lock | 0.1h | Reproducibility (done) |
| **P0** | TD-02: Extract timeline constants | 0.2h | DRY |
| **P0** | TD-03: Add logging to _fetch() | 0.2h | Debuggability |
| **P0** | TD-05: Fix st.session_state in tests | 0.5h | Test reliability |
| **P1** | C07: Customizable Event Thresholds | 12h | Feature (after D01) |
| **P1** | C02: Notification System (Email) | 16h | Feature (after D02) |
| **P1** | DR-01: Color System Violations | 1h | Design |
| **P1** | DR-02: st.cache_data in View | 0.5h | Architecture |
| **P1** | TD-06: Event Detection Tests (expanded) | 3h | Quality |
| **P1** | TD-08: Category Browser Optimization | 2h | Performance |
| **P1** | TD-09: ETF Dividend Cache | 1.5h | Performance |
| **P1** | TD-04: Rate Limit Visibility | 0.25h | UX |
| **P2** | C06: PPT Generation | 20h | Feature (after DR-03) |
| **P2** | C04: Market Thermometer | 14h | Feature |
| **P2** | D02: Background Worker Investigation | 6h | Foundation |
| **P2** | DR-04 through DR-08 | 5.3h | Design polish |
| **P2** | TD-07, TD-10, TD-13, TD-14, TD-16 | 12h | Infrastructure |
| **Defer** | TD-11, TD-12, TD-15 | 7h | Post-MVP |

### Revised Roadmap

**Sprint 1 — Foundation (Week 1, ~10h):**
- D01: M5 Verification (4h)
- TD-E01: Event Detection Tests (3h)
- DR-03: Financial Health Text Reduction (1.5h)
- All immediate tech debt (1.3h, mostly already done)

**Sprint 2 — Feature Foundation (Week 2, ~15h):**
- C07: Customizable Event Thresholds (12h) — starts after D01 gate passes
- D02: Background Worker Investigation (6h) — can parallelize with C07
- TD-08: Category Browser Optimization (2h)

**Sprint 3 — Core Features (Weeks 3-4, ~30h):**
- C02: Notification System Email (16h) — starts after D02
- C04: Market Thermometer (14h)

**Sprint 4 — Polish + Shareability (Weeks 5-6, ~25h):**
- C06: PPT Generation (20h) — starts after DR-03 is done
- DR-01 + DR-08: Color standardization (2h)
- DR-02: st.cache_data in View (0.5h)
- DR-04 through DR-07: Remaining design polish (2.5h)

**Post-MVP (when needed):**
- TD-11: Type checking
- TD-12: Storage abstraction
- TD-15: Pagination
- TD-16: Last known good fallback

### Key Metrics to Track

1. **M5 detection accuracy** — target >80% on 10+ stocks (from product vision M5 milestone)
2. **Financial Health page grade** — target B+ or better after DR-03 fix
3. **Category browser load time** — target <10s after TD-08
4. **Test coverage** — target all pure functions in adaptive_engine.py tested
5. **Design system compliance** — target all pages B+ or better

---

*This challenge report was produced by the Challenger subagent on 2026-06-10 as part of the review round (Architect + Design Reviewer + Developer + Challenger).*
