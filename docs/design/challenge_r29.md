## 2026-06-13 Challenge Log — Sprint 14 Scope (Round 29)

### Team Preliminary Decision

**Option C: "Quick Wins + Infrastructure" Sprint**

| Feature | Effort | Status |
|---------|--------|--------|
| C126 Moat Comparison | 10-14h | Include |
| C40 Mode Toggle Propagation | 4-6h | Include |
| C47 Education Academy Spike (3-5 lesson prototype) | 10-12h | Include |

**Defer:**
- C123 Revenue Geography (data blocker — no FinMind API)
- C125 Segment Profitability (lower priority)

**Total effort: 24-32h** (within 26-38h budget)

**Team Rationale:** Delivers immediate user value (C126), completes existing work (C40), establishes education infrastructure without over-committing on content creation (C47 spike). C123/C125 deferred for data availability reasons, not technical complexity.

---

### Round 1: Feature Direction Challenge

**Challenges:**

1. **C126 Moat Comparison — "All infrastructure exists" oversimplification:**
   The architect claims all infrastructure exists because C46 is complete and `moat_data.yaml` has 20 stocks. However, the **comparison view** is a fundamentally different UX problem than single-company display. C46 was designed for *individual company storytelling* ("台積電的護城河"). C126 requires *cross-company normalization* — ensuring scores from the same scoring function render comparably side-by-side. The designer specifies a grouped horizontal bar chart (not radar), but the existing `moat_analyzer.py` service returns structured summaries, not comparison-optimized data. The architect estimates 10-14h assuming "View-layer addition only," but the developer's estimate is 14-24h — a 100% discrepancy on the upper bound. Which is more realistic? If the service layer needs refactoring to support comparison output, this estimate is understated.

2. **C47 Education Academy Spike — Spike vs. Feature ambiguity:**
   The team calls this a "spike" but allocates 10-12h (half the sprint budget for this feature alone). A spike is typically a time-boxed experiment — yet 10-12h with "3-5 lesson prototype" sounds like a mini-feature, not a spike. The designer recommends 2 lessons for Phase 0; the architect says 5-8 MVP; the developer says 3-5 prototype. Which is it? This scope ambiguity risks scope creep during execution. Furthermore, a 3-5 lesson prototype that is deployed to users creates an **expectation of completion** — users who see 3 lessons in the nav will expect more. The product vision calls for education orientation, but a half-built academy may frustrate more than having none. Is the right approach to build 5 *complete* lessons (done properly) rather than a prototype that ships a broken experience?

3. **C125 Segment Profitability deferral — natural extension of C36:**
   The designer's own recommendation (line 245) states: *"C125 Segment Profitability should be bundled with C36 in Sprint 14."* The designer ranks it #2 in priority, higher than C126 (#3). Yet the team plan defers it. The designer calls it a "2-3h of additional work" toggle enhancement to C36 — yet the developer estimates 12-22h (which includes 4-6h for content curation). The core engineering (a margin overlay toggle on the existing treemap) is genuinely small. The data curation is the bottleneck, but **C126 also requires content curation** (4-6h for comparison explanations for 10-15 stock pairs). Both features have content creation needs, yet only C125 is deferred for being "content heavy." Why is C126's content burden acceptable but C125's isn't?

4. **C40 Mode Toggle Propagation — deceptively simple:**
   The architect says 4-6h with "no new modules needed," and the developer confirms 0h base + 4-6h for propagation. But the designer reveals significant complexity: the propagation requires defining what "Beginner Mode" means on *every single page* (Business Card, Peer Comparison, Financial Health, Operational Checkup, Group Structure, Education Academy). That's 6 pages × content decisions + UI changes. The designer's spec alone is the most detailed of any feature (lines 70-108). Is 4-6h realistic when content decisions per page are non-trivial? And critically, the designer says *"Remove C105 toggle when C40 is implemented"* — this is a **breaking change** to existing behavior. What if C105's page-level toggle is being used by current users?

