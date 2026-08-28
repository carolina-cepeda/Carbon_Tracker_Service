from app.application.dto.calculate_emission_request import CalculateEmissionRequest
from app.application.dto.calculate_emission_response import CalculateEmissionResponse
from app.application.interfaces.emission_calculator_factory import EmissionCalculatorFactory
from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.distance import Distance
from app.domain.value_objects.weight import Weight


class CalculateEmissionUseCase:
    def __init__(self, calculator_factory: EmissionCalculatorFactory) -> None:
        self._calculator_factory = calculator_factory

    def execute(self, request: CalculateEmissionRequest) -> CalculateEmissionResponse:
        request.validate()

        vehicle = Vehicle(
            id=request.vehicle_id,
            type=request.vehicle_type,
            base_efficiency_km_l=request.base_efficiency_km_l,
            base_consumption_kwh_km=request.base_consumption_kwh_km,
            electric_usage_ratio=request.electric_usage_ratio,
        )
        calculator = self._calculator_factory.get_calculator(request.vehicle_type)

        result = calculator.calculate(
            vehicle=vehicle,
            distance=Distance(request.distance_km),
            weight=Weight(request.weight_tons),
        )
        return CalculateEmissionResponse(
            vehicle_id=request.vehicle_id,
            vehicle_type=request.vehicle_type.value,
            distance_km=result.distance.value,
            weight_tons=result.weight.value,
            total_co2_kg=result.total_co2_kg,
            breakdown=result.breakdown,
            formula_used=result.formula_used,
        )