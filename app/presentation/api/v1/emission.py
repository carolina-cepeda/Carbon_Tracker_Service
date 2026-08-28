from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.calculate_emission_request import CalculateEmissionRequest
from app.application.use_cases.calculate_emission import CalculateEmissionUseCase
from app.domain.enums.vehicle_type import VehicleType
from app.domain.interfaces.factor_catalog import FactorCatalog
from app.presentation.dependencies.container import get_calculate_use_case, get_factor_catalog
from app.presentation.schemas.emission import EmissionCalculateRequest, EmissionCalculateResponse
from app.presentation.schemas.factors import FactorItem, FactorsResponse

router = APIRouter(prefix="/v1/emissions", tags=["emissions"])


@router.post(
    "/calculate",
    response_model=EmissionCalculateResponse,
    status_code=status.HTTP_200_OK,
    summary="Calcular emisiones de CO2 de un viaje",
)
def calculate_emission(
    request: EmissionCalculateRequest,
    use_case: CalculateEmissionUseCase = Depends(get_calculate_use_case),
) -> EmissionCalculateResponse:
    try:
        dto_request = CalculateEmissionRequest(
            vehicle_id=request.vehicle_id,
            vehicle_type=request.vehicle_type,
            distance_km=request.distance_km,
            weight_tons=request.weight_tons,
            base_efficiency_km_l=request.base_efficiency_km_l,
            base_consumption_kwh_km=request.base_consumption_kwh_km,
            electric_usage_ratio=request.electric_usage_ratio,
        )
        result = use_case.execute(dto_request)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return EmissionCalculateResponse(**result.to_dict())


@router.get("/factors", response_model=FactorsResponse, summary="Obtener factores de emisión configurados")
def get_factors(catalog: FactorCatalog = Depends(get_factor_catalog)) -> FactorsResponse:
    diesel = catalog.get_factor(VehicleType.DIESEL)
    gasoline = catalog.get_factor(VehicleType.GASOLINE)
    grid = catalog.get_grid_factor()
    return FactorsResponse(
        diesel=FactorItem(value=diesel.value, unit=diesel.unit),
        gasoline=FactorItem(value=gasoline.value, unit=gasoline.unit),
        grid_electricity=FactorItem(value=grid.value, unit=grid.unit),
    )