import csv
from typing import List, Dict


def to_udemy_csv(qas: List[Dict], path: str) -> None:
    """Write Q/A pairs to a simplified Udemy-compatible CSV."""
    fieldnames = ["Question", "Answer", "Explanation"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for qa in qas:
            writer.writerow({
                "Question": qa.get("question", ""),
                "Answer": qa.get("answer", ""),
                "Explanation": qa.get("explanation", ""),
            })
