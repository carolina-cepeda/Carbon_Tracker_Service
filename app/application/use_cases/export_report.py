from app.application.dto.history_dto import ExportReportRequest, ExportReportResponse
from app.domain.interfaces.history_repository import HistoryRepository
from app.domain.services.auth.token_verifier import TokenVerifier


class ExportReportUseCase:
    def __init__(
        self, repository: HistoryRepository, report_generator, token_verifier: TokenVerifier
    ) -> None:
        self._repository = repository
        self._report_generator = report_generator
        self._token_verifier = token_verifier

    def execute(self, request: ExportReportRequest, admin_token: str) -> ExportReportResponse:
        if not self._token_verifier.verify_admin_token(admin_token):
            return ExportReportResponse(
                success=False,
                file_path="",
                message="Invalid admin token",
            )

        file_path = self._report_generator.generate_pdf(request.file)
        return ExportReportResponse(
            success=True,
            file_path=file_path,
            message="Report generated successfully",
        )