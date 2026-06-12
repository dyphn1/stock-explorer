## 2026-06-13 Design Discussion — Post-Sprint 10 Feature Directions

### Context
Sprint 10 is locked: C34 (Company Story Timeline) + C105 (Simple/Detailed Toggle) + M5 remediation + D-061 (test infra). This discussion evaluates what comes **after** Sprint 10 — ranking the remaining backlog by UX impact and providing design direction for each.

---

### High-UX-Impact Features (ranked)

| Rank | ID | Title | Priority | Effort | UX Impact Rationale |
|------|----|-------|----------|--------|---------------------|
| 1 | C58 | Beginner Onboarding Flow | P1 | 14-20h | **Retention-critical.** Without onboarding, beginners bounce before discovering any other feature. Every other feature's value is gated by this. |
| 2 | C43 | Company Snowflake Health Visualization | P1 | 12-16h | **Ten-second test enabler.** Gives beginners an instant visual answer to "How healthy is this company?" — the single most important question for a beginner. |
| 3 | C56 | Explain This Metric | P1 | 12-16h | **Core design system fulfillment.** The design system *requires* "All professional terms must have plain-language translations" — this feature delivers it interactively. |
| 4 | C42 | Stock Screener / Discovery Engine | P1 | 16-24h | **Product transformation.** Converts Stock Explorer from a lookup tool (user must know the stock) into a discovery tool (user explores by criteria). |
| 5 | C45 | Valuation Band Chart | P2 | 8-10h | **Highest ROI.** 8-10h effort for a feature that 財報狗 proves is one of the most-used features. Beginners cannot interpret P/E without historical context. |
| 6 | C48 | Company Story Card | P2 | 8-12h | **Ten-second test made real.** A 30-second visual summary at the top of every company page — the "hook" that keeps users exploring. |
| 7 | C51 | Sector Heatmap | P2 | 8-12h | **Context expansion.** Beginners think in companies; this teaches them to think in sectors. Visual-first, aligns with PPT-style. |
| 8 | C52 | Quiz Mode | P2 | 10-14h | **Active learning.** Transforms passive reading into active recall. Khan Academy proves this is the gold standard for education retention. |
| 9 | C44 | "What Could Go Wrong" Risk Analysis | P2 | 10-14h | **Historian differentiator.** No TW competitor has plain-language risk analysis with historical evidence. Perfect alignment with "explain, don't predict." |
| 10 | C46 | Moat Analysis | P2 | 12-16h | **Unique TW differentiator.** Morningstar's moat rating is iconic but US-only. No TW competitor has this. |

---

### Design Direction per Feature

#### 1. C58 — Beginner Onboarding Flow (P1, Retention-Critical)

