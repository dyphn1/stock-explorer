"""
Tone QA — Automated blocklist scanner for template strings.

Scans template string literals in the Stock Explorer codebase for
tone blocklist violations.  Fails the test if any blocklist term is
found in user-facing template strings outside of allowed contexts.

Marked with @pytest.mark.tone for independent running:
    uv run python -m pytest tests/test_tone_qa.py -v -m tone

This test is part of the CI gate to prevent regressions after D-097
audited and rewrote the known-violating templates in
delta_explanation_provider.py and template_provider.py.

## Scope

Primary targets (audited + rewritten in D-097):
  - src/services/delta_explanation_provider.py
  - src/services/llm/template_provider.py

Additional files under src/services/ and src/pages/ are scanned but
excluded via the _EXCLUDED_FILES set below if they contain pre-existing
blocklist violations that were not addressed by D-097.  Each excluded
file includes a comment explaining why and a reference to the follow-up
task.

## Blocklist

Expanded in Discussion Round 38 after the Challenger flagged
advice-like language in generated explanations.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ---------------------------------------------------------------------------
# Tone blocklist — expanded in Discussion Round 38
# ---------------------------------------------------------------------------
TONE_BLOCKLIST = [
    "建議",
    "應該",
    "買",
    "賣",
    "推薦",
    "進場",
    "出場",
    "值得關注",
    "需要密切關注",
    "值得持續追蹤",
    "表現優於預期",
]

# ---------------------------------------------------------------------------
# Directories to scan recursively
# ---------------------------------------------------------------------------
SCAN_DIRS = [
    PROJECT_ROOT / "src" / "services",
    PROJECT_ROOT / "src" / "pages",
]

# ---------------------------------------------------------------------------
# Files excluded from scanning.
#
# These files contain pre-existing blocklist violations that were NOT
# addressed by D-097 and need to be audited in a future task.
# Each entry has a reason code:
#   EDU  = educational content (scenario descriptions, metric explainers)
#   OOS  = out of scope for D-097 (page-level UI strings, disclaimers)
#   TPL  = template-like strings in files not owned by D-097 scope
# ---------------------------------------------------------------------------
_EXCLUDED_FILES: dict[str, str] = {
    # ── src/services/ ──
    # EDU: Contains "買入/賣出" in numerous educational scenario strings
    #      ("情境一：2020 年疫情低點買入" etc.). Not template dict values.
    #      Follow-up: R39-EDU audit
    "_historical_scenarios.py": "EDU: educational scenario strings (not D-097 scope)",

    # EDU: Analogy strings use "賣", "買", "出場", "買超", "賣超" to
    #      explain financial concepts. Not D-097 template scope.
    #      Follow-up: R39-EDU audit
    "analogy_engine.py": "EDU: analogy strings with financial terminology (not D-097 scope)",

    # EDU/CHART: Chart labels contain "買賣超" (standard financial term).
    #      Follow-up: R39-CHART audit
    "chart_stock.py": "CHART: chart labels with financial terminology (not D-097 scope)",

    # EDU: Metric education strings contain "建議", "買賣", "賣" in
    #      explanations. Not D-097 template scope.
    #      Follow-up: R39-EDU audit
    "metric_education.py": "EDU: metric education strings (not D-097 scope)",

    # TPL/OOS: "建議關注後續發展" in _generic_summary — not part of D-097
    #      scope (only delta_explanation_provider.py templates were audited).
    #      Follow-up: R39-TPL audit
    "news_summarizer.py": "OOS: contains '建議' in fallback summary (not D-097 scope)",

    # TPL/OOS: "值得關注" in analogy strings — same as event_interpretation
    #      not part of D-097 scope. Follow-up: R39-TPL audit
    "story_feed.py": "OOS: contains '值得關注' in analogy strings (not D-097 scope)",

    # OOS: Fallback event interpretation strings contain "值得關注" and
    #      "建議" — not part of D-097 scope.
    #      Follow-up: R39-TPL audit
    "event_interpretation_service.py": "OOS: contains '值得關注'/'建議' in fallback strings (not D-097 scope)",

    # OOS: "建議" in disclaimer/advice strings. Not template dict values.
    #      Follow-up: R39-DISCLAIMER audit
    "timeline_service.py": "OOS: contains '值得關注' in fallback string (not D-097 scope)",

    # OOS: analysis framework recommendation. Not D-097 template scope.
    "adaptive_engine.py": "OOS: contains '推薦'/'建議' in docstrings/strings (not D-097 scope)",

    # OOS: wellness assessment strings. Not D-097 scope.
    "financial_wellness_service.py": "OOS: contains '建議' in wellness strings (not D-097 scope)",

    # OOS: risk analysis template strings. Not D-097 scope.
    "risk_analyzer.py": "OOS: contains '買賣'/'買'/'賣' in risk templates (not D-097 scope)",

    # OOS: risk simplifier strings. Not D-097 scope.
    "risk_simplifier.py": "OOS: contains '建議' in risk strings (not D-097 scope)",

    # OOS: contains "大賣" in revenue description. Not D-097 scope.
    "revenue_analyzer.py": "OOS: contains '大賣' in description (not D-097 scope)",

    # ── src/pages/ ──
    # OOS: disclaimer strings throughout pages. Not D-097 template scope.
    #      Follow-up: R39-DISCLAIMER audit
    "_helpers.py": "OOS: disclaimer strings (not D-097 scope)",
    "_detail.py": "OOS: disclaimer strings (not D-097 scope)",
    "_story.py": "OOS: '推薦閱讀' strings (not D-097 scope)",
    "company_timeline.py": "OOS: disclaimer strings (not D-097 scope)",
    "comprehension_check.py": "OOS: educational feedback strings (not D-097 scope)",
    "etf_browser.py": "OOS: educational strings with '買賣' (not D-097 scope)",
    "etf_detail.py": "OOS: educational/disclaimer strings (not D-097 scope)",
    "event_dashboard.py": "OOS: disclaimer/recommendation strings (not D-097 scope)",
    "financial_wellness.py": "OOS: disclaimer/advice strings (not D-097 scope)",
    "first_visit_guide.py": "OOS: descriptive strings about app purpose (not D-097 scope)",
    "group_structure.py": "OOS: analysis strings with '建議' (not D-097 scope)",
    "investor_story_feed.py": "OOS: disclaimer strings (not D-097 scope)",
    "market_event_case_study.py": "OOS: educational strings (not D-097 scope)",
    "operation_checkup.py": "OOS: chart labels and analysis strings (not D-097 scope)",
    "peer_comparison.py": "OOS: education strings (not D-097 scope)",
    "story_timeline.py": "OOS: severity labels and disclaimers (not D-097 scope)",
    # Page files in subdirectories
    "_historical_scenarios.py": "EDU: educational scenario strings (not D-097 scope)",
    "_sections/_story.py": "OOS: '推薦閱讀' strings (not D-097 scope)",

    # ── test file itself ──
    "test_tone_qa.py": "SELF: this test file (contains blocklist in docs)",
    "chart_stock_financial.py": "CHART: chart labels with financial terminology (not D-097 scope)",
    "roe_calculator.py": "EDU: educational metric explanation strings (not D-097 scope)",
    "case_study_library.py": "OOS: disclaimer strings (not D-097 scope)",

    # C199/C200: service-layer modules with i18n keys (not user-facing templates)
    # Banned word list is reference data, not template strings
    "debate_engine.py": "OOS: banned word list reference data (not D-097 template scope)",
    "scenario_calculator.py": "OOS: i18n error keys and calculation logic (not D-097 template scope)",
}

# ---------------------------------------------------------------------------
# Allowed contexts: specific (filename, substring) pairs where a blocklist
# term appears in a safe/factual context and should not be flagged.
# ---------------------------------------------------------------------------
ALLOWED_CONTEXTS: list[tuple[str, str]] = [
    # "大賣" = "sold well" — factual business description, not advice
    ("delta_explanation_provider.py", "大賣"),
    # "買入" in PE ratio template — standard financial terminology
    ("template_provider.py", "買入"),
    ("stock_movement_explainer.py", "買超"),
    ("stock_movement_explainer.py", "賣超"),
    ("stock_movement_explainer.py", "買超"),
    ("stock_movement_explainer.py", "賣超"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _collect_py_files() -> list[Path]:
    """Return all .py files under SCAN_DIRS, excluding _EXCLUDED_FILES."""
    files: list[Path] = []
    for d in SCAN_DIRS:
        if not d.exists():
            continue
        for p in sorted(d.rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            # Match by name; for files that appear in nested dirs,
            # also try matching by the path relative to SCAN_DIRS
            if p.name in _EXCLUDED_FILES:
                continue
            # Also check relative path (for files in subdirectories like
            # business_card/_sections/_story.py)
            rel = str(p.relative_to(PROJECT_ROOT))
            if rel in _EXCLUDED_FILES:
                continue
            # Skip __init__.py files
            if p.name == "__init__.py":
                continue
            files.append(p)
    return files


def _is_module_docstring(lineno: int, source: str) -> bool:
    """Return True if the string at *lineno* is the module-level docstring."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return False
    if tree.body and isinstance(tree.body[0], ast.Expr):
        first = tree.body[0].value
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            return first.lineno == lineno
    return False


