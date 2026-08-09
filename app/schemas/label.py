from pydantic import BaseModel, ConfigDict

from app.models.enums import LaneType, ParkingStatus, VehicleType


class LabelCreate(BaseModel):
    prediction_id: int | None = None
    labeler_name: str
    x1: float
    y1: float
    x2: float
    y2: float
    vehicle_type: VehicleType
    parking_status: ParkingStatus
    lane_type: LaneType
    matched_ai: bool = False


class LabelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_id: int
    prediction_id: int | None
    x1: float
    y1: float
    x2: float
    y2: float
    vehicle_type: VehicleType
    parking_status: ParkingStatus
    lane_type: LaneType
    matched_ai: bool
