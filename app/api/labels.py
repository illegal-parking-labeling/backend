from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import ImageStatus
from app.models.image import Image
from app.models.label import Label
from app.models.labeler import Labeler
from app.schemas.label import LabelCreate, LabelOut

router = APIRouter(tags=["labels"])


@router.post("/images/{image_id}/labels", response_model=LabelOut)
def create_label(image_id: int, payload: LabelCreate, db: Session = Depends(get_db)):
    image = db.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다")

    labeler = db.query(Labeler).filter(Labeler.name == payload.labeler_name).first()
    if not labeler:
        labeler = Labeler(name=payload.labeler_name)
        db.add(labeler)
        db.flush()

    label = Label(
        image_id=image_id,
        prediction_id=payload.prediction_id,
        labeler_id=labeler.id,
        x1=payload.x1,
        y1=payload.y1,
        x2=payload.x2,
        y2=payload.y2,
        vehicle_type=payload.vehicle_type,
        parking_status=payload.parking_status,
        lane_type=payload.lane_type,
        matched_ai=payload.matched_ai,
    )
    db.add(label)
    image.status = ImageStatus.LABELED
    db.commit()
    db.refresh(label)
    return label


@router.get("/images/{image_id}/labels", response_model=list[LabelOut])
def list_labels(image_id: int, db: Session = Depends(get_db)):
    return db.query(Label).filter(Label.image_id == image_id).all()
