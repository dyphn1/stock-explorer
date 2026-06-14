# Designer Discussion Analysis — Round 40

## UX Impact Assessment

| Feature | UX Impact | Design Effort | Alignment with Design System |
|---------|-----------|---------------|------------------------------|
| C167 (AI Screener Explanations) | **High** | 14-18h | ✅ Strong — plain-language is core to "historian" positioning; screener is a new entry point that needs the same PPT-style treatment |
| C152 (Multi-Factor Event Narratives) | **High** | 16-20h | ✅ Strong — directly extends the "story first" principle; combines existing event data into unified narrative, reinforcing "historian" over "stock picker" |
| C163 (Learn First Gate) | **Medium** | 8-12h | ⚠️ Moderate — aligns with "beginner-friendly" principle but risks adding friction before value delivery; must not violate the "ten-second test" by making users wait |
| C37 (Key Takeaways Summary Card) | **High** | 6-8h | ✅ Strong — directly addresses the "ten-second test" design principle; highest ROI per hour; synthesizes scattered metrics into scannable summary |
| C40 (Beginner/Expert Mode Toggle) | **Medium** | 10-14h | ✅ Strong — aligns with "progressive drill-down" and "point-to-point knowledge construction"; but adds a persistent UI control that must not clutter Zone A |
| C36 (Visual Revenue Tree) | **Medium** | 10-14h | ✅ Strong — extends existing pie chart into hierarchical view; aligns with PPT-style "one key point per page" and "image-first" principles |
| C39 (What Changed Recently Delta Card) | **High** | 8-10h | ✅ Strong — makes data feel alive and relevant; plain-language delta explanations reinforce "historian" positioning; high impact for low effort |
| C41 (Read Next Recommendations) | **Low-Medium** | 6-8h | ⚠️ Moderate — supports discovery and "point-to-point knowledge construction" but is a secondary feature; doesn't directly address core UX gaps |

## Recommended Priority (Design Perspective)

### 1. C37 — Key Takeaways Summary Card (P2, 6-8h)

**Why this UX matters:**
This is the single highest-ROI feature for the "ten-second test." Currently, a beginner opening TSMC's page sees 15+ metrics scattered across sections with no synthesis. The competitor research (Round 8) confirms that Seeking Alpha and Public.com both have this pattern — it's becoming table stakes for narrative-driven stock tools. Simply Wall St's "snowflake" diagram proves that a single synthesized visual can replace minutes of data scanning. Without a summary card, Stock Explorer violates its own core design principle on every single page load.

**Design direction:**
- Position as the **first element in Zone C**, below the Zone A tabs but above all other content
- Use a **card with blue left border** (info card pattern from Section 3.3 of design system) — consistent with existing metric cards
- 3-5 bullet points, each ≤ 200 characters total across all bullets (per PPT-style text limits in Section 5.2)
- Each bullet follows the pattern: `① [Metric] → [Plain-language meaning]` — e.g., "① 毛利率55% → 每賣100元賺55元，代表產品很有競爭力"
- Auto-generated from existing `key_takeaways.py` service (already built per architect analysis)
- **No interactive controls** — this is a pure display element (Zone C principle: no interactive controls mixed with data)

**Components needed:**
- Reuse existing info card HTML pattern (blue border, `#F8F9FA` background, 12px border-radius)
- Bullet list rendered via `st.markdown` with numbered emoji markers
- Data sourced from `key_takeaways.py` service → rendered by `_summary.py` section module

**Layout approach:**
```
Zone A: [Company] [Price] [Tabs...]
Zone B: [Sidebar nav]
Zone C:
  ┌─────────────────────────────────────┐
  │ 📋 重點摘要 (blue border card)       │
  │ ① ... ② ... ③ ...                  │
  └─────────────────────────────────────┘
  ─── (st.markdown("---"))
  [Rest of page content...]
```

**Ten-second test validation:** A user reading this card for 10 seconds should be able to say "TSMC makes most of the world's advanced chips, has very high margins, and has been growing steadily." ✅

---

### 2. C39 — What Changed Recently Delta Card (P2, 8-10h)

**Why this UX matters:**
Static data feels dead. Koyfin and Finary both highlight recent changes because it's the #1 way to make financial data feel relevant to beginners. Currently, Stock Explorer shows 3-year charts but a beginner doesn't know what to look at — the signal is buried in the noise. This card acts as a "narrative cursor" that points to what matters right now. It directly supports the "historian" positioning: "here's what happened recently" rather than "here's what to buy."

