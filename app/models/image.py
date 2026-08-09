from sqlalchemy import DateTime, Enum as SAEnum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.enums import ImageStatus


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ImageStatus] = mapped_column(SAEnum(ImageStatus), default=ImageStatus.PENDING, nullable=False)
    uploaded_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("Prediction", back_populates="image", cascade="all, delete-orphan")
    labels = relationship("Label", back_populates="image", cascade="all, delete-orphan")
