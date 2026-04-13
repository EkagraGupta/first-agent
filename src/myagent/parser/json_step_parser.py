import json

def extract_first_json_object(text: str) -> dict:
    text = text.strip()

    start = text.find("{")
    if start == -1:
        raise ValueError(f"No JSON object found in model output: \n\t{text}")
    
    decoder = json.JSONDecoder()
    print(text[start:])
    obj, end = decoder.raw_decode(text[start:])
    return obj


def parse_json_step(text: str) -> dict:
    obj = extract_first_json_object(text)

    if not isinstance(obj, dict):
        raise ValueError("Top-level JSON must be an object")

    step_type = obj.get("type")
    if step_type == "tool":
        name = obj.get("name")
        args = obj.get("args")

        if not isinstance(name, str) or not name:
            raise ValueError("Tool step must include a non-empty 'name'")

        if not isinstance(args, dict):
            raise ValueError("Tool step must include an 'args' object")

        return {
            "type": "tool",
            "name": name,
            "args": args,
        }
    
    if step_type=="final":
        answer = obj.get("answer")
        if not isinstance(answer, str):
            raise ValueError("Final step must include string answer")
        return {
            "type": "final",
            "answer": answer,
        }

    if step_type=="final":
        answer = obj.get("answer")
        if not isinstance(answer, str):
            raise ValueError("Final step must include string answer")
        return {
            "type": "final",
            "answer": answer,
        }
    
    raise ValueError(f"Invalid step type: {step_type}")
