## 2026-06-14 Design Review — Sprint 16b Discussion

### UX Impact Assessment

**C28 Full Story Timeline**
- **Impact**: High - Transforms event dashboard from disconnected list to chronological narrative
- **UX Benefits**: 
  - Addresses "historian" positioning by connecting events into a coherent story
  - Provides context for why events matter (revenue impact, price movement correlation)
  - Enables progressive disclosure: summary view first, details on expansion
  - Aligns with ten-second test - user can grasp company's recent history at a glance
- **Risks**: Potential information overload if not properly scoped; must maintain beginner-friendly language

**C02 Notifications**
- **Impact**: Critical - Missing core feature all competitors have
- **UX Benefits**:
  - Completes M5 event detection engine (currently wasted without delivery mechanism)
  - Enables proactive engagement - users informed of important changes without checking
  - Supports historian role by alerting users to new "chapters" in company story
  - Reduces cognitive load - system pushes relevant information instead of user pulling
- **Implementation Considerations**: 
  - Must respect user preferences (frequency, channel)
  - Should include plain-language explanations of why event matters
  - Needs clear opt-in/opt-out mechanisms

**C134 Change Explanations**
- **Impact**: Medium-High - Enhances existing data with causal understanding
- **UX Benefits**:
  - Transforms "what changed" into "why it matters" - core historian value
  - Reduces ambiguity in data interpretation
  - Supports ten-second test by highlighting most significant changes
  - Builds trust through transparent causality explanations
- **Design Challenges**: 
  - Must avoid over-explanation (maintain PPT-style brevity)
  - Need clear visual distinction between data and explanation
  - Should integrate seamlessly with existing metric displays

**C39 What Changed Recently**
- **Impact**: Medium - Complements C134 with temporal focus
- **UX Benefits**:
  - Addresses recency bias - helps users focus on relevant timeframes
  - Creates engagement hook - "what's new" drives regular check-ins
  - Supports adaptive/self-evolving positioning by highlighting evolution
  - Works well with notification system (C02) for immediate awareness
- **UX Considerations**:
  - Must define "recently" clearly (last 30 days? last quarter?)
  - Should prioritize magnitude of change over mere recency
  - Needs clear visual hierarchy (most significant changes first)

**C36 Revenue Tree V2**
- **Impact**: Medium - Enhances existing revenue pie with hierarchical view
- **UX Benefits**:
  - Transforms "what percentage" into "how money flows" - deeper business model understanding
  - Aligns with story-first approach by showing revenue generation process
  - Addresses beginner confusion about complex business structures
  - Complements existing pie chart with drill-down capability
- **Design Constraints**:
  - Must maintain chart >60% area rule (PPT-style)
  - Should limit to 2-3 levels of hierarchy to avoid complexity
  - Needs clear labeling and plain-language explanations for each node

### Design Direction Proposals

**Story Timeline Integration**
- **Placement**: Dedicated "Story" tab alongside existing tabs (Business Card, Operational Checkup, etc.)
- **Visual Treatment**: 
  - Horizontal timeline with events as nodes (similar to Gantt chart principles from design system)
  - Color-coded by event type (revenue, price, product, regulatory)
  - Each node shows: date, icon, one-sentence headline, expandable for details
  - Timeline should be horizontally scrollable with zoom capability (per design system Gantt rules)
- **Interaction**: 
  - Click event node to expand inline with plain-language explanation
  - Hover shows tooltip with date and category
  - Selected event highlights related metrics in main content area

**Notification System**
- **Bell Icon Placement**: Zone A navbar (right side, after price/change indicator)
- **Visual Design**:
  - Standard bell icon with badge for unread count (red circle with number)
  - Badge only shows when count > 0 (follows PPT-style minimalism)
  - Hover shows tooltip: "You have X new updates"
- **Notification Drawer** (on click):
  - Panel slides from right (respects Zone boundaries)
  - Header: "Updates" with clear all button
  - List items: each shows company icon, timestamp, plain-language headline
  - Click item navigates to relevant company page with event highlighted
  - Uses existing card styling for consistency

