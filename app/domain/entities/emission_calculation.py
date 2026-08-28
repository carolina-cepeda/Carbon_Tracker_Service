from dataclasses import dataclass

from app.domain.value_objects.distance import Distance
from app.domain.value_objects.weight import Weight


@dataclass(frozen=True)
class EmissionCalculation:
    distance: Distance
    weight: Weight
    total_co2_kg: float
    breakdown: dict[str, float]
    formula_used: str

    def to_dict(self) -> dict:
        return {
            "distance_km": self.distance.value,
            "weight_tons": self.weight.value,
            "total_co2_kg": round(self.total_co2_kg, 3),
            "breakdown": self.breakdown,
            "formula_used": self.formula_used,
        }