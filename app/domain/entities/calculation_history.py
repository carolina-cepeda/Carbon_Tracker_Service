from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CalculationHistory:
    id: int
    vehicle_id: str
    vehicle_type: str
    distance_km: float
    weight_tons: float
    total_co2_kg: float
    breakdown: dict
    formula_used: str
    created_at: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "vehicle_id": self.vehicle_id,
            "vehicle_type": self.vehicle_type,
            "distance_km": self.distance_km,
            "weight_tons": self.weight_tons,
            "total_co2_kg": round(self.total_co2_kg, 3),
            "breakdown": self.breakdown,
            "formula_used": self.formula_used,
            "created_at": self.created_at.isoformat(),
        }