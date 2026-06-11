## Friday, June 12, 2026 Technical Analysis — Round 13 Discussion

### Competitive Landscape Summary
Based on the Round 12 competitor research (9 competitors analyzed) and key insights, Stock Explorer's current positioning as a "Beginner Education (Historian)" tool addresses several gaps but leaves opportunities in specific areas. The competitor landscape shows:

**Addressed Gaps (Planned or In Progress):**
- **Social Learning**: Lightweight social sharing (C53-1 URL, C53-2 image) planned for Sprint 4.
- **AI Features**: AI Q&A Chatbot (C59) planned for Sprint 7+; Explain This Metric (C56) provides interactive educational AI-adjacent explanations.
- **Visual Analysis**: PPT-style visuals already implemented; Sector Heatmap (C51) and Sector Rotation Visualizer (C61) in progress.
- **Notifications**: ❌ MISSING — no current plans for push, in-app, or email notifications.
- **Glossary/Tooltips**: ❌ MISSING — C33 (Glossary) not yet scheduled despite being a core educational tool.
- **Risk Visualization**: C44 (Risk Analysis MVP) in progress for Sprint 3.
- **Daily Engagement**: Daily Market Pulse (C49) planned for Sprint 5.
- **Reflection Tools**: Investment Diary (C55) planned for Sprint 6.
- **Gamification**: Concept Mastery Badges (C60) planned for Sprint 5.
- **Onboarding**: Beginner Onboarding Flow (C58) planned for Sprint 5.
- **Interactive Education**: Explain This Metric (C56), Compare Concepts (C57), Pre-Investment Checklist (C62) cover interactive learning.
- **Sector Rotation**: Sector Rotation Visualizer (C61) planned for Sprint 6 adds time dimension to sector analysis.

**Key Insights from Round 12:**
1. Social learning dominates engagement (eToro CopyTrader, 富邦e富 following, Webull community, Tastytrade live streams).
2. AI is becoming table stakes in TW broker apps (富邦e富 AI Compass, 元大證券 AI Chatbot, 永豐金 AI Alerts).
3. Interactive education is the new standard (Magnify.money AI Visual Explanations, 永豐金 Financial Statement Visualizer, Robinhood metric tooltips).
4. Onboarding is critical for beginner retention (玉山證券 Beginner Village, Robinhood First Stock, eToro Virtual Portfolio).
5. Gamification drives learning engagement (Robinhood Learn→Earn, Khan Academy badges, Finimize certificates).
6. TW broker apps with integrated education features are direct competitors, requiring Stock Explorer to deepen its historian differentiation.
7. Reflection tools remain a white space (元大證券 Investment Diary, Tastytrade Trade Journal) — a unique historian opportunity.

**Emerging Gaps for Round 13 Consideration:**
- **Notifications**: Missing engagement loop to bring users back for learning moments.
- **Static Educational References**: Lack of always-available glossary/tooltips for just-in-time learning.
- **Passive Social Learning**: Opportunity to leverage anonymous aggregated behavior for community insights without compromising privacy or historian focus.
- **AI-Augmented Historical Narratives**: Potential to use AI for deeper historical contextualization while avoiding predictive stock-picking.
- **Structured Learning Paths**: Beyond isolated features, a guided curriculum could strengthen the education platform positioning.

