# AI Certification Exam Generator

This repository contains a prototype pipeline that ingests official
Terraform documentation and PDFs into a vector database. Later
milestones will generate practice exam questions from this corpus.

## Quick Start

1. Copy `.env.example` to `.env` and adjust values if needed.
2. Start Postgres with `docker compose up -d`.
3. Install dependencies: `pip install -r requirements.txt`.
4. Ingest content with your own PDF:
   ```bash
   python ingest.py --url https://developer.hashicorp.com/terraform/docs --pdf path/to/terraform.pdf
   ```
5. Run a retrieval test:
   ```python
   from exam_gen import retrieval
   print(retrieval.query("terraform backend"))
   ```

## Development

Tests run against the Docker database. Use:

```bash
docker compose up -d
pytest
```

CI is configured via GitHub Actions in `.github/workflows/ci.yml`.
