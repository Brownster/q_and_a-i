from exam_gen import db, embeddings
from exam_gen.generate import generate_exam


def setup_module(module):
    db.init_db()
    db.clear()
    chunks = ["This is a unique snippet for generate tests"]
    embs = embeddings.embed_texts(chunks)
    db.insert_chunks("generate", chunks, embs)


def test_generate_exam():
    results = generate_exam(["terraform"], n=1)
    assert len(results) == 1
    qa = results[0]
    assert "question" in qa and qa["question"]
    assert "answer" in qa
    assert "explanation" in qa
    assert "distractors" in qa and isinstance(qa["distractors"], list)
