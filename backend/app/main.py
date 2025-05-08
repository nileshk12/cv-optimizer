from fastapi import FastAPI
from app.api import resume, job

app = FastAPI(title="CV Optimizer API")

# Include routes
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(job.router, prefix="/api/job", tags=["Job Description"])

@app.get("/")
def root():
    return {"message": "CV Optimizer Backend is running."}