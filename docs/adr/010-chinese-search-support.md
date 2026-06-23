# ADR-010: Chinese Stock Name Search Support

## Status
Proposed

## Context
The Stock Explorer application currently has a search box in the sidebar that supports:
1. Stock ID lookup (numeric input, e.g., "2330")
2. Limited Chinese name lookup via a hardcoded YAML mapping (config/chinese_names.yaml)
3. English name/partial match fallback via FinMind API

User feedback (UX-01) requests full Chinese stock name search support. Currently, the YAML mapping only contains ~14 entries, making it ineffective for most Taiwanese stocks.

Upon investigation, the backend FinMindClient already provides comprehensive search capability via the `search_stocks()` method (src/data/finmind_client.py:263-278), which searches both stock_id (exact match) and stock_name (partial match, including Chinese characters).

However, the current frontend implementation in src/main.py (lines 264-292) does not leverage this backend capability effectively:
- It first checks if input is numeric (stock ID)
- If not numeric, it ONLY checks the limited YAML mapping
- Only if NOT found in YAML does it fall back to searching all stocks via get_all_stocks()
- This creates a suboptimal user experience where most Chinese stock names fail to resolve

## Decision
We will enhance the search functionality to leverage the existing FinMindClient.search_stocks() method, which provides comprehensive search capabilities for both stock IDs and Chinese/English stock names.

## Alternatives Considered

### Approach 1: Enhance existing YAML mapping (Status Quo Enhancement)
**Pros:**
- Minimal code changes
- Leverages existing caching mechanism in get_chinese_name_mapping()
- No additional API calls beyond current implementation

**Cons:**
- Requires maintaining and expanding YAML mapping with thousands of stock names
- Difficult to keep synchronized with FinMind database
- Still limited to exact matches only (no partial matching)
- Poor scalability

### Approach 2: Replace YAML mapping with direct FinMind search (Recommended)
**Pros:**
- Leverages existing, robust search_stocks() method in FinMindClient
- Provides exact stock_id matching AND partial stock_name matching (Chinese & English)
- Automatically stays current with FinMind database
- Eliminates need for manual YAML maintenance
- Provides better user experience with partial matching capabilities

**Cons:**
- Slightly more API calls (but mitigated by Streamlit caching)
- Requires minor refactoring of search logic in src/main.py

### Approach 3: Hybrid approach (YAML cache + FinMind fallback)
**Pros:**
- Fast lookup for common stocks via YAML
- Fallback to comprehensive search for edge cases

**Cons:**
- Increased complexity
- Cache invalidation challenges
- Still requires YAML maintenance
- Most complex implementation

## Recommendation
**Approach 2: Replace YAML mapping with direct FinMind search**

We will modify the search logic in src/main.py to:
1. First check if input is numeric (stock ID validation)
2. If numeric, validate using existing validate_stock_id() function
3. If not numeric, directly call FinMindClient.search_stocks() to search both stock_id and stock_name
4. Handle results appropriately (exact match, multiple matches, no matches)

This approach leverages the existing robust backend capability while simplifying the codebase by removing the need for manual YAML maintenance.

## Implementation Plan
1. Modify src/main.py search logic (lines 264-292):
   - Remove dependency on get_chinese_name_mapping() and config/chinese_names.yaml
   - For non-numeric input, call client.search_stocks(query) instead
   - Handle the DataFrame results to extract stock_id(s)
   - Maintain existing UX patterns for single/multiple/no matches
2. Remove unused get_chinese_name_mapping() function and its cache
3. Optionally remove config/chinese_names.yaml (or keep as fallback/deprecated)
4. Update any relevant documentation

## Data Flow Changes
**Current Flow:**
```
User Input → [is numeric?] 
   → Yes: validate_stock_id() → stock_id
   → No:  check chinese_names.yaml → stock_id? 
          → Yes: use stock_id
          → No:  get_all_stocks() → filter stock_name.contains() → stock_id(s)
```

**Proposed Flow:**
```
User Input → [is numeric?]
   → Yes: validate_stock_id() → stock_id
   → No:  client.search_stocks(query) → DataFrame results
          → If 1 row: use stock_id from result
          → If >1 rows: show selectbox with options
          → If 0 rows: show not found error
```

## Consequences

### Positive Outcomes
- Full Chinese stock name search support with partial matching
- Automatic synchronization with FinMind database (no manual YAML updates needed)
- Simplified codebase (removes YAML parsing logic)
- Better user experience (partial matching, not just exact matches)
- Leverages existing, tested, cached backend functionality

### Negative Outcomes
- Slight increase in API calls for Chinese name searches (mitigated by @st.cache_data)
- Removal of YAML file may break any external dependencies on it
- Need to ensure search_stocks() performance is adequate for UI responsiveness

### Implementation Risks
- Low: The search_stocks() method already exists and is tested
- Low: Streamlit caching will minimize API call impact
- Low: Maintaining backward compatibility during transition

## Implementation Notes
1. The search_stocks() method in FinMindClient already implements:
   - Exact match on stock_id (mask_id)
   - Partial match on stock_name (mask_name using str.contains)
   - Returns pandas DataFrame with matching results
2. We should preserve the existing UX patterns:
   - Stock ID validation with error messages
   - Single result: auto-select
   - Multiple results: selectbox for disambiguation
   - No results: error message
3. Consider adding a loading state for search operations
4. The existing get_all_stocks() function may become redundant and could be deprecated

## Related Files
- src/main.py: Search logic modification (lines 264-264-292)
- src/data/finmind_client.py: Contains search_stocks() method (already implemented)
- config/chinese_names.yaml: To be deprecated/removed
- docs/overview/02-architecture.md: Document data flow changes if needed

## Success Metrics
- Users can search for Taiwanese stocks using Chinese names (partial or full)
- Search returns relevant results quickly (leveraging existing caching)
- No regression in stock ID search functionality
- Reduced code complexity and maintenance overhead