import argparse
import logging

from exam_gen import ingest

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Ingest docs into vector DB")
    parser.add_argument('--url', action='append', help='Documentation URL', default=[])
    parser.add_argument('--pdf', action='append', help='Path to PDF', default=[])
    args = parser.parse_args()

    if args.url:
        ingest.ingest_from_urls(args.url)
    if args.pdf:
        ingest.ingest_from_pdfs(args.pdf)


if __name__ == '__main__':
    main()
