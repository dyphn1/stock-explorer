# 🎨 Design Reviewer Analysis — Discussion Round 15

> **Author**: Design Reviewer
> **Cycle**: Discussion Round 15
> **Date**: 2026-06-20
> **Context**: Sprint 4 complete (Grade A, 6th consecutive). Sprint 5 prerequisites (D-039/040/D-041) about to start. Evaluating UX impact of proposed future features and providing design directions for the next wave.

---

## 1. UX Impact Evaluation of Proposed Features

### 1.1 Sprint 5 Features (C71, C74, C73) — Imminent Impact

| Feature | UX Impact | Zone Impact | PPT-Style Risk |
|---------|-----------|-------------|-----------------|
| **C71 (Study Log)** | Adds a new engagement layer — users track learning progress. Introduces "study streak" metaphor to a financial education tool. | Adds section to Zone C (business card) or new Zone B nav item. | LOW — uses new `_study_card()` component (D-041). If designed as a dashboard widget, fits PPT-style. |
| **C74 (Historical Scenarios)** | Highest historian-alignment. "What would have happened if..." interactive exploration. Introduces branching narrative to financial data. | New Zone C section with scenario selector at top (controls), narrative + chart below. | MEDIUM — Scenario cards must follow `_scenario_card()` component. Risk: narrative text could exceed 200-char limit per page. |
| **C73 (Expert Analysis, 10 stocks)** | Curated expert synthesis — "one-paragraph expert opinion." Introduces *authorship* to a tool that previously only had algorithmic content. | Adds new Zone C section with expert card + disclaimer. | MEDIUM — Expert cards need `_expert_card()` component (D-041). Risk: 10 stocks × inline disclaimer text = PPT text limit pressure. |

**Net UX Impact**: All three features add *depth* to the existing business card page without requiring new pages. This is good — it preserves the existing navigation IA and PPT-style one-page-per-concept philosophy. The risk is that the business card page becomes a "super page" with too many sections, violating the "one core message per page" principle (Section 5.1 of design system).

### 1.2 C81-C85 Features (Round 16 Review) — Post-Sprint 5 Impact

| Feature | UX Impact | Zone Impact | PPT-Style Risk |
|---------|-----------|-------------|-----------------|
| **C83 (Investment Memo Template)** | Structured reflection — users write their own analysis. First *productive* feature (user creates content, not just consumes). | New page or modal. If new page: Zone B nav item + Zone C form. | LOW — Template can be card-based. Form fields naturally limit text per section. |
| **C85 (Financial Wellness Check)** | Behavioral finance self-assessment. "How do you feel about market drops?" Introduces *psychology* dimension to company analysis. | New standalone page (like sector heatmap). Zone B nav item. | LOW — Quiz format fits PPT-style. Progressively disclosed questions align with "progressive disclosure" principle. |
| **C81 (Historical Decision Scenarios)** | "What would have happened if you bought at the peak?" Interactive historical branching. | New Zone C section or new page. | HIGH — Branching narratives are inherently multi-path. Violates "one key point per page" unless carefully scoped to single-scenario-per-page. |
| **C82 (Animated Data Story)** | Scrollable visual company history with animations. | New tab or page. | HIGH — Animation in Streamlit requires custom JS/CSS. JS risk flagged by Challenger. PPT-style is static-first. Animated content could conflict with "charts occupy >60%" principle if animations replace charts. |
| **C84 (Market Event Case Study)** | Interactive historical market event exploration. "What happened during the 2008 crisis for TW stocks?" | New page. Zone B nav item + Zone C content. | MEDIUM — Case study format naturally follows "one key point per page" (one event = one page). Risk: text volume for detailed case studies. |

**Net UX Impact**: C83 and C85 are *standalone pages* — they expand the product horizontally without complicating existing pages. C81, C82, C84 are more invasive — they risk diluting the PPT-style philosophy with complex interactions.

### 1.3 Long-Range Features (C63-C68 from Round 14) — Sprint 6-9 Impact

