# Handoff – Review Round 41 (2026-06-14)

## Summary
- **Topic**: Review (🔍) — Round 41, Sprint 20 Mid-Cycle: C167 Post-Mortem + C163/C40 Prerequisites
- **Date**: 2026-06-14
- **Sprint Status**: Sprint 20 🔧 IN PROGRESS (C167 ✅ done, C163 + C40 pending)
- **Participants**: PM, Architect, Developer, Designer, QA, Challenger

## Key Metrics
- **Architecture**: 🟢 HEALTHY — 47 service modules, 0 god modules, 100% Streamlit-free
- **Design**: A- (downgraded from A — D-003 regression in C167 screener page)
- **L0**: 125/125 (2 pre-existing quiz_service.py) | **Tests**: 319 passed, 1 failed (tone QA)
- **Sprint 20 Cost**: 30-42h budget, C167 ~14h actual
- **New Feature Gaps**: 11 (C175-C185), 6 P1 + 5 P2
- **New Debt Items**: 7 (D-121 through D-127), all Medium/Low
- **Inline HTML**: 4 new instances in stock_screener.py (D-003 regression)

## C167 Post-Mortem
| Aspect | Assessment |
|--------|------------|
| Architecture | ✅ Excellent — ScreenerExplanationProvider follows ExplanationProvider protocol, compose-and-enrich, zero Streamlit |
| Design | ⚠️ A- — 4 inline HTML blocks (D-121/D-122), 3 non-standard colors (D-123), green misuse (D-124) |
| Tone QA | ❌ FAILING — `_DISCLAIMER` line 20 and implication line 282 contain `建議` (blocklist word) |
| Tests | ✅ 27+ unit tests, all pass |
| Historian framing | ✅ Past tense, factual, mandatory disclaimer |

## New Debt Items (D-121 through D-127)
| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-121 | screener_explanation_provider.py templates hardcoded in Python — YAML exists but not loaded | Medium | 1-2h |
| D-122 | stock_screener.py 4 unsafe_allow_html instances (3 preset cards + 1 result card) | Medium | 1-2h |
| D-123 | Tone QA failure: `建議` in disclaimer (line 20) and implication (line 282) | Medium | 0.5h |
| D-124 | TemplateExplanationProvider (131 lines) zero test coverage | Medium | 1-2h |
| D-125 | No composite "match score" on screener result cards | Low | 1-2h |
| D-126 | Result cards lack visual hierarchy vs competitors | Low | 1.5-2h |
| D-127 | explain() called in loop, no batching | Low | 1h |

## New Feature Gaps (C175-C185)
| ID | Feature | Priority | Effort | Source |
|----|---------|----------|--------|--------|
| C175 | NL-First Screening — search-box interface | P1 | 14-18h | Screenful |
| C176 | Screener+Education Integration — micro-lessons in results | P1 | 10-14h | Tickertape |
| C179 | Explain Every Element — tap any UI element for explanation | P1 | 12-16h | Tijori Finance |
| C183 | Financial Terms Deep Dive — formula + explanation + interpretation | P1 | 8-12h | Gurufocus |
| C184 | NL Q&A — natural language questions about stocks | P1 | 16-20h | Koyfin |
| C185 | Warning Signs — plain-language risk indicators | P1 | 8-12h | Gurufocus |
| C177 | Community Screens — share screening strategies | P2 | 10-14h | Tickertape |
| C178 | Document Analysis — upload annual reports → AI insights | P2 | 18-24h | Tijori Finance |
| C180 | Visual Margin of Safety — DCF visualization | P2 | 12-16h | Alphaspread |
| C181 | Scenario Analysis — what-if on financials | P2 | 14-18h | Alphaspread |
| C182 | Guru Holdings Tracker — follow famous investors | P2 | 10-14h | Gurufocus |

## Sprint 20 Readiness Assessment (C163 + C40)
| Prerequisite | Status | Action |
|-------------|--------|--------|
| D-123 (tone QA fix) | 🔴 BLOCKING | Fix before any new feature merge |
| D-122 (screener inline HTML) | 🟡 Recommended | Fix during C163/C40 dev |
| C163 content (educational cards) | 🟡 Ready | Designer to write 3-5 cards |
| C40 beginner spec | 🟡 Ready | PM+Designer to write shared spec |
| L0/Tests | ✅ PASSING | 319/320 (1 tone QA fix needed) |
| Architecture | 🟢 HEALTHY | No blockers |

**Verdict**: ✅ READY with 1 blocking prerequisite (D-123 tone QA fix)

