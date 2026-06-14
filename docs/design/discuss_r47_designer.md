# 2026-06-15 Design Review — Discussion Round 47

> **Reviewer**: Design Reviewer
> **Sprint**: Discussion Cycle Round 47
> **Current Design Grade**: C+ (stable since Round 7)
> **Focus**: Sprint 23 Feature Candidates — C202, C199, C200
> **Prerequisite**: Round 46 evaluations (discuss_r46_designer.md) for C199, C200, C202 already completed

---

## Context

Round 46 evaluated all 8 features (C199–C206) and produced detailed design specs for the top picks. Round 47 now re-evaluates the three Sprint 23 candidates — **C202** (Story Arc Labels, P2 MUST), **C199** (Bear vs Bull Debate Cards, P2 SHOULD), and **C200** (What If Calculator, P2 COULD) — against:

1. The current codebase state (post-Sprint 21, Sprint 22 C201 in progress)
2. The known design issues (81 cumulative issues, C+ grade)
3. The existing component library and design system constraints
4. Interactions with C201 (Daily Market Story) which is currently being built
5. Realistic assessment of design feasibility within stated effort budgets (10–16h)

---

## C202: "Story Arc" Timeline Labels — Auto-Detected Narrative Arcs

### UX Impact: **Medium-High** (confirmed from Round 46)

**Rationale**: C202 directly serves the **historian positioning** — it transforms the existing timeline from a flat event list into a narrative with named chapters. This is the single most differentiating feature for the platform's core identity. No TW stock app presents company history as "story arcs."

**Updated Assessment (Round 47)**:

The existing `story_timeline.py` page and `timeline_service.py` already render timeline entries with severity-based border colors. C202 adds a **layer of interpretation** on top of this existing structure. The UX impact depends entirely on arc detection quality — if arcs feel insightful, users will spend 2–3× longer on timeline pages; if arcs feel arbitrary, the feature becomes noise that clutters the existing timeline.

**Key UX Question**: Will auto-detected arcs match the user's mental model? For well-known companies (e.g., TSMC going through "📈 成長期" during the AI boom), yes. For obscure companies with sparse data, arcs may feel random.

### Design Direction

**Layout — Arc Band Above Timeline**:

```
┌─────────────────────────────────────────────────┐
│  Zone C: 公司故事時間軸                           │
│                                                 │
│  ┌─────────────────────────────────────────────┐│
│  │  📈 成長期 (2020–2023)  ⚠️ 挑戰期 (2024–)  ││ ← Arc band
│  │  [████████████░░░] [░░░░░░░░░░░░]           ││ ← Proportional bars
│  └─────────────────────────────────────────────┘│
│                                                 │
│  ── 2024 ────────────────────────────────────── │
│  │ ⚠️ Q3 營收意外下滑，市場擔憂成熟製程需求      │
│  │ 💡 這主要是因為手機晶片庫存調整               │
│  ─────────────────────────────────────────────  │
│  │ 📰 宣布美國廠擴建計畫，投資超過 100 億美元    │
│  ───────────────────────────────────────────── │
│  ── 2023 ────────────────────────────────────── │
│  │ 📈 AI 營收占比首次超過 10%                    │
│  │ 💡 這代表台積電成功打入 AI 供應鏈             │
│  ───────────────────────────────────────────── │
│  │ 🔄 宣布與日本 Sony 合資設廠                    │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Arc Band Component** (new `_arc_band()` helper in `_router_base.py`):

```python
def _arc_band(arcs: list[dict]) -> None:
    """Render narrative arc labels as a horizontal band above the timeline.

    Args:
        arcs: List of arc dicts, each containing:
            - name: Arc name (e.g. "成長期")
            - icon: Emoji icon (e.g. "📈")
            - start_year: int
            - end_year: int (or "now" for ongoing)
            - color: Hex color from design system
            - explanation: One-line plain-language description (≤ 60 chars)
            - confidence: Float 0.0–1.0 (arc detection confidence)

    Max 4 arcs per company. Band uses proportional bar widths.
    """
