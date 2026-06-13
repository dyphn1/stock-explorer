## 2026-06-14 Technical Analysis — Sprint 16b Discussion

### Problem Description
Sprint 16a is complete (C14 Health Score Badge, C45 Valuation Band, C28 Story Timeline Spike, C41 Read Next Phase A). The C28 Story Timeline spike passed with Option A (compose-and-enrich pipeline) recommended. Sprint 16b must now decide between implementing the full C28 Story Timeline feature or pursuing alternative notification-focused work. The decision impacts our competitive positioning as a "Historian" (story-first) platform versus addressing a critical P0 gap in notifications that competitors universally provide.

### Option A: C28 Full Story Timeline
- Pros: 
  - Directly implements our unique "Historian" positioning — no competitor has narrative timeline (per competitor research rounds 7-8)
  - Builds on validated spike architecture (Option A compose-and-enrich pipeline)
  - Creates a foundational narrative layer that can be extended by future features (C38 Compare Stories, C134 Change Explanations)
  - Addresses the #1 competitive gap identified in research: "The event dashboard is a disconnected list. What's missing is a narrative timeline"
  - Leverages existing data sources (events.yaml, case_studies.yaml, milestones) without requiring new integrations
- Cons:
  - Requires addressing spike-identified gaps: sparse event history, missing milestone data, undated company facts
  - Higher effort estimate (26-36h) may delay other high-impact features like notifications
  - Narrative generation complexity risks inconsistent historian tone without careful QA gating
  - Does not address the P0 notifications gap where all competitors have alerting capabilities
- Effort: 26-36h (based on spike planning)

### Option B: C28 Core Story Timeline + C39 What Changed Recently
- Pros:
  - Delivers partial timeline functionality faster (core events + milestones) while adding complementary "recent changes" feature
  - C39 (What Changed Recently) is a lower-effort, high-impact feature (8-10h) that addresses another competitive gap
  - Combines two related narrative-driven features that share data pipelines and plain-language explanation logic
  - Provides immediate value: users get both historical context (timeline) and current awareness (recent changes)
  - Reduces risk by splitting work into two verifiable increments rather than one large narrative undertaking
- Cons:
  - Still requires solving the same data gap issues as Option A (sparse history, missing milestones)
  - Total effort (34-46h) may exceed sprint capacity, requiring further scope reduction
  - C39 implementation may need to wait for timeline data pipeline to be established
  - Potential overlap in explanation generation logic between timeline entries and delta cards
- Effort: 34-46h (26-36h for core timeline + 8-10h for C39)

### Option C: C02 Notifications + C07 Custom Thresholds (Fallback Path)
- Pros:
  - Addresses the universal P0 competitive gap — all major competitors (StatementDog, GoodInfo, CMoney, WantGoo) have notifications
  - Activates the existing M5 (Adaptive Engine) event detection system that currently lacks alerting output
  - Lower combined effort estimate (18-28h) than full timeline implementation
  - C07 Custom Thresholds enables personalized alerting, increasing feature utility and retention
  - Implements a proven engagement pattern: users return for timely alerts on their watchlist
  - Creates foundation for future explanation-rich notifications (C138 Smart Notifications)
- Cons:
  - Does not advance our unique "Historian" positioning; focuses on table-stakes feature parity
  - Notification systems require ongoing maintenance (permission handling, platform integration, spam prevention)
  - Less differentiation potential compared to narrative timeline which competitors lack entirely
  - Defers the strategic differentiator (story timeline) to later sprints, extending our competitive vulnerability
- Effort: 18-28h (based on handoff estimates)

### Recommendation
**Proceed with Option A: C28 Full Story Timeline**. The spike has already validated technical feasibility and identified specific, addressable gaps. As the System Architect, I recommend this path because:

1. **Strategic Alignment**: Our core differentiation is the "Historian" positioning — telling company stories through data. The narrative timeline is the manifestation of this vision, while notifications are a table-stakes feature that competitors already provide adequately.

2. **Validated Approach**: The spike passed with clear go/no-go criteria. We have a proven architecture (Option A compose-and-enrich pipeline) and known gaps to solve, reducing implementation risk compared to starting a new feature area.

3. **Foundation for Future Work**: A implemented timeline creates the data pipeline and explanation infrastructure that subsequent features (C38 Compare Stories, C134 Change Explanations, C138 Smart Notifications) can leverage, reducing their future effort.

4. **Gap Resolution**: The spike-identified gaps (sparse event history, missing milestone data, undated company facts) are concrete data issues that can be solved through curation and pipeline enhancements, unlike architectural unknowns.

To manage risk within the sprint:
- Phase 1 (Weeks 1-2): Implement core compose-and-enrich pipeline with existing data
- Phase 2 (Weeks 3-4): Address gap mitigation — curate milestone data, enhance event interpretation coverage, optimize for <200ms response
- If gaps prove more substantial than anticipated, de-scope to Option B (core timeline only) and move C39 to a later sprint

This approach delivers our unique strategic value while maintaining technical feasibility. Notifications (C02) should be prioritized for Sprint 17 once the narrative pipeline is established, as explanation-rich notifications (C138) will benefit from the timeline's plain-language explanation framework.