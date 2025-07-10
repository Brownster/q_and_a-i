import os
import hashlib
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
