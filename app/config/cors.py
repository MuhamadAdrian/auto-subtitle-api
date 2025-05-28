# app/config/cors.py

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.config.config import get_cors_origins

def add_cors(app: FastAPI):
    origins = get_cors_origins()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