**Design Direction:**
- **5-step guided tour** (not 7 — we're a web app, not a broker; fewer steps = higher completion):
  1. "Welcome to 股識" — one sentence: "We help you understand companies, not pick stocks."
  2. "Search for a company" — highlight the sidebar search box with a pulsing blue border (`#3498DB`)
  3. "Read the business card" — navigate to TSMC's page, highlight the one-liner
  4. "Explore the story" — click the Story tab (C34 from Sprint 10), show the timeline
  5. "You're ready!" — suggest 3 beginner-friendly companies: TSMC (2330), 鴻海 (2317), 富邦媒 (8454)
- **PPT-style:** Each step is one screen, one key point, < 200 characters of text
- **Ten-second test:** After onboarding, a beginner should be able to say "This tool helps me understand companies by showing me their story"
- **Skip option:** Always visible — "Skip tour" in the top-right corner. Forcing onboarding creates resentment
- **Replay:** A "? 新手導覽" button in the Zone A navbar (right side, secondary text color `#7F8C8D`) to replay anytime
- **Session state:** `onboarding_complete` flag. Show onboarding only on first visit. Do NOT show on every page load

**Competitor reference:** 玉山證券 "Beginner Village" (7 steps — too many for web), Robinhood "First Stock" (too trading-focused), Zerodha Varsity module 1 (closest match — one concept per step)

---

#### 2. C43 — Company Snowflake Health Visualization (P1, Ten-Second Test Enabler)

**Design Direction:**
- **Placement:** Top of the business card page, below the one-liner, above all other metrics. This is the FIRST thing a user sees
- **Visual format:** Radar chart (5 axes) using Plotly — NOT a snowflake shape (too complex for Streamlit). Five dimensions:
  1. 獲利能力 (Profitability) — ROE-based
  2. 成長潛力 (Growth) — Revenue growth trend
  3. 財務健康 (Financial Health) — Debt ratio + current ratio
  4. 股息品質 (Dividend Quality) — Dividend yield + payout consistency
  5. 估值合理 (Valuation) — P/E vs historical range
- **Scoring:** Each dimension scored 0-5 (0=poor, 5=excellent). Use color coding: `#27AE60` (4-5), `#F39C12` (2-3), `#E74C3C` (0-1)
- **Plain-language:** Below the radar chart, show ONE sentence per dimension, e.g.:
  - "🟢 獲利能力強：ROE 25%，每100元股東資金賺25元"
  - "🟡 估值合理：本益比18倍，處於歷史中間位置"
- **Benchmark-oriented:** Show a subtle dotted line for the industry leader's score on the same radar chart (aligns with core value #5)
- **Text limit:** Total text below chart ≤ 200 characters (design system Section V.2)
- **Ten-second test:** A beginner should be able to say "TSMC is strong in profitability and growth, but the valuation is average" within 10 seconds

**Competitor reference:** Simply Wall St snowflake (visual model), Morningstar star rating (simplicity model), TipRanks Smart Score (composite model). **Avoid:** Simply Wall St's proprietary algorithm opacity — our scores must be explainable.

---

#### 3. C56 — Explain This Metric (P1, Design System Fulfillment)

**Design Direction:**
- **Trigger:** An "❓" icon button next to every metric label on the business card page. Small, subtle, `#7F8C8D` color — not intrusive
- **Interaction:** Click → expander opens below the metric card with:
  1. **One-sentence definition** (≤ 15 characters tagline): "ROE = 淨利 / 股東權益"
  2. **Plain-language analogy** (≤ 2 sentences): "ROE就像是你投資100元，一年能賺幾元。ROE 25%代表你每投資100元，一年賺25元"
  3. **Mini chart:** A small Plotly sparkline showing this metric's 3-year trend (inline, ~80px height)
  4. **"為什麼重要"** (Why it matters): One sentence, e.g. "ROE越高，代表公司用股東的錢賺錢的效率越好"
- **Priority metrics (first 10):** ROE, P/E, P/B, gross margin, revenue growth, dividend yield, debt ratio, EPS, free cash flow, institutional ownership
- **Design system compliance:** Each explanation ≤ 2 sentences (Section V.2). Charts ≤ 80px height (mini inline). Text ≤ 200 characters per explanation
- **No AI dependency:** All explanations are pre-written in `metric_explanations.yaml`. Template-based, not LLM-generated. This ensures consistency and avoids hallucination
- **Ten-second test:** A beginner clicks ❓ on ROE and within 10 seconds understands "ROE tells me how efficiently the company uses shareholder money"

**Competitor reference:** Robinhood metric tooltips (simplest model), Magnify.money AI visual explanations (most advanced), 永豐金證券 Financial Statement Visualizer (interactive model). **Adopt:** Robinhood's simplicity + Magnify's visual approach. **Avoid:** AI-generated explanations (hallucination risk, inconsistent quality).

---

#### 4. C42 — Stock Screener / Discovery Engine (P1, Product Transformation)

**Design Direction:**
- **Page placement:** New tab in Zone A navbar: "🔍 選股探索"
- **Beginner-first presets (3-4 buttons):**
  - "穩定收息" → dividend yield > 4%, payout ratio < 70%
  - "成長潛力" → revenue growth > 15% for 3 years
  - "便宜估值" → P/E < industry average, P/B < 2
  - "護城河寬" → ROE > 20%, gross margin > 40%
- **Results format:** Each result is a card (not a table row):
  - Company name + ticker + one-liner
  - 3 key metrics with color coding
  - "了解更多" button → navigates to business card page
- **PPT-style:** One key point per result card. Maximum 10 results per page (no infinite scroll)
- **No "custom screening" in v1:** Custom screening with 100+ metrics is what 財報狗 does. We differentiate by making the presets educational — each preset explains WHY these criteria matter
- **Plain-language:** Each preset has a one-sentence explanation: "穩定收息 = 公司每年穩定配息，適合需要現金流的投資人"
- **Ten-second test:** A beginner clicks "穩定收息" and within 10 seconds understands "These are companies that pay consistent dividends"

**Competitor reference:** 財報狗 screener (most comprehensive), StockEdge visual heatmap (most visual), Zerodha Varsity screening + stories (best educational integration). **Adopt:** 財報狗's preset approach + Zerodha's educational context. **Avoid:** 財報狗's 100+ metric custom screener (too complex for beginners, wrong positioning).

---

#### 5. C45 — Valuation Band Chart (P2, Highest ROI)

**Design Direction:**
- **Placement:** On the business card page, in the "Financial Health" section or as a standalone card
- **Visual format:** Horizontal bar chart showing:
  - 5-year P/E range (min to max) as a light gray bar (`#F8F9FA`)
  - Current P/E as a blue vertical line (`#3498DB`)
  - Industry average P/E as a dotted green line (`#27AE60`)
- **Plain-language interpretation (≤ 2 sentences):**
  - "目前本益比18倍，處於過去5年區間(12-25倍)的中間位置，不算貴也不算便宜"
- **Color coding:** Current P/E position in the range:
  - Bottom 25%: `#27AE60` (cheap) + "估值偏低"
  - Middle 50%: `#F39C12` (fair) + "估值合理"
  - Top 25%: `#E74C3C` (expensive) + "估值偏高"
- **Text limit:** ≤ 200 characters total (chart title + interpretation)
- **Ten-second test:** A beginner sees the chart and within 10 seconds understands "TSMC's P/E is in the middle of its historical range — fairly valued"

**Competitor reference:** 財報狗 P/E band chart (proven demand), Morningstar fair value with uncertainty (visual model). **Adopt:** 財報狗's horizontal band + plain-language interpretation. **Avoid:** Morningstar's premium paywall approach.

---

#### 6. C48 — Company Story Card (P2, Ten-Second Test Made Real)

**Design Direction:**
- **Placement:** TOP of the business card page, above even the C43 Snowflake. This is the hero element
- **Content (4 elements only):**
  1. **One-liner** (≤ 15 characters): "台積電是全球90%先進晶片的製造商"
  2. **3 key metrics** (auto-selected based on what's most notable): e.g., ROE 25%, Gross Margin 55%, Revenue Growth 18%
  3. **One "Did You Know?" fact** (rotating): "你知道嗎？台積電佔全球先進晶片市佔率超過90%"
  4. **"了解更多 →" button:** Scrolls down to the full analysis
- **Visual style:** Card with `#F8F9FA` background, `#3498DB` left border (4px), padding 1.2rem. Larger than standard info cards
- **Chart:** None. This is text + numbers only. Charts come below in the detailed sections
- **Ten-second test:** A beginner reads the story card and within 10 seconds can say "TSMC makes most of the world's advanced chips, is very profitable, and is growing fast"

**Competitor reference:** Stake "Company Story" cards (30-second visual summaries), Finimize "Quick Summary" (bite-sized), Public.com story cards (visual-first). **Adopt:** Stake's card structure + Finimize's brevity. **Avoid:** Public.com's social features (not relevant).

---

#### 7. C51 — Sector Heatmap (P2, Context Expansion)

**Design Direction:**
- **Page placement:** New tab in Zone A navbar: "🔥 產業熱度"
- **Visual format:** Plotly treemap (not heatmap — treemap is more intuitive for beginners). Each rectangle = one TW sector. Size = market cap. Color = daily performance (green = up, red = down)
- **Interaction:** Click a sector → expand to show top 3 companies in that sector with their individual performance
- **Plain-language:** Below the treemap, one sentence: "今天半導體族群上漲3%，主要受AI晶片需求帶動"
- **PPT-style:** One key point: "Which sectors are hot today?"
- **Time selector:** 1 day (default), 1 week, 1 month — placed at the top of Zone C (per Section IV.3)
- **Ten-second test:** A beginner looks at the treemap and within 10 seconds understands "Tech and semiconductor sectors are up today, energy is down"

**Competitor reference:** StockEdge sector heatmaps (visual model), Moomoo "Market Heatmap with Education" (educational overlay). **Adopt:** StockEdge's visual approach + Moomoo's educational context. **Avoid:** TradingView's complex multi-chart layouts (too advanced).

---

#### 8. C52 — Quiz Mode (P2, Active Learning)

**Design Direction:**
- **Trigger:** A "🧪 小測驗" button at the bottom of the business card page (after all content)
- **Format:** 5 multiple-choice questions per quiz, generated from templates using real data from the current company
- **Question types:**
  1. Metric interpretation: "TSMC的毛利率是55%，代表什麼？" → A) 每賣100元賺55元 B) 花55元在研發 C) 配55元股息
  2. Comparison: "台積電的ROE比聯電子高還是低？"
  3. Concept: "本益比(P/E)越高，代表股票越便宜還是越貴？"
  4. Risk: "台積電最大的風險來源是什麼？" → A) 客戶集中度高 B) 員工太多 C) 現金太少
  5. Story: "過去3年，台積電的營收趨勢是？" → A) 穩定成長 B) 持續下降 C) 波動不定
