from dataclasses import dataclass

from app.domain.entities.emission_calculation import EmissionCalculation
from app.domain.value_objects.emission_factor import EmissionFactor


@dataclass
class ElectricEmissionCalculator:
    grid_factor: EmissionFactor
    weight_adjustment_factor: callable

    def calculate(self, vehicle, distance, weight) -> EmissionCalculation:
        adjusted_consumption = vehicle.base_consumption_kwh_km * self.weight_adjustment_factor(weight.value)
        energy_consumed_kwh = distance.value * adjusted_consumption
        co2_kg = energy_consumed_kwh * self.grid_factor.value
        breakdown = {
            "energy_consumed_kwh": round(energy_consumed_kwh, 3),
            "emissions_kg": round(co2_kg, 3),
        }
        return EmissionCalculation(
            distance=distance,
            weight=weight,
            total_co2_kg=co2_kg,
            breakdown=breakdown,
            formula_used="electric: CO2 = (distance * kwh_per_km) * weight_factor * grid_factor",
        )