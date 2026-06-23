import pytest
from unittest.mock import patch, MagicMock

from src.components.ai_explanation_card import _ai_explanation_card


def test_ai_explanation_card_without_confidence():
    """Test the AI explanation card without confidence level."""
    with patch('streamlit.info') as mock_info, \
         patch('src.components.ai_explanation_card.t') as mock_t:
        # Mock the translation function
        mock_t.side_effect = lambda key: {
            'ai_explanation.title': 'AI Explanation Title',
            'ai_explanation.explanation': 'This is an explanation.'
        }.get(key, key)

        # Call the function
        _ai_explanation_card(
            title='ai_explanation.title',
            explanation_text='ai_explanation.explanation'
        )

        # Verify translations were called
        assert mock_t.call_count == 2
        mock_t.assert_any_call('ai_explanation.title')
        mock_t.assert_any_call('ai_explanation.explanation')

        # Verify st.info was called with the expected content
        expected_content = (
            "**AI Explanation Title**\n\n"
            "This is an explanation."
        )
        mock_info.assert_called_once_with(expected_content)


def test_ai_explanation_card_with_confidence():
    """Test the AI explanation card with confidence level."""
    with patch('streamlit.info') as mock_info, \
         patch('src.components.ai_explanation_card.t') as mock_t:
        # Mock the translation function
        mock_t.side_effect = lambda key: {
            'ai_explanation.title': 'AI Title',
            'ai_explanation.explanation': 'Explanation text',
            'ai_explanation.confidence': 'Confidence'
        }.get(key, key)

        # Call the function with confidence
        _ai_explanation_card(
            title='ai_explanation.title',
            explanation_text='ai_explanation.explanation',
            confidence_level=85
        )

        # Verify translations were called
        assert mock_t.call_count == 3
        mock_t.assert_any_call('ai_explanation.title')
        mock_t.assert_any_call('ai_explanation.explanation')
        mock_t.assert_any_call('ai_explanation.confidence')

        # Verify st.info was called with the expected content
        expected_content = (
            "**AI Title**\n\n"
            "Explanation text\n\n"
            "---\n"
            "**Confidence:** 85%"
        )
        mock_info.assert_called_once_with(expected_content)


def test_ai_explanation_card_confidence_clamping():
    """Test that confidence level is clamped between 0 and 100."""
    with patch('streamlit.info') as mock_info, \
         patch('src.components.ai_explanation_card.t') as mock_t:
        mock_t.side_effect = lambda key: {
            'ai_explanation.title': 'Title',
            'ai_explanation.explanation': 'Explanation',
            'ai_explanation.confidence': 'Confidence'
        }.get(key, key)

        # Test with value below 0
        _ai_explanation_card(
            title='ai_explanation.title',
            explanation_text='ai_explanation.explanation',
            confidence_level=-5
        )
        args, _ = mock_info.call_args
        assert "**Confidence:** 0%" in args[0]

        # Reset mock
        mock_info.reset_mock()

        # Test with value above 100
        _ai_explanation_card(
            title='ai_explanation.title',
            explanation_text='ai_explanation.explanation',
            confidence_level=150
        )
        args, _ = mock_info.call_args
        assert "**Confidence:** 100%" in args[0]


if __name__ == '__main__':
    pytest.main([__file__])