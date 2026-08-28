from pydantic import BaseModel, Field


class FactorItem(BaseModel):
    value: float
    unit: str


class FactorsResponse(BaseModel):
    diesel: FactorItem
    gasoline: FactorItem
    grid_electricity: FactorItem