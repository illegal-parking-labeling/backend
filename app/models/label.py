from sqlalchemy import Boolean, DateTime, Enum as SAEnum, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import LaneType, ParkingStatus, VehicleType


class Label(Base):
    """사람이 최종 확정한 라벨. AI 예측(prediction)을 그대로 승인했거나 수정한 결과."""

    __tablename__ = "labels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("images.id"), nullable=False)
    prediction_id: Mapped[int | None] = mapped_column(ForeignKey("predictions.id"), nullable=True)
    labeler_id: Mapped[int] = mapped_column(ForeignKey("labelers.id"), nullable=False)

    x1: Mapped[float] = mapped_column(Float, nullable=False)
    y1: Mapped[float] = mapped_column(Float, nullable=False)
    x2: Mapped[float] = mapped_column(Float, nullable=False)
    y2: Mapped[float] = mapped_column(Float, nullable=False)

    vehicle_type: Mapped[VehicleType] = mapped_column(SAEnum(VehicleType), nullable=False)
    parking_status: Mapped[ParkingStatus] = mapped_column(SAEnum(ParkingStatus), nullable=False)
    lane_type: Mapped[LaneType] = mapped_column(SAEnum(LaneType), nullable=False)

    matched_ai: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    image = relationship("Image", back_populates="labels")
    labeler = relationship("Labeler", back_populates="labels")
