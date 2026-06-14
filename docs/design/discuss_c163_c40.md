# 2026-06-14 Design Review — C163 + C40 UX Direction

> **Designer**: Design Reviewer (openrouter/google/gemma-4-31b-it:free)
> **Context**: Sprint 20 — C163 (Learn First Gate) and C40 (Beginner/Expert Mode) pending design direction
> **References**: `docs/design/design_system.md`, `docs/research/competitor_research.md` (Rounds 8–9, C40/C163 sections), `docs/architecture/discuss_c163_c40.md`, `docs/roles/designer.md`

---

## Competitor Design Patterns

### Sharesies (NZ) — Complexity Levels
- **Pattern**: During onboarding, Sharesies asks users to self-select their experience level (Beginner / Intermediate / Advanced). This sets the default complexity of all content.
- **UX Impact**: Users feel the product is "built for them" from the start. The choice is explicit and respected throughout the experience.
- **Relevance to Stock Explorer**: Validates C40's mode toggle concept. Sharesies proves that investors will actively choose a complexity level if asked. However, Sharesies places this in onboarding, not as a persistent toggle — this is the gap C163 + C40 together fill.

### NerdWallet (US) — "Simple View"
- **Pattern**: NerdWallet has a persistent "Simple View" toggle globally available. When enabled, every page hides advanced details and shows only the essentials with plain-language explanations.
- **UX Impact**: The toggle is always accessible but not intrusive. Users can switch at any time without losing their place.
- **Relevance to Stock Explorer**: Validates the persistent toggle concept for C40. Key lesson: the toggle must be **global** (not page-level) and **persistent** (not resetting on navigation).

### Webull (US) — "Learn First, Trade Later"
- **Pattern**: Webull requires new users to complete a brief educational module before accessing trading features. The module covers basic concepts (P/E ratio, market cap, volatility) with interactive explanations. Users can skip, but the default path encourages learning.
- **UX Impact**: The gate reduces impulsive behavior and builds user confidence. The skip option prevents frustration.
- **Relevance to Stock Explorer**: Directly validates C163's "soft gate" approach. Key lesson: the gate is **encouraging, not enforced**. A skip/dismiss option is essential to prevent engagement drop-off.

### Tastytrade (US) — "Learn → Paper Trade → Live Trade" Pipeline
- **Pattern**: Tastytrade structures the entire user journey as a progression: Learn first, then practice, then invest. The learning content is gated behind short quizzes that unlock the next stage.
- **UX Impact**: Users feel a sense of progression and achievement. The quiz mechanism ensures comprehension, not just exposure.
- **Relevance to Stock Explorer**: Strongly validates the combined C163→C40 flow. The "Learn First Gate" (C163) teaches concepts, and "Beginner Mode" (C40) provides a safe environment to explore those concepts. Future features (C165 Varsity Mode) can add quiz-based progression.

### Stash (US) — "Learn Before Invest" Gate
- **Pattern**: Stash shows 2 micro-cards on first visit before showing any portfolio data. Each card has a single concept, plain-language text, and a dismiss button. Writing level is 8th grade.
- **UX Impact**: Minimal friction. Users understand the product's value proposition in under 30 seconds.
- **Relevance to Stock Explorer**: Our existing C103 (`first_visit_guide.py`) is modeled on this pattern. C163 should **extend** this, not replace the pattern entirely.

### Simply Wall St (AU) — Snowflake Visual Summary
- **Pattern**: Each stock page opens with a visual "snowflake" diagram that gives a 30-second company overview across 5 dimensions. Users see the summary first, then drill down into details.
- **UX Impact**: The "summary first, details on demand" approach perfectly aligns with our "ten-second test" design principle.
- **Relevance to Stock Explorer**: C163's gate should end with a similar "here's what you'll see" preview that sets expectations before users enter the stock page.

### Stocksera (US) — "Story" Tab + Narrative Summaries
- **Pattern**: Every stock has a "Story" tab that presents a narrative summary of the company. The story is written in plain language with key metrics woven into the narrative.
- **UX Impact**: Beginners understand the company as a story, not a collection of metrics.
- **Relevance to Stock Explorer**: C163's gate content should use narrative format ("Here's what happened to TSMC...") rather than bullet-point definitions. This aligns with our "Story first, data second" core value.

---

## C163 Learn First Gate — Design Direction

### Format: Full-Page Gate (Not Modal, Not Slide-Over)

**Decision**: C163 should be a **full-page experience** — a dedicated "學習入門" page that serves as the default landing page for first-time users.

