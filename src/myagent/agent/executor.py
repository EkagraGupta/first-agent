from myagent.tools.registry import TOOLS


def execute_tool(tool_name: str, kwargs: dict):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    tool_fn = TOOLS[tool_name]
    return tool_fn(**kwargs)

