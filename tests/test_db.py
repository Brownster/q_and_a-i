import os
import time

from exam_gen import db, embeddings


def wait_for_db(retries=5):
    for _ in range(retries):
        try:
            conn = db.get_conn()
            conn.close()
            return
        except Exception:
            time.sleep(2)
    raise RuntimeError('DB not available')


def test_insert_and_search():
    wait_for_db()
    db.init_db()
    text = 'terraform state management'
    chunks = ['terraform state management example']
    embs = embeddings.embed_texts(chunks)
    db.insert_chunks('test', chunks, embs)
    results = db.search(embeddings.embed_texts(['state'])[0], top_k=1)
    assert results
    src, chunk = results[0]
    assert src == 'test'
    assert 'terraform' in chunk