**Rationale**:
- A **modal** would violate the "no mixing" zone principle — modals overlay content, creating an implicit Zone D.
- A **slide-over** would compete with Zone B (sidebar) for attention and feel like a temporary interruption.
- A **full-page** is consistent with existing patterns (C103 First Visit Guide was a standalone page, C47 Academy is a standalone page). The gate should be a first-class page in the router.
- Full-page allows proper use of PPT-style layout (one concept per screen, charts > 60% of area).
- The gate should **replace** `first_visit_guide.py` (C103), not coexist with it. Having both "新手導覽" and "學習入門" pages would confuse users.

### Placement: Router-Level Default Landing Page

**Decision**: The gate is the default page for users who haven't completed onboarding (`st.session_state["first_visit_dismissed"] == False`). After dismissal, the default landing page becomes the business card page for the default stock.

**Navigation flow**:
```
User opens Stock Explorer
    → Gate page shown (if first visit)
    → User completes/skips gate
    → Redirect to Business Card (default stock)
    → Gate never shown again (unless user manually navigates to "學習入門" in the future)
```

### Content: 4 Micro-Lessons (Not 3, Not 5)

**Decision**: The gate contains **4 micro-lessons**, each on its own "slide" within the gate page. Users navigate through lessons with a "Next" button and see progress indicators (dots).

| # | Lesson Topic | Format | Key Message |
|---|---|---|---|
| 1 | "What is a stock?" | Analogy card + icon | "Owning a stock means owning a piece of a company. Like owning one slice of a pizza." |
| 2 | "How does a company make money?" | Mini revenue tree (pie chart) | "TSMC makes money by manufacturing chips. 40% comes from advanced chips (5nm)." |
| 3 | "How do I know if a company is doing well?" | 2 metric cards (Revenue + P/E) | "Revenue = how much they sell. P/E = how many years to earn back the price." |
| 4 | "What is Stock Explorer?" | Plain-language card + historian positioning | "We tell you what happened to companies. We never tell you what to buy." |

**Content rules**:
- Each lesson follows PPT-style: **one key point per screen**, max 40 characters for the key point, plus one analogy.
- Plain-language explanation ≤ 2 sentences per lesson (design system §5.2).
- Visual content (charts, icons) must occupy > 60% of each lesson screen.
- All financial terms in the gate must have inline glossary tooltips (hover/tap to expand).

### Gate Controls: Soft Gate with Skip

**Decision**: The gate is a **soft gate** with a persistent "跳過教學" (Skip) button in the top-right corner. Users can skip at any time without completing lessons.

**Controls**:
- **Primary**: "繼續 →" button at the bottom of each lesson (advances to next lesson)
- **Secondary**: "跳過教學" link in the top-right (dismisses gate entirely, sets `first_visit_dismissed = True`)
- **Progress**: Dot indicators at the bottom showing current lesson (1/4, 2/4, 3/4, 4/4)
- **Completion**: After lesson 4, "開始探索" button that navigates to business card page

**Critical**: The gate must NEVER feel like a mandatory barrier. The skip option must be visible on every lesson screen, not hidden behind a menu.

### Visual Design Spec

```
┌─────────────────────────────────────────────────────────┐
│  Zone A: Navbar (standard — company name + price + tabs) │
│  No gate-specific elements in Zone A                      │
├──────────┬──────────────────────────────────────────────┤
│ Zone B   │  Zone C: Gate Content                         │
│ Sidebar  │                                                │
│ (hidden  │  ┌──────────────────────────────────────────┐ │
│  or      │  │  📖 Lesson 1 of 4                         │ │
│  dimmed) │  │                                            │ │
│          │  │  [Key Point — ≤ 40 chars]                  │ │
│          │  │  [Visual / Chart — > 60% of space]         │ │
│          │  │  [Plain-language analogy — ≤ 2 sentences] │ │
│          │  │                                            │ │
│          │  │  ○ ● ○ ○  (progress dots)                 │ │
│          │  │                                            │ │
│          │  │              [繼續 →]    [跳過教學]        │ │
│          │  └──────────────────────────────────────────┘ │
└──────────┴──────────────────────────────────────────────┘
```

### Interaction Notes
- **Session state**: `st.session_state["first_visit_dismissed"]` is checked in the router. When `False`, the default page is "學習入門". After dismissal, the router redirects to the business card page.
- **Loading state**: Each lesson should load instantly (static content). No spinner needed.
- **Animation**: Subtle fade-in for each lesson transition (CSS transition, not Streamlit animation). Duration: 300ms.
- **Accessibility**: Gate content must be keyboard-navigable (Tab → Next button, Enter → advance).

