from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "carbon-footprint-service"
    version: str = "1.0.0"
    grid_factor_kg_kwh: float = Field(default=0.4, description="Factor de emisión de la red eléctrica (kg CO2/kWh)")
    weight_penalty_per_ton: float = 0.02
    admin_api_key: str = Field(default="", validation_alias="CFS_ADMIN_API_KEY")

    model_config = {"env_prefix": "CFS_"}


settings = Settings()