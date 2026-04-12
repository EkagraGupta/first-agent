import sys
from pathlib import Path

# Allow running script directly
sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from myagent.model.generate import MyLLM
from myagent.agent.loop import Agent

from myagent.model.config import MODEL_ID

def main():
    llm = MyLLM(model_id=MODEL_ID)
    agent = Agent(llm)

    result = agent.run("What is half of 8?")
    print(f"\n Final result: {result}")


if __name__=="__main__":
    main()