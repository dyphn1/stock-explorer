## [Designer] Round 13 Feature Discussion — UX Analysis

> **Author**: Design Reviewer
> **Date**: 2026-06-12
> **Context**: 💡 Discussion theme — evaluating 6 new Round 13 features (C63-C68) for UX impact, design system integration, and design direction.
> **Current Design Grade**: A (0 P0, 7 P1, 10 P2)

---

## Evaluation Framework

Each feature is evaluated across 5 dimensions:

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **UX Fit** | 25% | Alignment with PPT-style, ten-second test, Zone A/B/C, color system |
| **New UI Components** | 20% | Number and complexity of new card types, widgets, or patterns needed |
| **Ten-Second Test** | 20% | A beginner can restate the core concept within 10 seconds |
| **Design Risk** | 15% | Page overload, positioning dilution, Streamlit constraints, content bottleneck |
| **Strategic Value** | 20% | Competitive differentiation, "historian" alignment, engagement impact |

---

### C63: Audio Market Story — Daily 3-Minute Market Narrative

**Summary**: A daily audio narration summarizing what happened in the market, in plain language, consumable in ~3 minutes. P2, 12-16h.

#### UX Fit: **MEDIUM**

**Strengths:**
- "Story first" alignment: Audio narrative about "what happened" directly reinforces historian positioning — it's a daily history briefing.
- Reaches auditory learners who don't engage with text-heavy PPT-style pages. Complements (not replaces) existing visual content.
- Ten-second test for the concept is trivial: "每天 3 分鐘，聽聽市場發生什麼事" — passes instantly.
- Low page-load impact: Audio widget is a component, not a page.

**Concerns:**
- **Zone placement is ambiguous.** An audio player doesn't fit neatly into Zone A (navbar — no interactive controls allowed), Zone B (sidebar — no page content), or Zone C (main content — it's a cross-cutting feature, not company-specific). This is the FIRST feature that challenges the Zone A/B/C model.
- **Streamlit has no native audio player widget** for dynamic content. `st.audio()` supports static files but not streaming or text-to-speech. Implementation requires: (a) pre-generating audio files and storing them, or (b) embedding a custom HTML5 audio player via `st.markdown(unsafe_allow_html=True)`. Option (a) is more reliable but requires audio generation infrastructure (D28: audio service layer).
- **New modality = new design patterns.** The entire existing design system is visual (cards, charts, typography). Audio introduces a completely new dimension — playback controls, progress indicators, playback speed, "listen history" — none of which have precedent in the current design system.

#### New UI Components Needed:
1. **`_audio_player_card()`** — NEW card type: Light blue border (`#3498DB`), background `#EBF5FB`, with embedded HTML5 audio player, playback controls, and "今日故事" title. Must handle loading states (audio generation may be async).
2. **Audio badge in Zone A** — Small "🔊 今日故事" indicator in navbar showing availability. This technically violates Zone A's "no interactive controls" rule — must be a display-only indicator.
3. **Audio service UI states** — Loading (spinner while generating), Ready (play button), Error ("音訊暫時無法播放"), Empty ("今日尚未更新").

| Component | Complexity | Precedent |
|-----------|-----------|-----------|
| `_audio_player_card()` | HIGH — new card type, HTML5 embed, state management | None — first audio UI |
| Audio badge (Zone A) | LOW — display only | C41 "Read Next" uses similar link pattern |
| Loading/error states | MEDIUM — new patterns | C44 Risk Analysis `st.expander` pattern |

#### Ten-Second Test: **PASS**
"每天 3 分鐘語音，聽聽市場今天發生什麼事" — any beginner understands this instantly. The concept is self-evident.

#### Design Risks:

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Streamlit audio limitations** — `st.audio()` only plays static files; dynamic generation requires custom HTML | P1 | Start with pre-generated MP3 files served statically. Defer real-time TTS to v2. Add to D28 (audio service layer). |
| **Zone A violation** — Audio availability indicator in navbar challenges "no interactive controls" rule | P2 | Make it display-only (badge, not button). Actual player lives in Zone C or Zone B sidebar. |
| **Audio quality perception** — Robotic TTS damages credibility and historian tone | P1 | MVP approach: Start with human-written scripts narrated by TTS engine with acceptable quality (e.g., Google TTS zh-TW). Accept robotic quality for MVP; upgrade in v2. |
| **Content creation** — 365 daily narrations/year = massive content burden | P2 | Start with weekly (not daily). Template-based generation from existing analogy_engine + adaptive_engine content. Auto-markup with SSML for TTS. |
| **Accessibility paradox** — Audio helps auditory learners but excludes hearing-impaired users | P2 | Always provide text transcript below the audio player. Transcript is default view; audio is opt-in. |

