from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api import images, labels, leaderboard
from app.core.config import settings
from app.core.database import Base, engine
from app.models import Image, Label, Labeler, Prediction  # noqa: F401  (테이블 등록을 위해 import)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Illegal Parking Labeling API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(settings.upload_dir)), name="uploads")

app.include_router(images.router)
app.include_router(labels.router)
app.include_router(leaderboard.router)


@app.get("/health")
def health():
    return {"status": "ok"}
