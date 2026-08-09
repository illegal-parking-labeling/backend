# illegal-parking-labeling / backend

FastAPI + SQLAlchemy(SQLite) + Ultralytics YOLOv8n.
전체 프로젝트 설명은 [org 프로필](https://github.com/illegal-parking-labeling) 참고.

## 실행

```bash
python3.12 -m venv .venv && ./.venv/bin/pip install -r requirements.txt
./.venv/bin/uvicorn app.main:app --reload   # http://localhost:8000
```

첫 업로드 시 `yolov8n.pt`를 `storage/models/`에 자동 다운로드합니다. 파인튜닝한 가중치로 교체하려면 같은 경로에 덮어쓰면 됩니다.

## 구조

```
app/
  models/     Image, Prediction(AI 예측), Label(사람이 확정한 값), Labeler
  ml/         YOLO 추론
  api/        /images, /images/{id}/labels, /leaderboard, /stats/ai
```
