from abc import ABC, abstractmethod

from app.domain.entities.emission_calculation import EmissionCalculation
from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.distance import Distance
from app.domain.value_objects.weight import Weight


class EmissionCalculator(ABC):
    @abstractmethod
    def calculate(self, vehicle: Vehicle, distance: Distance, weight: Weight) -> EmissionCalculation:
        ...