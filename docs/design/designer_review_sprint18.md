# Design Review: Sprint 18 Features (C139, C141, C143)

> **Reviewer**: Design Reviewer
> **Date**: 2026-06-14
> **Scope**: C139 (Explain This Number), C141 (Source Badge), C143 (Implication Sentence on Delta Cards)

---

## 1. Product Vision Alignment

Stock Explorer's vision is **"Historian, not a stock picker"** — explain what happened, not what to buy. Three core design principles govern all features:

1. **PPT-style presentation**: one key point per page, images lead text supports
2. **Ten-second test**: a beginner can restate the core concept within 10 seconds
3. **Historian tone QA gate**: factual past-tense only, no investment advice words

All three Sprint 18 features are **strongly aligned** with this vision. They deepen the educational layer without crossing into advisory territory. None of them recommend buying or selling. All three explain *what happened* in plain language.

---

## 2. Feature-by-Feature Evaluation

### 2.1 C139: "Explain This Number" One-Click Metric Explainer

**UX Impact: HIGH — This is the most impactful feature in the sprint.**

Currently, 15+ metrics are displayed across pages with zero explanation UI. A beginner seeing "ROE: 25%" or "P/E: 18x" has no idea what it means. This is the single biggest gap between data display and genuine understanding.

**Design Direction:**

| Aspect | Recommendation |
|--------|---------------|
| **Trigger** | Small `💡` icon button rendered inline after each metric value, using `st.button("💡", key="explain_{metric_id}")`. |
| **Display** | Use `st.popover()` (Streamlit native) — not a modal, not an expander. A popover keeps context visible and doesn't disrupt page flow. |
| **Content** | The popover body shows: (1) metric name in plain language, (2) what this specific value means, (3) the analogy/白话 explanation from `TemplateExplanationProvider`. |
| **Component** | Reuse `_info_card()` INSIDE the popover if the explanation is long (>1 line), or plain `st.markdown()` for short explanations. Do NOT create a new component — Streamlit popovers accept markdown but not raw HTML, so keep content simple. |
| **Placement** | Wire to all metric display locations: business card page metrics, financial condition section, peer comparison deltas. Prioritize the business card page first (highest traffic). |

**Ten-second test**: PASS. Clicking 💡 on "ROE 25%" shows "每100元股東資金，這家公司賺25元" — restatable in 3 seconds.

**Design risks:**
- ⚠️ **Icon clutter**: 15+ 💡 buttons on a page could look noisy. **Mitigation**: Use a subtle, smaller button style (`font-size: 0.8rem`, no border, light gray). Only show 💡 on metrics above a complexity threshold (skip trivial ones like stock code or date).
- ⚠️ **Popover width**: Streamlit popovers have limited width. Keep explanation text under 80 characters per line.
- ⚠️ **No inline HTML in popover**: Streamlit popovers do not support `unsafe_allow_html`. All content must be pure markdown. This is fine — the existing templates are text-only.

---

### 2.2 C141: Confidence/Source Badge on Explanations

**UX Impact: MEDIUM — Trust-building, low visual weight.**

Competitor research (Round 8, Round 12) confirms: Public.com, eToro, and Webull all badge their data sources. Robinhood's "Market Data Explanations" and Metric Tooltips include source attribution. Users trust explanations more when they know where the data comes from.

**Design Direction:**

| Aspect | Recommendation |
|--------|---------------|
| **Badge text** | Two variants: `📊 系統估算` (system estimate / template-generated) and `📊 FinMind` (data-sourced). Use ONLY these two. |
| **Badge placement** | Render as a small `st.caption()` or inline `st.markdown()` badge at the bottom-left of each explanation popover (C139) and each delta card explanation (C143). Font size: 0.7rem, color: `#95A5A6`. |
| **Component** | No new component. Add as a parameter to existing flow: `_info_card()` and popover content get an optional `source` string param. If `source` is non-empty, append the badge at the bottom. |
| **Scope** | Badge ALL explanations uniformly — both C139 popovers and C143 delta card explanations. Consistency matters more than selective display. |

**Ten-second test**: PASS (neutral). The badge is a trust signal, not core content. It does not affect concept restatement.

**Design risks:**
- ⚠️ **Badge fatigue**: If every metric has a tiny badge, the page feels annotated. **Mitigation**: Use the lightest possible visual weight — small gray text, not a colored chip/badge element.
- ⚠️ **Source accuracy**: `TemplateExplanationProvider` templates are system-generated, not directly from FinMind. The badge must match: template explanations → `📊 系統估算`, data-backed statements → `📊 FinMind`. Do NOT badge LLM-generated content as `📊 FinMind` — this would be a factual error.

---

### 2.3 C143: Implication Sentence on Delta Cards

**UX Impact: HIGH — Transforms data into narrative, the core of "historian" positioning.**

Currently, delta cards show metric changes (revenue up 15%, margin down 3%) but leave the user asking "so what?". The implication sentence answers this naturally: "如果你正在觀察這家公司，[ factual observation]". This is exactly what Public.com and Koyfin do — take the "so what" question off the user's plate.

**Design Direction:**

