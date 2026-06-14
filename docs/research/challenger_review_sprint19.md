# 🔥 Three-Round Challenge — Sprint 19 Planning

> **Role**: Challenger
> **Date**: 2026-06-14
> **Sprint**: Sprint 19 (follows Sprint 18 ✅ COMPLETE — 27.6h actual vs 24-32h estimate)
> **Team Proposal**: Direction A "Pattern-First" — C147 + C140, C152 Deferred

---

## Round 1: Feature Direction Challenge

### Challenger Questions

**Q1: Is deferring C152 the right call? What is the opportunity cost?**

The team proposes a 2-4h spike for C152 in Sprint 19 with full implementation deferred to Sprint 20. Let me push back:

- **C152 is P1** — same priority as C147. The architect's analysis shows C152 has the highest architectural complexity but also the highest user value ("transforms Stock Explorer from data display to historian that tells stories"). The designer rates it 8/10 UX impact.
- **C152's full implementation in Sprint 20 is not guaranteed.** Sprint 20 already has C142 (Glossary Gate, 8-12h) and C146 (Emoji Sentiment, 3-5h) in the pipeline. At 22-29h for C152 alone, adding it to Sprint 20 would create a 33-46h sprint — matching Sprint 19's current load. The team is effectively betting that C152's design spike will reduce implementation risk. But the spike itself (2-4h in Sprint 19, plus the Sprint 20 implementation) splits the work across two sprints, adding context-switching overhead.
- **The architect identified a soft dependency**: C152 can link to C147's `HistoricalPattern` data for historical parallels. If C152 is deferred, Sprint 20 gets the benefit of C147's infrastructure. But this is a *soft* dependency — C152 can function without C147 patterns.
- **Real question**: If C152 is the most differentiating feature ("no competitor combines historical pattern matching + multi-factor narratives + curated case studies"), why deliver it last rather than first?

**My assessment**: Deferring C152 is defensible but costly. The 2h feasibility spike for C147 already answers the key data-mapping question. A 4-6h design spike for C152 (as the developer recommends) would cost more than the team budgets. The "spike only" approach risks producing design artifacts that gather dust — knowledge decay between Sprint 19 and Sprint 20 is real. A full C152 design doc (2h) that captures the key decisions would be more valuable than a shallow spike.

**Q2: Is the C147 feasibility spike sufficient at 2h?**

The developer says *"2h is sufficient, barely."* This is the minimum viable spike, and it carries real risk:

- The spike must validate whether `case_studies.yaml` scenarios map to `adaptive_engine.py` event types. The existing 5 case studies have NO event-type field. The spike must determine whether to: (a) add an `event_types` field, or (b) create a separate `historical_patterns.yaml`.
- If option (b) is chosen, the 2h spike is enough to identify this but NOT enough to create the mapping. The content creation estimate (3-4h) assumes the mapping approach is already decided. If the spike reveals a mismatch, the team needs a new YAML file *and* new content — potentially adding 3-5h that aren't budgeted.
- The architect's critical success factor: *"If the spike reveals that case studies don't map cleanly to event types, Direction C should be used instead."* But Direction C (Content Foundation) defers both C147 full AND C152 — a massive scope reduction. The team hasn't planned for this contingency.

**My assessment**: 2h is the right spike budget, BUT the team needs a pre-defined decision tree for the spike outcome: (a) mapping succeeds → proceed with C147, (b) mapping partially succeeds → reduce C147 scope to top 5 event types, (c) mapping fails → fall back to Direction C and re-plan the sprint mid-sprint. Without this decision tree, the spike becomes an inconclusive exploration.

**Q3: Are there alternative directions the team hasn't considered?**

The architect proposed three directions (A, B, C). The team chose Direction A. But there's a **Direction D** that wasn't analyzed:

**Direction D: "Narrative Core First" — C152 full + C147 spike, C140 deferred to Sprint 20.**
- C140 (Case Study Library) is the *least* UX-impactful feature (7/10) and is primarily a content creation task. It doesn't depend on C147 or C152 architecturally.
- C152 is the *most* differentiating P1 feature. Getting it done in Sprint 19 means Sprint 20 can focus on C140 + C142 + C146.
- C140's content creation can happen as background work during Sprint 19 (pre-writing case studies) without the UI implementation.
- Cost: C152 (22-29h) + C147 spike+impl (17-22h) = 39-51h. This is tighter but achievable, especially since content creation runs in parallel.

