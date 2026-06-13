# Stock Explorer Design Review — Feature Candidates C36-C47

> **Author**: Design Reviewer (Designer)
> **Date**: 2026-06-15
> **Context**: Sprint 10 complete, Design Grade A (13th consecutive A/A-)
> **Scope**: 12 competitor-inspired feature candidates from Round 8 (C36-C41) and Round 9 (C42-C47)

---

## I. Feature Alignment Table

### Scoring Criteria

Each feature scored against 5 Core Values (CV) and 4 Design Principles (DP):

**Core Values:**
- CV1: Story first, data second
- CV2: PPT-style presentation
- CV3: Adaptive and self-evolving
- CV4: Point-to-point knowledge construction
- CV5: Benchmark-oriented analysis

**Design Principles:**
- DP1: Ten-second test
- DP2: Beginner-friendly
- DP3: Progressive drill-down
- DP4: Historian, not stock picker

**Score Legend**: ⭐⭐⭐ = Strong alignment | ⭐⭐ = Moderate alignment | ⭐ = Weak alignment | — = No alignment

---

### C36: Visual Revenue Tree

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | Shows HOW money flows — natural storytelling format |
| CV2 PPT-style | ⭐⭐⭐ | Treemap/sunburst is inherently visual-first |
| CV3 Adaptive | ⭐ | Static data; updates with revenue breakdown but not self-evolving |
| CV4 Point-to-point | ⭐⭐ | Shows parent→subsidiary→customer relationships |
| CV5 Benchmark | ⭐ | No inherent benchmarking; could add industry comparison |
| DP1 Ten-second test | ⭐⭐ | Visual tree is glanceable, but hierarchy may confuse beginners |
| DP2 Beginner-friendly | ⭐⭐ | Needs plain-language labels; treemap can be overwhelming |
| DP3 Progressive drill-down | ⭐⭐⭐ | Natural drill-down: click segment → see sub-segments |
| DP4 Historian | ⭐⭐⭐ | Explains business model, not buy/sell signal |
| **Overall** | **Strong** | Excellent fit for "historian" positioning; extends existing pie chart |

**New Components**: Treemap/sunburst chart (Plotly), "Revenue Tree" tab
**Layout Impact**: New tab on Business Card page; replaces or supplements pie chart
**Design System Impact**: Minimal — uses existing color palette for segments

---

### C37: Key Takeaways Summary Card

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | Synthesizes data into narrative bullets |
| CV2 PPT-style | ⭐⭐⭐ | 3-5 bullet points = one key message |
| CV3 Adaptive | ⭐⭐ | Auto-generated; updates with data changes |
| CV4 Point-to-point | ⭐⭐ | Can connect key takeaways across related companies |
| CV5 Benchmark | ⭐⭐ | Can include benchmark context in takeaways |
| DP1 Ten-second test | ⭐⭐⭐ | **Directly addresses the ten-second test** — this IS the ten-second test |
| DP2 Beginner-friendly | ⭐⭐⭐ | Plain-language summaries are the core of beginner-friendliness |
| DP3 Progressive drill-down | ⭐⭐ | Summary → detail is progressive disclosure |
| DP4 Historian | ⭐⭐⭐ | Summarizes what happened, not what to do |
| **Overall** | **Critical** | Highest alignment with core design principles |

**New Components**: Summary card component (auto-generated), "📋 重點摘要" card
**Layout Impact**: New card at TOP of Business Card page (above all existing content)
**Design System Impact**: New card variant (summary card with bullet points); uses existing card styles

---

### C38: Compare Stories

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | Narrative comparison — "How are these stories different?" |
| CV2 PPT-style | ⭐⭐ | Side-by-side layout works for PPT-style; needs careful design |
| CV3 Adaptive | ⭐ | Static comparison; doesn't self-evolve |
| CV4 Point-to-point | ⭐⭐⭐ | Connects companies through narrative relationships |
| CV5 Benchmark | ⭐⭐⭐ | Natural benchmark comparison — "How does TSMC differ from UMC?" |
| DP1 Ten-second test | ⭐⭐ | Side-by-side can be scanned quickly if well-designed |
| DP2 Beginner-friendly | ⭐⭐ | Narrative comparison is more accessible than metric comparison |
| DP3 Progressive drill-down | ⭐⭐ | Can drill into specific comparison points |
| DP4 Historian | ⭐⭐⭐ | Compares company stories, not stock picks |
| **Overall** | **Strong** | Perfect for "historian" positioning; extends existing peer comparison |

