from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.enums import ImageStatus
from app.models.image import Image
from app.models.label import Label
from app.models.labeler import Labeler
from app.models.prediction import Prediction
from app.schemas.label import LabelCreate, LabelOut, LabelUpdate

router = APIRouter(tags=["labels"])


def _get_label_or_404(image_id: int, label_id: int, db: Session) -> Label:
    label = db.query(Label).filter(Label.id == label_id, Label.image_id == image_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="라벨을 찾을 수 없습니다")
    return label


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


@router.patch("/images/{image_id}/labels/{label_id}", response_model=LabelOut)
def update_label(image_id: int, label_id: int, payload: LabelUpdate, db: Session = Depends(get_db)):
    label = _get_label_or_404(image_id, label_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(label, field, value)
    db.commit()
    db.refresh(label)
    return label


@router.delete("/images/{image_id}/labels/{label_id}", status_code=204)
def delete_label(image_id: int, label_id: int, db: Session = Depends(get_db)):
    label = _get_label_or_404(image_id, label_id, db)
    db.delete(label)
    db.flush()

    remaining = db.query(Label).filter(Label.image_id == image_id).count()
    if remaining == 0:
        image = db.get(Image, image_id)
        has_predictions = db.query(Prediction).filter(Prediction.image_id == image_id).first() is not None
        image.status = ImageStatus.PREDICTED if has_predictions else ImageStatus.PENDING
    db.commit()
    return Response(status_code=204)
