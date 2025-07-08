from fastapi import APIRouter, UploadFile, Form, File
from core.extractor import extract_text_from_file
from storage.db import insert_chapter, insert_chunks
from core.embedding_model import model


router = APIRouter()


@router.post("/upload-material")
async def upload_material(chapter: str = Form(...), file: UploadFile = File(...)):
    content = await file.read()
    try:
        # Step 1: Extract full text & chunks
        text, chunks = extract_text_from_file(file.filename, content)

        # Step 2: Embed chunks
        embeddings = model.encode(chunks)

        # Step 3: Store in PostgreSQL
        chapter_id = insert_chapter(chapter, text)
        insert_chunks(chapter_id, chunks, embeddings)

        return {"message": f"Chapter '{chapter}' uploaded and saved in database."}
    except Exception as e:
        return {"error": str(e)}