**New Components**: Side-by-side narrative layout, "故事比較" tab
**Layout Impact**: New tab on Peer Comparison page; two-column layout
**Design System Impact**: Two-column comparison layout pattern needed

---

### C39: What Changed Recently

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | "Here's what changed" is inherently narrative |
| CV2 PPT-style | ⭐⭐ | Delta card with 2-3 key changes is PPT-friendly |
| CV3 Adaptive | ⭐⭐⭐ | Directly shows what's new — core of "adaptive and self-evolving" |
| CV4 Point-to-point | ⭐ | Limited; shows changes for one company |
| CV5 Benchmark | ⭐⭐ | Can compare change vs industry average |
| DP1 Ten-second test | ⭐⭐⭐ | "Here are 3 things that changed" is instantly understandable |
| DP2 Beginner-friendly | ⭐⭐⭐ | Plain-language change explanations are ultra-beginner-friendly |
| DP3 Progressive drill-down | ⭐⭐ | Summary of changes → detail on each change |
| DP4 Historian | ⭐⭐⭐ | Explains what changed historically, not future predictions |
| **Overall** | **Strong** | Excellent fit for "adaptive" core value and ten-second test |

**New Components**: "🔄 最近有什麼變化" delta card, change detection logic
**Layout Impact**: New card on Business Card page (near top, after summary card)
**Design System Impact**: Delta indicators (📈📉) with green/red for direction

---

### C40: Beginner/Expert Mode

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐ | Beginner mode simplifies stories; expert mode shows full data |
| CV2 PPT-style | ⭐⭐⭐ | Beginner mode IS PPT-style — one key point, minimal text |
| CV3 Adaptive | ⭐⭐ | Adapts complexity to user level |
| CV4 Point-to-point | ⭐⭐⭐ | Progressive complexity is point-to-point knowledge construction |
| CV5 Benchmark | ⭐ | No direct benchmark alignment |
| DP1 Ten-second test | ⭐⭐⭐ | Beginner mode is DESIGNED for the ten-second test |
| DP2 Beginner-friendly | ⭐⭐⭐ | **This IS the beginner-friendly feature** |
| DP3 Progressive drill-down | ⭐⭐⭐ | Toggle between complexity levels = progressive disclosure |
| DP4 Historian | ⭐⭐ | Both modes maintain historian positioning |
| **Overall** | **Strong** | Directly implements "progressive drill-down" design principle |

**New Components**: Mode toggle in navbar, conditional rendering logic
**Layout Impact**: Navbar toggle (Zone A); affects ALL page content
**Design System Impact**: New toggle component; conditional visibility patterns

---

### C41: Read Next Recommendations

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐ | "After TSMC, learn about Apple" creates narrative continuity |
| CV2 PPT-style | ⭐⭐ | 2-3 recommendations as cards is PPT-friendly |
| CV3 Adaptive | ⭐ | Static recommendations; could be personalized |
| CV4 Point-to-point | ⭐⭐⭐ | Connects companies through business relationships |
| CV5 Benchmark | ⭐⭐ | Can recommend industry leader for benchmark comparison |
| DP1 Ten-second test | ⭐⭐ | "You might also like" is glanceable |
| DP2 Beginner-friendly | ⭐⭐⭐ | Guided discovery is ultra-beginner-friendly |
| DP3 Progressive drill-down | ⭐⭐⭐ | Natural learning path: company → related company |
| DP4 Historian | ⭐⭐⭐ | Relationship-based, not price-based recommendations |
| **Overall** | **Strong** | Unique differentiator; no competitor has relationship-based recommendations |

**New Components**: "📖 接著看" recommendation section, relationship-based logic
**Layout Impact**: New section at bottom of Business Card page
**Design System Impact**: Recommendation card variant (smaller, with relationship label)

---

### C42: Stock Screener

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐ | Screening is data-first, not story-first |
| CV2 PPT-style | ⭐ | Screening results are list-based, not PPT-style |
| CV3 Adaptive | ⭐⭐ | Results update with data; presets can evolve |
| CV4 Point-to-point | ⭐⭐⭐ | Discovery → company page = point-to-point learning |
| CV5 Benchmark | ⭐⭐ | Can screen relative to industry benchmarks |
| DP1 Ten-second test | ⭐ | Screening interface is complex; results need synthesis |
| DP2 Beginner-friendly | ⭐⭐ | Presets help, but screening is inherently complex |
| DP3 Progressive drill-down | ⭐⭐⭐ | Presets → custom → results → company page |
| DP4 Historian | ⭐⭐ | "Interesting companies to learn about" framing maintains historian |
| **Overall** | **Moderate** | Important for discovery but risks diluting core positioning |