**My assessment**: Direction D wasn't even considered. It's riskier (C152 is the hardest feature) but delivers the highest-value feature first. The team should at least explain why C152-in-Sprint-19 was rejected.

**Q4: How do competitors handle historical patterns and multi-factor narratives?**

The designer's competitor analysis is thorough but there's a critical gap:

- **Quiver Quantitative** shows historical trade patterns (averages, not ranges). Stock Explorer's range-of-outcomes display is the right differentiator — BUT Quiver's approach is data-driven (real trade data), while Stock Explorer's is content-curated (YAML). This means the quality ceiling is determined by content creation, not data pipeline. Is the team confident that 10-15 manually-written case studies can match the breadth of Quiver's data-driven approach?
- **Public.com** has story cards that combine factors, but uses editorial curation, not template generation. Stock Explorer's template-based narrative generation (C152) is more scalable but also more prone to sounding generic. Has the team tested template output quality?
- **None of the competitors combine all three features** (patterns + narratives + case library). This is Stock Explorer's white space. But delivering them across three sprints (C147 in S19, C152 in S20, C140 shared) means the "complete" narrative experience doesn't exist until Sprint 20+. Is that acceptable from a product positioning standpoint?

### Team Response Assessment

The PM formed Direction A based on:
1. Shared data source (C140 + C147 both use `case_studies.yaml`) — elegant but creates a bottleneck.
2. C152 deferral reduces risk — true, but delays the highest-impact feature.
3. 33-46h fits the sprint budget — but this assumes the C147 spike succeeds.

**My assessment**: Direction A is a safe, reasonable choice. But "safe" isn't always "right." The team has optimized for risk minimization over value maximization. Given that Sprint 18 came in at 27.6h (mid-range of estimate), the team is capable of handling more than 33-46h of work — especially with content creation running in parallel.

### Round 1 Verdict

**⚠️ CONDITIONAL PASS** — C147's feasibility spike must have a pre-defined decision tree (success/partial/failure). C152 deferral is acceptable only if the spike produces a complete design doc (not just notes). Direction D (Narrative Core First) needs explicit rejection reasoning or consideration.

---

## Round 2: Priority Challenge

### Challenger Questions

**Q1: Is the execution order correct?**

The proposed order: C147 spike → C140 dev (parallel) → C147 dev → C152 spike → testing.

Let me unpack this:

- **C147 spike (Day 1, 2h)** → Sequential blocker. Nothing else depends on C147 dev start except C147 dev itself.
- **C140 dev (parallel with spike, Day 1-5)** → C140 is independent and can start immediately. Good. But C140 content creation (6-10h) is the bottleneck — it's a designer/PM task, not a developer task. The dev can build the service & page (8-11h) but then waits for content.
- **C147 dev (Day 2-5)** → Starts after spike confirms approach. Uses the same `case_studies.yaml` that C140 is extending. If C140's schema extension (adding `category`/`tags`) isn't done first, C147's pattern matching may not benefit from the enriched schema. This is a **soft dependency the team hasn't acknowledged**: C140's schema extension should happen BEFORE C147's service implementation, or at minimum, both teams must coordinate on the YAML schema.
- **C152 spike (Day 4-5)** → Late in the sprint. If the spike reveals blockers, there's no time to adjust. The C152 spike should happen in parallel with the C147 spike on Day 1, not after C147 dev.
- **Testing (Day 6-7)** → Adequate if everything goes to plan. But there's no buffer for the C147 spike failure or C152 spike issues.

**My assessment**: The execution order is **back-loaded with risk**. The C152 spike happens too late. The C140/C147 YAML schema coordination is unaddressed. Testing has no buffer.

**Proposed revised order**:
1. **Day 1 (AM)**: C147 spike (2h) + C152 spike (2h of 4-6h, can start in parallel)
2. **Day 1 (PM)**: C140 schema extension + service begins
3. **Day 2-3**: C140 page dev + C147 service dev (parallel) + C152 spike completes
4. **Day 4-5**: C147 page integration + C152 spike results → decision on C152 approach
5. **Day 6-7**: Testing, tone QA, content cross-linking
6. **Content (parallel throughout)**: C140 case studies (PM/Designer), C147 patterns YAML, C152 narrative templates

