from fastapi import FastAPI
from api import upload, chat
from api import tools

app = FastAPI(title="Chapterwise AI Tutor")

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(tools.router)
