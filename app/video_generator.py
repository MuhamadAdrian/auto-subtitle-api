import os
import uuid
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
from app.utils import FONT_PATH, OUTPUT_FOLDER

def generate_video_with_subtitles(video_path, corrected_text):
    output_video_path = os.path.join(OUTPUT_FOLDER, f"output_{uuid.uuid4().hex}.mp4")
    video = VideoFileClip(video_path)

    corrected_segments = corrected_text.strip().split('\n')
    new_segments = []
    for line in corrected_segments:
        if "]" in line:
            time_part, text = line.split("] ", 1)
            time_range = time_part.strip("[").split(" - ")
            start, end = float(time_range[0]), float(time_range[1])
            new_segments.append({"start": start, "end": end, "text": text})

    subtitles = []
    for seg in new_segments:
        subtitle = (TextClip(text=seg["text"], font=FONT_PATH, fontsize=32, color='white', bg_color='black')
                    .set_position(("center", video.h - 300))
                    .set_start(seg["start"])
                    .set_end(seg["end"]))
        subtitles.append(subtitle)

    final = CompositeVideoClip([video] + subtitles)
    final.write_videofile(
        output_video_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )

    final.close()
    video.close()
    return output_video_path
