# Handoff – Discussion Round 48

## Summary
- **Topic**: 💡 Discussion (Round 48 — 2026-06-17)
- **Participants**: Product Manager, System Architect, Challenger
- **Sprint Status**: Sprint 22 (C201) in progress → Sprint 23 planning
- **Challenger Verdict**: ⚠️ CONDITIONAL ALIGNED — 5 blocking questions resolved, 4 recommendations accepted

---

## Sprint 23 Final Plan (Post-Challenge, Round 48)

| Priority | Feature | Effort | Risk | Go/No-Go Gate |
|----------|---------|--------|------|----------------|
| MUST | C202 Story Arc Labels | 11-18h | Low | i18n wrapping complete + quality check on 3 test stocks |
| SHOULD | C199 Bear vs Bull Debate Cards | 14-22h | Medium | Tone QA gate — 2 revision max, then defer |
| COULD | C200 What If Calculator | 12-17h (+2-3h gate) | Medium-High | Week 1: FinMind API caching + historian framing + data completeness |
| **Total** | | **37-57h (+2-3h gate)** | | |

### Implementation Order
1. **Pre-Sprint** (before Day 1): Resolve locale conflict, delete `src/core/locales/`, add i18n keys
2. **Week 1**: C202 (Story Arc) — i18n wrapping + quality check on TSMC/鴻海/緯穎
3. **Week 1-2**: C199 (Debate Cards) — only after four-safeguard pattern is designed
4. **Week 2-3**: C200 (What If Calculator) — only if Week 1 gate passes AND C202+C199 < 30h

---

## 5 Blocking Questions — RESOLVED

| # | Question | Resolution |
|---|----------|------------|
| Q1 | Which locale directory is canonical? | **Keep `locales/`** (project root). Delete `src/core/locales/`. All existing `t()` calls reference this schema. |
| Q2 | How will `story_arc_detector.py` output be i18n-wrapped? | **Service returns keys, page calls `t()`**. Refactor `story_arc_detector.py` to return arc type keys (`growth`, `decline`, `volatile`, `recovery`) instead of Chinese text. Page-level code wraps with `t()`. |
| Q3 | Is `story_arcs.yaml` config or display text? | **Config only**. Move display strings (label, description) into locale YAML files. Keep only thresholds/color in `story_arcs.yaml`. |
| Q4 | Is the four-safeguard pattern designed? | **Pre-sprint dependency for C199**. PM + Designer must define the four-safeguard pattern before C199 service development begins. C199 cannot start without this. |
| Q5 | Has `get_daily_price()` been tested with 5Y date ranges? | **Week 1 gate criterion**. Must verify data completeness (no gaps > 5 trading days) for TSMC before C200 implementation begins. |

---

## 4 Recommendations — ACCEPTED

| # | Recommendation | Status |
|---|---------------|--------|
| R1 | Delete `src/core/locales/` immediately | ✅ ACCEPTED — Pre-sprint cleanup |
| R2 | Set explicit C200 deferral criteria | ✅ ACCEPTED — "If C202 + C199 > 30h, C200 auto-deferred to Sprint 24" |
| R3 | Add +2-3h for Week 1 gate work | ✅ ACCEPTED — Included in total estimate |
| R4 | Standardize i18n approach for service-layer modules | ✅ ACCEPTED — Services return keys, pages call `t()` |

---

## i18n Conflict Resolution

### Decision: `locales/` is canonical

**Action items:**
1. Delete `src/core/locales/` directory (dead code, incompatible schema)
2. Add Sprint 23 i18n keys to both `locales/zh-TW.yaml` and `locales/en.yaml`:
   - `story_arc.*` — arc labels, descriptions, legend
   - `debate.*` — debate card labels, disclaimers
   - `scenario.*` — calculator labels, disclaimers
3. Refactor `story_arc_detector.py` to return keys instead of Chinese text
4. Wrap all `story_timeline.py` UI strings with `t()` calls

### i18n Key Schema for Sprint 23

```yaml
# locales/zh-TW.yaml and locales/en.yaml
story_arc:
  growth: "成長期" / "Growth Phase"
  decline: "調整期" / "Decline Phase"
  volatile: "震盪期" / "Volatile Phase"
  recovery: "復甦期" / "Recovery Phase"
  growth_desc: "過去6個月營收與市場評價偏向正面..." / "Past 6 months showed positive revenue and market sentiment..."
  decline_desc: "過去6個月面臨較多負面事件..." / "Past 6 months faced more negative events..."
  volatile_desc: "過去6個月正負事件交織..." / "Past 6 months had mixed positive and negative events..."
  recovery_desc: "調整後出現正面訊號..." / "Positive signals emerged after adjustment..."
  legend_title: "故事弧線圖例" / "Story Arc Legend"
  section_title: "故事弧線" / "Story Arcs"
  section_desc: "自動偵測公司故事的主要階段..." / "Auto-detected narrative arcs..."
  period_label: "此區間共 {count} 個事件" / "{count} events in this period"

debate:
  title: "多方 vs 空方" / "Bull vs Bear"
  bull_case: "多方論點" / "Bull Case"
  bear_case: "空方論點" / "Bear Case"
  evidence_balance: "證據平衡" / "Evidence Balance"
  more_bull: "多方證據較多" / "More Bull Evidence"
  more_bear: "空方證據較多" / "More Bear Evidence"
  balanced: "雙方證據相當" / "Balanced"
  disclaimer: "以上論點由系統自動整理..." / "Arguments are auto-generated..."
  auto_generated_label: "自動產生" / "Auto-Generated"

scenario:
  title: "如果當時投資了？" / "What If I Had Invested?"
  input_label: "投資日期" / "Investment Date"
  amount_label: "投資金額" / "Investment Amount"
  result_label: "至今價值" / "Value Today"
  return_label: "報酬率" / "Return"
  dividend_label: "含股息" / "Incl. Dividends"
  disclaimer: "⚠️ 歷史情境為假設性試算..." / "⚠️ Historical scenarios are hypothetical..."
  no_data: "無法取得該日期的資料" / "No data available for selected date"
  before_ipos: "所選日期早於公司上市日期" / "Selected date is before IPO date"
  featured_scenarios: "精選情境" / "Featured Scenarios"
  custom_scenario: "自訂情境" / "Custom Scenario"
```

