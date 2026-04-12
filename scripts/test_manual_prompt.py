import sys
from pathlib import Path

# Allow running script directly
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from myagent.model.generate import MyLLM
from myagent.prompting.manual_prompt import render_prompt

from myagent.model.config import MODEL_ID

def main() -> None:
    llm = MyLLM(model_id=MODEL_ID)

    user_query = "If I have 8 balls and out of those half of the balls are blue, how many blue balls do i have?"
    prompt = render_prompt(user_query=user_query)

    output = llm.generate(prompt, max_new_tokens=80)

    print(output)

if __name__=="__main__":
    main()