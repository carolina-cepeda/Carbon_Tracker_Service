import pytest

from app.domain.enums.vehicle_type import VehicleType
from app.domain.interfaces.factor_catalog import FactorCatalog
from app.domain.services.emission.combustion_calculator import CombustionEmissionCalculator
from app.domain.services.emission.electric_calculator import ElectricEmissionCalculator
from app.domain.services.emission.hybrid_calculator import HybridEmissionCalculator
from app.domain.services.emission.weight_policy import weight_adjustment_factor
from app.domain.value_objects.emission_factor import EmissionFactor
from app.infrastructure.composition import build_calculate_use_case
from app.infrastructure.config.settings import Settings
from app.infrastructure.factors.ipcc_factors import IpccFactorCatalog

VEHICLE_DIESEL = {
    "vehicle_id": "TRK-001",
    "vehicle_type": VehicleType.DIESEL,
    "base_efficiency_km_l": 4.5,
    "base_consumption_kwh_km": 1.0,
}

VEHICLE_ELECTRIC = {
    "vehicle_id": "EV-001",
    "vehicle_type": VehicleType.ELECTRIC,
    "base_efficiency_km_l": 10.0,
    "base_consumption_kwh_km": 0.2,
}

VEHICLE_HYBRID = {
    "vehicle_id": "HYB-001",
    "vehicle_type": VehicleType.HYBRID,
    "base_efficiency_km_l": 5.0,
    "base_consumption_kwh_km": 0.15,
    "electric_usage_ratio": 0.4,
}


@pytest.fixture
def settings() -> Settings:
    return Settings(grid_factor_kg_kwh=0.4, weight_penalty_per_ton=0.02)


@pytest.fixture
def catalog(settings) -> FactorCatalog:
    return IpccFactorCatalog(grid_factor_kg_kwh=settings.grid_factor_kg_kwh)


@pytest.fixture
def combustion_calculator(catalog) -> CombustionEmissionCalculator:
    return CombustionEmissionCalculator(
        fuel_factor=catalog.get_factor(VehicleType.DIESEL),
        weight_adjustment_factor=weight_adjustment_factor,
    )


@pytest.fixture
def electric_calculator(catalog) -> ElectricEmissionCalculator:
    return ElectricEmissionCalculator(
        grid_factor=catalog.get_grid_factor(),
        weight_adjustment_factor=weight_adjustment_factor,
    )


@pytest.fixture
def hybrid_calculator(catalog) -> HybridEmissionCalculator:
    return HybridEmissionCalculator(
        fuel_factor=catalog.get_factor(VehicleType.GASOLINE),
        grid_factor=catalog.get_grid_factor(),
        weight_adjustment_factor=weight_adjustment_factor,
    )


@pytest.fixture
def use_case(settings):
    return build_calculate_use_case(settings)


@pytest.fixture
def generic_factor() -> EmissionFactor:
    return EmissionFactor(fuel_type=VehicleType.ELECTRIC, value=0.5, unit="kg/kWh")