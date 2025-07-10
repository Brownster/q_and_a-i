from typing import List


def chunk_text(text: str, max_tokens: int = 400) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_tokens):
        chunk = ' '.join(words[i:i+max_tokens])
        chunks.append(chunk)
    return chunks
