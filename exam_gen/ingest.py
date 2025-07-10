import logging
import os
from typing import List

import fitz  # PyMuPDF
import requests
from bs4 import BeautifulSoup

from .chunker import chunk_text
from .embeddings import embed_texts
from . import db

logger = logging.getLogger(__name__)


def fetch_html(url: str) -> str:
    logger.info("Fetching %s", url)
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    # remove navigation
    for nav in soup(['nav', 'header', 'footer', 'script']):
        nav.decompose()
    text = soup.get_text(separator=' ')
    return text


def parse_pdf(path: str) -> str:
    logger.info("Parsing PDF %s", path)
    doc = fitz.open(path)
    text = " ".join(page.get_text() for page in doc)
    doc.close()
    return text


def ingest(source: str, text: str):
    db.init_db()
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    db.insert_chunks(source, chunks, embeddings)


def ingest_from_urls(urls: List[str]):
    for url in urls:
        text = fetch_html(url)
        ingest(url, text)


def ingest_from_pdfs(paths: List[str]):
    for path in paths:
        text = parse_pdf(path)
        ingest(os.path.basename(path), text)

