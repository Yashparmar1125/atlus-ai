# llm/config.py

# ---------- PROVIDERS ----------
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ---------- MODELS ----------
MODELS = {
    "intent": {
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "temperature": 0.2,
        "max_tokens": 512,
        "reasoning": False,
    },
    "planning": {
        "provider": "openrouter",
        "model": "openai/gpt-oss-120b:free",
        "temperature": 0.3,
        "max_tokens": 1024,
        "reasoning": True,
    },
    "reasoning": {
        "provider": "openrouter",
        "model": "arcee-ai/trinity-mini:free",
        "temperature": 0.5,
        "max_tokens": 8192,
        "reasoning": True,
    },
    "verification": {
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "temperature": 0.2,
        "max_tokens": 2048,
        "reasoning": True,
    },
    "writing": {
        "provider": "openrouter",
        "model": "nvidia/nemotron-3-nano-30b-a3b:free",
        "temperature": 0.7,
        "max_tokens": 16384,
        "reasoning": False,
    },
    "chatting":{
        "provider": "groq",
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "temperature": 1,
        "max_tokens": 1024,
        "reasoning": True,
    }
}