**New Components**: "🔍 選股探索" page, filter UI, preset buttons, results list
**Layout Impact**: New top-level page; significant new UI surface
**Design System Impact**: Filter/chip components, results list pattern, preset cards

**⚠️ Design Risk**: Screening interfaces are inherently complex. Must use beginner-friendly presets ("穩定收息", "成長潛力") rather than raw metric filters. Results must link to existing Business Card pages, not show raw data.

---

### C43: Company Snowflake Health

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | Visual summary tells the company's health story at a glance |
| CV2 PPT-style | ⭐⭐⭐ | One visual = one key message; perfect PPT-style |
| CV3 Adaptive | ⭐⭐ | Updates with data changes |
| CV4 Point-to-point | ⭐⭐ | Each dimension can drill into details |
| CV5 Benchmark | ⭐⭐⭐ | Can show industry benchmark overlay on radar |
| DP1 Ten-second test | ⭐⭐⭐ | **This IS the ten-second test perfected** — one glance = health assessment |
| DP2 Beginner-friendly | ⭐⭐⭐ | Color-coded visual is universally understandable |
| DP3 Progressive drill-down | ⭐⭐⭐ | Radar → dimension → detailed metrics |
| DP4 Historian | ⭐⭐⭐ | Shows historical health, not future prediction |
| **Overall** | **Critical** | Highest impact for ten-second test; multiple competitors prove demand |

**New Components**: Radar chart (Plotly), 5-dimension scoring, "Company Snowflake" card
**Layout Impact**: New card at TOP of Business Card page (or integrated with C37)
**Design System Impact**: Radar chart component; 5-dimension color coding (extend existing green/yellow/red)

**⚠️ Design Risk**: Radar charts can be confusing for beginners. Must use simple color coding (🟢🟡🔴) and plain-language labels. Consider a "snowflake" visual instead of radar for better PPT-style alignment.

---

### C44: Risk Analysis

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | "Here's what went wrong before" is narrative |
| CV2 PPT-style | ⭐⭐ | 3-5 risks as cards is PPT-friendly |
| CV3 Adaptive | ⭐⭐ | Risks update with company changes |
| CV4 Point-to-point | ⭐⭐ | Can connect risks across related companies |
| CV5 Benchmark | ⭐⭐ | Can compare risk profile vs industry |
| DP1 Ten-second test | ⭐⭐ | "3 things that could go wrong" is glanceable |
| DP2 Beginner-friendly | ⭐⭐⭐ | Historical risk evidence is educational |
| DP3 Progressive drill-down | ⭐⭐⭐ | Risk summary → historical evidence → current indicators |
| DP4 Historian | ⭐⭐⭐ | **Perfect historian feature** — explains historical risks, doesn't predict |
| **Overall** | **Strong** | Unique differentiator; perfect for historian positioning |

**New Components**: "⚠️ 風險分析" section, risk card component
**Layout Impact**: New section on Business Card page
**Design System Impact**: Warning/risk card variant (orange/yellow border, ⚠️ icon)

---

### C45: Valuation Band Chart

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | "Is this expensive or cheap?" is a natural story |
| CV2 PPT-style | ⭐⭐⭐ | Horizontal bar showing position in range is visual-first |
| CV3 Adaptive | ⭐⭐ | Updates with price/EPS changes |
| CV4 Point-to-point | ⭐ | Limited; single metric focus |
| CV5 Benchmark | ⭐⭐⭐ | Historical range IS a benchmark |
| DP1 Ten-second test | ⭐⭐⭐ | "Green zone = fairly valued" is instantly understandable |
| DP2 Beginner-friendly | ⭐⭐⭐ | Visual position in range is ultra-beginner-friendly |
| DP3 Progressive drill-down | ⭐⭐ | Band chart → P/E history → P/E calculation |
| DP4 Historian | ⭐⭐⭐ | Shows historical valuation, not future target |
| **Overall** | **Strong** | High impact, low effort; 財報狗 proves demand |

**New Components**: Horizontal band chart (Plotly), "📊 估值區間" card
**Layout Impact**: New card on Business Card page
**Design System Impact**: Band chart component (horizontal bar with range markers)

---