**Q2: Should C140 come before C147 (content foundation first)?**

The architect's Direction A recommends: *"C140's `case_study_library.py` service is built first, extending `case_studies.yaml` with category/tags. C147's `historical_pattern_service.py` is built as a thin layer on top of the case study library."*

But the execution order lists them in parallel! If C140's schema extension isn't done first, C147's pattern service may need to be rebuilt when the schema changes. This is a classic coordination failure waiting to happen.

Additionally, the developer notes that `timeline_service.py` imports a non-existent `market_event_service.py` (silent failure). Neither C147 nor C140 should depend on this broken import path. But if the team is building new services that reuse patterns from `timeline_service.py`, they may inadvertently inherit this dead code path.

**My assessment**: C140's schema extension MUST be a hard prerequisite for C147's service implementation. The execution order must reflect this.

**Q3: Is the 33-46h estimate realistic?**

Let's check the math against Sprint 18 actuals:

| Item | Estimated | Actual (Sprint 18 comparable) |
|------|-----------|-------------------------------|
| C147 service (6-8h) + page (4-5h) + content (3-4h) + testing (2-3h) | 15-20h (not counting spike) | — |
| C140 service (3-4h) + page (5-7h) + content (6-10h) + testing (2-3h) | 16-24h | — |
| C152 spike | 2-4h | — |
| Tone QA YAML fix | 0.5h | — |
| **Total (Dev only)** | **~24-35h** | **Sprint 18 actual: 27.6h** |
| **Total (Dev + Content)** | **33-46h** | — |

Key observations:
- Sprint 18 actual was 27.6h (dev only, no major content creation). Sprint 19 adds content creation work (6-10h for C140 case studies + 3-4h for C147 patterns = 9-14h content). This content work should be done by PM/Designer, NOT the developer. If the developer is the only person working, this is a 55-75h sprint — not 33-46h.
- The 33-46h estimate assumes PM/Designer handles all content creation. Is this realistic? Sprint 18 had no comparable content creation work. The team hasn't demonstrated that PM/Designer can deliver 9-14h of content in parallel with dev work.
- The developer's "risk adjustment" adds +3-5h, bringing the realistic range to 36-51h. This doesn't account for the C147 spike failure contingency or the C152 spike overrun.

**My assessment**: The estimate is **optimistic but achievable IF**:
1. PM/Designer delivers content on time (this is the biggest risk)
2. C147 spike succeeds (or the team quickly falls back to Direction C)
3. No major tone QA failures in new content requiring rewrites

**Q4: What happens if the C147 spike fails?**

The architect's critical success factor states: *"If the spike reveals that case studies don't map cleanly to event types, Direction C should be used instead."*

Direction C defers both C147 full and C152, keeping only C140 content creation and a minimal C147 spike version. This would reduce Sprint 19 to:
- C140 full (16-24h including content)
- C147 spike only (2h)
- C152 deferred entirely
- Total: 18-26h

This is a **massive scope reduction** — roughly half the planned work. The team would need to fill Sprint 19 with something else or accept a lighter sprint. There's no "partial C147" contingency plan — only "full C147" or "no C147."

**My assessment**: The missing contingency is "partial C147." If the spike reveals that only some event types map cleanly, the team should implement C147 for those event types only, reducing scope without abandoning the feature. This is not addressed in the plan.

### Team Response Assessment

The PM coordinated a reasonable execution plan, but:
1. C152 spike timing is wrong — must be Day 1 parallel with C147 spike
2. C140→C147 schema dependency is unaddressed
3. Content creation timeline commitment from PM/Designer is unverified
4. No partial-C147 contingency plan

### Round 2 Verdict

**⚠️ CONDITIONAL PASS** — C152 spike must move to Day 1 (parallel with C147 spike). C140 schema extension must be C147 service's hard prerequisite. PM/Designer must confirm content creation timeline commitment. Partial C147 contingency must be added.

---

## Round 3: Goal Alignment Challenge

### Challenger Questions

**Q1: Does this plan align with the "historian, not stock picker" positioning?**

