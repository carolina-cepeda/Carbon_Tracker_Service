from abc import ABC, abstractmethod

from app.domain.enums.vehicle_type import VehicleType
from app.domain.interfaces.emission_calculator import EmissionCalculator


class EmissionCalculatorFactory(ABC):
    @abstractmethod
    def get_calculator(self, vehicle_type: VehicleType) -> EmissionCalculator:
        ...

    @property
    @abstractmethod
    def supported_types(self) -> list[str]:
        ...
