from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.application.dto.history_dto import HistoryListRequest, ExportReportRequest
from app.application.use_cases.get_history import GetHistoryUseCase
from app.application.use_cases.export_report import ExportReportUseCase
from app.domain.interfaces.history_repository import HistoryRepository
from app.domain.services.auth.token_verifier import TokenVerifier
from app.infrastructure.services.report_generator import ReportGeneratorService
from app.presentation.dependencies.container import get_history_use_case, get_export_use_case
from app.presentation.schemas.history import (
    HistoryListResponse,
    HistoryItemResponse,
    ExportReportRequest as ExportReportRequestSchema,
    ExportReportResponse,
)

router = APIRouter(prefix="/v1/history", tags=["history"])


@router.get(
    "",
    response_model=HistoryListResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener historial de cálculos",
)
def get_history(
    vehicle_id: str | None = Query(None, description="Filtrar por ID de vehículo"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    use_case: GetHistoryUseCase = Depends(get_history_use_case),
) -> HistoryListResponse:
    request = HistoryListRequest(vehicle_id=vehicle_id, limit=limit, offset=offset)
    result = use_case.execute(request)
    return HistoryListResponse(
        items=[HistoryItemResponse.from_entity(item) for item in result.items],
        total=result.total,
        limit=result.limit,
        offset=result.offset,
    )


@router.get(
    "/export",
    response_model=ExportReportResponse,
    status_code=status.HTTP_200_OK,
    summary="Exportar reporte de emisiones",
)
def export_report(
    file: str = Query(..., description="Nombre del archivo a exportar"),
    format: str = Query("pdf", description="Formato de exportación"),
    admin_token: str = Query(..., description="Token de administrador"),
    use_case: ExportReportUseCase = Depends(get_export_use_case),
) -> ExportReportResponse:
    request = ExportReportRequest(file=file, format=format)
    result = use_case.execute(request, admin_token)
    return ExportReportResponse(**result.__dict__)


@router.get(
    "/download/{filepath:path}",
    status_code=status.HTTP_200_OK,
    summary="Descargar archivo exportado",
)
def download_export(filepath: str) -> dict:
    base_dir = "reports"
    full_path = f"{base_dir}/{filepath}"
    try:
        with open(full_path, "r") as f:
            content = f.read()
        return {"content": content, "file": filepath}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")