| Feature | UX Impact | Zone Impact | PPT-Style Risk |
|---------|-----------|-------------|-----------------|
| **C63 (Audio Market Story)** | Weekly audio narrative. Introduces *temporal* content (episodes over time). | New page or player widget in Zone A/C. | MEDIUM — Audio is a new modality. PPT-style is visual-first. Audio player UI must not dominate visual layout. |
| **C64 (Community Q&A)** | Peer learning forum. Introduces *social* dimension. | New page with thread list + detail view. | HIGH — Community content is inherently unstructured. Violates "one key point per page." Needs strong moderation + historian tone QA gate. |
| **C65 (Company Story Game)** | Gamified learning through play. Introduces *achievement* system. | New page or embedded widget. | MEDIUM — Game cards can follow PPT-style. Risk: game mechanics (scores, streaks) could conflict with "historian, not stock picker" positioning. |
| **C68 (Financial Concept Storytelling)** | Narrative-based concept explanations. Pairs with C47 (Education Academy). | New section or page. | LOW — Storytelling is the core of PPT-style. Well-aligned if text limits are respected. |

---

## 2. Competitor Design Patterns Worth Adopting

### From Simply Wall St (Visual-First Pioneer)
**Pattern: "Snowflake" Summary Visualization**
- Every stock has a 30-second visual health overview using a radar/snowflake diagram
- Color-coded scores (green/yellow/red) for 5 dimensions
- Progressive disclosure: summary first, details on click
- **Relevance to Stock Explorer**: Directly addresses "ten-second test" design principle. Our implementation (C43) should add plain-language explanations that Simply Wall St lacks — this is our differentiator. Design recommendation: Position the snowflake at the **top** of the business card page, above the existing one-liner. This gives users the 30-second overview BEFORE scrolling into details.

### From Public.com (Story Card Model)
**Pattern: "Company Story" Cards**
- 30-second visual summary of what a company does
- Card-stack UX (swipe-based on mobile)
- "One-liner + 3 key metrics + icon" format
- **Relevance to Stock Explorer**: C48 (Company Story Card) already implemented in Sprint 4. Design recommendation: Ensure the story card uses the **hero card** layout — large font, generous spacing, single visual metaphor. Do not cram it with data. One number, one chart, one sentence.

### From Stocksera (Narrative-First AI)
**Pattern: "Story" Tab Per Stock**
- Every stock has a dedicated narrative tab
- AI-generated summaries with "Key Events," "Growth Drivers," "Risks"
- Conversational tone (not financial jargon)
- **Relevance to Stock Explorer**: Our "historian" positioning is essentially the same idea. Design recommendation: When implementing C34 (Company Story Timeline), use a **vertical timeline** layout (not horizontal) to fit PPT-style scrolling. Each timeline event should follow the card format: date + one-line description + mini chart.

### From Zerodha Varsity (Structured Education)
**Pattern: Module-Based Progressive Learning**
- 14 numbered modules, completed in order
- Each module: concept → example → quiz → mastery check
- Plain-language first, jargon only with tooltip
- **Relevance to Stock Explorer**: C47 (Education Academy) and C50 (Learning Progress Tracker). Design recommendation: Use a **left-side progress indicator** (like a table of contents) in Zone B for learning modules. This is an exception to "Zone B must not contain page content" — learning navigation is fundamentally different from stock navigation.

### From Finimize (Bite-Sized Engagement)
**Pattern: "Market Mood" Sentiment Indicator**
- Single emoji + color indicator for market sentiment (😰 Fear → 😊 Neutral → 🤩 Greed)
- Daily summary in 3 minutes or less
- Push notification for daily engagement loop
- **Relevance to Stock Explorer**: C49 (Daily Market Pulse) and C35 (Market Mood Index). Design recommendation: Add a **compact mood indicator to Zone A** (navbar) — a small colored dot + emoji next to the page title. This gives beginners constant market context without navigating to a separate page. Replaces the need for a full market mood page.

### Pattern Synthesis: What to Adopt vs. Adapt vs. Reject

| Competitor Pattern | Adopt? | Adaptation Needed |
|---|---|---|
| Simply Wall St snowflake | ✅ Adopt | Add plain-language explanations per dimension |
| Public.com story cards | ✅ Adopt (done in Sprint 4) | Hero card layout, not data-dense |
| Stocksera narrative tab | ✅ Adapt | Vertical timeline, not horizontal; cards, not prose |
| Zerodha module progression | ✅ Adapt | Left-side progress in Zone B (exception to zone rules) |
| Finimize mood indicator | ✅ Adopt | Compact Zone A widget, not full page |
| TradingView social feed | ❌ Reject | Violates "historian" positioning; social features deferred to Sprint 8 (C64) |
| Tickeron AI Grade | ❌ Reject | Black-box scores violate "plain-language" principle |