**Design direction:**
- Position **below the Key Takeaways card** but **above charts** in Zone C
- Use a **warning-style card** (orange/yellow border, `#FEF9E7` background) to signal "attention needed" — distinct from the blue info card
- Show 2-3 significant changes (>10% delta) with directional indicators: `📈` for positive, `📉` for negative
- Each delta follows the pattern: `[Direction] [Metric] from X% to Y% → [Plain-language explanation of why]`
- Example: "📈 最近3個月營收成長15%，是過去一年最快的增速 → 因為AI晶片需求大增"
- Time comparison: current 30 days vs previous 30-60 days (configurable in service layer)
- If no significant changes, show a subtle "✅ 近期無重大變化" message (don't hide the card — consistency matters)

**Components needed:**
- New card variant: "delta card" with orange left border (`#F39C12`) and `#FEF9E7` background
- Reuse `delta_engine.py` (already built) for change detection
- Reuse `delta_explanation_provider.py` for plain-language explanations
- Directional emoji as visual indicators (not color-only, for accessibility)

**Layout approach:**
```
Zone C:
  [Key Takeaways Card]
  ───
  ┌─────────────────────────────────────┐
  │ 🔄 最近有什麼變化 (orange border)    │
  │ 📈 營收 +15% → AI晶片需求大增       │
  │ 📉 毛利率 -3% → 價格競爭加劇        │
  └─────────────────────────────────────┘
  ───
  [Charts...]
```

**Ten-second test validation:** "TSMC's revenue grew 15% recently because of AI chip demand, but margins dipped slightly due to pricing pressure." ✅

---

### 3. C152 — Multi-Factor Event Narratives (P1, 16-20h)

**Why this UX matters:**
This is the most strategically important P1 feature because it's where Stock Explorer's "historian" positioning becomes truly differentiated. Currently, events are shown as individual timeline entries. But real business stories are multi-factor: "TSMC's revenue grew BECAUSE of AI demand AND because they expanded 5nm capacity AND because Apple switched from Samsung." No competitor connects these dots into a single narrative. Stocksera has a "Story" tab but it's AI-generated without structured multi-factor composition. This feature turns Stock Explorer from "a tool that shows data" into "a tool that tells the company's story."

**Design direction:**
- Add a new **"故事" (Story) tab** in Zone A's tab bar, positioned after "Business Card"
- Each story page follows the **PPT-style one-key-point-per-page** principle: one story = one page = one core message
- Story structure:
  1. **Headline**: One sentence summarizing the story (≤ 15 characters for tagline, ≤ 50 for headline)
  2. **Narrative body**: 3-5 sentences weaving together events, metrics, and context (≤ 200 characters total)
  3. **Supporting chart**: One visualization that illustrates the story (chart occupies > 60% of page)
  4. **Key factors**: 2-3 factor chips/tags showing what drove this story
- Use the existing `compose-and-enrich` pipeline (`timeline_service.py`) to merge events + case studies + milestones
- Stories are **chronologically ordered** with the most recent first
- Navigation between stories uses simple "← 上一個故事 / 下一個故事 →" buttons at the bottom of Zone C

**Components needed:**
- New page template following existing PPT-style page pattern
- Story card component: extends the tip card pattern (orange border) with narrative text
- Factor chips: small inline tags using `#3498DB` blue background with white text, `border-radius: 16px`
- Story navigation buttons: reuse existing button pattern with `use_container_width=False`
- Data from `timeline_service.py` → enriched `TimelineEntry` dicts with multi-factor composition

**Layout approach:**
```
Zone A: [Company] [Price] [Business Card] [**故事**] [Operational Checkup] ...
Zone B: [Sidebar nav]
Zone C:
  ┌─────────────────────────────────────┐
  │ 📖 2024年AI晶片爆發的故事            │
  │                                     │
  │ [3-5 sentence narrative weaving     │
  │  together events and metrics]       │
  │                                     │
  │ [Factor chips: AI需求] [5nm量產]    │
  │                                     │
  │ ┌─────────────────────────────────┐ │
  │ │                                 │ │
  │ │    [Plotly chart - 60%+ area]   │ │
  │ │                                 │ │
  │ └─────────────────────────────────┘ │
  │                                     │
  │ [← 上一個故事]    [下一個故事 →]    │
  └─────────────────────────────────────┘
```

**Ten-second test validation:** "In 2024, TSMC's revenue surged because AI chips were in huge demand, they ramped up 5nm production, and Apple switched more orders from Samsung." ✅

---

## Design System Updates Needed

### 1. New Card Variant: Delta Card
The design system currently defines info cards (blue border) and tip cards (orange border). C39 requires a new **delta card** variant:
```html
<!-- Delta card (orange/yellow border) -->
<div style="background:#FEF9E7;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">🔄 最近有什麼變化</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.8;">
        📈 營收 <span style="color:#27AE60;font-weight:600;">+15%</span> → AI晶片需求大增<br>
        📉 毛利率 <span style="color:#E74C3C;font-weight:600;">-3%</span> → 價格競爭加劇
    </div>
</div>
```

### 2. New Component: Factor Chips
C152 requires inline factor tags. These are new to the design system:
```html
<!-- Factor chip (blue) -->
<span style="display:inline-block;background:#3498DB;color:#fff;padding:0.2rem 0.6rem;border-radius:16px;font-size:0.8rem;margin:0.2rem;">AI需求</span>
<!-- Factor chip (green for positive) -->
<span style="display:inline-block;background:#27AE60;color:#fff;padding:0.2rem 0.6rem;border-radius:16px;font-size:0.8rem;margin:0.2rem;">5nm量產</span>
<!-- Factor chip (red for negative) -->
<span style="display:inline-block;background:#E74C3C;color:#fff;padding:0.2rem 0.6rem;border-radius:16px;font-size:0.8rem;margin:0.2rem;">價格競爭</span>
```

### 3. Zone A Tab Bar Extension
Adding a "故事" tab to Zone A requires updating the tab bar specification. The tab bar currently lists 9 tabs. The new tab should be inserted after "Business Card" (position 1) to maintain logical flow: overview → story → operational → financial → comparison.

### 4. Summary Card Typography
The Key Takeaways card needs a new typography treatment for numbered bullets. Update Section 5.4:
- Takeaway bullets: `font-size: 0.9rem, color: #2C3E50, line-height: 1.8`
- Numbered markers: `font-weight: 700, color: #3498DB`

### 5. Empty State for Delta Card
When no significant changes exist, the delta card should show a subdued "no changes" state rather than disappearing. Add to Section 4.4:
- No significant deltas: show `st.info("✅ 近期無重大變化，所有指標穩定")` styled as a mini card within the delta card area

### 6. Story Page Navigation Pattern
C152 introduces sequential page navigation (story N-1 → story N → story N+1). This is a new interaction pattern that should be added to Section 4:
- Story navigation uses `st.button` with `use_container_width=False`
- Buttons positioned at bottom of Zone C, centered
- State managed via `session_state["story_index"]`
- Boundary handling: disable "previous" on first story, disable "next" on last story (don't hide — show disabled state)

---

## Competitive Design Patterns to Reference

### From Simply Wall St (Round 9)
- **Snowflake Analysis**: The gold standard for "ten-second test" design. Stock Explorer's Key Takeaways card (C37) should aspire to the same synthesis quality — a beginner looks at it and immediately understands the company's situation.
- **Infographic-style layout**: Simply Wall St proves that visual-first stock pages work for beginners. Stock Explorer's PPT-style approach is validated by this parallel.
- **Progressive disclosure**: Simply Wall St shows summary first, details on click. This directly supports the Beginner/Expert toggle (C40) as a future enhancement.

### From Seeking Alpha (Round 8)
- **Key Takeaways / Quick Summary**: The exact pattern C37 implements. Seeking Alpha shows 3-5 bullet points at the top of each analysis article. Stock Explorer should adapt this for the business card page.
- **Side-by-side comparison**: Seeking Alpha's compare mode validates the "Compare Stories" concept (C38, future sprint).

### From Public.com (Round 8)
- **Story cards**: Public.com's narrative cards are the closest competitor to Stock Explorer's "historian" positioning. C152's multi-factor narratives should study Public.com's card layout for inspiration.
- **Revenue tree**: Public.com's hierarchical revenue breakdown validates C36 (Visual Revenue Tree) as a competitive gap.

### From Koyfin (Round 8)
- **Recent changes highlighting**: Koyfin's "What's New" section is the direct inspiration for C39. Koyfin uses color-coded badges for metric changes — Stock Explorer should use directional emoji + plain-language for better accessibility.
- **Dashboard narratives**: Koyfin shows that even data-dense platforms benefit from narrative summaries.

### From 財報狗 / StatementDog (Round 9)
- **Stock screener as discovery**: 財報狗's #1 feature is screening. This validates C167 (AI Screener Explanations) — but Stock Explorer must differentiate by adding plain-language explanations to screener results, which 財報狗 lacks.
- **P/E Band Chart**: Shows historical valuation visually. This is a future feature candidate (not in Sprint 20) but validates the "visual-first" approach.

### From Investopedia (Round 9)
- **Concept-first approach**: Investopedia teaches concepts before showing data. This aligns with C163 (Learn First Gate) but also informs how C152's stories should be structured — teach the concept, then show the data.
- **Financial Dictionary**: Validates the glossary feature (C33, already planned) as essential infrastructure.

### Key Competitive Insight
**No TW competitor combines narrative + plain-language + visual-first.** 財報狗 has screening but no narratives. Yahoo has data but no education. JZ Invest has community but no structured stories. Stock Explorer's "historian" positioning is a genuine white space in the TW market. C37 (Key Takeaways) and C152 (Multi-Factor Narratives) are the two features that most directly defend this positioning against international competitors entering the TW market.

---

## Summary of Recommendations

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **1st** | C37 (Key Takeaways) | Highest ROI, directly fixes "ten-second test" violation, lowest effort (6-8h), already partially built |
| **2nd** | C39 (Delta Card) | Makes data feel alive, low effort (8-10h), no TW competitor has this with plain-language |
| **3rd** | C152 (Multi-Factor Narratives) | Strategic differentiator, defends "historian" positioning, but higher effort (16-20h) — start design in Sprint 20, implement across Sprint 20-21 |

**Defer to Sprint 21+:** C167 (AI Screener — needs C37/C39 as foundation), C40 (Mode Toggle — needs more user research on what "beginner" means), C36 (Revenue Tree — nice-to-have visual enhancement), C163 (Learn First Gate — risks adding friction), C41 (Read Next — secondary discovery feature).
