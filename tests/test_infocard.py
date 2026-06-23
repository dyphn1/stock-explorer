"""
Unit tests for the infocard component.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# Ensure src/ is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_infocard_with_value_and_no_trend():
    """Test infocard rendering with value and no trend indicator."""
    # Create a mock for streamlit
    mock_st = MagicMock()
    
    # Temporarily replace streamlit module
    sys.modules['streamlit'] = mock_st
    
    # Reload the module to use the mocked streamlit
    import importlib
    import src.components.infocard
    importlib.reload(src.components.infocard)
    from src.components.infocard import _infocard
    
    # Call the function
    _infocard("Revenue", "$1.2M")
    
    # Verify st.markdown was called
    assert mock_st.markdown.called
    
    # Get the HTML that was passed to st.markdown
    call_args = mock_st.markdown.call_args
    html_content = call_args[0][0]  # First positional argument
    
    # Verify the content contains expected elements
    assert "Revenue" in html_content
    assert "$1.2M" in html_content
    assert "background:white" in html_content
    assert "border-left:4px solid #3498DB" in html_content


def test_infocard_with_up_trend():
    """Test infocard rendering with upward trend."""
    # Create a mock for streamlit
    mock_st = MagicMock()
    
    # Temporarily replace streamlit module
    sys.modules['streamlit'] = mock_st
    
    # Reload the module to use the mocked streamlit
    import importlib
    import src.components.infocard
    importlib.reload(src.components.infocard)
    from src.components.infocard import _infocard
    
    # Call the function with up trend
    _infocard("Profit Margin", "15.3%", "up")
    
    # Verify st.markdown was called
    assert mock_st.markdown.called
    
    # Get the HTML that was passed to st.markdown
    call_args = mock_st.markdown.call_args
    html_content = call_args[0][0]  # First positional argument
    
    # Verify the content contains expected elements
    assert "Profit Margin" in html_content
    assert "15.3%" in html_content
    assert "📈" in html_content  # Up arrow emoji
    assert "background:white" in html_content


def test_infocard_with_down_trend():
    """Test infocard rendering with downward trend."""
    # Create a mock for streamlit
    mock_st = MagicMock()
    
    # Temporarily replace streamlit module
    sys.modules['streamlit'] = mock_st
    
    # Reload the module to use the mocked streamlit
    import importlib
    import src.components.infocard
    importlib.reload(src.components.infocard)
    from src.components.infocard import _infocard
    
    # Call the function with down trend
    _infocard("Expense Ratio", "2.1%", "down")
    
    # Verify st.markdown was called
    assert mock_st.markdown.called
    
    # Get the HTML that was passed to st.markdown
    call_args = mock_st.markdown.call_args
    html_content = call_args[0][0]  # First positional argument
    
    # Verify the content contains expected elements
    assert "Expense Ratio" in html_content
    assert "2.1%" in html_content
    assert "📉" in html_content  # Down arrow emoji
    assert "background:white" in html_content