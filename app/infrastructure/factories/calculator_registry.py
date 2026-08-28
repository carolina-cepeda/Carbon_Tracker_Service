from app.application.interfaces.emission_calculator_factory import EmissionCalculatorFactory
from app.domain.enums.vehicle_type import VehicleType
from app.domain.interfaces.emission_calculator import EmissionCalculator


class CalculatorRegistry(EmissionCalculatorFactory):
    def __init__(self, calculators: dict[VehicleType, EmissionCalculator]) -> None:
        self._calculators = calculators

    def get_calculator(self, vehicle_type: VehicleType) -> EmissionCalculator:
        try:
            return self._calculators[vehicle_type]
        except KeyError as exc:
            raise ValueError(f"Unsupported vehicle type: {vehicle_type}") from exc

    @property
    def supported_types(self) -> list[str]:
        return [v.value for v in self._calculators]
