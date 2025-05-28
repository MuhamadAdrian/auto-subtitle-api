from dotenv import load_dotenv
import os

load_dotenv()

def get_cors_origins():
    raw = os.getenv("CORS_ORIGINS", "")
    # Split by comma and strip whitespace
    return [origin.strip() for origin in raw.split(",") if origin.strip()]