**Change Explanations Inline**
- **Placement**: Directly beneath affected metrics in Zone C content area
- **Visual Treatment**:
  - Subtle background tint (tip background #FFF8F0) for explanation container
  - Icon prefix: 🔄 for change explanations
  - Typography: same as plain-language (0.85rem, #27AE60, italic)
  - Length limit: 1 sentence maximum (stricter than general 2-sentence rule for explanations)
  - Appears only when significant change detected (>15% threshold)
- **Example**: 
  ```
  Revenue: $580B ↑12%
  🔄 Revenue growth accelerated due to strong AI chip demand
  ```

**What Changed Recently Card**
- **Placement**: Top of Business Card page, above existing metrics
- **Visual Treatment**:
  - Tip card styling (orange border #F39C12) 
  - Header: "🔄 最近有什麼變化" (Recently Changed)
  - Content: 2-3 bullet points max, each with:
    - Metric name + change direction (📈/📉)
    - Percentage change 
    - One-sentence plain-language explanation
  - Only shows when significant changes exist
  - Hidden by default if no significant changes (maintains PPT-style minimalism)

**Revenue Tree V2**
- **Placement**: New tab alongside revenue pie chart on Business Card page
- **Visual Treatment**:
  - Sunburst or treemap chart (Plotly, transparent background)
  - Hierarchical labeling: Company → Division → Product Line → Customer
  - Size represents revenue proportion
  - Color intensity shows year-over-year growth (green=up, red=down)
  - Hover tooltip shows: exact amount, percentage, plain-language description
  - Click node to drill down/up one level
- **Example Flow**:
  ```
  TSMC (100%)
  │
  ├── 5nm Chips (40%) 
  │   ├── Apple (25%) [📈 +18% YoY]
  │   ├── NVIDIA (15%) [📈 +32% YoY] 
  │   └── AMD (10%) [📉 -5% YoY]
  │
  ├── 3nm Chips (30%) [...]
  └── Packaging Services (30%) [...]
  ```

### Competitor Design References

**Simply Wall St Snowflake**
- **Pattern**: Radial visualization showing 5 dimensions (value, future, past performance, financial health, dividends)
- **Relevance**: Validates need for synthesized visual health score (C43 from research)
- **Adaptation for Stock Explorer**: 
  - Use same 5-dimension approach but with plain-language explanations on hover
  - Maintain PPT-style constraint: one key visual per concept
  - Add historian twist: explain how each dimension evolved historically

**Public.com Story Cards**
- **Pattern**: Visual cards showing company narrative with key milestones
- **Relevance**: Directly applicable to C28 Story Timeline and C48 Company Story Card
- **Adaptation for Stock Explorer**:
  - Convert to horizontal timeline format (better for chronological storytelling)
  - Maintain visual-first approach but add expandable detail sections
  - Use Stock Explorer's analogy engine for plain-language milestone descriptions

**Seeking Alpha Key Takeaways**
- **Pattern**: 3-5 bullet point summary at top of page
- **Relevance**: Validates C39 What Changed Recently and C48 Company Story Card
- **Adaptation for Stock Explorer**:
  - Apply PPT-style constraints: max 3 bullets, each under 15 characters for label
  - Use tip card styling for visual separation
  - Focus exclusively on factual changes (not predictions/opinions) to maintain historian positioning

**Common Themes from Research**:
1. **Progressive Disclosure**: Summary first, details on demand (used by all competitors)
2. **Visual-First Metrics**: Charts/icons before text (aligns with Stock Explorer PPT-style)
3. **Contextual Explanations**: Every significant metric has plain-language why (core Stock Explorer strength)
4. **Temporal Awareness**: Clear indication of timeframe for displayed data
5. **Actionable Insights**: Not just what happened, but why it matters to user

### Recommendations

1. **Implement C28 Story Timeline as horizontal scrollable timeline** with expandable event nodes, placed in dedicated tab. This best serves the historian positioning while maintaining PPT-style constraints through progressive disclosure.

2. **Add notification bell to Zone A navbar** with badge indicator. Use existing tip card styling for notification drawer to maintain visual consistency. This completes the M5 event detection loop critical for user engagement.

3. **Implement C134 Change Explanations as inline tip-container text** beneath affected metrics, limited to one sentence with 🔄 icon. This enhances existing data without violating PPT-style text limits.

4. **Implement C39 What Changed Recently as tip card** at top of Business Card page, showing max 3 significant changes with plain-language explanations. Only display when meaningful changes exist.

5. **For C36 Revenue Tree V2**, implement as sunburst chart in new tab alongside pie chart, using Plotly with transparent background and hover tooltips containing plain-language explanations. Limit to 3 hierarchy levels to maintain clarity.

6. **Cross-feature consistency**: 
   - Use identical plain-language explanation styling across all features
   - Maintain chart >60% area rule for all visualizations
   - Apply ten-second test to each feature implementation
   - Ensure all interactive elements have clear loading states (per design system)

7. **Historian positioning emphasis**: 
   - All features should answer "what happened and why it matters" not "what will happen"
   - Use past tense language exclusively
   - Focus on causal explanations, not predictions
   - Highlight how events connect to form company narrative

This approach maintains Stock Explorer's A design grade while adding meaningful UX enhancements that serve the core historian positioning and beginner-friendly principles.