#### Integration Approach:

**Recommended: Zone B sidebar widget + dedicated Zone C page.**
- **Zone B**: Small "🔊 每日市場故事" widget in sidebar with mini-play button and "播放今日故事" CTA. When clicked, navigates to the audio page.
- **Zone C**: Dedicated "每日故事" page with full audio player card, transcript below, and archive of past stories. Follows the existing PPT-style: one story per page, chart supplement, ≤ 200 chars summary.

**Streamlit-specific constraint**: Use `st.audio(filename, format="audio/mp3")` for static files. For a daily story, generate the MP3 on a cron schedule and save to `static/audio/YYYY-MM-DD.mp3`. The page loads the current day's file.

```
Zone C — Daily Story Page:
┌─────────────────────────────────────────────┐
│  🔊 每日市場故事                   6月12日  │
│  "聽聽今天市場發生了什麼事"                    │
│                                              │
│  [▶️ 播放今日故事 (3分鐘)]                     │
│  ━━━━━━━●━━━━━━━━ 1:23 / 3:00              │
│                                              │
│  ── 文字版 ──                                │
│  [Story summary card: ≤ 200 chars]           │
│  [Key chart: market movement visualization]  │
│                                              │
│  ── 過去故事 ──                              │
│  [6月11日] [6月10日] [6月9日] ...           │
└─────────────────────────────────────────────┘
```

**Quick Win vs. Major Redesign**: **Medium-term feature** — not a quick win due to D28 (audio service layer) dependency and content generation infrastructure. However, the UI itself is simple (one card type + one page). The complexity is in the backend audio generation, not the frontend design.

---

### C64: Community Q&A — Peer Learning Forum

**Summary**: A forum where users can ask questions about stocks, financial concepts, and market events, and get answers from other users. P2, 16-24h.

#### UX Fit: **LOW-MEDIUM**

**Strengths:**
- "Point-to-point knowledge construction" — directly aligns with the education-first vision. Peer learning is the dominant engagement model among competitors (Naver Finance, 雪球, Dcard, Reddit).
- Ten-second test passes: "問問題，學投資" — trivially clear.
- Creates a reason to return: Users come back to check answers, respond to comments, and see new questions.

**Concerns:**
- **Fundamentally challenges the "historian" positioning.** Community Q&A is inherently social and opinion-based. Answers may contain speculation, predictions, or buy/sell advice — directly contradicting the "only say what happened" principle. This is the HIGHEST positioning risk of any Round 13 feature.
- **Requires a persistence layer.** Unlike session-only features (C55, C60), Q&A content must persist across sessions. This requires D22 (persistence layer) — a known open architecture debt item. Without D24/D22, this feature cannot be built.
- **Moderation burden.** User-generated content requires moderation to maintain historian tone and prevent investment advice. This is an ongoing operational cost, not a one-time development effort.
- **Streamlit is not a forum platform.** There is no native forum/thread/comment widget. Everything must be built from scratch: question listing, thread view, reply input, voting, sorting. This is the most complex UI feature proposed in Round 13.
- **Zone placement**: Where does the forum live? It's not company-specific (doesn't belong on business card page), not a navigation element (not Zone B), not a navbar item (not Zone A). It needs its own top-level page — adding to an already crowded navbar.

#### New UI Components Needed:
1. **`_question_card()`** — NEW card type: White border, question title, preview text, metadata (author, date, reply count, tags). Follows existing card patterns but with social metadata.
2. **`_answer_card()`** — NEW card type: Nested inside question thread, with vote indicator, author, content, timestamp.
3. **`_tag_badge()`** — NEW micro-component: Small colored badges for topic tags (e.g., "台積電", "本益比", "新手問題"). Uses existing color system.
4. **Thread view page** — Full page with question at top, sorted answers below, reply input at bottom.
5. **Question composition form** — Title input, body textarea, tag selector. Must include historian tone guidelines ("問『發生什麼』，不是問『該不該買』").

| Component | Complexity | Precedent |
|-----------|-----------|-----------|
| `_question_card()` | MEDIUM — new card with metadata | `_info_card()` pattern |
| `_answer_card()` | MEDIUM — nested card with voting | None — first social UI |
| `_tag_badge()` | LOW — small colored pill | Industry tag in Zone A |
| Thread view | HIGH — full page, multiple components | None — first forum UI |
| Composition form | MEDIUM — form + validation | C55 Diary input pattern |

#### Ten-Second Test: **PASS**
"問問題，學投資，大家一起討論" — passes easily. The concept is universally understood.