```

**Arc Color System** (extends design system):

| Arc Type | Color | Hex | Icon |
|----------|-------|-----|------|
| 成長期 (Growth) | Green | `#27AE60` | 📈 |
| 挑戰期 (Challenge) | Yellow | `#F39C12` | ⚠️ |
| 轉型期 (Transformation) | Blue | `#3498DB` | 🔄 |
| 衰退期 (Decline) | Red | `#E74C3C` | 📉 |

⚠️ **DESIGN NOTE**: These colors reuse the existing design system palette — NO new colors introduced. Green = positive, Red = negative, Blue = neutral/transitional, Yellow = caution. This is consistent with existing severity badge colors.

**Design Compliance**:

| Rule | Status | Notes |
|------|--------|-------|
| Zone separation | ✅ | Arc band is in Zone C only, above timeline content |
| Color system | ✅ (conditional) | Uses existing palette; arcs reuse severity colors — NOTE: `#F39C12` is in design system as "warning" per Round 7 issue log, NOT in base palette but explicitly documented as warning bg in III.3.1 |
| Text limits | ✅ | Arc name ≤ 15 chars; explanation ≤ 60 chars; total band text ≤ 100 chars |
| PPT style | ⚠️ | Timeline page already has moderate text; arc band adds ~100 chars — must reduce timeline entries shown (default to top 8, with "顯示更多") |
| Ten-second test | ✅ | "這家公司經歷了哪些階段？四個顏色告訴你" |
| No advice | ✅ | Arcs describe what happened, not what to do |
| Mobile responsive | ⚠️ | Horizontal arc band wraps on narrow screens — needs stacked arc chips fallback |

**Component Reuse**:
- Arc band renders as inline HTML within a `_summary_card()` wrapper — no new raw HTML needed
- Individual arc chips follow `_mini_score_card()` visual pattern (colored border-left + label + value)
- Timeline entries use existing `_render_timeline_card()` — no changes needed to existing component

**Interaction Pattern** (progressive disclosure):
1. **Default view**: Arc band visible, top 8 timeline entries visible
2. **Tap arc chip**: Filter timeline to show only entries within that arc's date range (using existing `filter_by_timeline()` with custom date range)
3. **"顯示最多" expander**: Full timeline with all entries
4. **Hover/Tap arc explanation**: `_glossary_tooltip()` style popover with plain-language description

**Service Layer** (no Streamlit):

```python
# New: src/services/story_arc_service.py

class StoryArc(TypedDict):
    name: str
    icon: str
    start_year: int
    end_year: int  # 0 means "ongoing"
    color: str
    explanation: str
    confidence: float  # 0.0–1.0

def detect_story_arcs(
    stock_id: str,
    financial_data: pd.DataFrame,
    events: list[dict],
    milestones: list[dict],
) -> list[StoryArc]:
    """Auto-detect narrative arcs from data signals.

    Algorithm:
    1. Calculate YoY revenue growth rate per quarter
    2. Identify sustained growth periods (>4 quarters positive) → 成長期
    3. Identify sustained decline (>2 quarters negative) → 挑戰期/衰退期
    4. Detect major strategic events (acquisition, expansion) → 轉型期
    5. Score confidence based on data density and signal clarity

    Returns 1–4 arcs, sorted chronologically.
    """
```

### Risks

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| 1 | **Arc detection accuracy** — If arcs don't match reality, trust is undermined | **High** | Confidence indicator (ties to C204) required. Show "演算法自動偵測" label. Allow arc dismissal. |
| 2 | **False sophistication** — Users may think arcs are expert-labeled | Medium | Always show "自動偵測" label + confidence emoji. Never present as professional analysis. |
| 3 | **📊 emoji conflict with `_section_title()`** (D-005) | Medium | Arc band renders as inline HTML, doesn't use `_section_title()`. Not affected by the confirmed D-005 emoji prefix bug. |
| 4 | **Timeline page text budget** — Arc band + existing content exceeds 200-char limit | Medium | Default timeline to 8 entries (collapsible). Arc band counts as "chart" element, not text. |
| 5 | **Mobile arc band wrapping** — Horizontal bars break on <768px screens | Low-Medium | Fallback: stack arcs as vertical chips (similar to `_render_adaptive_banner` pattern) |
| 6 | **Empty/sparse data** — Companies with <2 years of data get meaningless arcs | Medium | Minimum data threshold: require 8 quarters. If insufficient, hide arc band gracefully. Show "資料不足以判斷故事階段" |
| 7 | **Color confusion with severity badges** — Arcs use same colors as event severity | Low | Different visual context (band vs. card border) prevents confusion. Arc chips are wider and labeled with arc names, not severity text. |
| 8 | **#F39C12 color** — Not in base design system palette per Round 7 audit | Medium | `#F39C12` IS documented as "warning background" in design_system.md section III.3.1. It's in the system. No violation. |

