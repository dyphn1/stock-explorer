# 2026-06-17 Design Review — C201 Daily Market Dashboard

> **Reviewer**: Designer (Stock Explorer AI Team)
> **Date**: 2026-06-17
> **Context**: Pre-implementation review of C201 Daily Market Dashboard architecture design
> **Related**: `docs/architecture/c201_daily_market.md`

## Summary

Review of the C201 Daily Market Dashboard architecture design against the Stock Explorer Design System. The design follows the historian positioning and reuses existing shared components, but contains critical color system violations that must be fixed before implementation.

## Design Compliance Assessment

### ✅ Compliant Areas

| Criterion | Status | Notes |
|-----------|--------|-------|
| **Zone Layering** | ✅ Pass | Uses Zone A (navbar) and Zone C (content only). No sidebar mixing. |
| **Component Reuse** | ✅ Pass | Reuses `_白话_card()`, `_info_card()`, `_summary_card()`, `_section_title()` from `_router_base.py`. |
| **PPT-Style Adherence** | ✅ Pass | One key point per section: Market Overview, Market Sentiment, Sector Performance, Top Movers, Key Events. |
| **Loading State** | ✅ Pass | Uses `st.spinner` during data load. |
| **Error Handling** | ✅ Pass | Shows `st.error` for data loading failures, `st.warning` for no data. |
| **Plain-Language System** | ✅ Pass | Historian tone throughout, no investment advice. |
| **Ten-Second Test** | ✅ Pass | Clear purpose: "What happened in the Taiwan market today?" |
| **Button Keys** | ✅ Pass | Not yet implemented but follows conventions in doc. |
| **Disclaimer** | ✅ Pass | Includes educational disclaimer at page bottom. |

### ❌ Non-Compliant Areas (Must Fix)

| Issue | Location | Severity | Description | Fix |
|-------|----------|----------|-------------|-----|
| **D-C201-01: Color System Reversal** | Sector Strip (`_render_sector_strip` lines 528-529) | P1 | Gainers (positive change) shown in Red (`#E74C3C`), Losers (negative change) shown in Green (`#27AE60`). This violates the design system where Green = Positive/Up, Red = Negative/Down. | Reverse the color logic: `color = "#27AE60" if chg > 0 else ("#E74C3C" if chg < 0 else "#7F8C8D")` |
| **D-C201-02: Emoji Reversal** | Sector Strip (`_render_sector_strip` line 534) | P1 | Up count shown with 🔴 (red circle), Down count shown with 🟢 (green circle). Should be opposite to match color semantics. | Swap emojis: 🟢 for up count, 🔴 for down count |
| **D-C201-03: Inconsistent Color Usage** | Top Movers (`_render_mover_row` line 573-578) | P1 | Same color reversal issue: gainers get red, losers get green. | Fix color assignment: `color = "#27AE60" if is_gainer else "#E74C3C"` |

### ⚠️ Potential Issues (Verify During Implementation)

| Issue | Location | Status | Notes |
|-------|----------|--------|-------|
| **Text Volume in Overview** | Overview template (`daily_market.overview.template_*`) | To verify | The generated paragraph may approach 200-character PPT limit. Monitor during implementation with real data. |
| **Mobile Responsiveness** | Sector Strip (`st.columns()`) and Top Movers (`st.columns()`) | To verify | Horizontal layouts may not stack gracefully on mobile. Consider responsive fallback. |
| **Volume Comment Logic** | Overview (`volume_comment` variable) | To verify | Currently hardcoded to "normal". Should implement actual 5-day average comparison or remove if too complex for MVP. |

## i18n String Length Check

Reviewed all new i18n keys in `locales/en.yaml` and `locales/zh-TW.yaml` under `daily_market:` section:

- All section titles: < 20 characters
- All labels: < 15 characters  
- Template strings: ~100-150 characters with placeholders (acceptable for summary cards)
- Disclaimers: < 100 characters
- No strings exceed reasonable UI element constraints

## Hard-Coded Chinese String Check

- No `.backup` files found in repository
- Architecture doc shows all UI strings use `t()` function calls or template keys
- No hard-coded Chinese strings visible in design spec

## Recommendations

### Immediate Fixes (Before Development)
1. **Fix color logic** in `_render_sector_strip()` and `_render_mover_row()` to match design system:
   - Green (`#27AE60`) for positive values/up/gainers
   - Red (`#E74C3C`) for negative values/down/losers
2. **Fix emoji assignment** in sector strip to match corrected color semantics
3. **Add mobile responsiveness testing** to implementation plan

### Implementation Verification
Once Developer implements C201, verify:
1. Colors match design system in all sections
2. Emojis correctly represent up/down direction
3. i18n strings fit within UI elements (no overflow/truncation)
4. Zone separation maintained (no controls in navbar/sidebar)
5. PPT-style adhered to (one key point per section, charts > 60% of area)

## Open Questions from Architecture Doc

1. **TAIEX index data**: Verify if FinMind free tier provides direct TAIEX data or if proxy computation is needed
2. **Volume baseline**: For MVP, consider showing absolute volume only (vs 5-day average) to simplify
3. **Event filtering**: Confirm adaptive engine returns market-level events or implement post-filter
4. **Market hours handling**: Show "last trading day" indicator when market is closed

--- 
*This design review must be addressed before Developer begins implementation of C201.*