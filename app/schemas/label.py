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


class LabelUpdate(BaseModel):
    prediction_id: int | None = None
    x1: float | None = None
    y1: float | None = None
    x2: float | None = None
    y2: float | None = None
    vehicle_type: VehicleType | None = None
    parking_status: ParkingStatus | None = None
    lane_type: LaneType | None = None
    matched_ai: bool | None = None


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
