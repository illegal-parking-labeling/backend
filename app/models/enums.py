import enum


class ImageStatus(str, enum.Enum):
    PENDING = "pending"
    PREDICTED = "predicted"
    LABELED = "labeled"


class VehicleType(str, enum.Enum):
    CAR = "car"
    TRUCK = "truck"
    BUS = "bus"
    MOTORCYCLE = "motorcycle"


class ParkingStatus(str, enum.Enum):
    NORMAL = "normal"
    ILLEGAL = "illegal"
    MOVING = "moving"


class LaneType(str, enum.Enum):
    SIDEWALK = "sidewalk"
    CROSSWALK = "crosswalk"
    BUS_ONLY = "bus_only"
    NONE = "none"
