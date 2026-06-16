# Pending Review — Daniel Decisions

> **Last Updated**: 2026-06-17
> **Source**: Round 49 Discussion

## Open Questions for Daniel

### Sprint 24 Decisions — NEED CONFIRMATION

#### 1. C201 Daily Market Dashboard — Narrative Style Approval
- **Context**: Architecture design complete at `docs/architecture/c201_daily_market.md`
- **Proposal**: Template-based narrative (no LLM) with 5 sections: overview, sentiment, sectors, movers, events
- **Question**: Should the market overview paragraph be more data-heavy or more story-heavy?
- **Status**: ⏳ Pending Daniel

#### 2. C203 Supply Chain Visual Map — FinMind API Limitation
- **Context**: FinMind's supply chain API is paid-only
- **Proposal**: Redefined as "Company Ecosystem Cards" v1 — card-based layout for top 15-20 stocks using existing `group_structures.yaml` + manually curated data. No network graph in v1.
- **Revised estimate**: 12-15h (down from 36-50h)
- **Status**: ⏳ Pending Daniel — approve "ecosystem cards" approach?

### Previously Open Items (Still Pending)

#### 3. Dark/Light Theme Implementation (D-126)
- **Context**: Design review identified missing dark/light theme implementation.
- **Proposal**: Add theme preference in settings with CSS variables.
- **Estimated Effort**: 8-12h
- **Status**: ⏳ Pending Daniel

#### 4. Missing Component: _infocard() for Visual-First Metrics (D-127)
- **Context**: Missing _infocard() component for infographic-style visual cards.
- **Proposal**: Create _infocard(icon, sparkline_data, label, value, analogy) component.
- **Estimated Effort**: 6-9h
- **Status**: ⏳ Pending Daniel

## Resolved This Cycle (Round 49)

| Item | Decision |
|------|----------|
| C201 TAIEX data source | ✅ Use avg change % proxy — no absolute index value needed |
| C201 volume baseline | ✅ Simplified to absolute total (億元) — no 5-day comparison |
| C201 event filtering | ✅ Post-filter by market-relevant types only |
| C203 scope | ✅ Redefined as "Company Ecosystem Cards" v1 (12-15h) |
| C209 design | ✅ Redesigned as collapsible "資料來源" section (4-6h) |
| Sprint 23 completion | ✅ All 3 features verified complete, 545 tests green |
| Round 48 blockers | ✅ All 5 blocking questions resolved in codebase |

---

*This file is maintained by the PM. Items move to resolved when Daniel confirms.*
