from functools import lru_cache

from ultralytics import YOLO

from app.core.config import settings

# COCO 클래스 중 이 프로젝트에서 다루는 차종만 남기고 매핑한다.
VEHICLE_CLASS_MAP = {
    "car": "car",
    "truck": "truck",
    "bus": "bus",
    "motorcycle": "motorcycle",
}


@lru_cache(maxsize=1)
def get_model() -> YOLO:
    # 지정한 경로에 가중치가 없으면 ultralytics가 최초 1회 해당 경로로 자동 다운로드한다.
    return YOLO(str(settings.yolo_model_path))


def predict_vehicles(image_path: str, confidence: float | None = None) -> list[dict]:
    model = get_model()
    conf = confidence if confidence is not None else settings.yolo_confidence_threshold
    results = model.predict(source=image_path, conf=conf, verbose=False)

    detections: list[dict] = []
    for result in results:
        names = result.names
        for box in result.boxes:
            raw_class = names[int(box.cls[0])]
            if raw_class not in VEHICLE_CLASS_MAP:
                continue
            x1, y1, x2, y2 = (float(v) for v in box.xyxy[0])
            detections.append(
                {
                    "class_name": VEHICLE_CLASS_MAP[raw_class],
                    "confidence": float(box.conf[0]),
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                }
            )
    return detections
