from fastapi import Depends

from app.application.interfaces.emission_calculator_factory import EmissionCalculatorFactory
from app.application.use_cases.calculate_emission import CalculateEmissionUseCase
from app.domain.interfaces.factor_catalog import FactorCatalog
from app.infrastructure.composition import build_calculate_use_case, build_calculator_factory
from app.infrastructure.config.settings import Settings, settings as app_settings
from app.infrastructure.factors.ipcc_factors import IpccFactorCatalog


def get_settings() -> Settings:
    return app_settings


def get_calculator_factory(settings: Settings = Depends(get_settings)) -> EmissionCalculatorFactory:
    return build_calculator_factory(settings)


def get_calculate_use_case(
    factory: EmissionCalculatorFactory = Depends(get_calculator_factory),
) -> CalculateEmissionUseCase:
    return CalculateEmissionUseCase(factory)


def get_factor_catalog(settings: Settings = Depends(get_settings)) -> FactorCatalog:
    return IpccFactorCatalog(grid_factor_kg_kwh=settings.grid_factor_kg_kwh)