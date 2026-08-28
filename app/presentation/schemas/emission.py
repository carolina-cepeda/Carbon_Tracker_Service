from pydantic import BaseModel, Field, model_validator

from app.domain.enums.vehicle_type import VehicleType


class EmissionCalculateRequest(BaseModel):
    vehicle_id: str = Field(min_length=1)
    vehicle_type: VehicleType
    distance_km: float = Field(gt=0)
    weight_tons: float = Field(ge=0)
    base_efficiency_km_l: float = Field(gt=0)
    base_consumption_kwh_km: float = Field(gt=0)
    electric_usage_ratio: float = Field(default=0.0, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def validate_hybrid_ratio(self) -> "EmissionCalculateRequest":
        if self.vehicle_type == VehicleType.HYBRID and self.electric_usage_ratio <= 0:
            raise ValueError("electric_usage_ratio must be > 0 for hybrid vehicles")
        return self


class BreakdownItem(BaseModel):
    value: float


class EmissionCalculateResponse(BaseModel):
    vehicle_id: str
    vehicle_type: str
    distance_km: float
    weight_tons: float
    total_co2_kg: float
    breakdown: dict[str, float]
    formula_used: str