## 🔥 Three-Round Challenge (Round 41)
**Challenger**: ✅ CONFIRMED with 6 conditions

### Round 1: Gap Authenticity
- C175 (NL-First Screening) confirmed authentic — Screenful proves the model, C167's filter-based UI is the intermediate step
- C176 (Screener+Education) confirmed authentic — Tickertape's embedded micro-lessons have no TW equivalent
- C183 (Financial Terms Deep Dive) confirmed authentic — Gurufocus's formula+explanation+interpretation is exactly our "historian" positioning
- C178 (Document Analysis) confirmed authentic — unique white space, no TW competitor has it
- C184 (NL Q&A) confirmed authentic — Koyfin Answers proves demand, overlaps with C59 boundary needs definition

### Round 2: Priority
- D-123 must be fixed immediately (unblocks CI gate)
- C163 before C40 confirmed (Challenger condition from R40 still binding)
- C175 should NOT displace C163/C40 in Sprint 20 — queue for Sprint 22
- D-121/D-124 (YAML migration + template tests) should be Sprint 21 infrastructure

### Round 3: Goal Alignment
- C175 NL interface aligns with "ten-second test" — simplest possible interface
- C178 document analysis aligns with "historian" — explaining what happened in plain language
- C184 NL Q&A must be scoped as "historian agent" not "stock picker" (same condition as C162)
- C182 Guru Holdings is borderline "stock picker" — must use historian framing (what they bought, not what you should buy)

### 6 Challenger Conditions
1. D-123 tone QA fix is BLOCKING — no new feature merges until `建議` is removed from user-facing text
2. C175 NL-First Screening queued for Sprint 22, NOT Sprint 21 (C152+C170+D-120 take priority)
3. C184 NL Q&A must be scoped as "historian agent" — factual answers only, no recommendations
4. C182 Guru Holdings must use historian framing — "張磊在2020年買進台積電" not "你應該跟著買"
5. D-121 YAML migration + D-124 template tests must be Sprint 21 infrastructure (pre-C152)
6. C163 content creation must start NOW (parallel with Sprint 20 remaining work)

## Sprint 20 Final Plan (Post-Challenge, Unchanged)
| Order | Task | Estimate | Status |
|-------|------|----------|--------|
| 1 | C167 AI Screener Explanations | 12-16h | ✅ DONE (14h) |
| 2 | C163 Learn First Gate | 10-14h | ⏳ Next |
| 3 | C40 Beginner/Expert Mode Toggle | 8-12h | ⏳ Pending |
| — | D-123 tone QA fix | 0.5h | 🔴 Blocking |

## Feature Pipeline (Updated)
| Sprint | Features | Effort | Status |
|--------|----------|--------|--------|
| Sprint 20 | C167+C163+C40 | 30-42h | 🔧 IN PROGRESS (1/3 done) |
| Sprint 21 | D-120(pre)+C170+C152+C172(stretch) | 38-52h | 📋 Planned |
| Sprint 22 | C175 NL-Screening + enhancements | TBD | 🔮 Future |

## Action Items
| Item ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| R41-DEV1 | Fix D-123: Remove `建議` from screener_explanation_provider.py lines 20+282 | Developer | 🔴 Blocking |
| R41-DEV2 | Fix D-122: Replace inline HTML in stock_screener.py with shared components | Developer | 🟡 Sprint 20 |
| R41-DEV3 | Fix D-121+D-124: YAML migration + template provider tests | Developer | 🟡 Sprint 21 infra |
| R41-DES1 | Write C163 educational cards (3-5 cards) — start NOW | Designer | 🔴 Parallel |
| R41-DES2 | Fix D-121: Replace 3 non-standard preset colors with design system colors | Developer | 🟡 Sprint 20 |
| R41-QA1 | Add screener_explanation_provider.py to tone QA scan after D-123 fix | QA | 🔴 Required |
| R41-FEAT1 | Plan C175 NL-First Screening for Sprint 22 | PM | 🟡 Sprint 22 |

## Next Cycle
🔧 Development Round 42: Continue Sprint 20 with C163 Learn First Gate (10-14h), then C40 Beginner/Expert Mode Toggle (8-12h). D-123 tone QA fix must be completed before any new feature merge.

---
*Full research artifacts: docs/research/review41_qa.md, docs/design/design_review.md (updated)*
*Architect analysis: 47 service modules, 0 god modules, 100% Streamlit-free, 319 tests passing*
*Competitor research: 6 new competitors (Screenful, Tickertape, Tijori, Alphaspread, Gurufocus, Koyfin), 11 new gaps (C175-C185)*
