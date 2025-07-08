import fitz, io
from docx import Document
from PIL import Image
import pytesseract


def extract_text_from_file(filename, content):
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=content, filetype="pdf")
        text = "\n".join(page.get_text() for page in doc)
    elif filename.endswith(".docx"):
        doc = Document(io.BytesIO(content))
        text = "\n".join(p.text for p in doc.paragraphs)
    elif filename.endswith((".jpg", ".png", ".jpeg")):
        image = Image.open(io.BytesIO(content))
        text = pytesseract.image_to_string(image)
    else:
        raise ValueError("Unsupported file type")

    chunks = [c.strip() for c in text.split("\n") if len(c.strip()) > 30]
    return text, chunks


def ocr_image(content):
    img = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(img)
