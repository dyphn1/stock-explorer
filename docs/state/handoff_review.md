# Handoff – Review

## Summary
- **Topic**: Review (🔍) — Round 35, Sprint 15 Post-Mortem + Sprint 16 Prerequisites
- **Date**: 2026-06-14
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger

## Competitor Research Findings
| Platform | Feature Gap | Suggested Improvement |
|----------|-------------|-----------------------|
| StatementDog | Advanced stock screener with 100+ financial metrics | C42: Stock Screener / Discovery Engine (P1, 16-24h) |
| GoodInfo | P/E band chart showing historical valuation ranges | C45: Valuation Band Chart (P2, 8-10h) - Already in Sprint 16a |
| CMoney | App push notifications with AI explanations | C138: Smart Notifications with Explanations (P1, 10-14h) |
| WantGoo | Market temperature/PPT export | C35: Market Mood Index (P1, 10-12h), C06: PPT Export |
| Public.com | Revenue tree visualization showing money flow | C36: Visual Revenue Tree (P2, 10-14h) |
| Seeking Alpha | Key takeaways summary card (3-5 bullet points) | C37: Key Takeaways Summary Card (P2, 6-8h) |
| Koyfin | Recent changes highlighting significant metric movements | C39: What Changed Recently Delta Card (P2, 8-10h) |
| Stocksera | Side-by-side narrative comparison mode | C38: Compare Stories Side-by-Side (P2, 12-16h) |
| 財報狗 | Stock screener (#1 feature in TW market) | C42: Stock Screener / Discovery Engine (P1, 16-24h) |
| Simply Wall St | Snowflake health visualization (5 dimensions scored 0-5) | C43: Company Snowflake Health Visualization (P1, 12-16h) |
| Stockopedia | StockRank system + educational content | C47: Financial Education Academy (P2, 20-30h) |
| Investopedia | 10K+ term financial glossary | C33: Beginner Glossary / Tooltip System (P2, 8-12h) |

## Decisions Made
- **Technical Debt Priority**: Resolve D6 YAML migration (3-4h) and D5 LLM abstraction layer (2-3h) before Sprint 16 feature work to unblock content contributions and enable LLM-dependent features
- **Test Infrastructure**: Fix D-074 by adding filelock dependency (0.25h) to restore full test coverage before Sprint 16
- **Design System**: Address P1 design issues D-003 (inconsistent card styling) and D-006 (mobile responsiveness) beginning in Sprint 16
- **Sprint 16a Execution**: Proceed with planned features (C14 Health Score + Narrative, C132 Risk Simplification, C45 Valuation Band, C28 Story Timeline Spike) with updated effort estimate of 17-24h
- **Sprint 16b Strategy**: Make conditional decision based on C28 spike validation results:
  - If spike passes data richness criteria (≥5 entries per stock, all dated, interpretation coverage, dedup works, <200ms response): Invest in unique differentiation with C28 Full Story Timeline (26-36h)
  - If spike fails: Close competitive gaps with C02 Notifications System (12-19h) + C07 Custom Event Thresholds (6-9h)
- **Educational Feature Pipeline**: Leverage YAML migration to implement systematic educational features post-Sprint 16 (C33 Glossary, C47 Education Academy)
- **Narrative-First Focus**: All recommended features align with "historian, not stock picker" positioning by emphasizing explanatory narratives, contextual learning, and educational value

## Action Items
| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|----------|
| R35-OPT1 | Complete D6 YAML migration (remaining hardcoded data blocks: revenue_analyzer.py, group_structure.py, analogy_engine.py, key_takeaways.py) | Developer | Before Sprint 16 feature work |
| R35-OPT2 | Create LLM abstraction layer (src/services/llm/ with protocol.py, template_engine.py, llm_provider.py) | Developer | Before Sprint 16 feature work |
| R35-OPT3 | Fix D-074 test infrastructure (add filelock>=3.0.0 to pyproject.toml or requirements.txt) | Developer/QA Engineer | Before Sprint 16 feature work |
| R35-DES1 | Fix inconsistent card styling (D-003) by enforcing use of shared components (_白话_card, _info_card, _summary_card, _subsidiary_card) in watchlist_page.py, etf_detail.py, business_card.py | Designer/Developer | Ongoing - begin Sprint 16 |
| R35-DES2 | Improve mobile responsiveness (D-006) with mobile-specific CSS to force column stacking, increase touch targets, adjust chart fonts | Designer/Developer | Ongoing - begin Sprint 16 |
| R35-DES3 | Update design system documentation (docs/design/design_system.md) to include all current components and usage rules | Designer | Sprint 16 |
| R35-FEAT1 | Implement Sprint 16a planned features: C14 Health Score Badge + Narrative, C132 Risk Simplification (1-5 Scale), C45 Valuation Band Chart, C28 Story Timeline Spike (feasibility validation) | Developer | Sprint 16a |
| R35-FEAT2 | Prepare Sprint 16b decision framework based on C28 spike validation results against go/no-go criteria | PM/Architect | End of Sprint 16a |
| R35-FEAT3 | Design and prototype Beginner/Expert Mode toggle (C40) for progressive disclosure to address business card overload | Designer/Developer | Post-Sprint 16 |
| R35-FEAT4 | Create glossary data structure plan for C33 (src/data/glossary.yaml with term, definition, analogy, related_terms, category fields) | Designer/QA Engineer | Sprint 16 |

## Next Cycle Handoff
The next theme will be determined based on Sprint 16a completion and C28 spike validation outcome:
- If Sprint 16a completes successfully and C28 spike passes validation: Next theme will be 🔧 Development for Sprint 16b (C28 Full Story Timeline)
- If Sprint 16a completes successfully but C28 spike fails validation: Next theme will be 🔧 Development for Sprint 16b (C02 Notifications + C07 Custom Thresholds)
- Reference the appropriate `handoff_*.md` file for the next theme's detailed handoff.