import csv
from exam_gen.export import to_udemy_csv


def test_to_udemy_csv(tmp_path):
    qas = [{"question": "What is Terraform?", "answer": "A tool", "explanation": "IaC"}]
    out = tmp_path / "out.csv"
    to_udemy_csv(qas, out)
    with open(out) as f:
        rows = list(csv.DictReader(f))
    assert rows[0]["Question"] == "What is Terraform?"
    assert rows[0]["Answer"] == "A tool"
    assert rows[0]["Explanation"] == "IaC"
