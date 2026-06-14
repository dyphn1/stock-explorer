# Handoff – Discussion Round 43 (2026-06-14)

## Summary
- **Topic**: Discussion (💡) — C163 Learn First Gate + C40 Beginner/Expert Mode: Implementation Direction & Sprint 20/21 Planning
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Design Reviewer, Developer, Challenger
- **Sprint Status**: Sprint 20 🔧 IN PROGRESS (C167 ✅ done, C163 + C40 pending) → Sprint 21 📋 PLANNED

---

## Key Discovery: All Roles Converge on Option A (Unified Beginner Experience)

The Architect, Designer, and Challenger independently validated the same core approach:

| Role | Primary Recommendation | Key Risk Flagged |
|------|----------------------|------------------|
| **Architect** | Option A: Unified system with shared `user_experience_level` state | Sprint 20 overflow (18-24h vs 16-28h budget) |
| **Designer** | Full-page gate (not modal) + sidebar toggle (Zone B, not Zone A) | C163/C40 definition conflict without shared spec |
| **Challenger** | ✅ Confirmed Option A with 3 binding conditions | Session state granularity (2 vs 3 levels); Sprint 21 overcommitment |

---

## Idea Proposals

| Idea ID | Description | Proposed By | Status |
|---------|-------------|-------------|--------|
| DIR-1 | C163 Learn First Gate — Full-page 4-lesson soft gate replacing C103 | Architect + Designer | ✅ Sprint 20 |
| DIR-2 | C40 Beginner/Expert Mode — Sidebar toggle (Zone B), all pages | Architect + Designer | ✅ Sprint 20 |
| DIR-3 | `experience_service.py` — Pure service for mode checks + lesson loading | Architect | ✅ Sprint 20 |
| DIR-4 | `gateway_lessons.yaml` — 4 micro-lessons content file | Architect + Designer | ✅ Sprint 20 |
| DIR-5 | Per-page beginner mode spec — 3-5 key sections per page | Designer | ✅ Spec done in design doc |

---

## Decisions Made

### Sprint 20 Final Plan: C163 + C40 (Option A — Unified Beginner Experience)

