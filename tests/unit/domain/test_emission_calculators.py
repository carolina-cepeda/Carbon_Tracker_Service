from app.domain.enums.vehicle_type import VehicleType
from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.distance import Distance
from app.domain.value_objects.weight import Weight

import pytest


def _vehicle(**overrides) -> Vehicle:
    data = dict(
        id="V1",
        type=VehicleType.DIESEL,
        base_efficiency_km_l=4.5,
        base_consumption_kwh_km=0.2,
    )
    data.update(overrides)
    return Vehicle(**data)


def test_diesel_no_load_emissions(combustion_calculator):
    vehicle = _vehicle()
    distance = Distance(100)
    weight = Weight(0)

    result = combustion_calculator.calculate(vehicle, distance, weight)

    liters = 100 / 4.5
    assert result.total_co2_kg == pytest.approx(liters * 2.68, rel=1e-9)
    assert result.formula_used.startswith("combustion")


def test_diesel_with_load_increases_emissions(combustion_calculator):
    vehicle = _vehicle()
    distance = Distance(100)
    weight = Weight(10)

    result = combustion_calculator.calculate(vehicle, distance, weight)

    liters = (100 / 4.5) * (1 + 10 * 0.02)
    assert result.total_co2_kg == pytest.approx(liters * 2.68, rel=1e-9)


def test_electric_no_load_emissions(electric_calculator):
    vehicle = _vehicle(type=VehicleType.ELECTRIC)
    distance = Distance(100)
    weight = Weight(0)

    result = electric_calculator.calculate(vehicle, distance, weight)

    assert result.total_co2_kg == pytest.approx(100 * 0.2 * 0.4, rel=1e-9)


def test_hybrid_is_weighted_sum(hybrid_calculator):
    vehicle = _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=0.4)
    distance = Distance(100)
    weight = Weight(0)

    result = hybrid_calculator.calculate(vehicle, distance, weight)

    fuel_part = (100 / 4.5) * 0.6 * 2.31
    grid_part = (100 * 0.2) * 0.4 * 0.4
    assert result.total_co2_kg == pytest.approx(fuel_part + grid_part, rel=1e-9)


def test_hybrid_fully_electric_has_no_fuel(hybrid_calculator):
    vehicle = _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=1.0)
    distance = Distance(100)
    weight = Weight(0)

    result = hybrid_calculator.calculate(vehicle, distance, weight)

    assert result.breakdown["fuel_consumed_liters"] == 0
    assert result.total_co2_kg > 0


def test_vehicle_rejects_invalid_ratio():
    with pytest.raises(ValueError):
        _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=1.5)