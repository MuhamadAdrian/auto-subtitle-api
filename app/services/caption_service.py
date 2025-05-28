from fastapi import UploadFile
from app.subtitles import extract_subtitles

async def process_video_and_generate_captions(video: UploadFile):
    video_bytes = await video.read()
    video_path, segments, video_file_name = extract_subtitles(video_bytes)
    
    mapped_captions = [
        {"start": segment["start"], "end": segment["end"], "text": segment["text"]}
        for segment in segments
    ]

    return {
        "data": {
            "file_name": video_file_name,
            "captions": mapped_captions
        }
    }
