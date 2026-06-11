# Handoff – Discussion

## Summary
- **Topic**: Discussion (💡)
- **Date**: 2026-06-13
- **Participants**: Product Manager, System Architect, Developer, Designer, QA Engineer, Challenger
- **Git Commit**: 1dd103215c337662e7ff2e6b2b6c8a4ba2ad366d

## Idea Proposals
|| Idea ID | Description | Owner | Status |
|---------|-------------|-------|--------|
|| C36 | Visual Revenue Tree - shows how money flows through business (e.g., TSMC → 5nm chips → Apple, NVIDIA, AMD) | Architect/Designer/Developer | Deferred to Sprint 4 (top 10 stocks only) |
|| C37 | Key Takeaways Summary Card - 3-5 auto-generated bullet points synthesizing most important information | Architect/Designer/Developer | Approved for Sprint 2 |
|| C38 | Compare Stories Side-by-Side - narrative comparison of two companies' key events, revenue milestones, business models | Architect/Designer/Developer | Deferred (Phase 1 considered for future) |
|| C39 | What Changed Recently Delta Card - highlights significant recent changes (>10%) with plain-language explanations | Architect/Designer/Developer | Approved for Sprint 4 |
|| C40 | Beginner/Expert Mode Toggle - complexity toggle showing/hiding advanced metrics | Architect/Designer/Developer | Cut - replaced with "beginner mode by default" design principle |
|| C41 | Read Next Recommendations - suggests related companies based on industry, parent-subsidiary, customer-supplier relationships | Architect/Designer/Developer | Approved for Sprint 3 |

## Decisions Made
- Prioritized features that directly support the "ten-second test" design principle and beginner education
- Selected C37 as foundational feature for Sprint 2 to establish page experience and ten-second test compliance
- Chose C36 and C41 for Sprint 3 as complementary storytelling features (visualization + guided discovery)
- Placed C39 in Sprint 4 to pair with C37 for teaching what metrics to monitor over time
- Cut C40 (mode toggle) and replaced with "beginner by default" design philosophy to avoid zone violations and maintenance burden
- Deferred C38 (Compare Stories) due to complexity and dependence on LLM architecture decisions
- Reduced C36 scope to top 10 stocks only to mitigate data curation bottleneck
- All approved features follow layered architecture, reuse existing services, and pose low technical risk
- Verification commitment: ten-second test to be conducted after each feature implementation

## Action Items
|| Item ID | Description | Owner | Due Date |
|---------|-------------|-------|--------|----------|
|| DISCUSS-001 | Implement C37 Key Takeaways Summary Card in business_card.py | Developer | End of Sprint 2 |
|| DISCUSS-002 | Implement C36 Visual Revenue Tree (top 10 stocks) in chart.py and business_card.py | Developer | End of Sprint 4 |
|| DISCUSS-003 | Implement C41 Read Next Recommendations section in business_card.py | Developer | End of Sprint 3 |
|| DISCUSS-004 | Implement C39 What Changed Recently Delta Card in business_card.py | Developer | End of Sprint 4 |
|| DISCUSS-005 | Create curated data files for top 10 stocks (revenue tree relationships) | Developer/QA | During Sprint 4 |
|| DISCUSS-006 | Create curated data files for top 20 stocks (read next relationships) | Developer/QA | During Sprint 3 |
|| DISCUSS-007 | Conduct ten-second test verification for each implemented feature | QA | After each feature completion |
|| DISCUSS-008 | Update documentation and analogy engine for new plain-language explanations | Developer | During respective sprints |

## Next Cycle Handoff
Reference the appropriate `handoff_*.md` for the next theme.
Next theme: 🔧 Development → Sprint 1 (C28 Spike + LLM Architecture)
Next dev cycle: Sprint 1
For full Sprint 0 context, see `docs/state/handoff_dev.md`
For pending Daniel decisions, see `docs/state/pending_review.md`