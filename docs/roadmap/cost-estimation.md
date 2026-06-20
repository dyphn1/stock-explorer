# Cost Estimation Summary

> **Source**: `docs/decisions/cost_estimation.md` (2026-06-12)
> **Estimation Basis**: Single developer, including coding + basic testing

---

## Overview

| Category | Items | Estimated Hours |
|----------|-------|-----------------|
| **A. Technical Debt Fixes** | 12+ | ~30h |
| **B. UX Improvements** | 14 | ~40h |
| **C. Design System Fixes** | 20+ | ~35h |
| **D. New Features** | 25+ | ~80h |
| **E. Sidebar Refactor** | 13 | ~45h |
| **Total** | **76+** | **~230h** |

---

## A. Technical Debt Fixes

| ID | Item | Hours | Status |
|----|------|-------|--------|
| TD-01 | Commit uv.lock | 0.1h | Done |
| TD-02 | Extract timeline constants | 0.2h | Pending |
| TD-03 | Add logging | 0.2h | Pending |
| TD-04 | Rate limit visibility | 0.25h | Done |
| TD-05 | Fix session_state tests | 0.5h | Done |
| TD-06 | Watchlist filelock | 0.5h | Pending |
| TD-07 | Cache cleanup | 0.3h | Pending |
| TD-08 | API cache key fix | 1.0h | Pending |
| TD-09 | business_card.py split | 4.0h | Pending |
| TD-10 | chart_stock.py split | 2.0h | Pending |
| TD-11 | INDUSTRY_BENCHMARKS dedup | 0.5h | Pending |
| TD-12 | _is_etf() logic dedup | 0.5h | Pending |

---

## B. UX Improvements (by Priority)

### P0 (Immediate)
| ID | Item | Hours |
|----|------|-------|
| UX-08 | DuplicateWidgetID crash | 0.1h |

### P1 (Sprint 1)
| ID | Item | Hours |
|----|------|-------|
| UX-05 | ROE TTM fix | 1.0h |
| UX-07 | Watchlist toast | 0.5h |
| UX-11 | Cache cleanup | 0.3h |
| UX-14 | Concurrent write filelock | 0.5h |

### P2 (Sprint 2)
| ID | Item | Hours |
|----|------|-------|
| UX-01 | Chinese search | 2.0h |
| UX-02 | Loading indicator | 2.0h |
| UX-04 | Single-period chart fallback | 1.5h |
| UX-06 | Peer comparison auto-suggest | 2.0h |
| UX-09 | Timeline error message | 1.0h |
| UX-13 | Dark mode contrast | 2.0h |

### P3 (Sprint 3)
| ID | Item | Hours |
|----|------|-------|
| UX-03 | Browser back button | 4.0h |
| UX-10 | Rate limit warning | 3.0h |
| UX-12 | Responsive layout | 5.0h |

---

## C. New Features (by Priority)

### P1
| ID | Item | Hours |
|----|------|-------|
| C170 | Clickable Glossary | 3.0h |
| C188 | Why Did This Move? | 4.0h |
| C204 | Confidence Indicator | 3.0h |
| C205 | Reading Time Indicator | 1.5h |

### P2
| ID | Item | Hours |
|----|------|-------|
| C199 | Today's Market Overview | 5.0h |
| C201 | Daily Market Dashboard | 6.0h |
| C202 | Story Arc Detection | 5.0h |
| C206 | Industry Heatmap | 4.0h |

---

## D. Sidebar Refactor

| ID | Item | Hours |
|----|------|-------|
| SB-04 | Collapsible but expandable (bug) | 0.5h |
| SB-01 | Watchlist inline data | 3.0h |
| SB-02 | Multi-list management | 4.0h |
| SB-03 | Market overview | 2.0h |
| SB-05-08 | P1 improvement items | 8.0h |
| SB-09-13 | P2 bonus features | 10.0h |
