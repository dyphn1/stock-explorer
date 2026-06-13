## 2026-06-13 Design Review — Sprint 14 Feature Candidates

> **Author**: Design Reviewer
> **Context**: Sprint 13b COMPLETE (C46 Moat Analysis + C36 Revenue Tree). Design Grade A (18th consecutive A/A-)
> **Scope**: Sprint 14 candidates — C47 Education Academy, C40 Mode Toggle, C123 Revenue Geography, C125 Segment Profitability, C126 Moat Comparison — UX evaluation and design direction

---

### Current Design State

After 18 consecutive A/A- design grades, the design system is mature and disciplined. The Business Card page is the central hub, now featuring 15+ sections across C33 (Glossary), C36 (Revenue Tree), C37 (Key Takeaways), C39 (What Changed), C43 (Snowflake), C44 (Risk), C45 (Valuation Band), C46 (Moat), and C48 (Story Card). The page already risks "super page" overload (flagged in D-005 since Round 9, flagged again in Round 27). Any new feature must be evaluated not just on its own merit, but on its impact on the overall information architecture.

**Key design debt entering Sprint 14**:
- D-005: Business Card page overload remains unresolved. 15+ sections compete for attention.
- D-003: Inconsistent card styling (partially fixed, but regressions on new pages).
- D-006: Mobile responsiveness gaps (no improvement since Round 9).
- D-079/D-080: Tooltip text issues (partially addressed in Sprint 13b).

**New navigation tab established**: Sprint 13b added "🏰 護城河分析" (Moat Analysis) as a Business Card section. C46's moat analysis is now a foundational element that C126 Moat Comparison must extend.

---

### UX Impact Analysis

#### C47 Education Academy — Structured Learning Path

- **UX Impact**: HIGH — This is the most architecturally significant feature since the original Business Card page. It introduces a **second navigation paradigm**: from "explore a company" to "learn a concept." This fundamentally changes the product from a stock reference tool into an education platform. The competitor research confirms this direction: Zerodha Varsity (14 modules), Investopedia Academy, Finary's "Learn" section, and Sharesies' "Discover" section all prove demand. However, no competitor combines structured curriculum WITH real-time stock data — this is Stock Explorer's unique angle.

- **Design Direction**:

  **Placement: New Zone B nav item + standalone Zone C page.** Following the Round 15 designer recommendation (discuss_designer_round15.md, line 73): Use a **left-side progress indicator in Zone B** for learning modules. This is a **conscious exception** to the "Zone B must not contain page content" rule — learning navigation is fundamentally different from stock navigation.

  **Page structure** (PPT-style applied to education):
  ```
  Zone A: Navbar (unchanged, company name hidden on Academy pages)
  Zone B: Learning progress sidebar
    ├── Module 1: What is Revenue? ✅
    ├── Module 2: What is ROE? ✅
    ├── Module 3: What is P/E? 🔒 (locked)
    ├── Module 4: What is a Moat? 🔒
    └── Module 5: How to Read a Balance Sheet? 🔒
  Zone C: Lesson content area
    ├── Hero card: Module title + one-sentence summary
    ├── Concept card: Plain-language explanation (≤ 200 chars)
    ├── Example card: Real TW stock example (e.g., TSMC)
    ├── Quiz card: 3 multiple-choice questions
    └── Next module: "接著學" button
  ```

  **Visual approach**: Each lesson follows the **card stack** model established in Round 15's PPT-Style 2.0 direction. Hero card → Concept card → Example card → Quiz card. Maximum 5 cards per lesson page (consistent with "max 5 cards per page section" principle). Quiz cards use `st.radio` for multiple choice, with immediate feedback ("✅ Correct! TSMC's ROE of 25% means..." / "❌ Not quite. Try thinking about it this way...").

  **Progress tracking**: Use `session_state` to track completed modules. Store in format `{"module_1": "completed", "module_2": "in_progress", ...}`. Show a **"學習進度"** badge in Zone B next to the Education Academy nav item (e.g., "2/5 完成").

  **Competitor reference**: Zerodha Varsity is the best model — 14 numbered modules with sequential unlock. Our adaptation: fewer modules (5 in v1), each with a real TW stock example (Zerodha uses generic examples), and integrated with the existing glossary system (C33) so technical terms in lessons are automatically linked.