#### Design Risks:

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Positioning dilution** — Q&A becomes a stock-picking forum, not a historian community | P0 | Strict moderation guidelines. Auto-flag keywords ("買", "賣", "建議", "報明牌"). Required disclaimer on every post: "本討論區僅分享公司歷史與事實，不構成投資建議。" |
| **Persistence layer dependency** — Cannot build without D22 | P0 | Defer until D22 is resolved. MVP alternative: Use YAML file storage (like watchlist.py) as a stopgap. |
| **Empty forum problem** — New users see zero questions, no reason to participate | P1 | Seed with 10-15 curated Q&A pairs from existing analogy_engine content. Show "熱門問題" prominently. |
| **Moderation at scale** — Manual moderation doesn't scale | P1 | MVP: Single moderator (the team). v2: Community flagging + auto-moderation rules. Accept that moderation is an ongoing cost. |
| **Streamlit re-rendering** — Forum requires real-time updates; Streamlit's re-run model means new answers only appear on refresh | P2 | Acceptable for MVP. Use `st.rerun()` after form submission. v2: Consider WebSocket or polling. |
| **Navbar crowding** — Adding "社群討論" to navbar adds another tab | P2 | Consolidate with existing "Event Dashboard" or add as a sidebar item instead of navbar tab. |

#### Integration Approach:

**Recommended: Dedicated top-level page + sidebar entry point.**
- **Zone B**: Add "💬 社群討論" to sidebar with question count badge.
- **Zone C**: Full forum page with question list → thread view → composition form.
- **Tone enforcement**: Every question/answer form includes a visible historian tone reminder. Auto-flagged content goes to moderation queue.

```
Zone C — Community Q&A Page:
┌─────────────────────────────────────────────┐
│  💬 社群討論                                  │
│  "問問題，學投資，大家一起討論"                 │
│                                              │
│  [+ 提問]  [熱門] [最新] [未回答]             │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ ❓ 台積電的本益比為什麼這麼高？          │   │
│  │ 回覆：3  瀏覽：156  標籤：#台積電 #本益比│   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │ ❓ 自由現金流跟淨利有什麼不同？          │   │
│  │ 回覆：5  瀏覽：89  標籤：#財務報表 #新手  │   │
│  └──────────────────────────────────────┘   │
│  ...                                         │
└─────────────────────────────────────────────┘
```

**Quick Win vs. Major Redesign**: **Major redesign** — this is the most complex feature in Round 13 from a UX perspective. It requires new card types, new page types, new interaction patterns (voting, threading, moderation), and a persistence layer. It also carries the highest positioning risk. Should NOT be built until the core education features (C56, C58, C62) are stable.

---

### C65: Company Story Game — Gamified Learning Through Play

**Summary**: Gamified learning where users progress through company stories via interactive gameplay — matching events to companies, sequencing historical events, or identifying company milestones. P2, 10-14h.

#### UX Fit: **MEDIUM-HIGH**

**Strengths:**
- "Point-to-point knowledge construction" + "Ten-second test" + "Engagement" — aligns with three of five core design principles simultaneously.
- Gamification is the strongest engagement driver among competitors (Wall Street Survivor, 雪球 Investment Diary, Stake onboarding all prove this).
- Ten-second test: "玩遊戲，學公司故事" — trivially clear.
- Can reuse existing company facts, events, and analogy content — no new content creation needed if built on top of existing data.

**Concerns:**
- **Game UI is a completely new interaction model.** Stock Explorer has no game mechanics. Everything is read-only data display. Adding interactive gameplay (drag-and-drop, matching, sequencing) requires custom JavaScript or Streamlit components — both are fragile and hard to maintain.
- **Zone C game area needs significant space.** Games require a large interactive area, which conflicts with PPT-style "charts take >60% of page area" principle. A game page would be 100% game, 0% chart — which is fine for a dedicated game page but breaks the visual consistency of other pages.
- **Scoring/feedback UI** — Games need score displays, progress indicators, correct/incorrect feedback, and completion states. None of these exist in the current design system.
- **Historian tone in game context** — Game mechanics (points, levels, competition) can trivialize the educational content. "You scored 800 points on TSMC!" vs "You now understand TSMC's history." The framing matters enormously.

#### New UI Components Needed:
1. **`_game_card()`** — NEW card type: Purple/violet border (NEW COLOR — not in existing palette), game-specific layout with interactive elements. This is the first component that may need a color outside the existing blue/green/red/amber system.
2. **`_game_feedback()`** — NEW component: Correct/incorrect feedback overlay with plain-language explanation. Must use blue (correct) and amber (incorrect) — NOT green/red (reserved for price direction).
3. **`_progress_bar()`** — NEW micro-component: Visual progress indicator for game levels/rounds.
4. **`_score_display()`** — NEW micro-component: Score badge with historian-flavored framing ("你認識了 5 家公司" not "你得了 500 分").

