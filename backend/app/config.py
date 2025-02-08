# backend/app/config.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
STORAGE = BASE_DIR / "storage"
PDF_DIR = STORAGE / "evidence_pdfs"
VIDEO_DIR = STORAGE / "evidence_videos"

# Create directories if they don't exist
PDF_DIR.mkdir(parents=True, exist_ok=True)
VIDEO_DIR.mkdir(parents=True, exist_ok=True)