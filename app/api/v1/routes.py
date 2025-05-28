from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.services.caption_service import process_video_and_generate_captions
from app.services.video_service import generate_video_from_captions
import os

router = APIRouter(prefix="/api/v1")

@router.get("/")
def health_check():
    return {"message": "API v1 is live. Visit /docs for Swagger UI."}

@router.post("/generate-captions")
async def generate_captions(video: UploadFile = File(...)):
    return await process_video_and_generate_captions(video)

@router.post("/generate-video")
async def generate_video(
    video_path: str = Form(...),
    corrected_captions: str = Form(...)
):
    output_path = generate_video_from_captions(video_path, corrected_captions)
    return FileResponse(
        path=output_path,
        filename=os.path.basename(output_path),
        media_type="video/mp4"
    )
