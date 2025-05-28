import os
import uuid
from moviepy import VideoFileClip
from app.whisper_model import model
from app.utils import UPLOAD_FOLDER

def extract_subtitles(video_file_bytes):
    video_file_name = f"uploaded_{uuid.uuid4().hex}.mp4"
    input_video_path = os.path.join(UPLOAD_FOLDER, video_file_name)
    with open(input_video_path, "wb") as f:
        f.write(video_file_bytes)

    temp_audio_path = os.path.join(UPLOAD_FOLDER, f"temp_audio_{uuid.uuid4().hex}.wav")
    video = VideoFileClip(input_video_path)
    video.audio.write_audiofile(temp_audio_path)

    result = model.transcribe(temp_audio_path)
    segments = split_segments_by_max_words(result["segments"], max_words=7)

    os.remove(temp_audio_path)
    return input_video_path, segments, video_file_name

def split_segments_by_max_words(segments, max_words=7):
    new_segments = []
    for seg in segments:
        words = seg['text'].strip().split()
        start_time = seg['start']
        end_time = seg['end']
        duration = end_time - start_time

        if len(words) <= max_words:
            new_segments.append(seg)
        else:
            dur_per_word = duration / len(words)
            for i in range(0, len(words), max_words):
                chunk_words = words[i:i+max_words]
                chunk_text = ' '.join(chunk_words)
                chunk_start = start_time + i * dur_per_word
                chunk_end = chunk_start + len(chunk_words) * dur_per_word
                new_segments.append({
                    "start": chunk_start,
                    "end": chunk_end,
                    "text": chunk_text
                })
    return new_segments
