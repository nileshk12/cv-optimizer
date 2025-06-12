from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import resume, job

app = FastAPI(title="CV Optimizer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://54.212.237.103:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory to serve optimized CVs
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(job.router, prefix="/api/job", tags=["Job Description"])

@app.get("/")
def root():
    return {"message": "CV Optimizer Backend is running."}
