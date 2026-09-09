"""라벨 생성/수정/삭제 self-check. pytest 없이도 `python backend/tests/test_labels.py`로 실행 가능."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.labels import create_label, delete_label, list_labels, update_label
from app.core.database import Base
from app.models.enums import ImageStatus, LaneType, ParkingStatus, VehicleType
from app.models.image import Image
from app.schemas.label import LabelCreate, LabelUpdate


def make_session():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def demo():
    db = make_session()
    image = Image(filename="a.jpg", file_path="/tmp/a.jpg", width=100, height=100, status=ImageStatus.PENDING)
    db.add(image)
    db.commit()
    db.refresh(image)

    payload = LabelCreate(
        labeler_name="tester",
        x1=0, y1=0, x2=10, y2=10,
        vehicle_type=VehicleType.CAR,
        parking_status=ParkingStatus.ILLEGAL,
        lane_type=LaneType.CROSSWALK,
    )
    label = create_label(image.id, payload, db)
    assert image.status == ImageStatus.LABELED

    updated = update_label(image.id, label.id, LabelUpdate(parking_status=ParkingStatus.NORMAL), db)
    assert updated.parking_status == ParkingStatus.NORMAL
    assert updated.x1 == 0  # 지정하지 않은 필드는 그대로

    delete_label(image.id, label.id, db)
    assert list_labels(image.id, db) == []
    db.refresh(image)
    assert image.status == ImageStatus.PENDING  # 라벨이 없어지면 예측도 없으니 PENDING으로 복귀

    print("ok")


if __name__ == "__main__":
    demo()
