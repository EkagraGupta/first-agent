import json

from myagent.prompting.manual_prompt import render_prompt
from myagent.parser.json_step_parser import parse_json_step
from myagent.agent.executor import execute_tool
from myagent.model.config import MAX_NEW_TOKENS


class Agent:
    def __init__(self, llm, max_steps: int=5):
        self.llm = llm
        self.max_steps = max_steps

    def run(self, user_query: str) -> str:
        history: list[str] = []

        tool_manifest = """
        calculator(a: float, b: float, op: str) -> float
        Performs arithmetic operations. op must be one of: add, sub, mul, div. 
        """

        for step in range(self.max_steps):
            prompt = render_prompt(
                user_query=user_query,
                history=history,
                tool_manifest=tool_manifest,
            )

            model_output = self.llm.generate(prompt, max_new_tokens=MAX_NEW_TOKENS)
            parsed = parse_json_step(text=model_output)

            print(f"\n ===== STEP {step+1} =====")
            print(model_output)

            if parsed["type"]=="final":
                return parsed["answer"]
            
            result = execute_tool(
                tool_name=parsed["name"],
                kwargs=parsed["args"],
            )

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            if step==0:
                history.append(f"User: {user_query}" if step==0 else "")
            history.append(
                "Assistant: " + json.dumps(
                    {
                        "type": "tool",
                        "name": parsed["name"],
                        "args": parsed["args"],
                    },
                    ensure_ascii=False,
                )
            )
            history.append(f"Observation: {result}")

        raise RuntimeError("Max steps reached without getting Final Answer!")