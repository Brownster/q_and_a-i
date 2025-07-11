"""CSV export utilities."""

import csv
import random
from typing import List, Dict


def to_udemy_csv(qas: List[Dict], path: str) -> None:
    """Write questions in Udemy's multiple-choice CSV format."""

    fieldnames = [
        "Question Text",
        "Question Type",
        "Answer 1",
        "Answer 2",
        "Answer 3",
        "Answer 4",
        "Correct Answer",
        "Explanation",
    ]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for qa in qas:
            correct = qa.get("answer", "")
            distractors = qa.get("distractors", [])

            # Combine correct answer with distractors and shuffle
            options = [correct] + distractors
            random.shuffle(options)

            # Ensure exactly four options
            while len(options) < 4:
                options.append("")
            options = options[:4]

            correct_idx = options.index(correct) + 1  # 1-based index

            writer.writerow({
                "Question Text": qa.get("question", ""),
                "Question Type": "multiple-choice",
                "Answer 1": options[0],
                "Answer 2": options[1],
                "Answer 3": options[2],
                "Answer 4": options[3],
                "Correct Answer": str(correct_idx),
                "Explanation": qa.get("explanation", ""),
            })
