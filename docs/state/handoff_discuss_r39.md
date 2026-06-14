# Handoff – Discussion (Round 39)

## Summary
- **Topic**: Discussion (💡) — Round 39, Sprint 19 Planning
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer (via research), Challenger
- **Sprint**: Sprint 19 (follows Sprint 18 ✅ COMPLETE: C139 + C141 + C143 + C149 + D-097 + Tone QA)

---

## 1. Sprint 19 Features Under Discussion

| ID | Feature | Priority | PM Est | Dev Est | Architect Direction |
|----|---------|----------|---------|---------|-------------------|
| C147 | Historical Event Pattern — "When This Happened Before" | P1 | 14-18h | 17-22h | Pattern-First Direction A |
| C152 | Multi-Factor Event Narratives — One Story, All Factors | P1 | 16-20h | 22-29h | spike only, defer to Sprint 20 |
| C140 | Historical Case Study Library — Browseable Collection | P1 | 16-22h | 16-24h | shared case_studies.yaml with C147 |

---

## 2. Idea Proposals

| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
| C147 | Historical Event Pattern — st.expander() below event cards with range-of-outcomes Plotly chart + outcome cards + historian disclaimer | Developer | ✅ Accepted with spike prerequisite |
| C140 | Case Study Library — New "案例庫" navbar tab, searchable grid, cross-linked with events | Developer | ✅ Accepted with content prerequisite |
| C152 | Multi-Factor Narratives — SPIKE ONLY in Sprint 19 (4-6h design spike), full impl deferred to Sprint 20 | Developer/Designer | ✅ Accepted as spike-only |
| D-112 | Fix `market_event_service.py` silent import failure in `timeline_service.py` | Developer | ✅ Accepted as Day 1 prerequisite |
| D-113 | Extend tone QA to scan YAML content files (not just .py files) | Developer/QA | ✅ Accepted, budget 2-3h |

---

## 3. Decisions Made

### Architecture Decision: Direction A ("Pattern-First")
- C147 + C140 share `case_studies.yaml` as unified data source
- C140 schema extension (category/tags) is **hard prerequisite** for C147 service implementation
- C152 deferred to Sprint 20 after design spike
- New services: `historical_pattern_service.py` (~120 lines), `case_study_library.py` (~80 lines)
- Fix broken `market_event_service` import in `timeline_service.py` (silent failure discovered by Architect)

### Design Decisions
- **C147**: `st.expander("📜 過去類似事件發生時，後續發展...")` below event cards. Range-of-outcomes Plotly chart (min/max/median at 1/3/6mo) + 2-3 compact outcome cards. Mandatory historian disclaimer.
- **C140**: New "案例庫" navbar tab in Zone A. 2-column case card grid with search/filter. Case detail page with 背景→發展→啟示 sections.
- **C152 spike**: Must produce 4 artifacts: (a) event correlation logic, (b) 3-5 tone-audited templates, (c) `NarrativeProvider` protocol design, (d) integration point identified.
- **Cross-linking**: "📚 相關案例" links from event cards → case studies. Drives discovery of case library.
- **Inline HTML budget**: 15 instances (up from 11). Within acceptable range.

