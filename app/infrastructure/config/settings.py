from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "carbon-footprint-service"
    version: str = "1.0.0"
    grid_factor_kg_kwh: float = Field(default=0.4, description="Factor de emisión de la red eléctrica (kg CO2/kWh)")
    weight_penalty_per_ton: float = 0.02

    model_config = {"env_prefix": "CFS_"}


settings = Settings()