from exam_gen import db, embeddings
from exam_gen.quality import evaluate


def setup_module(module):
    db.init_db()
    db.clear()
    chunk = "Terraform is an infrastructure as code tool."
    db.insert_chunks("qa", [chunk], embeddings.embed_texts([chunk]))


def test_evaluate():
    qas = [{
        "objective": "terraform",
        "question": "What is Terraform?",
        "answer": "Terraform is an infrastructure as code tool.",
        "context": "Terraform is an infrastructure as code tool.",
        "distractors": [
            "A configuration language",
            "A cloud service",
            "A monitoring tool",
        ],
    }]
    score = evaluate(qas)
    assert score >= 0.8

