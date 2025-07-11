"""Utilities for splitting text into semantically coherent chunks."""

from typing import List

from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(text: str, max_tokens: int = 400) -> List[str]:
    """Split ``text`` into roughly ``max_tokens`` sized chunks.

    Uses ``RecursiveCharacterTextSplitter`` with a ``tiktoken`` encoder so tests
    remain deterministic without an API key.
    """

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=max_tokens,
        chunk_overlap=0,
    )
    return splitter.split_text(text)