---

## C40 Beginner/Expert Mode — Design Direction

### Toggle Placement: Zone B Sidebar (NOT Zone A Navbar)

**Decision**: **Beginner/Expert toggle must be placed in Zone B (sidebar)**, NOT in Zone A (navbar).

**Rationale**:
- **Design system Zone A rule**: "Must NOT contain: search box, filters, or any interactive controls." (design_system.md §II, Zone A spec — line 45). A mode toggle is an interactive control. Adding it to Zone A violates the "no mixing" principle.
- **Navbar crowding**: The navbar already contains 26 page tabs via `st.radio`. Adding a toggle would make navigation significantly harder on mobile.
- **Sidebar is Zone B (navigation)**: A complexity toggle is a **navigation control** — it determines which "version" of content the user navigates to. This is semantically a navigation concern and belongs in Zone B.
- **Architectural note**: The architect's analysis (Option A, P4 prerequisite) reached the same conclusion: "Place the toggle in the sidebar as a prominent element above the search box."
- **Competitor alignment**: Sharesies places the level selector in the main navigation area (sidebar), not the top bar.

**Sidebar toggle spec**:
```
┌──────────────────┐
│ 🌱 新手模式       │  ← st.toggle or st.radio
│ 🔬 進階模式       │
│ ───────────────── │
│ 🔍 搜尋...        │  ← existing search box
│ 📈 熱門個股        │  ← existing hot stocks
│ 📊 熱門 ETF        │  ← existing hot ETFs
│ 📋 我的觀察清單     │  ← existing watchlist
│ 📅 事件儀表板      │  ← existing events
└──────────────────┘
```

**Toggle component**: Use `st.radio` with two options ("🌱 新手模式" / "🔬 進階模式") rather than `st.toggle` for clarity. A radio makes both options always visible; a toggle hides the unselected option.

**Default state**: Beginner mode (`"新手模式"`) for all new users. Expert mode (`"進階模式"`) for users who explicitly switch. State persisted in `st.session_state["user_experience_level"]`.

### What Changes in Beginner Mode (All Stock Pages)

C40 must affect ALL stock pages, not just the business card page. Here's the page-by-page spec:

#### Business Card Page (already has C105 toggle)
| Section | Beginner Mode | Expert Mode |
|---------|---------------|-------------|
| Key Takeaways (C37) | ✅ Shown | ✅ Shown |
| Revenue Pie Chart | ✅ Shown | ✅ Shown |
| Revenue Tree (C36) | ❌ Hidden | ✅ Shown |
| Key Metrics (3-4) | ✅ Shown (3-4 cards) | ✅ Shown (all 8-12 cards) |
| Institutional Investors | ❌ Hidden (expander) | ✅ Shown |
| What Changed Recently (C39) | ✅ Shown (summary only) | ✅ Shown (full detail) |
| Read Next (C41) | ✅ Shown | ✅ Shown |
| Did You Know? | ✅ Shown | ✅ Shown |

#### Operation Checkup Page
| Section | Beginner Mode | Expert Mode |
|---------|---------------|-------------|
| Revenue Trend | ✅ Shown | ✅ Shown |
| Revenue Stability (analogy) | ✅ Shown | ✅ Shown |
| Volume Analysis | ❌ Hidden | ✅ Shown |
| Seasonal Patterns | ❌ Hidden | ✅ Shown |
| Institutional Flow | ❌ Hidden | ✅ Shown |

#### Financial Health Page
| Section | Beginner Mode | Expert Mode |
|---------|---------------|-------------|
| Profit Funnel | ✅ Shown | ✅ Shown |
| Key Ratios (ROE, P/E,毛利率) | ✅ Shown (3 cards) | ✅ Shown (6+ cards) |
| Debt Analysis | ❌ Hidden (expander) | ✅ Shown |
| Cash Flow | ❌ Hidden | ✅ Shown |
| Dividend Details | ❌ Hidden | ✅ Shown |

#### Peer Comparison Page
| Section | Beginner Mode | Expert Mode |
|---------|---------------|-------------|
| Top 3 Peers | ✅ Shown | ✅ Shown |
| Plain-language comparison | ✅ Shown | ✅ Shown |
| Detailed metric table | ❌ Hidden | ✅ Shown |
| Compare Stories (C38) | ❌ Hidden | ✅ Shown |

