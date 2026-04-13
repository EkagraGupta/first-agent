# tests/test_json_step_parser.py
import pytest

from src.myagent.parser.json_step_parser import *

def test_extracts_first_json_object_when_model_overgenerates():
    text = (
        '{"type":"tool","name":"calculator","args":{"a":8,"b":2,"op":"div"}}\n'
        'Do not include anything else.'
    )
    obj = extract_first_json_object(text)
    pass
    assert obj=={
        "type": "tool",
        "name": "calculator",
        "args": {
            "a": 8,
            "b": 2,
            "op": "div",
        }
    }


def test_parse_tool_step():
    text = '{"type":"tool","name":"calculator","args":{"a":7,"b":6,"op":"mul"}}'
    parsed = parse_json_step(text)
    assert parsed["type"]=="tool"
    assert parsed["name"]=="calculator"
    assert parsed["args"]=={
        "a": 7,
        "b": 6,
        "op": "mul",
    }


def test_parse_final_step():
    text = '{"type":"final","answer":"42"}'
    parsed = parse_json_step(text)
    assert parsed == {"type": "final", "answer": "42"}


def test_rejects_missing_type():
    with pytest.raises(ValueError, match="Invalid step type"):
        parse_json_step('{"answer": "42"}')


def test_rejects_tool_without_args_object():
    with pytest.raises(ValueError, match="args"):
        parse_json_step('{"type":"tool","name":"calculator","args":"bad"}')


def test_rejects_final_without_string_answer():
    with pytest.raises(ValueError, match="string answer"):
        parse_json_step('{"type":"final","answer":42}')