- **Risks**:
  | Risk | Severity | Mitigation |
  |------|----------|------------|
  | Content creation burden (8-12h of high-quality writing) | P1 | Phase 1: 5 lessons only. Use existing analogy_engine.py patterns for consistency. |
  | Learning navigation in Zone B conflicts with stock navigation | P1 | Use a **collapsible subsection** in Zone B. Default collapsed. Label: "📚 學習中心". Only expands when user clicks it. |
  | Quiz interaction may violate PPT-style simplicity | P2 | Keep quizzes to 3 questions max. Use `st.radio` (Streamlit native). No animations. |
  | Text volume per lesson may exceed 200-char limit | P2 | Strict card budget: Hero (30 chars) + Concept (80 chars) + Example (60 chars) + Quiz (30 chars per question) = ~260 chars for quiz question text only. The concept + example cards must stay within 140 chars combined. |
  | Maintenance cost of curriculum as new features are added | P2 | Lessons are independent YAML files (`academy_lessons.yaml`). New lessons can be added without touching existing ones. Each lesson file is self-contained. |
  | Navigation confusion: "Am I in stock mode or education mode?" | P1 | Use visual mode indicator in Zone A: When in Education Academy, show a book icon (📚) next to the navbar title. When viewing a stock, show the company name. Never show both simultaneously. |

- **Placement**: Zone B (nav item) + Zone C (standalone page). NOT on the Business Card page. This feature is too large and conceptually different to embed as a Business Card section. It deserves its own page.

---

#### C40 Mode Toggle — Beginner/Expert Complexity Toggle

- **UX Impact**: MEDIUM — C105 already implements a basic toggle (`簡易/詳細`) on the Business Card page (confirmed in feasibility analysis line 67: "C105 已實現 `簡易/詳細` toggle（在 `_main.py` 內 `st.toggle`）"). C40 is an **expansion** of this concept: moving the toggle to the navbar (Zone A) and making it global (affects all pages, not just Business Card). The UX question is: what does "beginner mode" actually hide/show across the entire application?

- **Design Direction**:

  **Placement: Zone A (navbar), right side, next to existing elements.** The toggle should be a **pair of `st.button` elements styled as a segmented control** (matching the existing tab pattern). Use compact sizing so it doesn't dominate the navbar.

  ```
  Zone A: [Company Name 2330.TW] [Tabs...]    [🌱 新手 | 🔬 專家]
  ```

  **Scope of Beginner Mode** (what gets hidden/simplified):
  - **Business Card**: Show only Sections 1-3 (C37 Summary, C39 What Changed, C43 Snowflake). Hide everything below in a "顯示更多分析" expander. In Beginner Mode, the Business Card becomes a true "business card" — one glance, three key sections, done.
  - **Peer Comparison**: Show only side-by-side metric comparison (no moat comparison, no risk comparison). Label it "跟同業第一名的比較" instead of "Peer Comparison."
  - **Financial Health**: Show only revenue and profit charts (hide debt analysis, cash flow details). Label it "賺了多少錢" instead of "Financial Health."
  - **Operational Checkup**: Show only revenue trend and margin trend (hide detailed ratio analysis). Label it "生意穩定嗎" instead of "Operational Checkup."
  - **Group Structure**: Unchanged (already simple — point-to-point mapping).
  - **Education Academy**: Unchanged (always visible in Zone B).

  **Expert Mode**: Current behavior (everything visible). No changes needed.

  **Session persistence**: Store as `session_state["mode"]` = `"beginner"` or `"expert"`. Persist across page navigation and stock switches. Do NOT reset to default when switching stocks.

  **Visual indicator**: Use emoji for instant recognition. 🌱 (seedling = beginner/growing) and 🔬 (microscope = expert/analytical). No text labels needed in the toggle itself — the emoji are universally understood. Add a `st.sidebar.markdown()` explanation only in the "關於" section.

  **Alternative considered**: `st.toggle` (like the existing C105). **Rejected** — a toggle implies binary on/off, but we want to feel like a level selector. Two buttons side-by-side communicate "choose your level" better than a toggle switch.

