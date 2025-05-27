from fastapi import APIRouter, UploadFile, File
from pdfminer.high_level import extract_text
from docx import Document
import io
import spacy

router = APIRouter()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file: UploadFile) -> str:
    content = file.file.read()
    pdf_file = io.BytesIO(content)
    text = extract_text(pdf_file)
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    content = file.file.read()
    docx_file = io.BytesIO(content)
    doc = Document(docx_file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_keywords(text: str) -> list:
    doc = nlp(text)
    keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in ["experience", "years", "role"]:
            keywords.append(token.text.lower())
    return sorted(list(set(keywords)))

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Extract text based on file type
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        resume_text = extract_text_from_docx(file)
    else:
        return {"error": "Unsupported file format. Please upload a PDF or DOCX file."}

    # Extract keywords from the resume
    resume_keywords = extract_keywords(resume_text)

    return {
        "filename": file.filename,
        "status": "Resume processed",
        "content": resume_text[:500],  # First 500 characters
        "keywords": resume_keywords
    }
