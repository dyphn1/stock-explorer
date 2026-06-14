## 2026-06-18 主題: 檢討

### Round 1
- **團隊方案**: 團隊提出8項新功能缺口（C55-C62），來源於競爭對手研究，包括投資日誌、互動式財務概念解釋、概念比較工具、新手導流、AI問答聊天機器人、概念掌握徽章、產業輪動視覺化和投資前檢查清單。所有功能均聲稱與「歷史學家」定位、點對點知識建構、十秒測試和故事優先等對齊。
- **質疑**: 這些功能缺口是否真正符合我們的核心定位「歷史學家，而非選股工具」？例如：
  - C55（投資日誌）和C62（投資前檢查清單）似乎更側重於個人投資行為追蹤和決策輔助，是否會引導使用者向短期操作或選股方向發展？
  - C56（互動式財務概念解釋）和C59（AI問答聊天機器人）雖主張知識建構，但若設計不當，可能變成即時股票查詢工具，違反「非選股」原則。
  - C57（概念比較工具）和C61（產業輪動視覺化）涉及市場層面分析，是否會誘導使用者進行市場時機判斷而非深入理解公司歷史？
  - 是否有競爭對手缺失但我們應該補強的功能？例如，更深入的公司歷史事件時間線、多維度歷史績效分解或歷史案例研究庫？
  - 建議重新評估每項功能的歷史學價值：它是否幫助使用者理解公司過去的決策脈絡、業務演變或歷史事件影響，而非預測未來股價？

### Round 2
- **團隊回應**: 團隊堅持這些功能缺口是必要的，原因是：(1) 競爭對手（尤其台資券商）正在加速教育功能落地，我們若不跟進將失落新手使用者；(2) 每項功能均經過對齊檢查，設計為服務於知識建構而非選股；(3) 例如投資日誌可幫助使用者反思過去投資決策，屬歷史學習；AI問答聊天機器人將被限制在解釋歷史財務數據而非提供買賣建議。
- **再次質疑**: 優先順序是否正確？具體質疑：
  - 為何C56（P1）和C58（P1）被列為最高優先，而架構債項D16（拆分類比引擎）被識為關鍵路徑項目？D16不僅是高優先架構債，且被明確指出為解鎖C44、C38和C48的必要前置作業。若不先處理D16，後續功能開發將受嚴重阻礙。
  - 團隊是否低估了技術債對新功能開發的影響？例如，類比引擎神模組使得新功能如C44（風險分析）和C38（比較故事）難以擴展和維護。
  - 在資源有限的情況下，是應該先投入開發可能偏離核心定位的新功能（如C59 AI聊天機器人），還是先鞏固基礎架構並開發更直接服務於歷史學家定位的功能（如C44風險分析，它需要分析歷史風險事件）？
  - 建議將D16提升為絕對優先（P0），在完成D16後重新評估哪些新功能真正服務於歷史學家定位，然後按歷史學價值排序開發。

### Round 3
- **最終方案**: 團隊在考慮挑戰後維持原計畫：(1) D16將在Sprint 3中處理（如報告所述），但新功能缺口（尤其C56和C58）仍將優先開發以應對競爭壓力；(2) 團隊相信透過嚴格的功能設計審核（例如限制AI聊天機器人只回答歷史問題）可以確保功能不偏離定位；(3) 教育功能是必要的防禦性策略，以防止使用者被競爭對手的同類功能吸引。
- **確認**: ✅ 目標一致
  說明：經過三輪挑戰，團隊展示了他們如何嘗試將新功能與歷史學家定位對齊（例如透過使用限制和設計約束）。雖然仍存在潛在風險（功能可能演變為選股輔助工具），但團隊已承諾在實施過程中加強定位檢查。關鍵是D16的處理被納入計畫，這將改善架構並使未來功能更易於維護和對齊定位。因此，目前方案可以被視為與產品願望整體一致，前提是團隊嚴格執行他們的對齊聲明。

## 2026-06-18 主題: 檢討 (Round 13)

### Round 1
- **團隊方案**: 團隊提出6項新功能缺口（C63-C68），來源於競爭對手研究，包括Audio Market Story、Community Q&A、Company Story Game、Conversational Tone、Community-Curated Stock Stories和Financial Concept Storytelling。所有功能均聲稱與「歷史學家」定位、點對點知識建構、十秒測試和故事優先等對齊。
- **質疑**: 這些功能缺口是否真正符合我們的核心定位「歷史學家，而非選股工具」？例如：
  - C63（Audio Market Story）和C68（Financial Concept Storytelling）是否只是另一種形式的內容遞送，而非深入的公司歷史分析？
  - C64（Community Q&A）和C67（Community-Curated Stock Stories）是否會將焦點從結構化公司分析轉向社交閒聊和未經驗證的使用者觀點？
  - C65（Company Story Game）是否將教育內容簡化為遊戲機制，可能降低歷史學習的嚴肅性？
  - 是否有競爭對手缺失但我們應該補強的功能？例如，公司歷史深度時間線、多代業務演變分析或歷史決策案例庫？
  - 建議重新評估每項功能的歷史學價值：它是否幫助使用者理解公司過去的決策脈絡、業務演變或歷史事件影響，而非僅是娛別或社交互動？

