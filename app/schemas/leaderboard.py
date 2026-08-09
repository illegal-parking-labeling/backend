from pydantic import BaseModel


class LeaderboardEntry(BaseModel):
    labeler_name: str
    label_count: int


class AiStats(BaseModel):
    total_predictions: int
    matched_labels: int
    acceptance_rate: float