### Direction A: Company Story Timeline (C34)
- Description: A visual, interactive timeline showing key historical events (product launches, leadership changes, regulatory shifts, market cycles) that shaped a company's present state. Each event includes a plain-language explanation of its impact, connecting past to present. This is the purest expression of the "historian" positioning — showing how history explains the present, not predicting the future.
- Technical Approach: 
  - Leverage existing `adaptive_engine.py` (event detection, freshness checking) to identify significant events from news and financial data.
  - Create a new service `historical_timeline.py` in `src/services/` that processes event data into a chronological narrative.
  - Use the `chart.py` service (or a new timeline-specific chart service) to generate an interactive timeline visualization (e.g., using Plotly or Streamlit's native timeline components).
  - The View (`src/pages/business_card.py` or a new timeline page) receives event data from the service and renders the UI.
  - Data layer remains unchanged; FinMind client provides raw news and fundamental data; service layer computes event significance and impact.
- Pros: 
  - Directly addresses the #1 competitor gap identified in Round 7 (no TW competitor has this).
  - Perfect alignment with "historian, not stock picker" — focuses on causal historical explanation.
  - Reuses existing event detection and data pipelines.
  - High educational value: users learn to see companies as evolving stories.
  - Can be implemented incrementally (start with major event types).
- Cons: 
  - Requires defining what constitutes a "significant historical event" (may need domain knowledge).
  - Potential overlap with planned C48 (Company Story Card) and C55 (Investment Diary); needs clear scoping.
  - UI/UX complexity for presenting timelines cleanly on mobile and desktop.
- Effort: 16-24h (includes service creation, timeline chart component, content definition for event types, View integration).
- Risks: 
  - Risk of veering into stock-picking if event implications are framed predictively (mitigate by strict tone guidelines: "This event led to X outcome in the past" not "This event will cause Y").
  - Dependency on C38 (Compare Stories Phase 1) for data structures; if C38 delays, may need to adjust.
  - Content creation effort for event templates and impact explanations.

### Direction B: Notification System for Learning Engagement
- Description: A lightweight, opt-in notification system that delivers timely educational nudges to encourage learning and re-engagement. Examples: "New analogy added for ROE — check it out!", "Your investment diary has an unwritten entry for TSMC", "Daily market fact: Semiconductor sector up 2% this week", "You haven't explored the Pre-Investment Checklist for this week's featured stock". Notifications appear as in-app toasts/banners and optionally as email digests.
- Technical Approach:
  - Use Streamlit's `st.toast()` or custom CSS-based banners for in-app notifications (View layer responsibility).
  - Track user state (companies viewed, features used, diary entries, checklist completion) in `session_state` (Router/View layer, adhering to session_state conventions).
  - Implement a notification service (`src/services/notification_service.py`) that evaluates conditions and returns notification data (no side effects; pure function taking session_state and config).
  - Router layer triggers notification check on `st.rerun()` and passes notifications to View for display.
  - For email digests (optional future extension), would require external service; start with in-app only to keep scope manageable.
  - No changes to data layer; all state is ephemeral (session_state) or configured via YAML (e.g., notification templates in `src/data/notification_templates.yaml`).
- Pros: 
  - Addresses the critical notifications gap and supports daily engagement (Insight #4).
  - Low technical risk: uses existing session_state patterns and Streamlit toast API.
  - Aligns with historian positioning by nudging users toward reflection and learning (not trading actions).
  - Can be implemented as a standalone feature with minimal dependencies.
  - Increases retention by bringing users back to the app for educational moments.
- Cons: 
  - Requires careful design to avoid annoyance; must be opt-in and frequency-controlled.
  - Limited to active session unless extended to email/push (which would increase complexity).
  - Does not directly add new educational content; acts as an engagement layer.
- Effort: 8-12h (service, YAML templates, View integration, toast/banner styling, session_state updates in relevant pages).
- Risks: 
  - Over-notification could degrade UX (mitigate with user controls and smart frequency capping).
  - Session-state-only persistence means notifications reset on refresh (acceptable for MVP; persistent storage would require D22 persistence layer).
  - Potential for notification fatigue if not tied to meaningful learning milestones.

### Direction C: AI-Augmented Historical Narrator
- Description: An AI-powered feature that generates plain-language historical narratives from financial and event data, answering questions like "How did this company get to where it is today?" or "What past events explain this year's revenue change?" The AI is constrained to strictly historical, factual explanations (no future predictions, no buy/sell advice) and outputs are templated and reviewed for tone compliance. Integrates with the existing analogy engine and financial metrics service to enrich narratives with data-driven insights.
- Technical Approach:
  - Create a new service `historical_narrator.py` in `src/services/` that takes financial metrics, company facts, and event data as input.
  - Use pattern matching or rule-based AI (not LLM) to map data points to pre-written historical narrative templates (e.g., "Revenue growth driven by [product] launch in [year], which increased market share by X%").
  - For more advanced natural language, could integrate with a lightweight LLM API (e.g., via OpenRouter) but with strict prompt engineering to enforce historian tone and avoid stock-picking; however, to minimize risk and complexity, start with template-based approach.
  - Output is plain text that can be displayed in the View (e.g., as a section on the business card or in a new "Company Story" page).
  - Service layer does not call FinMind API directly; receives processed data from router (like other services).
  - No changes to data layer; reuses `financial_metrics.py`, `company_facts.py`, `adaptive_engine.py` outputs.
- Pros: 
  - Leverages AI trend (Insight #2) while maintaining historian positioning by focusing on past explanations.
  - Builds on existing analogy engine and financial metrics services — low coupling.
  - Provides dynamic, contextualized explanations that adapt to the user's selected stock and timeframe.
  - Can start with template-based MVP and evolve to LLM if proven valuable.
  - Differentiates from competitors who use AI for stock-picking or predictive analytics.
- Cons: 
  - Template-based approach may feel repetitive; LLM integration increases complexity and risk of tone violations.
  - Requires careful curation of narrative templates and validation rules to prevent drifting into analysis or prediction.
  - May overlap with planned C56 (Explain This Metric) and C59 (AI Q&A Chatbot); needs clear boundaries.
- Effort: 12-18h for template-based MVP (service, template YAML, View integration, tone guidelines). LLM integration would add 8-16h.
- Risks: 
  - Tone violation risk if AI generates predictive or prescriptive language (mitigate with strict template whitelisting and/or LLM output filtering).
  - Dependency on quality of input data services; if financial_metrics or company_facts have gaps, narratives may suffer.
  - User expectations may exceed capabilities if marketed as "AI" (manage expectations by emphasizing historical, not predictive, nature).

### Recommendation
For Round 13 discussion, the team should prioritize **Direction A: Company Story Timeline (C34)** as the primary feature to discuss. It directly addresses the most significant competitor gap (reflection tools/historian white space) identified in early research, aligns perfectly with the core positioning, and reuses existing event detection infrastructure. While Direction B (Notification System) is valuable for engagement, it is secondary to delivering core historian value. Direction C (AI-Augmented Historical Narrator) offers intriguing potential but carries higher tone risk and may be better explored after the education core (C56, C57, C62) stabilizes.

**Suggested Discussion Points:**
1. Scope C34 to focus on 3-4 major event types (e.g., product launches, leadership changes, regulatory events, market cycles) to keep effort manageable.
2. Ensure C34 complements, not duplicates, C48 (Company Story Card) by defining C34 as the deep historical narrative and C48 as the curated present-day story.
3. Prototype a minimal timeline View using Streamlit's existing components before investing in custom charting.
4. Consider tying C34 to C55 (Investment Diary) by allowing users to attach diary entries to specific timeline events.
5. Defer notification system to after C58 (Onboarding) is stable, as onboarding is prerequisite for effective engagement features.

This direction strengthens Stock Explorer's unique historian moat and delivers on the promise of helping users understand "how we got here" rather than guessing "what comes next."