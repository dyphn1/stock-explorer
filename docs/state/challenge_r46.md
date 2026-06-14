# Challenge Log — Discussion Round 46

> **Challenger**: Challenge Agent (Round 46)
> **Date**: 2026-06-15
> **Context**: Sprint 20 COMPLETE. Sprint 21 planned: C170 + C188 + D-125/126/127.
> **Features Challenged**: C199-C206 (8 features from Round 46 competitor research)
> **Team Positions**: Architect (C201 #1, C200 #2), Designer (C201 #1, C199 #2), Developer (C204+C205 #1, C202 #2)

---

## Round 1: Feature Direction Challenge

### Team Preliminary Decision

The PM consolidated the following tiered plan:

**Tier 1 — Sprint 22**: C201 "Daily Market Story" (P1, 12-18h), C204 "Confidence Indicator" (4-6h), C205 "Read Time Indicator" (3-5h)
**Tier 2 — Sprint 23**: C199 "Bear vs Bull Debate Cards" (10-14h), C200 "What If I Had Invested?" (12-16h), C202 "Story Arc Timeline Labels" (10-14h)
**Tier 3 — Sprint 24+**: C206 "Recurring Investment Education" (8-12h), C203 "Supply Chain Visual Map" (18-24h, deferred)

Key disagreements: Architect wants C200 as #2; Designer wants C199 as #2; Developer wants C202 as #2 and C204+C205 in Sprint 21.

### Challenger's Challenges

#### Challenge 1.1: C201 "Daily Market Story" — Historian Positioning or Investment Advice?

**The problem**: C201 is described as a "3-minute morning briefing" that tells users "what happened in the market today." But the "historian, not stock picker" positioning means we explain the past, not narrate the present as a guide to action. A daily market narrative — especially one that says "tech stocks rallied today because of AI demand" — is functionally indistinguishable from the morning briefings that investment banks send to clients. Finimize's product IS investment advice wrapped in friendly language. We're copying their format without their license to advise.

**Specific risks**:
- The Designer's spec says each bullet should include "plain-language cause" (e.g., "AI chip demand exceeded expectations"). Causal explanations about today's market move are inherently forward-looking — they imply the cause will continue.
- The fallback content ("market is quiet, here's what happened recently") is safer but defeats the purpose of a DAILY briefing. If the fallback triggers often, the feature becomes a generic event dashboard, not a daily story.
- The Architect's own analysis notes: "Market-level narratives can easily sound like investment advice." This is acknowledged but not resolved — the mitigation is just "3-layer tone QA."

**The challenge**: Are we building a feature that requires us to constantly police the boundary between "historian explaining yesterday" and "advisor suggesting what happens tomorrow"? That's an operational cost that the 12-18h estimate doesn't include.

#### Challenge 1.2: C201 vs Existing Event Dashboard / Story Timeline — Feature Overlap

**The problem**: The codebase already has:
- `src/pages/story_timeline.py` — a full page showing company event timelines
- `src/services/timeline_service.py` (299 lines) — composes timeline entries from events, case studies, milestones
- `src/services/market_event_service.py` — provides market-level event detection
- `src/pages/business_card/_sections/_story.py` — story sections on company pages

C201 is described as "3-4 bullet points of market events in plain language on the homepage." But `story_timeline.py` already shows events. `market_event_service.py` already detects market events. The new feature is essentially a condensed, homepage-positioned version of existing functionality.

**The challenge**: What is the user-facing difference between "Today's market story on the homepage" and "the event timeline page"? If the answer is "the homepage card is a teaser that links to the timeline," then we're building a marketing component, not a feature. If the answer is "the homepage card is a daily narrative, not just event listing," then we're back to the advice boundary problem.

#### Challenge 1.3: C200 vs Existing Historical Scenarios — Feature Overlap

**The problem**: The codebase already has:
- `src/pages/business_card/_historical_scenarios.py` (320 lines) — hardcoded scenario cards for major stocks
- `src/data/yaml/historical_scenarios.yaml` — curated scenarios for 2330, 2317, 2454, 2308

C200 is described as "interactive 'what if' calculator." But the Developer's own analysis says the upgrade path is to "add interactive calculation" to the existing `_historical_scenarios.py`. This means C200 is not a new feature — it's an enhancement to an existing feature (C74).

**The challenge**: Are we double-counting? The PM lists C200 as a new P2 feature with 12-16h of work. But the existing scenarios already serve the same educational purpose. The incremental value is the interactivity (date picker + amount input), not the concept. Should this be scoped as "enhance C74" rather than "new feature C200"?

#### Challenge 1.4: P1 Elevation of C201 — Is It Justified?

**The problem**: C201 was elevated from C196 to P1 because "daily cadence is #1 retention pattern from competitor research." But:
- The Architect rates feasibility as MEDIUM (content pipeline is the bottleneck)
- The Developer rates effort as 14-18h (revised UP from 12-16h) and warns "content curation cost may outweigh code cost"
- The Designer rates UX impact as "Very High" but acknowledges "if content is stale or generic, it damages credibility"
- All three roles acknowledge that template-based explanations will produce formulaic, uncompelling narratives

**The challenge**: The P1 label means C201 should be the highest-value, lowest-risk feature. But it's actually the highest-risk feature in the set. The #1 retention pattern from competitors is based on competitors who have DEDICATION content teams (Finimize employs writers) or AI models (Robinhood has ML pipelines). We have templates. Are we elevating a feature based on competitor outcomes we can't replicate with our current infrastructure?

#### Challenge 1.5: Competitor Implementation — Are We Copying or Differentiating?

**The problem**: The team cites Finimize and Robinhood as C201's inspiration. But:
- Finimize: Professional editorial team writes every daily briefing. Human-curated, 15+ journalists.
- Robinhood: ML-driven narrative generation with real-time data feeds. Dedicated data engineering team.
- StockStory: Has "Story Arcs" (C202) — a more structured, less risky approach to the same concept.
- Magnify.money: Has "What If" calculator (C200) — simpler, proven, no daily cadence risk.

**The challenge**: We're taking the surface-level feature (daily briefing) from competitors who have fundamentally different content infrastructure. Meanwhile, StockStory's approach (C202 Story Arcs) is actually MORE aligned with our historian positioning and has lower content risk. Are we choosing C201 because it's the best fit for our product, or because it's the most visible competitor feature?

### Team Responses

#### Response 1.1: Historian Positioning — "Yesterday's News, Not Tomorrow's Advice"

The Architect and Designer jointly respond:

**Acknowledged**: The advice boundary is real. C201 must be explicitly framed as "yesterday's news" not "today's action items."

**Resolution**:
- C201 content will be explicitly PAST-TENSE: "昨日市場重點" (yesterday's market highlights), not "today's market story"
- All bullets will describe what ALREADY HAPPENED with closed-outcomes: "台積電昨日漲 2%，因為 AI 晶片需求超乎預期" — this is a historical fact, not a prediction
- The word "故事" (story) will be reconsidered — "今日市場動態" (today's market dynamics) may be more accurate and less narrative-driven
- The 3-layer tone QA will include a specific "advice boundary check": no forward-looking verbs, no implied action, no causal language that extends beyond the reported date
- Weekend/holiday fallback will use historical education content (tying to C206), not generic event summaries

**Verdict**: The historian positioning is maintained by making C201 explicitly retrospective. The feature is "what happened yesterday" not "what to do today."

#### Response 1.2: Feature Overlap — C201 vs Event Dashboard

The Developer responds:

**Acknowledged**: There IS overlap with `story_timeline.py` and `market_event_service.py`.

**Resolution**:
- C201 is a HOMEPAGE CARD, not a page. It's a 4-bullet summary that appears BEFORE the user searches for a stock. The event timeline is a DEEP-DIVE PAGE that users navigate to.
- The distinction: C201 = "here's what you need to know" (passive, scannable, 10 seconds). Event timeline = "here's the full story" (active, explorable, 5 minutes).
- Implementation will reuse `market_event_service.py` for data but add a new `morning_briefing.py` service that condenses and formats for the homepage card.
- The existing `story_timeline.py` page remains unchanged. C201 is a new entry point, not a replacement.

**Verdict**: Overlap acknowledged but resolved — different user contexts (homepage glance vs deep dive). The data layer is shared; the presentation layer is new.

#### Response 1.3: C200 vs Existing Historical Scenarios

The Architect responds:

**Acknowledged**: C200 builds on existing `_historical_scenarios.py` (C74).

**Resolution**:
- C200 is scoped as "interactive enhancement to C74" not "new feature from scratch"
- The 12-16h estimate already reflects this: the Developer's analysis shows the existing 320-line file with 4 stock scenarios is the foundation
- The incremental value is significant: going from 4 hardcoded scenarios for 4 stocks to an interactive calculator for ALL stocks
- The PM will update the issues file to note C200 = "C74 interactive upgrade"
- This is NOT double-counting — it's a feature enhancement with clear incremental scope

**Verdict**: Acknowledged and resolved. C200 is an enhancement, not a new feature. The 12-16h estimate is for the interactive layer only.

#### Response 1.4: P1 Elevation — Justified with Conditions

The PM responds:

**Partially acknowledged**: The P1 elevation carries real risk. But the retention argument is strong.

**Resolution**:
- C201 remains P1 but with a **phased delivery plan**:
  - **Sprint 22 MVP**: Template-based, on-demand generation (user opens homepage → fetches data → generates story). No daily caching pipeline. Content quality is "good enough" with templates.
  - **Sprint 23+ Enhancement**: If MVP proves valuable, add daily caching pipeline and richer templates.
  - **Sprint 24+ Future**: If LLM layer gets real implementation, upgrade to AI-generated narratives.
- The 12-16h estimate is for the MVP only. The daily caching pipeline (3-4h) is deferred to Sprint 23.
- Success metric: If C201 doesn't improve 7-day retention by Sprint 23 review, it gets deprioritized.

**Verdict**: P1 maintained but with explicit MVP scope and success criteria. The team accepts the risk but has a kill switch.

#### Response 1.5: Competitor Differentiation — We're Adopting, Not Copying

The Designer responds:

**Acknowledged**: We don't have Finimize's editorial team or Robinhood's ML pipeline.

**Resolution**:
- Our differentiation is NOT the content quality — it's the HISTORIAN FRAMING. Finimize tells you what to think; we teach you how to think about what happened.
- The confidence indicator (C204) will be integrated into C201 bullets, adding a layer no competitor has: "台積電昨日漲 2% 🟢" — teaching users to evaluate data quality even in a briefing context.
- The read time indicator (C205) will be on the C201 card: "⏱ 閱讀時間 2 分鐘" — respecting the user's time, which is a beginner-friendly differentiator.
- StockStory's Story Arcs (C202) are indeed a good fit and are included in Sprint 23. We're not choosing C201 OVER C202 — we're doing BOTH, sequenced by effort and impact.

**Verdict**: The team acknowledges the infrastructure gap but believes the historian framing + C204/C205 bundling creates a differentiated experience even with template-based content.

---

## Round 2: Priority Challenge

### Team Preliminary Decision

Priority order: C201 (P1) → C204+C205 (Sprint 22) → C199/C200/C202 (Sprint 23) → C206/C203 (Sprint 24+)

### Challenger's Challenges

#### Challenge 2.1: C204+C205 Should Be Sprint 21 Stretch Goals, Not Sprint 22

**The problem**: The Developer explicitly recommends C204+C205 as Sprint 21 stretch goals. The analysis is compelling:
- C204: 4-6h, no dependencies, improves ALL existing explanations
- C205: 3-5h, no dependencies, improves ALL existing content
- Combined: 7-11h, zero dependencies, presentation-layer only
- Both features touch `_router_base.py` and section files — they're naturally bundled

The PM consolidated them into Sprint 22, but the Developer's reasoning for Sprint 21 is strong: these are quick wins that improve the entire app immediately. Every Sprint 21 feature (C170 glossary, C188 "Why Did This Move?") would benefit from C204+C205 being present.

**The challenge**: Why delay 7-11h of high-impact, zero-dependency work by one sprint? The opportunity cost is that Sprint 21 features launch without confidence indicators and read time estimates, making them feel less polished. If Sprint 21 has ANY slack (and the 27.5-40.5h estimate has a 13h range), C204+C205 should be stretch goals.

#### Challenge 2.2: C199 (Debate Cards) vs C202 (Story Arcs) — Is the Priority Order Correct?

**The problem**: The Designer wants C199 as the #2 pick (after C201). The Developer wants C202. The PM put both in Sprint 23 without internal ordering. But consider:

| Feature | Effort | Differentiation | Risk | Historian Alignment |
|---------|--------|-----------------|------|-------------------|
| C199 Debate Cards | 10-14h | High (no TW competitor) | Medium (false balance risk) | ⚠️ (borderline advisory) |
| C202 Story Arcs | 10-14h | Very High (no competitor has auto-detected arcs) | Low (heuristic, data-driven) | ✅ (core historian identity) |

C202 has:
- Same effort as C199
- HIGHER differentiation (no competitor has auto-detected narrative arcs)
- LOWER risk (heuristic-based, no false-balance problem)
- BETTER historian alignment (narrative arcs are inherently historical)

**The challenge**: Why is C199 listed before C202 in Sprint 23? The Designer's argument is "visual impact for demos," but that's a stakeholder management concern, not a user value concern. If we're prioritizing by user value and product alignment, C202 should be before C199.

#### Challenge 2.3: C200 (What If) — Should It Be Deferred Given Existing Infrastructure?

**The problem**: C200 builds on existing `_historical_scenarios.py` (C74). The Developer's analysis shows:
- 320 lines of existing scenario code
- 4 stocks with curated scenarios in YAML
- The upgrade path is to add interactive calculation to this existing feature

The Architect wants C200 as #2 priority. But consider: the existing scenarios already serve the educational purpose. The interactive calculator is a nice-to-have enhancement, not a new capability. Meanwhile:
- C202 (Story Arcs) is a genuinely NEW capability — no existing equivalent
- C199 (Debate Cards) is a genuinely NEW capability — no existing equivalent
- C200 is an ENHANCEMENT to an existing feature

**The challenge**: Should an enhancement to an existing feature (C200) be prioritized over genuinely new capabilities (C202, C199)? The PM's Sprint 23 has all three, but if we can only pick two due to capacity, shouldn't C200 be the one that waits?

#### Challenge 2.4: The Sprint 23 Triple Booking Problem

**The problem**: Sprint 23 contains C199 (10-14h) + C200 (12-16h) + C202 (10-14h) = 32-44h of work. Sprint 21 is 27.5-40.5h. If Sprint 21 took 5-8 weeks, Sprint 23 at 32-44h would take a similar duration.

But the Developer's recommended order puts C204+C205 FIRST (7-11h), then C202 (10-14h), then C199 (10-14h), then C200 (12-16h). The Developer's total for the top 4 is 39-55h — nearly 2 sprints worth.

**The challenge**: The PM's Sprint 23 is overloaded. Three features with 32-44h total is optimistic given the team's velocity. Which feature gets cut if capacity is constrained? The PM hasn't specified a Sprint 23 priority order, which means all three are equal — and equal priority means no priority.

### Team Responses

#### Response 2.1: C204+C205 — Accepted as Sprint 21 Stretch Goals

The PM responds:

**Accepted**: C204+C205 will be added to Sprint 21 as stretch goals.

**Resolution**:
- Sprint 21 core remains: C170 + C188 + D-125/126/127 (27.5-40.5h)
- Sprint 21 stretch: C204 (4-6h) + C205 (3-5h) = 7-11h
- If Sprint 21 core finishes early, C204+C205 start immediately
- If Sprint 21 core takes full time, C204+C205 move to Sprint 22 Day 1 (before C201 starts)
- This gives the best of both worlds: quick wins if capacity exists, no delay if it doesn't

**Verdict**: The Challenger's argument is accepted. C204+C205 are Sprint 21 stretch goals with Sprint 22 fallback.

#### Response 2.2: C202 Before C199 — Accepted with Rationale

The Designer responds:

**Partially accepted**: C202 will be prioritized before C199 within Sprint 23.

**Resolution**:
- Sprint 23 order: C202 (Story Arcs) → C199 (Debate Cards) → C200 (What If)
- Rationale: C202 is lower risk, higher differentiation, and better historian alignment. It should be built first to validate the narrative infrastructure that C199 can then leverage.
- C199's "visual impact for demos" argument is noted but is a stakeholder concern, not a user value concern. The team will find other ways to create demo moments.
- If C202 and C199 are both completed, they form a powerful "narrative + debate" duo that's unique in the market.

**Verdict**: C202 > C199 priority accepted. Sprint 23 internal order: C202 → C199 → C200.

#### Response 2.3: C200 — Kept in Sprint 23, But Last

The Architect responds:

**Partially accepted**: C200 stays in Sprint 23 but is last in priority.

**Resolution**:
- C200 is an enhancement to existing infrastructure (C74), not a new feature. This is acknowledged.
- However, the interactive calculator has PROVEN engagement value from competitor research (Magnify.money, StockStory). It's a safe bet.
- The 12-16h estimate is for the interactive layer only — the foundation already exists.
- C200 will be the LAST feature in Sprint 23, after C202 and C199. If capacity runs out, C200 is the one that moves to Sprint 24.
- This ordering (C202 → C199 → C200) also makes technical sense: C202's narrative infrastructure (arc detection, timeline enhancement) could inform C200's scenario presentation.

**Verdict**: C200 kept but deprioritized within Sprint 23. It's the "if we have time" feature.

#### Response 2.4: Sprint 23 Capacity — Explicit Priority Order Established

The PM responds:

**Acknowledged**: Sprint 23 was overloaded with three features and no internal priority.

**Resolution**:
- Sprint 23 priority order: C202 (10-14h) → C199 (10-14h) → C200 (12-16h)
- If capacity is constrained: C202 is MUST, C199 is SHOULD, C200 is COULD (MoSCoW)
- Sprint 24 absorbs any overflow: C206 (8-12h) + deferred C200 if needed
- Total Sprint 23 target: 20-28h (C202 + C199), with C200 as stretch

**Verdict**: Explicit priority order established. The MoSCoW framework prevents the "all equal" problem.

---

## Round 3: Goal Alignment Challenge

### Team Preliminary Decision (Updated After Rounds 1-2)

**Sprint 21**: C170 + C188 + D-125/126/127 + **C204+C205 stretch goals**
**Sprint 22**: C201 "Daily Market Story" (P1, MVP scope)
**Sprint 23**: C202 → C199 → C200 (MoSCoW priority)
**Sprint 24+**: C206, C203 (deferred)

### Challenger's Challenges

#### Challenge 3.1: Do These Features Collectively Move Stock Explorer Toward the Product Vision?

**The problem**: Stock Explorer's product vision is "historian, not stock picker" — teaching beginners to understand stocks through historical context, plain-language explanations, and structured narratives.

Let's audit each feature against this vision:

| Feature | Vision Alignment | Concern |
|---------|-----------------|---------|
| C201 Daily Briefing | ⚠️ Medium | Daily cadence creates pressure to be "fresh" which pushes toward advice territory |
| C204 Confidence Indicator | ✅ High | Teaches critical thinking — core historian value |
| C205 Read Time | ✅ Medium | Respects user's time — beginner-friendly |
| C199 Debate Cards | ⚠️ Medium | Balanced arguments are educational but could imply "both sides are equal" |
| C200 What If Calculator | ✅ High | Historical, educational, non-advisory |
| C202 Story Arcs | ✅ Very High | Core historian identity — narrative structure from historical data |
| C206 Recurring Investment | ⚠️ Medium | Educational but close to advisory boundary |
| C203 Supply Chain Map | ✅ Medium | Historical relationships, but low priority |

**The observation**: The features with the HIGHEST vision alignment (C202, C204, C200) are not the highest priority. C201, the P1 feature, has the LOWEST vision alignment. This is a structural tension in the plan.

**The challenge**: Is the priority order driven by product vision or by competitor FOMO? If it's vision-driven, C202 should be P1. If it's competitor-driven, C201 makes sense but needs stronger vision alignment.

#### Challenge 3.2: Contradictions Between Recommended Features

**The problem**: There are subtle contradictions:

1. **C201 vs C202 — Both tell stories, but differently**: C201 tells a DAILY market-level story. C202 tells a COMPANY-LEVEL historical narrative. If both exist, users may be confused by two "story" features at different scopes. The naming is also similar ("Daily Market Story" vs "Story Arc Timeline").

2. **C204 on C201 — Confidence on template content**: C204 adds confidence indicators to all explanations. But C201's explanations are template-based with confidence scores that are synthetic (based on template match quality, not data quality). Showing 🟢 on a template-generated daily briefing is misleading — it says "high confidence" when it really means "template matched." This undermines C204's credibility.

3. **C205 Read Time on C201 — Circular dependency**: C205 adds read time to all content. C201 already shows "⏱ 閱讀時間 2 分鐘" in the Designer's spec. If C205 is also applied, we'd have double read-time indicators on the same card.

**The challenge**: These features were designed independently. When combined, they create naming confusion, confidence score inflation, and UI redundancy. Has anyone done a combined UX review?

#### Challenge 3.3: Overlooked Risks

**Regulatory Risk**:
- C201 (daily market narrative) + C206 (recurring investment education) + C200 (what-if returns) = a suite of features that, taken together, could be construed as an "investment advisory service" under Taiwanese financial regulations
- Even with individual disclaimers, the AGGREGATE impression of a daily briefing + investment calculator + recurring investment education is "this app tells me how to invest"
- **No regulatory review is planned** in the current roadmap

**Technical Risk**:
- C201's performance risk is real: the Developer warns "if event detection is slow (>1s), it blocks the entire page"
- The homepage is the FIRST thing users see. A slow-loading daily briefing card delays the entire app experience
- No performance budget or timeout mechanism is specified for C201

**UX Risk**:
- C201 adds homepage real estate. The homepage already has: search bar, beginner mode toggle, navigation. Adding a briefing card pushes search below the fold on mobile
- The Designer's spec shows the card appearing BEFORE the search bar. This is a significant homepage redesign that hasn't been tested with users

**Content Risk**:
- C201's template-only content will be formulaic. The Architect acknowledges this. But the PM's success metric is 7-day retention. If the daily content is boring, it won't drive retention — it'll become noise that users ignore
- The fallback content ("market is quiet") will trigger on weekends, holidays, and low-volatility days — potentially 30-40% of the time. That's a lot of fallback content needed

### Team Responses

#### Response 3.1: Vision Alignment — C201's Role Reconsidered

The PM responds:

**Acknowledged**: The tension between vision alignment and priority is real.

**Resolution**:
- C201's P1 status is RETAINED but reframed. It's not the highest vision alignment feature — it's the highest GROWTH potential feature. The distinction matters:
  - **Vision alignment** = how well the feature embodies "historian, not stock picker"
  - **Growth potential** = how much the feature drives retention and daily engagement
- C201 is P1 for growth, not for vision. C202 is P1 for vision alignment. Both are important.
- The team explicitly accepts that C201 carries vision alignment risk and mitigates it through:
  - Retrospective framing ("yesterday's news")
  - C204 confidence indicators (teaches critical thinking)
  - Strict tone QA
  - Kill switch if retention doesn't improve
- C202 (highest vision alignment) is Sprint 23 #1 priority, ensuring vision-aligned features are not starved

**Verdict**: The dual-axis framework (vision vs growth) is accepted. C201 is P1 for growth, C202 is P1 for vision. Both get priority in their respective dimensions.

#### Response 3.2: Feature Contradictions — Resolved Through Integration

The Designer responds:

**Acknowledged**: The contradictions are real and need resolution.

**Resolution**:

1. **C201 vs C202 naming**: Rename C201 to "今日市場動態" (Today's Market Dynamics) to avoid the "story" naming collision with C202 Story Arcs. C201 = market-level daily briefing. C202 = company-level historical narrative. Different scopes, different names.

2. **C204 on C201**: C204 confidence indicators will NOT be applied to C201 bullets in the MVP. C201's content is template-generated market summaries, not analytical explanations. Applying confidence indicators to market summaries would be misleading. C204 will be applied to company-level analytical explanations only (business card sections, financial health, etc.). This will be revisited when C201 gets real LLM-generated content.

3. **C205 on C201**: C205 read time indicators will NOT be double-applied. C201's card already includes "⏱ 閱讀時間 X 分鐘" as part of its design. C205 will be applied to all OTHER content sections. The C201 card is exempt from C205 to avoid redundancy.

**Verdict**: All three contradictions resolved through explicit scoping decisions. The Designer will update the design spec to reflect these boundaries.

#### Response 3.3: Overlooked Risks — Mitigation Plan

The Architect and PM jointly respond:

**Regulatory Risk**:
- Acknowledged. The team will add a "regulatory review gate" before Sprint 22 starts.
- All features with investment-adjacent content (C201, C200, C206) will be reviewed by a compliance advisor.
- The review will focus on the AGGREGATE impression, not just individual disclaimers.
- If regulatory concerns are raised, C206 (recurring investment education) will be deferred until legal review is complete.
- C201 and C200 are lower risk because they are explicitly retrospective and educational.

**Technical Risk (C201 Performance)**:
- C201 will implement a **2-second timeout**: if data fetching + narrative generation takes >2s, the card is not shown. The user sees the homepage without the briefing card.
- The card will use `st.cache_data(ttl=3600)` to cache the daily briefing for 1 hour.
- A loading skeleton (not a blocking spinner) will be shown during fetch.
- Performance test: C201 card must render in <2s on 3G network simulation before Sprint 22 ships.

**UX Risk (Homepage Real Estate)**:
- The Designer will conduct a quick mobile viewport test: does the C201 card push search below the fold on iPhone SE (smallest common TW device)?
- If yes, the card will be moved BELOW the search bar on mobile, or collapsed by default.
- Desktop layout remains as designed (card above search).

**Content Risk (Template Quality)**:
- The PM will commission 2 weeks of daily briefing content templates in advance (14 days × 4 bullets = 56 bullet templates).
- These templates will cover common market scenarios: single stock move, sector rotation, market-wide movement, geopolitical event, earnings season, quiet day.
- The fallback content library will have 10 pre-written educational snippets for quiet days.
- Content quality will be reviewed weekly during Sprint 22, with template adjustments as needed.

**Verdict**: All four risk categories acknowledged with specific mitigations. The regulatory review gate is the most important addition — it was completely missing from the original plan.

---

## Final Verdict

### ✅ ALIGNED — With 3 Conditions

After 3 rounds of challenge, the team's plan is **aligned** with the product vision and technically sound. The challenges surfaced real issues that were resolved through constructive dialogue.

### Resolved Decisions

1. **C201 "Daily Market Story"** — P1 for GROWTH (not vision). Reframed as retrospective "yesterday's market dynamics." Phased delivery: MVP in Sprint 22, enhancement in Sprint 23+. Kill switch if retention doesn't improve. Renamed to "今日市場動態" to avoid naming collision with C202.

2. **C204+C205** — Sprint 21 stretch goals (not Sprint 22). If Sprint 21 core finishes early, these start immediately. If not, they move to Sprint 22 Day 1.

3. **Sprint 23 Priority** — Explicit MoSCoW order: C202 (MUST) → C199 (SHOULD) → C00 (COULD). C202 is the highest vision-alignment feature and gets priority.

4. **C200** — Acknowledged as C74 enhancement, not new feature. Last in Sprint 23 priority. Moves to Sprint 24 if capacity constrained.

5. **Feature Boundaries** — C204 confidence indicators NOT applied to C201 bullets (template content). C205 read time NOT double-applied to C201 card. Clear scoping prevents UI redundancy.

### 3 Conditions (Must Be Met Before Sprint 22)

| Condition | Owner | Deadline |
|-----------|-------|----------|
| **Regulatory review gate**: Compliance review of C201 + C200 + C206 aggregate impression | PM + External advisor | Before Sprint 22 kickoff |
| **C201 performance budget**: 2-second timeout + cache strategy + mobile viewport test | Developer + Designer | During Sprint 22 development |
| **C201 content preparation**: 14-day template library + 10 fallback educational snippets | PM + Content | Before Sprint 22 content freeze |

### Remaining Tensions (Monitored, Not Blocking)

1. **Vision vs Growth tension**: C201 is P1 for growth but has lower vision alignment. The team accepts this tradeoff with explicit kill-switch criteria.

2. **Template quality ceiling**: C201's content will be formulaic with templates. The team accepts this for MVP with a plan to enhance when LLM infrastructure matures.

3. **Sprint 23 capacity**: 32-44h of work in one sprint is ambitious. The MoSCoW priority ensures the most important features ship first.

---

*Challenge completed: 2026-06-15*
*Challenger: Challenge Agent*
*Next review: Sprint 22 kickoff (pending regulatory review gate)*
