from fastapi import Depends

from app.application.interfaces.emission_calculator_factory import EmissionCalculatorFactory
from app.application.use_cases.calculate_emission import CalculateEmissionUseCase
from app.application.use_cases.get_history import GetHistoryUseCase
from app.application.use_cases.export_report import ExportReportUseCase
from app.domain.interfaces.factor_catalog import FactorCatalog
from app.domain.interfaces.history_repository import HistoryRepository
from app.domain.services.auth.token_verifier import TokenVerifier, Pbkdf2TokenVerifier
from app.infrastructure.composition import build_calculate_use_case, build_calculator_factory
from app.infrastructure.config.settings import Settings, settings as app_settings
from app.infrastructure.factors.ipcc_factors import IpccFactorCatalog
from app.infrastructure.repositories.sqlite_history_repo import SqliteHistoryRepository
from app.infrastructure.services.report_generator import ReportGeneratorService


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


def get_history_repository(settings: Settings = Depends(get_settings)) -> HistoryRepository:
    return SqliteHistoryRepository(db_path="history.db")


def get_token_verifier() -> TokenVerifier:
    return Pbkdf2TokenVerifier()


def get_report_generator() -> ReportGeneratorService:
    return ReportGeneratorService(output_dir="reports")


def get_history_use_case(
    repo: HistoryRepository = Depends(get_history_repository),
) -> GetHistoryUseCase:
    return GetHistoryUseCase(repo)


def get_export_use_case(
    repo: HistoryRepository = Depends(get_history_repository),
    generator: ReportGeneratorService = Depends(get_report_generator),
    verifier: TokenVerifier = Depends(get_token_verifier),
) -> ExportReportUseCase:
    return ExportReportUseCase(repo, generator, verifier)