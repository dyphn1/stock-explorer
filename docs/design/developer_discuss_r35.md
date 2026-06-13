## 2026-06-14 Developer Estimate — Sprint 16b Discussion

### Feature Cost Estimates
| Feature | Hours | Complexity | Risk | Dependencies |
|---------|-------|------------|------|--------------|
| C28 Full Story Timeline | 30-40h | Medium-High | Medium | timeline_service.py, company_milestones.yaml, adaptive_engine, event_interpretation_service |
| C02 Notifications | 0h (Already Done) | Low | None | None - implementation complete |
| C134 Change Explanations | 20-26h | High | High | LLM abstraction layer (D5), delta_engine.py, analogy_engine.py |
| C39 What Changed Recently | 0h (Already Done) | Low | None | None - implementation complete |
| C07 Custom Thresholds | 12-16h | Medium | Medium | risk_analyzer.py, notification_service.py, config UI |

### Technical Risks

**C28 Full Story Timeline:**
- **Data sparsity risk**: events.yaml only contains ~1 week of data; timeline may appear empty without sufficient historical events
- **Milestone data gap**: company_milestones.yaml doesn't exist yet - requires curation of founding dates, IPO dates, product launches
- **Deduplication complexity**: same-day events from multiple sources (news, price, revenue) need intelligent merging
- **Performance**: Merging 3 data sources (events, case studies, milestones) and sorting by date must stay <200ms
- **UI/UX challenge**: Creating a compelling narrative timeline that doesn't overwhelm users with too many events

**C134 Change Explanations:**
- **LLM abstraction dependency**: Cannot start until D5 (LLM integration layer) is built - this is a blocker
- **Quality control**: Ensuring explanations are accurate, historian-aligned (past-focused, not predictive), and not repetitive
- **Prompt engineering**: Designing effective prompts for financial change explanations that work consistently across metrics
- **Cost/latency**: If using external LLM API, need to manage costs and response times; if local model, need to manage model size and loading time
- **Testing difficulty**: Non-deterministic outputs make automated testing challenging

**C07 Custom Thresholds:**
- **Configuration complexity**: Building a UI that allows users to customize risk thresholds without breaking existing logic
- **Persistence**: Storing user preferences in session_state or config files while maintaining system stability
- **Backwards compatibility**: Ensuring existing risk assessments continue to work when users modify thresholds
- **Validation**: Preventing users from setting illogical threshold values (e.g., medium > high)

### Recommendations

1. **Prioritize C28 Full Story Timeline first** since:
   - Spike has already passed (GO verdict)
   - No blocking dependencies (unlike C134 which needs LLM layer)
   - High differentiation factor - no competitors have narrative timelines
   - Builds on existing adaptive_engine and event_interpretation_service

2. **Build LLM abstraction layer (D5) immediately after C28** to unblock C134:
   - Create src/services/llm/base.py with ExplanationProvider protocol
   - Implement TemplateExplanationProvider as fallback (using existing analogy_engine/news_summarizer)
   - This enables future LLM integration while maintaining backward compatibility
   - Estimated effort: 3-4h (based on architecture debt item D5)

3. **Implement C07 Custom Thresholds concurrently with LLM work**:
   - Start with exposing existing risk_analyzer.py thresholds via UI
   - Add validation logic to prevent invalid threshold combinations
   - Store preferences in session_state with config persistence option
   - Can leverage existing notification_service patterns for config management

4. **Defer C134 Change Explanations until LLM layer is complete**:
   - Once abstraction layer exists, implement ChangeExplanationService
   - Focus on explaining deltas computed by delta_engine.py (C39)
   - Use historian-aligned, past-tense explanations only (no predictive language)
   - Reuse existing explanation patterns from event_interpretation_service

5. **Leverage existing infrastructure**:
   - C28 can reuse: adaptive_engine.get_events_for_stock(), event_interpretation_service.get_interpretation(), market_event_service.get_milestones()
   - C07 can reuse: risk_analyzer.py assessment functions, notification_service config patterns
   - Both can use existing session_state patterns and URL synchronization

6. **Risk mitigation strategies**:
   - For C28: Implement fallback to show "Limited timeline data available" when <3 events found
   - For C134: Start with template-based explanations as fallback before LLM integration
   - For C07: Provide "Reset to defaults" button and validate thresholds on save

**Estimated total for Sprint 16b**: 42-56 hours (assuming C28 + C07 + initial LLM layer work)
**Note**: C134 would be targeted for Sprint 17 after LLM layer completion.