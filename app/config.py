import os
from pathlib import Path

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    BASE_DIR = Path(__file__).resolve().parent.parent
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'app.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False