5. **Alignment with product vision — "historian, not stock picker":**
   The product vision's core values are (1) Story first, data second, (2) PPT-style presentation, (3) Benchmark-oriented analysis, (4) Point-to-point knowledge construction. C126 directly serves value #3 (benchmark-oriented analysis). C40 serves #2 (PPT-style simplification). But C47 serves none directly — it's a platform play, not a historian play. The vision says "Historian, not a stock picker" and "curious observers who want to know how companies around them make money." A structured learning path about abstract financial concepts (Module 1: What is P/E?) serves a different audience than the target user who wants to understand *specific companies*. Is C47 the right strategic direction for Sprint 14, or does it dilute the "historian" positioning by turning the product into a generic finance education platform?

**Team Response:**

1. **C126 discrepancy resolved:** The developer's 14-24h estimate is *total* (including service extensions + view + curation + integration). The architect's 10-14h is for the *comparison page itself*. The ~2h service extension (`moat_analyzer.py` comparison wrapper) + ~8-9h view layer + ~4h curation + ~2h integration = ~14-20h total from developer, which aligns with architect's upper bound when the service extension is accounted for. The real estimate is **10-14h for the comparison feature** assuming service layer minor extension. The 14-24h upper bound assumes significant refactoring, which is unlikely if C46 was built comparison-ready (as Challenge Log R2 required).

2. **C7 scope defined:** The "spike" is scoped at **5 complete lessons** (not 3, not 8). This is the MVP. The lessons will use existing `glossary_service.py` for term definitions and `quiz_engine.py` for quizzes. Content will be sourced from existing analogy patterns. The term "spike" refers to *architectural validation* — we're testing the YAML schema, progress tracking pattern, and page layout — not doing throwaway research. Done properly, 5 curriculum-quality lessons × 2h content each = 10h content + ~2h engineering = **12h total**. This is a *feature*, not a spike.

3. **C125 vs C126 content burden:** Accepted — C125 should be included if C126 content is acceptable. The real differentiator is that C126 extends C46 (the most recent completion) and supports the "benchmark-oriented analysis" core value. C125 extends C36 (one sprint older). Both deserve inclusion, but C125's data is inconsistently available across stocks (only ~10-15 of 20 have segment data), requiring fallback UI. **Recommend:** Include C15 as a "stretch goal" if C126 and C40 complete early.

