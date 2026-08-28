from dataclasses import dataclass

from app.domain.entities.emission_calculation import EmissionCalculation
from app.domain.value_objects.emission_factor import EmissionFactor


@dataclass
class HybridEmissionCalculator:
    fuel_factor: EmissionFactor
    grid_factor: EmissionFactor
    weight_adjustment_factor: callable

    def calculate(self, vehicle, distance, weight) -> EmissionCalculation:
        ratio = vehicle.electric_usage_ratio
        combustion_ratio = 1 - ratio

        base_consumption_l_km = 1 / vehicle.base_efficiency_km_l
        adjusted_consumption = base_consumption_l_km * self.weight_adjustment_factor(weight.value)
        fuel_used_liters = distance.value * adjusted_consumption * combustion_ratio
        fuel_emissions_kg = fuel_used_liters * self.fuel_factor.value

        adjusted_kwh = vehicle.base_consumption_kwh_km * self.weight_adjustment_factor(weight.value)
        energy_consumed_kwh = distance.value * adjusted_kwh * ratio
        grid_emissions_kg = energy_consumed_kwh * self.grid_factor.value

        total_co2_kg = fuel_emissions_kg + grid_emissions_kg
        breakdown = {
            "fuel_consumed_liters": round(fuel_used_liters, 3),
            "fuel_emissions_kg": round(fuel_emissions_kg, 3),
            "energy_consumed_kwh": round(energy_consumed_kwh, 3),
            "grid_emissions_kg": round(grid_emissions_kg, 3),
        }
        return EmissionCalculation(
            distance=distance,
            weight=weight,
            total_co2_kg=total_co2_kg,
            breakdown=breakdown,
            formula_used="hybrid: CO2 = electric_part(grid) + combustion_part(fuel)",
        )