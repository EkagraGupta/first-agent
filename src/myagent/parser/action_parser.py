import ast


def _extract_call_expression(action_str: str) -> str:
    # TODO: Should not be needed, 'Action' should only contain tool func call
    action_str = action_str.strip()
    start = action_str.find("(")

    if start == -1:
        return action_str

    depth = 0
    in_string = False
    string_quote = ""
    escaped = False

    for idx, char in enumerate(action_str):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == string_quote:
                in_string = False
            continue

        if char in {"'", '"'}:
            in_string = True
            string_quote = char
            continue

        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return action_str[: idx + 1].strip()

    return action_str


def parse_action(action_str: str) -> tuple[str, dict]:
    """
    Example:
    calculator(a=8, b=2, op='div')
    """

    call_expr = _extract_call_expression(action_str)
    node = ast.parse(call_expr, mode="eval")
    expr = node.body

    if not isinstance(expr, ast.Call):
        raise ValueError("Action must be a function call")
    
    if not isinstance(expr.func, ast.Name):
        raise ValueError("Only direct function names are allowed")
    
    tool_name = expr.func.id
    kwargs = {}

    if expr.args:
        raise ValueError("Only keyword arguments are allowed in actions")
    
    for kw in expr.keywords:
        if kw.arg is None:
            raise ValueError("**kwargs are not allowed")
        kwargs[kw.arg] = ast.literal_eval(kw.value)
    
    return tool_name, kwargs


if __name__=="__main__":
    tool_name, kwargs = parse_action("calculator(a=8, b=2, op='div')")

    print(f"Tool name: {tool_name}\nkwargs: {kwargs}")