### C46: Moat Analysis

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | "This company has a castle with a moat" is pure storytelling |
| CV2 PPT-style | ⭐⭐⭐ | Moat type + strength is one key visual |
| CV3 Adaptive | ⭐ | Moat assessment is relatively static |
| CV4 Point-to-point | ⭐⭐ | Can compare moats across companies |
| CV5 Benchmark | ⭐⭐⭐ | Compare moat strength vs industry leader |
| DP1 Ten-second test | ⭐⭐⭐ | "Wide moat = strong competitive advantage" is instantly clear |
| DP2 Beginner-friendly | ⭐⭐⭐ | Castle/moat metaphor is universally understood |
| DP3 Progressive drill-down | ⭐⭐⭐ | Moat type → evidence → historical protection |
| DP4 Historian | ⭐⭐⭐ | Explains historical competitive advantage, doesn't predict durability |
| **Overall** | **Strong** | Unique differentiator for TW market; perfect historian feature |

**New Components**: "🏰 護城河分析" section, moat strength indicator
**Layout Impact**: New section on Business Card page
**Design System Impact**: Moat strength indicator (wide/narrow/none), castle metaphor visual

---

### C47: Education Academy

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| CV1 Story first | ⭐⭐⭐ | Each lesson uses real stock examples |
| CV2 PPT-style | ⭐⭐ | Lessons are inherently PPT-style (one concept per lesson) |
| CV3 Adaptive | ⭐⭐ | Content grows with curriculum |
| CV4 Point-to-point | ⭐⭐⭐ | Structured learning paths = point-to-point knowledge |
| CV5 Benchmark | ⭐ | Limited benchmark alignment |
| DP1 Ten-second test | ⭐⭐ | Individual lessons pass; full academy is complex |
| DP2 Beginner-friendly | ⭐⭐⭐ | Structured learning IS beginner-friendly |
| DP3 Progressive drill-down | ⭐⭐⭐ | Beginner → intermediate → advanced = progressive |
| DP4 Historian | ⭐⭐⭐ | Education-focused, not advice-focused |
| **Overall** | **Moderate** | High strategic value but high effort; transforms product from tool to platform |

**New Components**: "📚 學習學院" page, lesson cards, quiz components, progress tracking
**Layout Impact**: New top-level page; significant new UI surface
**Design System Impact**: Lesson card, quiz component, progress indicator patterns

---

## II. Summary Scoring Matrix

| ID | Feature | CV1 | CV2 | CV3 | CV4 | CV5 | DP1 | DP2 | DP3 | DP4 | Total ⭐ | Priority |
|----|---------|-----|-----|-----|-----|-----|-----|-----|-----|-----|---------|----------|
| C37 | Key Takeaways | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | **24** | 🔴 Critical |
| C43 | Company Snowflake | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **24** | 🔴 Critical |
| C39 | What Changed | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | **22** | 🟠 High |
| C40 | Beginner/Expert | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **22** | 🟠 High |
| C44 | Risk Analysis | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **22** | 🟠 High |
| C46 | Moat Analysis | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **24** | 🟠 High |
| C36 | Revenue Tree | ⭐⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **21** | 🟡 Medium |
| C38 | Compare Stories | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | **21** | 🟡 Medium |
| C41 | Read Next | ⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **21** | 🟡 Medium |
| C45 | Valuation Band | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | **23** | 🟡 Medium |
| C42 | Stock Screener | ⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **17** | 🟢 Lower |
| C47 | Education Academy | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **22** | 🟢 Lower |

---

## III. Proposed Design Directions

### Design Direction A: "The Ten-Second Company Page" (Ten-Second Test Maximization)

**Theme**: Transform the Business Card page into a perfectly synthesized, glanceable company overview that passes the ten-second test on every visit.

**Features Included**:
1. **C37 Key Takeaways** — Top of page, 3-5 bullet synthesis
2. **C43 Company Snowflake** — Visual health radar at top, alongside takeaways
3. **C39 What Changed Recently** — Delta card showing recent changes
4. **C45 Valuation Band Chart** — Visual "expensive/cheap" indicator

**Rationale**:
- These 4 features work together as a "dashboard layer" at the top of the Business Card page
- A beginner can land on the page and within 10 seconds know: what this company does (C37), how healthy it is (C43), what changed recently (C39), and whether it's expensive (C45)
- All 4 features are visual-first, PPT-style, and beginner-friendly
- Combined effort: ~36-42h (C37: 6-8h + C43: 12-16h + C39: 8-10h + C45: 8-10h)
- This directly addresses the product vision's #1 design principle: "ten-second test"

