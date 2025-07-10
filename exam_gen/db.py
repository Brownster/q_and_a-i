import os
import psycopg2
from psycopg2.extras import execute_values

DB_PARAMS = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'dbname': os.getenv('DB_NAME', 'exam'),
    'user': os.getenv('DB_USER', 'exam'),
    'password': os.getenv('DB_PASSWORD', 'exam'),
}

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    source TEXT,
    chunk TEXT,
    embedding VECTOR(1536)
);
"""

CREATE_EXT = "CREATE EXTENSION IF NOT EXISTS vector;"


def get_conn():
    return psycopg2.connect(**DB_PARAMS)


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_EXT)
            cur.execute(TABLE_SCHEMA)
        conn.commit()


def insert_chunks(source, chunks, embeddings):
    records = list(zip([source] * len(chunks), chunks, embeddings))
    with get_conn() as conn:
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO documents (source, chunk, embedding) VALUES %s",
                records,
            )
        conn.commit()


def search(query_embedding, top_k=5):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT source, chunk FROM documents ORDER BY embedding <-> %s::vector LIMIT %s",
                (query_embedding, top_k),
            )
            return cur.fetchall()