### Round 2
- **團隊回應**: 團隊堅持這些功能缺口是必要的，原因是：(1) 競爭對手（特別是韓國Naver Finance、中國雪球、台灣Dcard和Reddit r/investing）正在使用社區驅動和多模式學習來吸引新手使用者；(2) 每項功能均經過對齊檢查，設計為服務於知識建構而非選股——音訊內容聚焦於過去市場事件敘述，社區功能限於歷史公司故事和財務概念解釋；(3) 音訊內容提供替代學習模式，滿足通勤學習需求；社區功能提供同儕學習，這在財務教育中被證明能提高留存率。
- **再次質疑**: 優先順序是否正確？具體質疑：
  - 在資源有限的情況下，是應該先投入開發C63-C68這些新功能，還是先完成Sprint 3的核心開發項目（C44、C41、C38、D16、D-025）？
  - 團隊是否考慮了C64-C67社區功能的審核成本？使用者產生的內容需要監督以防止錯誤資訊或投資建議。
  - C65遊戲化功能是否會分散使用者對核心公司分析的注意力？是否應該先鞏固基礎教育功能（C47、C50、C52）再考慮遊戲化？
  - 建議採用階段性方法：首先完成Sprint 3核心項目，然後在Sprint 4中試點C66對話式語調（低成本，高影響），最後在Sprint 5+根據結果決定是否實施其他功能。

### Round 3
- **最終方案**: 團隊在考慮挑戰後調整計畫：(1) 確認Sprint 3重點仍是完成C44、C41、C38、D16和D-025；(2) 接納C66（Conversational Tone）為Sprint 4的優先項目，因為其開發成本低（6-10h）且可立即改善使用者體驗；(3) 將C63（Audio Market Story）、C64（Community Q&A）、C65（Company Story Game）、C67（Community-Curated Stock Stories）和C68（Financial Concept Storytelling）列為Sprint 5+的評估項目，建議先進行原型驗證；(4) 團隊同意所有社區功能將包含嚴格的內容準則和審核機制，以確保歷史準確性並防止投資建議。
- **確認**: ✅ 目標一致
  說明：經過三輪挑戰，團隊展示了他們如何平衡創新與定位對齊。團隊承認Sprint 3的首要任務是完成已承諾的核心開發項目，同時識別出C66（Conversational Tone）為一個低風險、高影響力的改進，可在Sprint 4中實施。對於其他功能，團隊同意採用謹慎的階段性方法：先驗證核心假設（透過使用者研究和原型測試），再考慮大規模實施。關鍵保證包括：所有音訊內容將限於歷史市場事件敘述（類似The Indicator的模式）；所有社區功能將禁止買賣建議並聚焦於歷史公司故事；遊戲化元素將服務於教育目標而非取代它們。經過這些調整後，目前方案被視為與產品願望整體一致。

---

## 2026-06-19 主題: 討論 — Round 13 Feature Challenge (Revised PM Consolidation)

> **Context**: PM consolidated Architect, Designer, and Developer analyses into a revised sprint plan for C63-C68 with updated feature definitions and sprint placements (Sprint 6-8+). This is a NEW challenge addressing the revised plan, not a duplicate of the prior Round 13 entry above.

### Round 1 — Feature Direction Challenge

**Team Proposal**: Sprint 6: C66 (Conversational Tone, 13-20h) + C68 (Financial Concept Storytelling, P1, 30-44h). Sprint 7: C63 (Audio Market Story, 18-24h) + C65 (Company Story Game, 22-32h). Sprint 8+: C64 (Community Q&A, 26-38h) + C67 (Community-Curated Stock Stories, 26-38h, must follow C64).

**Challenges**:

1. **Scope inflation from sub-agent estimates to PM consolidation.** Developer estimated C66 at 7-12h, C68 at ~13h, C63 at 11-17h, C65 at 17-28.5h. PM's consolidated figures are significantly higher: C66 at 13-20h, C68 at 30-44h, C63 at 18-24h, C65 at 22-32h. The ~2x inflation on C68 (13h → 30-44h) needs justification. Is this including 20-30h of content creation? Content hours must be explicitly separated from engineering hours so they can be parallelized and owned by different team members.

2. **Sprint 6 overload risk.** C66 (13-20h) + C68 (30-44h) = 43-64h in one sprint. Sprint 5 is already 42-68h. If Sprint 5 slips, Sprint 6 inherits the delay AND must deliver a P1 feature. C68 should be split (5 concepts in Sprint 6, 5 in Sprint 7) to reduce single-sprint risk.

3. **C63 dependency chain is understated.** PM says C63 "depends on Sprint 4's market_data.py." This glosses over the much harder dependency: D28 (audio service layer for TTS generation) and content creation for 365 daily narrations/year. Neither D28 nor the audio content pipeline are in the 18-24h estimate explicitly.

