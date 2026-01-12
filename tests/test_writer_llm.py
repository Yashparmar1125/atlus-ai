"""
Unit tests for WriterLLM.
Tests final writing LLM functionality with mocked API calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add app directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from llm.writer_llm import WriterLLM
from llm.config import MODELS


class TestWriterLLM:
    """Test suite for WriterLLM class."""

    @patch('llm.writer_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_init(self, mock_openai):
        """Test WriterLLM initialization."""
        llm = WriterLLM()
        
        # Verify config is loaded correctly
        assert llm.cfg == MODELS["writing"]
        assert llm.cfg["model"] == "nvidia/nemotron-3-nano-30b-a3b:free"
        assert llm.cfg["temperature"] == 0.7
        assert llm.cfg["max_tokens"] == 2048
        assert llm.cfg["reasoning"] == False
        
        # Verify OpenAI client is initialized
        mock_openai.assert_called_once()
        call_args = mock_openai.call_args
        assert call_args[1]["base_url"] == "https://openrouter.ai/api/v1"
        assert call_args[1]["api_key"] == "test-key"

    @patch('llm.writer_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_success(self, mock_openai):
        """Test successful generation."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = (
            "Here is a polished, professional response to your query. "
            "This has been refined and is ready for the user."
        )
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = WriterLLM()
        messages = [
            {"role": "system", "content": "You are a professional writer."},
            {"role": "user", "content": "Write a final response"}
        ]
        result = llm.generate(messages)
        
        # Verify API call
        mock_client.chat.completions.create.assert_called_once()
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        
        assert call_kwargs["model"] == MODELS["writing"]["model"]
        assert call_kwargs["messages"] == messages
        assert call_kwargs["temperature"] == MODELS["writing"]["temperature"]
        assert call_kwargs["max_tokens"] == MODELS["writing"]["max_tokens"]
        # WriterLLM doesn't include extra_body for reasoning
        
        # Verify return value
        assert "polished" in result.lower() or "professional" in result.lower()

    @patch('llm.writer_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_no_reasoning_extra_body(self, mock_openai):
        """Test that WriterLLM doesn't include reasoning extra_body."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = WriterLLM()
        messages = [{"role": "user", "content": "test"}]
        llm.generate(messages)
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        # WriterLLM doesn't include extra_body parameter
        assert "extra_body" not in call_kwargs

    @patch('llm.writer_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_high_temperature(self, mock_openai):
        """Test that writer uses higher temperature for creativity."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "creative output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = WriterLLM()
        messages = [{"role": "user", "content": "test"}]
        llm.generate(messages)
        
        call_kwargs = mock_client.chat.completions.create.call_args[1]
        # Writer should use higher temperature (0.7) for more creative output
        assert call_kwargs["temperature"] == 0.7

    @patch('llm.writer_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_with_kwargs(self, mock_openai):
        """Test generate method accepts additional kwargs."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "test output"
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = WriterLLM()
        messages = [{"role": "user", "content": "test"}]
        result = llm.generate(messages, some_kwarg="value")
        
        # Should still work with extra kwargs
        assert result == "test output"

    @patch('llm.writer_llm.OpenAI')
    @patch.dict(os.environ, {'OPENROUTER_API_KEY': 'test-key'})
    def test_generate_empty_response(self, mock_openai):
        """Test handling of empty response."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = ""
        
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        llm = WriterLLM()
        messages = [{"role": "user", "content": "test"}]
        result = llm.generate(messages)
        
        assert result == ""