| Component | Complexity | Precedent |
|-----------|-----------|-----------|
| `_game_card()` | HIGH — interactive, custom JS likely | None — first game UI |
| `_game_feedback()` | MEDIUM — overlay with animation | None — first feedback UI |
| `_progress_bar()` | LOW — simple visual | None — first progress indicator |
| `_score_display()` | LOW — badge component | C60 Badge card (planned) |

#### Ten-Second Test: **PASS**
"玩遊戲，學公司故事" — passes easily. Everyone understands "learn through play."

#### Design Risks:

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Streamlit game limitations** — No native game widgets; drag-and-drop, matching, sequencing all require custom JS | P1 | Start with simple multiple-choice format (like C64 Daily Quiz). Avoid drag-and-drop for MVP. Use radio buttons + submit pattern. |
| **New color needed** — Game cards may want purple/violet for "fun" feel, but this violates the color system | P2 | Use existing blue (`#3498DB`) for game cards. The "fun" factor comes from interaction, not color. |
| **Gamification trivializes content** — Points/scores can undermine historian seriousness | P1 | Frame scores as "understanding" not "points." "你認識了 5 家公司" not "500 分." No leaderboards in MVP. |
| **Content dependency** — Game questions need structured event/timeline data per company | P2 | Build on existing `company_facts.yaml` and `events` data. Start with 5 companies that have rich event histories. |
| **Accessibility** — Game interactions may not be keyboard-accessible or screen-reader friendly | P2 | Ensure all game interactions work with keyboard. Provide text-based alternative for each game type. |

#### Integration Approach:

**Recommended: Dedicated game page accessible from sidebar + contextual links from company pages.**
- **Zone B**: "🎮 公司故事遊戲" sidebar entry with "開始遊戲" button.
- **Zone C**: Full game page with game type selection (配對遊戲, 排序遊戲, 選擇題) → game area → feedback → next round.
- **Contextual**: On business card page, add a "🎮 玩這個公司的故事遊戲" link that launches the game pre-loaded with that company's data.

```
Zone C — Game Page:
┌─────────────────────────────────────────────┐
│  🎮 公司故事遊戲                              │
│  "玩遊戲，學公司故事"                          │
│                                              │
│  ── 選擇遊戲 ──                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ 配對遊戲  │ │ 排序遊戲  │ │ 選擇題   │    │
│  │ 事件→公司 │ │ 時間排序  │ │ 公司知識 │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│                                              │
│  ── 遊戲中 ──                                 │
│  第 3 題 / 10                               │
│  ━━━━━━●━━━━━━━━━━━━                        │
│                                              │
│  「台積電成立於哪一年？」                       │
│  ○ 1985  ○ 1987  ○ 1990  ○ 1995           │
│                                              │
│  [提交答案]                                   │
└─────────────────────────────────────────────┘
```

**Quick Win vs. Major Redesign**: **Medium-term feature** — the concept is simple but the implementation requires new interaction patterns. The multiple-choice game format (simplest variant) could be a quick win if built on top of C64's quiz infrastructure. The more complex game types (matching, sequencing) require custom JS and are major undertakings.

---

### C66: Conversational Tone — UX Writing Overhaul for Approachability

**Summary**: A comprehensive overhaul of all UI text — labels, descriptions, card content, error messages, empty states — to use a warm, conversational tone that lowers barriers for beginners. P2, 6-10h.

#### UX Fit: **HIGH**

**Strengths:**
- **Zero new UI components needed.** This is a content/writing change, not a design change. Every existing card, page, and component stays the same — only the text changes.
- **Directly supports three core principles**: "Story first" (narrative tone), "Ten-second test" (simpler language = faster comprehension), "Beginner-friendly" (conversational = less intimidating).
- **Competitor validation**: Morning Brew's success proves conversational tone dramatically lowers barriers to financial learning.
- **Ten-second test**: "用更親切的方式學投資" — trivially clear.
- **No Zone A/B/C impact.** Text changes don't affect layout.
- **No color system impact.** Text changes don't affect colors.
- **No Streamlit limitations.** It's just string changes.

**Concerns:**
- **Scope ambiguity.** "All UI text" could mean 500+ strings across 12+ page modules. Need clear scope definition: MVP = card labels + section titles + error messages + empty states. v2 = full content rewrite.
- **Tone consistency.** Without a style guide, different sections may end up with different tones. Need a "tone guideline" document before starting.
- **Historian tone vs. conversational tone tension.** "Conversational" could drift into "casual" or "flippant," undermining the historian's authority. The tone must be warm but factual, friendly but not silly.