4. **C65 redefinition from "Company Filing Explorer" to "Company Story Game" hasn't been technically validated.** Developer estimated the original C65 (Filing Explorer) at 17-28.5h with a HIGH risk data source blocker. The redefined "Company Story Game" at 22-32h is a completely different feature. Multiple-choice is Streamlit-feasible; drag-and-drop matching is not. What specifically makes this a "game" vs. "another multiple-choice quiz" like C64's quiz infrastructure?

5. **C64/C67 P0 positioning risks are NOT resolved by deferring to Sprint 8+.** Designer flagged both as P0 positioning risk. Architect flagged D22 (persistence layer) as a hard dependency. If D22 keeps getting deferred, both features are blocked indefinitely. What is the concrete plan to resolve D22?

6. **Missing daily engagement loop.** Architect's Round 14 analysis identified "daily engagement loop" as a P1 competitor gap. The current plan has no daily feature — C64 is redefined as Community Q&A (not daily), C63 is weekly audio at best. Where is the daily engagement hook?

### Round 2 — Priority Challenge

**Team Response**:
(1) Hour inflation reflects total cost of ownership including content creation, QA, and deployment — engineering hours remain close to developer estimates.
(2) C68 can be split into two phases (5+5 concepts) if Sprint 6 capacity is insufficient.
(3) D28 (audio service) is included in the 18-24h estimate as a prerequisite sub-task.
(4) C65 is specifically multiple-choice + sequencing via radio buttons — no custom JS. The "game" framing comes from narrative context per-company.
(5) Moderation strategy: C64 uses curated seed content + auto-flag keywords + single-moderator model. C67 defers until C64 proves the model works.
(6) C66 drives daily engagement through improved readability; a lightweight daily feature can be added in Sprint 7.

**Re-challenges**:

1. **Content creation needs a calendar, not just a bucket of hours.** C68 (10 concepts × 2-3h), C63 (audio scripts), C65 (game questions for 10 companies), C64 (seed Q&A) = 40-60h of content work across Sprints 6-8. Who creates this? If it's the same engineers, effective velocity drops drastically. Content creation must start NOW (Sprint 4) as a parallel workstream or Sprint 6 ships code with no content.

2. **C68 P1 priority is correct, but Sprint 6 timing assumes Sprints 3-5 complete on schedule.** Sprint 3 is still in progress. Sprint 4: 24-33h planned. Sprint 5: 42-68h planned. That's 66-101h before Sprint 6 begins. At ~20h/week, Sprint 6 starts week 5-6 from now. Meanwhile, P1 design issues (D-003 card inconsistency, D-005 page overload, D-006 mobile) remain. Why isn't C66 (improves ALL pages) fast-tracked into Sprint 3 spillover / Sprint 4 instead of waiting for Sprint 6?

3. **C65 estimate of 22-32h is a new figure that needs Developer validation.** The Developer estimated the *original* C65 (Filing Explorer) at 17-28.5h. The redefined Company Story Game at 22-32h hasn't been re-estimated by the Developer. Where did this number come from? Is the Developer on board?

4. **Sprint 7 sequencing: C63 (Audio) before C65 (Game) is backwards.** C63 depends on D28 — a completely new audio service layer the team has never built. C65 builds on existing quiz patterns. C65 should come first; C63 should move to Sprint 8+ when D28 is proven.

5. **C64/C67 "must follow C64" creates a D22 deadlock.** If D22 stays on the debt list indefinitely, both features are permanently blocked. D22 needs a concrete sprint commitment, not "Sprint 8+" which keeps receding.

### Round 3 — Goal Alignment Challenge

**Team Response**:
(1) C66 will be fast-tracked to late Sprint 3 / Sprint 4 as a parallel workstream (zero engineering dependency).
(2) C65 estimate of 22-32h was revised upward by the Developer after the reframe, accounting for session state management, company-specific game data preparation, and 50 question templates across 10 companies.
(3) Sprint 7 order reversed: C65 moves to Sprint 7, C63 moves to Sprint 8+ (D28 risk too high for Sprint 7).
(4) D22 is being promoted to Sprint 6 as a P0 prerequisite, unblocking C64/C67 for Sprint 8.
(5) C66 content creation (analogies for conversational tone) starts immediately as a parallel workstream.
(6) Content audit will cap total new content items; C63 will generate weekly (not daily) to limit content burden.

**Final Re-challenges**:

1. **Content sustainability is still the elephant in the room.** Even with weekly audio and 10 concepts, we're asking a small team to sustain hundreds of content items across 5 features. Zerodha Varsity (C68's closest analog) has 5+ full-time writers. We need an honest cap: recommend max 100 content items across all features until team capacity is proven.

2. **Historian tone protection needs a structural mechanism, not just good intentions.** The plan adds audio, games, community Q&A, and community stories — ALL of which can drift toward stock picking. C66 makes content MORE engaging, amplifying any tone drift. A mandatory "historian tone QA gate" must be added as a cross-cutting checkpoint before any content feature ships.

