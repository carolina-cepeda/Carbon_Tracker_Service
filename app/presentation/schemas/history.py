from pydantic import BaseModel, Field
from typing import List, Optional

from app.domain.entities.calculation_history import CalculationHistory


class HistoryItemResponse(BaseModel):
    id: int
    vehicle_id: str
    vehicle_type: str
    distance_km: float
    weight_tons: float
    total_co2_kg: float
    breakdown: dict
    formula_used: str
    created_at: str

    @classmethod
    def from_entity(cls, entity: CalculationHistory) -> "HistoryItemResponse":
        return cls(**entity.to_dict())


class HistoryListResponse(BaseModel):
    items: List[HistoryItemResponse]
    total: int
    limit: int
    offset: int


class ExportReportRequest(BaseModel):
    file: str = Field(min_length=1)
    format: str = Field(default="pdf")


class ExportReportResponse(BaseModel):
    success: bool
    file_path: str
    message: str