**P1 Issues**: None identified. C202 is a P2 MUST with clean design compliance.

**Effort Validation**: 10–14h estimate is reasonable:
- Service layer (`story_arc_service.py`): 3–4h (algorithm + tests)
- Arc band component (`_arc_band()`): 1–2h (inline HTML, uses existing patterns)
- Integration into `story_timeline.py`: 2–3h (modify page, wire up filtering)
- Mobile responsive fallback: 1–2h
- Testing + edge cases: 2–3h

---

## C199: "Bear vs Bull" Visual Debate Cards

### UX Impact: **High** (confirmed from Round 46)

**Rationale**: C199 is the strongest **differentiator** among the three candidates. No TW stock app presents "both sides" visually. This feature teaches critical thinking — beginners learn that investing involves weighing evidence, not following a single opinion.

**Updated Assessment (Round 47)**:

Round 46 identified the core risk: this feature sits closest to the **advisor boundary**. The design direction must be extremely careful about historian framing. The side-by-side card format is also the hardest to implement responsively in Streamlit.

**Critical UX Debate**: Should both sides always be shown, or should one side have more cards if the evidence strongly favors it? Round 46's spec assumes symmetric 3-vs-3 points. This is a **design risk** — false balance can be misleading. Recommendation: allow asymmetric presentation (e.g., Bear 2 points + Bull 3 points) with a brief explanation ("目前數據顯示看多證據較多").

### Design Direction

**Layout — Zone C Main Area, New "觀點" Tab**:

```
┌─────────────────────────────────────────────────┐
│  这家公司 2330 台積電                             │
│  [名片] [體檢] [財報] [同業] [集團] [觀點] ← NEW │
├─────────────────────────────────────────────────┤
│                                                 │
│  🐻 看空觀點                                      │
│  ┌ border-left: 4px solid #E74C3C ──────────┐  │
│  │                                          │  │
│  │  ⚠️ 毛利率從 56% 降到 52%                │  │
│  │     代表定價能力可能減弱                   │  │
│  │                                          │  │
│  │  📉 資本支出持續高漲                       │  │
│  │     自由現金流被壓縮                       │  │
│  │                                          │  │
│  │  💡 競爭加劇是最大風險                     │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  🐂 看多觀點                                      │
│  ┌ border-left: 4px solid #27AE60 ──────────┐  │
│  │                                          │  │
│  │  ✅ 營收連續 5 季成長超過 15%             │  │
│  │     代表需求穩定增長                       │  │
│  │                                          │  │
│  │  📈 AI 晶片需求推動先進製程營收            │  │
│  │     技術領先優勢難以被超越                  │  │
│  │                                          │  │
│  │  💡 護城河依然穩固                         │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ ⚠️ 這不是投資建議，只是整理兩種觀點。       │  │
│  │    數據來自財報，觀點是根據數據推論。        │  │
│  │    請自行判斷。                             │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Component: New `_debate_card()` helper**:

```python
def _debate_card(
    side: str,           # "bear" or "bull"
    points: list[dict],  # 2-3 points, each: {icon, metric, interpretation}
    evidence_score: int, # 0-100, affects header Emphasis
) -> None:
    """Render a single debate card (bear or bull side).

    Uses design-system colors:
    - Bear: #E74C3C border-left, "🐻 看空觀點" header
    - Bull: #27AE60 border-left, "🐂 看多觀點" header

    Each point: icon (emoji) + metric (bold) + interpretation (plain-language)
    Max 3 points per card. Each point ≤ 50 chars.

    Component follows _info_card() structural pattern.
    """
