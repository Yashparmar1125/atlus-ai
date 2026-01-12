"""
Unit tests for PlanningLLM.
Tests planning LLM functionality with mocked API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from llm.planning_llm import PlanningLLM
from llm.config import MODELS


class TestPlanningLLM:
    """Test suite for PlanningLLM class."""

    @patch('llm.planning_llm.OpenAI')
    @patch('llm.planning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_init(self, mock_dotenv, mock_openai):
        """Test PlanningLLM initialization."""
        llm = PlanningLLM()
        
        # Verify config is loaded correctly
        assert llm.cfg == MODELS["planning"]
        assert llm.cfg["model"] == "openai/gpt-oss-20b:free"
        assert llm.cfg["temperature"] == 0.3
        assert llm.cfg["max_tokens"] == 1024
        
        # Verify OpenAI client is initialized
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args
        assert call_args[1]["base_url"] == "https://openrouter.ai/api/v1"
        assert call_args[1]["api_key"] == "test-key"

    @patch('llm.planning_llm.OpenAI')
    @patch('llm.planning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_success(self, mock_dotenv, mock_openai):
        """Test successful generation."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = '{"plan": ["Step 1", "Step 2", "Step 3"]}'
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = PlanningLLM()
        messages = [{"role": "user", "content": "Plan this task"}]
        result = llm.generate(messages)
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        
        assert call_kwargs["model"] == MODELS["planning"]["model"]
        assert call_kwargs["messages"] == messages
        assert call_kwargs["temperature"] == MODELS["planning"]["temperature"]
        assert call_kwargs["max_tokens"] == MODELS["planning"]["max_tokens"]
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == True
        
        # Verify return value
        assert result == '{"plan": ["Step 1", "Step 2", "Step 3"]}'

    @patch('llm.planning_llm.OpenAI')
    @patch('llm.planning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_reasoning_config_default(self, mock_dotenv, mock_openai):
        """Test that reasoning defaults to True when not in config."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = PlanningLLM()
        messages = [{"role": "user", "content": "test"}]
        llm.generate(messages)
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        # Planning config doesn't have "reasoning" key, should default to True
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == True

    @patch('llm.planning_llm.OpenAI')
    @patch('llm.planning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_empty_response(self, mock_dotenv, mock_openai):
        """Test handling of empty response."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = PlanningLLM()
        messages = [{"role": "user", "content": "test"}]
        result = llm.generate(messages)
        
        assert result == ""



