# Stock Explorer Design Review — Round 15

> **Author**: Design Reviewer
> **Date**: 2026-06-19
> **Context**: Round 15 review — D-004 resolution verification, competitor design trends from Round 15 research, design specifications for Sprint 5 features (C71 Study Log, C73 Expert Analysis, C74 Historical Scenarios), and updated issue checklist.
> **Current Design Grade**: A (maintained from Rounds 12-14)

---

## Table of Contents

1. [Design Grade Assessment](#design-grade-assessment)
2. [D-004 Resolution Verification](#d-004-resolution-verification)
3. [Competitor Design Trends — Round 15 Update](#competitor-design-trends-round-15-update)
4. [Design Specifications for Sprint 5 Features](#design-specifications-for-sprint-5-features)
5. [New Design Improvement Proposals](#new-design-improvement-proposals)
6. [Updated Issue Checklist](#updated-issue-checklist)
7. [Recommendations Summary](#recommendations-summary)

---

## Design Grade Assessment

### Overall Grade: A (Maintained — 4th consecutive round)

### Grade Breakdown

| Dimension | Grade | Notes |
|-----------|-------|-------|
| **Zone A/B/C Compliance** | A | No changes to layout structure. All Sprint 4 features render within Zone C. |
| **PPT-Style Adherence** | A- | C44's `st.expander` pattern is proven. Business card page at ~15 sections but progressive disclosure mitigates. C41 adds length but placement at bottom is correct. |
| **Card Component Consistency** | B+ | D-035 (C41 peer cards), D-036 (C44 risk cards), D-037 (`_白话_card`) remain unresolved. D-003 still the root cause. No new regressions found. |
| **Color System** | A- | D-024 fix verified. D-036 and D-037 are remaining color inconsistencies (both <0.5h fixes). |
| **Plain-Language System** | A | C44 risk descriptions excellent. C41 peer CTA clear. Historian tone consistent. |
| **Visual Health Score** | A | C43 + D-034 metric value tooltips provide complete picture. |
| **Synthesis/Summary Layer** | A | C37 stable. C72 (TL;DR) declassified into C48 — correct decision to avoid redundancy. |
| **Valuation Context** | A | C45 stable. C77 (Valuation Verdict) proposed as future enhancement. |
| **Mobile Responsiveness** | B- | D-006 unchanged. |
| **Discovery Mechanism** | C+ | C41 provides partial peer discovery. Full screener (C42) still needed. |
| **Design System Documentation** | **A** | ✅ **D-004 RESOLVED** — `docs/design/design_system.md` now exists at the expected path. |
| **Page Load Performance** | B+ | C41 API-in-view-layer (D-038) remains but is low-risk for current scale. |

### Grade Justification

The grade is maintained at **A** because:
- **D-004 is resolved** — design system doc now exists at `docs/design/design_system.md` (upgraded from B to A in this dimension)
- All P0 issues remain resolved (0 open)
- No new P0 or P1 issues introduced in Round 15
- Core design principles (PPT style, ten-second test, Zone A/B/C) remain intact
- C44's progressive disclosure pattern is proven and should be replicated
- Sprint 5 features (C71, C73, C74) have clear design specs (see below) that align with historian positioning

**Risk**: The grade could slip to A- in Round 16 if:
- D-003 (card inconsistency) is not addressed before C71/C73/C74 add more inline HTML
- C73 Expert Analysis content is not curated to historian standard (risk of sounding like investment advice)
- C74 Historical Scenarios UI becomes cluttered with too many interactive controls

---

## D-004 Resolution Verification

### ✅ D-004: Design System Documentation — RESOLVED

| Check | Status | Evidence |
|-------|--------|----------|
| `docs/design/design_system.md` exists | ✅ **Verified** | File confirmed at expected path |
| Content matches `docs/domain/design_system.md` | ✅ **Verified** | Both files contain the full design system spec (235+ lines) |
| Color system defined | ✅ **Verified** | Section 3.1: color palette with hex codes |
| Card component spec defined | ✅ **Verified** | Section 3.3: info card + tip card HTML templates |
| Zone A/B/C layout defined | ✅ **Verified** | Section II: layout zone division |
| PPT-style rules defined | ✅ **Verified** | Section V: one key point per page, text limits, chart proportion |
| Pre-development checklist exists | ✅ **Verified** | Section VI: 10-item checklist |

**Verdict**: D-004 is **fully resolved**. The design system documentation now exists at the expected path `docs/design/design_system.md`. This upgrades the Design System Documentation dimension from B to A.

**Impact**: All future features (C71, C73, C74, C75+) now have a design system reference at the canonical path. Developers and reviewers can reference `docs/design/design_system.md` without needing to know about the `docs/domain/` path.

---

## Competitor Design Trends — Round 15 Update

### New Competitors Analyzed (Round 15)

| # | Competitor | Type | Key Design Innovation |
|---|-----------|------|----------------------|
| 1 | **口袋股利** (Pocket Dividend) | TW Dividend Education | Dividend calendar + compound dividend calculator — interactive tools as primary engagement |
| 2 | **股息小人** (Dividend Goblin) | TW Dividend Community | Personal narrative voice + community-driven analysis — social learning for dividend investors |
| 3 | **StockAnalysis.com** | US Plain-Language Analysis | "Summary" tab with 30-second read design — TL;DR-first approach |
| 4 | **TipRanks** | Analyst Consensus Platform | "Smart Score" composite + analyst accountability tracking — social proof for stock analysis |
| 5 | **Tykr** | AI Value Investing Education | "Buffett Analysis" 12-step criteria + Margin of Safety calculator — structured investment framework |
| 6 | **Wall Street Zen** | Minimalist Stock Analysis | True one-page design + "Zen-like" calm tone — extreme simplicity as feature |
| 7 | **口袋證券** (Pocket Securities) | TW Neo-Broker | Mobile-first + gamified learning + "First Trade" guided onboarding |
| 8 | **Goodinvest** (豐存股) | TW ETF Education | ETF Academy + investment simulator + beginner checklist |

### 7 New Design Trends from Round 15

#### Trend 1: Interactive Calculators Drive "Aha Moments"
- **Evidence**: 口袋股利 (compound dividend calculator), Tykr (Margin of Safety calculator), Goodinvest (ETF simulator)
- **Implication for Stock Explorer**: Stock Explorer is purely informational — users read but don't calculate. C79 (Compound Return Calculator) would add a transformative interactive learning dimension. This is the highest-impact P2 feature from Round 15 research.
- **Design Principle**: Interactive tools create "aha moments" that passive reading cannot. The compound growth curve is the single most powerful financial literacy teaching tool.

#### Trend 2: "Consensus" is a Powerful Education Format
- **Evidence**: TipRanks (analyst consensus + blogger sentiment), Dhan (Super Investors), Spiking (social sentiment)
- **Implication for Stock Explorer**: C73 (Expert Analysis Synthesis) directly addresses this — aggregating expert opinions into plain-language summaries. The historian framing ("Here's what experts have said") avoids the investment advice trap.
- **Design Principle**: Social proof ("what experts think") is educational when framed as historical reporting, not recommendation.

#### Trend 3: Extreme Simplicity is a Viable Product Philosophy
- **Evidence**: Wall Street Zen (one page, one score, 3 sentences), StockAnalysis.com (30-second summary tab)
- **Implication for Stock Explorer**: C72 was declassified into C48, which is correct — but the "TL;DR First" concept remains valuable. C73's Expert Analysis should follow the Wall Street Zen principle: one paragraph, one verdict, plain language.
- **Design Principle**: "Less is more" applies especially to expert analysis — beginners want the expert's conclusion, not their entire thesis.

#### Trend 4: Structured Investment Frameworks Add Analytical Rigor
- **Evidence**: Tykr (Buffett's 12 criteria), TipRanks (Smart Score composite), Simply Wall St (Snowflake)
- **Implication for Stock Explorer**: C43 (Snowflake) already provides a structured framework. C74 (Historical Scenario Explorer) should add a "what does this mean" layer — not just showing data, but scoring it against criteria.
- **Design Principle**: Structured frameworks ("here's how this company scores") are more educational than raw data ("here are the numbers").

#### Trend 5: "Calm Tone" Differentiates from Anxiety-Inducing Financial News
- **Evidence**: Wall Street Zen ("Here's what you need to know. No rush."), Tykr (Buffett-branded reassurance)
- **Implication for Stock Explorer**: Stock Explorer's "historian" tone is already calm and factual. C73 and C74 should maintain this — especially C74, which could easily become anxiety-inducing if scenarios are framed as "what could go wrong" rather than "what happened before."
- **Design Principle**: Calm, factual tone is a competitive advantage in financial education. Never use urgency or fear.

#### Trend 6: TW Dividend Education is a Distinct Niche
- **Evidence**: 口袋股利 (dividend calendar + calculator), 股息小人 (community dividend analysis)
- **Implication for Stock Explorer**: C1 (ex-dividend countdown) covers single-stock dividend info. C75 (Dividend Calendar) would add the market-wide view. This is a P2 feature but fills a clear gap.
- **Design Principle**: Dividend investors are a distinct audience with specific needs (calendar, calculator, yield tracking).

#### Trend 7: Gamification is Table Stakes for Engagement
- **Evidence**: 口袋證券 (points + badges + milestones), SoFi (3x higher retention with streaks), Cake Finance (XP system)
- **Implication for Stock Explorer**: C71 (Study Log) is the reframed version of C71 (Learning Streak). The "study log" framing is better for historian positioning — it's a personal learning record, not a gamification gimmick.
- **Design Principle**: Gamification works but must be framed as "learning progress" not "achievement" to maintain historian positioning.

### Competitive Gap Analysis (Updated)

| Feature | Best-in-Class | Stock Explorer Status | Gap |
|---------|--------------|----------------------|-----|
| Visual Health Score | Simply Wall St | ✅ C43 implemented | 🟢 Closed |
| Synthesis/Summary | Public.com | ✅ C37 implemented | 🟢 Closed |
| Valuation Context | 財報狗 | ✅ C45 implemented | 🟢 Closed |
| Risk Analysis | Simply Wall St | ✅ C44 implemented | 🟢 Closed |
| Peer Discovery | Robinhood | ✅ C41 implemented | 🟢 Closed |
| Interactive Calculator | 口袋股利, Tykr | ❌ Not built (C79) | 🔴 Gap |
| Expert Consensus | TipRanks | ⏳ C73 planned Sprint 5 | 🟡 In Progress |
| Historical Scenarios | Sensibull | ⏳ C74 planned Sprint 5 | 🟡 In Progress |
| Study Log / Streak | SoFi, Cake Finance | ⏳ C71 planned Sprint 5 | 🟡 In Progress |
| Dividend Calendar | 口袋股利 | ❌ Not built (C75) | 🔴 Gap |
| Discovery/Screening | 財報狗 | ❌ Not built (C42) | 🔴 Gap |
| Onboarding | 玉山證券 | ❌ Not built (C58) | 🔴 Gap |
| Glossary/Tooltips | Robinhood | ❌ Not built (C33) | 🔴 Gap |
| Mobile App | All competitors | ❌ Streamlit only | 🔴 Structural |

---

## Design Specifications for Sprint 5 Features

### C71: Study Log — Personal Learning Record

> **Reframed from**: Learning Streak (original C71)
> **Priority**: P2
> **Effort**: 8-12h
> **Competitor Sources**: SoFi (3x retention with streaks), Cake Finance (XP system), 口袋證券 (gamified learning)

#### Design Philosophy

The Study Log is **not a gamification feature** — it's a personal learning record that happens to include streak tracking. The historian positioning demands this distinction:

- ❌ **Wrong**: "🔥 連續學習 7 天！你太棒了！" (gamification voice)
- ✅ **Right**: "📚 你已連續 7 天查看公司資料，記錄了 12 家公司的學習筆記" (historian voice — factual, record-keeping)

#### UI Specification

**Location**: Sidebar (below search box), collapsed by default on mobile

**Components**:
1. **Study Counter** (sidebar widget):
   - "📚 本週學習：N 家公司"
   - "🔥 連續 N 天" (secondary, smaller text)
   - Subtle, not hero section — should not dominate the page

2. **Study Log Page** (accessible from sidebar "📖 我的學習紀錄"):
   - Table/card view of recently studied stocks
   - Columns: 日期 | 公司 | 產業 | 查看次數
   - Sorted by most recent
   - Empty state: "還沒有學習紀錄，從搜尋一家公司開始吧！" with search CTA

3. **Milestone Badges** (session-only, non-persistent):
   - 7 days: "🌱 初學者" badge
   - 30 days: "📖 勤學者" badge
   - 100 companies: "🏛️ 見習歷史學家" badge
   - Displayed as small badges in the study log page, NOT as popups or celebrations

#### Design Rules

| Rule | Specification |
|------|--------------|
| **Card style** | Use `_info_card()` for study log entries — no inline HTML |
| **Color** | Blue border (`#3498DB`) for study log cards — informational, not celebratory |
| **Tone** | Factual, record-keeping — "你查看了 N 家公司" not "你太棒了！" |
| **Text limit** | Study log entries: date + company name + industry only |
| **Empty state** | Use `_empty_state("📚", "還沒有學習紀錄", "從搜尋一家公司開始吧")` |
| **Ten-second test** | "This page shows what I've studied" — immediately clear |
| **Session state keys** | `study_log_*`, `streak_*` — namespaced to avoid collisions |
| **Persistence** | YAML file (like watchlist) — survives page refresh |

#### Historian Positioning Guardrail

The Study Log must **never**:
- Use competitive language ("你超過了 80% 的使用者！")
- Show leaderboards or social comparisons
- Use urgency ("再學習 1 天就能獲得徽章！")
- Frame learning as a game

The Study Log **must**:
- Frame as personal record-keeping ("你的學習歷程")
- Use past tense ("你查看了..." not "你正在...")
- Be factual and neutral in tone

---

### C73: Expert Analysis Synthesis — Plain-Language Fundamental Analysis Summary

> **Pivoted from**: Super Investor Thesis (original C73)
> **Priority**: P1 (elevated from P2)
> **Effort**: 8-12h (reduced from 12-16h due to scope refinement)
> **Competitor Sources**: TipRanks (analyst consensus), StockAnalysis.com (Analysis tab), Dhan (Super Investors)

#### Design Philosophy

The Expert Analysis Synthesis is **not** "what famous investors think" — it's a plain-language synthesis of fundamental analysis from multiple expert sources. The pivot from "Super Investor Thesis" to "Expert Analysis Synthesis" is critical:

- ❌ **Wrong**: "巴菲特看好台積電" (implies endorsement, investment advice)
- ✅ **Right**: "多數分析師認為台積電在AI晶片領域具有領先地位，但部分擔憂資本支出過高" (factual synthesis of expert opinions)

#### Content Sources (Priority Order)

1. **TW brokerage research reports** (TWSE public filings) — primary source
2. **Institutional investor holdings** (TWSE public filings) — "哪些機構持有這家公司"
3. **Analyst consensus estimates** (if available for TW market)
4. **Curated expert commentary** (from public interviews, annual reports)

#### UI Specification

**Location**: Business card page, after C43 (Health Score) and C44 (Risk Analysis), before C45 (Valuation)

**Section Title**: `### 🧑‍🏫 專家怎麼看`

**Components**:
1. **Expert Consensus Card** (primary):
   - One-paragraph synthesis (3-5 sentences max)
   - Plain-language summary of expert opinions
   - Source attribution: "根據 X 家券商研究報告綜合"
   - Historian framing: past tense, attributed quotes only

2. **Key Expert Points** (expandable):
   - `st.expander("📋 主要觀點")` — collapsed by default
   - 3-5 bullet points of key expert arguments
   - Each bullet: one sentence, plain language
   - Color-coded: 🟢 positive view, 🟡 neutral/mixed, 🔴 concern

3. **Institutional Holdings** (secondary):
   - "哪些機構持有這家公司" — top 5 institutional holders
   - Plain-language explanation: "這表示專業投資者對這家公司的看法"
   - Disclaimer: "機構持有不代表投資建議"

#### Design Rules

| Rule | Specification |
|------|--------------|
| **Card style** | Use `_summary_card()` for consensus card (orange border = important info) |
| **Bullet card style** | Use `_info_card()` for key points (blue border = informational) |
| **Color** | Consensus card: `#F39C12` border (important), `#FFF8F0` background |
| **Text limit** | Synthesis: 3-5 sentences max. Bullets: 1 sentence each. |
| **Tone** | Past tense, attributed, factual — "分析師認為..." not "應該..." |
| **Empty state** | `_info_card("專家分析", "目前沒有找到相關的分析師報告", "🧑‍🏫")` |
| **Ten-second test** | "Experts think this company is strong in X but face risk Y" — clear in 10 seconds |
| **Disclaimer** | Required: "以上為分析師意見綜合，不構成投資建議" |

#### Historian Positioning Guardrail

The Expert Analysis must **never**:
- Use present tense for opinions ("巴菲特看好..." → "巴菲特在2019年表示...")
- Present opinions as facts
- Recommend action based on expert opinions
- Use superlatives ("最看好", "強烈推薦")

The Expert Analysis **must**:
- Attribute all opinions to specific sources
- Use past tense for all statements
- Include disclaimer on every instance
- Present multiple perspectives (not just bullish)

#### MVP Scope

- **10 pilot stocks**: TSMC, 鴻海, 聯發科, 台達電, 富邦金, 台泥, 中鋼, 台塑, 華碩, 廣達
- **One synthesis paragraph per stock** (not multiple investor theses)
- **Content creation**: Start in Sprint 4 as parallel workstream (not blocking engineering)

---

### C74: Historical Scenario Explorer — Past-Tense Factual Scenario Exploration

> **Pivoted from**: Interactive What-If Scenarios (original C74)
> **Priority**: P1
> **Effort**: 10-15h (reduced from 14-20h due to pivot simplification)
> **Competitor Sources**: Sensibull (interactive options scenarios), Groww (Vola game), Tastytrade (probability analysis)

#### Design Philosophy

The Historical Scenario Explorer is **NOT** a prediction tool — it's an educational exploration of what happened in the past under specific conditions. The pivot from "What-If" to "Historical Scenario" is essential for historian positioning:

- ❌ **Wrong**: "如果營收成長 20%，股價會怎樣？" (prediction framing)
- ✅ **Right**: "2021年當營收成長 22% 時，這家公司的獲利變化是..." (historical framing)

#### UI Specification

**Location**: Business card page, after C45 (Valuation), before C41 (Read Next)

**Section Title**: `### 📜 歷史情境探索`

**Components**:
1. **Scenario Selector** (top):
   - Pre-built historical scenarios (not free-form sliders)
   - `st.selectbox` with 4-6 historical scenarios:
     - "📈 營收成長超過 20% 的年度"
     - "📉 營收下降超過 10% 的年度"
     - "💰 毛利率超過 60% 的時期"
     - "⚠️ 負債比超過 60% 的時期"
     - "🏆 獲利能力最強的年度"
   - Default: "選擇一個歷史情境來探索"

2. **Scenario Result Card** (main):
   - Shows what actually happened during that scenario
   - Key metrics: revenue, margin, health score, risk level
   - Plain-language explanation: "在營收成長超過 20% 的年度，這家公司的獲利能力通常..."
   - Uses `_summary_card()` with scenario-specific color

3. **Comparison View** (expandable):
   - `st.expander("📊 與目前比較")` — collapsed by default
   - Side-by-side: historical scenario metrics vs current metrics
   - Plain-language delta: "當時的毛利率比現在高 5%"

#### Design Rules

| Rule | Specification |
|------|--------------|
| **Card style** | Use `_summary_card()` for scenario result (contextual border color) |
| **Comparison card** | Use `_info_card()` for comparison view |
| **Color** | Scenario result: `#3498DB` border (exploration/learning) |
| **Text limit** | Scenario explanation: 2-3 sentences max |
| **Tone** | Past tense, factual — "當時...", "在...時期", "歷史上..." |
| **Empty state** | `_info_card("歷史情境", "這家公司的歷史資料不足以產生情境分析", "📜")` |
| **Ten-second test** | "This shows what happened in the past under specific conditions" — clear |
| **Disclaimer** | "歷史表現不代表未來結果。此為教育用途，非投資建議。" |
| **Interaction** | Selectbox only — NO sliders (avoids prediction framing) |
| **Max scenarios** | 6 pre-built scenarios (curated, not user-defined) |

#### Historian Positioning Guardrail

The Historical Scenario Explorer must **never**:
- Use future tense ("如果...就會...")
- Allow users to define arbitrary parameters (sliders = prediction framing)
- Show probability distributions or confidence intervals
- Imply that historical patterns will repeat

The Historical Scenario Explorer **must**:
- Use only pre-built, historically-grounded scenarios
- Always show what **actually happened**, not what could happen
- Use past tense exclusively
- Include disclaimer on every instance
- Frame as "learning from history" not "predicting the future"

#### MVP Scope

- **6 pre-built scenarios** per stock (based on actual historical data)
- **10 pilot stocks** (same as C73)
- **No free-form inputs** — selectbox only
- **Data source**: Existing financial data (no new API calls needed)

---

## New Design Improvement Proposals

### Proposal 1: D-039 — Standardized Section Header Pattern for Business Card

**Priority**: P2
**Effort**: 1-2h
**Source**: D-003 (card inconsistency) + C71/C73/C74 integration planning

**Problem**: The business card page has 15+ sections, each with different header styles. Some use `### 📊 標題`, others use `st.markdown("### ...")`, and C44 uses `st.expander("⚠️ 標題")`. This creates visual inconsistency as new sections are added.

**Proposal**: Standardize all business card section headers:
```python
def _section_header(icon: str, title: str, collapsed: bool = False):
    """Standardized section header for business card page.
    
    - icon: emoji for the section
    - title: section title in Chinese
    - collapsed: if True, wrap in st.expander; if False, use markdown header
    """
    header_text = f"{icon} {title}"
    if collapsed:
        return st.expander(header_text, expanded=False)
    else:
        st.markdown(f"### {header_text}")
        return None
```

**Design Rationale**: This ensures C71, C73, and C74 sections use the same header pattern as existing sections. Collapsed sections (C44, C73 key points, C74 comparison) use `st.expander`; visible sections use `###` markdown.

### Proposal 2: D-040 — Content Disclaimer Component

**Priority**: P2
**Effort**: 0.5h
**Source**: C73 (Expert Analysis) + C74 (Historical Scenarios) historian positioning requirements

**Problem**: Both C73 and C74 require historian positioning disclaimers. Currently, disclaimer text is written inline in each feature. A standardized component would ensure consistency.

**Proposal**: Create a shared disclaimer component:
```python
def _historian_disclaimer(disclaimer_type: str = "general"):
    """Standardized historian positioning disclaimer.
    
    disclaimer_type: 'expert' | 'scenario' | 'general'
    """
    messages = {
        "expert": "以上為分析師意見綜合，不構成投資建議。",
        "scenario": "歷史表現不代表未來結果。此為教育用途，非投資建議。",
        "general": "本頁面僅提供歷史資料分析，不構成投資建議。"
    }
    st.caption(f"⚠️ {messages[disclaimer_type]}")
```

**Design Rationale**: Using `st.caption()` for disclaimers is consistent with Streamlit conventions — small, unobtrusive, but visible. The `⚠️` emoji provides visual scanning cue.

### Proposal 3: D-041 — Sprint 5 Feature Card Component Standard

**Priority**: P2
**Effort**: 1h
**Source**: D-003 (card inconsistency) + Sprint 5 feature integration

**Problem**: C71, C73, and C74 will each add new card types to the business card page. Without a standard, these will likely use inline HTML (continuing D-003).

**Proposal**: Before implementing C71/C73/C74, create the following card components in `_router_base.py`:
- `_study_card()` — for C71 study log entries (blue border, `#F8F9FA` background)
- `_expert_card()` — for C73 expert analysis (orange border, `#FFF8F0` background)
- `_scenario_card()` — for C74 historical scenarios (blue border, `#F8F9FA` background)
- `_disclaimer_caption()` — for historian positioning disclaimers

**Design Rationale**: Creating these components **before** feature implementation prevents D-003 regressions. This is the "design system first" approach.

---

## Updated Issue Checklist

### P0 — Blocking Issues
*(None)*

### P1 — Important Issues (3 items, reduced from 6)

| ID | Title | Status | Effort | Notes |
|----|-------|--------|--------|-------|
| **D-003** | Inconsistent Card Styling | ❌ Unresolved | 2-3h | Root cause for D-035, D-036, D-037. Must be addressed before/during Sprint 5. |
| **D-005** | Business Card Page Overload | ⚠️ Stable | 3-4h | C44 expander helps. C73/C74 will add sections — use `_section_header(collapsed=True)` for new sections. |
| **D-006** | Mobile Responsiveness Gaps | ❌ Unresolved | 4-6h | Unchanged. |

**Priority Changes since Round 14**:
- **D-004 → RESOLVED**: `docs/design/design_system.md` now exists at expected path.
- **D-021 → RESOLVED**: D-034 fix verified — metric values shown in hover and dimension cards.
- **D-034 → RESOLVED**: Same as D-021 — resolved in Sprint 4.
- **D-007 → P2** (already downgraded in Round 14)
- **D-032 → P2** (already downgraded in Round 14)

### P2 — Optimization Issues (16 items)

| ID | Title | Status | Effort | Notes |
|----|-------|--------|--------|-------|
| **D-007** | No Discovery Mechanism | ⏳ Partial | 12-16h | Downgraded to P2 — C41 provides partial peer discovery. |
| **D-008** | Loading State Inconsistency | ❌ Unresolved | 1-2h | Unchanged. |
| **D-009** | Error State Inconsistency | ❌ Unresolved | 1h | Unchanged. |
| **D-010** | Watchlist Uses Non-PPT Layout | ❌ Unresolved | 2-3h | Unchanged. |
| **D-011** | Category Browser Uses Dense Tables | ❌ Unresolved | 2-3h | Unchanged. |
| **D-012** | No Glossary/Tooltip System | ❌ Unresolved | 8-12h | Unchanged. |
| **D-015** | No Structured Learning Path | ❌ Unresolved | 20-30h | Unchanged. |
| **D-032** | No Progressive Disclosure | ⏳ Partial | 3-4h | Downgraded to P2 — C44 proves the pattern. |
| **D-033** | No Standardized Empty State | ❌ Unresolved | 1h | Unchanged. |
| **D-035** | C41 Peer Cards Use Inline HTML | ❌ Unresolved | 0.5-1h | D-003 regression. Fix before Sprint 5. |
| **D-036** | C44 Risk Cards Non-Standard BG | ❌ Unresolved | <0.5h | `#FFF8F0` → `#F8F9FA`. One-line fix. |
| **D-037** | `_白话_card` Wrong Background | ❌ Unresolved | <0.5h | `#F5F5F5` → `#F8F9FA`. One-line fix. |
| **D-038** | C41 API Call in View Layer | ❌ Unresolved | 1-2h | Move to router layer. |
| **D-039** | No Standardized Section Header | 🆕 New | 1-2h | Prevents inconsistency as C71/C73/C74 add sections. |
| **D-040** | No Standardized Disclaimer Component | 🆕 New | 0.5h | C73/C74 both need historian disclaimers. |
| **D-041** | No Sprint 5 Card Components | 🆕 New | 1h | Prevents D-003 regression for C71/C73/C74. |

### Resolved Issues (15 items)

| ID | Title | Severity | Resolved | Resolution |
|----|-------|----------|----------|------------|
| D-001 | No Visual Health Score | P0 | 2026-06-17 | C43 (Snowflake) implemented |
| D-002 | No Synthesis Layer | P0 | 2026-06-17 | C37 (Key Takeaways) implemented |
| D-004 | No Design System Documentation | P1 | 2026-06-19 | `docs/design/design_system.md` now exists at expected path |
| D-013 | No Risk Analysis Section | P2 | 2026-06-19 | C44 (Risk Analysis MVP) implemented |
| D-014 | No Valuation Context | P2 | 2026-06-17 | C45 (Valuation Band) implemented |
| D-016 | C37 Missing Orange/Amber Hero Card | P1 | 2026-06-18 | `_summary_card()` created |
| D-017 | C37 Bullet Count Exceeds Spec | P2 | 2026-06-18 | Cap changed to 3 bullets |
| D-018 | C39 Placement Too Low | P1 | 2026-06-18 | Moved directly after C37 |
| D-019 | C39 Missing Delta Count Cap | P2 | 2026-06-18 | `return deltas[:2]` added |
| D-020 | C39 Missing Directional Color Coding | P2 | 2026-06-18 | Green/red color spans added |
| D-021 | C43 Missing Metric Values | P1 | 2026-06-19 | D-034 fix — metric values in hover + cards |
| D-022 | C43 Placement Not Near Top | P2 | 2026-06-18 | Now 3rd content section |
| D-023 | C45 Uses 2-Year Window | P2 | 2026-06-18 | Extended to 5-year window |
| D-024 | _info_card Wrong Background | P1 | 2026-06-19 | Changed to `#F8F9FA` |
| D-025 | C39 Missing Empty State | P2 | 2026-06-19 | Added "近期無顯著變化" fallback |
| D-034 | C3 Metric Value Tooltips | P1 | 2026-06-19 | Enhanced hover template + dimension cards |

---

## Recommendations Summary

### Immediate Actions (Sprint 4 — remaining)

1. **D-036 + D-037**: Batch color fixes (<1h total) — D-036 changes C44 risk card background from `#FFF8F0` to `#F8F9FA`; D-037 changes `_白话_card` background from `#F5F5F5` to `#F8F9FA`. Both are one-line CSS changes.
2. **D-035**: Standardize C41 peer cards with shared card component (0.5-1h) — use `_info_card()` or create `_peer_card()`.
3. **D-038**: Move `client.get_stock_info()` call from view to router layer (1-2h) — architecture compliance.

### Sprint 5 Preparation (Design-First)

4. **D-041**: Create Sprint 5 card components BEFORE feature implementation (1h):
   - `_study_card()` for C71
   - `_expert_card()` for C73
   - `_scenario_card()` for C74
   - `_disclaimer_caption()` for historian positioning
5. **D-039**: Create `_section_header()` component (1-2h) — standardizes all section headers.
6. **D-040**: Create `_historian_disclaimer()` component (0.5h) — standardized disclaimer.

### Sprint 5 Feature Design Priority

7. **C71 (Study Log)** — Design is straightforward. Key risk: tone must be factual, not gamified. Use `_study_card()` + sidebar widget pattern.
8. **C73 (Expert Analysis)** — Highest design risk. Content creation is the bottleneck. Start content curation in Sprint 4. Use `_expert_card()` + `_historian_disclaimer("expert")`.
9. **C74 (Historical Scenarios)** — Highest UI complexity. Must use selectbox-only interaction (no sliders). Use `_scenario_card()` + `_historian_disclaimer("scenario")`.

### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A+ | D-003 resolved via D-041; C71/C73/C74 use standardized components; card consistency achieved |
| **Expected case** | A | D-035/036/037/038 fixed in Sprint 4; D-041 created before Sprint 5; new features use shared components |
| **Worst case** | A- | D-003 not addressed; C71/C73/C74 add more inline HTML; card inconsistency worses |

### Key Competitor Design Trends to Watch

1. **Interactive calculators** (口袋股利, Tykr) — C79 is the right response; highest-impact P2 feature
2. **Expert consensus** (TipRanks) — C73 directly addresses this; must maintain historian framing
3. **Historical scenarios** (Sensibull) — C74 pivots this to past-tense; selectbox-only is key design decision
4. **Calm tone** (Wall Street Zen) — Stock Explorer's historian tone is already aligned; maintain in C73/C74
5. **Study logs** (SoFi, Cake Finance) — C71 reframes this as learning record; avoid gamification language
6. **Structured frameworks** (Tykr, Simply Wall St) — C43 + C74 provide this; consider adding scoring to C74 scenarios

---

*This file is maintained by the Design Reviewer. Update after each review cycle. Next update: After Sprint 5 feature implementation (C71, C73, C74).*
