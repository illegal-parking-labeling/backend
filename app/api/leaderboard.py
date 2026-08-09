from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.label import Label
from app.models.labeler import Labeler
from app.models.prediction import Prediction
from app.schemas.leaderboard import AiStats, LeaderboardEntry

router = APIRouter(tags=["leaderboard"])


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def get_leaderboard(db: Session = Depends(get_db)):
    rows = (
        db.query(Labeler.name, func.count(Label.id).label("label_count"))
        .join(Label, Label.labeler_id == Labeler.id)
        .group_by(Labeler.id)
        .order_by(func.count(Label.id).desc())
        .all()
    )
    return [LeaderboardEntry(labeler_name=name, label_count=count) for name, count in rows]


@router.get("/stats/ai", response_model=AiStats)
def get_ai_stats(db: Session = Depends(get_db)):
    """사람이 AI의 예측(bbox+차종)을 수정 없이 그대로 승인한 비율 = AI 예측 신뢰도 지표."""
    total_predictions = db.query(func.count(Prediction.id)).scalar() or 0
    matched_labels = db.query(func.count(Label.id)).filter(Label.matched_ai.is_(True)).scalar() or 0
    rate = (matched_labels / total_predictions) if total_predictions else 0.0
    return AiStats(total_predictions=total_predictions, matched_labels=matched_labels, acceptance_rate=rate)
