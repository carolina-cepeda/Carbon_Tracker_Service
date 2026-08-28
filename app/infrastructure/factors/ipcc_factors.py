from app.domain.enums.vehicle_type import VehicleType
from app.domain.interfaces.factor_catalog import FactorCatalog
from app.domain.value_objects.emission_factor import EmissionFactor


class IpccFactorCatalog(FactorCatalog):
    """Factores de emisión IPCC (kg CO2e por unidad de consumo)."""

    _DIESEL = EmissionFactor(fuel_type=VehicleType.DIESEL, value=2.68, unit="kg CO2/litro")
    _GASOLINE = EmissionFactor(fuel_type=VehicleType.GASOLINE, value=2.31, unit="kg CO2/litro")

    def __init__(self, grid_factor_kg_kwh: float) -> None:
        self._grid = EmissionFactor(fuel_type=VehicleType.ELECTRIC, value=grid_factor_kg_kwh, unit="kg CO2/kWh")

    def get_factor(self, fuel_type) -> EmissionFactor:
        catalog = {
            VehicleType.DIESEL: self._DIESEL,
            VehicleType.GASOLINE: self._GASOLINE,
            VehicleType.ELECTRIC: self._grid,
        }
        try:
            return catalog[fuel_type]
        except KeyError as exc:
            raise ValueError(f"Unknown fuel type: {fuel_type}") from exc

    def get_grid_factor(self) -> EmissionFactor:
        return self._grid