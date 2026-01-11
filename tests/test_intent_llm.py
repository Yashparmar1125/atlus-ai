"""
Unit tests for IntentLLM.
Tests intent extraction LLM functionality with mocked API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from llm.intent_llm import IntentLLM
from llm.config import MODELS


class TestIntentLLM:
    """Test suite for IntentLLM class."""

    @patch('llm.intent_llm.OpenAI')
    @patch('llm.intent_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_init(self, mock_dotenv, mock_openai):
        """Test IntentLLM initialization."""
        llm = IntentLLM()
        
        # Verify config is loaded correctly
        assert llm.cfg == MODELS["intent"]
        assert llm.cfg["model"] == "nvidia/nemotron-3-nano-30b-a3b:free"
        assert llm.cfg["temperature"] == 0.2
        assert llm.cfg["max_tokens"] == 512
        
        # Verify OpenAI client is initialized
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args
        assert call_args[1]["base_url"] == "https://openrouter.ai/api/v1"
        assert call_args[1]["api_key"] == "test-key"

    @patch('llm.intent_llm.OpenAI')
    @patch('llm.intent_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_success(self, mock_dotenv, mock_openai):
        """Test successful generation."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"goal": "test", "constraints": [], "expected_output": "result"}'
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = IntentLLM()
        messages = [{"role": "user", "content": "Test message"}]
        result = llm.generate(messages)
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        
        assert call_kwargs["model"] == MODELS["intent"]["model"]
        assert call_kwargs["messages"] == messages
        assert call_kwargs["temperature"] == MODELS["intent"]["temperature"]
        assert call_kwargs["max_tokens"] == MODELS["intent"]["max_tokens"]
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == False
        
        # Verify return value
        assert result == '{"goal": "test", "constraints": [], "expected_output": "result"}'

    @patch('llm.intent_llm.OpenAI')
    @patch('llm.intent_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_with_kwargs(self, mock_dotenv, mock_openai):
        """Test generate method accepts additional kwargs."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "test output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = IntentLLM()
        messages = [{"role": "user", "content": "test"}]
        result = llm.generate(messages, some_kwarg="value")
        
        # Should still work with extra kwargs (they're passed but not used)
        assert result == "test output"

    @patch('llm.intent_llm.OpenAI')
    @patch('llm.intent_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_reasoning_config_default(self, mock_dotenv, mock_openai):
        """Test that reasoning defaults to False when not in config."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = IntentLLM()
        messages = [{"role": "user", "content": "test"}]
        llm.generate(messages)
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        # Intent config doesn't have "reasoning" key, should default to False
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == False

