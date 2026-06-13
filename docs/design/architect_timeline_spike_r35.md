# Architect Analysis — C28 Story Timeline Spike (Round 35)

## Data Source Assessment

| Source | Data Available | Quality | Timeline Value |
|--------|---------------|---------|----------------|
| `adaptive_engine` (events.yaml) | 20 detected events (2026-06-07 to 2026-06-13) with stock_id, date, type, severity, title, summary | **High** — structured, dated, typed, with dedup | **Core timeline backbone** — provides the chronological event stream per stock |
| `event_interpretation_service` (C98) | 6 event-type templates (revenue_surge, news_major, news_medium, price_abnormal, dividend_change, institutional_shift) with short/detail/key_concept | **Medium** — static templates, no per-stock personalization | High — adds interpretive layer to each timeline event |
| `case_studies.yaml` (C84) | 5 historical case studies (dotcom 2000, financial crisis 2008, TSMC 2020–21, shipping 2021, AI boom 2023–24) with dates, severity, lessons, related_stocks | **High** — rich narrative, analogies, educational value | **Contextual anchoring** — provides historical parallels ("this looks like 2008") |
| `company_facts.py` | 70 facts for 7 stocks (2330, 2454, 2317, 1101, 2881, 0050) | **Medium** — static, fun facts with no dates | Low-Medium — provides "About the Company" sidebar, not timeline events |
| `news_summarizer` | Template-based news summarizer with 10 categories, impact level detection (high/medium/low) | **Medium** — keyword matching, no LLM, generates plain-language summaries | Medium — can generate timeline-friendly summaries from raw news titles |
| `story_feed.py` | Generates daily story dicts from watchlist events with analogies, historian notes, severity sorting | **Medium-High** — already composes event→story pipeline | Medium — existing pattern to reuse; already calls adaptive_engine for events |
| `market_event_service` | Thin wrapper around case_studies.yaml; filters by stock_id via related_stocks | **Low** — just a data access layer | Low — helper only |
| `news_templates.yaml` | 10 news category templates with keywords, implication strings | **Medium** — Chinese-only, static | Low — supporting data for news_summarizer |

## Key Findings

### What We Have
1. **Event pipeline is live**: `adaptive_engine.run_auto_detection()` detects revenue, news, and price events, persists them to `events.yaml` with dates, and `get_events_for_stock()` retrieves them sorted by date. This is the timeline's backbone.
2. **Interpretation layer exists**: `event_interpretation_service.get_interpretation()` provides structured explanations per event type ready for timeline display.
3. **Historical case studies provide narrative anchors**: 5 richly-written case studies with dates and stock linkages can serve as "era markers" on the timeline.
4. **Story feed already composes events into narrative**: `story_feed._event_to_story()` demonstrates the event→story conversion pattern we can extend.

### What's Missing / Weak
1. **Short event history**: events.yaml currently holds ~20 entries across 1 week. Timeline will look sparse for most stocks without backfilling or longer lookback.
2. **Company facts are undated**: company_facts.yaml has no temporal dimension — facts say "TSMC was founded in 1987" but the date isn't structured data. Can't auto-place on timeline.
3. **No milestone events**: Missing structured data for founding dates, IPO dates, product launches, leadership changes — the "big moments" that make a company story compelling.
4. **News titles are noisy**: Many detected events have clickbait titles ("今周刊", "CMoney投資網誌" sources). Timeline quality depends on title cleaning.
5. **No cross-stock relationship data**: No supply chain, competitor, or group ownership data to show interconnecting events.

## Proposed Architecture

### Option A: Event-Layered Timeline (Recommended)
**Approach**: Build `timeline_service.py` as a compose-and-enrich pipeline that merges three event streams — detected events (events.yaml), case studies (case_studies.yaml), and milestones (new yaml) — sorts by date, and attaches interpretations.

```
timeline_service.py
├── get_timeline(stock_id, lookback_days=365) → list[TimelineEntry]
│   ├── 1. Fetch detected events from adaptive_engine.get_events_for_stock()
│   ├── 2. Fetch matching case studies from market_event_service.get_events_for_stock()
│   ├── 3. Fetch company milestones from new company_milestones.yaml
│   ├── 4. Merge + sort by date
│   ├── 5. Deduplicate overlapping entries
│   ├── 6. Attach interpretation from event_interpretation_service
│   └── 7. Return enriched timeline entries
├── TimelineEntry: {date, type, severity, title, summary, 
│                    interpretation, analogy, source, icon}
```

- **Pros**: Reuses 3 existing services + data files. Minimal new code. Clear enrichment pipeline. Case studies provide historical depth.
- **Cons**: Timeline density depends on detected events (may be sparse). Milestone data doesn't exist yet (needs creation). No LLM-generated narrative.
- **Effort**: Spike = 3–5h validates pipeline. Full impl = 1–2 sprints.

### Option B: LLM-Enriched Timeline
**Approach**: Same as Option A but pass the merged event list through an LLM to generate a narrative paragraph per time period (e.g., monthly or quarterly summary).

- **Pros**: Richer narrative output. Can generate "story so far" summaries. More compelling UX.
- **Cons**: Adds LLM dependency/cost/latency. Harder to test deterministically. Overkill for spike validation.
- **Effort**: Spike = 5–8h. Full impl = 2–3 sprints. Defer to post-validation.

## Recommendation

**Go with Option A for the spike.** The key question is: *Does the composed timeline look meaningful with existing data?* The spike should:

1. Build `timeline_service.py` with `get_timeline(stock_id)` that merges events.yaml + case_studies.yaml
2. Test with stock `2317` (鴻海 — 8 events) and `2330` (台積電 — 3 events + case study links)
3. Verify timeline entries are date-sortable, deduplicated, and have clean display titles
4. Check whether 30/60/90-day lookback produces enough entries to look like a "story"

If the merged output looks compelling with 2-3 data sources, we have a green light for Sprint 16b to add milestones, improve dedup, and enrich the UI.

## Go/No-Go Criteria for Sprint 16b

1. **Timeline density**: After merging all 3 sources, at least 5 meaningful entries per stock for a 90-day lookback across 3+ test stocks. Otherwise the feature looks empty.
2. **Date quality**: Every timeline entry has a valid `date` field. No undated items leaking into the sorted output. Milestone data must be datable.
3. **Interpretation coverage**: Every event type in the timeline has a matching interpretation template. No raw/uninterpreted events in the output.
4. **Deduplication works**: Same-day events from different sources (e.g., 5 news_major about the same 法說) collapse into a single timeline entry with a count badge.
5. **Performance**: `get_timeline()` returns in <200ms for any stock with existing cached data (no API calls needed — all from local YAML).

## Data Gaps

1. **Company milestones** (founding date, IPO date, major product launches) — no structured data exists. Need `company_milestones.yaml` or similar.
2. **Sparse event history** — events.yaml only has ~1 week of data. Timeline will be sparse unless we: (a) backfill from historical news, or (b) extend lookback and accept sparse output, or (c) supplement with case studies more aggressively.
3. **No dividend events detected** — `dividend_change` event type exists in templates but no detection logic in adaptive_engine. Gap between data and template.
4. **No institutional shift detection** — Same as above. Template exists, no detector.
5. **Company facts are undated** — Would need temporal metadata (year/period) to place facts on timeline meaningfully.
6. **Clickbait title noise** — Many news titles are "阮慕驊：..." or source-stamped. Need title cleaning before timeline display.
