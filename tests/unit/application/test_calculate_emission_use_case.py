"""Pruebas del caso de uso de cálculo.

Foco: que el cálculo en sí se comporte bien ante datos rebuscados:
distancias de 0, cargas negativas, vehículos sin nombre, o tipos que
no conocemos.
"""
import pytest

from app.application.dto.calculate_emission_request import CalculateEmissionRequest
from app.domain.enums.vehicle_type import VehicleType
from app.infrastructure.factories.calculator_registry import CalculatorRegistry


def _peticion(**cambios) -> CalculateEmissionRequest:
    base = dict(
        vehicle_id="TRK-001",
        vehicle_type=VehicleType.DIESEL,
        distance_km=100,
        weight_tons=0,
        base_efficiency_km_l=4.5,
        base_consumption_kwh_km=0.2,
        electric_usage_ratio=0.0,
    )
    base.update(cambios)
    return CalculateEmissionRequest(**base)


def test_peticion_diesel_calcula_correctamente(use_case):
    resultado = use_case.execute(_peticion())
    assert resultado.total_co2_kg == pytest.approx((100 / 4.5) * 2.68, rel=1e-9)
    assert resultado.vehicle_type == "diesel"


def test_distancia_cero_se_rechaza_antes_de_calcular(use_case):
    with pytest.raises(ValueError) as error:
        use_case.execute(_peticion(distance_km=0))
    assert "greater than zero" in str(error.value), (
        "El mensaje debería explicar que la distancia debe ser mayor que cero."
    )


def test_distancia_negativa_se_rechaza(use_case):
    with pytest.raises(ValueError):
        use_case.execute(_peticion(distance_km=-50))


def test_carga_negativa_se_rechaza(use_case):
    with pytest.raises(ValueError):
        use_case.execute(_peticion(weight_tons=-1))


def test_carga_cero_es_un_caso_valido(use_case):
    resultado = use_case.execute(_peticion(weight_tons=0))
    assert resultado.weight_tons == 0


def test_vehiculo_sin_nombre_se_rechaza(use_case):
    with pytest.raises(ValueError) as error:
        use_case.execute(_peticion(vehicle_id="   "))
    assert "empty" in str(error.value), (
        "El mensaje debería aclarar que el identificador del vehículo no puede "
        "estar vacío."
    )


def test_hibrido_con_ratio_invalido_se_rechaza(use_case):
    with pytest.raises(ValueError):
        use_case.execute(
            _peticion(vehicle_type=VehicleType.HYBRID, electric_usage_ratio=1.5)
        )


def test_eficiencia_cero_se_rechaza(use_case):
    with pytest.raises(ValueError) as error:
        use_case.execute(_peticion(base_efficiency_km_l=0))
    assert "greater than zero" in str(error.value), (
        "La eficiencia de combustible debe ser mayor que cero para poder calcular."
    )


def test_consumo_electrico_cero_se_rechaza(use_case):
    with pytest.raises(ValueError) as error:
        use_case.execute(_peticion(base_consumption_kwh_km=0))
    assert "greater than zero" in str(error.value), (
        "El consumo eléctrico en kWh/km debe ser mayor que cero para poder calcular."
    )


def test_tipo_de_vehiculo_no_soportado_explica_el_problema():
    fabrica = CalculatorRegistry({})
    with pytest.raises(ValueError) as error:
        fabrica.get_calculator(VehicleType.DIESEL)
    assert "Unsupported vehicle type" in str(error.value), (
        "El mensaje debería señalar que ese tipo de vehículo no está soportado."
    )


def test_fabrica_vacia_lista_ningun_tipo():
    fabrica = CalculatorRegistry({})
    assert fabrica.supported_types == []