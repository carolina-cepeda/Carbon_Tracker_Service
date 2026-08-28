from enum import Enum


class VehicleType(str, Enum):
    ELECTRIC = "electric"
    DIESEL = "diesel"
    GASOLINE = "gasoline"
    HYBRID = "hybrid"