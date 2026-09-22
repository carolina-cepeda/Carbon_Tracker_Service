from app.application.dto.history_dto import HistoryListRequest, HistoryListResponse
from app.domain.entities.calculation_history import CalculationHistory
from app.domain.interfaces.history_repository import HistoryRepository


class GetHistoryUseCase:
    def __init__(self, repository: HistoryRepository) -> None:
        self._repository = repository

    def execute(self, request: HistoryListRequest) -> HistoryListResponse:
        if request.vehicle_id:
            items = self._repository.get_by_vehicle_id(request.vehicle_id)
        else:
            items = self._repository.get_all(request.limit, request.offset)

        return HistoryListResponse(
            items=items,
            total=len(items),
            limit=request.limit,
            offset=request.offset,
        )