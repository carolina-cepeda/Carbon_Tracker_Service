from dataclasses import dataclass


@dataclass(frozen=True)
class CalculateEmissionResponse:
    vehicle_id: str
    vehicle_type: str
    distance_km: float
    weight_tons: float
    total_co2_kg: float
    breakdown: dict
    formula_used: str

    def to_dict(self) -> dict:
        return {
            "vehicle_id": self.vehicle_id,
            "vehicle_type": self.vehicle_type,
            "distance_km": round(self.distance_km, 3),
            "weight_tons": round(self.weight_tons, 3),
            "total_co2_kg": round(self.total_co2_kg, 3),
            "breakdown": self.breakdown,
            "formula_used": self.formula_used,
        }