#### Group Structure Page
| Section | Beginner Mode | Expert Mode |
|---------|---------------|-------------|
| Parent + Top 3 Subsidiaries | ✅ Shown | ✅ Shown |
| Ownership percentages | ✅ Simplified | ✅ Full detail |
| Full tree structure | ❌ Hidden | ✅ Shown |

#### Category Browse / ETF Zone
| Section | Beginner Mode | Expert Mode |
|---------|---------------|-------------|
| Category list | ✅ Simplified (names only) | ✅ Full (with metrics) |
| ETF comparison | ✅ Basic (3 metrics) | ✅ Full (10+ metrics) |

### Visual Indicators for Beginner Mode

When in beginner mode, pages should have a subtle visual indicator confirming the current mode:

- **In-page banner**: A single-line banner at the top of Zone C (below tabs): "🌱 新手模式：目前顯示簡化版本，切換至進階模式可查看更多內容。" Uses background color `#FEF9E7` (warning yellow) with text color `#2C3E50`.
- **Hidden sections indicator**: Where sections are hidden, show a collapsed expander labeled "🔬 🔰 進階內容（切換至進階模式即可查看）". This teaches users that more content exists and how to access it.
- **Color compliance**: The beginner mode banner uses the existing warning background color (`#FEF9E7`). No new colors needed.

### State Persistence and URL Sync

- **Default**: `st.session_state["user_experience_level"] = "beginner"` for new users.
- **Persistence**: The value persists across page switches and session refreshes (stored in session_state, not URL params to avoid URL pollution).
- **Switching**: Changing the toggle in the sidebar immediately triggers `st.rerun()` to re-render the current page in the new mode.
- **No data reload**: Switching modes does NOT reload data from the API. It only changes which sections are shown/hidden. This must be instant (< 0.5s).

---

## UX Risks and Mitigations

### Risk 1: C163 Gate as Engagement Barrier (Severity: P1)

**Risk**: Users arriving at Stock Explorer with a specific stock in mind (e.g., from a search engine) will be forced through a 4-lesson gate before seeing data. This could increase bounce rate.

**Mitigation**:
- The gate MUST have a prominent "跳過教學" (Skip) link visible on every lesson screen, not just the first.
- The gate auto-advances after lesson 4 without requiring explicit "Next" clicks (after a 3-second pause).
- Future enhancement: if the user arrives with a specific `stock_id` in the URL, skip the gate entirely (they already know what they want to see).

### Risk 2: Inconsistent Beginner Mode Across Pages (Severity: P1)

**Risk**: If C40 is implemented page-by-page without a consistent spec, some pages may show too much complexity in beginner mode while others show too little, creating a jarring experience.

