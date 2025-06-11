from fastapi import APIRouter, UploadFile, File
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.skill_extractor_class import SkillExtractor
from skillNer.general_params import SKILL_DB
from pdfminer.high_level import extract_text
from docx import Document
import io
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Load spaCy model and initialize SkillExtractor
nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab)
skill_extractor = SkillExtractor(nlp, SKILL_DB, matcher)

# Define a Pydantic model for the response
class ResumeResponse(BaseModel):
    filename: str
    content: str
    keywords: List[str]

def extract_text_from_pdf(file: UploadFile) -> str:
    content = file.file.read()
    text = extract_text(io.BytesIO(content))
    return text

def extract_text_from_docx(file: UploadFile) -> str:
    content = file.file.read()
    doc = Document(io.BytesIO(content))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

@router.post("/upload", response_model=ResumeResponse)
async def upload_resume(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        content = extract_text_from_pdf(file)
    elif file.filename.endswith(".docx"):
        content = extract_text_from_docx(file)
    else:
        return {"error": "Unsupported file format. Please upload a PDF or DOCX file."}

    # Extract skills using skillNer
    annotations = skill_extractor.annotate(content)
    skills = []
    for match in annotations["results"]["full_matches"]:
        skills.append(match["doc_node_value"].lower())
    for match in annotations["results"]["ngram_scored"]:
        skills.append(match["doc_node_value"].lower())
    
    skills = sorted(list(set(skills)))
    
    return ResumeResponse(
        filename=file.filename,
        content=content,
        keywords=skills
    )
