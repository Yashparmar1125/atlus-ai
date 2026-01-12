"""
Preference extraction service.
Extracts user preferences and facts from conversations for long-term memory.
"""

import re
from typing import Dict, List, Optional
from app.utils.logger import get_logger

logger = get_logger("atlus.service.preference")


class PreferenceExtractor:
    """
    Extracts user preferences and facts from conversations.
    """

    # Patterns for common preferences
    LANGUAGE_PATTERNS = [
        r"i\s+(prefer|use|like|love|work with|code in)\s+(\w+)",
        r"my\s+(favorite|preferred)\s+(language|lang)\s+is\s+(\w+)",
        r"(\w+)\s+is\s+my\s+(favorite|preferred|go-to)\s+(language|lang)",
    ]
    
    API_PREFERENCE_PATTERNS = [
        r"(free|paid|premium|tier)",
        r"(no|don't|avoid).*paid.*api",
        r"only.*free.*tier",
    ]
    
    STYLE_PATTERNS = [
        r"(detailed|brief|concise|verbose|short)",
        r"(explain|tell).*(simply|in detail|briefly)",
    ]

    @classmethod
    def extract_preferences(cls, user_message: str, conversation_history: List[Dict] = None) -> Dict[str, any]:
        """
        Extract preferences from user message and conversation history.
        
        Args:
            user_message: Current user message
            conversation_history: Previous conversation turns
            
        Returns:
            Dict of extracted preferences/facts
        """
        preferences = {}
        message_lower = user_message.lower()
        
        # Extract programming language preference
        lang_pref = cls._extract_language_preference(user_message, message_lower)
        if lang_pref:
            preferences["preferred_language"] = lang_pref
            logger.debug(f"Extracted language preference: {lang_pref}")
        
        # Extract API/tier preference
        api_pref = cls._extract_api_preference(user_message, message_lower)
        if api_pref:
            preferences["api_preference"] = api_pref
            logger.debug(f"Extracted API preference: {api_pref}")
        
        # Extract communication style
        style_pref = cls._extract_style_preference(user_message, message_lower)
        if style_pref:
            preferences["communication_style"] = style_pref
            logger.debug(f"Extracted style preference: {style_pref}")
        
        # Extract explicit preferences from conversation history
        if conversation_history:
            history_prefs = cls._extract_from_history(conversation_history)
            preferences.update(history_prefs)
        
        return preferences

    @classmethod
    def _extract_language_preference(cls, message: str, message_lower: str) -> Optional[str]:
        """Extract programming language preference."""
        common_languages = [
            "python", "javascript", "java", "typescript", "go", "rust", 
            "cpp", "c++", "c#", "php", "ruby", "swift", "kotlin", "dart"
        ]
        
        for pattern in cls.LANGUAGE_PATTERNS:
            matches = re.finditer(pattern, message_lower, re.IGNORECASE)
            for match in matches:
                # Try to find a language in the match
                words = match.group(0).split()
                for word in words:
                    word_clean = re.sub(r'[^\w]', '', word.lower())
                    if word_clean in common_languages:
                        return word_clean.title()
        
        # Direct language mention
        for lang in common_languages:
            if re.search(rf"\b{lang}\b", message_lower):
                # Check context - is it a preference statement?
                context = message_lower[max(0, message_lower.find(lang)-20):message_lower.find(lang)+30]
                if any(word in context for word in ["prefer", "use", "like", "love", "favorite"]):
                    return lang.title()
        
        return None

    @classmethod
    def _extract_api_preference(cls, message: str, message_lower: str) -> Optional[str]:
        """Extract API/tier preference."""
        if any(term in message_lower for term in ["free tier", "free api", "free only"]):
            if "no" not in message_lower[:message_lower.find("free")]:
                return "free_only"
        
        if any(term in message_lower for term in ["no paid", "avoid paid", "don't use paid"]):
            return "free_only"
        
        if "paid" in message_lower and "prefer" in message_lower:
            return "paid_ok"
        
        return None

    @classmethod
    def _extract_style_preference(cls, message: str, message_lower: str) -> Optional[str]:
        """Extract communication style preference."""
        if any(term in message_lower for term in ["brief", "concise", "short", "quick"]):
            return "brief"
        
        if any(term in message_lower for term in ["detailed", "in detail", "explain thoroughly"]):
            return "detailed"
        
        if any(term in message_lower for term in ["simple", "simply", "plain language"]):
            return "simple"
        
        return None

    @classmethod
    def _extract_from_history(cls, conversation_history: List[Dict]) -> Dict[str, any]:
        """Extract preferences from conversation history."""
        preferences = {}
        
        # Combine all user messages
        user_messages = [
            msg["content"] for msg in conversation_history 
            if msg.get("role") == "user"
        ]
        combined_text = " ".join(user_messages).lower()
        
        # Look for recurring preferences
        # This is a simple implementation - can be enhanced with LLM-based extraction
        
        return preferences