Product vision states: *"Do not say buy or sell; only explain what has happened to the company over time."* All three features are strongly aligned — they're the deepest execution of the historian positioning to date.

But there's a **critical escalation in advice-perception risk**:

- C147 shows historical patterns with specific outcome ranges. *"3 of 5 cases showed +5% to +15% in 1 month"* — this IS a historian framing, but it's dangerously close to implying prediction. The designer's mitigation (mandatory disclaimer + range display + past tense) is correct, but is it sufficient?
- C152 synthesizes multiple factors into a narrative. A narrative that says "revenue up + institutional buying + new product launch" inherently *feels* like a bullish thesis, even with historian framing. The designer's mitigation (historian framing sentence, factual past tense) may not be enough.
- C140's "啟示" (lessons) section is the highest-risk content. Without careful framing, lesson-learned becomes investment advice. The designer's gate (可以觀察到 framing) is correct but has not been tested against real content.

**Key concern**: Sprint 18's tone QA only scans `.py` files via AST. Sprint 19 adds THREE new YAML files (`historical_patterns.yaml`, `narrative_templates.yaml`, extended `case_studies.yaml`) that are loaded at runtime and NOT scanned by the existing tone QA. The team adds 0.5h for "YAML content scanning to test_tone_qa.py" — but this is described as a gap in the *current* test, not as a comprehensive addition for Sprint 19's new content.

**My assessment**: The 0.5h allocation is **grossly insufficient** for what's needed. Adding YAML scanning to `test_tone_qa.py` is a code change to the test infrastructure. But the bigger issue is that all new YAML content (case studies, patterns, narrative templates) must pass tone QA BEFORE being committed — not just before merge. This requires a pre-commit or CI check that scans YAML. The 0.5h budget only adds a YAML scanner to the existing test — it doesn't cover:

1. Extending blocklist for Sprint 19-specific risk phrases (設計師identified 12 new phrases like "通常會," "往往會," "預期")
2. Creating a YAML tone scanner that covers `src/data/*.yaml` files
3. Tone auditing all new content before it's committed
4. Expanding the excluded-files list for new modules

Realistic estimate for comprehensive tone QA coverage for Sprint 19: **2-3h**, not 0.5h.

**Q2: Are the tone QA safeguards sufficient for the new content types?**

From the designer:
- C147 needs expanded blocklist: "通常會," "往往會," "預期," "可能會上漲," "可能會下跌"
- C152 needs expanded blocklist: "買入信號," "賣出信號," "看多," "看空," "利多," "利空," "強烈建議"
- C140 lessons need content gate: "可以觀察到" framing, not "建議" framing

From the developer:
- YAML tone scanning gap: +0.5h
- All templates must pass tone blocklist

**Critical gap**: The tone QA blocklist was expanded in Sprint 18 (Round 38) with 11 phrases. Sprint 19 adds **12+ new risk phrases** identified by the designer. The blocklist expansion itself is not budgeted as a separate task — it's implicitly included in the 0.5h YAML scanning fix. But blocklist expansion requires:
1. Updating `TONE_BLOCKLIST` in `test_tone_qa.py`
2. Adding new allowed-context entries for new modules
3. Testing that the expanded blocklist doesn't create false positives in existing content
4. Adding C147/C152/C140-specific YAML content to the scan scope
5. Potentially adding new files to the excluded-files list

**My assessment**: The tone QA budget (0.5h) is an **order-of-magnitude underestimate**. The team is adding the highest-advice-risk content in the product's history, while allocating less than an hour to tone QA coverage. This is the single biggest risk in Sprint 19.

**Q3: Are there contradictions between the architect's, designer's, and developer's recommendations?**

Yes — several:

| Issue | Architect | Designer | Developer | Contradiction |
|-------|-----------|----------|-----------|---------------|
| C152 spike duration | Implicitly 2-4h | Supports C152 deferral | Recommends 4-6h spike | Developer says 2h is insufficient for a thorough spike; team budgets 2-4h |
| C147 data source | `case_studies.yaml` extension OR new `historical_patterns.yaml` | Uses `case_studies.yaml` implicitly (cross-linking C140↔C147) | Spike must decide between (a) and (b) | Designer assumes C140↔C147 cross-linking requires shared schema; architect says C147 can use separate YAML |
| Tone QA scope | LOW risk rating | Expanded blocklist +12 phrases needed | Known gap: +0.5h | Designer and developer disagree on severity; architect doesn't mention tone risk for C147/C152 at all |
| Content creation | 40% of effort is content (architect acknowledges) | Content quality gate + pre-write 10 cases from NOW | Content is separate track | All agree content is important but none commit to a pre-sprint content delivery date |