---

## Feature-by-Feature Final Assessment

### C202 — Story Arc Labels (MUST) ✅ PROCEED
- **Status**: Service layer complete (211 lines), tests complete (327 lines), integration in progress
- **Remaining work**: i18n wrapping in `story_timeline.py` (15+ strings), refactor `story_arc_detector.py` to return keys
- **Effort**: 11-18h (includes i18n work)
- **Risk**: Low
- **Gate**: Quality check on TSMC (2330), 鴻海 (2317), 緯穎 (6669) with 1Y/3Y/5Y lookback + all strings i18n-wrapped

### C199 — Bear vs Bull Debate Cards (SHOULD) ✅ PROCEED (CONDITIONAL)
- **Status**: Full greenfield — no service, no templates, no page
- **Pre-sprint dependency**: Four-safeguard pattern must be designed by PM + Designer before development
- **Files to create**: `debate_engine.py` (~150-200 lines), `debate_templates.yaml` (~100-150 lines), `debate_cards.py` (~200-250 lines)
- **Effort**: 14-22h (includes four-safeguard pattern + Tone QA)
- **Risk**: Medium
- **Gate**: Tone QA review — 2 revision max, then defer to Sprint 24

### C200 — What If Calculator (COULD) ✅ PROCEED (WEEK 1 GATE)
- **Status**: C74 foundation exists (320 lines), but calculator logic is greenfield
- **Week 1 gate criteria**:
  1. FinMind API caching validated
  2. Data completeness verified (5Y daily data for TSMC, no gaps > 5 trading days)
  3. Historian framing passes tone QA (no FOMO language)
- **Deferral criteria**: If C202 + C199 combined exceed 30h, C200 auto-deferred to Sprint 24
- **Effort**: 12-17h (+2-3h gate work)
- **Risk**: Medium-High
- **Gate**: Week 1 go/no-go

---

## Sprint 24 (Provisional)
- C200 (if deferred from Sprint 23)
- C201 follow-ups (daily caching pipeline)
- C206 Recurring Investment Education (pending regulatory review)
- C203 Supply Chain Visual Map
- C209 Source Transparency Layer (pending Round 49 evaluation)

---

## Action Items

| Item ID | Description | Owner | Sprint | Status |
|---------|-------------|-------|--------|--------|
| A48-01 | Delete `src/core/locales/` directory | Developer | Pre-Sprint 23 | ⏳ Pending |
| A48-02 | Add Sprint 23 i18n keys to `locales/zh-TW.yaml` and `locales/en.yaml` | Developer | Pre-Sprint 23 | ⏳ Pending |
| A48-03 | Refactor `story_arc_detector.py` to return keys instead of Chinese text | Developer | Sprint 23 | ⏳ Pending |
| A48-04 | Wrap all `story_timeline.py` UI strings with `t()` calls | Developer | Sprint 23 | ⏳ Pending |
| A48-05 | Move display strings from `story_arcs.yaml` to locale files | Developer | Sprint 23 | ⏳ Pending |
| A48-06 | Design four-safeguard advisor boundary pattern for C199 | PM + Designer | Pre-C199 | ⏳ Pending |
| A48-07 | Create `debate_engine.py` service module | Developer | Sprint 23 | ⏳ Pending |
| A48-08 | Create `debate_templates.yaml` content templates | Developer + PM | Sprint 23 | ⏳ Pending |
| A48-09 | Create `debate_cards.py` page renderer | Developer | Sprint 23 | ⏳ Pending |
| A48-10 | Create `scenario_calculator.py` service module | Developer | Sprint 23 | ⏳ Pending |
| A48-11 | Validate FinMind API data completeness (5Y daily data) | Developer | Sprint 23 Week 1 | ⏳ Pending |
| A48-12 | Evaluate C209 and C210 in Round 49 Discussion | PM + QA | Round 49 | ⏳ Pending |

---

## Key Architectural Decisions (Updated)

1. **`locales/` is canonical** — `src/core/locales/` deleted as dead code
2. **Services return keys, pages call `t()`** — standard i18n pattern for all service-layer modules
3. **`story_arcs.yaml` is config only** — display strings moved to locale files
4. **C202 arc labels stay in `story_timeline.py`** — no separate page needed
5. **C199 is a new page** (`debate_cards.py`) — standalone feature with Tone QA gate
6. **C200 extends C74** — add "Custom Scenario" expander, don't replace curated content
7. **C200 deferral criteria: C202 + C199 > 30h → auto-defer** — explicit numeric threshold
8. **No LLM dependency for any Sprint 23 feature** — all rules-based

---

## Documentation Created
- `docs/architecture/discuss_r48_architect.md` — Full architecture analysis
- `docs/state/challenge_r48.md` — 3-round challenge with 9 questions
- `docs/state/handoff_discuss_r48.md` — This document

---

*Created: 2026-06-17 by PM*
*Source: docs/architecture/discuss_r48_architect.md, docs/state/challenge_r48.md, docs/state/handoff_discuss_r47.md*
