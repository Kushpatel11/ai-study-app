import psycopg2
import numpy as np


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",  # your username
    password="Kush@97252",  # your password
    host="localhost",
    port="5432",
)
cur = conn.cursor()


def insert_chapter(name, text):
    cur.execute(
        "INSERT INTO chapters (name, raw_text) VALUES (%s, %s) RETURNING id",
        (name, text),
    )
    chapter_id = cur.fetchone()[0]
    conn.commit()
    return chapter_id


def insert_chunks(chapter_id, chunks, embeddings):
    for chunk, embed in zip(chunks, embeddings):
        cur.execute(
            "INSERT INTO chunks (chapter_id, chunk_text, embedding) VALUES (%s, %s, %s)",
            (chapter_id, chunk, embed.tolist()),
        )
    conn.commit()


def search_similar_chunk(chapter_id, question_embedding, threshold=0.6):
    norm_embed = question_embedding / np.linalg.norm(question_embedding)

    cur.execute(
        """
        SELECT chunk_text, embedding <#> %s::vector AS distance
        FROM chunks
        WHERE chapter_id = %s
        ORDER BY distance
        LIMIT 1
        """,
        (norm_embed.tolist(), chapter_id),
    )

    result = cur.fetchone()
    if result:
        similarity = 1 - result[1]
        if similarity >= threshold:
            return result[0], similarity
        else:
            return None, similarity  # ❌ No good match
    return None, 0.0


def log_question(chapter_id, question, answer=""):
    cur.execute(
        "INSERT INTO questions (chapter_id, question, answer) VALUES (%s, %s, %s)",
        (chapter_id, question, answer),
    )
    conn.commit()


def get_chapter_id_by_name(name):
    cur.execute("SELECT id FROM chapters WHERE name = %s", (name,))
    result = cur.fetchone()
    return result[0] if result else None