**Severity assessment**:
1. **C152 spike duration**: If the developer says 4-6h and the team budgets 2-4h, the spike will either be shallow (missing key risks) or overrun. This is a planning risk.
2. **C147 data source**: This is the core feasibility spike question. The designer's cross-linking design assumes C140↔C147 shared schema. If the spike reveals C147 needs a separate YAML, the cross-linking design breaks. This is an architectural risk.
3. **Tone QA scope**: The designer identifies 12+ new blocklist phrases but the budget allocates 0.5h. This is a quality risk that could result in shipping content that violates historian positioning.
4. **Content creation**: All three roles acknowledge content is critical, but there's no pre-sprint commitment date. "Start now" has been the recommendation since Round 37 and Sprint 18 is now complete — has any pre-writing happened?

**Q4: What are the overlooked risks?**

**Risk 1: `market_event_service` import failure propagation**
The architect identified that `timeline_service.py` imports non-existent `market_event_service.py` (silent failure). Both C147 and C140 are building on patterns from `timeline_service.py`. If the new services inadvertently reuse the broken import path, they'll inherit the silent failure. The fix (replacing import with direct YAML loading) should be a prerequisite for C140/C147 dev start.

**Risk 2: C140↔C147 schema coordination**
C140 extends `case_studies.yaml` with `category`/`tags`. C147's pattern matching may need to query by category or tags. If C140's schema extension isn't defined before C147's service implementation starts, C147 may need refactoring. This coordination point is not in the execution order.

**Risk 3: Content creation timeline mismatch**
C140's page can be built by the developer in 5-7h, but the content (10-15 case studies) takes 6-10h and depends on PM/Designer availability. If content isn't ready when the page is complete, the developer either waits (idle time) or moves to other work (context switching). Neither is efficient.

