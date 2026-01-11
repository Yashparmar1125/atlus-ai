"""
Main Agent Orchestrator.
Classifies user intent and routes to appropriate specialized agent.
"""

import json
import time

from app.llm.router import get_llm
from app.prompts.classifier_prompt import build_classifier_prompt
from app.utils.parsers.json_parser import parse_json, JSONParseError
from app.utils.validators.classifier_validator import validate_classifier, ClassifierValidationError
from app.utils.logger import get_logger

from app.agent.simple_agent import SimpleAgent
from app.agent.task_agent import TaskAgent


class Agent:
    """
    Main agent orchestrator with intelligent routing.
    
    Flow:
    1. Intent Classification (simple vs complex)
    2. Route to appropriate agent:
       - SimpleAgent: Greetings, simple questions, casual conversation
       - TaskAgent: Complex tasks requiring full pipeline
    
    This prevents wasting resources on simple requests like "hi".
    """
    
    MAX_RETRIES = 2
    
    def __init__(self):
        self.logger = get_logger("atlus.agent")
        self.logger.info("=" * 80)
        self.logger.info("Initializing ATLUS Agent Orchestrator")
        self.logger.info("=" * 80)
        
        # Initialize classifier LLM
        self.logger.debug("Initializing classifier LLM...")
        self.classifier_llm = get_llm("intent")  # Use intent LLM for classification
        
        # Initialize specialized agents (lazy loading)
        self._simple_agent = None
        self._task_agent = None
        
        self.logger.info("Agent orchestrator initialized successfully")
    
    def run(self, user_message: str) -> str:
        """
        Main entry point with intelligent routing.
        
        Args:
            user_message: User's input request
            
        Returns:
            Response string from appropriate agent
        """
        start_time = time.time()
        self.logger.info("=" * 80)
        self.logger.info("AGENT ORCHESTRATOR STARTED")
        self.logger.info("=" * 80)
        self.logger.info(f"User Input: {user_message}")
        self.logger.info(f"Input Length: {len(user_message)} characters")
        
        try:
            # Step 1: Classify Intent
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 1: INTENT CLASSIFICATION")
            self.logger.info("-" * 80)
            
            classification = self._classify_intent(user_message)
            intent_type = classification.get("intent_type", "complex")  # Default to complex if unclear
            confidence = classification.get("confidence", 0.5)
            
            self.logger.info(f"Intent classified as: {intent_type} (confidence: {confidence:.2f})")
            if "reasoning" in classification:
                self.logger.debug(f"Classification reasoning: {classification['reasoning']}")
            
            # Step 2: Route to Appropriate Agent
            self.logger.info("\n" + "-" * 80)
            self.logger.info(f"STEP 2: ROUTING TO {intent_type.upper()} AGENT")
            self.logger.info("-" * 80)
            
            if intent_type == "simple":
                agent = self._get_simple_agent()
                self.logger.info("Using SimpleAgent for quick response")
            else:
                agent = self._get_task_agent()
                self.logger.info("Using TaskAgent for complex task processing")
            
            # Execute with selected agent
            response = agent.run(user_message)
            
            # Summary
            elapsed_time = time.time() - start_time
            self.logger.info("\n" + "=" * 80)
            self.logger.info("AGENT ORCHESTRATOR COMPLETED")
            self.logger.info("=" * 80)
            self.logger.info(f"Intent Type: {intent_type}")
            self.logger.info(f"Agent Used: {agent.__class__.__name__}")
            self.logger.info(f"Total execution time: {elapsed_time:.2f} seconds")
            self.logger.info(f"Response length: {len(response)} characters")
            self.logger.info("=" * 80)
            
            return response
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error("=" * 80)
            self.logger.error("AGENT ORCHESTRATOR FAILED")
            self.logger.error("=" * 80)
            self.logger.error(f"Error: {str(e)}", exc_info=True)
            self.logger.error(f"Execution time before failure: {elapsed_time:.2f} seconds")
            self.logger.error("=" * 80)
            
            # Fallback to simple agent on error
            self.logger.warning("Falling back to SimpleAgent")
            try:
                agent = self._get_simple_agent()
                return agent.run(user_message)
            except:
                return "I apologize, but I encountered an error. Please try again."
    
    def _classify_intent(self, user_message: str) -> dict:
        """
        Classify user intent as simple or complex.
        
        Args:
            user_message: User's input message
            
        Returns:
            Classification dictionary with intent_type, confidence, reasoning
        """
        # Quick heuristic check for obvious cases (skip LLM call)
        message_lower = user_message.lower().strip()
        
        # Obvious simple cases
        simple_keywords = ["hi", "hello", "hey", "good morning", "good afternoon", 
                          "good evening", "thanks", "thank you", "bye", "goodbye"]
        if any(keyword in message_lower for keyword in simple_keywords) and len(message_lower) < 20:
            self.logger.debug("Quick classification: simple (heuristic)")
            return {
                "intent_type": "simple",
                "confidence": 0.95,
                "reasoning": "Simple greeting or short message"
            }
        
        # Obvious complex cases (task-oriented keywords)
        complex_keywords = ["build", "create", "implement", "design", "develop", 
                           "make", "write", "generate", "plan", "solve"]
        if any(keyword in message_lower for keyword in complex_keywords) and len(message_lower) > 15:
            self.logger.debug("Quick classification: complex (heuristic)")
            return {
                "intent_type": "complex",
                "confidence": 0.95,
                "reasoning": "Task-oriented request"
            }
        
        # Use LLM for classification
        self.logger.debug("Using LLM for intent classification...")
        prompt = build_classifier_prompt(user_message)
        
        for attempt in range(self.MAX_RETRIES):
            try:
                self.logger.debug(f"Classification attempt {attempt + 1}/{self.MAX_RETRIES}")
                raw = self.classifier_llm.generate(prompt)
                
                self.logger.debug(f"Classifier response: {raw[:100]}...")
                
                # Parse JSON
                parsed = parse_json(raw)
                
                # Validate
                classification = validate_classifier(parsed)
                
                self.logger.info(f"Intent classification successful: {classification['intent_type']}")
                return classification
                
            except (JSONParseError, ClassifierValidationError) as e:
                self.logger.warning(f"Classification failed on attempt {attempt + 1}: {str(e)}")
                
                if attempt < self.MAX_RETRIES - 1:
                    # Try to repair
                    try:
                        repair_prompt = [
                            {
                                "role": "system",
                                "content": "You fix invalid JSON. Return ONLY valid JSON: {\"intent_type\": \"simple\" or \"complex\", \"confidence\": 0.0-1.0, \"reasoning\": \"string\"}"
                            },
                            {
                                "role": "user",
                                "content": f"Fix this JSON: {raw}\nError: {str(e)}"
                            }
                        ]
                        raw = self.classifier_llm.generate(repair_prompt)
                    except:
                        pass
                else:
                    # Default to complex on failure (safer to use full pipeline)
                    self.logger.warning("Classification failed, defaulting to complex")
                    return {
                        "intent_type": "complex",
                        "confidence": 0.5,
                        "reasoning": "Classification failed, using complex agent"
                    }
    
    def _get_simple_agent(self) -> SimpleAgent:
        """Get or create SimpleAgent instance (lazy loading)."""
        if self._simple_agent is None:
            self.logger.debug("Creating SimpleAgent instance")
            self._simple_agent = SimpleAgent()
        return self._simple_agent
    
    def _get_task_agent(self) -> TaskAgent:
        """Get or create TaskAgent instance (lazy loading)."""
        if self._task_agent is None:
            self.logger.debug("Creating TaskAgent instance")
            self._task_agent = TaskAgent()
        return self._task_agent
