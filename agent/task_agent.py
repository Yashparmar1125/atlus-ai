"""
Complex Task Agent for multi-step task processing.
Handles complex requests requiring planning, reasoning, and verification.
This is the full pipeline agent for complex tasks.
"""

import json
import time
from typing import List

# LLMs - Use router for centralized LLM management
from llm.router import get_llm

# Prompts
from prompts.intent_prompt import build_intent_prompt
from prompts.planner_prompt import build_planner_prompt
from prompts.reasoning_prompt import build_reasoning_prompt
from prompts.verifier_prompt import build_verifier_prompt
from prompts.refactor_prompt import build_refactor_prompt
from prompts.writer_prompt import build_writer_prompt

# Parsers
from utils.parsers.json_parser import parse_json, JSONParseError
from utils.parsers.plan_parser import parse_plan, PlanParseError

# Validators
from utils.validators.intent_validator import validate_intent, IntentValidationError
from utils.validators.plan_validator import validate_plan, PlanValidationError

# Logging
from utils.logger import get_logger


class TaskAgent:
    """
    Complex task agent for multi-step processing.
    
    Full pipeline: Intent → Plan → Reasoning → Verification → Refactor → Writing
    
    Use cases:
    - Complex task requests
    - Implementation requests
    - Planning requests
    - Problem-solving tasks
    - Multi-step workflows
    """
    
    MAX_RETRIES = 1

    def __init__(self):
        self.logger = get_logger("atlus.agent.task")
        self.logger.info("Initializing TaskAgent (complex task processing)")
        
        self.logger.debug("Initializing LLM instances using router...")
        self.intent_llm = get_llm("intent")
        self.planning_llm = get_llm("planning")
        self.reasoning_llm = get_llm("reasoning")
        self.verifier_llm = get_llm("verification")
        self.writer_llm = get_llm("writing")
        self.logger.info("TaskAgent LLM instances initialized successfully")

    def run(self, user_message: str) -> str:
        """
        Process complex task request through full pipeline.
        
        Args:
            user_message: User's input request
            
        Returns:
            Final polished response string
        """
        start_time = time.time()
        self.logger.info("=" * 80)
        self.logger.info("TASK AGENT EXECUTION STARTED")
        self.logger.info("=" * 80)
        self.logger.info(f"User Input: {user_message}")
        self.logger.info(f"Input Length: {len(user_message)} characters")
        
        try:
            # Step 1: Intent Extraction
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 1: INTENT EXTRACTION")
            self.logger.info("-" * 80)
            intent = self._safe_intent_extraction(user_message)
            self.logger.info(f"Intent extracted successfully: {json.dumps(intent, indent=2)}")
            
            # Step 2: Planning
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 2: PLANNING")
            self.logger.info("-" * 80)
            plan = self._safe_plan_creation(intent)
            self.logger.info(f"Plan created with {len(plan)} steps")
            for i, step in enumerate(plan, 1):
                self.logger.debug(f"  Step {i}: {step}")
            
            # Step 3: Reasoning
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 3: REASONING")
            self.logger.info("-" * 80)
            draft = self._execute_reasoning(intent, plan)
            self.logger.info(f"Draft generated: {len(draft)} characters")
            self.logger.debug(f"Draft preview (first 200 chars): {draft[:200]}...")
            
            # Step 4: Verification
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 4: VERIFICATION")
            self.logger.info("-" * 80)
            verified = self._verify_output(draft)
            issues_count = len(verified.get("issues", []))
            fixes_count = len(verified.get("suggested_fixes", []))
            self.logger.info(f"Verification complete: {issues_count} issues, {fixes_count} fixes")
            if issues_count > 0:
                self.logger.debug(f"Issues: {verified.get('issues', [])}")
            
            # Step 5: Refactor
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 5: REFACTOR")
            self.logger.info("-" * 80)
            refactored = self._refactor_draft(draft, verified)
            self.logger.info(f"Refactored draft: {len(refactored)} characters")
            self.logger.debug(f"Refactored preview (first 200 chars): {refactored[:200]}...")
            
            # Step 6: Final Writing
            self.logger.info("\n" + "-" * 80)
            self.logger.info("STEP 6: FINAL WRITING")
            self.logger.info("-" * 80)
            final = self._write_final_response(refactored)
            self.logger.info(f"Final response generated: {len(final)} characters")
            
            # Summary
            elapsed_time = time.time() - start_time
            self.logger.info("\n" + "=" * 80)
            self.logger.info("TASK AGENT EXECUTION COMPLETED")
            self.logger.info("=" * 80)
            self.logger.info(f"Total execution time: {elapsed_time:.2f} seconds")
            self.logger.info(f"Final response length: {len(final)} characters")
            self.logger.info("=" * 80)
            
            return final
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error("=" * 80)
            self.logger.error("TASK AGENT EXECUTION FAILED")
            self.logger.error("=" * 80)
            self.logger.error(f"Error: {str(e)}", exc_info=True)
            self.logger.error(f"Execution time before failure: {elapsed_time:.2f} seconds")
            self.logger.error("=" * 80)
            raise

    # ==========================================================
    # STEP 1 — INTENT EXTRACTION (SAFE)
    # ==========================================================
    def _safe_intent_extraction(self, user_message: str) -> dict:
        """Extract structured intent from user message."""
        self.logger.debug("Building intent extraction prompt...")
        prompt = build_intent_prompt(user_message)
        self.logger.debug(f"Prompt messages: {len(prompt)} messages")

        for attempt in range(self.MAX_RETRIES):
            self.logger.info(f"Intent extraction attempt {attempt + 1}/{self.MAX_RETRIES}")
            attempt_start = time.time()
            
            try:
                self.logger.debug("Calling IntentLLM.generate()...")
                raw = self.intent_llm.generate(prompt)
                attempt_time = time.time() - attempt_start
                self.logger.debug(f"LLM response received in {attempt_time:.2f}s")
                self.logger.debug(f"Raw response length: {len(raw)} characters")
                self.logger.debug(f"Raw response preview: {raw[:100]}...")
                
                self.logger.debug("Parsing JSON response...")
                parsed = parse_json(raw)
                self.logger.debug("Validating intent structure...")
                data = validate_intent(parsed)
                
                self.logger.info(f"Intent extraction successful on attempt {attempt + 1}")
                return data
                
            except (JSONParseError, IntentValidationError) as e:
                attempt_time = time.time() - attempt_start
                self.logger.warning(f"Intent extraction failed on attempt {attempt + 1}: {str(e)}")
                self.logger.debug(f"Attempt took {attempt_time:.2f}s before failure")
                self.logger.debug(f"Failed response: {raw[:200]}...")
                
                if attempt < self.MAX_RETRIES - 1:
                    self.logger.info("Attempting to repair output...")
                    raw = self._repair(
                        llm=self.verifier_llm,
                        bad_output=raw,
                        error=str(e),
                        schema_description="""{"goal": string, "constraints": string | list, "expected_output": string}"""
                    )
                    self.logger.debug("Repair attempt completed")

        self.logger.error("Intent extraction failed after all retries")
        raise RuntimeError("Intent extraction failed after retries")

    # ==========================================================
    # STEP 2 — PLANNING (SAFE)
    # ==========================================================
    def _safe_plan_creation(self, intent: dict) -> List[str]:
        """Create execution plan from intent."""
        intent_json = json.dumps(intent, indent=2)
        self.logger.debug("Building planner prompt...")
        self.logger.debug(f"Intent JSON length: {len(intent_json)} characters")
        prompt = build_planner_prompt(intent_json)
        self.logger.debug(f"Prompt messages: {len(prompt)} messages")

        for attempt in range(self.MAX_RETRIES):
            self.logger.info(f"Plan creation attempt {attempt + 1}/{self.MAX_RETRIES}")
            attempt_start = time.time()
            
            try:
                self.logger.debug("Calling PlannerLLM.generate()...")
                raw = self.planning_llm.generate(prompt)
                attempt_time = time.time() - attempt_start
                self.logger.debug(f"LLM response received in {attempt_time:.2f}s")
                self.logger.debug(f"Raw response length: {len(raw)} characters")
                self.logger.debug(f"Raw response preview: {raw[:100]}...")
                
                self.logger.debug("Parsing plan from JSON...")
                parsed_plan = parse_plan(raw)
                self.logger.debug("Validating plan structure...")
                plan = validate_plan(parsed_plan)
                
                self.logger.info(f"Plan creation successful on attempt {attempt + 1}")
                self.logger.debug(f"Plan contains {len(plan)} steps")
                return plan
                
            except (JSONParseError, PlanParseError, PlanValidationError) as e:
                attempt_time = time.time() - attempt_start
                self.logger.warning(f"Plan creation failed on attempt {attempt + 1}: {str(e)}")
                self.logger.debug(f"Attempt took {attempt_time:.2f}s before failure")
                self.logger.debug(f"Failed response: {raw[:200]}...")
                
                if attempt < self.MAX_RETRIES - 1:
                    self.logger.info("Attempting to repair output...")
                    raw = self._repair(
                        llm=self.verifier_llm,
                        bad_output=raw,
                        error=str(e),
                        schema_description="""{"plan": ["Step description 1", "Step description 2"]}"""
                    )
                    self.logger.debug("Repair attempt completed")

        self.logger.error("Plan creation failed after all retries")
        raise RuntimeError("Planner failed after retries")

    # ==========================================================
    # STEP 3 — REASONING (COMPREHENSIVE DRAFT)
    # ==========================================================
    def _execute_reasoning(self, intent: dict, plan: List[str]) -> str:
        """Generate comprehensive draft solution."""
        self.logger.debug("Formatting intent context...")
        constraints_str = (
            ", ".join(intent['constraints']) 
            if isinstance(intent['constraints'], list) 
            else str(intent['constraints'])
        )
        
        context = (
            f"Goal: {intent['goal']}\n"
            f"Constraints: {constraints_str}\n"
            f"Expected Output: {intent['expected_output']}"
        )
        self.logger.debug(f"Context length: {len(context)} characters")
        self.logger.debug(f"Plan steps: {len(plan)}")
        
        self.logger.debug("Building reasoning prompt...")
        prompt = build_reasoning_prompt(
            context=context,
            plan=plan
        )
        self.logger.debug(f"Prompt messages: {len(prompt)} messages")
        
        self.logger.info("Generating comprehensive draft solution...")
        reasoning_start = time.time()
        
        result = self.reasoning_llm.generate(prompt)
        
        reasoning_time = time.time() - reasoning_start
        self.logger.info(f"Reasoning completed in {reasoning_time:.2f}s")
        self.logger.debug(f"Generated draft length: {len(result)} characters")
        
        return result

    # ==========================================================
    # STEP 4 — VERIFICATION
    # ==========================================================
    def _verify_output(self, draft: str) -> dict:
        """Verify draft and identify issues."""
        self.logger.debug(f"Building verifier prompt for draft ({len(draft)} chars)...")
        prompt = build_verifier_prompt(draft)
        self.logger.debug(f"Prompt messages: {len(prompt)} messages")
        
        self.logger.info("Running verification...")
        verify_start = time.time()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                raw = self.verifier_llm.generate(prompt)
                
                if not raw or not raw.strip():
                    self.logger.warning(f"Verifier returned empty response on attempt {attempt + 1}")
                    if attempt < self.MAX_RETRIES - 1:
                        continue
                    else:
                        raise ValueError("Verifier returned empty response after retries")
                
                verify_time = time.time() - verify_start
                self.logger.info(f"Verification completed in {verify_time:.2f}s")
                self.logger.debug(f"Verifier response length: {len(raw)} characters")
                self.logger.debug(f"Verifier response preview: {raw[:200]}...")

                self.logger.debug("Parsing verifier JSON response...")
                result = parse_json(raw)
                issues = result.get("issues", [])
                fixes = result.get("suggested_fixes", [])
                self.logger.info(f"Verification parsed: {len(issues)} issues, {len(fixes)} fixes")
                if issues:
                    self.logger.debug(f"Issues found: {issues}")
                return result
                
            except (JSONParseError, ValueError) as e:
                verify_time = time.time() - verify_start
                self.logger.warning(f"Verifier failed on attempt {attempt + 1}: {str(e)}")
                self.logger.debug(f"Failed response: {raw[:200] if 'raw' in locals() else 'No response'}...")
                
                if attempt < self.MAX_RETRIES - 1:
                    self.logger.info("Retrying verification...")
                    continue
                else:
                    self.logger.warning("Verifier failed after all retries, continuing with default feedback")
                    return {
                        "issues": ["Verifier failed to return valid JSON"],
                        "suggested_fixes": []
                    }

    # ==========================================================
    # STEP 5 — REFACTOR (IMPROVE DRAFT)
    # ==========================================================
    def _refactor_draft(self, draft: str, verifier_feedback: dict) -> str:
        """Refine draft based on verifier feedback."""
        issues = verifier_feedback.get("issues", [])
        fixes = verifier_feedback.get("suggested_fixes", [])
        self.logger.debug(f"Building refactor prompt with {len(issues)} issues and {len(fixes)} fixes...")
        self.logger.debug(f"Original draft length: {len(draft)} characters")
        
        if not issues or (len(issues) == 1 and "Verifier failed" in str(issues[0])):
            self.logger.info("No significant issues found, skipping refactoring")
            return draft
        
        prompt = build_refactor_prompt(
            previous_draft=draft,
            verifier_feedback=verifier_feedback
        )
        self.logger.debug(f"Prompt messages: {len(prompt)} messages")
        
        self.logger.info("Refactoring draft based on verifier feedback...")
        refactor_start = time.time()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                refactored = self.reasoning_llm.generate(prompt)
                
                if not refactored or not refactored.strip():
                    self.logger.warning(f"Refactor returned empty output on attempt {attempt + 1}")
                    if attempt < self.MAX_RETRIES - 1:
                        self.logger.info("Retrying refactoring...")
                        continue
                    else:
                        self.logger.warning("Refactor failed after retries, using original draft")
                        return draft
                
                refactor_time = time.time() - refactor_start
                self.logger.info(f"Refactoring completed in {refactor_time:.2f}s")
                self.logger.debug(f"Refactored draft length: {len(refactored)} characters")
                self.logger.debug(f"Length change: {len(refactored) - len(draft)} characters")
                
                return refactored
                
            except Exception as e:
                refactor_time = time.time() - refactor_start
                self.logger.warning(f"Refactor failed on attempt {attempt + 1}: {str(e)}")
                if attempt < self.MAX_RETRIES - 1:
                    continue
                else:
                    self.logger.warning("Refactor failed after retries, using original draft")
                    return draft

    # ==========================================================
    # STEP 6 — FINAL WRITING
    # ==========================================================
    def _write_final_response(self, refactored_draft: str) -> str:
        """Generate polished final response."""
        if not refactored_draft or not refactored_draft.strip():
            self.logger.error("Refactored draft is empty, cannot generate final response")
            return "Error: No content was generated. Please try again."
        
        self.logger.debug(f"Building writer prompt for refactored draft ({len(refactored_draft)} chars)...")
        prompt = build_writer_prompt(refactored_draft)
        self.logger.debug(f"Prompt messages: {len(prompt)} messages")
        
        self.logger.info("Generating final polished response...")
        writer_start = time.time()
        
        for attempt in range(self.MAX_RETRIES):
            try:
                final = self.writer_llm.generate(prompt)
                
                if not final or not final.strip():
                    self.logger.warning(f"Writer returned empty output on attempt {attempt + 1}")
                    if attempt < self.MAX_RETRIES - 1:
                        self.logger.info("Retrying final writing...")
                        continue
                    else:
                        self.logger.warning("Writer failed after retries, returning refactored draft")
                        return refactored_draft
                
                writer_time = time.time() - writer_start
                self.logger.info(f"Final writing completed in {writer_time:.2f}s")
                self.logger.debug(f"Final response length: {len(final)} characters")
                self.logger.debug(f"Final response preview: {final[:200]}...")
                
                return final
                
            except Exception as e:
                writer_time = time.time() - writer_start
                self.logger.warning(f"Writer failed on attempt {attempt + 1}: {str(e)}")
                if attempt < self.MAX_RETRIES - 1:
                    continue
                else:
                    self.logger.warning("Writer failed after retries, returning refactored draft")
                    return refactored_draft

    # ==========================================================
    # REPAIR MECHANISM (CORE RELIABILITY)
    # ==========================================================
    def _repair(self, llm, bad_output: str, error: str, schema_description: str) -> str:
        """Repair invalid LLM outputs."""
        self.logger.debug("Attempting to repair invalid LLM output...")
        self.logger.debug(f"Error: {error}")
        self.logger.debug(f"Bad output length: {len(bad_output)} characters")
        self.logger.debug(f"Bad output preview: {bad_output[:100]}...")
        
        repair_prompt = [
            {
                "role": "system",
                "content": (
                    "You fix invalid LLM outputs.\n"
                    "Return ONLY valid JSON.\n"
                    "No explanations."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Invalid output:\n{bad_output}\n\n"
                    f"Error:\n{error}\n\n"
                    f"Required schema:\n{schema_description}"
                )
            }
        ]

        repair_start = time.time()
        repaired = llm.generate(repair_prompt)
        repair_time = time.time() - repair_start
        self.logger.debug(f"Repair completed in {repair_time:.2f}s")
        self.logger.debug(f"Repaired output length: {len(repaired)} characters")
        
        return repaired


