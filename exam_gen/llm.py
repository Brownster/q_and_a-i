import os
import hashlib
import json
from typing import List, Dict, Any

import openai

MODEL = os.getenv("CHAT_MODEL", "gpt-3.5-turbo")
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat(messages: List[Dict[str, str]], **kwargs) -> str:
    """Call OpenAI chat completion with fallback deterministic output."""
    if openai.api_key:
        response = openai.chat.completions.create(model=MODEL, messages=messages, **kwargs)
        return response.choices[0].message.content.strip()
    # Fallback deterministic stub
    text = " ".join(m.get("content", "") for m in messages)
    h = hashlib.sha256(text.encode()).hexdigest()
    return f"Stub response to: {h[:8]}"


def _chat_function(messages: List[Dict[str, str]], schema: Dict[str, Any], func_name: str,
                   **kwargs) -> Dict[str, Any]:
    """Helper for calling a chat completion that returns structured data."""

    if openai.api_key:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[{"type": "function", "function": {
                "name": func_name,
                "description": "Return structured data",
                "parameters": schema,
            }}],
            tool_choice={"type": "function", "function": {"name": func_name}},
            **kwargs,
        )
        args = response.choices[0].message.tool_calls[0].function.arguments
        return json.loads(args)

    # Deterministic fallback for tests
    text = chat(messages, **kwargs)
    # naive placeholder values based on schema
    if schema.get("type") == "object":
        result = {}
        for key, prop in schema.get("properties", {}).items():
            if prop.get("type") == "array":
                result[key] = [text]
            else:
                result[key] = text
        return result
    return {"result": text}


def chat_structured(messages: List[Dict[str, str]], **kwargs) -> Dict[str, str]:
    """Return structured answer/explanation pairs."""

    schema = {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "explanation": {"type": "string"},
        },
        "required": ["answer", "explanation"],
    }

    return _chat_function(messages, schema, "format_answer", **kwargs)


def chat_list(messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
    """Return a list of strings using structured function calling."""

    schema = {
        "type": "object",
        "properties": {
            "distractors": {
                "type": "array",
                "items": {"type": "string"},
            }
        },
        "required": ["distractors"],
    }

    return _chat_function(messages, schema, "format_distractors", **kwargs)
