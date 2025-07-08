from fastapi import APIRouter, Form, UploadFile, File
from core.extractor import ocr_image
from core.ollama_helper import ollama_answer
from storage.db import get_chapter_id_by_name, search_similar_chunk, log_question
import numpy as np
from core.embedding_model import model


router = APIRouter()


@router.post("/chat")
async def chat(question: str = Form(...), chapter: str = Form(...)):
    chapter_id = get_chapter_id_by_name(chapter)
    if not chapter_id:
        return {"error": "Chapter not uploaded."}

    q_embed = model.encode([question])[0]
    chunk, similarity = search_similar_chunk(chapter_id, np.array(q_embed))

    # Context: use best chunk if similar, else full chapter can be fallback (optional)
    context = chunk if chunk and similarity > 0.5 else ""

    # Ask local LLM (Mistral via Ollama)
    response = ollama_answer(question, context)

    log_question(chapter_id, question, response)

    return {
        "answer": response,
        "similarity": float(similarity),
    }


@router.post("/upload-question-image")
async def upload_image(file: UploadFile = File(...), chapter: str = Form(...)):
    text = ocr_image(await file.read())
    return await chat(question=text, chapter=chapter)
