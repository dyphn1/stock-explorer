# Challenge Log

> **Compressed**: Rounds 1-12 distilled. Rounds 13-14 full. Max 200 lines enforced.

## Distilled Lessons from Rounds 1-12
- **Positioning**: Every feature must pass "historian, not stock picker" test
- **Priority**: Architecture debt (D16, D24) consistently blocks features — must be proactive
- **Pattern**: Tier 3 changes (core logic/arch) require Challenger; Tier 1 (minor fixes) can fast-track
- **Key resolved**: C48 replaces C37 (not alongside); C44 scoped to 3 historical risk dimensions; C68 replaces C49
- **Recurring theme**: Competitor features must be filtered through historian positioning, not copied directly

---

## Round 13: Final Confirmation (2026-06-19)
**Theme**: Sprint 3 completion + Sprint 4 preparation

### Round 1 (Gap Authenticity)
- 6 features from Round 13 competitor research validated by multiple competitors
- C65 (Company Filing Explorer) confirmed unique TW market opportunity

### Round 2 (Priority)
- C66 elevated to higher priority due to competitor consensus
- D-038 IA decision elevated to Sprint 4

### Round 3 (Goal Alignment)
- D24 must precede C44; tone guidelines needed before C51

**✅ CONFIRMED** with 4 conditions: C68 replaces C49, C67 deferred, D-032 Sprint 4, D-038 IA Sprint 4

---

## Round 15: Final Confirmation (2026-06-19)
**Theme**: Review Round 15 — New features + Architecture + Design

### Round 1 (Gap Authenticity): ❌ REVISED
- 5 of 6 new features REJECTED (C76, C77, C78, C80 positioning conflict; C75 deferred)
- C79 consolidated into C74 (saves ~6-9h)
- D37 downgraded to monitor (_sections.py is coherent, unlike analogy_engine.py)
- D-039, D-040, D-041 confirmed as legitimate Sprint 5 prerequisites

### Round 2 (Priority): ⚠️ REVISED
- D16 hard deadline: first 25% of Sprint 4
- D-041/D-040/D-039 are Sprint 5 prerequisites (not parallel work)
- D23 added to Sprint 4 parallel content work

### Round 3 (Goal Alignment): ✅ CONFIRMED with conditions
- A grade conditional on D-041 before Sprint 5
- C73 locked at 10 stocks (permanent MVP)
- Feature Intake Filter adopted (4-question historian test)

## Round 16: Final Confirmation (2026-06-20)
**Theme**: Review Round 16 — New features + Architecture + Design

### Round 1 (Gap Authenticity): ✅ CONFIRMED
- C83 (Investment Memo) and C85 (Wellness Check) validated as genuine gaps — no TW competitor has these
- C81 (Decision Scenarios), C82 (Animated Story), C84 (Case Studies) are medium-term opportunities
- No features rejected — all pass historian filter

### Round 2 (Priority): ✅ CONFIRMED
- Sprint 4/5 planned work remains priority
- C83/C85 for Sprint 6+; C81, C82, C84 post-Sprint 5
- No priority changes to existing sprint plans

### Round 3 (Goal Alignment): ✅ CONFIRMED with conditions
- All new features pass historian test
- A grade conditional on D-041 before Sprint 5
- C82 de-risked: start with static MVP

**✅ CONFIRMED** with 4 conditions. No fundamental strategic disagreements.

### Round 1 (Gap Authenticity): ❌ REQUIRES REVISION
- **C69 REJECTED** — Paper trading contradicts historian positioning
- **C70 DECLASSIFIED** — Fold into C37 redesign, not standalone
- **C72 DECLASSIFIED** — Merge into C48, layout change not feature
- **C73 PIVOT** — From investor holdings to fundamental analysis synthesis
- **C74 PIVOT** — From prediction to historical scenario exploration
- **C71 REFRAME** — From login streak to study log
- Zero competitor-blind-spot analysis done

### Round 2 (Priority): ⚠️ PARTIALLY RESOLVED
- D24→D16→C38 confirmed sound
- New features need recalculation after declassifications
- "Fix one, build one" policy recommended

### Round 3 (Goal Alignment): ❌ REQUIRES REVISION
- 0 of 6 new features serve "Story first" in original form
- Structural changes needed: Positioning Impact Score, Feature Budget Rule, Beginner/Advanced paths

### Final Challenger Decision: ❌ REQUIRES REVISION
10 required changes adopted by PM. Sprint 4 approved with revised Sprint 5.

### PM Revised Decision
**Approved**: D24 → D16 → R3 → C38 → C51 → C53-1
**Sprint 5**: P1 fixes + C71 (Study Log) + C73 (Expert Analysis) + C74 start
**Structural policies**: Positioning Impact Score, Feature Budget (+1/-1), Beginner/Advanced labels, Fix one build one

---

## Round 17: Three-Round Challenge (2026-06-21)
**Theme**: Review Round 17 — 5 New Features (C93-C97) + Architecture Debt + Design Debt

### Round 1 (Gap Authenticity): ⚠️ PARTIALLY REVISED

**Challenger Questions:**

1. **C93 (Dividend Income Calendar) — Real gap or feature creep?** We already have C1 (ex-dividend countdown) on individual stock pages. Is a market-wide calendar truly a gap, or is it a "nice to have" that dividend investors would use but beginners (our core audience) wouldn't need? Beginners typically own 0-3 stocks — a market-wide calendar is overkill for them.

2. **C94 (Earnings Story) — Are we building a news product?** The description says "auto-generate earnings narratives within 24 hours of release." This sounds like a news/summary product, not a historian tool. The "What happened next" section ("After beating expectations 3 quarters in a row, TSMC's stock rose an average of X%") borders on predictive framing. Is this really "historian" or are we drifting toward "stock picker"?

3. **C95 (Watchlist Health Dashboard) — Do beginners have watchlists?** Our target user is a beginner. Beginners don't have watchlists with enough stocks to make an "aggregate health score" meaningful. A beginner with 3 stocks doesn't need portfolio diversification analysis. Is this feature for our actual target user?

4. **C96 (Sector Ecosystem Map) — Too complex for the value?** At 16-22h, this is the second-most expensive new feature. It requires a `sector_ecosystems.yaml` data file that must be manually curated (5-7 ecosystems, each with companies + relationships + descriptions). This is essentially a content-heavy feature disguised as a technical feature. The maintenance burden alone is significant — supply chains change, companies pivot. Who updates this data? And does a beginner really need to understand TSMC → 鴻海 → Apple supply chain relationships?

5. **C97 (First 30 Days) — Too ambitious for a single feature?** At 18-24h, this is the most expensive new feature. It requires 30 unique daily lessons, each with content, micro-tasks, and interactive elements. That's essentially a full course creation project. We already have C58 (Beginner Onboarding Flow) planned. Is C97 replacing C58 or duplicating it? And 30 days of content is a massive content creation effort — is this really a "feature" or a "content project"?

