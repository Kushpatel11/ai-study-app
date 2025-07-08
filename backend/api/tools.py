from fastapi import APIRouter, Query
from storage.db import get_chapter_id_by_name  # ✅ Use DB instead of storage
from core.ollama_helper import ollama_answer
from storage.db import conn

router = APIRouter()


@router.get("/chapter-summary")
async def chapter_summary(chapter: str = Query(...)):
    chapter_id = get_chapter_id_by_name(chapter)
    if not chapter_id:
        return {"error": "Chapter not uploaded."}

    # ✅ Fetch raw_text directly from DB
    cur = conn.cursor()
    cur.execute("SELECT raw_text FROM chapters WHERE id = %s", (chapter_id,))
    result = cur.fetchone()

    if not result:
        return {"error": "Chapter text not found."}

    full_text = result[0][:5000]  # Optional cutoff for LLM

    # 🧠 Ask Ollama to summarize
    summary = ollama_answer(
        "Summarize this chapter",
        f"""
You are an expert ICSE tutor.

Summarize the following chapter into:
1. A brief overview (2-3 lines)
2. List of important formulas
3. Key concepts or tips students should remember

Chapter:
{full_text}
""",
    )

    return {"summary": summary}
