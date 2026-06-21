# Development Roadmap — Stock Explorer

> **Current Phase**: Sprint 21 in progress | **Last Updated**: 2026-06-21

---

## 1. Milestone Overview

| Milestone | Status | Completion Date | Description |
|-----------|--------|-----------------|-------------|
| **M0**: Project foundation | ✅ Complete | 2026-06-06 | Environment, dependencies, directory structure |
| **M1**: MVP business card page | ✅ Complete | 2026-06-07 | One-line positioning, pie chart, key metrics |
| **M2**: Four deep-dive sections | ✅ Complete | 2026-06-07 | Operations checkup, financial health, peer comparison, group structure |
| **M3**: Timeline and categories | ✅ Complete | 2026-06-07 | Timeline component, category browser |
| **M4**: ETF and subscription | ✅ Complete | 2026-06-07 | ETF section, watchlist |
| **M5**: Adaptive updates | ✅ Code complete | 2026-06-07 | Event detection, freshness indicators |

---

## 2. Current Sprint Status

### Key Metrics
| Metric | Value |
|--------|-------|
| L0 tests | 319+ passing |
| Design rating | B- |
| Architecture rating | B+ |
| Major blockers | None |

---

## 3. Work Items

### P0 — Critical
| ID | Item | Description |
|----|------|-------------|
|| TD-02 | Full i18n | Phase 1 complete (5 major pages, ~300 strings), Phase 2a complete (zh-TW translations for adaptive_engine, dividend, revenue_analyzer — 5 tests fixed), remaining ~42 files with ~1,200 strings |
|| D-125 | chart_stock.py split | ~~Split chart_stock.py into smaller modules~~ ✅ Already done (split into chart_stock_financial.py, chart_stock_health.py, chart_stock_valuation.py) |
|| D-126 | INDUSTRY_BENCHMARKS dedup | Remove duplicate industry benchmark data ✅ Complete (2026-06-21) |

### P1 — High
| ID | Item | Description |
|----|------|-------------|
| UX-01 | Chinese search support | Search box supports Chinese stock names |
| UX-02 | Loading indicator | Show spinner during page transitions |
| UX-05 | ROE TTM fix | Use TTM annualization for seasonal industries |
| UX-07 | Watchlist feedback | Show toast when adding/removing |
| C170 | Clickable Glossary | Real-time professional term lookup |
| C188 | Why Did This Move? | Plain-language explanation of price changes |
| C204 | Confidence Indicator | Data reliability indicator |
| C205 | Reading Time Indicator | Estimated reading time |
| TD-03 | API cache fix | get_stock_info full table fetch issue |
| TD-05 | Unit test coverage improvement | Currently 699 passing but insufficient coverage |
|| TD-06 | Color system unification | All pages use design system colors | ✅ Complete (2026-06-21) |
| TD-07 | Component consistency | Standardize on `_plain_card()` | ✅ Complete (2026-06-21) |
| SB-01~03 | Sidebar core | Inline data, multi-list, market overview |
| SB-05~08 | Sidebar improvements | Category entry, history, width adjustment |
| ADR-009 | Two-layer navigation architecture | Activity Bar + FAB |
| D-127 | _infocard() component | Visual metric card |
| D-128 | _calculator_card() component | Interactive financial tool |
| D-129 | _ai_explanation_card() component | AI explanation card |
| D-130 | Beginner onboarding flow | Structured onboarding |

### P2 — Normal
| ID | Item | Description |
|----|------|-------------|
| UX-03 | Browser back button | URL query_params sync |
| UX-10 | Rate limit warning | API rate limit notification |
| UX-12 | Responsive layout | Small screen adaptation |
| C199 | Today's Market Overview | Market overview dashboard |
| C201 | Daily Market Overview | Market story-driven presentation |
| C202 | Story Arc Detection | Company historical narrative analysis |
| C206 | Industry Heatmap | Industry sector visualization |
| D-126-ui | Light/dark theme toggle | User preference setting |

---

## 4. Completed Technical Debt

| ID | Item | Status |
|----|------|--------|
| TD-01 | Plugin Chassis refactor | ✅ Complete — Phase 1+2 complete, all 24 pages migrated to PluginRegistry |
| TD-04 | business_card.py split | ✅ Complete — Split into business_card/ sub-directory |

---

## 5. Long-Term Vision

### Phase 1: MVP Stabilization (Current)
- Complete M0-M5 features
- Fix known technical debt
- Establish stable testing foundation

### Phase 2: Experience Enhancement
- Plugin Chassis architecture
- Full i18n support
- Beginner onboarding flow
- Light/dark theme

### Phase 3: Community and Expansion
- User-customizable analysis frameworks
- Sharing feature (company analysis report export)
- Multi-market support (US stocks, HK stocks)
- Mobile adaptation
