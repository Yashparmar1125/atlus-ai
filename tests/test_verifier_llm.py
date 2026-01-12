"""
Unit tests for VerifierLLM.
Tests verification/critique LLM functionality with mocked API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from llm.verifier_llm import VerifierLLM
from llm.config import MODELS


class TestVerifierLLM:
    """Test suite for VerifierLLM class."""

    @patch('llm.verifier_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_init(self, mock_openai):
        """Test VerifierLLM initialization."""
        llm = VerifierLLM()
        
        # Verify config is loaded correctly
        assert llm.cfg == MODELS["verification"]
        assert llm.cfg["model"] == "nvidia/nemotron-3-nano-30b-a3b:free"
        assert llm.cfg["temperature"] == 0.2
        assert llm.cfg["max_tokens"] == 1024
        assert llm.cfg["reasoning"] == True
        
        # Verify OpenAI client is initialized
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args
        assert call_args[1]["base_url"] == "https://openrouter.ai/api/v1"
        assert call_args[1]["api_key"] == "test-key"

    @patch('llm.verifier_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_success(self, mock_openai):
        """Test successful verification generation."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            '{"issues": ["Missing error handling"], "suggested_fixes": ["Add try-except blocks"]}'
        )
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = VerifierLLM()
        messages = [{"role": "user", "content": "Review this code"}]
        result = llm.generate(messages)
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        
        assert call_kwargs["model"] == MODELS["verification"]["model"]
        assert call_kwargs["messages"] == messages
        assert call_kwargs["temperature"] == MODELS["verification"]["temperature"]
        assert call_kwargs["max_tokens"] == MODELS["verification"]["max_tokens"]
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == True
        
        # Verify return value
        assert "issues" in result
        assert "suggested_fixes" in result

    @patch('llm.verifier_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_reasoning_enabled(self, mock_openai):
        """Test that reasoning is enabled from config."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = VerifierLLM()
        messages = [{"role": "user", "content": "test"}]
        llm.generate(messages)
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        # Verification config has "reasoning": True
        assert call_kwargs["extra_body"]["reasoning"]["enabled"] == True

    @patch('llm.verifier_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_reasoning_config_default(self, mock_openai):
        """Test that reasoning defaults to False when not in config."""
        # Temporarily modify config to test default behavior
        original_reasoning = MODELS["verification"].get("reasoning")
        if "reasoning" in MODELS["verification"]:
            del MODELS["verification"]["reasoning"]
        
        try:
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "output"
            
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = mock_response
            mock_openai.return_value = mock_client
            
            llm = VerifierLLM()
            messages = [{"role": "user", "content": "test"}]
            llm.generate(messages)
            
            call_kwargs = mock_client.chat.completions.create.call_args[1]
            # Should default to False if not in config
            assert call_kwargs["extra_body"]["reasoning"]["enabled"] == False
        finally:
            # Restore original config
            if original_reasoning is not None:
                MODELS["verification"]["reasoning"] = original_reasoning

    @patch('llm.verifier_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_with_feedback_structure(self, mock_openai):
        """Test that verifier returns structured feedback."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            '{"issues": ["Issue 1", "Issue 2"], "suggested_fixes": ["Fix 1", "Fix 2"]}'
        )
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = VerifierLLM()
        messages = [{"role": "user", "content": "Verify this"}]
        result = llm.generate(messages)
        
        # Verify it returns JSON-like structure
        assert "issues" in result
        assert "suggested_fixes" in result



