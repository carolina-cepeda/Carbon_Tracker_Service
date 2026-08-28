from dataclasses import dataclass

from app.domain.entities.emission_calculation import EmissionCalculation
from app.domain.value_objects.emission_factor import EmissionFactor


@dataclass
class CombustionEmissionCalculator:
    fuel_factor: EmissionFactor
    weight_adjustment_factor: callable

    def calculate(self, vehicle, distance, weight) -> EmissionCalculation:
        base_consumption_l_km = 1 / vehicle.base_efficiency_km_l
        adjusted_consumption = base_consumption_l_km * self.weight_adjustment_factor(weight.value)
        fuel_used_liters = distance.value * adjusted_consumption
        co2_kg = fuel_used_liters * self.fuel_factor.value
        breakdown = {
            "fuel_consumed_liters": round(fuel_used_liters, 3),
            "emissions_kg": round(co2_kg, 3),
        }
        return EmissionCalculation(
            distance=distance,
            weight=weight,
            total_co2_kg=co2_kg,
            breakdown=breakdown,
            formula_used="combustion: CO2 = (distance * 1/eff) * weight_factor * fuel_factor",
        )