3. **Sprint-level cut-line rules needed.** The plan is viable ONLY if Sprints 3-5 complete on schedule. Explicit cut-line rules must be defined before Sprint 5: if Sprint 5 runs over, which features slide? If Sprint 6 runs over, C66 or C68 first?

**Confirmation**: ✅ **目標一致 — with conditions**

**Conditions**:
1. C66 fast-tracked to Sprint 3 late / Sprint 4 start (parallel workstream, zero dependency).
2. C63 (Audio) moved to Sprint 8+ (D28 risk too high for Sprint 7); C65 moved to Sprint 7.
3. D22 (persistence layer) promoted to Sprint 6 P0 prerequisite for C64/C67.
4. Content creation started as parallel workstream in Sprint 4 (not waiting until Sprint 6).
5. Content cap: max 100 new content items across all features until team capacity is proven. Prioritize C68 (10 concepts) and C65 (50 questions). C63: weekly only (52/year, not 365).
6. Mandatory historian tone QA gate before any content feature ships.
7. Sprint 5/6 cut-line rules defined before Sprint 5 starts.

**Alignment Basis**: After 3 rounds, the team addressed sequencing risks (C63→Sprint 8+, C65→Sprint 7, D22→Sprint 6), content bottlenecks (parallel workstream from Sprint 4), and positioning risks (tone QA gate). The core "historian" vision is preserved: C66 + C68 form the "story core," C65 adds engagement via existing patterns, and community features (C64/C67) are properly gated behind infrastructure and moderation readiness. The plan is ambitious but achievable IF all 7 conditions are met.

---

*This challenge record was created by the Challenger during the Round 13 (Revised) discussion cycle. 2026-06-19.*

---

## 2026-06-14 Theme: Sprint 21 Planning — Challenger Analysis

> **Context**: Sprint 20 is in progress (C167 ✅ done, C163 + C40 pending). The PM has formed a "team preliminary decision" for Sprint 21: Option A (P1 Focus) with D-120 + C170 + C152 + C171(stretch). This challenge stress-tests that plan through 3 rounds of rigorous questioning.
>
> **Team Preliminary Decision (Option A: P1 Focus)**:
> | Order | Task | Estimate | Running Total |
> |-------|------|----------|---------------|
> | 1 | D-120: Benchmark extraction (INDUSTRY_BENCHMARKS from 3 files → YAML + shared service) | 1.5-2.5h | 1.5-2.5h |
> | 2 | C170: Tappable Glossary (inline metric definitions, reuses _glossary_tooltip from _router_base.py) | 8-12h | 9.5-14.5h |
> | 3 | C152: Multi-Factor Event Narratives (NarrativeExplanationProvider extending ExplanationProvider protocol) | 18-24h | 27.5-38.5h |
> | 4 | C171: Valuation Band Chart (stretch goal) | 10-14h | 37.5-52.5h |

---

### Round 1: Feature Direction Challenge

#### Challenge 1.1 — Is C152 really ready for implementation?

C152 has been deferred twice: first as a spike in Sprint 19 (deferred to Sprint 20), then as a swap condition in Sprint 20 (not triggered). Now it's the centerpiece of Sprint 21. The Developer flagged C152's scope creep as the **#1 risk** — multi-factor narrative is inherently open-ended. The Designer's own review rates C152 as "highest-risk feature for advice perception" with a **🔴 CRITICAL** severity on the advice-perception risk.

The core question: **Does the team have a concrete, bounded definition of what "multi-factor narrative" means in practice?** The Designer's spec says "≥2 significant events within 30-day window" — but the Developer's estimate of 14-18h includes "designing ~10-15 multi-factor narrative templates in YAML (~4h)" and "the composition service that picks the right template based on event combination (~4h)." This is not spike work; this is full implementation of an open-ended template design problem.

**Specific questions for the team:**
1. How many multi-factor combinations will be supported in Sprint 21? Is there a hard cap (e.g., 8 combinations) or is it "as many as we can build"?
2. What happens when the system encounters a combination that doesn't have a template? Is there a graceful degradation path?
3. Has the team pre-written and tone-audited even ONE multi-factor narrative template? If not, how can the estimate be 18-24h?
4. The Designer flagged "false causality" as a 🟡 MEDIUM risk — using "同時發生" (occurred simultaneously) framing instead of "因為...所以..." (because...therefore...). Has this framing been validated? Are there example templates that demonstrate this?

**Recommended team response:** The team should commit to a **hard cap of 8 multi-factor narrative templates** for Sprint 21, covering the most common event combinations (revenue+price, revenue+institutional, product+price, etc.). All 8 templates must be pre-written and tone-audited BEFORE Sprint 21 coding begins. If templates aren't ready, C152 scope reduces to 5 templates and the effort drops to 12-15h.

#### Challenge 1.2 — Is C170 truly P1, or is it infrastructure masquerading as a feature?

