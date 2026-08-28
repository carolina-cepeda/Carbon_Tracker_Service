from dataclasses import dataclass

from app.domain.enums.vehicle_type import VehicleType


@dataclass(frozen=True)
class CalculateEmissionRequest:
    vehicle_id: str
    vehicle_type: VehicleType
    distance_km: float
    weight_tons: float
    base_efficiency_km_l: float
    base_consumption_kwh_km: float
    electric_usage_ratio: float = 0.0

    def validate(self) -> None:
        if not self.vehicle_id.strip():
            raise ValueError("vehicle_id cannot be empty")
        if self.distance_km <= 0:
            raise ValueError("distance_km must be greater than zero")
        if self.weight_tons < 0:
            raise ValueError("weight_tons cannot be negative")
        if self.base_efficiency_km_l <= 0:
            raise ValueError("base_efficiency_km_l must be greater than zero")
        if self.base_consumption_kwh_km <= 0:
            raise ValueError("base_consumption_kwh_km must be greater than zero")
        if not 0.0 <= self.electric_usage_ratio <= 1.0:
            raise ValueError("electric_usage_ratio must be between 0 and 1")