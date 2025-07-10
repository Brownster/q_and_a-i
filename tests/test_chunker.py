from exam_gen.chunker import chunk_text


def test_chunk_text():
    text = 'word ' * 900
    chunks = chunk_text(text, max_tokens=400)
    assert len(chunks) == 3
    assert all(len(c.split()) <= 400 for c in chunks)
