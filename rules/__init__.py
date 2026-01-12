"""
Rules package.
Contains editable rules and configurations for prompts.
Separated from prompts for easier maintenance and updates.
"""

from rules.behavior_rules import (
    get_brand_identity_rules,
    get_behavior_rules,
    get_interaction_guidelines,
    get_restrictions,
    get_memory_usage_instructions
)
from rules.json_schemas import (
    get_intent_schema,
    get_plan_schema,
    get_classifier_schema,
    get_verifier_schema,
    get_json_output_instruction
)
from rules.classification_rules import (
    get_classification_rules,
    get_simple_examples,
    get_complex_examples
)
from rules.plan_constraints import (
    get_plan_constraints,
    get_plan_example
)
from rules.verifier_rules import (
    get_verifier_rules,
    get_verifier_examples
)
from rules.reasoning_rules import (
    get_reasoning_instructions,
    get_memory_context_instruction
)
from rules.refactor_rules import get_refactor_rules
from rules.writer_rules import get_writer_rules

__all__ = [
    "get_brand_identity_rules",
    "get_behavior_rules",
    "get_interaction_guidelines",
    "get_restrictions",
    "get_memory_usage_instructions",
    "get_intent_schema",
    "get_plan_schema",
    "get_classifier_schema",
    "get_verifier_schema",
    "get_json_output_instruction",
    "get_classification_rules",
    "get_simple_examples",
    "get_complex_examples",
    "get_plan_constraints",
    "get_plan_example",
    "get_verifier_rules",
    "get_verifier_examples",
    "get_reasoning_instructions",
    "get_memory_context_instruction",
    "get_refactor_rules",
    "get_writer_rules",
]

