from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    database_url: str = f"sqlite:///{BASE_DIR / 'storage' / 'app.db'}"
    upload_dir: Path = BASE_DIR / "storage" / "uploads"
    yolo_model_path: Path = BASE_DIR / "storage" / "models" / "yolov8n.pt"
    yolo_confidence_threshold: float = 0.25
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
settings.upload_dir.mkdir(parents=True, exist_ok=True)
settings.yolo_model_path.parent.mkdir(parents=True, exist_ok=True)