- **Feedback:** Instant. Correct → green highlight + "答對了！" + one-sentence explanation. Incorrect → red highlight + "答錯了" + correct answer + explanation
- **Score display:** "你答對了 4/5 題" with a simple progress bar
- **No high scores or leaderboards:** This is learning, not competition. Avoid gamification that creates anxiety
- **PPT-style:** One question per screen (expander or page-like section). Clean, focused, no distractions
- **Ten-second test:** After the quiz, a beginner should be able to explain the key metrics of the company they just analyzed

**Competitor reference:** Khan Academy interactive exercises (gold standard), Zerodha Varsity module quizzes (structured), Finimize Academy quizzes (completion certificates). **Adopt:** Khan Academy's instant feedback model. **Avoid:** Finimize's completion certificates (too complex for v1).

---

#### 9. C44 — "What Could Go Wrong" Risk Analysis (P2, Historian Differentiator)

**Design Direction:**
- **Placement:** On the business card page, as a dedicated section (not a separate tab)
- **Header:** "⚠️ 風險分析" with a light yellow background (`#FEF9E7`)
- **Format:** 3-5 risk cards, each with:
  1. **Risk title** (≤ 15 characters): "客戶集中度高"
  2. **What it means** (≤ 2 sentences): "台積電90%營收來自3個客戶。如果任何一個客戶轉向競爭對手，營收可能下降30%"
  3. **Historical evidence:** "2023年，蘋果曾考慮轉向英特爾，台積電股價單週下跌8%"
  4. **What to watch:** "注意蘋果的晶片訂單變化、英特爾製程進度"
