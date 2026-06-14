## 2026-06-15 Design Review — Discussion Round 45

### Feature Direction Evaluations

#### 1. C170: Tappable Glossary (inline metric definitions)
- UX Impact: Positive for beginners — reduces friction in understanding terminology without disrupting learning flow
- PPT-style Alignment: Good — supports image-first approach by keeping definitions contextual and non-intrusive
- Ten-second Test: Positive — helps beginners quickly grasp term meanings to comprehend core concepts faster
- Design Direction: Subtle hover/tap tooltip using tip card style (orange border, #FFF8F0 background) with concise plain-language definition (1 sentence max). Place metric labels with dotted underline indicator.
- Pitfalls: Overuse could clutter interface; definitions must be rigorously vetted for accuracy and simplicity; ensure touch targets meet accessibility standards
- Competitor Reference: FinChat, StockStory, Finimize implementations; Investopedia's financial dictionary sets the standard for beginner-friendly definitions

#### 2. C152: Multi-Factor Event Narratives
- UX Impact: Positive for beginners — transforms complex multi-factor events into single coherent stories
- PPT-style Alignment: Excellent — embodies "one key point per page" with narrative as text supplement to supporting visuals
- Ten-second Test: Positive — a beginner should understand what happened to the stock within ten seconds from the narrative
- Design Direction: Narrative card at top of Event Dashboard using info card style (blue border, #F8F9FA background) with bold headline and 1-2 sentence plain-language explanation. Include "Show factors" toggle for detail expansion.
- Pitfalls: Risk of oversimplification; must maintain historical accuracy and avoid implying causation without evidence; balance simplicity with completeness
- Competitor Reference: Public.com's "Spiking" model for event explanations; Cake Finance's narrative comparison approach; Seeking Alpha's "Smart Comment" summaries

#### 3. C175: NL-First Screening
- UX Impact: Very positive for beginners — lowers discovery barrier by allowing natural language queries instead of requiring metric knowledge
- PPT-style Alignment: Good — search box in Navbar (Zone A) follows existing pattern; results page must adhere to PPT style (one key point per result)
- Ten-second Test: Positive — helps beginners find relevant stocks quickly to begin their learning journey
- Design Direction: Prominent search box in Navbar (replacing current search) with placeholder examples like "Show me dividend stocks" or "Which companies make chips?". Use NL processing to interpret intent and show understood query confirmation.
- Pitfalls: NL processing errors could frustrate users; must clearly show system interpretation; provide fallback to traditional screening; avoid over-promising capabilities
- Competitor Reference: Screenful's natural language screening interface; Koyfin's NL search; Simply Wall St's question-based discovery

#### 4. C184: Natural Language Q&A
- UX Impact: Very positive for beginners — allows questioning in familiar language without needing to know specific metrics to ask about
- PPT-style Alignment: Good — Q&A results should follow PPT style: one clear answer with visual support (chart/icon) as primary element
- Ten-second Test: Positive — answers must be concise enough to pass the ten-second test (beginner can restate core information)
- Design Direction: Chat-like interface in Main Content Area (Zone C) with clear visual separation. Use tip cards for answers, suggest example questions, and always cite data sources. Include follow-up question suggestions.
- Pitfalls: AI hallucinations risk; must ground responses in structured data with source citations; manage expectations about answer scope; avoid overwhelming with lengthy responses
- Competitor Reference: Koyfin's natural language Q&A; Investopedia's AI explanation features; Finimize's "Ask Finimize" functionality

#### 5. C188: Why Did This Stock Move? (inline AI explanations)
- UX Impact: Positive for beginners — explains price movements in accessible language rather than leaving users to interpret charts alone
- PPT-style Alignment: Good — inline explanations should be brief and visually supported (e.g., small callout near price change)
- Ten-second Test: Positive — explanations should be short enough to grasp quickly while maintaining accuracy
- Design Direction: Small callout near significant price change indicators (in Zone A navbar or above charts) using tip card style. Trigger only for meaningful moves (>3% daily change). Use historical language ("when X happened, Y typically followed").
- Pitfalls: Risk of implying causation or predictive insight; must use careful historical language; avoid over-explaining minor fluctuations; ensure explanations don't become noise
- Competitor Reference: Public.com's event explanation model; Spiking's real-time alerts with context; Yahoo Finance's "Why it's moving" tags

#### 6. C194: Explain Why Good/Bad (metric judgment callout)
- UX Impact: Very positive for beginners — builds intuition about what makes metrics favorable or unfavorable through contextual explanations
- PPT-style Alignment: Excellent — adds educational layer to existing metric displays without altering core PPT layout or adding clutter
- Ten-second Test: Positive — helps beginners quickly learn judgment criteria for key metrics
- Design Direction: Small question-mark badge or icon next to metric labels that expands to plain-language explanation on hover/tap. Reuse the "Explain This Number" pattern from C139. Apply selectively to 3-4 key metrics per page.
- Pitfalls: Must avoid overwhelming with too many callouts; focus only on metrics where judgment is non-obvious; ensure explanations are accurate, unbiased, and educational rather than advisory
- Competitor Reference: Morningstar's transparency in metric ratings; Inderes' detailed metric explanations; Gurufocus' "Why this matters" callouts; Note: current research indicates no competitor explains reasoning behind good/bad labels — this is a unique opportunity

#### 7. C196: Daily Market Story (3-min daily narrative for retention)
- UX Impact: Very positive for beginners — provides regular, digestible market education that builds habit and retention
- PPT-style Alignment: Excellent — each story should embody PPT principles: one key point, visual-first, with text as supplement
- Ten-second Test: Each story must be designed so beginners can grasp the core concept within ten seconds (headline + visual)
- Design Direction: Dedicated page/section with consistent template: headline, 1-2 sentence summary, supporting visual (chart/map/trend graphic), optional 3-minute audio narration. Use story card layout with clear visual hierarchy.
- Pitfalls: Must maintain consistent quality and avoid repetition; ensure stories are truly educational (explaining "why") not just news reporting; balance timeliness with enduring insights
- Competitor Reference: Finimize's daily lessons; Acorns' Grow Magazine educational content; Morning Brew's newsletter-style explanation; Simply Wall St's weekly visual stories

### Overall Design Recommendations
Top design priorities based on UX impact, principle alignment, and competitive landscape:

1. **Prioritize features that directly support the "ten-second test"** — C170 (Tappable Glossary), C194 (Explain Why Good/Bad), and C196 (Daily Market Story) all help beginners grasp concepts quickly. These have high impact with relatively low implementation effort.

2. **Maintain strict PPT-style compliance** — All new features must adhere to the one-key-point-per-page principle, with visuals as the primary element. C152 (Multi-Factor Event Narratives) and C196 (Daily Market Story) are particularly well-suited to this approach.

3. **Leverage existing design patterns** — Reuse established components like tip cards (C139, C194), info cards, and the explanation pattern from C139 to ensure consistency and reduce cognitive load.

4. **Focus on beginner onboarding flow** — Features like C175 (NL-First Screening) and C170 (Tappable Glossary) lower barriers for new users. Consider integrating these into a cohesive beginner experience.

5. **Avoid feature bloat through progressive disclosure** — Use toggles, expandable sections, and contextual hints to show advanced information only when requested, maintaining clean interfaces for beginners.

6. **Ensure historical accuracy in all narratives** — Features like C152, C188, and C196 must rigorously adhere to the "historian, not stock picker" principle — explaining what happened without implying predictive insight or giving advice.

The designer should advocate for implementing C170, C194, and C196 in the next sprint as they collectively address beginner comprehension, retention, and judgment skills — core weaknesses identified in competitor research. These form a cohesive "beginner comprehension toolkit" that aligns strongly with Stock Explorer's educational positioning.