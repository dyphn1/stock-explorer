"""
Unit tests for the calculator card component.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ensure src/ is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def _import_calculator_card(mock_st):
    """Import the calculator_card module with mocked streamlit."""
    # Remove the module if already loaded
    mod_name = 'src.components.calculator_card'
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    # Replace streamlit with our mock
    sys.modules['streamlit'] = mock_st
    # Import the module
    module = __import__(mod_name, fromlist=['_calculator_card'])
    return module


def test_calculator_card_renders_inputs_and_button():
    """Test calculator card renders with inputs and button."""
    # Create a mock for streamlit
    mock_st = MagicMock()
    # Mock session_state as a dict-like object
    mock_st.session_state = {}
    # Default return values
    mock_st.number_input.return_value = 0.0
    mock_st.button.return_value = False

    # Mock st.columns to return two mock columns that work as context managers
    mock_col1 = MagicMock()
    mock_col2 = MagicMock()
    # Make the columns usable in a with statement
    mock_col1.__enter__ = MagicMock(return_value=mock_col1)
    mock_col1.__exit__ = MagicMock(return_value=False)
    mock_col2.__enter__ = MagicMock(return_value=mock_col2)
    mock_col2.__exit__ = MagicMock(return_value=False)
    mock_st.columns.return_value = [mock_col1, mock_col2]

    # Import the module with mocked streamlit
    module = _import_calculator_card(mock_st)
    from src.components.calculator_card import _calculator_card

    # Call the function
    _calculator_card(
        title="ROE Calculator",
        formula="ROE = (Net Income / Shareholder's Equity) × 100",
        input1_label="Net Income",
        input2_label="Shareholder's Equity",
        result_label="ROE",
    )

    # Verify st.markdown was called (for the container)
    assert mock_st.markdown.called

    # Verify st.number_input was called twice
    assert mock_st.number_input.call_count == 2

    # Verify st.button was called
    assert mock_st.button.called

    # Verify st.columns was called
    assert mock_st.columns.called


def test_calculator_card_displays_result():
    """Test calculator card displays result when session_state has value."""
    mock_st = MagicMock()
    mock_st.session_state = {}
    mock_st.number_input.return_value = 0.0
    mock_st.button.return_value = False

    # Mock st.columns
    mock_col1 = MagicMock()
    mock_col2 = MagicMock()
    mock_col1.__enter__ = MagicMock(return_value=mock_col1)
    mock_col1.__exit__ = MagicMock(return_value=False)
    mock_col2.__enter__ = MagicMock(return_value=mock_col2)
    mock_col2.__exit__ = MagicMock(return_value=False)
    mock_st.columns.return_value = [mock_col1, mock_col2]

    # Import the module with mocked streamlit
    module = _import_calculator_card(mock_st)
    from src.components.calculator_card import _calculator_card

    # Title, formula, labels, button label
    title = "ROE Calculator"
    formula = "ROE = (Net Income / Shareholder's Equity) × 100"
    input1_label = "Net Income"
    input2_label = "Shareholder's Equity"
    result_label = "ROE"
    button_label = "Calculate"

    # Generate the expected key (same as in the function)
    key = f"_calculator_{hash((title, formula, input1_label, input2_label, result_label, button_label))}"
    result_key = f"{key}_result"

    # Pre-set the result in session_state
    mock_st.session_state[result_key] = 12.5

    # Call the function
    _calculator_card(
        title=title,
        formula=formula,
        input1_label=input1_label,
        input2_label=input2_label,
        result_label=result_label,
        button_label=button_label,
    )

    # Check that st.markdown was called with a string containing the result
    found = False
    for call in mock_st.markdown.call_args_list:
        args, kwargs = call
        if args and isinstance(args[0], str):
            # Format the expected result: 12.50%
            if "12.50" in args[0] and "%" in args[0]:
                found = True
                break
    assert found, "Expected to find formatted result in markdown output"