### Scope Decisions
- C147 scope: Feasibility spike first (2h). If successful, implement for all mappable event types. If partial, implement for top 5 event types only.
- C140 scope: Ship with minimum 10 case studies (5 existing + 5 new). Target 15 for full library.
- C152 scope: 4-6h design spike only. No implementation in Sprint 19.
- Sprint 19 total: **35-49h** (revised from 33-46h after Challenger's conditions)

### Execution Order (revised after Challenger Rounds 2 & 3)
1. **Day 1 (AM)**: C147 feasibility spike (2h) + C152 design spike (parallel, 4-6h)
2. **Day 1 (PM)**: Fix `market_event_service` import (0.5h) + C140 schema extension begins
3. **Day 2-3**: Tone QA blocklist expansion (2-3h) + C140 service + page dev. C147 service starts after schema extension.
4. **Day 3-4**: Content delivery deadline — C140 case studies from PM/Designer
5. **Day 4-5**: C147 page integration + C152 spike results → Sprint 20 planning
6. **Day 6-7**: Testing, tone QA for all new YAML content, L0/L1 verification

---

## 4. 🔥 Three-Round Challenge (Round 39)

### Round 1: Feature Direction Challenge
**Challenger**: Is Direction A (C147+C140, C152 deferred) the right call? C152 is P1 with highest UX impact (8/10). What's the opportunity cost of deferral? Is the C147 feasibility spike sufficient at 2h? Are there alternative directions (Direction D: "Narrative Core First")?

**Team Response**: Direction A is optimal because (1) C140+C147 share data source, reducing content overhead, (2) C152's architectural complexity (new `NarrativeProvider` protocol, event correlation logic, 57 combination space) makes it the riskiest feature, (3) the 2h spike has a pre-defined decision tree (success/partial/failure), (4) Direction D (C152 first) was considered and rejected due to risk — Sprint 20 can deliver C152 with C147's infrastructure in place.

**Verdict**: ✅ Feature directions confirmed authentic. Direction A accepted with pre-defined spike decision tree.

### Round 2: Priority Challenge
**Challenger**: C152 spike is scheduled Day 4-5 (too late). C140 schema extension must precede C147 service (unaddressed dependency). 33-46h estimate assumes PM/Designer delivers 9-14h content in parallel (unverified). No partial-C147 contingency plan.

**Team Response**: Challenger's timing critique accepted. C152 spike moves to Day 1 parallel with C147 spike. C140 schema extension is now explicit hard prerequisite for C147 service. Partial-C147 contingency added (top 5 event types if spike is partially successful). PM/Designer must commit to Day 3-4 content delivery.

**Verdict**: ✅ Priority order revised. Execution order updated.

### Round 3: Goal Alignment Challenge
**Challenger**: Tone QA budget is grossly insufficient (0.5h vs 2-3h needed). 12+ new blocklist phrases identified by Designer but not budgeted. YAML content is NOT scanned by existing tone QA (known gap). `market_event_service` import failure could propagate to new services. Content creation bottleneck has no mitigation.

**Team Response**: Tone QA budget revised to 2-3h. Blocklist expansion (12+ phrases) must complete before content creation. `market_event_service` fix is Day 1 prerequisite. Content fallback: ship with 5+2 cases if 10 aren't ready by Day 4.

**Verdict**: ✅ CONFIRMED with 8 binding conditions.

---

## 5. Final Challenger Verdict: ✅ CONFIRMED with 8 Conditions

### Binding Conditions
1. **C147 spike must have pre-defined decision tree** before spike starts: success (≥3 event types with ≥3 mapped cases each), partial (1-2 types → top 5 event types only), failure (no mapping → Direction C, ship C140 only).
2. **C152 spike must happen on Day 1**, parallel with C147 spike. Cannot wait until after C147 dev.
3. **C140 schema extension is hard prerequisite** for C147 service implementation. `category`/`tags` fields must be committed before `historical_pattern_service.py` is built.
4. **Tone QA budget is 2-3h** (not 0.5h). Covers: blocklist extension (12+ phrases), YAML scanning for `src/data/*.yaml`, pre-audit of all new content.
5. **Blocklist expansion must complete before content creation starts**. Writers need tone boundaries before writing.
6. **PM/Designer must commit to Day 3-4 content delivery** for C140 case studies. Fallback: ship with 5 existing + 2 new minimum.
7. **Fix `market_event_service` import failure** as Day 1 prerequisite before any new dev. Replace with direct YAML loading.
8. **C152 spike success criteria defined pre-spike**: 4 required artifacts (event correlation logic, 3-5 tone-audited templates, `NarrativeProvider` protocol design, integration point). If not delivered, defer to Sprint 21.

---

## 6. Action Items

| Item ID | Description | Owner | Due Date | Priority |
|---------|-------------|-------|----------|----------|
| R39-PRE1 | Fix `market_event_service` import in timeline_service.py | Developer | Sprint 19 Day 1 | 🔴 FIRST |
| R39-PRE2 | Expand tone QA blocklist with 12+ new phrases | Developer/QA | Before content creation | 🔴 FIRST |
| R39-PRE3 | Pre-write 10 C140 case studies | PM/Designer | Sprint 19 Day 3-4 | 🔴 P1 |
| R39-SPIKE1 | C147 feasibility spike (2h) | Developer | Sprint 19 Day 1 AM | 🔴 FIRST |
| R39-SPIKE2 | C152 design spike (4-6h) | Developer/Designer | Sprint 19 Day 1 | 🔴 P1 |
| R39-DEV1 | C140 schema extension + service + page (8-11h dev) | Developer | Sprint 19 Day 1-5 | 🔴 P1 |
| R39-DEV2 | C147 service + page (12-16h, post-schema + post-spike) | Developer | Sprint 19 Day 2-5 | 🔴 P1 |
| R39-DEV3 | C147 patterns YAML content (4-6 patterns, 3-4h) | PM/Designer | Sprint 19 Day 4-5 | 🟡 P2 |
| R39-QA1 | Tone QA for all new YAML content (2-3h) | QA | Sprint 19 Day 6-7 | 🔴 Required |
| R39-QA2 | All C147/C140 content must pass tone QA before merge | QA | Sprint 19 Day 7 | 🔴 Required |
| R39-PLAN1 | Plan C152 for Sprint 20 based on spike results | PM | Sprint 19 Day 5 | 🟡 P2 |

---

## 7. Consolidated Team Consensus

All roles agree:
- **Architect**: Direction A (Pattern-First) is lowest risk, leverages shared data, defers highest-complexity feature. `timeline_service.py` import fix is critical prerequisite.
- **Designer**: C147 (9/10) is highest UX impact. C140 (7/10) builds historian credibility. C152 spike (8/10) validates Sprint 20 approach. Cross-linking is key integration.
- **Developer**: 35-49h total with C152 spike. C147=17-22h, C140=16-24h, C152 spike=4-6h, Tone QA=2-3h, Prerequisites=1h. Content creation (9-14h) runs in parallel by PM/Designer.
- **Challenger**: ✅ CONFIRMED with 8 conditions after 3 rigorous rounds. Tone QA budget increase and C152 spike timing are the most critical changes.

---

## 8. Feature Pipeline (Updated)

| Sprint | Features | Effort | Status |
|--------|----------|--------|--------|
| Sprint 18 | C139 + C141 + C143 + C149 + D-097 + Tone QA | 24-32h | ✅ COMPLETE (27.6h actual) |
| Sprint 19 | C147 + C140 + C152 spike + D-112 + D-113 | 35-49h | 📋 Planned |
| Sprint 20 | C152 + C142 + C146 | 33-43h | 📋 Planned |
| Sprint 21+ | Remaining P2 features | TBD | 📋 Planned |

---

## 9. New Debt Items (D-112, D-113)

| ID | Description | Severity | Effort |
|----|-------------|----------|--------|
| D-112 | `timeline_service.py` imports non-existent `market_event_service.py` (silent failure, case studies never loaded) | Medium | 0.5h |
| D-113 | Tone QA (`test_tone_qa.py`) only scans .py files via AST — YAML content loaded at runtime is NOT scanned | Medium | 2-3h (includes blocklist expansion) |

---

## 10. New Feature Gaps (from this discussion)

No new feature gaps identified this cycle. All three features (C147, C152, C140) were already in the backlog from Round 38 Review.

---

## Next Cycle Handoff
💡 Discussion Round 39 Complete (Sprint 19: C147 + C140 + C152 spike + D-112 + D-113) → 🔍 Review Round 39 → 🔧 Development Round 40 (Sprint 19 execution)

Reference `docs/research/architect_analysis_sprint19.md` for full technical analysis.
Reference `docs/design/designer_review_sprint19.md` for full design review.
Reference `docs/research/developer_estimates_sprint19.md` for full cost estimates.
Reference `docs/research/challenger_review_sprint19.md` for full challenge record.