**Layout Concept**:
```
┌─────────────────────────────────────────────┐
│  Zone A: Navbar (company + price + tabs)    │
├──────────┬──────────────────────────────────┤
│          │  C37: 📋 重點摘要 (3-5 bullets)   │
│  Zone B  │  C43: ❄️ Company Snowflake       │
│  Sidebar │  ┌──────┬──────┬──────┬──────┐   │
│          │  │ 獲利 │ 成長 │ 財務 │ 股息 │   │
│          │  │ 🟢   │ 🟢   │ 🟡   │ 🟢   │   │
│          │  └──────┴──────┴──────┴──────┘   │
│          │  C39: 🔄 最近有什麼變化            │
│          │  C45: 📊 估值區間                  │
│          │  ─────────────────────────────    │
│          │  [Existing tabs content below]     │
└──────────┴──────────────────────────────────┘
```

---

### Design Direction B: "The Historian's Toolkit" (Unique Positioning Maximization)

**Theme**: Double down on the "historian, not stock picker" positioning with features no competitor has — especially features that explain business fundamentals through storytelling.

**Features Included**:
1. **C36 Visual Revenue Tree** — How money flows through the business
2. **C44 Risk Analysis** — Historical risks with evidence
3. **C46 Moat Analysis** — Competitive advantage explained through history
4. **C38 Compare Stories** — Narrative comparison of two companies

**Rationale**:
- These 4 features are uniquely aligned with the "historian" positioning
- No TW competitor has any of these features (C44 and C46 have zero TW competition)
- Together they form a complete "business understanding toolkit": how it makes money (C36), what could go wrong (C44), why it's hard to compete with (C46), and how it compares to peers (C38)
- Combined effort: ~42-54h (C36: 10-14h + C44: 10-14h + C46: 12-16h + C38: 12-16h)
- This direction strengthens the product's unique market position

**Layout Concept**:
```
New "商業模式" tab on Business Card page:
┌─────────────────────────────────────────────┐
│  C36: Revenue Tree (Treemap/Sunburst)       │
│  ┌─────────────────────────────────────┐    │
│  │  TSMC → 5nm (40%) → Apple (25%)     │    │
│  │              → NVIDIA (15%)          │    │
│  │              → AMD (10%)             │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  C46: 🏰 護城河分析                          │
│  ┌─────────────────────────────────────┐    │
│  │  技術領先 │ 寬護城河 │ 毛利率>50%    │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  C44: ⚠️ 風險分析                            │
│  ┌─────────────────────────────────────┐    │
│  │  1. 客戶集中風險 (Apple 25%)        │    │
│  │  2. 地緣政治風險 (中國營收12%)       │    │
│  └─────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

### Design Direction C: "The Learning Journey" (Progressive Drill-Down Maximization)

**Theme**: Transform Stock Explorer from a lookup tool into a guided learning experience with progressive complexity and relationship-based discovery.

**Features Included**:
1. **C40 Beginner/Expert Mode** — Complexity toggle for progressive disclosure
2. **C41 Read Next Recommendations** — Relationship-based company discovery
3. **C47 Education Academy** — Structured learning paths
4. **C42 Stock Screener** — Beginner-friendly discovery engine

**Rationale**:
- These 4 features work together as a "learning ecosystem"
- Beginner mode (C40) → Education Academy (C47) → Read Next (C41) → Screener (C42) = complete learning journey
- Transforms the product from "look up a company" to "learn about companies"
- Combined effort: ~52-76h (C40: 10-14h + C41: 6-8h + C47: 20-30h + C42: 16-24h)
- Highest strategic impact but highest effort; recommend phased implementation

**Layout Concept**:
```
New "學習中心" section in sidebar:
┌──────────┬──────────────────────────────────┐
│ 🔍 搜尋   │  C40: 🌱新手 / 🔬進階 toggle     │
│ 📚 學院   │                                  │
│ 🔥 熱門   │  [Beginner Mode: simplified      │
│ 📖 推薦   │   content with 3-4 metrics]      │
│ ⭐ 觀察   │                                  │
│ 📊 選股   │  [Expert Mode: full metrics      │
│          │   and all sections]               │
│          │                                  │
│          │  C41: 📖 接著看                    │
│          │  → Apple (TSMC最大客戶)            │
│          │  → UMC (競爭對手)                  │
│          │  → 日月光 (供應鏈夥伴)              │
└──────────┴──────────────────────────────────┘
```

---

## IV. Design System Impact Assessment

### 4.1 New Components Needed

| Component | Used By | Complexity | Priority |
|-----------|---------|------------|----------|
| Summary Card (bullet points) | C37 | Low | 🔴 Critical |
| Radar Chart (5-dimension) | C43 | Medium | 🔴 Critical |
| Delta Card (change indicators) | C39 | Low | 🟠 High |
| Band Chart (horizontal range) | C45 | Medium | 🟡 Medium |
| Treemap/Sunburst Chart | C36 | Medium | 🟡 Medium |
| Moat Strength Indicator | C46 | Low | 🟡 Medium |
| Risk Card (warning style) | C44 | Low | 🟡 Medium |
| Recommendation Card (small) | C41 | Low | 🟡 Medium |
| Mode Toggle (navbar) | C40 | Medium | 🟠 High |
| Two-Column Comparison Layout | C38 | Medium | 🟡 Medium |
| Filter/Chip Components | C42 | High | 🟢 Lower |
| Lesson Card + Quiz | C47 | High | 🟢 Lower |

### 4.2 Color System Updates

**Current Colors**: Blue #3498DB, Green #27AE60, Red #E74C3C, Light Gray #F8F9FA, Warning Yellow #FEF9E7, Tip Orange #FFF8F0, Dark Text #2C3E50, Secondary Text #7F8C8D

**Proposed Additions**:

| New Color | Hex | Usage | Justification |
|-----------|-----|-------|---------------|
| Yellow/Warning | `#F39C12` | Snowflake neutral zone, moat "narrow" | Already used in Tip card border; extend to status indicator |
| Light Orange | `#FFF8F0` | Risk card background | Already in system; reuse for risk analysis cards |
| Neutral Gray | `#BDC3C7` | Snowflake "no data" / "not applicable" | Needed for incomplete data states |