6. **Cross-competitor synthesis — Are we combining things that shouldn't be combined?** The research says "Cross-competitor synthesis creates category-of-one features." But just because competitor A has X and competitor B have Y doesn't mean X+Y is a good feature. Are we falling into the "feature smoothie" trap — blending everything competitors have into an incoherent product?

**Team Response:**
- C93: Dividend investors ARE a huge TW market segment. C1 serves single-stock users; C93 serves the "income planning" use case. Beginners who want passive income need this. The "annual income timeline" makes abstract dividend investing concrete.
- C94: The "What happened next" section is historical ("here's what happened historically after similar earnings"), not predictive. This is pure historian. M5 already detects earnings events — we're just adding narrative to existing detection.
- C95: Even beginners with 3 stocks benefit from "your watchlist is 100% tech" awareness. This teaches diversification concepts early. It's educational even for small watchlists.
- C96: TW's supply chain position IS the story of TW stocks. This is the ultimate "historian" feature — explaining how companies relate to each other. The YAML data file is a one-time cost with low maintenance.
- C97: This IS C58 — it's the implementation of the onboarding flow. 30 days of 5-minute tasks is manageable content. Each task leverages existing features (explore a company, add to watchlist). The content creation is front-loaded; maintenance is minimal.
- Cross-competitor synthesis: The synthesis approach is validated — C68 (Financial Concept Storytelling) from Round 13 was approved and fits perfectly. The key is filtering through "historian" positioning.

**Challenger Verdict: ⚠️ PARTIALLY REVISED**
- **C93 CONDITIONAL**: Confirmed for dividend investors, but must NOT be positioned as a beginner feature. It's for intermediate users who already have watchlists. If it becomes a beginner-facing feature, it fails the ten-second test. Condition: Position as "股利投資者工具" not "新手入門."
- **C94 CONDITIONAL**: The "What happened next" section must be strictly historical with clear disclaimers. Must use _historian_disclaimer() (D-040) for every earnings story. Condition: Add explicit "歷史資料，不構成投資建議" disclaimer to every earnings narrative.
- **C95 REJECTED for current sprint**: This is a Sprint 7+ feature. Beginners don't need portfolio analytics. Reclassify as post-Sprint 6. The 10-14h is better spent on Sprint 5 prerequisites.
- **C96 REJECTED for current sprint**: 16-22h for a content-heavy feature with ongoing maintenance burden is not justified when Sprint 5 isn't started. The YAML data file is a hidden cost — every quarter, supply chain relationships change. Reclassify as Sprint 7+.
- **C97 CONDITIONAL**: This is essentially C58 implementation. Rename to "C58 Implementation" to avoid confusion. 18-24h is realistic for 30 days of content. Condition: Must reuse existing features (company pages, watchlist, event dashboard) — no new feature development within the 30 days. Pure content + task design.
- **Net result**: 5 features → 3 conditional (C93, C94, C97), 2 rejected for current sprint (C95, C96). Effort reduced from 70-94h to 42-58h for near-term.

---

### Round 2 (Priority): ⚠️ REVISED

**Challenger Questions:**

1. **Should C93-C97 take priority over Sprint 5 planned work (C71, C73, C74)?** Sprint 5 has been planned for 3+ rounds now. D-039, D-040, D-041 (Sprint 5 prerequisites) haven't been started. Every review round adds new features but Sprint 5 never starts. When does planned work take priority over new discoveries?

2. **What's the right sequence?** We have: P0 bug (D-043, 0.25h), Sprint 5 prerequisites (D-039, D-040, D-041, ~2.5h), Sprint 5 features (C71, C73, C74, 42h), design debt (D-042-D-048, 5.75h), architecture debt (D-044, D-046, 3.5h), and now 5 new features (42-58h after revision). That's ~96-112h of work. What gets done first?

3. **Is the P0 bug (D-043) being given enough urgency?** D-043 crashes the business card page for certain stocks (NameError on `get_roe_analyzer()`/`get_pbr_analyzer()`). This is a runtime crash — users see an error page. It's been identified as P0 but is only 0.25h to fix. Why hasn't it been fixed immediately? It's been at least 1 round since discovery.

4. **Should D37 (sections split) be elevated to P0?** `_sections.py` is now 918 lines (was 612 after D24 extraction, grew from C38 + C48 + C53-1). The threshold for splitting was 600 lines. It's now 53% over threshold. Every new feature added to the business card page makes this worse. At what point does the file become unmaintainable?

5. **The 918-line `_sections.py` is a bigger crisis than any new feature.** We extracted `business_card.py` into a sub-directory specifically to avoid monoliths, and now `_sections.py` is the new monolith. Shouldn't splitting this be THE priority before any new features are added to the business card page?

