from typing import Sequence

SYSTEM_PROMPT = """You are a reasoning agent.

You must follow the format exactly and consider 'Rules' as ground truth.

At each step output:

Thought: <brief reasoning about what to do next, NOT the final answer>
Final Answer: <only the answer>

Rules:
- DO NOT add any text before 'Thought:'.
- DO NOT add any text after 'Final Answer:'.
- Output only those two lines.
- Do not output bullet points.
- Do not output markdown.
- Do not output JSON.
- Do not output code fences.
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

Conversation history:
{history_block}

Current user request:
User: {user_query}

Respond now using exactly:
Thought: ...
Final Answer: ...
"""
    return prompt