- **Risks**:
  | Risk | Severity | Mitigation |
  |------|----------|------------|
  | C105 toggle and C40 toggle do the same thing (redundant) | P1 | **Remove C105 toggle** when C40 is implemented. C40 supersedes C105. Do not have two toggles doing the same thing. |
  | Navbar already crowded with tabs | P2 | Mode toggle is a compact 2-button pair (~120px wide). If tabs + toggle exceed navbar width, collapse to a single `st.selectbox` in the sidebar instead. |
  | Beginner Mode hides too much useful information | P2 | Show a small "💡 進階模式可查看更多分析_info" banner at the bottom of the Business Card in Beginner Mode. One line, dismissible. |
  | Scope creep: every new feature needs Beginner/Expert variants | P2 | Define a **rule**: New features added in Expert Mode only by default. Beginner Mode gets new features only after they've been in Expert Mode for 1 sprint AND the feature has been simplified for beginners. |
  | Session_state mode not persisting across browser sessions | P3 | Acceptable limitation. Mode resets to "expert" on full reload. Add a note in the sidebar settings. |

- **Placement**: Zone A (navbar), replacing/removing the existing C105 toggle. Global scope — affects all pages.

---

#### C123 Revenue Geography — Where Customers Are

- **UX Impact**: LOW-MEDIUM — This is a natural companion to C36 Revenue Tree. Where C36 shows "what the company sells" (segment breakdown), C123 shows "who buys it" (geographic breakdown). Together they answer the complete "where does money come from" question. The competitor research is strong (Koyfin, Simply Wall St both have this). BUT the data availability is uncertain (flagged in Challenge Log Round 1: "C123 has uncertain data availability for TW stocks").

