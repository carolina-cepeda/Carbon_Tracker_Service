from app.application.interfaces.emission_calculator_factory import EmissionCalculatorFactory
from app.application.use_cases.calculate_emission import CalculateEmissionUseCase
from app.domain.enums.vehicle_type import VehicleType
from app.domain.services.emission.combustion_calculator import CombustionEmissionCalculator
from app.domain.services.emission.electric_calculator import ElectricEmissionCalculator
from app.domain.services.emission.hybrid_calculator import HybridEmissionCalculator
from app.domain.services.emission.weight_policy import weight_adjustment_factor
from app.infrastructure.config.settings import Settings
from app.infrastructure.factories.calculator_registry import CalculatorRegistry
from app.infrastructure.factors.ipcc_factors import IpccFactorCatalog


def build_calculator_factory(settings: Settings) -> EmissionCalculatorFactory:
    catalog = IpccFactorCatalog(grid_factor_kg_kwh=settings.grid_factor_kg_kwh)

    diesel = CombustionEmissionCalculator(
        fuel_factor=catalog.get_factor(VehicleType.DIESEL),
        weight_adjustment_factor=weight_adjustment_factor,
    )
    gasoline = CombustionEmissionCalculator(
        fuel_factor=catalog.get_factor(VehicleType.GASOLINE),
        weight_adjustment_factor=weight_adjustment_factor,
    )
    electric = ElectricEmissionCalculator(
        grid_factor=catalog.get_grid_factor(),
        weight_adjustment_factor=weight_adjustment_factor,
    )
    hybrid = HybridEmissionCalculator(
        fuel_factor=catalog.get_factor(VehicleType.GASOLINE),
        grid_factor=catalog.get_grid_factor(),
        weight_adjustment_factor=weight_adjustment_factor,
    )
    return CalculatorRegistry(
        {
            VehicleType.DIESEL: diesel,
            VehicleType.GASOLINE: gasoline,
            VehicleType.ELECTRIC: electric,
            VehicleType.HYBRID: hybrid,
        }
    )


def build_calculate_use_case(settings: Settings) -> CalculateEmissionUseCase:
    return CalculateEmissionUseCase(build_calculator_factory(settings))