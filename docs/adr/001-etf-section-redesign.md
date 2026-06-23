# ADR-001: ETF Section Redesign

## Status
Proposed

## Context
User feedback #4: "ETF 功能與股票功能相同 — ETF 跟股票性質不同，不應該有一樣的功能"

Current state: `src/pages/etf_browser.py` mirrors stock browsing patterns (price, volume, change).
The ETF browser currently offers three subpages:
1. Hot ETFs (by trading volume)
2. ETF Categories (by keyword matching)
3. Dividend Ranking (by dividend yield)

However, ETFs are fundamentally different from stocks:
- ETFs are baskets of securities (providing diversification)
- ETFs have expense ratios, tracking error, and AUM (Assets Under Management)
- ETFs have dividend schedules and yield
- ETF comparison is more useful than individual ETF deep-dive

The current ETF browser focuses on stock-like metrics (price, volume, change) and basic categorization/dividend yield, which does not adequately serve ETF investors who need to compare ETFs based on their unique characteristics.

## Decision
We will redesign the ETF section to focus on ETF-specific metrics and comparative analysis, moving away from stock-like individual ETF deep-dives.

## Alternatives Considered

### Approach A: Enhance with ETF-specific metrics
**Pros:**
- Minimal changes to existing structure
- Adds valuable ETF metrics (expense ratio, tracking error, AUM) to existing views
- Maintains familiarity for users familiar with stock browsing

**Cons:**
- Still focuses on individual ETF deep-dives rather than comparison
- Does not fully address the core user need for ETF comparison
- Category and dividend views remain rudimentary
- Does not leverage the basket nature of ETFs

### Approach B: Redesign for ETF comparison/screening
**Pros:**
- Directly addresses user feedback about ETF vs stock differentiation
- Enables meaningful ETF comparison (side-by-side, screening)
- Highlights ETF-specific metrics (expense ratio, tracking error, AUM, holdings overlap)
- Better serves ETF investors who prioritize diversification and cost efficiency
- Provides more valuable insights than individual ETF deep-dives

**Cons:**
- Requires significant redesign of the ETF section
- May require new data fields (expense ratio, tracking error, holdings data)
- Users accustomed to individual ETF deep-dives may need adjustment
- More complex UI/UX to design and implement

### Approach C: Hybrid
**Pros:**
- Keeps some familiar individual ETF views while adding comparison tools
- Balances innovation with familiarity
- Can gradually introduce ETF-specific features

**Cons:**
- May result in a cluttered interface with competing paradigms
- Still retains some stock-like ETF views that don't fully serve ETF investors
- Development effort spread across multiple approaches

## Recommendation
**Approach B: Redesign for ETF comparison/screening**

This approach directly addresses the user feedback that ETF functionality should differ from stock functionality. ETF investors primarily want to compare funds based on cost, performance tracking, asset composition, and dividend characteristics—not individual price movements. A comparison/screening interface will provide more actionable insights for ETF investors.

## Implementation Plan
1. **Data Enhancement** (Backend)
   - Expand ETF data model to include: expense_ratio, tracking_error, aum, inception_date, replication_method, dividend_frequency
   - Enhance ETF categorization with standardized taxonomies (e.g., asset class, region, sector, strategy)
   - Consider adding holdings overlap data for comparison features

2. **UI Redesign** (Frontend)
   - Replace current three-tab structure with:
     * **ETF Screener**: Filter by asset class, region, sector, expense ratio, AUM, dividend yield, etc.
     * **ETF Compare**: Side-by-side comparison of selected ETFs (up to 5) showing key metrics side-by-side
     * **ETF Categories**: Enhanced categorization with standardized taxonomies and performance comparisons between categories
     * **ETF Details** (optional): Simplified view focusing on ETF-specific metrics rather than stock-like price/volume

3. **User Flow Changes**
   - Remove individual ETF deep-dive as primary focus (keep as optional detailed view)
   - Emphasize comparison tools and screening capabilities
   - Highlight expense ratios and tracking errors prominently in comparisons
   - Show holdings overlap and correlation matrices for selected ETFs

4. **Data Integration**
   - Enhance FinMind client or add new data sources for ETF-specific metrics
   - Consider integrating with external ETF data providers if needed
   - Ensure data is updated regularly (expense ratios change infrequently, AUM daily)

5. **UI/UX Design**
   - Use comparison tables with sortable columns
   - Implement screening sliders and dropdowns for common ETF filters
   - Visualize holdings overlap with Venn diagrams or correlation heatmaps (for advanced compare)
   - Keep dividend yield and dividend history views but enhance with ETF-specific context

6. **Migration Plan**
   - Keep existing ETF browser temporarily during transition
   - Deploy new ETF section alongside existing one
   - Gather user feedback and iterate
   - Deprecate old ETF browser after validation

## Consequences
### Changes
- `src/pages/etf_browser.py` will be replaced with new ETF comparison/screening pages
- Potential new components: `etf_screener.py`, `etf_compare.py`, `etf_categories_enhanced.py`
- Backend enhancements to FinMind client or new ETF data service
- UI components for comparison tables, screening controls, and visualization widgets

### Breaking Changes
- Removal of current ETF browser navigation (hot ETFs, categories, dividend ranking as currently implemented)
- Users will need to adapt to new comparison/screening paradigm
- Bookmarked links to specific ETF detail views may need redirection (if we keep detailed view)

### Positive Outcomes
- Addresses user feedback directly about ETF vs stock differentiation
- Provides more valuable tools for ETF investors (cost comparison, tracking error analysis)
- Positions the platform as ETF-focused rather than treating ETFs as just another stock type
- Enables better investment decisions through comparative analysis

### Risks
- Development effort for new UI and data enhancements
- Potential user confusion during transition
- Dependence on availability of ETF-specific data (expense ratios, holdings)

### Success Metrics
- User engagement with new ETF comparison/screening features
- Positive user feedback on ETF section usefulness
- Increased time spent in ETF section compared to previous version