- **Tone:** Factual, educational, never alarmist. Use past tense — "This happened before" not "This will happen"
- **No risk score:** Unlike Simply Wall St's risk analysis, we don't give a numerical risk score. Scores create false precision. Instead, we explain risks in plain language
- **Ten-second test:** A beginner reads the risk section and within 10 seconds understands "TSMC's main risk is that it depends on too few customers"

**Competitor reference:** Simply Wall St visual risk analysis (visual model), Morningstar uncertainty rating (quantitative model), Tastytrade probability analysis (probabilistic model). **Adopt:** Simply Wall St's visual approach + Tastytrade's probabilistic framing. **Avoid:** Morningstar's numerical risk scores (too abstract for beginners).

---

#### 10. C46 — Moat Analysis (P2, Unique TW Differentiator)

**Design Direction:**
- **Placement:** On the business card page, as a dedicated section
- **Header:** "🏰 護城河分析" with a light orange background (`#FFF8F0`)
- **Format:** Single card with:
  1. **Moat type** (icon + label): "技術領先" (technology), "品牌價值" (brand), "成本優勢" (cost), "網路效應" (network), "轉換成本" (switching costs)
  2. **Moat strength:** "寬" (wide) / "窄" (narrow) / "無" (none) — with color coding
  3. **Historical evidence** (≤ 2 sentences): "過去10年，這個技術領先讓台積電的毛利率維持在50%以上"
  4. **Plain-language explanation:** "護城河就像城堡周圍的城河，保護公司不被競爭對手攻擊。台積電的城河是技術領先，因為全球只有它能生產最先進的晶片"
- **Data source:** Manual curation for top 20 stocks. Template-based for others (using industry classification + financial metrics to infer moat type)
- **No prediction:** "This is what the moat IS and how it has protected the company" — never "This is how long the moat will last"
- **Ten-second test:** A beginner reads the moat section and within 10 seconds understands "TSMC's competitive advantage is that it's the only company that can make the most advanced chips"

**Competitor reference:** Morningstar moat rating (gold standard), TEJ industry analysis (data-driven). **Adopt:** Morningstar's moat type classification + plain-language explanation. **Avoid:** Morningstar's "wide/narrow/none" without explanation — we always explain WHY.

---

### Design System Updates Needed

#### 1. New Component: Hero Story Card (for C48)
The current design system (Section III.3) defines Info Cards and Tip Cards but has no "Hero Card" component. Add:

```html
<!-- Hero story card (blue border, larger) -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.5rem;border-left:6px solid #3498DB;margin:0.5rem 0 1rem 0;">
    <div style="font-size:0.85rem;color:#7F8C8D;">{label}</div>
    <div style="font-size:1.8rem;font-weight:700;color:#2C3E50;margin:0.3rem 0;">{value}</div>
    <div style="display:flex;gap:1rem;margin-top:0.5rem;">
        <!-- 3 key metrics as mini cards -->
    </div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.5rem;">{did_you_know}</div>
</div>
```

#### 2. New Component: Risk Card (for C44)
```html
<!-- Risk card (yellow border) -->
<div style="background:#FEF9E7;border-radius:12px;padding:1.2rem;border-left:4px solid #F1C40F;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">⚠️ {risk_title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.3rem;line-height:1.6;">{explanation}</div>
    <div style="font-size:0.8rem;color:#7F8C8D;margin-top:0.3rem;">📜 {historical_evidence}</div>
</div>
```

#### 3. New Component: Metric Explanation Expander (for C56)
The design system needs a standard pattern for inline expandable explanations:
- Trigger: `❓` icon button, `key="explain_{metric}_{stock_id}"`
- Content: Definition + analogy + mini chart + "為什麼重要"
- Max height: 200px (prevents page from becoming too long)
- Background: `#F8F9FA` with `#3498DB` left border

#### 4. New Component: Quiz Card (for C52)
```html
<!-- Quiz card -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #9B59B6;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">🧪 {question}</div>
    <div style="margin-top:0.5rem;">
        <!-- Options as st.button elements -->
    </div>
    <div style="font-size:0.85rem;color:{feedback_color};margin-top:0.3rem;">{feedback}</div>
</div>
```

#### 5. Color System Extension
The current color system (Section III.1) has 7 colors. Add one:
- **Quiz/Purple:** `#9B59B6` — for quiz mode, concept comparison, and educational interactive elements. This is NOT a status color (red/green/blue rule still applies) — it's an interaction color for educational features.

#### 6. Typography Addition
Add a "mini chart label" style:
- Mini chart labels: `font-size: 0.75rem, color: #7F8C8D`
- This is needed for the inline sparklines in C56 (Explain This Metric)

#### 7. Text Limit Adjustment for Interactive Content
Current text limit: 200 characters per page (Section V.2). This is too restrictive for interactive features:
- **Proposal:** 200 characters for *static* text. Interactive content (expanders, explanations) can have up to 400 characters total, but the *visible* text before expansion must still be ≤ 200 characters
- **Rationale:** C56 explanations need ~300 characters for definition + analogy + "why it matters." The expander pattern keeps the page clean while allowing deeper content

---

### Competitor Patterns to Adopt

| Pattern | Source | Why Adopt | How to Adapt |
|---------|--------|-----------|--------------|
| **Instant visual health score** | Simply Wall St, Morningstar, TipRanks | Beginners need a 30-second answer to "Is this company good?" | C43 Snowflake — radar chart with 5 dimensions, plain-language explanations |
| **Metric tooltips on every data point** | Robinhood, 永豐金證券 | Design system requires plain-language translations — this delivers it interactively | C56 Explain This Metric — ❓ button next to every metric |
| **Beginner onboarding tour** | 玉山證券, Robinhood, Zerodha Varsity | Without onboarding, beginners bounce before discovering value | C58 — 5-step guided tour, always skippable |
| **Preset-based stock screening** | 財報狗, StockEdge | Beginners can't build custom screens — presets lower the barrier | C42 — 4 educational presets with plain-language explanations |
| **Valuation band chart** | 財報狗, Morningstar | P/E without context is meaningless — beginners need historical range | C45 — horizontal band chart with plain-language interpretation |
| **Interactive concept explanations** | Magnify.money, Khan Academy | Static text is insufficient — users expect to click and explore | C56 + C52 — expandable explanations + quiz mode |
| **Pre-investment checklist** | 永豐金證券, Tastytrade | Teaches users WHAT to look for, not WHAT to buy — perfect "historian" feature | C62 — 5-item checklist at bottom of company page |
| **Company story cards** | Stake, Finimize, Public.com | 30-second visual summary — the "ten-second test" made real | C48 — hero card at top of business page |
| **Sector heatmap with education** | Moomoo, StockEdge | Beginners think in companies — this teaches sector-level thinking | C51 — treemap with plain-language explanations |
| **Concept comparison** | Magnify.money | Helps beginners understand metrics as tools, not answers | C57 — side-by-side concept comparison |

### Competitor Patterns to Avoid

