"""
Unit tests for ReasoningLLM.
Tests reasoning LLM functionality with mocked API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from llm.reasoning_llm import ReasoningLLM
from llm.config import MODELS


class TestReasoningLLM:
    """Test suite for ReasoningLLM class."""

    @patch('llm.reasoning_llm.OpenAI')
    @patch('llm.reasoning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_init(self, mock_dotenv, mock_openai):
        """Test ReasoningLLM initialization."""
        llm = ReasoningLLM()
        
        # Verify config is loaded correctly
        assert llm.cfg == MODELS["reasoning"]
        assert llm.cfg["model"] == "arcee-ai/trinity-mini:free"
        assert llm.cfg["temperature"] == 0.5
        assert llm.cfg["max_tokens"] == 2048
        assert llm.cfg["reasoning"] == True
        
        # Verify OpenAI client is initialized
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args
        assert call_args[1]["base_url"] == "https://openrouter.ai/api/v1"
        assert call_args[1]["api_key"] == "test-key"

    @patch('llm.reasoning_llm.OpenAI')
    @patch('llm.reasoning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_success(self, mock_dotenv, mock_openai):
        """Test successful generation."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Let me think step by step...\n\nStep 1: Analyze the problem..."
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = ReasoningLLM()
        messages = [
            {"role": "system", "content": "You are a reasoning engine."},
            {"role": "user", "content": "Solve this problem"}
        ]
        result = llm.generate(messages)
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        
        assert call_kwargs["model"] == MODELS["reasoning"]["model"]
        assert call_kwargs["messages"] == messages
        assert call_kwargs["temperature"] == MODELS["reasoning"]["temperature"]
        assert call_kwargs["max_tokens"] == MODELS["reasoning"]["max_tokens"]
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == True
        
        # Verify return value
        assert "Let me think step by step" in result

    @patch('llm.reasoning_llm.OpenAI')
    @patch('llm.reasoning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_reasoning_enabled(self, mock_dotenv, mock_openai):
        """Test that reasoning is enabled from config."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = ReasoningLLM()
        messages = [{"role": "user", "content": "test"}]
        llm.generate(messages)
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        # Reasoning config has "reasoning": True
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == True

    @patch('llm.reasoning_llm.OpenAI')
    @patch('llm.reasoning_llm.load_dotenv')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_multiple_steps(self, mock_dotenv, mock_openai):
        """Test generation with complex multi-step reasoning."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            "Step 1: Understanding the requirements\n"
            "Step 2: Breaking down the problem\n"
            "Step 3: Implementing the solution"
        )
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = ReasoningLLM()
        messages = [{"role": "user", "content": "Complex task"}]
        result = llm.generate(messages)
        
        assert "Step 1" in result
        assert "Step 2" in result
        assert "Step 3" in result