C170 (Tappable Glossary) closes D-012 — the oldest P2 gap, open since Round 9. The Designer's analysis is honest: "Investopedia has 10,000+ term glossary. Stock Explorer's analogy engine provides explanations but only in card format, not as hover tooltips." The question is whether a 50-100 entry glossary can compete with Investopedia's 10K+ terms.

But this question misses the point. C170 isn't trying to compete with Investopedia's encyclopedia — it's trying to provide **inline, contextual definitions** for the specific metrics shown on Stock Explorer pages. This is a fundamentally different use case. Investopedia requires you to leave the page; C170 brings the definition to you.

**The real question is about scope and approach:**
1. The estimate is 8-12h. The Developer's original estimate for C170 was 6-10h. Where did the extra 2-2h come from?
2. The description says "reuses _glossary_tooltip from _router_base.py" — but looking at the codebase, `_glossary_tooltip` exists as a component. Does C170 need to build a new service layer, or is it primarily a UI integration task?
3. How many terms will be in the glossary at launch? 50? 100? Is there a content creation plan?
4. The Designer noted that C170 "enables C152" — narrative quality improves when terms are defined. If this is true, shouldn't C170 come BEFORE C152 in the sprint order?

**Recommended team response:** The team should clarify that C170 is a **UI integration + content creation** task, not a new service. The 8-12h estimate should be broken down: 3-4h for UI integration (wrapping metric displays with tooltip components), 5-8h for content creation (writing 50-80 glossary entries). Content creation should start NOW (parallel with Sprint 20 C163/C40) so that C170 ships with substantive content, not an empty tooltip shell.

#### Challenge 1.3 — Should D-120 really be bundled with Sprint 21?

D-120 (benchmark extraction) has been open since Round 38 — that's **3 sprints** of deferral. The Architect's review says "Do in Sprint 20 alongside C163" — but Sprint 20 is now in progress with C163 and C40 as the remaining items. D-120 was not included in Sprint 20.

The question: **Why is D-120 in Sprint 21 instead of being done as Sprint 20 infrastructure?** The Developer flagged "D-120 regression risk (extracting from 3 files)" — this is a known, bounded task that should have been done already. Every sprint it's deferred, the risk of the 3 duplicated dicts diverging increases.

**Specific questions:**
1. What is the concrete risk of extracting INDUSTRY_BENCHMARKS from 3 files? The Architect says 1-2h. The PM's estimate says 1.5-2.5h. Is there a technical reason this can't be done in 1.5h?
2. If D-120 is truly a Day 1 prerequisite, why wasn't it done in Sprint 20? The team had 30-42h capacity and used it on C167+C163+C40. Was D-120 considered and rejected, or simply not considered?
3. Does D-120 need to be done before C170 or C152? If not, why is it ordered first?

**Recommended team response:** D-120 should be a **Day 0 prerequisite** — done before any Sprint 21 feature work begins. It should take 1.5-2.5h and is pure infrastructure. The team should commit to completing D-120 before C170 or C152 development starts. If D-120 reveals that the 3 dicts have diverged, the reconciliation work should be included in the 1.5-2.5h estimate.

#### Challenge 1.4 — Are we overlooking C163/C40 carry-over risk?

Sprint 20 has C163 (Learn First Gate, 10-14h) and C40 (Beginner/Expert Mode, 8-12h) pending. The Sprint 20 total is 30-42h, and C167 took ~14h, leaving 16-28h for C163+C40. This is tight but feasible.

**The risk:** If C163 or C40 aren't completed in Sprint 20, they carry over into Sprint 21, displacing Sprint 21 features. The Developer flagged this explicitly: "C163/C40 carry-over risk from Sprint 20."

**Specific questions:**
1. What is the current status of C163 and C40? Are they on track for Sprint 20 completion?
2. If C163 carries over, does it displace C170 or C152 in Sprint 21?
3. If C40 carries over, does it displace C171 (stretch) or C152?
4. Is there a contingency plan for Sprint 21 if both C163 and C40 carry over?

**Recommended team response:** The team should define a **Sprint 20 cut-line rule** before Sprint 21 planning is finalized: if C163 is not done by Sprint 20 close, C170 is dropped from Sprint 21 and C163 takes its place. If C40 is not done, C171 (stretch) is dropped and C40 takes its place. C152 is non-negotiable as the Sprint 21 centerpiece.

---

### Round 2: Priority Challenge

#### Challenge 2.1 — Should C170 come before C152?

The current order is: D-120 → C170 → C152 → C171(stretch). But the Designer explicitly noted that C170 "enables C152" — narrative quality improves when terms are defined. The Developer's analysis confirms: C152's multi-factor narratives will reference financial metrics, and having inline glossary definitions will make those narratives more useful to beginners.

**The argument for C170 before C152:**
- Lower risk (8-12h vs 18-24h)
- Enables C152's narrative quality
- Closes D-012 (oldest P2 gap, open since Round 9)
- Can be done in parallel with C152's template pre-work

