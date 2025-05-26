from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import resume
from app.api import job

app = FastAPI(title="CV Optimizer API")
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://54.218.89.19:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routes
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(job.router, prefix="/api/job", tags=["Job Description"])

@app.get("/")
def root():
    return {"message": "CV Optimizer Backend is running."}