```

**Design Compliance**:

| Rule | Status | Notes |
|------|--------|-------|
| Zone separation | ✅ | Full Zone C content; tab in Zone A follows existing pattern |
| Color system | ✅ | Bear = `#E74C3C` (red/negative), Bull = `#27AE60` (green/positive) — both in design system |
| Text limits | ✅ | Each card ≤ 140 chars; combined ≤ 280 chars (within PPT limit for content-rich page) |
| PPT style | ⚠️ | This is the most text-heavy planned feature. Must keep points concise. Icon + metric + one-line interpretation per point is the minimum viable format. |
| Ten-second test | ✅ | "有人看好，也有人看壞 — 這是雙方的論點" |
| No advice | ⚠️ (CRITICAL) | Must implement ALL four safeguards: (1) disclaimer card, (2) "自動產生" label, (3) data-driven points only, (4) no specific action language |
| Mobile responsive | ⚠️ | Streamlit columns collapse to stack on mobile. Must use `use_column_width=True` and test stacked layout |

**Interaction Pattern** (progressive disclosure):
1. **Default view**: Both cards visible, 2 points each (most significant)
2. **"查看第三點"**: Expander or button to show 3rd point if available
3. **Point tap**: Popover with full data source (`st.popover` with metric detail) — follows `_explain_button()` pattern
4. **Disclaimer**: Always visible as footer card, not hidden

**Asymmetric Evidence Display**:

```python
def _debate_balance_indicator(bear_score: int, bull_score: int) -> None:
    """Show which side has stronger evidence, without giving advice.

    Renders a subtle bar below the cards:
    ████████░░░░░░░░ 看多證據目前較多

    NOT a recommendation — just a summary of data signals.
    """
```

**Service Layer**:

```python
# Extends: src/services/analogy_service.py or new debate_service.py

def generate_debate_points(
    stock_id: str,
    financial_metrics: dict,
    peer_comparison: dict,
) -> dict:
    """Generate bear and bull points from same data.

    Returns:
        {
            "bear": [{"icon": "⚠️", "metric": "...", "interpretation": "...", "confidence": 0.8}, ...],
            "bull": [{"icon": "✅", "metric": "...", "interpretation": "...", "confidence": 0.9}, ...],
            "evidence_balance": {"bear": 45, "bull": 55},  # not 50/50 if data favors one side
            "disclaimer": "數據來自最近 8 季財報，觀點根據數據推論"
        }
    """
```

### Risks

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| 1 | **Advisor boundary violation** — Bear/bull framing sounds like investment advice | **CRITICAL** | Four safeguards: prominent disclaimer, "自動產生" label, data-driven points only, banned word list (買/賣/推薦/建議/進場/出场) |
| 2 | **False balance** — Presenting 3-vs-3 when evidence is 80/20 | High | Asymmetric display. Show evidence balance indicator. "證據較多" ≠ "應該買/賣" |
| 3 | **Streamlit column collapse on mobile** — Side-by-stack stacking looks bad | Medium | Test stacked layout as fallback. Consider vertical divider instead of side-by-side. |
| 4 | **Data freshness** — If debate points use stale data, quality suffers | Medium | Include data freshness indicator. Don't generate debate if data is >90 days old. |
| 5 | **User misinterpretation of "證據較多"** — Might still read as recommendation | Medium | Add tooltip: "這只是根據財報數據的統計，不是投資建議" on the evidence balance bar. |
| 6 | **Tab naming in Zone A** — "觀點" tab introduces opinion-adjacent language to navbar | Low | Acceptable — tab label is descriptive of page content, not advice. "觀點" = "perspectives on this company" |
| 7 | **D-003 regression** — Custom debate card HTML tempts inline styles | Medium | Must use shared component pattern. Create `_debate_card()` in `_router_base.py`, not inline HTML per page. |

**P1 Issues**: **#1 (Advisor Boundary)** is a P1 issue that must be resolved before development starts. The four-safeguard pattern must be baked into the spec, not added later. Failure mode: user screenshots the debate cards and posts them as "Stock Explorer says buy TSMC" — reputational risk.