**⚠️ Key Decision**: The snowflake's 5-dimension color coding needs 3 states (good/neutral/bad). Current system only has green/red. **Recommendation**: Add `#F39C12` (yellow) as a formal "neutral/caution" status color. This is the ONLY new color needed and it aligns with the existing warning yellow `#FEF9E7` background.

### 4.3 Layout Pattern Updates

| Pattern | Used By | Description | Impact |
|---------|---------|-------------|--------|
| Dashboard Top Layer | C37+C43+C39+C45 | Stacked cards at top of Business Card page | Moderate — new "dashboard" zone above tab content |
| Two-Column Comparison | C38 | Side-by-side narrative comparison | Low — reuse existing column pattern |
| Navbar Toggle | C40 | Mode toggle in Zone A | Low — small addition to navbar |
| Relationship Cards | C41 | Small cards with relationship labels | Low — variant of existing card pattern |
| Filter Panel | C42 | Left-side filter panel on screener page | High — new page type with complex interactions |
| Lesson List | C47 | Structured lesson cards with progress | High — new page type |

### 4.4 Typography Updates

No new typography needed. All new components use existing type scales:
- Card values: `1.6rem, font-weight: 700`
- Labels: `0.85rem, color: #7F8C8D`
- Plain-language: `0.85rem, color: #27AE60, font-style: italic`

---

## V. Top UX Recommendations

### 🥇 Tier 1: Must-Have (Next Sprint)

**1. C37 Key Takeaways Summary Card**
- **Why**: Directly addresses the #1 design principle (ten-second test). Highest ROI (6-8h effort). Every other competitor has this; we're missing it.
- **Design Direction**: Place at absolute top of Business Card page. 3-5 auto-generated bullets. Each bullet ≤ 50 characters. Use existing analogy engine for plain-language generation.
- **Risk**: Low. New card component; doesn't change existing layout.

**2. C43 Company Snowflake Health Visualization**
- **Why**: Multiple international competitors prove demand (Simply Wall St, Morningstar, Stockopedia). Directly serves ten-second test. Visual health score is becoming table stakes.
- **Design Direction**: Radar chart with 5 dimensions (獲利/成長/財務/股息/估值). Color-coded (🟢🟡🔴). Plain-language explanation on click. Consider snowflake visual instead of radar for better PPT-style alignment.
- **Risk**: Medium. Radar charts can be confusing for beginners. Must test with real users.

### 🥈 Tier 2: High Priority (Sprint 2-3)

