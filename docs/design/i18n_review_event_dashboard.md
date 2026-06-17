# i18n Review: event_dashboard.py

## Overview
This document reviews the internationalization (i18n) status of `src/pages/event_dashboard.py` and its backup file `.backup`.

## Findings

### Current File (`src/pages/event_dashboard.py`)
The file has been partially i18n'd but still contains numerous hard-coded Chinese strings that should be replaced with `t()` calls.

#### Hard-coded Strings Requiring i18n:
1. **Page Header**
   - Line 51: `st.markdown(\"## 🔔 事件儀表板\")`
   - Line 52: `st.markdown(\"*近期市場重大事件與異動*\")`

2. **Section Headers**
   - Line 56: `st.markdown(\"### 📋 近期重大事件\")`
   - Line 61: `st.info(\"近期無重大事件記錄。事件會在瀏覽股票頁面時自動偵測。\")`

3. **Event Details**
   - Line 100: `st.caption(f\"💡 核心概念：{interp['key_concept']}\")` - "核心概念：" is hard-coded
   - Line 113: `st.button(\"🔍 為什麼？\", key=f\"why_{evt_idx}\")` - button text is hard-coded
   - Line 127: `st.caption(\"⚠️ 以上解讀僅說明事件背景與可能意涵，不構成投資建議。\")` - full caption is hard-coded

4. **Usage Explanation Section**
   - Line 133: `st.markdown(\"### 💡 關於事件儀表板\")`
   - Lines 134-144: The entire markdown block explaining event types is hard-coded Chinese

5. **Adaptive Banner**
   - Line 162: `_info_card(title=f\"🎯 分析框架：{framework['name']}\", ...)` - "分析框架：" is hard-coded
   - Line 163: `content=f\"{framework['description']} — {framework['focus']}\"` - While the framework data may be dynamic, the static text " — " is not translatable but acceptable as a separator

6. **Event Alerts**
   - Line 181: `title=f\"🔴 近期有 {len(high_events)} 項重大事件需要注意！\"` - hard-coded
   - Line 191: `title=f\"🟡 近期有 {len(medium_events)} 項注意事件\"` - hard-coded

### Backup File (`src/pages/event_dashboard.py.backup`)
The backup file contains the same hard-coded strings as the current file, indicating that the i18n work was not applied to this version. Since it's a backup, it should either be updated or removed to avoid confusion.

## Recommendations
1. Replace all hard-coded Chinese strings with appropriate `t()` calls.
2. Create translation keys in `locales/zh-TW.yaml` and `locales/en.yaml` for each string.
3. Follow the existing naming convention: `<module>.<submodule>.<component>.<purpose>`
   - Example: `event_dashboard.page_header`, `event_dashboard.section.recent_events`, etc.
4. For strings with dynamic values (like counts), use string formatting in the translation.
   - Example: `t(\"event_dashboard.alerts.high_count\", count=len(high_events))`
5. Consider extracting the event type labels and severity badges to i18n as well, though note that emojis are not translatable.
6. Remove or update the backup file to prevent accidental use of non-i18n'd code.

## Notes
- The file already uses `t()` for the data sources section (lines 149-151), which is a good practice to follow.
- The `_severity_badge` and `_event_type_label` functions return hard-coded strings with emojis. Consider if these should also be i18n'd (the text part, keeping emojis static).
- All user-facing strings in the presentation layer should go through `t()` to support language switching.

## Related Files
- `src/core/i18n.py` - the translation function
- `locales/zh-TW.yaml` - Chinese translations
- `locales/en.yaml` - English translations
- `docs/architecture/i18n_integration.md` - i18n integration guidelines