**Mitigation**:
- Define a per-page "Beginner Mode Spec" before coding begins (see Architect's prerequisite P1).
- Each page must show exactly 3-5 key sections in beginner mode, plus the collapsed "advanced content" expander.
- The Designer must audit all pages after implementation to verify consistency.

### Risk 3: Toggle Discoverability (Severity: P2)

**Risk**: If the C40 toggle is buried in the sidebar below the fold, users may not discover it. Beginner users will never know they can simplify the experience, and expert users will be stuck in beginner mode.

**Mitigation**:
- Place the toggle **above** the search box in the sidebar (top of Zone B, always visible when sidebar is expanded).
- Add a one-time tooltip on first visit: "👋 這裡可以切換新手/進階模式" pointing to the toggle. Dismissible.
- The default sidebar state is "expanded" (design_system.md §II, Zone B spec), so the toggle is visible by default.

### Risk 4: C163 and C40 Definition Conflict (Severity: P1)

**Risk**: C163 teaches concepts (e.g., "This is P/E ratio"), and C40 hides advanced content. If the definition of "beginner" differs between the two features, users will be confused — the gate teaches P/E but beginner mode still shows P/E in detail.

**Mitigation**:
- Write a **shared "Beginner Experience Spec"** before implementing either feature. This spec defines:
  - What "beginner" means (concepts, metrics, language level)
  - Which content appears in beginner mode vs expert mode
  - Which concepts C163 must teach before users see them in beginner mode
- C163's 4 lessons must cover all concepts that appear in C40's beginner mode. If beginner mode shows P/E, C163 must teach P/E.

### Risk 5: C163 Replacing C103 Cleanly (Severity: P2)

**Risk**: The existing `first_visit_guide.py` (C103) already has a `first_visit_dismissed` session state key. If C163 uses a different key or doesn't clean up the old one, users who saw C103 might not see C163 (or vice versa).

**Mitigation**:
- C163 MUST use the same `first_visit_dismissed` session state key as C103 for backward compatibility.
- `first_visit_guide.py` must be **deleted** from the codebase (not just disabled) to avoid import conflicts.
- The "新手導覽" page entry must be removed from the router page list.

### Risk 6: Mode Toggle State Loss on Session Expiry (Severity: P3)

**Risk**: If the Streamlit session expires, the user's mode preference is reset to beginner, which could frustrate expert users.

**Mitigation**:
- For Sprint 20, session-level persistence is acceptable (st.session_state).
- Future enhancement: Add a "記住我的設定" option that stores the preference in a cookie or URL parameter.

### Risk 7: Mobile Responsiveness of 4-Lesson Gate (Severity: P2)

**Risk**: 4 full-screen lessons on mobile could feel like too much content. The 26-tab navbar is already problematic on mobile.

**Mitigation**:
- Each lesson must be compact: visual content scaled for mobile viewport.
- Progress dots must be visible on mobile (don't rely on horizontal space).
- The "跳過教學" link must be accessible on mobile without horizontal scrolling.
- The gate should be tested on mobile viewport (375px width) before shipping.

---

## Design Recommendations

### For C163 (Learn First Gate)

1. **Format: Full-page, 4-lesson progressive walkthrough** — NOT a modal, NOT a slide-over. A dedicated page in the router that replaces C103.

2. **Content: 4 micro-lessons covering** — (1) What is stock ownership, (2) How companies make money (revenue), (3) Key metrics (P/E + ROE), (4) What is Stock Explorer (historian positioning). Each lesson: one key point, one analogy, one visual.

3. **Soft gate with skip** — Always-visible "跳過教學" link. Gate encourages but never requires learning.

4. **Replace C103, don't coexist** — Delete `first_visit_guide.py`, remove "新手導覽" from router. Same session state key (`first_visit_dismissed`).

5. **PPT-style compliance** — Each lesson screen follows PPT rules: one key point, charts > 60%, text ≤ 40 characters for key point, analogy ≤ 2 sentences.

6. **Competitor reference** — Model the gate on Webull's "Learn First" soft gate + Stash's 2-card micro-lesson pattern + Tastytrade's progressive encouragement.

### For C40 (Beginner/Expert Mode)

1. **Toggle placement: Zone B sidebar** — Above the search box, always visible when sidebar is expanded. **NOT** in Zone A navbar (violates "no interactive controls" rule). Use `st.radio` with "🌱 新手模式" / "🔬 進階模式".

2. **Scope: All stock pages** — Business card, operation checkup, financial health, peer comparison, group structure, category browse, ETF zone. Every page must have a beginner mode definition.

3. **Beginner mode content: 3-5 key sections per page** — Hide advanced sections behind collapsed expanders labeled "🔬 🔰 進階內容". Show the most important content first (revenue, key ratios, top peers).

4. **Visual indicator** — Subtle beginner mode banner at the top of Zone C: yellow background (#FEF9E7), "🌱 新手模式" text.

5. **Instant switching** — Mode change must be instant (< 0.5s), no data reload. Only DOM visibility changes.

6. **Default: Beginner** — All new users start in beginner mode. No onboarding quiz needed for Sprint 20 (C130 Investor Profile Quiz is a future enhancement).

7. **Competitor reference** — Model the toggle on Sharesies' complexity level selector (sidebar placement) + NerdWallet's "Simple View" toggle (persistent, both options visible).

### Cross-Cutting: Shared "Beginner Experience Spec"

**Critical prerequisite**: Before coding C163 or C40, write a shared spec that defines:
- What "beginner" means across the entire product (concepts, metrics, language level)
- Which content appears in C163's 4 lessons
- Which sections are hidden/shown in C40's beginner mode per page
- How C163 and C40 reference each other (e.g., C163 teaches P/E → C40 beginner mode hides advanced P/E analysis)

This spec prevents the #1 design risk: C163 and C40 defining "beginner" differently.

### Implementation Priority Within Sprint 20

1. **First**: Write the shared "Beginner Experience Spec" (2-3h, PM + Designer)
2. **Second**: Implement C163 Gate page (8-10h, Developer) — this unblocks C40 content design
3. **Third**: Write C163 lesson content (3-4h, PM, parallel with coding)
4. **Fourth**: Implement C40 sidebar toggle + per-page beginner mode (8-10h, Developer)

---

*Designer: Design Reviewer*
*Date: 2026-06-14*
*Status: Ready for PM review and Developer handoff*
*Next step: PM to approve per-page beginner mode spec before coding begins*
