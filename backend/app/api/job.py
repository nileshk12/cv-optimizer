from fastapi import APIRouter
from pydantic import BaseModel
import spacy

router = APIRouter()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class JobDescription(BaseModel):
    title: str
    description: str
    resume_keywords: list  # Add this to accept resume keywords from frontend

@router.post("/analyze")
async def analyze_job(job: JobDescription):
    # Process the job description with spaCy
    doc = nlp(job.description)
    
    # Extract JD keywords
    jd_keywords = []
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in ["experience", "years", "role"]:
            jd_keywords.append(token.text.lower())
    jd_keywords = sorted(list(set(jd_keywords)))
    
    # Compare JD keywords with resume keywords
    missing_skills = [keyword for keyword in jd_keywords if keyword not in job.resume_keywords]
    
    # Suggestions
    suggestions = []
    if missing_skills:
        suggestions.append(f"Consider adding the following skills to your resume: {', '.join(missing_skills)}.")
    
    return {
        "title": job.title,
        "jd_keywords": jd_keywords,
        "missing_skills": missing_skills,
        "suggestions": suggestions if suggestions else ["Your resume already covers most of the job description keywords!"]
    }