**Effort Validation**: 10–14h estimate is reasonable:
- `_debate_card()` component: 2–3h (new shared component in `_router_base.py`)
- `debate_service.py`: 4–5h (algorithm for generating both-sides points from same data)
- Page integration (new tab on company pages): 3–4h
- Mobile testing + responsive fallback: 1–2h
- Disclaimer + safeguards: 1–2h

---

## C200: "What If I Had Invested?" Historical Scenario Calculator

### UX Impact: **High** (confirmed from Round 46)

**Rationale**: C200 has the highest **emotional impact** ("if I had invested $10K in TSMC 5 years ago…"). This is a retention hook — users share these results. However, it's also the riskiest for advisor boundary and requires interactive controls in Zone C.

**Updated Assessment (Round 47)**:

Since Round 46:

1. C201 (Daily Market Story) is being built — it will set the pattern for interactive elements in Zone C
2. The design system now has `_confidence_badge()` and `_read_time()` in `_router_base.py` — C200 should include confidence on its calculated results
3. Round 46's assessment of "High" UX impact stands, but the **risk profile** has increased because this feature generates the most shareable (and therefore most likely to be misrepresented) content

### Design Direction

**Layout — Zone C Interactive Card**:

```
┌─────────────────────────────────────────────────┐
│  这家公司 2330 台積電                             │
│  [名片] [體檢] [財報] [同業] [集團] [觀點] [試算]│ ← NEW TAB
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌─ 互動控制區（頂部，與結果區分隔）──────────┐  │
│  │                                           │  │
│  │  投資日期：[2020-01-01 ▼]                  │  │
│  │  投資金額：[10,000] 元                     │  │
│  │                                           │  │
│  └───────────────────────────────────────────┘  │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│                                                 │
│  ┌─ 結果區 ─────────────────────────────────┐  │
│  │                                          │  │
│  │  如果在 2020-01-01 投入 10,000 元         │  │
│  │                                          │  │
│  │  現在價值                                  │  │
│  │  ┌──────────────┐                         │  │
│  │  │  NT$ 28,450  │ ← font-size:1.6rem     │  │
│  │  │  (+184.5%)   │    font-weight:700     │  │
│  │  └──────────────┘    color:#27AE60        │  │
│  │                                          │  │
│  │  💡 這主要是因為台積電在 AI 浪潮中         │  │
│  │     技術領先，營收大幅成長 🟡              │  │
│  │     ↳ 資料期間 2020–2025，數據完整度 95%  │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ┌─ 走勢圖 ──────────────────────────────────┐  │
│  │  📈                                          │  │
│  │  30K ┤           ╭────╮                     │  │
│  │  25K ┤      ╭───╯    │                     │  │
│  │  20K ┤  ╭──╯         │                     │  │
│  │  15K ┤──╯            │                     │  │
│  │  10K ┤─ ─ ─ ─ ─ ─ ─ ┼ ─ ─ ─ 投入金額     │  │
│  │   5K ┤               │                     │  │
│  │      └──┬──┬──┬──┬──┬─┘                     │  │
│  │       2020  21  22  23  24                  │  │
│  │                                          │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  ⚠️ 歷史報酬不代表未來表現。這只是讓你了解        │
│     這家公司過去的表現。不含股息。                │
│                                                  │
└─────────────────────────────────────────────────┘
```

**Design Compliance**:

| Rule | Status | Notes |
|------|--------|-------|
| Zone separation | ⚠️ | Interactive controls (date picker, amount input) MUST be at top of Zone C, clearly separated from results |
| Color system | ✅ | Gains in `#27AE60` (green), losses in `#E74C3C` (red), result number dominant |
| Text limits | ✅ | Result area: ≤ 100 chars; chart: 0 text (visual only); disclaimer: ≤ 80 chars |
| PPT style | ⚠️ | Interactive page — PPT rules relaxed for controls. But result display is classic PPT: one big number + one explanation |
| Ten-second test | ✅ | "如果當初投資一萬塊，現在會變多少？" |
| No advice | ⚠️ (CRITICAL) | Must NOT suggest "you should have bought" or "you should buy now." Pure historian framing. |
| Mobile responsive | ⚠️ | date_input + number_input in Streamlit columns — must stack on mobile |