**3. C39 What Changed Recently**
- **Why**: Makes data feel alive and relevant. Directly serves "adaptive and self-evolving" core value. Beginners don't know what to look for in charts.
- **Design Direction**: Delta card with 2-3 key changes. Use 📈📉 with green/red. Plain-language explanation for each change.
- **Risk**: Low. New card component; reuses existing data pipeline.

**4. C45 Valuation Band Chart**
- **Why**: Lowest effort (8-10h) with high impact. 財報狗 proves demand. "Is this expensive or cheap?" is a universal beginner question.
- **Design Direction**: Horizontal bar showing current position in 5-year range. Color-coded zones (green=cheap, yellow=fair, red=expensive). Plain-language interpretation.
- **Risk**: Low. New chart component; straightforward Plotly implementation.

**5. C40 Beginner/Expert Mode**
- **Why**: Directly implements "progressive drill-down" design principle. No TW competitor has this. Makes all other features more accessible.
- **Design Direction**: Toggle in navbar (Zone A). Beginner mode: show only 3-4 key metrics per section, hide advanced charts. Expert mode: current behavior.
- **Risk**: Medium. Affects all pages; requires careful conditional rendering. Must maintain state across page switches.

### 🥉 Tier 3: Medium Priority (Sprint 4-6)

**6. C44 Risk Analysis**
- **Why**: Perfect historian feature. No TW competitor has plain-language risk analysis. Unique differentiator.
- **Design Direction**: 3-5 risks as cards with historical evidence. Use warning card style (orange border).
- **Risk**: Medium. Requires customer concentration data and industry risk data.

**7. C46 Moat Analysis**
- **Why**: Morningstar's moat rating is iconic but only covers US stocks. No TW competitor has this. Castle metaphor is perfect for beginners.
- **Design Direction**: Moat type + strength indicator. Historical evidence of moat protection. Plain-language explanation.
- **Risk**: Medium-High. Requires manual curation for top 20 stocks.

**8. C36 Visual Revenue Tree**
- **Why**: Extends existing pie chart naturally. Shows business model visually. No TW competitor has this.
- **Design Direction**: Treemap or sunburst chart. Click to drill down. Plain-language labels.
- **Risk**: Medium. Hierarchical revenue data may not be available for all stocks.

### Tier 4: Lower Priority (Post-Sprint 6)

**9. C41 Read Next Recommendations**
- **Why**: Unique relationship-based discovery. Low effort (6-8h). Extends existing group structure data.
- **Design Direction**: 2-3 recommendation cards at bottom of Business Card page. Label relationship type (客戶/競爭/供應鏈).
- **Risk**: Low. Reuses existing data.

**10. C38 Compare Stories**
- **Why**: Extends existing peer comparison. Narrative layer adds unique value.
- **Design Direction**: Two-column layout on Peer Comparison page. Side-by-side key events and business model differences.
- **Risk**: Medium. Requires narrative data for both companies.

**11. C42 Stock Screener**
- **Why**: 財報狗's #1 feature. Transforms product from lookup to discovery. But complex UI risks diluting core positioning.
- **Design Direction**: Beginner-friendly presets only ("穩定收息", "成長潛力"). Results link to Business Card pages. No raw metric filters for beginners.
- **Risk**: High. Complex feature; must maintain historian positioning.

**12. C47 Education Academy**
- **Why**: Long-term strategic differentiator. Transforms product from tool to platform. But highest effort (20-30h).
- **Design Direction**: 10-15 structured lessons. Each lesson: title, 3-5 min read, real TW example, quiz. Progressive difficulty.
- **Risk**: High. Significant new UI surface; requires content creation.

---

## VI. UX Impact vs. Implementation Cost Ranking

| Rank | ID | Feature | UX Impact | Effort | ROI Score |
|------|----|---------|-----------|--------|-----------|
| 1 | C37 | Key Takeaways | 🔴 Critical | 6-8h | ⭐⭐⭐ |
| 2 | C45 | Valuation Band | 🟠 High | 8-10h | ⭐⭐⭐ |
| 3 | C39 | What Changed | 🟠 High | 8-10h | ⭐⭐⭐ |
| 4 | C43 | Company Snowflake | 🔴 Critical | 12-16h | ⭐⭐ |
| 5 | C41 | Read Next | 🟡 Medium | 6-8h | ⭐⭐ |
| 6 | C40 | Beginner/Expert | 🟠 High | 10-14h | ⭐⭐ |
| 7 | C36 | Revenue Tree | 🟡 Medium | 10-14h | ⭐⭐ |
| 8 | C44 | Risk Analysis | 🟠 High | 10-14h | ⭐⭐ |
| 9 | C46 | Moat Analysis | 🟡 Medium | 12-16h | ⭐⭐ |
| 10 | C38 | Compare Stories | 🟡 Medium | 12-16h | ⭐ |
| 11 | C42 | Stock Screener | 🟠 High | 16-24h | ⭐ |
| 12 | C47 | Education Academy | 🟠 High | 20-30h | ⭐ |