| Order | Task | Estimate | Type |
|-------|------|----------|------|
| 0 | **P1**: Per-page beginner mode spec (Designer's spec is sufficient) | 0h (done) | Prerequisite |
| 1 | **P2**: Write gateway lesson content (4 micro-lessons) | 3-4h | Content (parallel) |
| 2 | **P3**: Remove C103 (`first_visit_guide.py`) | 0.5h | Cleanup |
| 3 | **C163**: Implement Learn First Gate page | 8-10h | Feature |
| 4 | **C40**: Implement sidebar toggle + per-page beginner mode | 8-10h | Feature |
| 5 | **Shared**: `experience_service.py` + `gateway_lessons.yaml` | 2-4h | Infrastructure |
| | **Total (coding)** | **18.5-24.5h** | |
| | **Total (with content)** | **21.5-28.5h** | Fits 16-28h remaining at lower bound |

### Architecture Decisions

1. **Session state**: 2 levels only (`"beginner" | "expert"`). NO `intermediate` value. No 3-level enum.
2. **C163 format**: Full-page "學習入門" page in router (NOT modal, NOT slide-over). Replaces C103 entirely.
3. **C163 content**: 4 micro-lessons — (1) what is a stock, (2) how companies make money, (3) key metrics (P/E + ROE), (4) what is Stock Explorer (historian positioning).
4. **C163 gate type**: Soft gate with always-visible "跳過教學" (Skip) link. Never mandatory.
5. **C40 toggle placement**: Zone B sidebar, above search box. `st.radio` with "🌱 新手模式" / "🔬 進階模式". NOT in Zone A navbar (design system prohibits interactive controls in Zone A).
6. **C40 scope**: ALL stock pages. Per-page spec: 3-5 key sections shown, rest hidden behind expanders labeled "🔬 進階內容".
7. **C40 default**: Beginner mode for all new users. Instant switching (< 0.5s), no data reload.
8. **New service**: `src/services/experience_service.py` — pure functions, no Streamlit imports.
9. **New data**: `config/lessons/gateway_lessons.yaml` — lesson content.

### Competitor Validation

- **Webull**: "Learn First, Trade Later" soft gate → validates C163 soft gate approach
- **NerdWallet**: Persistent "Simple View" toggle → validates C40 persistent toggle
- **Sharesies**: Complexity level selector in sidebar → validates C40 sidebar placement
- **Stash**: 2-card micro-lesson first visit → baseline for C163 (extending to 4 lessons)
- **Tastytrade**: Learn → Practice → Invest progression → validates C163→C40 flow
- **Simply Wall St**: Snowflake visual summary → validates "ten-second test" alignment
- **No TW competitor** has either feature → white space confirmed

---

## 3 Binding Conditions (from Challenger — Non-Negotiable)

1. **Session state must be 2 levels only** (`"beginner" | "expert"`). The `experience_service.py` interface must explicitly define only 2 values. No `intermediate`, no 3-level enum. If 3 levels are desired later, that's a new feature (C122 Adaptive Learning).

2. **C163-alone shipping requires a "coming soon" indicator.** If C40 doesn't fit in Sprint 20, C163 ships with a visible but non-intrusive banner on stock pages: "🌱 新手模式開發中 — 目前顯示完整內容" (Beginner Mode in development — showing full content). This manages user expectations and avoids the "gate promises simplicity, pages delivers complexity" trap.

3. **Sprint 21 hard cut-line required before coding begins.** Before Sprint 21 development starts: if C40 carries over, C152 templates are capped at 5 (not 8), and C172 is dropped entirely. Sprint 21 is already overcommitted (38-52h vs 30-42h capacity) without carry-over.

---

## Action Items

| Item ID | Description | Owner | Priority |
|---------|-------------|-------|----------|
| R43-DISC1 | Write C163 gateway lesson content (4 micro-lessons) — start NOW | PM + Designer | 🔴 Parallel with Sprint 20 |
| R43-DISC2 | Remove C103 (`first_visit_guide.py`) + "新手導覽" from router | Developer | 🔴 During C163 implementation |
| R43-DEV1 | Implement C163 Learn First Gate page | Developer | 🔴 Sprint 20 |
| R43-DEV2 | Implement `experience_service.py` + `gateway_lessons.yaml` | Developer | 🔴 Sprint 20 |
| R43-DEV3 | Implement C40 sidebar toggle + per-page beginner mode | Developer | 🔴 Sprint 20 |
| R43-QA1 | Define Sprint 20 exit criteria for C163/C40 | QA + PM | 🔴 Before Sprint 21 |
| R43-QA2 | Mobile testing for C163 gate (375px viewport) | QA | 🟡 Before C163 ship |
| R43-PM1 | Define Sprint 21 hard cut-line (C152 template cap + C172 drop rule) | PM | 🔴 Before Sprint 21 |

---

## Feature Pipeline (Updated)

| Sprint | Features | Effort | Status |
|--------|----------|--------|--------|
| Sprint 20 | C167 + C163 + C40 | 32-38h | 🔧 IN PROGRESS (1/3 done) |
| Sprint 21 | D-120(pre) + C170 + C152 + C172(stretch) | 38-52h | 📋 Planned (hard cut-line TBD) |
| Sprint 22 | C175 NL-Screening + enhancements | TBD | 🔮 Future |

---

## Next Cycle
🔧 Development Round 44: Implement C163 Learn First Gate (8-10h) + C40 Beginner/Expert Mode Toggle (8-10h). Gateway lesson content creation runs in parallel. D-120 benchmark extraction should be completed as pre-Sprint 21 infrastructure.