4. **C40 propagation complexity:** The 4-6h estimate assumes content decisions are *already made* (per designer's spec). The designer has thoroughly spec'd what each page shows in beginner mode. Engineering is just adding `if not simple_mode` guards to sections on 5 pages. Each page takes ~45-90min. Total: 5 pages × 1h = 5h. The C105 removal is a net simplification (removing a toggle from the business card, replacing it with a navbar toggle).

5. **C47 alignment with vision:** Valid concern. C47 *as structured learning of abstract concepts* would dilute the historian positioning. However, C47 as *"understanding through company examples"* (each lesson anchored to a real TW stock, showing how TSMC demonstrates ROE, how Uni-President demonstrates brand moat) directly serves the "story first, data second" principle. The designer's spec emphasizes TW stock examples in every lesson. This alignment is maintained if lessons are example-first, abstract-second. **Condition:** Every lesson must lead with a TW stock example, not a definition.

---

### Round 2: Priority Challenge

**Challenges:**

1. **C40 Mode Toggle should be first — all three roles agree, but team plan lists it second:**
   The designer explicitly recommends (line 243): *"C40 Mode Toggle should be the first feature implemented. It is the lowest-risk, highest-leverage feature."* The architect lists it second (after C126). The developer doesn't specify order. The designer's logic is compelling: once C40 propagation exists, every other feature *and* the existing Business Card page gets a free "Beginner Mode" that reduces cognitive load. Building C126 without C40 means users see a complex moat comparison page that has no beginner-friendly view. The execution order should be **C40 → C126 → C47**, because C40 unblocks better UX for C126 and C47. Is there a reason to do C126 first?

2. **Is C47 Education Academy the right time for a 12h investment?**
   The Sprint 14 budget is 26-38h. C47 spike alone is 10-12h (up to 46% of minimum sprint budget). The product is at a stage where the Business Card page has 15+ sections and D-005 (page overload) is an increasing problem flagged since Round 9. C40 directly addresses D-005. C126 extends the moat story. Both deliver coherent incremental value. C47, however, adds a **new navigation paradigm** (education mode vs. stock mode) that the designer admits requires a "conscious exception" to Zone B rules and a visual mode indicator. This is the biggest architectural change since the original Business Card page. Investing 12h in education *infrastructure* (navigation exceptions, progress tracking, YAML schema) while the existing page has unresolved overload issues — is this the right priority?

3. **Budget math doesn't work at the pessimistic edge:**
   The team says 24-32h within 26-38h budget. But the *upper bound is 32h for 3 features*. That leaves only 6h for bug fixes, PR reviews, testing, design QA, and the inevitable unexpected issues. With C47 being the first new page type (education), QA effort will be non-trivial. At the pessimistic edge (C126: 14h + C40: 6h + C47: 12h = 32h), there's almost no buffer. Compare with Option B from the architect (C125 + C126 + C40 = 24-30h with lower risk). Does the team have confidence that 32h is a realistic upper bound?

4. **C125 deferral vs. C17 spike — inconsistent criteria:**
   C125 is deferred for being "lower priority" despite the designer ranking it #2 and calling it a 2-3h bundling opportunity with C36. C47 is included despite being a 12h infrastructure investment with higher content risk. The difference is *strategic positioning* — education differentiates from competitors. But this strategic argument isn't made explicitly. It should be: "We include C47 not because it's quick, but because education is our long-term moat." Is the team making this strategic tradeoff explicitly?

5. **Competitor analysis gap for C126:**
   The designer notes that Stockopedia has moat comparison (radar chart) and Morningstar has moat ratings but no multi-company view. But what about TW-specific competitors? 財報狗 (Cat Dog Finance) is the dominant TW retail investment platform — does it have moat comparison? If 財報狗 doesn't have it, C126 is a genuine differentiator. If it does, we need to differentiate our approach. The team hasn't addressed the TW competitor landscape for this specific feature.

**Team Response:**

1. **Execution order revised:** C40 propagation → C126 → C47. The designer is correct that C40 should come first. It's the smallest feature (4-6h), establishes the beginner/expert paradigm that C126 and C47 benefit from, and completing it first de-risks the rest of the sprint. C40 done first means C126's comparison page can include a beginner mode (simplified view showing only "wide/narrow/none" labels instead of full 5-dimension breakdown).

2. **C47 timing accepted:** Including C47 in Sprint 14 is a deliberate strategic investment. The "15+ section overload" on Business Card (D-005) is actually an *argument for* C47, not against it — because C47 provides an alternative navigation path that doesn't add to the Business Card page. Users who want education go to the Academy. Users who want stock analysis stay on the Business Card. C40 then solves the overload for the Business Card users. Together, C40 + C47 address D-005 through *navigation relief* (C47 moves traffic to a separate page) and *simplification* (C40 reduces Business Card density).

3. **Budget buffer analysis:** The pessimistic 32h case is tight but manageable. The developer's Option C (same scope) estimated 28-40h with "feasible" rating. The most realistic case is C126: 12h + C40: 5h + C47: 11h = 28h, leaving 10h buffer in a 38h sprint. The 32h upper bound is a true worst case. The go/no-go gate after C40+C126 (first ~17h) protects against overrun on C47. If after 17h the sprint is on track, C47 proceeds. If not, C47 is reduced to 5 lessons → 2 lessons, still creating a deployable education page skeleton.

4. **Strategic tradeoff made explicit:** Yes. The team prioritizes C47 (education infrastructure) over C125 (segment profitability) because: (a) Education aligns with the "education-oriented, not tool-oriented" differentiator in the product vision. (b) C47 navigating users *away* from the overloaded Business Card is architecturally healthier than C125 which adds another toggle to the already-dense Business Card. (c) C125 can be grafted onto C36 in any future sprint (2-3h enhancement), while C47 requires a full sprint grounding.

5. **Competitor landscape:** No TW competitor (財報狗, CMoney, Yahoo股市) offers structured moat comparison. Morningstar has moat ratings but no side-by-side comparison view and no TW stock coverage. Stockopedia has comparison but only UK stocks. **C126 is a genuine white space in the TW market.** The grouped horizontal bar chart approach differentiates from radar charts used by Stockopedia.

---

### Round 3: Goal Alignment Challenge

**Challenges:**

1. **Contradiction between designer's priority ranking and team scope:**
   Designer ranks: C40 (#1) > C125 (#2) > C126 (#3) > C123 (#4) > C47 (#5). Yet the team selects C126 + C40 + C47. The designer explicitly says C125 should be bundled in Sprint 14 (line 245) and C47 should be "Phase 0 only: skeleton + 2 lessons" (line 271) — not a full 3-5 lesson prototype. The team's scope contradicts the designer's explicit recommendation on C47 scope. Is the team overriding the designer's judgment about design consistency risk?

2. **C47 lessons — quality vs. quantity risk:**
   The product vision demands "high-quality plain-language explanations" that pass the ten-second test. Writing curriculum-quality financial lessons that anchor abstract concepts in real TW stock examples is a specialized skill. The team allocates 10h for content creation (5 lessons × 2h each). Investopedia Academy's lessons took weeks per module by professional financial educators. Can the team produce 5 curriculum-quality lessons that meet the ten-second test standard in 10h? If not, the academy launches with subpar content that *damages* the education brand promise. Is there a quality gate?

3. **Session state fragility for both C40 and C47:**
   Both C40 (mode toggle) and C47 (progress tracking) use `session_state`, which is ephemeral — lost on page navigation or browser refresh. For C40, this means a user who sets Expert mode gets reset to Beginner on reload. For C47, this means quiz progress is lost if the user accidentally closes the tab. The architect accepts this for MVP (line 160), but for a learning platform, losing progress is a **critical UX failure**. Users will not return to a platform that doesn't remember them. Is session_state-only truly acceptable for C47?

4. **D-005 (Business Card overload) — ignored in scope:**
   D-005 has been flagged since Round 9. The designer says (line 250): *"Address D-005 (Business Card Overload) as a prerequisite to Sprint 14."* The team's plan addresses it indirectly through C40 (simplification) but doesn't explicitly plan for it. If C40 propagation is done but doesn't adequately reduce the Business Card's cognitive load, the overload persists. Should D-005 have a specific remediation plan within Sprint 14?

5. **Missing definition of "done" for C47 spike:**
   The team calls C47 a "spike" but plans to deploy it. A spike's "done" criterion is "learning achieved" — not "feature shipped." But 3-5 lessons that are deployed to users mean "done" is really "feature shipped." What are the specific acceptance criteria? Does the education academy need to pass design review? Does it need 5 topics × complete content with analogies + quizzes? Does it need progress tracking working end-to-end? Without clear completion criteria, scope ambiguity will cause drift during execution.

**Team Response:**

1. **Designer override justified:** The designer's ranking (#1-#5) is correct in isolation, but the team's selection optimizes for *sprint coherence*, not individual feature priority. C40 + C126 + C47 creates a sprint theme: "Make existing features accessible (C40), make moat analysis comparable (C126), and make knowledge learnable (C47)." This is more coherent than C40 + C125 + C126 (which would be "make everything on the Business Card marginally better"). The designer's "Phase 0: skeleton + 2" recommendation is for a *design-consistency-first* approach; the team's "5 lessons" approach is a *minimum-viable-academy* approach. Both are valid; the team chooses deployable completeness over design purity.

2. **Quality gate established:** C47 lessons must pass the ten-second test: a beginner can restate the core concept within 10 seconds of reading the concept card. The glossary_service.py and quiz_engine.py provide content scaffolding. Each lesson must include: (a) One-sentence summary that passes the ten-second test, (b) Real TW stock example, (c) 3 quiz questions with feedback. If any lesson fails the ten-second test, it is not deployed. The Academy launches with however many lessons pass (minimum 3, target 5). This is a hard quality gate.

3. **Session state accepted for Sprint 14 with Sprint 15 commitment:** For C40, session_state is acceptable because mode preference is a light-weight choice (like selecting a tab). For C47, the team accepts the session_state limitation for Sprint 14 only, with a **commitment to add file-based persistence in Sprint 15** (1-2h work). In the meantime, a `st.info("學習進度僅在本次瀏覽中有效，重新開啟頁面將重從第一課開始")` banner informs users. This is an honest tradeoff.

4. **D-005 remediation via C40:** C40's beginner mode IS the D-005 remediation. When Beginner Mode shows only 3 core sections (Summary, What Changed, Snowflake) instead of 15+, the Business Card becomes a true "business card" again. The designer's own spec (lines 83-88) achieves exactly this. No separate D-005 task is needed — C40 propagation completes D-005 remediation. The key metric: in Beginner Mode, Business Card sections visible must be ≤ 5.

5. **C47 "done" criteria defined:**
   - [ ] `education_academy.py` page renders with Zone B progress sidebar
   - [ ] 5 lessons in `lessons.yaml` with complete content (title, difficulty, stock example, concept explanation ≤ 200 chars, 3 quiz questions with feedback)
   - [ ] All 5 lessons pass the ten-second test
   - [ ] Progress tracking in session_state works (completed lessons marked ✅)
   - [ ] "教育課程" nav item visible in navbar with progress badge ("0/5 完成")
   - [ ] Beginner mode concept on Education Academy page determined (deferred to Sprint 15 — Academy is always visible)
   - [ ] **Minimum viable:** If 5 lessons cannot be completed in budget, deploy with 3 lessons that pass quality gate

---

### Final Verdict

✅ **CONFIRMED** — with revisions

### Revisions

| # | Revision | Impact |
|---|----------|--------|
| 1 | **Execution order: C40 → C126 → C47** (not C126 → C40 → C47). C40 propagation first unblocks beginner-friendly views for all subsequent features. | Design quality ↑ |
| 2 | **C47 scope: 5 complete lessons** minimum 3, all passing the ten-second test. Not a throwaway spike — a deployable MVP. | Reduces scope creep risk |
| 3 | **C125 added as stretch goal**: If C40 + C126 complete under budget (realistic case: 28h), add C125 segment margin toggle (2-3h) from remaining buffer. | Analysis depth ↑ |
| 4 | **C47 quality gate**: Every lesson must pass the ten-second test before deployment. Launch with minimum 3 lessons if 5 aren't ready. | Content quality ↑ |
| 5 | **C40 + D-005 alignment**: C40 propagation must reduce Business Card to ≤ 5 sections in Beginner Mode. This is the D-005 remediation criterion. | Page overload resolved |
| 6 | **Session state disclaimer**: Add info banner in C47 that progress is session-only. Sprint 15 commitment to file-based persistence. | User expectation managed |
| 7 | **C47 done criteria**: 7-point checklist (see Round 3 response) must be met before feature is marked complete. No partial lesson deployment. | Completion clarity ↑ |

---

*Challenge conducted by Challenger, Round 29. Team alignment achieved across Architect, Designer, and Developer with 7 scope revisions incorporated.*