---

## 3. Design Direction Suggestions

### Direction A: "PPT-Style 2.0" — Progressive Card Stack

**Core Concept**: Evolve the PPT-style from "one page, one chart" to "one page, one narrative arc." Each page tells a *story* through a stack of cards, where each card is a self-contained concept that builds on the previous one.

**How it works**:
1. **Hero card** (top): 30-second summary — one-liner, snowflake, key metric
2. **Story cards** (middle): 3-5 cards that build the narrative chronologically or thematically
3. **Action card** (bottom): "What to explore next" — related companies, quiz, or learning module

**Design Specification**:
- Hero card uses full width, 16rem value font (existing spec)
- Story cards use the existing `_白话_card()` pattern with orange tip variant for "lessons learned"
- Cards separated by `st.markdown("---")` (existing spec)
- Maximum 5 cards per page (new rule — enforces PPT discipline)
- Total text per card: 30-50 characters for label, 1-2 sentences for plain-language explanation

**Applies to**: C71 (Study Log card), C73 (Expert Analysis card), C74 (Scenario card), C83 (Memo card), all future content features.

**Design System Impact**: Add new card type specification to Section 3.3:
```html
<!-- Story card (green border narrative) -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #27AE60;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">{icon} {narrative_title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.3rem;line-height:1.6;">{narrative_content}</div>
</div>
```

### Direction B: "Dual-Mode Disclosure" — Beginner/Expert Toggle

**Core Concept**: As complexity grows (C71/C73/C74 sections added), the business card page risks overwhelming beginners. Implement a session-state toggle that shows essential content by default and reveals advanced sections on demand.

**How it works**:
1. **Default (Beginner)**: Hero card + 3 core sections only (Revenue, Key Metrics, "Did You Know?")
2. **Toggle to Expert**: All sections visible, including C71/C73/C74 and future features
3. Toggle placed in **Zone A** (navbar), not Zone C — this is a *display preference*, not page content

**Design Specification**:
- Toggle uses `st.toggle` or two `st.button` items in Zone A (below tabs)
- Beginner mode: Maximum 6 sections visible, card-based layout
- Expert mode: All sections, with expandable accordions for dense sections
- Toggle state stored in `session_state["display_mode"]`
- Section rendering uses `if session_state.get("display_mode") == "expert":` guards

**Applies to**: All Sprint 5+ features. C71/C73/C74 render in expert mode by default. C85 (Wellness Check) is always visible (standalone page).

**Design System Impact**: Update Section II (Zone Division) to allow one interactive control in Zone A for display preferences.

### Direction C: "Color-Coded Narrative" — Semantic Card Borders

**Core Concept**: Expand the color system from price direction (red/green/blue) to *content type*. Use card border colors to communicate the nature of content at a glance, helping users navigate increasingly complex pages.

**Color Mapping** (extends existing Section 3.1):
| Content Type | Border Color | Usage |
|---|---|---|
| Data/Facts | `#3498DB` (blue) | Existing info cards — company metrics, charts |
| Narrative/Story | `#27AE60` (green) | Story cards, timelines, scenarios |
| Expert/Curated | `#8E44AD` (purple) — **NEW** | Expert analysis, memos, curated content |
| Warning/Risk | `#E74C3C` (red) | Risk sections, disclaimers (existing) |
| Learning/Education | `#F39C12` (orange) | Tips, quizzes, learning modules (existing tip cards) |
| Community/Social | `#1ABC9C` (teal) — **NEW** | Community Q&A, shared stories |

**Design Rationale**: The current design system only has 3 status colors + 3 background colors. As content types multiply, users need visual cues to distinguish "company facts" from "expert opinions" from "learning modules." Color-coded borders provide this without adding UI chrome.

**⚠️ Critical Constraint**: Purple and teal are NEW colors. This expands the palette beyond the current "only red/green/blue for status" rule. The rationale: these are *content type indicators*, not *status indicators*. They follow the same border-left card pattern, not the color system in Section 3.1 which is for price direction only. This is a **Daniel decision needed** — does expanding the color palette beyond RGB violate the design philosophy?

