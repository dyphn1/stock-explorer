# 2026-06-13 Design Review — Discussion Round 18

**Author**: Design Reviewer
**Role**: UX impact analysis for Sprint 9 candidate features
**Scope**: C98 (Event Interpretation Engine), C101 (Comprehension Check Quiz), C103 (First Visit Guide)
**Current Design Grade**: A- (downgraded from A — inline HTML enforcement gap)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [UX Impact Assessment](#ux-impact-assessment)
3. [Design Direction for C98](#design-direction-c98)
4. [Design Direction for C101](#design-direction-c101)
5. [Design Direction for C103](#design-direction-c103)
6. [Design Risks](#design-risks)
7. [Challenger Response Preparation](#challenger-response-preparation)
8. [Recommendation](#recommendation)

---

## Executive Summary

Sprint 8 cleared all 7 debt items, unlocking Sprint 9 for feature work. Three candidate features are on the table: C98 (Event Interpretation Engine, P1, 14-18h, CONDITIONAL), C101 (Comprehension Check Quiz, P2, 8-12h, CONFIRMED), and C103 (First Visit Guide, P2, 10-14h, CONDITIONAL). This review evaluates each feature's UX impact against the design system (PPT-style, ten-second test, beginner-friendly, historian-not-stock-picker) and the product vision (education over trading, story-first, plain-language).

**Overall UX verdict**: All three features are strongly aligned with the product vision. C98 and C101 together form a cohesive "educational feedback loop" (interpret → verify). C103 addresses the most critical UX gap for new users. The primary design risk is not *whether* to build these features but *how* to implement them without compounding the existing inline HTML enforcement gap (D-003) and without violating PPT-style text limits.

---

## UX Impact Assessment

### Current UX State (Post-Sprint 8)

| Dimension | State | Impact on Sprint 9 |
|-----------|-------|-------------------|
| **Zone A/B/C Compliance** | A — all pages properly separated | C103 must not inject onboarding content into Zone A (navbar). Zone C only. |
| **PPT-Style Adherence** | A- — text volume growing | C98 interpretations must be ≤2 sentences (design system rule). C101 questions must be ≤15 characters per tagline. C103 primer must be ≤200 chars total. |
| **Card Component Consistency** | B+ — D3 partially effective | All three features will introduce new card types. Must use shared components from `_router_base.py` or create new documented variants. |
| **Color System** | A — correct palette usage | C98 severity interpretations must use existing colors only (red/green/blue). C103 primer cards must use `#F8F9FA` background + `#3498DB` border. |
| **Plain-Language System** | A — historian tone consistent | C98 is the highest plain-language risk: interpretations must explain "why it matters" without crossing into "what to do about it." |
| **Ten-Second Test** | A — core concept clear | C103 directly strengthens this for first-time users. C98 strengthens it for event dashboard users. |
| **Mobile Responsiveness** | B- — D-006 unresolved | C103 primer must stack vertically on mobile. C98 interpretation text must not overflow on narrow screens. |

### Feature UX Impact Matrix

| Feature | Ten-Second Test | PPT-Style | Beginner-Friendly | Historian Tone | Overall UX Impact |
|---------|----------------|-----------|-------------------|----------------|-------------------|
| **C98** | ✅ Strengthens — events become immediately understandable | ⚠️ Risk — interpretations add text volume | ✅ Strengthens — plain-language "why it matters" | ⚠️ Risk — interpretation can drift toward advice | **HIGH POSITIVE** |
| **C101** | ✅ Strengthens — verifies understanding | ✅ Strengthens — interactive element breaks up text | ✅ Strengthens — gamified learning | ✅ Strengthens — quiz on facts, not opinions | **HIGH POSITIVE** |
| **C103** | ✅ Strengthens — orients first-time users | ✅ Strengthens — one key point per primer card | ✅ Strengthens — reduces initial overwhelm | ✅ Strengthens — sets historian expectation | **HIGH POSITIVE** |

### Cumulative UX Impact

If all three features are implemented well, the cumulative UX impact is **transformative**:

1. **New user journey**: C103 orients → user reads content → C98 explains events → C101 verifies understanding
2. **Engagement loop**: C101 quiz results → weak areas identified → C98 interpretations provide deeper context → user returns
3. **Retention**: C103 reduces bounce rate for first-time users. C101 increases return rate through gamified learning.

**However**, if implemented poorly, the cumulative UX impact is **negative**:
1. C103 primer adds friction to every first visit → user annoyance
2. C98 interpretations add text volume → PPT-style violation
3. C101 quiz feels disconnected from content → C52 déjà vu (the cancelled feature)

---

## Design Direction C98

### Feature Summary
C98 adds plain-language interpretation to detected events. Currently, events show *what* happened (title + summary). C98 adds *why it matters* in educational terms.

### UX Design Direction

#### 1. Interpretation Card Component

**New component needed**: `_interpretation_card()` in `_router_base.py`

```html
<!-- Event interpretation card -->
<div style="background:#FEF9E7;border-radius:12px;padding:1.2rem;border-left:4px solid #F39C12;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">💡 為什麼這很重要？</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.6;">{interpretation}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{historian_note}</div>
</div>
```

**Design rationale**:
- Uses **orange border** (`#F39C12`) to distinguish from info cards (blue) and tip cards (orange background). This is a new "interpretation" variant.
- Uses **warning background** (`#FEF9E7`) to signal "this needs attention" without being alarming.
- The "為什麼這很重要？" header is consistent across all event types — users learn to look for this pattern.
- The historian note (green italic) provides the "historian, not stock picker" guardrail.

**⚠️ Design system gap**: `#F39C12` (orange) is NOT in the current design system palette. The design system only specifies red, green, blue, and neutral colors. **Recommendation**: Either (a) add orange as a "warning/interpretation" color to the design system, or (b) use `#3498DB` (blue) border with `#EBF5FB` (light blue) background to stay within the existing palette. **Option B is preferred** to avoid palette expansion.

**Revised design (palette-compliant)**:
```html
<div style="background:#EBF5FB;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">💡 為什麼這很重要？</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.6;">{interpretation}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">{historian_note}</div>
</div>
```

#### 2. Placement in Event Dashboard

**Current event display** (event_dashboard.py):
```
[severity badge] [type badge] [title]
[summary text]
```

**With C98**:
```
[severity badge] [type badge] [title]
[summary text]
┌─────────────────────────────────────────┐
│ 💡 為什麼這很重要？                        │
│ [interpretation — 2 sentences max]       │
│ [historian note — 1 sentence]            │
└─────────────────────────────────────────┘
```

**Design rules**:
- Interpretation appears **below** the summary, separated by `st.markdown("---")`
- Interpretation is **always visible** (not in an expander) — it's the core value of C98
- Total added text: ≤3 sentences (interpretation + historian note)
- Must not exceed the 200-char text limit per page section (Design System V.5.2)

#### 3. Interpretation Content Rules

**Historian tone guardrails** (critical for C98):
- ✅ "營收大幅成長，代表公司產品需求增加，但需觀察是否能持續"
- ✅ "股價異常波動，可能反映市場對公司前景的看法變化"
- ❌ "營收大幅成長，建議買進" (buy/sell advice — violates historian positioning)
- ❌ "股價異常波動，可能是買進機會" (investment framing — violates historian positioning)
- ❌ "這表示公司前景看好" (forward-looking opinion — violates historian positioning)

**Template structure**:
```
[What happened in context] + [What this type of event typically means historically] + [Historian caveat]
```

**Example for revenue_surge (high severity)**:
```
最近月營收較去年同期成長 30%，幅度顯著。
過去類似情況通常反映產品需求擴張或新客戶增加。
歷史顯示營收成長不一定持續，需觀察後續數月數據。
```

#### 4. Interaction Pattern

**Dashboard view** (all events visible):
- Template-based interpretation (fast, no latency)
- All events show interpretation immediately
- No user interaction required

**Individual event drill-down** (optional LLM enhancement):
- Click event → expander opens with LLM-generated deeper interpretation
- Lazy-loaded (one at a time, on click)
- Loading spinner during LLM call (2-5s)
- Fallback: "暫時無法產生更詳細的解釋，請稍後再試"

**Design note**: The LLM drill-down is a **Phase 2** enhancement. Phase 1 should ship with template-only interpretations. This reduces risk and keeps the UX responsive.

#### 5. Ten-Second Test for C98

**Test**: Show a user an event with interpretation. Ask: "What happened and why does it matter?"

**Pass criteria**: User can restate both the event AND its significance in ≤10 seconds.

**Design implication**: If the interpretation is too long or complex, the ten-second test fails. Keep interpretations to 2 simple sentences.

---

## Design Direction C101

### Feature Summary
C101 adds contextual quiz questions after content sections. Replaces cancelled C52 (standalone quiz mode). Questions are multiple-choice with adaptive feedback.

### UX Design Direction

#### 1. Quiz Card Component

**New component needed**: `_quiz_card()` in `_router_base.py`

```html
<!-- Quiz question card -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">🧠 小測驗</div>
    <div style="font-size:0.95rem;color:#2C3E50;margin-top:0.5rem;">{question}</div>
    <div style="margin-top:0.5rem;">
        <!-- Options rendered as st.button per option -->
    </div>
</div>
```

**Design rationale**:
- Uses standard info card styling (blue border, gray background) — consistent with existing cards
- "🧠 小測驗" header is consistent across all sections
- Options are rendered as `st.button` (not radio buttons) — more touch-friendly, clearer interaction
- After answering, the card transforms to show feedback (see below)

#### 2. Quiz Interaction Flow

```
[User reads content section]
    ↓
[🧠 小測驗 button appears below section]
    ↓
[User clicks → quiz card expands]
    ↓
[User selects answer]
    ↓
[Immediate feedback: ✅ Correct / ❌ Incorrect]
    ↓
[Explanation: 1-2 sentences explaining WHY]
    ↓
[Session state records result]
```

**Feedback design**:
```html
<!-- Correct answer feedback -->
<div style="background:#EAFAF1;border-radius:8px;padding:0.8rem;margin-top:0.5rem;border-left:4px solid #27AE60;">
    <div style="font-weight:600;color:#27AE60;">✅ 答對了！</div>
    <div style="font-size:0.85rem;color:#5D6D7E;margin-top:0.3rem;">{explanation}</div>
</div>

<!-- Incorrect answer feedback -->
<div style="background:#FDEDEC;border-radius:8px;padding:0.8rem;margin-top:0.5rem;border-left:4px solid #E74C3C;">
    <div style="font-weight:600;color:#E74C3C;">❌ 再想想看</div>
    <div style="font-size:0.85rem;color:#5D6D7E;margin-top:0.3rem;">{explanation}</div>
    <div style="font-size:0.85rem;color:#27AE60;font-style:italic;margin-top:0.3rem;">💡 {hint}</div>
</div>
```

#### 3. Placement in Content Sections

**Design rule**: Quiz button appears at the **bottom** of each content section, separated by `st.markdown("---")`.

**Current section structure**:
```
[Section title]
[Content cards/charts]
[--- separator]
[🧠 小測驗 button]  ← NEW
```

**Important**: The quiz button must NOT be visible by default. It should appear only after the user has scrolled through the section content. This prevents the quiz from being the first thing users see (which would violate the "content first" principle).

**Implementation note**: In Streamlit, true scroll detection isn't possible. The practical solution is to place the quiz at the bottom of each section, after all content. Users who scroll to the bottom have likely read the content.

#### 4. Content Scope (Critical Design Decision)

**Risk**: Writing quiz questions is a PM/designer task, not a dev task. The 8-12h dev estimate assumes content is provided.

**Recommended scope for Sprint 9**:
- **5-8 questions total** (not per section)
- Cover the most important financial concepts: ROE, 毛利率, 本益比, 殖利率, 負債比
- Questions are **reusable across all stock pages** (generic, not stock-specific)
- Each question has 4 options (A/B/C/D format)

**Question format**:
```yaml
- id: "roe_concept"
  question: "ROE（股東權益報酬率）代表什麼？"
  options:
    - key: "A"
      label: "公司賺錢的效率"
      correct: true
      explanation: "ROE 衡量公司運用股東資金賺錢的能力，越高代表效率越好。"
    - key: "B"
      label: "公司負債的多寡"
      correct: false
      explanation: "負債多寡是負債比，不是 ROE。ROE 看的是股東權益的報酬。"
    # ... C, D options
```

#### 5. Ten-Second Test for C101

**Test**: Show a user a quiz question. Ask: "What concept is being tested?"

**Pass criteria**: User can identify the concept from the question alone in ≤10 seconds.

**Design implication**: Questions must use plain language. No jargon in the question stem. All options must be clearly distinct.

#### 6. Differentiation from C52 (Cancelled Feature)

**Why C52 was cancelled**: Standalone quiz mode — a separate page with disconnected questions. Users had no context for why they were being tested.

**Why C101 is different**: Contextual — questions appear after reading specific content. The quiz is directly relevant to what the user just learned. The UX is "check your understanding" not "take a test."

**Design guardrail**: C101 must NEVER become a standalone page. It must always be embedded within content sections. If a standalone quiz page is proposed, it should be rejected as a C52 regression.

---

## Design Direction C103

### Feature Summary
C103 adds an onboarding flow for first-time users. Shows a "Before you dive in" primer with 3-4 cards explaining what they'll learn, key terms, and estimated reading time. Users can skip it.

### UX Design Direction

#### 1. Primer Card Component

**New component needed**: `_primer_card()` in `_router_base.py`

```html
<!-- First visit primer card -->
<div style="background:#F8F9FA;border-radius:12px;padding:1.2rem;border-left:4px solid #3498DB;margin:0.5rem 0;">
    <div style="font-weight:600;color:#2C3E50;">{icon} {title}</div>
    <div style="font-size:0.9rem;color:#5D6D7E;margin-top:0.5rem;line-height:1.6;">{content}</div>
    <div style="font-size:0.85rem;color:#7F8C8D;margin-top:0.3rem;">⏱️ 預估閱讀時間：{time}</div>
</div>
```

**Design rationale**:
- Uses standard info card styling (blue border) — consistent with existing design system
- Each primer card answers one question: "What will I learn?" / "How long will it take?" / "What should I know first?"
- Estimated reading time sets expectations (reduces bounce rate)

#### 2. Primer Content Structure

**Recommended 4-card structure**:

| Card | Icon | Title | Content | Time |
|------|------|-------|---------|------|
| 1 | 🎯 | 你會學到什麼 | "這份名片會告訴你這家公司怎麼賺錢、財務健不健康、跟同業比起來如何。" | — |
| 2 | 📖 | 閱讀建議 | "建議從『營運摘要』開始，再看『財務體質』。每個區塊都可以展開看更多。" | — |
| 3 | ⏱️ 預估時間 | "完整閱讀約 5-8 分鐘。你可以隨時儲存到稍後觀看。" | — |
| 4 | 💡 | 小提醒 | "股識是歷史學家的角度，只說明發生過的事，不提供買賣建議。" | — |

**Total text**: ~150 Chinese characters (within 200-char limit)

#### 3. Placement and Interaction

**Design rule**: Primer appears at the **top of Zone C** (main content area), below the navbar (Zone A), above all content sections.

**Interaction flow**:
```
[First visit to business card page]
    ↓
[Primer cards appear at top of Zone C]
    ↓
[User reads primer → scrolls down to content]
    OR
[User clicks "跳過" button → primer collapses → content appears]
```

**Skip button design**:
```python
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("### 📋 開始前先看這裡")
with col2:
    if st.button("跳過", key=f"skip_primer_{stock_id}"):
        session_state["primer_dismissed"] = True
        st.rerun()
```

**Session state tracking**:
- `primer_dismissed` flag in session_state
- Once dismissed, primer never shows again (for that session)
- If persistence layer (D22) is implemented, store dismissal permanently

#### 4. Ten-Second Test for C103

**Test**: Show a first-time user the primer. Ask: "What is this page about and how long will it take?"

**Pass criteria**: User can answer both questions in ≤10 seconds.

**Design implication**: The primer must be scannable. Users should be able to grasp the purpose without reading every word. Icons + short titles + one-line descriptions.

#### 5. Mobile Considerations

**Risk**: 4 primer cards stacked vertically on mobile could push content far below the fold.

**Recommendation**: On mobile (< 768px), show only 2 primer cards:
1. "你會學到什麼" (what you'll learn)
2. "小提醒" (historian disclaimer)

Collapse the other 2 into an expander: "📖 更多閱讀建議"

---

## Design Risks

### Risk 1: Inline HTML Proliferation (HIGH)

**Description**: All three features require new card components. If developers create these as inline HTML instead of shared components, D-003 (inconsistent card styling) worsens.

**Probability**: HIGH — Sprint 7's C84 added 2 new inline HTML blocks despite D3 consolidation.

**Impact**: Card Component Consistency grade drops from B+ to B. Design grade at risk of A- → B+.

**Mitigation**:
- Create ALL new card components in `_router_base.py` BEFORE feature coding begins
- Add `_interpretation_card()`, `_quiz_card()`, `_primer_card()` to shared component library
- Pre-development checklist: "All new cards must use shared components"

### Risk 2: Historian Tone Violation in C98 (HIGH)

**Description**: C98 interpretations could drift from "why it matters historically" to "what you should do." This is the highest-risk design issue in Sprint 9.

**Probability**: MEDIUM — template-based interpretations are safer but still require careful wording.

**Impact**: Violates core product positioning. Could trigger Challenger rejection.

**Mitigation**:
- Write ALL interpretation templates before coding begins
- Each template must pass the "historian filter": does it explain what happened or advise what to do?
- Add `_historian_disclaimer("interpretation")` below every interpretation card
- QA gate: every interpretation must be reviewed by PM before shipping

### Risk 3: C103 Primer Becomes a Hard Gate (MEDIUM)

**Description**: If the primer is too prominent or can't be skipped easily, it becomes a barrier rather than a guide.

**Probability**: MEDIUM — depends on implementation.

**Impact**: User frustration, increased bounce rate, violates "ten-second test" (primer becomes the main content).

**Mitigation**:
- Primer must be dismissible with a single click ("跳過" button)
- Primer must NOT block content rendering (content should load behind/alongside primer)
- Primer should use `st.expander` with `expanded=True` (not a separate page or modal)
- On subsequent visits, primer must NOT appear

### Risk 4: C101 Content Scope Explosion (MEDIUM)

**Description**: Writing quiz questions is a content creation task that's hard to estimate. If the team tries to write questions for every section, the content effort could exceed the dev effort.

**Probability**: HIGH — the competitor research says "2-3 questions per section" which would be 12-18 questions per stock.

**Impact**: Sprint 9 scope creep, C101 becomes the bottleneck.

**Mitigation**:
- Cap at 5-8 questions total (not per section)
- Questions must be generic (reusable across stocks)
- Questions must be written by PM/designer, not developers
- If content isn't ready, defer C101 rather than shipping low-quality questions

### Risk 5: PPT-Style Text Limit Violation (MEDIUM)

**Description**: C98 interpretations + C101 quiz questions + C103 primer cards all add text to pages that are already approaching the 200-char limit.

**Probability**: MEDIUM — especially on the event dashboard where 50+ events each get an interpretation.

**Impact**: PPT-style grade drops. Pages become text-heavy.

**Mitigation**:
- C98: Interpretations must be ≤2 sentences (≤100 chars each)
- C101: Questions must be ≤50 chars, options ≤20 chars each
- C103: Total primer text ≤150 chars
- Event dashboard: Consider showing interpretations only for high/medium severity events (not low)

### Risk 6: Mobile Responsiveness Regression (LOW)

**Description**: New card components may not stack gracefully on mobile. C103 primer cards are especially risky (4 cards stacked vertically).

**Probability**: LOW — existing mobile CSS handles basic stacking.

**Impact**: Mobile grade remains B- (unchanged).

**Mitigation**:
- Test all new components on mobile viewport (375px width)
- C103: Reduce to 2 primer cards on mobile (see mobile considerations above)
- C98: Interpretation text must wrap (no fixed widths)

### Risk 7: Color Palette Expansion (LOW)

**Description**: C98 interpretation cards may need a new color (orange for "interpretation" variant). This would expand the design system palette.

**Probability**: LOW — can be mitigated by using existing blue palette (see C98 design above).

**Impact**: Design system color rules become more complex.

**Mitigation**: Use existing palette colors for all new cards. Do NOT add orange to the design system.

---

## Challenger Response Preparation

### Anticipated Challenge 1: "C98 without LLM is just a summary, not an interpretation"

**Response**: Agree. Template-based interpretations provide 80% of the value (consistent, fast, reliable) but lack the nuance of LLM. The recommended hybrid approach — templates for the dashboard, LLM for individual event drill-down — is the right balance. However, Phase 1 should ship with templates only. The LLM layer can be added in Phase 2 after the spike validates the approach. Shipping template-only C98 is better than shipping no C98.

**Design implication**: The template-only interpretation card must still pass the "why it matters" test. If templates feel like summaries, they need to be rewritten, not replaced with LLM.

### Anticipated Challenge 2: "C101 is just C52 rebranded. Why won't it fail the same way?"

**Response**: C52 was a standalone quiz page — disconnected from content, high friction, no context. C101 is contextual — questions appear after reading specific content, making them directly relevant. The UX is fundamentally different: C52 was "take a test," C101 is "check your understanding." The contextual approach has higher retention value and lower user friction.

**Design guardrail**: If C101 implementation starts looking like a standalone page, it should be flagged as a C52 regression.

### Anticipated Challenge 3: "C103 should be P1, not P2. First visit experience is critical for a beginner-focused product."

**Response**: Agree on the importance. The P2 rating is based on sprint capacity, not feature value. If the team believes C103 is more important than C98, the recommended direction would be C103 + C101 (deferring C98). However, C101 is CONFIRMED and should not be deferred. The question is whether to pair C101 with C98 or C103.

**Design note**: C103 is the lowest-risk feature (template content, no LLM, no complex logic). It could potentially be implemented alongside C101 if the team has capacity.

### Anticipated Challenge 4: "These features add a lot of text. How do you maintain PPT-style?"

**Response**: Valid concern. The design rules are:
- C98: ≤2 sentences per interpretation, only for high/medium severity events
- C101: ≤50 chars per question, collapsed by default (user clicks to expand)
- C103: ≤150 chars total, dismissible with one click
- All three features use progressive disclosure (expanders, buttons) to hide content until requested

The PPT-style principle is maintained by making all new content **optional** — users can skip the primer, ignore the quiz, and collapse interpretations.

---

## Recommendation

### Recommended Direction: Modified Direction A (C98 + C101) with C103 Lite

**Primary recommendation**: Implement C98 (hybrid) + C101 (scoped) in Sprint 9, with a lightweight C103 that adds minimal overhead.

#### Sprint 9 Scope

| Feature | Scope | Design Effort | Dev Effort |
|---------|-------|---------------|------------|
| **C98** | Template-based interpretations for event dashboard. 4 event types × 2 severities = 8 templates. LLM drill-down deferred to Phase 2. | 2h (template writing + card design) | 14-18h |
| **C101** | 5-8 generic quiz questions, embedded in content sections. Reusable across all stocks. | 3h (question writing + card design) | 8-12h |
| **C103 Lite** | 2-card primer (what you'll learn + historian disclaimer). Dismissible. No glossary, no reading time estimate. | 1h (content + card design) | 4-6h |
| **Total** | | **6h design** | **26-36h dev** |

#### Prerequisites (Before Coding)

1. **Create 3 new card components** in `_router_base.py` (1-2h):
   - `_interpretation_card(interpretation, historian_note)`
   - `_quiz_card(question, options, explanation)`
   - `_primer_card(icon, title, content, time)`

2. **Write all C98 interpretation templates** (2h):
   - 8 templates (4 types × 2 severities)
   - Each template must pass historian filter review

3. **Write all C101 quiz questions** (3h):
   - 5-8 questions covering core financial concepts
   - Each question must pass ten-second test

4. **Write C103 primer content** (1h):
   - 2 cards, ≤150 chars total

#### Design Grade Forecast

| Scenario | Grade | Condition |
|----------|-------|-----------|
| **Best case** | A | All 3 features use shared components, all content passes historian filter, PPT-style maintained |
| **Expected case** | A | C98 + C101 ship cleanly, C103 lite ships, 1-2 minor P2 issues from new components |
| **Worst case** | A- | New inline HTML in any feature, interpretation templates need rework, quiz content not ready |

#### Key Design Decisions Needed

1. **C98 color**: Use existing blue palette (`#3498DB` border, `#EBF5FB` background) or add orange to design system?
   - **Recommendation**: Use blue palette. Avoid palette expansion.

2. **C101 content ownership**: Who writes quiz questions?
   - **Recommendation**: PM/designer writes questions. Developers only implement the engine.

3. **C103 scope**: Full primer (4 cards) or lite (2 cards)?
   - **Recommendation**: Lite (2 cards) for Sprint 9. Full primer in Sprint 10 if D22 persistence is available.

4. **C98 LLM**: Include LLM drill-down in Sprint 9 or defer?
   - **Recommendation**: Defer to Phase 2. Ship templates only in Sprint 9.

---

## Appendix: New Card Component Specifications

### `_interpretation_card(interpretation, historian_note)`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `interpretation` | str | Yes | 2-sentence plain-language explanation of why the event matters |
| `historian_note` | str | Yes | 1-sentence historian caveat (green italic) |

**Styling**: `#EBF5FB` background, `#3498DB` left border, `border-radius:12px`, `padding:1.2rem`

### `_quiz_card(question, options, key_prefix)`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | str | Yes | Quiz question text (≤50 chars) |
| `options` | list[dict] | Yes | List of {key, label, correct, explanation} |
| `key_prefix` | str | Yes | Unique prefix for Streamlit button keys |

**Styling**: `#F8F9FA` background, `#3498DB` left border, feedback cards use `#EAFAF1` (correct) or `#FDEDEC` (incorrect)

### `_primer_card(icon, title, content, time)`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `icon` | str | Yes | Emoji icon |
| `title` | str | Yes | Card title (≤15 chars) |
| `content` | str | Yes | Card content (≤100 chars) |
| `time` | str | No | Estimated reading time (e.g., "5-8 分鐘") |

**Styling**: `#F8F9FA` background, `#3498DB` left border, `border-radius:12px`, `padding:1.2rem`

---

*Design Review by Design Reviewer. Next update: After Sprint 9 feature implementation or Round 21, whichever comes first.*
