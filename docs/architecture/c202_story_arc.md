# Story Arc Detector Architecture (C202)

> This document describes the architecture of the Story Arc Detector service and its integration with the Story Timeline page.

## Overview

The Story Arc Detector is a pure Python service that analyzes a company's event timeline to detect narrative arcs (growth, decline, volatile, recovery) over time. It is used by the Story Timeline page to display arc badges at transition points.

## Layer Placement

- **Service Layer**: `src/services/story_arc_detector.py`
  - Pure business logic, no Streamlit imports, no direct API calls.
  - Receives `TimelineEntry` objects (already loaded by the data layer) and returns arc labels as i18n keys.
  - Follows the service layer conventions: no side effects, pure functions.

- **Presentation Layer**: `src/pages/story_timeline.py`
  - View layer responsible for rendering UI with Streamlit.
  - Calls the service to get arc labels (i18n keys) and resolves them via `t()` function.
  - Renders arc badges and legend using resolved text.

## Data Flow

```mermaid
graph TD
    A[Timeline Service] -->|TimelineEntry list| B[Story Arc Detector]
    B -->|ArcLabel list (i18n keys)| C[Story Timeline Page]
    C -->|Resolve keys via t()| D[Streamlit UI]
```

1. **Data Layer**: `src/services/timeline_service.get_timeline()` returns a list of `TimelineEntry` objects (each with date, type, severity, etc.).
2. **Service Layer**: `story_arc_detector.detect_arcs()` processes the entries into 6-month buckets, scores them, and classifies each bucket into an arc type. It returns a list of `ArcLabel` dicts containing:
   - `arc_key`: i18n key for arc type (e.g., `"growth"`)
   - `arc_emoji`: emoji for the arc
   - `arc_description_key`: i18n key for description
   - `bucket_start`, `bucket_end`: date range of the bucket
   - `event_count`: number of events in the bucket
   - `score`: severity-weighted score
3. **Presentation Layer**: `story_timeline.py` receives the `ArcLabel` list, calls `t()` on the keys to get localized strings, and renders the badges.

## i18n Integration

- The service returns **keys**, not display text, to keep the service layer free of UI concerns.
- The page layer calls `t()` to resolve keys to localized strings.
- All arc-related keys are stored in the locale YAML files under the `story_arc.` namespace.

### Example Keys

```yaml
# In locales/zh-TW.yaml
story_arc:
  growth: "成長"
  decline: "衰退"
  volatile: "波動"
  recovery: "復甦"
  growth_description: "公司在這個時期展現出強勢的成長動能..."
  # ... etc.
```

## Dependencies

- **Input**: `TimelineEntry` list from `src/services.timeline_service.get_timeline()`
- **Output**: Arc label list for UI rendering
- **No direct dependencies on**: FinMind API, Streamlit, caching

## Error Handling

- If the input entry list is empty, returns an empty list.
- Invalid dates are skipped during bucket assignment.
- Buckets with fewer than `min_events` (default 3) are classified as no label (`""`).
- The service does not raise exceptions; it returns empty lists or default values on edge cases.

## Performance

- Time complexity: O(n log n) due to sorting bucket keys (n = number of entries)
- Space complexity: O(n) for bucketing entries
- Typically called with timeline data of ~50-200 entries, so performance is negligible.

## Security

- No user input is passed directly to the service; all data comes from trusted timeline service.
- No file I/O or network calls.

## Testing

- Unit tests in `tests/services/test_story_arc_detector.py` cover:
  - Bucket key calculation
  - Label classification
  - Arc detection logic
  - Edge cases (empty input, insufficient events, boundary conditions)
  - i18n key format (ensuring keys are English and not Chinese)