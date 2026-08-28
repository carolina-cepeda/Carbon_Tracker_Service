from dataclasses import dataclass

from app.domain.enums.vehicle_type import VehicleType


@dataclass(frozen=True)
class EmissionFactor:
    fuel_type: VehicleType
    value: float
    unit: str

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError("Emission factor must be greater than zero")