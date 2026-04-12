from typing import Sequence

SYSTEM_PROMPT = """You are an AI agent that must use tools to solve problems.

You are NOT allowed to compute answers yourself if a tool exists.

Available tools:
{tool_manifest}

Decision rules:
- If the question involves calculation → MUST use calculator
- If a relevant tool exists → MUST use it
- Only answer directly if NO tool can help

Output format:

If using a tool:
Thought: <why you need the tool>
Action: tool_name(arg=value)

If answering:
Thought: <why you can answer directly>
Final Answer: <answer>

Strict rules:
- Never skip tool usage when available
- Never compute math yourself
- Output exactly one Thought
- Then either Action OR Final Answer
- After an Observation is present in the conversation history, do not call a tool again for the same solved subproblem
- After receiving an Observation from a tool, use it to produce a Final Answer on the next turn unless another tool is still required
- The Action line must contain only the tool call and nothing else
- Do not add any explanation, punctuation, or commentary after the tool call
- Do not put the action on multiple lines
- Do not repeat the thought inside the Action line
- Do not repeat the Action after the Action line
- The Final Answer line must contain only the answer and nothing else
"""

EXAMPLES = """
Example 1:
User: What is 10 + 5?
Thought: This is a calculation, so I must use the calculator tool.
Action: calculator(a=10, b=5, op="add")

Example 2:
User: What is 7 * 6?
Thought: This requires multiplication, so I will use the calculator.
Action: calculator(a=7, b=6, op="mul")

Example 3:
User: What is the capital of France?
Thought: No tool is needed for this.
Final Answer: Paris

Example 4:
User: What is half of 8?
Thought: This requires division, so I must use the calculator tool.
Action: calculator(a=8, b=2, op="div")
Observation: 4.0
Thought: I have the calculator result, so I can answer the user directly.
Final Answer: 4.0

Invalid example 1:
Thought: I should use the calculator.
Action: calculator(a=8, b=2, op="div") because half means divide by 2

Invalid example 2:
Thought: I can answer directly.
Final Answer: Paris because no tool is needed

Invalid example 3:
User: What is half of 8?
Thought: This requires division, so I must use the calculator tool.
Action: calculator(a=8, b=2, op="div")
Observation: 4.0
Thought: I already have the result, but I will call the calculator again.
Action: calculator(a=8, b=2, op="div")
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

    {EXAMPLES}

    Available tools:
    {tool_manifest}

    Conversation history:
    {history_block}

    Current user request:
    User: {user_query}

    Respond now:
    Remember: the Action line must be exactly one tool call, with no extra words.
    If the history already contains an Observation that answers the user, respond with Final Answer.
"""
    
    return prompt
