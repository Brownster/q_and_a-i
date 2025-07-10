import argparse
import json

from exam_gen.generate import generate_exam


def main():
    parser = argparse.ArgumentParser(description="Generate exam JSON from objectives")
    parser.add_argument("objectives", help="Text file with one objective per line")
    parser.add_argument("output", help="Output JSON file")
    parser.add_argument("-n", type=int, default=150, help="Number of questions to generate")
    args = parser.parse_args()

    with open(args.objectives) as f:
        objs = [line.strip() for line in f if line.strip()]

    qas = generate_exam(objs, n=args.n)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(qas, f, indent=2)


if __name__ == "__main__":
    main()
