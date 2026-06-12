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
