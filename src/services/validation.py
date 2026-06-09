"""
Input validation utilities for Stock Explorer.
"""
import re


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
        return False, "請輸入股票代號"

    if not cleaned.isdigit():
        return False, f"股票代號必須是數字，您輸入的是「{cleaned}」"

    if len(cleaned) != 4:
        return False, f"股票代號必須是 4 位數字，您輸入的是 {len(cleaned)} 位「{cleaned}」"

    if not re.match(r"^\d{4}$", cleaned):
        return False, f"股票代號格式不正確：「{cleaned}」"

    return True, cleaned
