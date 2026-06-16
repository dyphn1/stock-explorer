"""
Input validation utilities for Stock Explorer.
"""
import re

from src.core.i18n import t


def validate_stock_id(raw: str) -> tuple[bool, str]:
    """Validate a Taiwanese stock ID.

    Args:
        raw: User-provided stock ID string (may contain whitespace).

    Returns:
        (is_valid, cleaned_or_error):
            If valid → (True, cleaned_4_digit_id)
            If invalid → (False, error_message)
    """
    cleaned = raw.strip()

    if not cleaned:
        return False, t("validation.error.empty")

    if not cleaned.isdigit():
        return False, t("validation.error.not_digit", input=cleaned)

    if len(cleaned) != 4:
        return False, t("validation.error.not_four_digit", input=cleaned, length=len(cleaned))

    if not re.match(r"^\d{4}$", cleaned):
        return False, t("validation.error.format", input=cleaned)

    return True, cleaned
