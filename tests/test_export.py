import csv
from exam_gen.export import to_udemy_csv


def test_to_udemy_csv(tmp_path):
    qas = [
        {
            "question": "What is Terraform?",
            "answer": "A tool",
            "explanation": "IaC",
            "distractors": ["A language", "A cloud", "An OS"],
        }
    ]
    out = tmp_path / "out.csv"
    to_udemy_csv(qas, out)
    with open(out) as f:
        rows = list(csv.DictReader(f))
    row = rows[0]
    assert row["Question Text"] == "What is Terraform?"
    options = [row["Answer 1"], row["Answer 2"], row["Answer 3"], row["Answer 4"]]
    assert set(options) >= set(qas[0]["distractors"] + ["A tool"])
    assert row["Correct Answer"] in {"1", "2", "3", "4"}
    assert row["Explanation"] == "IaC"
