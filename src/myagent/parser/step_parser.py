import re

def parse_step(text: str) -> dict:
    text = text.strip()

    thought_match = re.search(r"^Thought:\s*(.+)$", text, re.MULTILINE)
    action_match = re.search(r"^Action:\s*(.+)$", text, re.MULTILINE)
    final_match = re.search(r"^Final Answer:\s*(.+)$", text, re.MULTILINE)

    thought = thought_match.group(1).strip() if thought_match else None
    action = action_match.group(1).strip() if action_match else None
    final = final_match.group(1).strip() if final_match else None

    return {
        "thought": thought,
        "action": action,
        "final": final,
        "raw": text,
    }