| Aspect | Recommendation |
|--------|---------------|
| **Sentence placement** | Render as a `_白话_card()` or `_summary_card()` BELOW the delta metric, above any detailed breakdown. It should be the narrative bridge between "here's what changed" and "here's the detail". |
| **Tone** | STRICT historian: past tense, factual, no modal verbs. ✅ "如果你正在觀察這家公司，過去3個月營收成長15%，是近一年最快的增速。" ❌ "如果你正在觀察這家公司，應該留意營收加速的訊號。" |
| **Component** | Reuse `_白话_card()` with `label="觀察重點"`, `value=""` (empty), `analogy=<implication_sentence>`. The analogy field is the right slot for this narrative content — it already uses green italic styling that visually distinguishes it from data. |
| **Implementation** | `DeltaExplanationProvider` already exists (Sprint 17, C134). The implication sentence should be a NEW field on `ExplanationResponse` (e.g., `implication: str`) and a new template output from `DeltaExplanationProvider`. NOT a new provider — extend the existing one. |
| **QA gate** | Run every generated sentence through a blocklist check: 建議, 應該, 買, 賣, 推薦, 進場, 出場, 風險 (when used as advice). Automated test required before merge. |

**Ten-second test**: PASS. "過去3個月營收成長15%，是近一年最快的增速" — immediately restatable, gives the user the "so what" in one sentence.

**Design risks:**
- ⚠️ **Tone violation (CRITICAL)**: The `DeltaExplanationProvider` currently generates analysis-flavored text ("表現優於預期", "可能是需求回溫"). Adding implication sentences increases the risk of crossing into advisory language. **Hard gate**: the blocklist QA check must be automated in CI, not manual review.
- ⚠️ **Generic implications**: The `TemplateExplanationProvider` has a known issue (D-097, from tech debt review) — its templates are stock-agnostic ("可能是需求回溫"). Implication sentences that say "可能是需求回溫" without stock-specific context feel hollow. **Mitigation**: The `ExplanationRequest.context` field exists but is unused in `TemplateExplanationProvider`. Before C139/C143, D-097 (enhance templates with `request.context`) should be addressed — at least for industry context.
- ⚠️ **Length**: Implication sentences should be ONE sentence, max 50 Chinese characters. Longer = advice territory.
- ⚠️ **Card overload**: If a delta card already has: metric → value → delta badge → explanation text, adding an implication sentence makes it 4 elements. This approaches the complexity limit. **Mitigation**: If the explanation text already implies the observation, skip the implication sentence. The sentence should ADD information, not restate.

---

## 3. Cross-Feature Interaction Map

```
┌─────────────────────────────────────────────────────────┐
│                    Delta Card (existing)                  │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ Metric: 月營收      Value: 380億     Delta: +15%    │ │
│  │                                                       │ │
│  │ 💡 [C139 button] → popover with explanation           │ │
│  │                                                       │ │
│  │ "💰 這3個月賺380億，比去年多15%..."                   │ │
│  │             的小型成長"                               │ │
│  │                                                       │ │
│  │ [C143 implication sentence]                           │ │
│  │ "如果你正在觀察這家公司，營收增速是近一年最快..."     │ │
│  │                                                       │ │
│  │ 📊 系統估算                              [C141 badge]  │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

All three features work together on the same delta card: the 💡 button explains the metric, the implication sentence provides narrative context, and the source badge builds trust. This is a coherent progressive-disclosure pattern: data → narrative → trust signal.

---

## 4. Priority & Sequencing Recommendation

| Priority | Feature | Rationale |
|----------|---------|-----------|
| **P0** | C139 (Explain This Number) | Highest UX impact. Unlocks understanding for 15+ currently unexplained metrics. Directly addresses the core pain point: "information overload but insufficient understanding". |
| **P1** | C143 (Implication Sentence) | High UX impact but depends on C139 being in place for the popover context, AND on the tone QA gate being automated. Slightly higher risk due to tone violation potential. |
| **P2** | C141 (Source Badge) | Important trust signal but zero impact on understanding. Can be added incrementally. Lowest risk. |

**Suggested implementation order**: C139 → C143 → C141

This sequence lets you:
1. Build and validate the popover + explanation pattern first
2. Add implication sentences with tone gates in place
3. Add badges as a final polish pass (every explanation gets a badge at once)

---

## 5. Scope Adjustments Recommended

1. **Merge C141 into C139 and C143 implementation** — don't implement badges as a separate task. Add the `source` parameter to `ExplanationResponse` and render badges wherever explanations appear. This avoids a 3-4h standalone task for what is a trivial UI addition.

2. **Address D-097 (generic templates) BEFORE C143** — The `TemplateExplanationProvider` templates are stock-agnostic. Implication sentences that say "可能是需求回溫" without industry context undermine credibility. The `ExplanationRequest.context` field exists — use it. Estimated effort: 2-3h to thread industry context through.

3. **Automate tone QA in CI before C143 merge** — Add a test file `tests/test_tone_qa.py` that runs all generated explanations through the blocklist (建議/應該/買/賣/推薦/進場/出場). This is a prerequisite for C143, not a follow-up.

4. **Limit C139 scope to business card page only for Sprint 18** — 15+ metrics across all pages is too much for one sprint. Wire C139 to the business card page metrics first (5-7 metrics). Roll out to deep-dive sections in Sprint 19.

---

## 6. Design Verdict

| Feature | Vision Alignment | Ten-Second Test | Historian Tone | Risk | Score |
|---------|-----------------|-----------------|---------------|------|-------|
| C139 | ✅ Strong | ✅ Pass | ✅ Safe | Low (clutter) | **9/10** |
| C141 | ✅ Strong | ✅ Neutral | ✅ Safe | Minimal | **7/10** |
| C143 | ✅ Strong | ✅ Pass | ⚠️ Needs gate | Medium (tone) | **8/10** |

**Overall: APPROVE with conditions.**

- C139: Approved as-is.
- C141: Approved, merged into C139/C143 tasks.
- C143: Approved with prerequisite — automated tone QA + D-097 context fix must ship in the same sprint.

---

*Design Reviewer, Sprint 18 — 2026-06-14*