**The argument against:**
- C152 is the strategic centerpiece; it should get the team's full attention first
- C170 and C152 are independent; C152 doesn't technically depend on C170

**Recommended team response:** The current order (C170 before C152) is **correct** but for the wrong reasons. It's not because C170 "enables" C152 technically — it's because C170 is lower risk and should be completed first to reduce the number of open workstreams when the team focuses on C152's complex template work. The team should explicitly state: **C170 is done first to clear the deck for C152 focus.**

#### Challenge 2.2 — Is C171 the right stretch goal, or should C172 be prioritized?

The PM chose C171 (Valuation Band Chart, 10-14h) as the stretch goal. But C172 (Concept Comparison Tool, 10-14h) has higher educational value — it directly serves the "point-to-point knowledge construction" core value. The Designer's analysis shows that Magnify.money's concept comparison is a key differentiator.

**Comparing the two:**
- C171 (Valuation Band Chart): Visual, single-stock, extends existing valuation infrastructure. Lower educational value — it shows "where is this stock's P/E historically" but doesn't teach concepts.
- C172 (Concept Comparison): Educational, multi-concept, teaches relationships between financial concepts. Higher educational value — it teaches "what's the difference between ROE and ROA" with real TW stock examples.

**The problem with C171 as stretch:** If the team has 10-14h of stretch capacity, spending it on a single-stock chart (C171) instead of an educational tool (C172) is a missed opportunity. The "historian" positioning is about education, not visualization for its own sake.

**Recommended team response:** The team should **swap C171 for C172** as the stretch goal. C172 better serves the historian positioning and has higher educational value. If the team insists on C171, they should justify it with a specific user story: "As a beginner, I want to see where TSMC's P/E has been historically so I can understand if it's expensive relative to its own history."

#### Challenge 2.3 — Is the Sprint 20 → Sprint 21 transition clean?

The Sprint 21 plan assumes Sprint 20 completes cleanly with C167+C163+C40. But the Developer flagged "C163/C40 carry-over risk from Sprint 20." If either carries over, the Sprint 21 plan is disrupted.

**Specific questions:**
1. What is the definition of "done" for C163 and C40? Do they need to be fully tested and merged, or is "feature complete with known issues" acceptable?
2. If C163 carries over, what is the Sprint 21 contingency plan?
3. If C40 carries over, what is the Sprint 21 contingency plan?
4. Is there a Sprint 20 retrospective before Sprint 21 planning is finalized?

**Recommended team response:** The team should define **explicit Sprint 20 exit criteria** before Sprint 21 begins:
- C163: "Done" = gate UI implemented, 3+ educational cards written, session state tracking working, L0 passing
- C40: "Done" = toggle renamed, settings persistence working, 3+ sections with complexity variants, L0 passing
- If either doesn't meet exit criteria, the incomplete feature carries over and displaces the lowest-priority Sprint 21 item (C171 stretch first, then C170).

#### Challenge 2.4 — Why is D-120 ordered first instead of being a prerequisite?

The PM's plan lists D-120 as "Day 1 prerequisite" but also as the first item in the sprint. This is contradictory — a prerequisite should be done before the sprint starts, not as the first item.

**Recommended team response:** D-120 should be reclassified as a **Sprint 20 spillover task** or a **pre-Sprint 21 infrastructure task** that must be completed before any feature work begins. It should not consume Sprint 21 capacity. If it does, the effective Sprint 21 capacity for features is 27.5-38.5h minus 1.5-2.5h = 26-36h, which is below the proven 30-42h capacity.

---

### Round 3: Goal Alignment Challenge

#### Challenge 3.1 — Does C152 truly serve beginners, or does it serve intermediate users?

The product vision defines the target user as a **beginner** who needs explanations. But C152 (Multi-Factor Event Narratives) is a sophisticated feature that combines multiple events into a coherent story. The Designer's own analysis says: "This is the feature that transforms Stock Explorer from 'data display with explanations' to 'historian that tells stories.'"

**The tension:** A beginner who doesn't understand individual events won't benefit from a narrative that combines those events. C152 assumes the user already understands what each event means — it just connects the dots. This is an **intermediate user** feature, not a beginner feature.