---

## VII. Key Design Risks & Mitigations

### Risk 1: Feature Overload on Business Card Page
**Problem**: C37 + C39 + C43 + C45 all want to be at the top of the Business Card page. This could create a wall of cards that overwhelms beginners — the exact opposite of the ten-second test.
**Mitigation**: 
- Integrate C37 and C43 into a single "Company Snapshot" card (takeaways + snowflake in one component)
- Place C39 and C45 below the snapshot, in a "details" section
- Use progressive disclosure: show snapshot by default, expand details on scroll/click

### Risk 2: Radar Chart Usability
**Problem**: Radar/snowflake charts are notoriously confusing for beginners. The "ten-second test" could fail if users can't interpret the visual.
**Mitigation**:
- Use simple color coding (🟢🟡🔴) with large, clear labels
- Add plain-language interpretation below the chart: "這家公司整體健康，主要因為..."
- Consider alternative visual: 5 horizontal bars (one per dimension) instead of radar
- Test with real beginners before committing to radar

### Risk 3: Mode Toggle Complexity
**Problem**: C40 Beginner/Expert mode affects ALL pages. Conditional rendering logic could create maintenance nightmares and inconsistent experiences.
**Mitigation**:
- Define clear "beginner" vs "expert" metric lists upfront
- Beginner mode hides entire sections, not individual metrics (simpler logic)
- Store mode in session_state; persist across page switches
- Expert mode = current behavior (zero regression risk)

### Risk 4: Maintaining "Historian" Positioning with Screener
**Problem**: C42 Stock Screener could make Stock Explorer feel like a stock-picking tool, undermining the "historian" positioning.
**Mitigation**:
- Frame as "選股探索" (stock exploration), not "選股工具" (stock picking tool)
- Use educational presets ("穩定收息", "成長潛力"), not raw metric filters
- Results show Business Card pages, not raw data tables
- Add disclaimer: "探索有趣的公司，不是投資建議"

---

## VIII. Recommended Implementation Sequence

### Sprint 11 (Next Sprint) — "Ten-Second Test Sprint"
| Feature | Effort | Deliverable |
|---------|--------|-------------|
| C37 Key Takeaways | 6-8h | Auto-generated summary card at top of Business Card page |
| C45 Valuation Band | 8-10h | Horizontal band chart card on Business Card page |

**Combined effort**: 14-18h
**Design impact**: Business Card page now passes the ten-second test with synthesis + valuation context

### Sprint 12 — "Visual Health Sprint"
| Feature | Effort | Deliverable |
|---------|--------|-------------|
| C43 Company Snowflake | 12-16h | 5-dimension radar chart at top of Business Card page |
| C39 What Changed | 8-10h | Delta card showing recent changes |

**Combined effort**: 20-26h
**Design impact**: Business Card page now has complete "dashboard layer" (health + changes + takeaways + valuation)

### Sprint 13 — "Progressive Disclosure Sprint"
| Feature | Effort | Deliverable |
|---------|--------|-------------|
| C40 Beginner/Expert | 10-14h | Mode toggle in navbar; simplified beginner view |
| C41 Read Next | 6-8h | Relationship-based recommendations |

**Combined effort**: 16-22h
**Design impact**: Product now serves both beginners and advanced users; discovery mechanism in place

### Sprint 14+ — "Historian's Deep Dive"
| Feature | Effort | Deliverable |
|---------|--------|-------------|
| C44 Risk Analysis | 10-14h | Historical risk cards |
| C46 Moat Analysis | 12-16h | Competitive advantage assessment |
| C36 Revenue Tree | 10-14h | Hierarchical revenue visualization |
| C38 Compare Stories | 12-16h | Narrative comparison mode |

**Combined effort**: 44-60h
**Design impact**: Stock Explorer becomes the most comprehensive "historian" tool in TW market

---

*Created: 2026-06-15*
*Author: Design Reviewer (Designer)*
*Status: Ready for team review*
