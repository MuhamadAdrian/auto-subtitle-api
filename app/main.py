from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from app.subtitles import extract_subtitles, split_segments_by_max_words
from app.video_generator import generate_video_with_subtitles
import uuid
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API is live. Visit /docs for Swagger UI."}

@app.post("/generate-captions")
async def generate_captions(video: UploadFile = File(...)):
    video_bytes = await video.read()
    video_path, segments = extract_subtitles(video_bytes)
    captions = list(map(lambda segment: {
        "start": segment["start"], 
        "end": segment["end"], 
        "text": segment["text"]
    }, segments))
    return {
        "data": {
          "captions": captions
        }
    }

@app.post("/generate-video")
async def generate_video(
    video_path: str = Form(...),
    corrected_captions: str = Form(...)
):
    output_path = generate_video_with_subtitles(video_path, corrected_captions)
    return FileResponse(path=output_path, filename=os.path.basename(output_path), media_type="video/mp4")
