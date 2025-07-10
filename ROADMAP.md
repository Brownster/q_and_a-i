# Project Roadmap

This roadmap summarizes the four-week prototype schedule for building an AI pipeline that generates practice exams from documentation and PDFs. Each week has specific deliverables. Week 1 details are expanded below.

## Milestone Overview

| Week | Deliverables | Key Tasks |
| ---- | ------------ | --------- |
| **W1 – Scaffold & Ingest** | - Repo with Docker Compose<br>- Vector database seeded with Terraform docs and provided PDFs | 1. Spin up Postgres with `pgvector`.<br>2. Write ingestion script to scrape HashiCorp docs and parse the PDF.<br>3. Chunk text (~400 tokens) and store embeddings.<br>4. Smoke-test retrieval with a sample query. |
| **W2 – Agent Graph POC** | - Initial LangGraph (or CrewAI) flow that produces 5 Q/A pairs | Define Researcher, Questioner, Answerer, and Reviewer agents and connect them via function calls. |
| **W3 – Quality Harness** | - Automated evaluation script<br>- ≥80% factual-consistency score | Implement self-consistency checks and document-grounding verification. |
| **W4 – Packaging & Beta** | - 150 Terraform questions exported for Udemy<br>- Runbook in README | Convert JSON to Udemy format, generate exams, and prepare a Docker release. |

## Detailed Plan for Week 1

1. **Repository Setup**
   - Initialize Python project structure and add a `Dockerfile` plus `docker-compose.yml` for running Postgres with the `pgvector` extension.
   - Define environment variables for database connection and the OpenAI API key in `.env.example`.

2. **Postgres + pgvector**
   - Use Docker Compose to launch a Postgres 15 container.
   - Install the `pgvector` extension so embeddings can be stored efficiently.
   - Create a database schema with a table to hold document chunks and their embeddings.

3. **Ingestion Script**
   - Write `ingest.py` that accepts paths or URLs to documentation.
   - For HashiCorp Terraform docs, retrieve HTML pages and clean out navigation using BeautifulSoup.
   - Parse the provided PDF with `pdfminer` or `PyMuPDF`.
   - Break text into ~400 token windows and generate embeddings via the OpenAI API (`text-embedding-3`).
   - Insert chunks and embeddings into Postgres.

4. **Smoke Test**
   - Run a simple retrieval query like `similarity_search("terraform backend")` to ensure embeddings are stored correctly and search is operational.
   - Log sample outputs for review.

5. **Verification & Commit**
   - Document setup commands and usage in the README.
   - Commit all configuration files and the ingestion script once the pipeline successfully stores and retrieves example chunks.

This detailed Week 1 plan provides enough guidance to start coding the ingestion layer and ensure we have a working vector store by the end of the first sprint.