**Component Extensions**:

```python
# New in _router_base.py

def _what_if_result_card(
    invest_date: str,
    invest_amount: float,
    current_value: float,
    gain_pct: float,
    is_gain: bool,
    explanation: str,
    confidence_badge: str,
) -> None:
    """Render the 'What If' result display.

    Large number display per typography spec.
    Color: green for gains, red for losses.
    Includes inline confidence badge (ties to C204).
    """
```

**Interaction Rules**:
1. **Date picker**: Default to 5 years ago (not "today" — avoids recency bias)
2. **Amount input**: Default to 10,000 TWD (accessible amount for beginners)
3. **Date range**: Earliest = IPO date or 10 years ago (whichever is closer). Earliest date should be grayed out if data unavailable.
4. **Chart**: Plotly line chart, transparent background, showing portfolio value over time. >60% of result area (per chart proportion rule).
5. **Controls at top**: Date and amount inputs in a `st.container()` with subtle background. Results below a visual separator (`st.markdown("---")`).
6. **Key naming**: `what_if_date_{stock_id}`, `what_if_amount_{stock_id}` per button key convention.

**Data Processing** (service layer):

```python
# New: src/services/what_if_service.py

def calculate_historical_scenario(
    stock_id: str,
    invest_date: str,
    invest_amount: float,
    daily_prices: pd.DataFrame,
) -> dict:
    """Calculate historical investment scenario.

    Returns:
        {
            "invest_date": "2020-01-01",
            "invest_amount": 10000,
            "current_value": 28450,
            "gain_pct": 184.5,
            "is_gain": True,
            "portfolio_values": pd.DataFrame,  # for chart
            "explanation": "這主要是因為...",
            "confidence": 0.95,
            "data_completeness": 0.95,
            "disclaimer": "歷史報酬不代表未來表現..."
        }

    Pure function — no Streamlit imports.
    """
```

### Risks

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| 1 | **Regulatory/tone risk** — "What if" framing implies "you missed out" | **High** | Historian framing: "這只是歷史回顧，不代表未来" MUST be prominent. Tone = curiosity, not FOMO. |
| 2 | **Recency bias** — Users pick dates that show best returns | **Medium** | Default to 5 years ago. Don't allow dates within 30 days (too short-term). |
| 3 | **D-003 regression** — Multiple interactive controls tempt inline HTML | **Medium** | Use `st.date_input()` and `st.number_input()` natively. NO custom HTML for inputs. |
| 4 | **Widget key conflicts** — date_input and number_input need unique keys | **Low** | Follow convention: `what_if_date_{stock_id}`, `what_if_amount_{stock_id}` |
| 5 | **Mobile: controls + chart + results = long scroll** | **Medium** | Acceptable — interactive pages naturally scroll more than PPT pages. Chart should be responsive. |
| 6 | **Dividend handling** — Including dividends crosses into "total return" territory which is more complex and more advice-adjacent | **Low** | Explicitly exclude dividends. Show "不含股息" in disclaimer. This keeps it simple and reduces advisory perception. |
| 7 | **Sharing risk** — User screenshots "NT$28,450" without disclaimer | **Low** | Cannot prevent, but make disclaimer visually part of the result card (not below the fold). Watermark-style subtle text: "歷史回顧，非投資建議" |

**P1 Issues**: **#1 (FOMO framing)** is a design P1 that must be resolved. The feature must NOT use language like "你錯過了" or "早知道就". All copy must maintain historian tone: "回顧過去，這筆投資的價值變化是…"

**Effort Validation**: 12–16h estimate is accurate:
- `what_if_service.py`: 3–4h (calculation logic, edge cases)
- `_what_if_result_card()` component: 2–3h (result display with chart)
- Page integration: 3–4h (tab, controls, wiring)
- Edge cases + testing: 2–3h (missing data, pre-IPO dates, etc.)
- Disclaimer + safeguards: 1–2h
- Mobile testing: 1–2h

---

## Overall Design Recommendations

### Sprint 23 Priority Order