#### New UI Components Needed: **NONE**

This is purely a content change. No new card types, widgets, or patterns needed.

However, a **Tone Guide** document should be created:
```
Tone Guidelines (C66):
- Use "你" (informal you) — creates personal connection
- Use questions to engage: "知道為什麼嗎？" not "原因如下"
- Use analogies: "就像..." "好比..."
- Avoid: financial jargon without translation, passive voice, long sentences
- Maintain: historian authority (factual, past-tense, no predictions)
- Character limit: labels ≤ 15 chars, descriptions ≤ 40 chars, explanations ≤ 2 sentences
```

#### Ten-Second Test: **PASS**
"用更親切、更白話的方式學投資" — passes instantly.

#### Design Risks:

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Tone inconsistency** — Different writers produce different tones | P2 | Create tone guide FIRST. Use analogy_engine templates for consistency. Single reviewer for all text changes. |
| **Scope creep** — "All UI text" is unbounded | P2 | Define MVP scope: card labels + section titles + error/empty states only. Defer full content rewrite to v2. |
| **Historian authority erosion** — Too casual = loss of trust | P1 | Tone rule: "Friendly professor, not funny friend." Warm but authoritative. Review all text against historian positioning. |
| **Chinese writing quality** — Conversational TW Chinese is harder to write well than formal Chinese | P2 | Reference Morning Brew's Chinese edition (if available) or 白話金融 content for tone examples. |

#### Integration Approach:

**Recommended: Phased rollout across existing pages.**
1. **Phase 1 (MVP)**: Update all card labels, section titles, error messages, and empty states to conversational tone. 6-10h.
2. **Phase 2**: Update analogy engine templates to conversational tone. 4-6h.
3. **Phase 3**: Update all page-level descriptions and CTAs. 4-6h.

**No new pages, no new components, no layout changes.** This is a find-and-replace + rewrite operation across existing files.

**Example transformations:**
| Before (Formal) | After (Conversational) |
|------------------|----------------------|
| "關鍵數字" | "先看這三個數字" |
| "財務健康檢查" | "這家公司財務狀況如何？" |
| "暫無資料" | "這部分目前沒有資料哦" |
| "風險分析" | "什麼可能出問題？" |
| "推薦閱讀" | "接下來看什麼？" |

**Quick Win vs. Major Redesign**: **QUICK WIN** — lowest effort (6-10h), no new components, no dependencies, no architectural changes. Can be done in ANY sprint as a parallel workstream. Highest ROI per hour of any Round 13 feature.

---

### C67: Community-Curated Stock Stories — User-Generated Narrative Layer

**Summary**: Users can write and share their own "stock stories" — narrative explanations of what happened to a company, why it matters, and what they learned. Other users can read, react to, and learn from these stories. P2, 14-20h.

#### UX Fit: **LOW-MEDIUM**

**Strengths:**
- "Story first" + "Adaptive" + "Point-to-point knowledge construction" — aligns with three core principles.
- User-generated content scales education beyond what the team can create alone.
- Ten-second test: "看別人怎麼說公司故事" — clear.
- Competitor validation: 雪球 Stock Stories and eToro Investor Profiles prove this model works.

**Concerns:**
- **Highest positioning risk in Round 13** (tied with C64). User-generated stories may contain speculation, predictions, or investment advice. Unlike C64 (Q&A, which can be moderated question-by-question), stories are long-form and harder to moderate.
- **Requires persistence layer** (same as C64 — D22 dependency).
- **Requires moderation system** (same as C64 — ongoing operational cost).
- **New interaction model**: Story composition (long-form text input), story reading (narrative layout), story discovery (browsing/searching), and reaction system (emoji/likes). None of these exist in the current design system.
- **Content quality control**: Unlike structured cards, free-form stories vary wildly in quality, length, and accuracy. Need a quality framework.
- **Zone placement**: Stories are company-specific but user-generated. Do they live on the business card page (Zone C, but mixed with curated content) or on a separate page (Zone C, but disconnected from company data)?

#### New UI Components Needed:
1. **`_story_card()`** — NEW card type: User avatar, story title, preview text, author name, date, reaction count, "閱讀更多" CTA. Similar to `_question_card()` but for long-form content.
2. **`_story_compose_form()`** — NEW form: Title input, rich text area, company selector, tag selector, preview, submit. More complex than C55 Diary input.
3. **`_story_reader_page()`** — NEW page type: Full story view with title, author, date, content, reactions, related company link.
4. **`_reaction_bar()`** — NEW micro-component: Emoji reactions (👍 有用, 🤔 有趣, 📚 學到東西) with counts.

