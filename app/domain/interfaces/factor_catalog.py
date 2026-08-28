from abc import ABC, abstractmethod

from app.domain.value_objects.emission_factor import EmissionFactor


class FactorCatalog(ABC):
    @abstractmethod
    def get_factor(self, fuel_type) -> EmissionFactor:
        ...

    @abstractmethod
    def get_grid_factor(self) -> EmissionFactor:
        ...