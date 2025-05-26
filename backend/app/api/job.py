from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class JobDescription(BaseModel):
    title: str
    description: str

@router.post("/analyze")
async def analyze_job(job: JobDescription):
    # Stub for JD analysis
    return {"title": job.title, "keywords": ["python", "aws"]}