| Pattern | Source | Why Avoid |
|---------|--------|-----------|
| **Black-box scoring** | Simply Wall St (proprietary algorithm), TipRanks (Smart Score) | Violates our "explain, don't predict" principle — scores must be explainable |
| **AI stock picking** | Tickeron (AI Grade), Moomoo (AI Analyst) | Violates "historian, not stock picker" positioning |
| **Social trading / copy investing** | eToro (CopyTrader), 富邦e富 (social following) | Violates "not a stock picker" principle — shifts focus from learning to following |
| **Community forums** | JZ Invest, Dcard, Reddit r/investing | High moderation cost, off-brand for "historian" positioning, potential for misinformation |
| **Buy/sell signals** | Tickeron, Simply Wall St (some features) | Violates core positioning — we explain what happened, not what to do |
| **Dense data tables** | 財報狗, TEJ, 鉅亨網 | Violates PPT-style design principle — one key point per page |
| **Video-first content** | Khan Academy, Naver Academy | High production cost, doesn't leverage our text+visual strength |
| **Gamification with financial rewards** | Robinhood (Learn → Earn stock) | Inappropriate for a free tool, creates wrong incentives |
| **Complex multi-chart layouts** | TradingView (8-chart), 鉅亨網 (dense portal) | Violates "one key point per page" and "ten-second test" |
| **Push notifications** | Yahoo奇摩股市, CMoney, StatementDog | Streamlit limitation — push notifications require native app or messaging bot |

---

### Recommendations

#### Sprint 11 (Immediate Post-Sprint 10)
**Must-build (P1, highest UX impact):**
1. **C58 Beginner Onboarding Flow** — Without this, every other feature's value is gated. This is the single most important feature for beginner retention.
2. **C43 Company Snowflake Health Visualization** — The "ten-second test" made visual. This is the feature that makes Stock Explorer feel like a professional tool, not a data dump.

**Should-build (if capacity allows):**
3. **C45 Valuation Band Chart** — 8-10h effort, highest ROI in the entire backlog. 財報狗 proves this is a must-have feature.

#### Sprint 12 (Short-Term)
4. **C56 Explain This Metric** — Fulfills the design system's plain-language requirement interactively. Transforms every data point into a learning opportunity.
5. **C48 Company Story Card** — The "hook" that keeps users exploring after the first 10 seconds.
6. **C42 Stock Screener / Discovery Engine** — Transforms the product from lookup to discovery. Largest effort (16-24h) but highest strategic value.

#### Sprint 13 (Medium-Term)
7. **C51 Sector Heatmap** — Expands thinking from companies to sectors.
8. **C52 Quiz Mode** — Transforms passive reading into active learning.
9. **C44 Risk Analysis** — Unique "historian" differentiator, no TW competitor has it.

#### Sprint 14+ (Long-Term)
10. **C46 Moat Analysis** — Manual curation for top 20 stocks, template-based for others.
11. **C47 Financial Education Academy** — The "endgame" feature that transforms Stock Explorer from tool to platform. 20-30h effort — plan carefully.
12. **C55 Investment Diary** — Unique "historian of self" feature. Low competition, high differentiation.

#### Design System Maintenance
- **Add 4 new components** to the design system: Hero Story Card, Risk Card, Metric Explanation Expander, Quiz Card
- **Add 1 new color** (purple `#9B59B6`) for educational interactive elements
- **Update text limit rules** to accommodate interactive content (200 chars static, 400 chars expandable)
- **Add mini chart label** typography style

#### Key Design Principles for Post-Sprint 10
1. **Onboarding first** — C58 is the gating feature for all other features
2. **Visual synthesis before data** — C43 (Snowflake) and C48 (Story Card) give instant understanding before detailed metrics
3. **Interactive education over static text** — C56 (Explain This Metric) and C52 (Quiz) make learning active
4. **Discovery over lookup** — C42 (Screener) and C51 (Sector Heatmap) expand the product beyond single-stock lookup
5. **Plain-language always** — Every feature must pass the "ten-second test" and the "grandmother test" (could you explain this to your grandmother?)
6. **Historian, not picker** — Every feature must explain what happened, never predict what will happen

---

*This design discussion was prepared by the Design Reviewer for the Stock Explorer team. It evaluates the post-Sprint 10 backlog from a UX/design perspective, prioritizing features by their impact on the beginner investor experience. All recommendations align with the PPT-style design system, the ten-second test principle, and the "historian, not stock picker" product positioning.*
