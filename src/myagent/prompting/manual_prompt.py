from typing import Sequence

SYSTEM_PROMPT = """You are an AI agent.

Return exactly one JSON object and nothing else.

Valid formats:

{"type":"tool","name":"calculator","args":{"a":8,"b":2,"op":"div"}}

{"type":"final","answer":"4"}

Rules:
- For arithmetic, use calculator first.
- After an Observation is available, return a final answer.
- No explanations.
- No markdown.
- No extra text.
"""

EXAMPLES = """Example 1
User: What is 10 + 5?
{"type":"tool","name":"calculator","args":{"a":10,"b":5,"op":"add"}}

Example 2
User: What is half of 8?
{"type":"tool","name":"calculator","args":{"a":8,"b":2,"op":"div"}}

Example 3
Conversation history:
User: What is half of 8?
Assistant: {"type":"tool","name":"calculator","args":{"a":8,"b":2,"op":"div"}}
Observation: 4
Current user request:
What is half of 8?
{"type":"final","answer":"4"}

Example 4
User: What is the capital of France?
{"type":"final","answer":"Paris"}
"""

def render_prompt(
        user_query: str,
        history: Sequence[str] | None=None,
        tool_manifest: str = "No tools are currently available.",
) -> str:
    history = history or []
    history_block = "\n".join(history).strip()

    if not history_block:
        history_block = "(empty)"
    
    prompt = f"""{SYSTEM_PROMPT}

    Available tools:
    {tool_manifest}

    Examples:
    {EXAMPLES}

    Conversation history:
    {history_block}

    Current user request:
    {user_query}

    Respond with exactly one JSON object:
"""
    
    return prompt