**Applies to**: C73 (expert cards → purple border), C64 (community → teal border), C68 (education → orange border), all future multi-type features.

---

## 4. Design Risk Assessment

### Critical Risks (P0)

| Risk | Feature | Description | Mitigation |
|---|---|---|---|
| **Business card page bloat** | C71/C74/C73 | Adding 3+ sections to the business card page violates "one key point per page." Page could become 2000+ pixels long. | Direction B (Dual-Mode Disclosure). Beginner mode shows max 6 sections. Expert mode shows all. |
| **D-003 regression** | C71/C74/C73 | If D-041 (card components) is not completed before Sprint 5, developers will use inline HTML, recreating the D-003 duplication problem. | D-041 is a HARD PREREQUISITE. No feature coding until D-041 is done. |
| **Text limit violation** | C74/C73 | Historical scenarios and expert analysis inherently require more text. C74 narrative + C74 chart labels could exceed 200-char limit. | Enforce text limits at the component level. `_scenario_card()` must truncate at 150 chars with "查看更多" expansion. |

### Important Risks (P1)

| Risk | Feature | Description | Mitigation |
|---|---|---|---|
| **Zone A pollution** | C49 (Market Mood) | Adding a mood indicator to Zone A adds interactive controls to the navbar, violating Section II. | Make it a *display-only* indicator (colored dot + emoji), not interactive. Or place in Zone C as a floating widget. |
| **Snowflake chart complexity** | C43 | Radar charts with 5 dimensions can be confusing for beginners. Simply Wall St's snowflake works because it's the *only* thing on the page. | Add plain-language labels on each axis. Use tooltips with analogies. Test with 5 beginners before shipping. |
| **Disclaimer inconsistency** | C73/C74 | Expert analysis and historical scenarios both need historian disclaimers. Inconsistent wording creates regulatory risk. | D-040 (standardized disclaimer component) must be completed before C73/C74. Single `_historian_disclaimer()` helper. |
| **Animation JS risk** | C82 | Animated data stories require custom JavaScript in Streamlit. Streamlit's JS support is limited and fragile. | Start with static MVP (C82 de-risked per Round 16). Use CSS transitions only, no JS. Defer full animation to post-Sprint 7. |

### Optimization Risks (P2)

| Risk | Feature | Description | Mitigation |
|---|---|---|---|
| **Section header inconsistency** | All Sprint 5+ | 3 different header styles exist (markdown `###`, `st.expander`, inline HTML). Sprint 5 adds more. | D-039 (standardized section header) must be completed first. Single `_section_header()` helper. |
| **Mobile responsiveness** | All new features | Streamlit is desktop-first. New card layouts may break on narrow screens. | Test all new components at 768px width. Use `use_container_width=True` on all cards. |
| **Content type color confusion** | C73/C64 | New purple/teal colors for content types could be confused with status colors. | Add a one-time tooltip on first use: "紫色邊框 = 專家分析" / "青色邊框 = 社群內容" |

---

## 5. Design Infrastructure Needs

### 5.1 Design System Updates Required

**Immediate (Before Sprint 5)**:
1. **Section 3.3 (Cards)**: Add `_story_card()` (green border narrative) specification
2. **Section 3.3 (Cards)**: Add `_expert_card()` (purple border — if Daniel approves new color) specification
3. **Section 3.3 (Cards)**: Add `_scenario_card()` specification
4. **Section 3.3 (Cards)**: Add `_study_card()` specification
5. **Section II (Zone Division)**: Add exception for display preference toggle in Zone A
6. **Section 5.1 (One Key Point)**: Clarify that "one key point" means "one narrative arc" not "one chart" — multiple cards can build a single narrative

**Short-Term (Sprint 5-6)**:
7. **Section 3.1 (Color System)**: Add content-type color mapping (purple for expert, teal for community) — pending Daniel approval
8. **Section 5.2 (Text Limits)**: Add per-card text limits (30-50 chars label, 1-2 sentences explanation)
9. **Section 5.3 (Chart Proportion)**: Clarify that snowflake/radar charts count as "charts" for the >60% rule
10. **Section VI (Pre-Development Checklist)**: Add "Card count ≤ 5 per page" check

**Medium-Term (Post-Sprint 5)**:
11. **New Section VII (Interaction Patterns)**: Document progressive disclosure patterns (beginner/expert toggle, expandable cards, "查看更多" truncation)
12. **New Section VIII (Content Types)**: Document the distinction between factual content (blue), narrative content (green), expert content (purple), and community content (teal)

