from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import ImageStatus


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    class_name: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float


class ImageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    width: int
    height: int
    status: ImageStatus
    uploaded_at: datetime
    predictions: list[PredictionOut] = []
