import os
import hashlib
import json
from typing import List, Dict

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


def chat_structured(messages: List[Dict[str, str]], **kwargs) -> Dict[str, str]:
    """Return structured answer/explanation pairs using OpenAI function calling."""

    if openai.api_key:
        response = openai.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "format_answer",
                        "description": "Formats the final answer and explanation.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "answer": {"type": "string"},
                                "explanation": {"type": "string"},
                            },
                            "required": ["answer", "explanation"],
                        },
                    },
                }
            ],
            tool_choice={"type": "function", "function": {"name": "format_answer"}},
            **kwargs,
        )
        args = response.choices[0].message.tool_calls[0].function.arguments
        return json.loads(args)

    # Deterministic fallback for tests
    text = chat(messages, **kwargs)
    return {"answer": text, "explanation": ""}