**Team Response:**
- Sprint 5 planned work MUST take priority. The team has agreed: D-039, D-040, D-041 first, then C71, C73, C74. New features from review rounds are for future sprints, not current sprint insertion.
- Right sequence: (1) D-043 P0 bug fix immediately, (2) D-039/D-040/D-041 Sprint 5 prerequisites, (3) D37 sections split alongside C71/C73/C74, (4) Sprint 5 features, (5) design/architecture debt, (6) new features (C93, C94, C97) for Sprint 6+.
- D-043: Agreed — this should have been fixed in the previous round. It's a 15-minute fix that blocks users. Must be fixed before any other work.
- D37: Agreed on urgency. `_sections.py` at 918 lines is a crisis. However, splitting it alongside C71/C73/C74 implementation (rather than as a separate task) is the right approach — each new section function goes into the appropriate split file.
- The 918-line file is indeed a bigger crisis than new features. D37 should be elevated to P1 (not P0 — it doesn't crash, it just makes maintenance harder).

**Challenger Verdict: ⚠️ REVISED**
- **Priority sequence confirmed**: D-043 (P0, fix immediately) → D-039/D-040/D-041 (Sprint 5 prerequisites) → C71/C73/C74 with D37 split alongside → design/architecture debt → new features.
- **D-043**: Must be fixed in the current cycle. No new feature work until this is resolved. A P0 bug that crashes pages cannot wait another round.
- **D37**: Elevated to P1. Not P0 (doesn't crash), but must be addressed before or alongside Sprint 5 feature implementation. Every new section added to `_sections.py` increases the split effort.
- **C93/C94/C97**: Sprint 6 at earliest. No new features enter Sprint 5. Sprint 5 scope is locked: C71 + C73 + C74 + prerequisites.
- **C95/C96**: Sprint 7+. Not urgent, high effort, content-heavy.

---

### Round 3 (Goal Alignment): ⚠️ REVISED

**Challenger Questions:**

1. **Does the overall direction still align with "historian, not stock picker"?** C94's "What happened next" section ("After beating expectations 3 quarters in a row, TSMC's stock rose an average of X%") is dangerously close to implying future performance. Even with disclaimers, the framing teaches users to expect patterns to repeat. Is this really historian or are we teaching pattern-matching that leads to stock picking?

2. **Are there contradictions between new features and existing roadmap?** C97 (First 30 Days) overlaps with C58 (Beginner Onboarding Flow), C50 (Learning Progress Tracker), and C60 (Concept Mastery Badges). That's 4 features addressing beginner onboarding. Are we over-investing in onboarding at the expense of core analysis features?

3. **What are the risks of adding 5 more features when Sprint 5 isn't started?** We now have 97 identified features (C01-C97). Only ~30 are implemented. The gap between identified and implemented features grows every round. At what point does the feature backlog become demoralizing? Are we building a roadmap or a wish list?

4. **Is the total effort realistic?** The review estimates 57.1h for debt + fixes. Sprint 5 is 42h. New features (after revision) are 42-58h. That's ~141-157h total. At a realistic pace of 20-30h per sprint (accounting for testing, debugging, review), that's 5-8 sprints of work. Are we planning for a realistic timeline or an aspirational one?

5. **The "historian" positioning is being stretched.** C93 (dividend income projection), C94 (earnings narratives), C95 (portfolio health), C96 (ecosystem maps), C97 (onboarding curriculum) — these are 5 very different types of features. Dividend calendars are for income investors. Earnings stories are for news consumers. Ecosystem maps are for advanced learners. Are we trying to be everything to everyone?

6. **Feature Budget Rule**: Round 14 established a "+1/-1" feature budget — for every new feature added, one must be removed or deferred. We're adding 5 new features this round. Which 5 existing features are being removed or deferred?

**Team Response:**
- C94's "What happened next" is explicitly historical — "here's what happened in the past after similar events." This is the historian's approach: teaching patterns from history without predicting the future. The key is framing and disclaimers.
- C97 IS C58. They're the same feature. C58 was the concept; C97 is the implementation plan. No contradiction — just naming evolution. C50 and C60 are complementary (progress tracking + badges), not duplicative.
- The feature backlog (97 identified, ~30 implemented) is a natural consequence of review rounds. Not all 97 will be built. The prioritization process (P0/P1/P2 + sprint planning) ensures only the most important features get built. The backlog is a menu, not a mandate.
- Total effort: 57.1h (debt) + 42h (Sprint 5) + 42-58h (new features) = ~141-157h. At 25h/sprint average, that's ~6 sprints. This is realistic for a part-time development pace over 6-8 months.
- The "historian" positioning is broad enough to cover all these features. A historian explains dividends (C93), earnings (C94), portfolio composition (C95), market ecosystems (C96), and teaches beginners (C97). These are all "explaining the past and present," not "predicting the future."
- Feature Budget Rule: The rule applies within a sprint, not across review rounds. Sprint 5 scope is locked (C71/C73/C74). New features enter Sprint 6+ planning. No existing features need to be removed because new features are for future sprints.

**Challenger Verdict: ⚠️ REVISED**
- **Historian alignment**: CONDITIONAL. C94 must have explicit historical framing and disclaimers. The "What happened next" section must be labeled "歷史統計" not "未來展望." All 5 features pass the historian filter IF properly framed.
- **Feature overlap**: C97 replaces C58 (confirmed same feature). C50 and C60 remain complementary. No contradiction.
- **Backlog concern**: VALID. 97 features is a large backlog. Recommend the PM create a "Feature Triage" process — every 3 rounds, review the entire backlog and explicitly defer or cancel low-priority items. The backlog should shrink over time, not grow.
- **Effort realism**: 141-157h is realistic BUT only if Sprint 5 starts immediately. The risk isn't the total effort — it's that every review round adds more features before planned work is completed. Recommend a "Sprint 5 Lock" — no new features enter Sprint 5 scope, period.
- **Feature Budget Rule**: The team's interpretation (within-sprint, not cross-round) is accepted BUT with a modification: for every 5 new features identified, at least 1 existing P2 feature should be explicitly deferred or cancelled. This prevents indefinite backlog growth. This round: defer C52 (Quiz Mode) and C55 (Investment Diary) to "Sprint 8+" given the new beginner-focused features (C97) address similar needs.
- **Net direction**: The overall direction aligns with "historian, not stock picker" but the breadth of features risks diluting focus. Recommend grouping future features into "historian themes" (e.g., "Market Stories" = C93+C94, "Beginner Education" = C97, "Advanced Analysis" = C95+C96) to maintain coherence.

---

### Final Challenger Decision: ⚠️ REVISED

**Sprint 5 Scope (LOCKED):**
1. **D-043** — P0 bug fix (0.25h) — IMMEDIATE, before any other work
2. **D-039 + D-040 + D-041** — Sprint 5 prerequisites (2.5h)
3. **C71 + C73 + C74** — Sprint 5 features (42h)
4. **D37** — Sections split alongside feature implementation (elevated to P1)

**Sprint 6+ (New Features):**
- C93 (Dividend Income Calendar) — P1, 12-16h — CONDITIONAL on positioning as intermediate feature
- C94 (Earnings Story) — P1, 14-18h — CONDITIONAL on historical framing + disclaimers
- C97 (First 30 Days / C58 Implementation) — P1, 18-24h — CONDITIONAL on content-only (no new feature dev)

**Sprint 7+ (Deferred):**
- C95 (Watchlist Health Dashboard) — P2, 10-14h
- C96 (Sector Ecosystem Map) — P2, 16-22h

**Explicitly Deferred (Feature Budget):**
- C52 (Quiz Mode) — Sprint 8+ (C97 addresses beginner education more comprehensively)
- C55 (Investment Diary) — Sprint 8+ (lower priority than new features)

**Conditions:**
1. D-043 must be fixed before any new development work begins
2. Sprint 5 scope is locked — no new features added
3. D37 elevated to P1, split alongside C71/C73/C74
4. Feature Triage process established (every 3 rounds, review entire backlog)
5. C94 must use _historian_disclaimer() and "歷史統計" framing
6. C93 positioned as intermediate feature, not beginner feature

**Total Committed Effort:**
- Immediate: 0.25h (D-043)
- Sprint 5: ~47h (prerequisites + features + D37 split)
- Sprint 6+: 42-58h (C93 + C94 + C97)
- Sprint 7+: 26-36h (C95 + C96)
- **Grand Total: ~115-141h** (vs 141-157h pre-revision, -26h from deferrals)

---

## Round 18: Three-Round Challenge (2026-06-23)
**Theme**: Sprint 7 Planning — C84 Market Event Case Study + Debt Cleanup

### Round 1 (Gap Authenticity): ⚠️ PARTIALLY REVISED

**Challenger Findings:**

The team's summary contains **outdated status information** that materially affects Sprint 7 planning:

1. **D-043 is NOT "still open after 2 sprints"** — it was fixed in Sprint 5 (commit 318d30f, handoff_dev.md line 12). The `get_roe_analyzer`/`get_pbr_analyzer` → `get_roe_analogy`/`get_pbr_analogy` rename was completed. The tech_debt.md and review_report.md still list it as open, but the actual code in `_financial.py` already uses the correct function names. This is a **documentation debt** problem, not a code problem. The team summary incorrectly presents a fixed bug as a current crisis.

2. **D-046 is NOT "st.html() JS still broken"** — handoff_dev.md line 21 shows D-046 was about "Sector heatmap 4th KPI uses inline HTML" which was fixed with `_白话_card()` (344a895). The share section JS issue (if it still exists) is a separate, untracked problem. The team is conflating two different issues under one ID.

3. **st.markdown counts are dramatically overstated**:
   - D-048: financial_wellness.py has **14** st.markdown calls, not 84. The "84" figure may have been from a different version or included all st.* calls.
   - D-049: notification_center.py has **10** st.markdown calls, not 47.
   - D-050: investment_memo.py has **7** st.markdown calls, not 35.
   - The _sections/ sub-modules collectively have **32** st.markdown calls across 5 files.
   - **Total st.markdown across all Sprint 6 deliverables: ~63, not 166 as implied.** The debt severity is significantly lower than presented.

4. **Sprint 6 scope change is significant** — The team planned C93/C94/C97 for Sprint 6 but delivered C83/C85/C02/C43/C45 instead. This means:
   - C02 (Notifications) was added as a P0 competitive gap fix — correct decision
   - C43 (Health Snowflake) was extracted from existing code — correct decision
   - C93/C94/C97 were deferred — but the team summary doesn't acknowledge this as a scope change, it just lists them as "Sprint 7 priorities"
   - The real question: should C93/C94/C97 still be on the roadmap, or has the product moved past them?

5. **Is 38.4h realistic?** The estimate has several hidden costs:
   - C84's 12h dev estimate excludes **content creation** (5-10 case studies). The developer notes say "8-10h of PM/Designer time" for content — this is parallel work but it's real work that must happen.
   - D3 (inline HTML consolidation) at 3.5h is optimistic for 5+ pages with unique layouts. The risk section itself says "could hit 6-8h."
   - D6 (YAML migration) could break import chains — the risk section acknowledges this.
   - **Realistic range: 38-50h**, not 34-44h. The 38.4h midpoint assumes everything goes right.

**Team Response:**
- D-043: Acknowledged as fixed in Sprint 5. The tech_debt.md and review_report.md are outdated — documentation debt, not code debt. Will update status docs.
- D-046: The sector heatmap KPI fix is complete. The share section JS issue (st.html with fragile element IDs) may still exist but is a separate, lower-priority issue. Will create a new debt item if confirmed.
- st.markdown counts: The original counts (84/47/35) were from an earlier analysis that may have included all st.* calls or been from a pre-refactor version. The current counts (14/10/7) are accurate for the shipped code. Debt severity is lower than presented.
- Sprint 6 scope change: C02 and C43 were correctly prioritized as competitive gap fixes. C93/C94/C97 remain on the roadmap for future sprints.
- 38.4h estimate: Acknowledged as optimistic. The 34-44h range should be 38-50h to account for content creation and risk contingencies.

**Challenger Verdict: ⚠️ PARTIALLY REVISED**
- **D-043**: CLOSED (was fixed in Sprint 5). Remove from Sprint 7 priorities. Update tech_debt.md and review_report.md.
- **D-046**: CLOSED (sector heatmap KPI fixed). Share section JS issue needs a new debt item if confirmed.
- **D-048/D-049/D-050**: Severity DOWNGRADED. st.markdown counts are 55-78% lower than claimed. These are minor style issues, not architectural problems.
- **Sprint 6 scope change**: ACKNOWLEDGED. C02 and C43 were correct additions. C93/C94/C97 remain for future sprints.
- **38.4h estimate**: ADJUSTED to 38-50h. The 34-44h range is too narrow.

---

### Round 2 (Priority): ⚠️ REVISED

**Challenger Questions:**

1. **Should C84 (12h, 31% of Sprint 7 budget) be the main feature?** C84 is "Market Event Case Study" — an interactive historical market event explorer. At 12h dev + 8-10h content creation, it's actually a 20-22h feature. That's 46-58% of the adjusted Sprint 7 budget. Is this the right centerpiece for Sprint 7?

2. **Should we do more debt cleanup instead?** The top 5 debt items (D-044, D3, D6, D13, D7) total 17.6h. C84 alone is 12h. Combined: 29.6h + 4h verification = 33.6h before content creation. That leaves 4.6-16.4h of buffer in the 38-50h range. Is this enough buffer for a content-heavy feature?

3. **Is the Sprint 7 scope appropriate?** The original Sprint 7 plan was 30-45h. The current estimate is 38-50h. That's at the high end AND above the original range. Should we defer one debt item to Sprint 8 to create more buffer?

4. **C84 depends on content creation that's outside the dev estimate.** The developer notes say "8-10h of PM/Designer time" for case study writing. Who is doing this work? Is the PM/Designer available? If content creation slips, C84 ships with fewer case studies — is that acceptable?

5. **D13 (test infrastructure) at 4.2h is a long-term investment with no immediate user value.** Should D13 be deferred to Sprint 8 to free up 4.2h for C84 buffer or additional debt work? Tests are important but invisible to users.

6. **The debt items selected are all "infrastructure" improvements** (service extraction, component consolidation, YAML migration, test setup). None of them directly improve the user experience. Should we include at least one user-facing debt fix in Sprint 7?

**Team Response:**
- C84 as main feature: Yes — it's the #1 "historian" differentiator. No TW competitor has interactive historical market events. The 12h dev estimate is for the framework; content creation is parallel work that doesn't block other Sprint 7 items.
- Debt + C84 balance: 17.6h debt + 12h C84 = 29.6h is appropriate for a 38-50h sprint. The buffer (8.4-20.4h) accounts for content creation and risk contingencies.
- D13 deferral: Agreed — D13 (test infrastructure) can be deferred to Sprint 8. It's important but not urgent, and it frees 4.2h for buffer. **Revised Sprint 7: 34.2h (38 - 4.2h D13).**
- User-facing debt: Good point. Recommend adding D-045 (card-count limit compliance) as a user-facing fix — it directly improves the sector heatmap UX. Already included at 1.2h.
- Content creation risk: If PM/Designer bandwidth is constrained, C84 ships with 3 case studies instead of 5-10. The framework works regardless of content volume.

**Challenger Verdict: ⚠️ REVISED**
- **C84 as main feature**: CONFIRMED. It's the strongest "historian" feature in the pipeline. The 12h dev + parallel content creation model is sound.
- **D13 deferred to Sprint 8**: CONFIRMED. Frees 4.2h buffer. Revised Sprint 7 total: 34.2h (range 34-44h).
- **Debt + feature balance**: 13.4h debt (4 items) + 12h C84 + 4.8h spikes = 30.2h + 4h verification = 34.2h. This is appropriate.
- **Add user-facing debt**: D-045 (card-count audit) is already included. Additionally, recommend fixing the share section JS issue (currently untracked) as a quick win alongside D3.
- **Content creation**: C84 ships with minimum 3 case studies. If content creation slips, the feature still delivers value.

---

### Round 3 (Goal Alignment): ✅ CONFIRMED with conditions

**Challenger Questions:**

1. **Does C84 pass the "historian, not stock picker" test?** "Market Event Case Study" — exploring historical market events like the 2008 crisis, COVID crash, etc. This is pure historian: "here's what happened, here's how stocks behaved, here's what we learned." No prediction, no recommendation. This is the **strongest historian feature** in the entire roadmap.

2. **Does Sprint 7 balance features vs debt well?** 12h feature + 13.4h debt + 4.8h spikes = 30.2h. That's a 40/52/8% split (feature/debt/spikes). This is a reasonable balance — slightly debt-heavy, which is appropriate after 6 sprints of feature development.

3. **Are we building the right things in the right order?** Sprint 7 is the first sprint where we're NOT adding a major new page type. C84 is a standalone page, but it's thematically aligned with the business card page (historical context). The debt work (D-044, D3, D6, D7) improves existing pages. This feels like a "consolidation sprint" — appropriate timing.

4. **Is the "historian" positioning being diluted?** Looking at the full roadmap: C84 (historical events), C82 (animated data story), C81 (decision scenarios), C63 (weekly brief), C64 (community), C65 (filings), C68 (concept storytelling). Every feature is historian-aligned. No dilution detected.

5. **What about the deferred features (C93/C94/C97)?** These were deferred from Sprint 6, not cancelled. C93 (dividend calendar) and C94 (earnings story) are historian-aligned. C97 (first 30 days) is beginner education. All three should remain on the roadmap for Sprint 8+.

6. **The 9th consecutive Design Grade A is impressive but fragile.** Sprint 7 adds C84 (new page) + debt cleanup (touches existing pages). Each change is a regression risk. Should we add a design review gate before C84 ships?

**Team Response:**
- C84 historian alignment: Strongly confirmed. "What happened during the 2008 crisis for TW stocks?" is the quintessential historian question. No competitor has this.
- Feature/debt balance: 40/52/8% is appropriate. The debt work enables future features (D-044 enables market-level features, D3 enables consistent UI, D6 enables content scaling, D7 improves performance).
- Right order: Sprint 7 as consolidation sprint is correct timing. After 6 sprints of feature development, the infrastructure needs attention.
- Historian positioning: Not diluted. The roadmap is coherent — all features explain the past/present, none predict the future.
- Deferred features: C93/C94/C97 remain on the roadmap. C93 and C94 for Sprint 8, C97 for Sprint 9+.
- Design review gate: Agreed — add a design review checkpoint before C84 ships. The Designer should review the case study template, event timeline UI, and navigation patterns.

**Challenger Verdict: ✅ CONFIRMED with conditions**
- C84 is the **strongest historian feature** in the roadmap. Full support.
- Sprint 7 balance is appropriate — slightly debt-heavy, which is correct for this stage.
- Roadmap coherence is maintained. No positioning drift.
- Design review gate added as a condition.

---

### Final Challenger Decision: ✅ CONFIRMED with conditions

**Sprint 7 Scope (CONFIRMED):**
1. **C84** — Market Event Case Study (12h dev + parallel content creation) — Main feature
2. **D28 spike** — Animated Data Story feasibility (3.6h)
3. **D-045 spike** — Card-count limit compliance (1.2h)
4. **D-044** — market_data.py extraction (3.0h)
5. **D3** — ui_components.py consolidation (4.2h)
6. **D6** — YAML migration (4.2h)
7. **D7** — N+1 fix in category_browser.py (3.0h)

**Deferred to Sprint 8:**
- D13 (test infrastructure) — 4.2h, important but not urgent

**Revised Sprint 7 Total: 34.2h (range 34-44h)**

**Conditions:**
1. **D-043 status must be updated** in tech_debt.md and review_report.md — it's been fixed since Sprint 5
2. **D-046 status must be updated** — sector heatmap KPI fix is complete
3. **D-048/D-049/D-050 severity downgraded** — st.markdown counts are 55-78% lower than originally claimed
4. **C84 ships with minimum 3 case studies** — content creation is parallel and may slip
5. **Design review gate before C84 ships** — Designer reviews case study template, timeline UI, and navigation
6. **Share section JS issue** — create new debt item if confirmed still broken
7. **C93/C94/C97 remain on roadmap** for Sprint 8+

**Total Committed Effort:**
- Sprint 7: 34.2h (range 34-44h)
- Sprint 8+: C93 (14h) + C94 (16h) + C97 (21h) + D13 (4.2h) + C82 (conditional on D28) = 55.2h+ C82

---

## Round 20: Three-Round Challenge (2026-06-13)
**Theme**: Sprint 7 Completion Review — C84 Market Event Case Study + Debt Cleanup + 6 New Feature Gaps (C98-C103) + 8 New Debt Items (D-048 through D-056)

### Round 1 (Gap Authenticity): ⚠️ PARTIALLY REVISED

**Challenger Questions:**

1. **C98 (Event Interpretation Engine) — P1 or premature?** The concept is compelling: combine M5 event detection with AI narrative to answer "Why did this stock move?" But let's examine feasibility. M5 detects events from structured data (price spikes, volume anomalies, earnings releases). The "interpretation" layer requires an LLM to synthesize multiple data points into a coherent narrative. Our current LLM usage is strictly limited to "plain-language translation only" (per product vision line 76). Are we ready to expand LLM scope from translation to interpretation? And is this truly P1 — or is it P2 until M5 event detection is more mature? The 14-18h estimate assumes the M5 event data is clean enough to feed into narrative generation. Is it?

2. **C99 (Scrollytelling Visual Company History) — Who is this for?** At 16-22h, this is expensive. Scrollytelling is a premium visualization technique (think NYT-style interactive articles). Our target users are beginners who feel overwhelmed by jargon. Will a beginner appreciate — or even sit through — a scrollytelling experience? Or is this actually for advanced users who already understand the basics? If it's for advanced users, does it align with our "beginner-first" positioning?

3. **C100 (Natural Language Screener with "Why It Passed") — Feature creep toward stock picker?** A natural language screener that says "Show me companies with rising revenue and low debt" sounds useful. But the "Why It Passed" explanation is the dangerous part — it implies the screener is making recommendations. "This stock passed because revenue is rising" sounds like "this is a good stock." Are we building a screener (stock picker tool) or an educational tool? The product vision explicitly says "Do not say buy or sell; only explain what has happened." A screener inherently filters toward "buy" candidates.

4. **C101 (Comprehension Check Quiz) — Genuine gap or nice-to-have?** At 8-12h, this is relatively cheap. But we already have C52 (Quiz Mode) on the backlog. Is C101 a replacement for C52 or a different feature? If it's a replacement, we should explicitly cancel C52. If it's different, what's the distinction? Having two quiz features on the backlog is confusing.

5. **C102 (Market Narrative Feed) — Social media feature in a historian tool?** "Social-Media AI Story Stream" sounds like a news/social feed. Our product is about understanding companies, not consuming market news. This feels like it belongs in a trading platform, not Stock Explorer. The product vision says "Focus on the company itself, not short-term price movement." A narrative feed is inherently about short-term market sentiment. Is this a genuine gap or are we copying competitors because they have it?

6. **C103 (Learn First Gate) — Onboarding gate or user friction?** Requiring users to complete a learning module before accessing the tool is a bold UX decision. It signals "our tool is too complex to use without training" — which contradicts the "PPT-style presentation" and "ten-second test" principles. If users need a gate to understand our tool, the tool has failed. Is this solving a real problem or creating one?

7. **6 features at once — triage needed?** The competitor research identified 6 gaps simultaneously. But not all gaps are equal. C98 and C100 are P1; C99, C101, C102, C103 are P2. Should we focus on the P1 items first and validate them before even considering P2? Adding 6 features to the backlog in one round is how backlogs become unwieldy.

**Team Response:**
- C98: The M5 event detection is already operational. The interpretation layer uses the same LLM we already use for plain-language translation — we're expanding from "translate this number" to "explain this event." The structured data from M5 (event type, magnitude, timing) provides the factual backbone; the LLM adds narrative context. This is a natural extension, not a new capability. P1 is correct because no TW competitor offers event detection + narrative.
- C99: Scrollytelling is for the "curious observer" user persona — someone who wants to understand a company's journey. It's not for advanced users; it's for beginners who learn through narrative. The NYT comparison is apt — NYT uses scrollytelling for general audiences, not experts.
- C100: The screener is educational, not recommendatory. Users define criteria; the tool shows matching companies and explains WHY they match. "Why it passed" means "here's the data that matches your criteria," not "here's why you should buy." The historian framing is: "here's what the data shows." This is C68 (Concept Storytelling) applied to screening.
- C101: C101 IS C52. Same feature, renamed. C52 should be cancelled and replaced by C101. The distinction: C52 was a generic quiz concept; C101 is specifically "comprehension checks" tied to case studies and educational content.
- C102: The narrative feed is about market stories, not stock picks. "Here's what happened in the market today" — historian framing. It's not about sentiment or momentum; it's about explaining market events in plain language. This is C84 (Case Studies) in a feed format.
- C103: The Learn First Gate is optional — it's a "guided first visit" pattern, not a hard gate. Users can skip it. The goal is to reduce the "overwhelmed beginner" problem by providing a structured first experience. It aligns with the "ten-second test" by ensuring users understand the basics before exploring.
- Triage: Agreed — P1 items (C98, C100) should be prioritized. P2 items (C99, C101, C102, C103) are backlog items for future consideration.

**Challenger Verdict: ⚠️ PARTIALLY REVISED**
- **C98 CONDITIONAL**: Confirmed as P1, but the LLM scope expansion from "translation" to "interpretation" needs explicit approval. The product vision limits LLM to "plain-language translation only." Adding narrative interpretation is a policy change, not just a feature. Condition: Update product vision to allow LLM interpretation layer, with the constraint that all interpretations must cite structured data sources (no hallucinated narratives). The 14-18h estimate is realistic IF M5 event data is clean. Recommend a 2h spike to validate M5 data quality before committing to C98 development.
- **C99 DOWNGRADED to P2→P3**: Scrollytelling at 16-22h is too expensive for a P2 feature when we have 11-17h of debt to address. The "curious observer" persona is valid, but this feature doesn't serve the core "beginner investor" persona as directly as other features. Defer to Sprint 9+. The NYT comparison is misleading — NYT has a team of journalists and designers. We have one developer.
- **C100 REJECTED**: This is the most dangerous feature in the batch. A natural language screener, no matter how carefully framed, teaches users to filter stocks by criteria — which is stock-picking behavior. "Show me companies with rising revenue" is a stock screen. "Why it passed" is stock-picking logic. This directly contradicts "historian, not stock picker." The educational framing is a thin veneer over a screening tool. **REJECTED.** If the team wants educational screening, build it as a "Screening Concepts" educational page that teaches what screening IS, not a functional screener.
- **C101 CONFIRMED (replaces C52)**: Cancel C52, replace with C101. 8-12h is reasonable for comprehension checks tied to existing educational content. This is a natural extension of C84 case studies.
- **C102 REJECTED**: A "Market Narrative Feed" is a news/social product feature. It requires ongoing content curation, real-time data feeds, and moderation. It's not a historian feature — it's a market news feature. The product vision explicitly says "Focus on the company itself, not short-term price movement." A narrative feed is inherently about short-term market sentiment. **REJECTED.** If the team wants market event narratives, that's what C84 already provides — in a structured, educational format.
- **C103 CONDITIONAL**: The "optional guided first visit" pattern is acceptable IF truly optional (skip button prominent, no nag screens). But calling it a "gate" is misleading — it's an onboarding flow. Rename to "First Visit Guide" and position as C58 implementation, not a separate feature. Condition: Must be completable in under 3 minutes, must have a visible skip option, and must not block access to any feature.
- **Net result**: 6 features → 2 confirmed (C98 conditional, C101 confirmed), 2 rejected (C100, C102), 2 deferred (C99 P3, C103 conditional/rename). Effort reduced from 82-112h to 22-30h for near-term (C98 + C101).

---

### Round 2 (Priority): ⚠️ REVISED

**Challenger Questions:**

1. **D6 was claimed "resolved" in Sprint 7 but architect says only 1/6 blocks migrated. Is this acceptable?** The Sprint 7 summary says D6 (YAML migration) was delivered. The architect says only 1 of 6 data blocks was migrated, and market_event_service.py's _CASE_STUDIES (230 lines of hardcoded data) is a NEW violation. This is a significant discrepancy. Was D6 tested before marking it resolved? The 230-line _CASE_STUDIES block is the largest single hardcoded data block in the codebase — it's the exact problem D6 was supposed to solve.

2. **11-17h of debt before Sprint 8 features — is this acceptable?** The total remaining debt is: D6(3-4h) + D8(1-2h) + D9(1-2h) + D10(1-2h) + D-048(1-2h) + D-050(1-2h) + D-055(2-3h) = ~11-17h. That's essentially a full sprint of debt work before any new features. At what point do we stop adding new features and focus on debt? We've been accumulating debt for 7 sprints.

3. **D-048 (230-line _CASE_STUDIES) should be P1, not Medium.** This isn't just "hardcoded data" — it's 230 lines of educational content mixed with code. Every new case study requires a code change, not a data change. This is the exact anti-pattern D6 was supposed to fix. The fact that Sprint 7 delivered C84 (which added this block) while claiming to resolve D6 is ironic. Shouldn't migrating _CASE_STUDIES to YAML be the FIRST task of Sprint 8?

4. **The "No Inline HTML" rule failed — is it enforceable?** D3 (card consolidation) was marked resolved in Sprint 7, but C84 introduced 116 lines of new inline HTML in market_event_case_study.py (lines 109-117, 143-157). The sector_heatmap.py has 150+ lines of inline HTML. The etf_browser.py has inline HTML in the hot ETFs and dividend ranking tables. The pattern is clear: developers use inline HTML because it's faster than using shared components. Is the rule enforceable without a linting rule or code review checklist? "No Inline HTML" as a policy has failed — every sprint adds more inline HTML.

5. **D-056 (_section_title inverted logic) — is this really Low?** The architect flagged _section_title() as having "inverted logic." Looking at the code: `_section_title(icon, title)` calls `st.markdown(f"### {icon} {title}")` — this looks correct. But the architect says the logic is inverted. If there's a bug in a shared component used across 209 call sites, this isn't Low — it's at least Medium. A bug in a shared component has multiplied impact. What exactly is the inverted logic?

6. **Should we do a "Debt Sprint" before Sprint 8?** With 11-17h of debt, plus new debt from C84 (D-048, D-050), maybe Sprint 8 should be a debt-only sprint. No new features — just pay down the backlog. This would free up Sprint 9 for C98 and C101 without the debt overhang.

**Team Response:**
- D6 discrepancy: The Sprint 7 claim was based on migrating 1 of 6 blocks (the market_data.py block, D-044). The architect is correct that 5 blocks remain, and _CASE_STUDIES is a new violation. D6 should be reclassified as "partially resolved" not "resolved." The 3-4h remaining estimate is for the other 5 blocks.
- 11-17h debt: This is acceptable IF we dedicate Sprint 8 to debt + small features. The alternative — letting debt accumulate further — is worse. We recommend Sprint 8 be "debt-heavy" (60% debt, 40% features).
- D-048 priority: Agreed — D-048 should be elevated to P1. Migrating _CASE_STUDIES to YAML is the single highest-impact debt item because it unblocks content scaling (new case studies without code changes). Recommend D-048 as the first Sprint 8 task.
- "No Inline HTML" rule: The rule is enforceable but requires tooling. Recommend adding a pre-commit hook or CI check that flags `unsafe_allow_html=True` in new files. Without automated enforcement, the rule relies on code review — which has consistently missed inline HTML.
- D-056: The "inverted logic" refers to _section_title() being a shortcut for `_section_header(collapsed=False)`, but the function name doesn't convey "collapsed=False" — it's just "title." The logic isn't inverted per se; the naming is misleading. The architect's "inverted logic" label was overstated. This is a naming issue, not a logic bug. Downgrade to "naming clarity" — 0.1h to add a docstring.
- Debt Sprint: Agreed in principle. Sprint 8 should be debt-first. Recommend: D-048 (P1, 1-2h) → D6 remaining blocks (3-4h) → D-055 (2-3h) → D-050 (1-2h) → D8/D9/D10 (3-6h) = 10-17h debt, leaving 8-14h for C98 spike + C101.

**Challenger Verdict: ⚠️ REVISED**
- **D6 status**: CONFIRMED as "partially resolved" — update all status docs. The 1/6 migration is real progress, but claiming "resolved" was incorrect. Remaining: 5 blocks, 3-4h.
- **D-048 elevated to P1**: CONFIRMED. _CASE_STUDIES migration to YAML is the highest-impact debt item. First task of Sprint 8. This unblocks content scaling for C84.
- **"No Inline HTML" rule**: The rule is NOT enforceable without automated tooling. RECOMMENDATION: Add a CI check that fails on `unsafe_allow_html=True` in new code. Until then, the rule is aspirational, not enforceable. Every sprint will continue to add inline HTML without automated enforcement.
- **D-056**: DOWNGRADED to "naming clarity" — not a logic bug. 0.1h to improve docstring. No code change needed.
- **Debt Sprint 8**: CONFIRMED. Sprint 8 should be debt-first: D-048 → D6 → D-055 → D-050 → D8/D9/D10. This clears 10-17h of debt before Sprint 9 features.
- **11-17h debt + new debt**: The total debt burden is now ~13-21h (including D-048 and D-050 from C84). This is significant but manageable if Sprint 8 is debt-first. The risk is that Sprint 8 adds new features that create more debt — perpetuating the cycle.

---

### Round 3 (Goal Alignment): ⚠️ REVISED

**Challenger Questions:**

1. **Does the overall direction still align with "historian, not stock picker"?** Let's audit the full feature set: C84 (Case Studies) — pure historian ✅. C98 (Event Interpretation) — historian IF properly constrained ⚠️. C100 (Natural Language Screener) — stock picker ❌ (rejected). C102 (Narrative Feed) — market news ❌ (rejected). C99 (Scrollytelling) — historian ✅ but expensive. C101 (Comprehension Check) — education ✅. C103 (Learn First Gate) — onboarding ✅. The two rejected features (C100, C102) were the ones that most clearly violated historian positioning. This suggests the competitor research is identifying features that don't fit our positioning. Are we doing enough filtering BEFORE features reach the backlog?

2. **The product vision says "Refuse to implement all features at once" (line 85). Are we following this?** We now have ~103 identified features (C01-C103). ~30 are implemented. The gap grows every round. The product vision explicitly warns against this. At what point do we stop identifying new features and focus on implementing existing ones? Round 20 added 6 new features and 8 new debt items. That's 14 new items in one review cycle. Is this sustainable?

3. **The "ten-second test" (line 88) — do C98-C103 pass?** C98: "Why did this stock move?" — a beginner can restate this in 10 seconds ✅. C99: "Company history as a visual story" — ✅. C100: "Screen stocks with natural language" — this is jargon, fails the test ❌. C101: "Quiz to check understanding" — ✅. C102: "Market narrative feed" — "narrative feed" is jargon ❌. C103: "Learn before you explore" — ✅. The two that fail the ten-second test are the two we rejected. This validates the filtering approach.

4. **Design Grade A for 10 consecutive rounds — but inline HTML keeps growing.** How can the design grade be A when inline HTML is increasing every round? The designer noted that D3 (card consolidation) was "partially effective" — group_structure.py was consolidated, but C84 introduced new inline HTML. The grade seems to reflect the design system's quality, not its adoption. Is an A grade meaningful if developers keep bypassing the design system?

5. **The product vision's "Risks" section (line 102) lists "Scope creep" as a risk with countermeasure "Strict milestone verification enforcement." Are we enforcing this?** M5 (Adaptive updates) was the last milestone. We're now on Sprint 7, working on C84, C83, C85, and planning C98-C103. The milestones don't map to current features. M5 says "Content updated within 24 hours of a major event" — we don't have this yet. Are we verifying milestones or just sprint completions?

6. **The competitor research identified 10 competitors but the analysis is surface-level.** The QA engineer listed competitors (Luca AI, ticker.ai, Chartr, etc.) but the feature gaps are generic: "Event Interpretation," "Scrollytelling," "Natural Language Screener." These sound like features the competitors might have, not features that Stock Explorer needs. Are we doing competitor-driven development (copying) or vision-driven development (building what fits)? The product vision says "Competitor features must be filtered through historian positioning, not copied directly" (distilled lesson from Rounds 1-12). Are we following this?

**Team Response:**
- Historian alignment: The two rejected features (C100, C102) were the ones that violated historian positioning. The remaining features (C98, C99, C101, C103) are historian-aligned. The filtering is working — but it happens at the challenge stage, not at the research stage. Recommend adding a "historian filter" to the competitor research template so features are pre-filtered before reaching the backlog.
- Feature count: 103 identified features is a concern. Recommend a "Feature Triage" process (as suggested in Round 17) — every 3 rounds, review the entire backlog and explicitly defer or cancel low-priority items. The backlog should shrink over time.
- Ten-second test: Agreed — it's a good filter. The two rejected features failed it. Recommend adding the ten-second test to the competitor research template as a gating criterion.
- Design Grade A: The grade reflects the design system's quality, not its adoption. The designer acknowledges that inline HTML is a growing problem. The A grade is conditional on implementing automated enforcement (CI check for unsafe_allow_html). Without enforcement, the grade should be A- at best.
- Milestone verification: M5 (Adaptive updates) is not yet achieved. The adaptive_engine.py exists but doesn't update content within 24 hours of events. This is a gap between milestone definition and implementation. Recommend a milestone verification sprint (or adding milestone checks to sprint reviews).
- Competitor-driven vs vision-driven: The team acknowledges that competitor research is currently "feature identification" not "gap analysis." The features identified are competitor features, not necessarily Stock Explorer needs. Recommend restructuring competitor research to start from user pain points (from product vision) and check whether competitors address them, rather than starting from competitor features.

**Challenger Verdict: ⚠️ REVISED**
- **Historian alignment**: CONDITIONAL. The remaining features (C98, C99, C101, C103) pass the historian filter, but the research process needs improvement. RECOMMENDATION: Add "historian filter" and "ten-second test" to the competitor research template. Features that fail either filter should not reach the backlog.
- **Feature count**: VALID CONCERN. 103 features with ~30 implemented is a 71% backlog ratio. This is demoralizing and unmanageable. RECOMMENDATION: Implement Feature Triage (every 3 rounds) as a formal process. Target: reduce identified features to 60-70 by Sprint 10 through explicit deferrals and cancellations.
- **Design Grade A**: DOWNGRADE to A- until automated inline HTML enforcement is implemented. The design system is excellent (A), but adoption is inconsistent (B+). The composite grade should reflect both.
- **Milestone verification**: M5 is not achieved. This is a significant gap. RECOMMENDATION: Add milestone verification to the sprint review checklist. Each sprint should check: "Does this sprint advance any unachieved milestone?"
- **Competitor research quality**: The research is feature-identification, not gap-analysis. RECOMMENDATION: Restructure competitor research to start from the 5 market pain points in the product vision, then check whether competitors address each pain point. This ensures vision-driven, not competitor-driven, development.

---

### Final Challenger Decision: ⚠️ REQUIRES REVISION

**Sprint 8 Scope (REVISED — Debt-First):**
1. **D-048** — Migrate _CASE_STUDIES to YAML (P1, 1-2h) — FIRST task
2. **D6** — Complete remaining 5 YAML migrations (3-4h)
3. **D-055** — Extract inline HTML from sector_heatmap.py (2-3h)
4. **D-050** — Extract inline HTML from market_event_case_study.py (1-2h)
5. **D8** — Parallelize etf_browser.py (1-2h)
6. **D9** — Add cache to watchlist.py (1-2h)
7. **D10** — Add cache to adaptive_engine.py (1-2h)
8. **D-056** — Improve _section_title() docstring (0.1h)

**Sprint 9+ (New Features — Post-Debt):**
- C98 (Event Interpretation Engine) — P1, 14-18h — CONDITIONAL on: (a) 2h spike to validate M5 data quality, (b) product vision update to allow LLM interpretation layer, (c) all interpretations cite structured data sources
- C101 (Comprehension Check Quiz, replaces C52) — P2, 8-12h — CONFIRMED
- C103 (First Visit Gate, rename to "First Visit Guide") — P2, 10-14h — CONDITIONAL on: optional (prominent skip), completable in <3 min, no feature blocking

**Sprint 10+ (Deferred):**
- C99 (Scrollytelling) — P3, 16-22h — Defer until debt is cleared and core features are stable

**Explicitly Rejected:**
- C100 (Natural Language Screener) — REJECTED — Contradicts "historian, not stock picker" positioning
- C102 (Market Narrative Feed) — REJECTED — Market news feature, not historian feature

**Explicitly Cancelled:**
- C52 (Quiz Mode) — CANCELLED — Replaced by C101

**Structural Changes Required:**
1. **Add "historian filter" and "ten-second test" to competitor research template** — Features that fail either filter should not reach the backlog
2. **Implement Feature Triage process** — Every 3 rounds, review entire backlog and explicitly defer/cancel low-priority items. Target: reduce to 60-70 features by Sprint 10.
3. **Add automated inline HTML enforcement** — CI check that flags `unsafe_allow_html=True` in new code. Until implemented, Design Grade is A- not A.
4. **Add milestone verification to sprint review checklist** — Each sprint checks whether it advances unachieved milestones (M5 is currently not achieved).
5. **Restructure competitor research** — Start from product vision pain points, not competitor features.
6. **Update product vision** — Expand LLM scope from "plain-language translation only" to "plain-language translation and interpretation" with the constraint that all interpretations must cite structured data sources.

**Total Committed Effort:**
- Sprint 8 (Debt): 10-17h debt + 0.1h naming fix = ~10.2-17.1h
- Sprint 9: C98 spike (2h) + C98 dev (14-18h) + C101 (8-12h) + C103 (10-14h) = 34-46h
- Sprint 10+: C99 (16-22h) + remaining backlog
- **Sprint 8 is debt-first by design** — no new features until debt is cleared

**Key Metrics:**
- Features rejected: 2 (C100, C102) — both failed historian filter
- Features cancelled: 1 (C52) — replaced by C101
- Features deferred: 1 (C99) — P3, too expensive for current priority
- Features conditional: 3 (C98, C101, C103) — confirmed with conditions
- Debt items addressed: 8 (D-048, D6, D-055, D-050, D8, D9, D10, D-056)
- Structural changes required: 6

**Rationale:**
The consolidated findings revealed two critical issues: (1) Sprint 7's D6 "resolution" was overstated — only 1 of 6 blocks migrated, and C84 introduced a new 230-line violation; (2) the competitor research is producing features that don't pass the historian filter (C100, C102). The debt burden (13-21h including new debt from C84) requires a debt-first Sprint 8. The 6 new feature gaps were triaged: 2 rejected, 1 deferred, 3 confirmed with conditions. The structural changes (historian filter, feature triage, automated enforcement, milestone verification) address systemic issues that have persisted for 20 rounds.
