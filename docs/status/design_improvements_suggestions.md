# Design Improvement Suggestions

Based on review of `docs/status/current_problems.md`, `docs/domain/design_system.md`, and competitor research (`docs/research/competitor_research.md`), the following design improvements are recommended.

## Priority & Effort Summary

| ID | Suggestion | Priority | Effort | Notes |
|----|------------|----------|--------|-------|
| D-003 | Replace inline HTML cards with shared components (`_router_base.py`) and create additional card types (summary, warning) as needed. | P1 | 2-3h | Inconsistent card styling across pages |
| D-004 | Copy `docs/domain/design_system.md` to `docs/design/design_system.md` (expected path). | P1 | 0.5h | Missing design system documentation |
| D-005 | Apply “one new card per page per sprint” principle; use progressive disclosure (expandable sections) for less critical content; consider beginner‑mode default. | P1 | 3-4h | Business Card page overload risk |
| D-006 | Add mobile‑specific CSS that stacks columns vertically, increases touch‑target sizes, and adjusts chart heights. Consider mobile‑first redesign for Business Card. | P1 | 4-6h | Mobile responsiveness gaps |
| D-007 | Implement stock screener (C42) with beginner‑friendly presets (“穩定收息”, “成長潛力”, “便宜估值”） and card‑based results. | P1 | 5-8h | No discovery mechanism |
| D-016 | Create `_summary_card()` component with orange/amber styling (`border-left:4px solid #F39C12`, `background:#FFF8F0`) for C37 (Key Takeaways). | P1 | 0.5h | Missing hero card style |
| D-018 | Move C39 block (What Changed) to immediately after C37, before the “關鍵數字三連卡” section. | P1 | 0.25h | Placement too low |
| D-021 | Pass underlying metric values (ROE, gross margin, etc.) into hover templates for each dimension and add plain‑language explanation below each dimension card. | P1 | 1-2h | Missing per‑dimension explanations |
| D-008 | Standardize on a single spinner per page transition; consider skeleton loading for chart areas. | P2 | 1-2h | Loading state inconsistency |
| D-009 | Create a standardized empty‑state component with consistent messaging and styling. | P2 | 1h | Error state inconsistency |
| D-010 | Redesign watchlist using card‑based layout consistent with other pages (each item as a card with key info and actions). | P2 | 2-3h | Non‑PPT layout |
| D-011 | Redesign category browser with larger cards, fewer items per row, and more visual hierarchy; consider a “featured stock” card at top of each category. | P2 | 2-3h | Dense tables |
| D-012 | Implement glossary/tooltip system (C33): create `src/data/glossary.yaml` and add hover/tooltips on financial terms across all pages. | P2 | 8-12h | No glossary/tooltip system |
| D-013 | Implement risk analysis (C44: “What Could Go Wrong”) with 3‑5 key risks in plain language with historical evidence. | P2 | 3-4h | No risk analysis section |
| D-015 | Implement financial education academy (C47): 10‑15 structured lessons organized by difficulty, using real TW stock examples. | P2 | 8-12h | No structured learning path |
| D-017 | Change C37 bullet cap from 5 to 3 to match spec and enforce brevity. | P2 | 0.1h | Bullet count exceeds spec |
| D-019 | Add `return deltas[:2]` at end of `compute_recent_deltas()` to enforce 2‑delta cap. | P2 | 0.1h | Missing delta count cap |
| D-020 | Apply inline color styling to delta text: green (`#27AE60`) for positive, red (`#E74C3C`) for negative. | P2 | 0.5h | Missing directional color coding |
| D-022 | Move C43 block (snowflake chart) to immediately after C37, before C39 and key metrics. | P2 | 0.25h | Placement not near top |
| D-023 | Extend C45 valuation window to 5 years (1825 days) if data available; add fallback with note if <2 years. | P2 | 0.5h | Uses 2‑year window instead of 5‑year |
| **Competitive‑gap suggestions** | | | | |
| NOTIF | Implement notification system (Line/Email/Push) for M5 event detection (C02). | P0 | 6-10h | All competitors have notifications; M5 engine wasted without it |
| HEALTH | Implement visual health score (snowflake‑style) like Simply Wall St (C14). | P1 | 8-12h | Competitors have health scores; aligns with benchmark‑oriented value |
| EXPORT | Add PPT/PDF export leveraging existing PPT‑style CSS (C06). | P1 | 4-6h | Competitor WantGoo has one‑click export |
| LEARN | Implement structured learning path (C47) – already listed above; reiterate as competitive gap. | P2 | 8-12h | Competitors have academies/courses |
| MARKET | Add market mood index on homepage using institutional buy/sell surplus + volume + advance/decline ratio (C35). | P1 (conditional) | 10-12h | Beginner‑friendly market overview |
| STORY | Implement company story timeline/narrative (C34) weaving events, revenue, price into chronological narrative. | P2 | 16-24h | Unique differentiator; no competitor has narrative timeline |
| REV_TREE | Add visual revenue tree (treemap/sunburst) extending revenue pie chart (C36). | P2 | 10-14h | Helps beginners understand business model visually |
| KEY_TAKE | Add auto‑generated “Key Takeaways” summary card at top of business card (C37). | P2 | 6-8h | Directly addresses ten‑second test |
| COMP_STORY | Add side‑by‑side narrative comparison mode (C38) to peer comparison page. | P2 | 12-16h | Extends benchmark advantage with narrative layer |
| RECENT | Add “What Changed Recently” delta card (C39) highlighting significant metric changes (>10%) with plain‑language explanations. | P2 | 8-10h | Makes data feel alive and relevant |
| TOGGLE | Add Beginner/Expert mode complexity toggle (C40) in navbar to hide/show advanced sections. | P2 | 10-14h | Aligns with progressive drill‑down principle |
| READ_NEXT | Add “Read Next” recommendation engine (C41) based on industry, parent‑subsidiary, customer‑supplier relationships. | P2 | 6-8h | Creates learning path through business relationships |

## Key Themes
1. **Consistency & Design System** – enforce shared components, fix documentation gap.
2. **Progressive Disclosure & Beginner‑Friendly** – overload reduction, beginner mode, guided discovery.
3. **Mobile Responsiveness** – improve Stack layout and touch targets.
4. **Narrative & Synthesis** – story timelines, key takeaways, revenue trees, compare‑stories, recent‑changes cards.
5. **Competitive Parity** – notifications, health score, export, glossary, learning path, market mood.
6. **Specification Adherence** – bullet caps, delta caps, color coding, placement fixes.

These suggestions address the P1/P2 issues logged in `current_problems.md` and close the most significant UI/UX gaps identified in competitor research.