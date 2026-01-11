"""
Pytest configuration and shared fixtures for LLM tests.
"""

import pytest
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))


@pytest.fixture
def mock_openai_client():
    """Fixture providing a mocked OpenAI client."""
    from unittest.mock import MagicMock
    
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "test response"
    mock_client.chat.completions.create.return_value = mock_response
    
    return mock_client


@pytest.fixture
def sample_messages():
    """Fixture providing sample messages for testing."""
    return [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Test message"}
    ]