### 5.2 Component Library Status

**Completed Components** (from D-041 prerequisites):
- `_白话_card()` — info card (blue border) ✅
- `_tip_card()` — tip card (orange border) ✅

**Needed for Sprint 5** (D-041 deliverables):
- `_section_header()` — standardized section header (D-039)
- `_historian_disclaimer()` — standardized disclaimer (D-040)
- `_study_card()` — study log card (D-041)
- `_expert_card()` — expert analysis card (D-041)
- `_scenario_card()` — historical scenario card (D-041)

**Needed for Post-Sprint 5** (new proposals):
- `_story_card()` — narrative card (green border) — Direction A
- `_mood_indicator()` — compact market mood widget — Finimize pattern
- `_progress_tracker()` — learning progress bar — Zerodha pattern
- `_quiz_card()` — interactive quiz card — Khan Academy pattern

### 5.3 Design Grade A Maintenance Strategy

The project has maintained Grade A for 6 consecutive rounds. To preserve this as complexity grows:

1. **Enforce D-041 before any Sprint 5 feature coding** — this is the single most important gate. Without standardized components, every new feature will introduce inline HTML inconsistencies.

2. **Add a "card count" rule to the pre-development checklist** — maximum 5 cards per page section. This prevents the business card page from becoming a wall of cards.

3. **Text audit at every review** — as C73/C74 add narrative content, text volume will creep up. Every design review must measure total text per page against the 200-char limit.

4. **Color audit at every review** — as new content types are added, developers will be tempted to invent new colors. Every design review must verify all colors against the (expanded) palette.

5. **"Ten-second test" validation** — for every new feature, a beginner must be able to state the page's core message within 10 seconds. If the page has 15 sections, this test fails.

---

## 6. Recommendation

### Recommended Direction: **A + B (Progressive Card Stack + Dual-Mode Disclosure)**

**Rationale**: These two directions together solve the core tension of Sprint 5+ — how to add rich features (C71/C74/C73) without overwhelming beginners or violating PPT-style principles.

- **Direction A** (Card Stack) ensures every new feature follows a consistent visual pattern that fits the existing design system
- **Direction B** (Dual-Mode) ensures the business card page remains scannable for beginners while supporting power users

**Direction C** (Color-Coded Narrative) is recommended as a **Phase 2 enhancement** — adopt after Daniel approves the expanded color palette. The current RGB + orange palette is sufficient for Sprint 5 if we use border colors semantically (blue = data, green = narrative, orange = tips, red = risks).

### Priority Sequence for Design Infrastructure

1. **D-039 + D-040 + D-041** (Sprint 5 prerequisites) — MUST complete before any feature coding
2. **Design system Section 3.3 update** — add new card type specs (story, expert, scenario, study)
3. **Design system Section II update** — Zone A display preference exception
4. **Design system Section 5.1 update** — clarify "one key point = one narrative arc"
5. **Pre-development checklist update** — add card count rule + text audit rule

### Sprint 5 Feature Design Sequence (Recommended)

1. **C71 (Study Log)** first — lowest risk, uses `_study_card()`, adds engagement without content complexity
2. **C74 (Historical Scenarios)** second — highest historian alignment, uses `_scenario_card()`, narrative text must be carefully limited
3. **C73 (Expert Analysis)** last — highest content risk (10 stocks × curated text), uses `_expert_card()` + `_historian_disclaimer()`, requires D-040 completion

### Post-Sprint 5 Design Priority

**C83 (Investment Memo Template)** should be the first post-Sprint 5 feature from a design perspective — it's a standalone page (no business card bloat), it uses existing card components, and it extends the existing C55 pattern. Lowest design risk, highest historian alignment.

**C82 (Animated Data Story)** should be deferred the longest — highest JS risk, highest PPT-style philosophy conflict, and requires new animation design patterns not yet in the design system.

---

*This analysis is based on Sprint 4 completion state (R3, C48, C38, C51, C53-1), Sprint 5 planned features (C71, C74, C73), Round 14 discussion outputs (C63-C68), and Round 16 review outputs (C81-C85). All recommendations align with the existing design system at docs/design/design_system.md and competitor research at docs/research/competitor_research.md.*
