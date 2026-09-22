from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.infrastructure.config.settings import settings
from app.presentation.api.v1.emission import router as emission_router
from app.presentation.api.v1.health import router as health_router
from app.presentation.api.v1.history import router as history_router

app = FastAPI(title=settings.app_name, version=settings.version)

app.include_router(health_router)
app.include_router(emission_router)
app.include_router(history_router)


@app.exception_handler(ValueError)
async def value_error_handler(_request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request: the provided data does not meet business rules."},
    )


@app.exception_handler(Exception)
async def unhandled_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})