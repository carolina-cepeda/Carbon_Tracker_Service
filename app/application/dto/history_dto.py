from dataclasses import dataclass
from typing import List, Optional

from app.domain.entities.calculation_history import CalculationHistory


@dataclass(frozen=True)
class HistoryListRequest:
    vehicle_id: Optional[str] = None
    limit: int = 100
    offset: int = 0


@dataclass(frozen=True)
class HistoryListResponse:
    items: List[CalculationHistory]
    total: int
    limit: int
    offset: int


@dataclass(frozen=True)
class ExportReportRequest:
    file: str
    format: str = "pdf"


@dataclass(frozen=True)
class ExportReportResponse:
    success: bool
    file_path: str
    message: str