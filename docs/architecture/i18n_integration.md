# i18n Integration Design

## Goal
Wire the existing i18n module (`src/core/i18n.py`) into all user-facing strings in the codebase, replacing hardcoded strings with calls to `t("key.path")`. Add missing keys to the locale YAML files (`locales/zh-TW.yaml` and `locales/en.yaml`) as needed.

## Scope
- All Python files in `src/` directory that contain user-facing strings (UI labels, messages, tooltips, etc.).
- Exclude developer-facing strings (e.g., log messages, internal variable names).

## Approach
1. **Identify hardcoded strings**: Scan the codebase for strings passed to Streamlit functions (e.g., `st.write`, `st.label`, `st.button`, `st.warning`, `st.error`, `st.info`, `st.success`, `st.markdown` with plain text, etc.) that are not already wrapped in `t()`.
2. **Extract keys**: For each hardcoded string, generate a translation key based on the file path and context (e.g., `pages.router.nav_label`, `pages.business_card.section.title`).
3. **Update source files**: Replace the hardcoded string with `t("generated.key")`.
4. **Update locale files**: Add the key and its translation (in both zh-TW and en) to the respective YAML files. If the string already exists in the locale files (possibly from previous i18n efforts), reuse the existing key.
5. **Maintain consistency**: Use a consistent naming convention for keys (e.g., using dot notation, mirroring the file hierarchy).
6. **Verify**: Ensure that the UI still functions correctly and that all strings are properly translated when switching languages.

## Naming Convention for Translation Keys
- Use the format: `<module>.<submodule>.<component>.<purpose>`
- Example: `pages.router.nav_label` for the navigation label in the router.
- For strings within a specific component (e.g., a button in a section), use: `pages.business_card.section.header.button.label`.
- Avoid overly granular keys; group similar strings if appropriate (e.g., all labels in a form can share a common prefix).

## Handling Plurals and Variations
- If a string has variations (e.g., singular/plural), create separate keys for each variation.
- Use string formatting within the translation function for dynamic values (e.g., `t("pages.button.delete", count=5)` → "Delete 5 items").

## Fallback Mechanism
- The existing `t()` function returns the key itself if the translation is not found, which prevents crashes. However, we aim to have 100% coverage for all user-facing strings.

## Files to Modify
- All `.py` files under `src/` that contain user-facing strings.
- `locales/zh-TW.yaml`
- `locales/en.yaml`

## Implementation Steps
1. Run a script to collect all hardcoded strings in `src/` (optional but helpful).
2. For each file, manually replace strings (or use the script to generate replacements).
3. Update the locale files with the new keys and translations.
4. Test by switching languages in the UI and verifying that all strings appear correctly.

## Notes
- The i18n module already provides a `t()` function that supports nested keys via dot notation and string formatting.
- The locale files are YAML dictionaries; ensure proper indentation and structure.
- Do not modify functionality; this is a pure string extraction task.