- **Design Direction**:

  **Placement: New section on the Business Card page, below C36 Revenue Tree.** If C36 is the "what" of revenue, C123 is the "where." Positioning it directly below C36 creates a natural flow: first understand what the company sells (treemap), then understand where customers are (geography). Use `st.expanded(expanded=False)` for this section — geography is interesting but not essential for the ten-second test.

  **Visual approach**: **Horizontal stacked bar chart** (NOT a world map). Here's why:
  - World maps are misleading for TW stocks: 65% of TSMC's revenue is "Americas" which is a huge geographic area. A map would show a giant colored blob across an entire continent.
  - Stacked bars are more precise: each segment = one region, length = percentage, color = region. Instantly readable.
  - Maps violate the "ten-second test" for geographic regions: "Is that 65% the US or all of North America?"
  - Stacked bars align with the existing chart style in the Business Card page (all other charts are bar/line/treemap, no maps exist).

  **Chart specification**:
  ```
  Horizontal stacked bar: [Americas 65%] [China 15%] [Europe 10%] [Others 10%]
  ```
  - Color palette: Blue家族 ( Americas `#3498DB`, China `#5DADE2`, Europe `#85C1E9`, Others `#AED6F1`). All shades of primary blue. Do NOT use red/green — these are not directional indicators.
  - Labels: Region name + percentage on or next to each segment.
  - Hover tooltip: Region, percentage, plain-language description (e.g., "美洲（65%）：主要客戶為Apple、NVIDIA、AMD等美國公司").
  - Height: 80px (compact, doesn't dominate the page).

  **Section header**: "營收地區 — 客戶在哪裡" with an info tooltip: "此公司在哪些地區有最多客戶？了解公司的市場分佈"

  **Data sourcing**: If FinMind has `taiwan_stock_revenue_by_region`, use it. Otherwise, manual curation for top 20 stocks with fallback to `st.info("此公司暫無地區營收資料")`. This is the **same fallback pattern established for C36**.

  **Competitor reference**: Koyfin uses a horizontal bar with world map as background decoration (visual only, not data). Simply Wall St has a "Geography" toggle in the revenue section. Our improvement: plain-language descriptions per region (competitors just show region name + %).

- **Risks**:
  | Risk | Severity | Mitigation |
  |------|----------|------------|
  | Data not available in FinMind for TW stocks | P1 | Manual curation for top 20 stocks (same as C36/C46 approach). Fallback message for others. |
  | Region categories are too broad ("Americas" = everything from Canada to Argentina) | P2 | Add plain-language clarification in hover: "美洲地區：包含美國、加拿大、墨西哥等" |
  | Adds another chart to an already chart-heavy Business Card | P2 | Chart is compact (80px). Stacked bar is visual-efficient. Total section adds < 150px of vertical space. |
  | Geographic data may be outdated quickly | P3 | Show data year in label (e.g., "2024年營收分佈"). |

- **Placement**: Zone C (Business Card page), as a new section below C36 Revenue Tree. Wrapped in `st.expander(expanded=False)`. Fallback for missing data is a single `st.info()` line.

---

#### C125 Segment Profitability — Margin by Segment

- **UX Impact**: LOW — This is a value-add to C36 Revenue Tree, not a standalone feature. It transforms the treemap from "what the company sells" to "where the money actually comes from" (revenue × margin = profit contribution). The competitor research is compelling (Simply Wall St has margin-per-segment), but the UX value is incremental: it adds margin information to an existing chart rather than creating a new visualization.

- **Design Direction**:

  **Placement: Enhancement to C36 Revenue Tree, NOT a new section.** Add a **toggle within the C36 section** (alongside the existing pie chart / treemap toggle):
  ```
  View toggle: [圓餅圖 ▎樹狀圖]
  Overlay toggle: [營收比例 ▎利潤貢獻]  ← NEW
  ```

  When "利潤貢獻" is selected, the treemap segments are **resized by profit contribution** instead of revenue contribution. A segment that is 80% of revenue but has only 10% margin will appear much smaller in "利潤貢獻" mode. This is the key insight: **the same data, viewed differently, tells a different story.**

  **Color coding**:
  - Revenue mode: Blue palette (existing, `#3498DB` family)
  - Profit contribution mode: Green/yellow/red based on segment margin (green `#27AE60` for margin > industry average, yellow `#F39C12` for near average, red `#E74C3C` for below average)

  **Plain-language summary**: One line below the chart:
  ```
  "晶圓代工佔營收78%，但貢獻了92%的毛利 — 這是台積電真正的金雞母"
  ```

  **Design note**: This toggle adds ZERO new text to the page (switches the interpretation of an existing chart). It strictly decreases cognitive load while increasing insight density. Exactly the kind of progressive disclosure the design system advocates.

  **Data sourcing**: Segment margin data is harder to get than segment revenue. Use FinMind `taiwan_stock_financial_statement` expense breakdown where available. Manual curation for top 20 stocks. Fallback: hide the toggle for stocks without segment margin data (don't show an option that doesn't work).

- **Risks**:
  | Risk | Severity | Mitigation |
  |------|----------|------------|
  | Segment margin data not available for most stocks | P1 | Hide toggle for stocks without data. Only show "利潤貢獻" option when curated data exists. |
  | Color shift from blue to green/yellow/red may confuse users | P2 | Add a legend above the chart in profit mode: "🟢 高毛利 🟡 中等 🔴 低毛利". Clear, simple, bilingual (color + emoji). |
  | Two toggles in one section may feel cluttered | P2 | Use `st.segmented_control` (renders as a single horizontal control, not two separate toggles). Maximum 4 options across both dimensions. |
  | Revenue-to-profit mental math may lose beginners | P2 | The plain-language summary does the interpretation work. Don't make users calculate "80% revenue × 60% margin = 48% profit contribution." |

- **Placement**: Zone C (Business Card), embedded within the existing C36 Revenue Tree section as a second toggle. No new section header, no new area. This is an enhancement, not a new feature.

---

#### C126 Moat Comparison — Side-by-Side Competitive Landscape

- **UX Impact**: MEDIUM — This extends C46 Moat Analysis (completed in Sprint 13b) from single-company to multi-company view. The Peer Comparison page already exists — C126 adds a **moat dimension** to it. Because C46 was built with a structured 5-dimension scorer (per Challenge Log Round 2 condition #3: "C46 scoring rubric must be comparison-ready for C126 in Sprint 14"), the comparison UI can reuse existing scoring logic.

- **Design Direction**:

  **Placement: New tab on the existing Peer Comparison page.** The Peer Comparison page currently shows metric-by-metric comparison. C126 adds a "🏰 護城河比較" tab alongside existing comparison tabs. This is architecturally clean: the comparison page is designed for multi-company views, and moat comparison is a special case of multi-company comparison.

  **Visual approach: Grouped horizontal bar chart (NOT radar chart)**. Here's why:

  **Radar chart rejected** because:
  - The existing C43 Snowflake on the Business Card already uses a radial visual for financial health. Using another radial visual for moat comparison would create visual monotony (same chart type everywhere).
  - Radar charts with 3-5 companies overlaid become cluttered lines (the "spaghetti chart" problem).
  - Radar charts fail the ten-second test for most users — the relative shape comparison requires training to read.

  **Grouped horizontal bar chart** (recommended):
  ```
  技術壁壘   TSMC ████████████████████ 寬  |  UMC ██████████████░░░░ 窄  |  Samsung ████████░░░░░░░░ 無
  品牌價值   TSMC ██████████░░░░░░░░ 窄  |  UMC ████████████████░░ 寬  |  Samsung ██████████████░░ 窄
  成本優勢   TSMC ████████████████████ 寬  |  UMC ████████████████████ 寬  |  Samsung ██████░░░░░░░░░░ 無
  網路效應   TSMC ████░░░░░░░░░░░░░░ 無  |  UMC ██████░░░░░░░░░░░░ 無  |  Samsung ████░░░░░░░░░░░░░░ 無
  轉換成本   TSMC ████████████████░░ 寬  |  UMC ██████████████░░░░ 窄  |  Samsung ████████████░░░░ 窄
  ```

  - Each dimension is a row. Each company is a colored bar within that row.
  - Bar width = moat width ( Wide = full, Narrow = 2/3, None = 1/3). This encodes the three moat levels as visual length.
  - Color per company (use a consistent palette: TSMC = blue `#3498DB`, UMC = orange `#F39C12`, Samsung = purple `#9B59B6`). Color legend at top.
  - Labels: Full-width bars show "寬護城河" inside the bar. Narrow bars show "窄護城河." None bars show "無護城河."

  **Alternative considered: Moat "card stack" comparison** — show 3 mini-cards (one per company) with 5 dimension indicators each, like C46's dimension cards but side-by-side. **Rejected** — this requires 15 dimension indicators (3 companies × 5 dimensions) which exceeds the text limit and violates "max 5 cards per page section." The grouped bar chart condenses 15 data points into 5 rows.

  **Plain-language summary**: Below the chart:
  ```
  "台積電在技術壁壘和轉換成本方面領先聯電。聯電在品牌價值方面兩者相當。"
  ```

  **Competitor reference**: Stockopedia shows "Moat Comparison" for UK stocks using a radar chart — but the labels are small and it requires training to read. Our grouped bar chart is more intuitive and more aligned with PPT-style "charts > text" principle. Morningstar has moat ratings (Wide/Narrow/None) but no multi-company comparison view — this is a white space.

- **Risks**:
  | Risk | Severity | Mitigation |
  |------|----------|------------|
  | Peer Comparison page already has many tabs | P2 | Audit existing tabs. If > 5 tabs, consolidate into "Comparisons" dropdown or secondary row. |
  | Grouped bar chart with 3+ companies becomes wide | P2 | Limit to max 3 companies in comparison (consistent with existing peer comparison scope). Show a "選擇同業" selector at the top to change which peers are shown. |
  | Moat scoring must be consistent across companies for fair comparison | P2 | Use the EXACTsame scoring function from C46's `moat_analyzer.py`. Do not recalculate separately for comparison. Call the same service function. |
  | Color palette for 3 companies may conflict with red/green meaning | P1 | Use blue/orange/purple for companies (not red/green). Red/green in the bar encodes moat width, not company identity. |

- **Placement**: Zone C (Peer Comparison page), as a new "🏰 護城河比較" tab. Reuses C46's scoring logic. Max 3 companies displayed. Grouped horizontal bar chart with color-coded bars per company, labeled by moat width.

---

### Design Recommendations

1. **C40 Mode Toggle should be the first feature implemented.** It is the lowest-risk, highest-leverage feature. The existing C105 toggle is already built — C40 just needs to move it to the navbar and expand its scope. Crucially, **every subsequent feature will be simpler to design once C40 exists**, because each feature can have a "Beginner Mode" variant without cluttering the base design. C40 enables all other features to be more ambitious while keeping the beginner experience clean.

2. **C125 Segment Profitability should be bundled with C36 in Sprint 14 (or deferred with C123).** C125 is not a standalone feature — it's an enhancement to C36. If C36 was just completed in Sprint 13b, adding the margin toggle is a natural follow-up (2-3h of additional work) that significantly increases C36's educational value.

3. **C123 Revenue Geography and C126 Moat Comparison can be tackled together.** Both are "companion" features (C123 extends C36, C126 extends C46) and both are P2 priority. They share the same design pattern: a new visualization appended to an existing section/page. Implementing them together creates a "Sprint 14: Expansion" theme that's coherent and manageable.

4. **C47 Education Academy should be a separate sprint or Phase 0 spike.** At 20-30h with 40-50% content creation, this is almost double the effort of a typical Sprint. Attempting it alongside 3-4 other features risks both quality and design consistency. Recommend: **Phase 0 (Sprint 14)** — build the page skeleton, navigation integration, and 2 lessons. **Phase 1 (Sprint 15)** — complete all 5 lessons with quizzes.

5. **Address D-005 (Business Card Overload) as a prerequisite to Sprint 14.** With C123 and C20 (geography), C125 (margin overlay on C36), the Business Card page grows to 17+ sections. Without C40's Beginner Mode to hide non-essential sections, the page will violate the "one key point per page" principle. This is the strongest argument for implementing C40 FIRST in Sprint 14.

---

### Priority Ranking (Design Perspective)

| Rank | Feature | UX Impact | Effort | Design Risk | Recommendation |
|------|---------|-----------|--------|-------------|----------------|
| 1 | **C40 Mode Toggle** | HIGH (enables all others) | LOW (4-6h*) | LOW | **DO FIRST** — unblocks simpler designs for all other features |
| 2 | **C125 Segment Profitability** | LOW (enhancement) | LOW (2-3h) | LOW | **BUNDLE with C36 follow-up** — high value, near-zero design risk |
| 3 | **C126 Moat Comparison** | MEDIUM | MEDIUM (10-14h) | MEDIUM | **DO with C123** — extends C46 cleanly, but needs grouped bar chart spec |
| 4 | **C123 Revenue Geography** | LOW-MEDIUM | LOW (8-12h) | MEDIUM | **DO with C126** — stacked bar is proven, but data risk needs fallback |
| 5 | **C47 Education Academy** | HIGH (strategic) | HIGH (20-30h) | HIGH | **PHASE 0** — start in Sprint 14, complete in Sprint 15. Content creation is the bottleneck |

*C40 effort is low because C105 already exists — this is expansion from card-level to navbar-level.

**Sprint 14 Recommended Scope:**
- **Must have**: C40 Mode Toggle (prerequisite for everything)
- **Should have**: C125 Segment Profitability + C123 Revenue Geography (companion features)
- **Could have**: C126 Moat Comparison (if time allows)
- **Won't have (this sprint)**: C47 Education Academy (Phase 0 only: skeleton + 2 lessons)

---

### Design System Updates Needed

If this plan is approved, the following design system changes are required:

1. **Section 3.3 (Cards)**: Add `_mode_toggle_button()` component for the C40 navbar toggle
2. **Section 3.4 (Charts)**: Add grouped horizontal bar chart spec for C126 Moat Comparison
3. **Section II (Layout)**: Document the "Education Academy Mode" — when in Academy mode, Zone A shows 📚 instead of company name
4. **Section V (PPT Spec)**: Add "lesson page" template for C47 Phase 0
5. **New Section VII**: "Beginner/Expert Mode" — define what each mode hides/shows across all pages

---

*This design discussion was prepared by the Design Reviewer for Sprint 14 planning. All recommendations align with the PPT-style design system (docs/design/design_system.md), the "historian, not stock picker" product positioning (docs/domain/product_vision.md), and 18 consecutive A/A- design quality standards. Key designer references: discuss_designer_round15.md (card stack pattern, Zone B learning nav exception), designer_discussion_r27.md (C36/C46 design specs that C123/C125/C126 extend).*
