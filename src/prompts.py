"""Prompt and message construction for the LLM calls."""
 

REQUIREMENT_GENERATION_SYSTEM_PROMPT: str = """
You write concise functional requirements describing a change between
two versions of a function. Focus on behavior and intent, not
implementation details. Return plain text only, 1-3 sentences.
"""

REQUIREMENT_GENERATION_USER_PROMPT: str = """
Old function code:\n
---\n
{old_code}\n
---\n\n
New function code:\n
---\n
{new_code}\n
---\n\n
Write the functional requirement describing the change.
"""

FUNCTION_GENERATION_SYSTEM_PROMPT: str = """
You generate an updated function from an old function and a 
requirement. Return only the updated function code, with no extra 
explanations or code fences. Preserve the signature and indentation.
"""

FUNCTION_GENERATION_USER_PROMPT: str = """
Old function code:\n
---\n
{old_code}\n
---\n\n
Requirement:\n
---\n
{requirement}\n
---\n\n
Return the updated function code only.
"""
