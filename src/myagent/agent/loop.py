from myagent.prompting.manual_prompt import render_prompt
from myagent.parser.step_parser import parse_step
from myagent.parser.action_parser import parse_action
from myagent.agent.executor import execute_tool


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

            model_output = self.llm.generate(prompt, max_new_tokens=200)
            parsed = parse_step(model_output)

            print(f"\n ===== STEP {step+1} =====")
            print(model_output)

            if parsed["final"]:
                return parsed["final"]

            if not parsed["action"]:
                raise RuntimeError("Model produced neither Action nor Final Answer")
            
            tool_name, kwargs = parse_action(parsed["action"])
            result = execute_tool(
                tool_name=tool_name,
                kwargs=kwargs,
            )

            history.append(f"User: {user_query}" if step==0 else "")
            history.append(f"Thought: {parsed['thought']}")
            history.append(f"Action: {parsed['action']}")
            history.append(f"Observation: {result}")

        raise RuntimeError("Max steps reached without getting Final Answer!")