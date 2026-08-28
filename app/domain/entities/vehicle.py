from dataclasses import dataclass

from app.domain.enums.vehicle_type import VehicleType
from app.domain.value_objects.weight import Weight


@dataclass(frozen=True)
class Vehicle:
    id: str
    type: VehicleType
    base_efficiency_km_l: float
    base_consumption_kwh_km: float
    electric_usage_ratio: float = 0.0

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Vehicle id cannot be empty")
        if self.base_efficiency_km_l <= 0:
            raise ValueError("Base efficiency must be greater than zero")
        if self.base_consumption_kwh_km <= 0:
            raise ValueError("Base consumption must be greater than zero")
        if not 0.0 <= self.electric_usage_ratio <= 1.0:
            raise ValueError("Electric usage ratio must be between 0 and 1")