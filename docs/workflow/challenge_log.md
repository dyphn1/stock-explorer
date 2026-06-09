# Challenge Log

Record each important decision that goes through the Challenger review process.

## Format

```markdown
## [Date] Theme: [development/discussion/review]

### Round 1
- Plan:
- Challenge:
- Response:

### Round 2
- Revision:
- Challenge:
- Response:

### Round 3
- Final plan:
- Confirmation: aligned
```

---

## [2026-06-10] Theme: 🔧 開發 — 競品研究新功能實作

### Round 1

- **PM Proposal:** Implement 3 P0 features from competitor research in order C01 → C03 → C02:
  - C01 (P0): 除權息行事曆 — 1-2h, data already available
  - C03 (P0): 多 Watchlist 清單 — 3-4h, refactor YAML schema
  - C02 (P0): 推播通知系統 — 3-4h, new notifier service
  - Total: 7-10 hours

- **Challenger Questions:**
  1. Why skip the 2-hour "Immediate" tech debt cleanup? Building on broken foundation guarantees rework.
  2. C02 dependency on C03 is artificial — they touch completely different code paths.
  3. Not all 3 are truly P0: C01=P0 ✅, C02 needs design spike (downgrade to P1), C03 is nice-to-have (downgrade to P1).
  4. Daniel hasn't confirmed ANY of the 10 competitor-research features. Should we implement without approval?
  5. C02 is massively under-estimated: no user accounts, no email infrastructure, no background worker — this is 6-8h minimum.
  6. C01's data feasibility is unconfirmed (TaiwanStockDividend free tier?).
  7. P0/P1 bug fixes haven't been verified by Daniel yet.

- **PM Response:**
  - Challenger raises valid points. Adjusting plan:
    1. **Tech debt cleanup FIRST** — 2h investment before any features. Non-negotiable.
    2. **Downgrade C02 to P1** — needs design spike before implementation. Will schedule for Sprint 2.
    3. **Downgrade C03 to P1** — useful but not critical. Will implement in Sprint 1 after C01.
    4. **C01 stays P0** — biggest competitor gap, data likely available (already fetched in get_stock_data).
    5. **Verify C01 data feasibility** before implementing — quick API test.
    6. **Daniel approval**: We're an autonomous cron team. We implement, write to pending_review.md, and Daniel reviews on his schedule. We don't block on approval for every feature.
  - Revised order: Tech Debt Cleanup → C01 (verify data) → C03 → C02 (design spike first)

### Round 2

- **PM Revision:**
  - **Sprint 1a (2h):** Tech debt cleanup — remove duplicated card helpers from operation_checkup.py, financial_health.py, group_structure.py (import from _router_base instead). Consolidate `_is_etf` to use watchlist.py version everywhere. Remove dead `filter_by_timeline` from timeline_controls.py.
  - **Sprint 1b (1-2h):** C01 Dividend Calendar — verify TaiwanStockDividend API works on free tier first. If yes, implement dividend_analyzer.py + business_card.py section.
  - **Sprint 1c (3-4h):** C03 Multi-Watchlist — refactor watchlist.yaml schema, update watchlist.py API, update watchlist_page.py with st.tabs(), update business_card.py with list selector.
  - **Sprint 2 (future):** C02 Notification System — after design spike for background worker architecture.
  - Total Sprint 1: 6-8 hours.

- **Challenger Questions:**
  1. Tech debt cleanup is good but what about the `_find_value` duplication? That's also HIGH severity.
  2. C01 data verification — who does the API test? Need to confirm before committing sprint time.
  3. C03 schema migration — what if it fails mid-way? Need atomic migration with backup.
  4. What about the P2 items from competitor research? Are we ignoring them entirely?
  5. Should we also address the "partial data rendering" tech debt before adding new features to business_card.py?

- **PM Response:**
  1. `_find_value` consolidation is included in the tech debt cleanup sprint.
  2. C01 data verification will be the FIRST task — Developer runs a quick `uv run python -c "from src.data.finmind_client import FinMindClient; c=FinMindClient(); print(c.get_dividend('2330').columns.tolist())"` before any implementation.
  3. C03 migration will use the existing atomic write pattern (`_atomic_write` + `filelock`) with automatic backup of old YAML.
  4. P2 items (影音教學, 美股支援, 全球市場地圖) are explicitly deferred — they're future considerations.
  5. Partial data rendering is important but separate — we'll add it to the tech debt backlog for Sprint 2.

### Round 3

- **PM Final Plan:**
  **Sprint 1 — Tech Debt + C01 + C03 (8-10 hours total)**
  
  Phase 1 — Tech Debt Cleanup (2h):
  - Remove duplicated card helpers from 3 files (import from _router_base)
  - Consolidate `_find_value` / `_find_financial_value` into single utility
  - Consolidate `_is_etf` to use watchlist.py version everywhere
  - Remove dead `filter_by_timeline` from timeline_controls.py
  - Run Layer 0 + Layer 1 verification
  
  Phase 2 — C01 Dividend Calendar (1-2h):
  - Verify TaiwanStockDividend API on free tier (quick test)
  - Create `src/services/dividend_analyzer.py`
  - Add dividend section to `business_card.py`
  - Run Layer 0 + Layer 1 verification
  
  Phase 3 — C03 Multi-Watchlist (3-4h):
  - Schema migration with atomic backup
  - Refactor watchlist.py API
  - Update watchlist_page.py with st.tabs()
  - Update business_card.py with list selector
  - Run Layer 0 + Layer 1 verification
  
  **Sprint 2 (Future) — C02 Notification System**
  - Design spike for background worker architecture
  - Implement notifier.py + settings UI
  
  **Deferred:** P2 items (C08, C09, C10), partial data rendering tech debt

- **Challenger Confirms:** ✅ Target aligned
  - The revised plan addresses all major concerns: tech debt first, data verification before implementation, proper priority classification, atomic migration.
  - C02 deferral is correct — it needs architectural design before implementation.
  - The 3-phase approach is realistic and each phase has clear verification gates.
  - Proceed with implementation.