| Component | Complexity | Precedent |
|-----------|-----------|-----------|
| `_story_card()` | MEDIUM — card with social metadata | `_info_card()` pattern |
| `_story_compose_form()` | HIGH — multi-field form with validation | C55 Diary input (simpler) |
| `_story_reader_page()` | MEDIUM — article layout | None — first long-form content page |
| `_reaction_bar()` | LOW — emoji + count | None — first reaction UI |

#### Ten-Second Test: **PASS**
"看別人怎麼說公司故事，也可以自己寫" — passes easily.

#### Design Risks:

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Positioning dilution** — User stories become opinion/advice forums | P0 | Required historian tone guidelines. Auto-flag predictive language. Moderation queue for all submissions. |
| **Persistence layer dependency** — Cannot build without D22 | P0 | Defer until D22 resolved. YAML stopgap possible but not ideal for UGC. |
| **Content quality variance** — Free-form stories range from excellent to misleading | P1 | Template-based composition (guided prompts, not blank page). Minimum length requirement. "優質故事" curation. |
| **Low participation** — Chicken-and-egg: no readers without writers, no writers without readers | P1 | Seed with 10-15 team-written stories. Feature "本週精選故事" prominently. |
| **Mixed content on business card page** — User stories alongside curated data creates visual confusion | P1 | Keep user stories SEPARATE from curated content. Dedicated "社群故事" section with clear visual distinction (different card style, "社群創作" label). |
| **Copyright/plagiarism** — Users may copy content from other sources | P2 | DMCA-style reporting. Originality guidelines. Small enough scale that manual review is feasible. |

#### Integration Approach:

**Recommended: Dedicated story section on company pages + separate story discovery page.**
- **Zone B**: "📖 社群故事" sidebar entry.
- **Zone C (Company Page)**: "大家怎麼說" section at the bottom of the business card page, below all curated content. Clearly labeled "社群創作" with distinct card styling (dashed border or different background).
- **Zone C (Story Page)**: Full story reader with composition form, story browser, and "本週精選" section.

```
Zone C — Business Card Page (bottom section):
┌─────────────────────────────────────────────┐
│  📖 大家怎麼說 — 社群創作                      │
│  "其他使用者怎麼看這家公司"                      │
│                                              │
│  ┌──────────────────────────────────────┐   │
│  │ 📝 台積電的護城河觀察                    │   │
│  │ by 投資新手小明 | 👍 23 | 📚 15        │   │
│  │ 「我覺得台積電之所以難以取代，是因為...」  │   │
│  └──────────────────────────────────────┘   │
│  ┌──────────────────────────────────────┐   │
│  │ 📝 從蘋果訂單看台積電的客戶集中度         │   │
│  │ by 歷史學徒 | 👍 41 | 📚 28            │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  [+ 寫一個故事]                               │
└─────────────────────────────────────────────┘
```

**Quick Win vs. Major Redesign**: **Major redesign** — second most complex feature in Round 13 (after C64). Requires new card types, new page types, composition forms, moderation system, and persistence layer. Should be deferred until C64 (Community Q&A) is stable, as both share the same infrastructure needs.

---

### C68: Financial Concept Storytelling — Narrative-Based Concept Explanations

**Summary**: Structured educational content that explains financial concepts through narrative — "What is P/E Ratio?" becomes a story about a real company's P/E history, why it changed, and what it means. P1, 12-16h.

#### UX Fit: **HIGH**