| Priority | Feature | P-Level | Effort | Design Readiness | Recommendation |
|----------|---------|---------|--------|-----------------|----------------|
| 1 | C202 Story Arc Labels | P2 MUST | 10–14h | ✅ High — builds on existing timeline, low design risk | **Proceed** |
| 2 | C199 Bear vs Bull | P2 SHOULD | 10–14h | ⚠️ Medium — advisor boundary risk needs resolution | **Proceed with safeguards** |
| 3 | C200 What If Calculator | P2 COULD | 12–16h | ⚠️ Medium — interactive + FOMO risk needs resolution | **Defer to Sprint 24 or resolve P1 first** |

### Recommended Sprint 23 Scope

**Phase A (Sprint 23)**: Build C202 + C199 together
- Combined effort: 20–28h
- C202 establishes the "narrative timeline" pattern
- C199 adds the "both sides" analytical perspective
- Together they reinforce historian positioning
- **Prerequisite**: Resolve C199's P1 advisor boundary issue before coding

**Phase B (Sprint 24)**: Build C200
- C200 is higher risk and should follow after C201 (Daily Market Story) patterns are established
- Lessons from C201's interactive controls in Zone C will inform C200's implementation
- By Sprint 24, C204 (Confidence Indicator) may be available to include in C200 results

### Design System Impact

**New components needed for Sprint 23**:

| Component | Location | Reusability | Color Impact |
|-----------|----------|-------------|--------------|
| `_arc_band()` | `_router_base.py` | High — any timeline page | None — reuses existing colors |
| `_debate_card()` | `_router_base.py` | High — any comparison page | None — reuses existing colors |
| `_debate_balance_indicator()` | `_router_base.py` | Medium — debate features | None — uses existing green/red |
| `_story_arc_service.py` | `src/services/` | Medium — timeline pages | N/A |
| `_debate_service.py` | `src/services/` | Medium — comparison pages | N/A |

**Zero new colors** introduced. Zero new gradients. All components follow existing `_info_card()` / `_summary_card()` structural patterns. Sprint 23 is design-system clean.

### Cross-Feature Interactions

| Interaction | Description | Design Implication |
|-------------|-------------|-------------------|
| C202 ↔ C199 | Story arcs inform debate context | C199 could include arc context: "在目前的挑戰期，看空論點包括…" |
| C202 ↔ C204 | Arc confidence scores | C204 confidence badges should appear on arc band (🟢🟡🔴) |
| C199 ↔ C204 | Debate point confidence | Each debate point can have confidence indicator |
| C200 ↔ C204 | Calculator result confidence | Result card should include confidence badge |

**Recommendation**: Even if C204 is not yet built, the service layer interfaces for C202 and C199 should include `confidence` fields so C204 integration is zero-effort when available.

### Design Risks Summary (P1 Issues)

| # | Feature | Risk | Severity | Status |
|---|---------|------|----------|--------|
| 1 | C199 | Advisor boundary — debate framing sounds like recommendation | **P1** | Must resolve before development. Four-safeguard pattern. |
| 2 | C200 | FOMO framing — "what if" sounds like "you missed out" | **P1** | Must resolve before development. Historian tone enforcement. |

**Both P1 issues are resolvable through copy/design — neither requires architectural changes.**

### Pre-Development Checklist for Sprint 23

Before writing any code for C202 or C199:

- [ ] C199: Finalize banned word list for debate point generation (買/賣/推薦/建議/進場/出场)
- [ ] C199: Design disclaimer card copy and placement (footer, always visible)
- [ ] C199: Define evidence balance algorithm (how to weight bear vs bull points)
- [ ] C202: Define arc detection algorithm thresholds (min quarters, growth rate thresholds)
- [ ] C202: Define minimum data threshold for arc display (8 quarters recommended)
- [ ] C202: Design arc dismissal interaction (how users hide incorrect arcs)
- [ ] Both: Verify mobile responsive fallback layouts in Streamlit
- [ ] Both: Confirm service layer interfaces include `confidence` field for C204 future integration
- [ ] Both: Verify zero new colors, zero new gradients, zero inline HTML outside shared components

---

*Design Review completed: 2026-06-15*
*Next review: Round 48 (after Sprint 23 development or Sprint 22 completion)*
