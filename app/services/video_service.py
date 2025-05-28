from app.video_generator import generate_video_with_subtitles

def generate_video_from_captions(video_file_name: str, corrected_captions: str):
    video_path = f"app/uploads/{video_file_name}"
    if not video_path.endswith('.mp4'):
        raise ValueError("Invalid video file format. Only .mp4 files are supported.")
    return generate_video_with_subtitles(video_path, corrected_captions)