**Strengths:**
- **"Story first" + "Point-to-point knowledge construction" + "Ten-second test"** — aligns with three core principles, the strongest alignment of any Round 13 feature.
- **P1 priority** — the only P1 feature in Round 13, reflecting its strategic importance.
- **Builds on existing infrastructure**: analogy_engine (850 lines) already generates plain-language explanations. This feature wraps those explanations in narrative structure with real company examples.
- **Ten-second test**: "用故事學會財務概念" — passes instantly.
- **Competitor validation**: Zerodha Varsity (India's most popular investing education platform) uses exactly this approach. Khan Academy's financial lessons are narrative-based. 雪球投資學院 uses story-first explanations.
- **Fits PPT-style perfectly**: One concept = one story = one page. Chart shows the concept in action. Text ≤ 200 chars.
- **Fits Zone A/B/C perfectly**: New top-level page in Zone C. No zone violations.
- **Fits color system perfectly**: Uses existing blue/green/red for concept illustrations.

**Concerns:**
- **Content creation is the bottleneck.** Each concept story requires: (a) concept definition, (b) real company example, (c) narrative structure, (d) chart configuration, (e) plain-language explanation. At 2-3 hours per concept × 10 concepts = 20-30h content work.
- **New card type needed**: `_concept_story_card()` — but this follows the exact same pattern as existing cards, just with a specific content structure.
- **Depends on analogy_engine quality.** If analogy_engine explanations are generic, the stories will be too. May require analogy_engine improvements (D16 — splitting the god module) before this feature reaches its potential.

#### New UI Components Needed:
1. **`_concept_story_card()`** — NEW card type: Blue border (`#3498DB`), light blue background (`#EBF5FB`), with concept title, one-line definition, "看故事" CTA. Follows existing card patterns exactly.
2. **`_concept_detail_page()`** — NEW page type: Full story view with concept definition → narrative → real company example → chart → "為什麼重要" → related concepts. Follows PPT-style: one concept per page, chart > 60% of space.
3. **`_related_concepts()`** — NEW micro-component: "你可能也想學" links at the bottom of each concept page. Uses existing card styling.

| Component | Complexity | Precedent |
|-----------|-----------|-----------|
| `_concept_story_card()` | LOW — follows existing card pattern | `_info_card()` / `_explain_card()` |
| `_concept_detail_page()` | MEDIUM — new page, but follows PPT-style | Business card page pattern |
| `_related_concepts()` | LOW — simple link cards | C41 Read Next pattern |

#### Ten-Second Test: **PASS**
"用故事學會財務概念" — passes instantly. The concept is self-evident and compelling.

#### Design Risks:

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Content creation bottleneck** — 10 concepts × 2-3h = 20-30h content work | P1 | Start with 5 core concepts (P/E, ROE, P/B, Gross Margin, Debt Ratio). Use existing analogy_engine content as starting point. |
| **Analogy engine quality** — Generic explanations produce generic stories | P2 | Improve analogy_engine templates for narrative context. D16 (split god module) enables this. |
| **Concept selection** — Which 10 concepts to teach first? | P2 | Start with the 10 metrics already identified for C56 (Explain This Metric). Reuse the same content architecture. |
| **Overlap with C56** — Both explain financial concepts. C56 is interactive (tap to explain), C68 is narrative (read a story). | P2 | Clear boundary: C56 = "What does this metric mean right now?" (in-context, on-demand). C68 = "Let me teach you this concept through a story" (structured, educational). Complementary, not competing. |

#### Integration Approach:

**Recommended: Dedicated "學習" section accessible from sidebar + navbar.**
- **Zone B**: "📚 財務概念故事" sidebar entry.
- **Zone C**: Concept grid page (like Sector Stories grid) → concept detail page (full story).
- **Cross-linking**: C56 "Explain This Metric" buttons link to C68 concept stories. C68 concept stories link to relevant company pages.

```
Zone C — Concept Grid Page:
┌─────────────────────────────────────────────┐
│  📚 財務概念故事                              │
│  "用故事學會投資知識"                          │
│                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ 本益比    │ │ ROE      │ │ 毛利率   │    │
│  │ P/E      │ │ 股東權益  │ │ Gross    │    │
│  │ 3分鐘閱讀 │ │ 報酬率   │ │ Margin   │    │
│  └──────────┘ └──────────┘ └──────────┘    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐    │
│  │ 股價淨值比│ │ 負債比率  │ │ 殖利率   │    │
│  │ P/B      │ │ Debt     │ │ Dividend │    │
│  └──────────┘ └──────────┘ └──────────┘    │
└─────────────────────────────────────────────┘

Zone C — Concept Detail Page:
┌─────────────────────────────────────────────┐
│  📚 本益比 (P/E Ratio) 的故事                │
│  「股價是貴還是便宜？」                        │
│                                              │
│  [Concept Story Card: 2-3 sentences]         │
│  "本益比就像是在問：你願意花多少錢，買公司    │
│   賺的每一塊錢？"                              │
│                                              │
│  ── 用台積電來理解 ──                          │
│  [Narrative: TSMC's P/E history in story form]│
│  [Chart: TSMC P/E trend over 5 years]        │
│                                              │
│  ── 為什麼重要 ──                              │
│  [Plain-language explanation: ≤ 2 sentences] │
│                                              │
│  ── 你可能也想學 ──                            │
│  [ROE] [P/B] [毛利率]                        │
└─────────────────────────────────────────────┘
```

**Quick Win vs. Major Redesign**: **Medium-term feature** — the UI is simple (reuses existing card patterns), but the content creation is substantial. The P1 priority reflects its strategic value. Should be started as soon as C56 (Explain This Metric) is stable, as both share content infrastructure.

---

## Design Priority Ranking

### Quick Wins (can start immediately, no dependencies)

1. **C66: Conversational Tone** — 6-10h, zero new components, zero dependencies, highest ROI/hour. Can be done in ANY sprint as parallel workstream. Improves every existing page instantly.

### High-Value Medium-Term (build after Sprint 4)

2. **C68: Financial Concept Storytelling** — P1 priority, 12-16h, builds on existing analogy_engine. Strongest alignment with core design principles. New card type follows existing patterns. Content creation is the main bottleneck, not UI complexity.

3. **C63: Audio Market Story** — 12-16h, new modality but simple UI (one card type + one page). D28 (audio service layer) is the main dependency. Start with weekly (not daily) to reduce content burden.

### Engagement Drivers (build after core education features)

4. **C65: Company Story Game** — 10-14h, gamification drives retention. Multiple-choice variant can reuse C64 quiz infrastructure. Custom JS game types deferred to v2.

5. **C64: Community Q&A** — 16-24h, highest complexity. Requires D22 (persistence layer). Highest positioning risk. Must have moderation system. Defer until core education features are stable.

6. **C67: Community-Curated Stock Stories** — 14-20h, shares D22 dependency with C64. Second highest positioning risk. Should follow C64 (reuses forum infrastructure). Template-based composition reduces quality variance.

---

## Design Direction Recommendation

### Build First: C66 + C68 (The "Story Core")

**Why**: These two features form the foundation of Stock Explorer's education positioning:
- **C66** makes everything more approachable (writing change, not design change)
- **C68** makes concepts memorable (narrative structure + real examples)

Together, they transform Stock Explorer from "a tool that shows company data" into "a platform that teaches you to understand companies through stories." This is the purest expression of the "historian" positioning.

**Effort**: 18-26h total. Fits within a single sprint as parallel workstreams.

### Build Second: C63 (The "Multi-Modal" Expansion)

**Why**: Audio reaches users who don't engage with text. It also creates a daily habit loop (daily story = daily visit). The UI is simple; the backend audio generation is the complexity.

**Effort**: 12-16h + D28 audio service layer. Best placed in Sprint 5-6.

### Build Third: C65 (The "Engagement" Layer)

**Why**: Gamification drives retention. The multiple-choice variant is simple and can reuse C64's quiz infrastructure. More complex game types (matching, sequencing) require custom JS and should be deferred.

**Effort**: 10-14h for multiple-choice variant. Best placed in Sprint 5-6 alongside C63.

### Build Last: C64 + C67 (The "Community" Layer)

**Why**: Community features are the highest-risk, highest-complexity, and highest-positioning-risk features. They require D22 (persistence layer), moderation systems, and careful tone enforcement. They should only be built after the core education experience (C66, C68, C56, C58) is proven and stable.

**Effort**: 30-44h combined + D22 dependency. Best placed in Sprint 7+.

### Design System Impact Summary

| Feature | New Card Types | New Pages | New Colors | Zone Challenges | Persistence Needed |
|---------|---------------|-----------|------------|-----------------|-------------------|
| C63 | 1 (`_audio_player_card`) | 1 | None | Zone A badge (display-only) | No (static files) |
| C64 | 2 (`_question_card`, `_answer_card`) | 2 | None | None | **Yes (D22)** |
| C65 | 1 (`_game_card`) | 1 | None (use blue) | None | No (session-only MVP) |
| C66 | **0** | **0** | **0** | **0** | **0** |
| C67 | 1 (`_story_card`) | 2 | None | Mixed content on company pages | **Yes (D22)** |
| C68 | 1 (`_concept_story_card`) | 2 | None | None | No (static YAML) |

### New Design Issues to Track

| ID | Title | Severity | Source |
|----|-------|----------|--------|
| **D-036** | Audio player card needs new card type outside existing system | P2 | C63 |
| **D-037** | Community features (C64, C67) require persistence layer (D22) | P1 | C64, C67 |
| **D-038** | Community features (C64, C67) carry historian positioning risk | P1 | C64, C67 |
| **D-039** | C65 game interactions may require custom JS beyond Streamlit capabilities | P2 | C65 |
| **D-040** | C66 tone overhaul needs style guide to maintain consistency | P2 | C66 |
| **D-041** | C68 content creation bottleneck (20-30h) may delay launch | P1 | C68 |

---

*Design Review completed. 6 features evaluated. 2 quick wins identified (C66, C68). 2 medium-term features (C63, C65). 2 long-term features requiring infrastructure (C64, C67). 6 new design issues proposed. Recommendation: Build C66 + C68 first as the "Story Core" that defines Stock Explorer's education positioning.*
