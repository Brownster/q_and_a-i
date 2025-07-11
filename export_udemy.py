import argparse
import json

from exam_gen.export import to_udemy_csv


def main():
    parser = argparse.ArgumentParser(
        description="Convert exam JSON to Udemy multiple-choice CSV"
    )
    parser.add_argument("input", help="Input exam JSON file")
    parser.add_argument("output", help="Output CSV path")
    args = parser.parse_args()

    with open(args.input) as f:
        qas = json.load(f)

    to_udemy_csv(qas, args.output)


if __name__ == "__main__":
    main()