**Specific questions:**
1. Has the team validated that beginners want multi-factor narratives, or is this an assumption?
2. What percentage of Stock Explorer users are beginners vs. intermediate? (If this data doesn't exist, how does the team know?)
3. Is C152 the right feature for Sprint 21, or should the team focus on more beginner-centric features like C170 (glossary) and C172 (concept comparison)?
4. The Designer's ten-second test for C152: "最近有幾件重要的事同時發生，我們可以繼續觀察。" — Can a true beginner restate this? Or do they need to understand what "重要的事" means first?

**Recommended team response:** The team should acknowledge that C152 is an **intermediate feature** that builds on beginner infrastructure (C170 glossary, C163 onboarding). This is acceptable IF the beginner infrastructure is in place. The team should confirm: C170 (glossary) must be completed before or alongside C152, not after. If C170 is deferred, C152 should also be deferred.

#### Challenge 3.2 — Does the "historian" positioning support narrative synthesis or only single-event explanation?

The product vision says "explain what happened" — this is single-event explanation. C152 goes further: it **synthesizes** multiple events into a narrative. This is a different capability.

**The question:** Does the "historian" positioning support synthesis, or does it only support explaining individual events? A historian who only explains individual events is a chronicler. A historian who synthesizes multiple events into a narrative is an analyst. These are different roles.

**Specific questions:**
1. Has the team explicitly decided that "historian" includes synthesis, or is this an assumption?
2. If "historian" includes synthesis, what are the boundaries? Where does synthesis end and prediction begin?
3. The Designer flagged "false causality" as a risk — combining events implies they're related. How does the team prevent synthesis from becoming causal analysis?
4. Is there a competitor who does synthesis well without crossing into prediction? (Public.com's story cards are the closest, but they're AI-generated and less controlled.)

**Recommended team response:** The team should define a **"historian synthesis boundary"** document that explicitly states:
- Synthesis describes what happened (past tense)
- Synthesis does not predict what will happen (no future tense)
- Synthesis uses "同時發生" (occurred simultaneously) framing, not "因為...所以..." (because...therefore...) framing
- Synthesis includes a mandatory historian disclaimer
- All synthesis templates must pass tone QA before implementation

This document should be written BEFORE C152 implementation begins.

#### Challenge 3.3 — Are we building for the "ten-second test" or for feature completeness?

The "ten-second test" is a core design principle: a beginner can restate the core concept within 10 seconds. The Sprint 21 plan includes:
- D-120: Infrastructure (no direct user impact)
- C170: Glossary (supports ten-second test by defining terms)
- C152: Multi-factor narratives (may or may not support ten-second test — see Challenge 3.1)
- C171: Valuation chart (visual, supports ten-second test IF the chart is simple enough)

**The question:** Is the Sprint 21 plan optimized for the ten-second test, or is it optimized for feature completeness (checking off backlog items)?

**Specific questions:**
1. Which Sprint 21 features directly pass the ten-second test? (C170 yes, C152 uncertain, C171 maybe, D-120 no)
2. If the goal is ten-second test compliance, should C172 (concept comparison) replace C171 (stretch)?
3. Should the team conduct a ten-second test audit of the event dashboard BEFORE building C152, to ensure the foundation is solid?

**Recommended team response:** The team should conduct a **ten-second test audit** of the event dashboard before C152 implementation. If users can't restate individual event explanations in 10 seconds, adding multi-factor narratives won't help. The audit should be done with 3-5 beginner users (or simulated by the team) and results documented.

#### Challenge 3.4 — What does "Sprint 21 success" look like? How do we measure it?

The Sprint 21 plan has no success metrics. It has feature descriptions and estimates, but no definition of "done" beyond "features are built."

**Specific questions:**
1. What is the minimum viable Sprint 21? (D-120 + C170 only? D-120 + C170 + C152?)
2. What is the stretch Sprint 21? (All 4 items including C171?)
3. How will the team measure C152's success? (User testing? Template coverage? Tone QA pass rate?)
4. How will the team measure C170's success? (Number of glossary entries? Tooltip click-through rate?)
5. Is there a post-Sprint 21 user research plan to validate that the features work for beginners?

**Recommended team response:** The team should define **Sprint 21 success criteria** before development begins:
- **Minimum success:** D-120 complete, C170 live with 50+ glossary entries, C152 spike validated with 5 pre-written templates
- **Target success:** All of the above + C152 live with 8 multi-factor templates, all passing tone QA
- **Stretch success:** All of the above + C171 live with plain-language interpretation
- **Measurement:** L0 passing (125/125), tone QA pass rate (100% of new templates), ten-second test audit (C152 narrative restatable by beginners)

---

### Final Verdict

✅ **CONFIRMED — with 8 binding conditions**

The Sprint 21 plan (Option A: P1 Focus) is confirmed as a reasonable direction, but the team must address significant risks around C152 readiness, C163/C40 carry-over, and goal alignment. The plan is ambitious but achievable IF all 8 conditions are met.

#### Binding Conditions

1. **C152 template cap:** Maximum 8 multi-factor narrative templates in Sprint 21. All 8 must be pre-written and tone-audited BEFORE coding begins. If templates aren't ready by Sprint 21 Day 1, C152 scope reduces to 5 templates (12-15h).

2. **C170 before C152:** C170 (Tappable Glossary) must be completed before C152 implementation begins. C170 content creation (50-80 glossary entries) starts NOW as a parallel workstream during Sprint 20.

3. **D-120 as prerequisite:** D-120 (benchmark extraction) must be completed as a pre-Sprint 21 infrastructure task, not consuming Sprint 21 feature capacity. If D-120 reveals dict divergence, reconciliation is included in the 1.5-2.5h.

4. **Sprint 20 cut-line rule:** Before Sprint 21 begins, define explicit Sprint 20 exit criteria for C163 and C40. If either carries over, it displaces the lowest-priority Sprint 21 item (C171 stretch first, then C170). C152 is non-negotiable.

5. **C172 replaces C171 as stretch:** C172 (Concept Comparison) should replace C171 (Valuation Band Chart) as the stretch goal. C172 has higher educational value and better serves the historian positioning. If the team insists on C171, a specific beginner-facing user story must be provided.

6. **Historian synthesis boundary document:** Before C152 implementation, write a "historian synthesis boundary" document that defines: past-tense only, "同時發生" framing (not "因為...所以..."), mandatory disclaimer, tone QA pre-audit requirement for all templates.

7. **Ten-second test audit:** Conduct a ten-second test audit of the event dashboard BEFORE C152 implementation. If users can't restate individual event explanations in 10 seconds, fix the foundation before adding multi-factor narratives.

8. **Sprint 21 success criteria:** Define minimum/target/stretch success criteria before development begins (see Challenge 3.4). Measure: L0 passing, tone QA pass rate, ten-second test audit results.

#### Summary of Changes from Preliminary Decision

| Aspect | Preliminary Decision | Post-Challenge Decision |
|--------|---------------------|------------------------|
| C152 scope | 18-24h, open-ended | **18-24h with hard cap of 8 templates, pre-audited** |
| C170 timing | After D-120, before C152 | **Content creation starts NOW (parallel with Sprint 20)** |
| D-120 positioning | Sprint 21 item #1 | **Pre-Sprint 21 prerequisite (0h sprint cost)** |
| Stretch goal | C171 (Valuation Band) | **C172 (Concept Comparison) — higher educational value** |
| Carry-over risk | Not addressed | **Explicit cut-line rule: C163/C40 carry-over displaces C171→C170** |
| Success metrics | Not defined | **Minimum/target/stretch criteria with L0 + tone QA + ten-second test** |
| Historian boundary | Not defined | **Synthesis boundary document required before C152 coding** |
| Ten-second test | Not addressed | **Event dashboard audit before C152 implementation** |

#### Alignment Basis

After 3 rounds of challenge, the Sprint 21 plan is confirmed as directionally correct: C152 is the right centerpiece feature for defending the "historian" positioning against StockStory and Stockopedia AI. C170 is the right supporting feature (enables C152, closes oldest P2 gap). D-120 is the right infrastructure task (overdue, blocking future features).

The key risks are: (a) C152 scope creep (mitigated by template cap + pre-audit), (b) C163/C40 carry-over (mitigated by cut-line rule), (c) beginner alignment (mitigated by ten-second test audit + C170 before C152), and (d) synthesis boundary (mitigated by historian boundary document).

The plan is ambitious but achievable IF all 8 conditions are met. If conditions 1, 4, or 6 are not met, the plan should be reconsidered.

---

*This challenge record was created by the Challenger during the Sprint 21 planning cycle. 2026-06-14.*

---

## 2026-06-18 Theme: Review — Round 28

### Round 1
- **Team proposal**: 4 new feature gaps (C123-C126): Revenue Geography, Moat Types, Segment Profitability, Moat Comparison. All deferred to Sprint 14+. Sprint 13b focuses on C36 Revenue Tree + C46 Moat Analysis.
- **Challenge**: (1) C123 has uncertain data availability for TW stocks. (2) C124 (Moat Type Classification) is essentially already baked into C46's planned design — deferring it creates an incomplete feature. (3) C125 depends on C123's data sourcing. (4) C126 requires C46 scoring to be comparison-ready from day one. (5) No TW-competitor validation done. (6) Sprint 13b may be incorrectly prioritized over P1 backlog items (C42 Stock Screener, C119 Onboarding).

### Round 2
- **Team response**: C36 is low-risk enhancement; C46 is new but architecturally prepared. D-079 must be fixed before adding tooltips. D-080 can be fixed during Sprint 13b.
- **Re-challenge**: (1) 2-3h pre-work for C46 is likely insufficient — recommend 4-5h with dimension alignment. (2) D-079 must be Day 0, not concurrent. (3) D-080 should be coupled with C46's card work. (4) No content creation budget allocated for C46 despite 40% rule for education features. (5) No go/no-go gate between C36 and C46.

### Round 3
- **Team response**: C46 will use evidence-first (historian) design with disclaimer. Moat types from C124 will be included. Content will be budgeted.
- **Confirmation**: ✅ Aligned — with 6 conditions:
  1. C46 must be evidence-first (not rating-first) to avoid stock-picking drift
  2. C124 must be merged into C46's Sprint 13b scope — not deferred
  3. C46 scoring rubric must be comparison-ready for C126 in Sprint 14
  4. C123 needs TW-competitor validation before Sprint 14 commitment
  5. Content creation must be explicitly budgeted at 40% for C46
  6. D-079 must be a Day 0 prerequisite before any Sprint 13b tooltip work
