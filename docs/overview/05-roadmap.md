# Development Roadmap — Stock Explorer

> **Current Phase**: Sprint 21 in progress | **Last Updated**: 2026-06-18

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

## 2. Current Status (Sprint 20 → 21)

### Key Metrics
| Metric | Value |
|--------|-------|
| L0 tests | 319+ passing |
| Design rating | B- |
| Architecture rating | B+ |
| Major blockers | None |

### Items Awaiting Daniel's Decision
| ID | Item | Description |
|----|------|-------------|
| D-126 | Light/dark theme toggle | User preference setting |
| D-127 | _infocard() component | Visual metric card |
| D-128 | _calculator_card() component | Interactive financial tool |
| D-129 | _ai_explanation_card() component | AI explanation card |
| D-130 | Beginner onboarding flow | Structured onboarding |

---

## 3. Sprint 21 Plan

### Week 1
| Priority | Item | Description |
|----------|------|-------------|
| P0 | D-125 | chart_stock.py split |
| P0 | D-126 | INDUSTRY_BENCHMARKS dedup |
| P1 | C170 | Clickable Glossary |
| P1 | C205 | Reading time indicator |

### Week 2
| Priority | Item | Description |
|----------|------|-------------|
| P1 | C188 | Why Did This Move? |
| P1 | C204 | Confidence Indicator |
| P2 | Design system updates | Quick wins |

---

## 4. Feature Roadmap

### Completed Features (M0-M5)
- [x] Business card page (one-line positioning, revenue pie chart, key metric analogies)
- [x] Operations checkup (revenue trends, stock price trends, institutional investor activity)
- [x] Financial health (profit funnel, key ratios, balance sheet structure, cash flow)
- [x] Peer comparison (side-by-side comparison table, radar chart, difference analysis, 28 industry benchmarks)
- [x] Group structure (point-to-point relationships, 5 group data sets)
- [x] Timeline (1Y/3Y/5Y/ALL selector)
- [x] Category browser (blue-chip stocks, industry categories, hot lists)
- [x] ETF section (browser page, detail page, dividend ranking)
- [x] Watchlist (YAML-based, price alerts)
- [x] Event dashboard (event detection engine)
- [x] Adaptive updates (revenue changes, news events, stock price anomaly detection)

### Pending Features (Priority Order)

> 📋 Full list at [`docs/roadmap/`](../roadmap/)

| ID | Feature | Priority | Description |
|----|---------|----------|-------------|
| **UX Improvements** | | | |
| UX-01 | Chinese search support | P1 | Search box supports Chinese stock names |
| UX-02 | Loading indicator | P1 | Show spinner during page transitions |
| UX-03 | Browser back button | P2 | URL query_params sync |
| UX-05 | ROE TTM fix | P1 | Use TTM annualization for seasonal industries |
| UX-07 | Watchlist feedback | P1 | Show toast when adding/removing |
| UX-10 | Rate limit warning | P2 | API rate limit notification |
| UX-12 | Responsive layout | P2 | Small screen adaptation |
| **New Features** | | | |
| C170 | Clickable Glossary | P1 | Real-time professional term lookup |
| C188 | Why Did This Move? | P1 | Plain-language explanation of price changes |
| C204 | Confidence Indicator | P1 | Data reliability indicator |
| C205 | Reading Time Indicator | P1 | Estimated reading time |
| C199 | Today's Market Overview | P2 | Market overview dashboard |
| C201 | Daily Market Overview | P2 | Market story-driven presentation |
| C202 | Story Arc Detection | P2 | Company historical narrative analysis |
| C206 | Industry Heatmap | P2 | Industry sector visualization |
| **Sidebar** | | | |
| SB-01~03 | Sidebar core | P1 | Inline data, multi-list, market overview |
| SB-05~08 | Sidebar improvements | P1 | Category entry, history, width adjustment |
| **Layout Refactor** | | | |
| ADR-009 | Two-layer navigation architecture | P1 | Activity Bar + FAB |

### Technical Debt (Priority Order)
| ID | Item | Priority | Description |
|----|------|----------|-------------|
| TD-01 | Plugin Chassis refactor | ✅ Complete | Phase 1+2 complete, all 24 pages migrated to PluginRegistry |
| TD-02 | Full i18n | P0 | Phase 1 complete (5 major pages, ~300 strings), remaining ~42 files with ~1,200 strings |
| TD-03 | API cache fix | P1 | get_stock_info full table fetch issue |
| TD-04 | business_card.py split | ✅ Complete | Split into business_card/ sub-directory |
| TD-05 | Unit test coverage improvement | P1 | Currently 699 passing but insufficient coverage |
| TD-06 | Color system unification | P1 | All pages use design system colors |
| TD-07 | Component consistency | P1 | Standardize on `_plain_card()` |

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