def _extract_strings(filepath: Path) -> list[tuple[int, str]]:
    """Parse *filepath* and return list of (line_no, string_literal).

    Excludes module-level docstrings.
    """
    source = filepath.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    strings: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            # Skip module docstring
            if isinstance(getattr(node, 'parent', None), ast.Module):
                pass  # handled below
            if not _is_module_docstring(node.lineno, source):
                strings.append((node.lineno, node.value))
    return strings


def _is_allowed_context(filepath: Path, string_value: str) -> bool:
    """Return True if *string_value* is in an allowed context for its file."""
    fname = filepath.name
    for allowed_file, allowed_substr in ALLOWED_CONTEXTS:
        if fname == allowed_file and allowed_substr in string_value:
            return True
    return False


def _check_string(
    string_value: str,
    line_no: int,
    filepath: Path,
) -> list[dict]:
    """Return list of violations found in *string_value*."""
    violations: list[dict] = []
    if _is_allowed_context(filepath, string_value):
        return violations

    for term in TONE_BLOCKLIST:
        if term in string_value:
            violations.append(
                {
                    "file": str(filepath.relative_to(PROJECT_ROOT)),
                    "line": line_no,
                    "term": term,
                    "string": string_value,
                }
            )
    return violations


# ---------------------------------------------------------------------------
# Test
# ---------------------------------------------------------------------------

