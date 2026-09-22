from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.calculation_history import CalculationHistory


class HistoryRepository(ABC):
    @abstractmethod
    def save(self, history: CalculationHistory) -> None:
        ...

    @abstractmethod
    def get_by_vehicle_id(self, vehicle_id: str) -> List[CalculationHistory]:
        ...

    @abstractmethod
    def get_all(self, limit: int = 100, offset: int = 0) -> List[CalculationHistory]:
        ...

    @abstractmethod
    def get_by_id(self, history_id: int) -> Optional[CalculationHistory]:
        ...