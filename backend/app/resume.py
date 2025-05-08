from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    # Stub for parsing logic
    return {"filename": file.filename, "status": "Resume received"}