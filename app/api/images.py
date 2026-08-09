from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.ml.yolo_service import predict_vehicles
from app.models.enums import ImageStatus
from app.models.image import Image
from app.models.prediction import Prediction
from app.schemas.image import ImageOut
from app.services.storage import save_upload

router = APIRouter(prefix="/images", tags=["images"])


@router.post("", response_model=ImageOut)
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        stored_name, path, width, height = save_upload(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    image = Image(filename=stored_name, file_path=path, width=width, height=height, status=ImageStatus.PENDING)
    db.add(image)
    db.commit()
    db.refresh(image)

    detections = predict_vehicles(path)
    for det in detections:
        db.add(Prediction(image_id=image.id, **det))
    if detections:
        image.status = ImageStatus.PREDICTED
    db.commit()
    db.refresh(image)

    return image


@router.get("", response_model=list[ImageOut])
def list_images(status: ImageStatus | None = None, db: Session = Depends(get_db)):
    query = db.query(Image)
    if status:
        query = query.filter(Image.status == status)
    return query.order_by(Image.uploaded_at.desc()).all()


@router.get("/{image_id}", response_model=ImageOut)
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.get(Image, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다")
    return image