**Risk 4: Tone QA excludes critical files**
The current `_EXCLUDED_FILES` list has 16+ entries — nearly every service and page file is excluded. The tone QA effectively only scans delta_explanation_provider.py and template_provider.py deeply. Adding C147/C152/C140 will add more excluded files (new services that haven't been audited). At what point does the exclusion list become so comprehensive that the test has no teeth?

**Risk 5: Sprint 19 is the "historian" sprint, but tone QA is under-budgeted**
This is the deepest execution of the historian positioning in the product's history. It adds historical patterns, curated case studies, and (in Sprint 20) multi-factor narratives. The tone risk is the highest it's ever been. Yet the tone QA budget (0.5h) is the smallest Sprint 18 tone QA allocation (D-097 was 1.5h). This is backwards.

### Team Response Assessment

The plan is architecturally sound (Direction A is the team's recommendation). The designer's UX analysis is thorough and the cross-feature interaction map is excellent. The developer's estimates are detailed and include risk analysis. BUT:

1. The three roles are not fully aligned on tone QA scope (designer says +12 phrases, developer says +0.5h, architect doesn't address)
2. The three roles are not aligned on C152 spike depth (developer wants 4-6h, team budgets 2-4h)
3. The critical YAML schema coordination between C140 and C147 is unaddressed
4. The content creation bottleneck has no mitigation plan beyond "start now"
5. The `market_event_service` import fix should be Day 1 prerequisite

### Round 3 Verdict

**⚠️ CONDITIONAL PASS** — Tone QA budget must increase to 2-3h. The `market_event_service` fix must be a Day 1 prerequisite. C140→C147 schema coordination must be explicitly ordered. Content creation needs a pre-sprint delivery commitment or a ship-with-5-cases fallback.

---

## Final Verdict

### ✅ CONFIRMED with 8 conditions

Direction A ("Pattern-First") is a sound, defensible sprint plan. The features are strongly aligned with the product vision, the architectural approach is low-risk, and the execution order is mostly reasonable. However, the following 8 conditions must be met before development begins:

### Conditions

**1. C147 spike must have a pre-defined decision tree**
Before the 2h spike starts, the team must document: (a) what "success" looks like (minimum 3 event types with ≥3 mapped case studies each), (b) what "partial success" looks like (1-2 event types map → reduce C147 scope to top 5 event types), (c) what "failure" looks like (no clean mapping → fall back to Direction C, ship C140 only). Without this decision tree, the spike produces ambiguity, not clarity.

**2. C152 spike must happen on Day 1, parallel with C147 spike**
The C152 spike (2-4h, as budgeted) cannot wait until after C147 dev starts. Day 1 is spike day for both C147 (data mapping validation) and C152 (narrative template approach). If both spikes happen Day 1, the team has maximum information for the rest of the sprint.

**3. C140 schema extension is a hard prerequisite for C147 service implementation**
C140's extension of `case_studies.yaml` (adding `category`/`tags` fields) MUST be committed before C147's `historical_pattern_service.py` is built. This prevents C147 from building against an outdated schema and needing refactoring. The execution order must explicitly state: "C140 schema extension → C147 service implementation."

**4. Tone QA budget must be 2-3h, not 0.5h**
The 0.5h allocation only covers adding YAML file scanning to the existing test. Sprint 19 requires:
- Extending `TONE_BLOCKLIST` with 12+ new phrases (designer's recommendation)
- Adding YAML content scanning for `src/data/*.yaml`
- Adding new allowed-context and excluded-file entries for C147/C152/C140 services
- Pre-audit of all new YAML content before commit
- Total: 2-3h, not 0.5h

**5. Blocklist expansion for Sprint 19-specific risk phrases must be completed before content creation**
The designer identified 12+ new phrases that must be added to `TONE_BLOCKLIST`: "通常會," "往往會," "預期," "可能會上漲," "可能會下跌," "買入信號," "賣出信號," "看多," "看空," "利多," "利空," "強烈建議." These must be added to `test_tone_qa.py` BEFORE any C147 pattern text or C152 narrative templates are written, so the writers know the tone boundaries.

**6. PM/Designer must commit to a content delivery timeline for C140 case studies**
10-15 case studies (6-10h of writing) must be delivered by Day 3-4 of the sprint for integration. If content isn't ready by Day 4, the fallback plan is: ship with existing 5 case studies + 2-3 new ones minimum. PM/Designer must confirm they can deliver content on this timeline before Sprint 19 begins.

**7. Fix `market_event_service` import failure as Day 1 prerequisite (before any new dev)**
The broken import in `timeline_service.py` must be identified and replaced with correct YAML loading before C140 or C147 services are built. This prevents new services from inheriting the broken pattern. Estimated cost: 0.5h (add to the 0.5h tone QA budget OR combine into Day 1 spike time).

**8. Add mutual exclusion guard for Sprint 20 if C152 spike is shallow**
If the C152 spike (2-4h) produces only a thin design doc, Sprint 20's plan for full C152 implementation (22-29h) is at risk. The team should定义 what "successful C152 spike output" looks like: (a) event correlation logic validated with real data, (b) 3-5 narrative templates drafted and tone-audited, (c) `NarrativeProvider` protocol design documented, (d) integration point in `timeline_service.py` identified. If the spike doesn't deliver these 4 artifacts, C152 should be deferred to Sprint 21 and Sprint 20 should be replanned.

---

### Summary of Changes to Team Plan

| Item | Team Proposal | Challenger Revision |
|------|--------------|-------------------|
| C152 spike timing | After C147 dev (Day 4-5) | Day 1 parallel with C147 spike |
| Tone QA budget | 0.5h | 2-3h |
| C147 spike contingency | Direction C fallback | Add partial-success option (top 5 event types) |
| C140→C147 schema | Parallel development | C140 schema extension before C147 service |
| Blocklist expansion | Not budgeted separately | Before content creation starts |
| `market_event_service` fix | Not mentioned | Day 1 prerequisite |
| Content delivery | "Start now" | Commit to Day 3-4 delivery or ship with 5+2 cases |
| C152 spike success criteria | Not defined | 4 required artifacts documented pre-spike |

---

*Approved as Challenger. Sprint 19, Direction A "Pattern-First," with 8 binding conditions.*
*Signature: Challenger, 2026-06-14*