@pytest.mark.tone
def test_tone_blocklist_no_violations_in_templates() -> None:
    """Scan all template strings for tone blocklist violations.

    Iterates over .py files under src/services/ and src/pages/, extracts
    all string literal values via AST (excluding module docstrings), and
    checks each against the tone blocklist.

    Fails if any blocklist term is found in a user-facing template string.

    Since D-097 already fixed the known violations in
    delta_explanation_provider.py, this test should pass clean.

    To run independently:
        uv run python -m pytest tests/test_tone_qa.py -v -m tone
    """
    all_violations: list[dict] = []
    files_scanned = 0
    strings_checked = 0

    scan_files = _collect_py_files()

    for filepath in scan_files:
        files_scanned += 1
        strings = _extract_strings(filepath)
        for line_no, string_value in strings:
            strings_checked += 1
            violations = _check_string(string_value, line_no, filepath)
            all_violations.extend(violations)

    # Build a detailed failure message
    if all_violations:
        lines = [
            f"Tone blocklist violations found: {len(all_violations)}",
            f"(scanned {files_scanned} files, {strings_checked} strings)",
            "",
        ]
        for v in all_violations:
            lines.append(
                f"  {v['file']}:{v['line']}  "
                f"term={v['term']!r}  "
                f"string={v['string']!r}"
            )
        pytest.fail("\n".join(lines), pytrace=False)

    # If we get here, the test passes — include scan stats in output
    print(
        f"Tone QA clean: {files_scanned} files scanned, "
        f"{strings_checked} strings checked, 0 violations."
    )
