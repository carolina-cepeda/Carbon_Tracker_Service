"""Pruebas del factor de emisión.

Un factor de emisión indica cuánto CO2 se produce por cada unidad quemada
o consumida. Debe ser siempre positivo.
"""
import pytest

from app.domain.enums.vehicle_type import VehicleType
from app.domain.value_objects.emission_factor import EmissionFactor


def test_factor_valido_se_crea_correctamente():
    factor = EmissionFactor(fuel_type=VehicleType.DIESEL, value=2.68, unit="kg CO2/litro")
    assert factor.value == 2.68
    assert factor.unit == "kg CO2/litro"


def test_factor_cero_o_negativo_es_rechazado():
    with pytest.raises(ValueError):
        EmissionFactor(fuel_type=VehicleType.DIESEL, value=0, unit="kg/l")
    with pytest.raises(ValueError):
        EmissionFactor(fuel_type=VehicleType.DIESEL, value=-2.5, unit="kg/l")


def test_factor_con_fraccion_muy_pequena_es_valido():
    factor = EmissionFactor(fuel_type=VehicleType.ELECTRIC, value=0.001, unit="kg/kWh")
    assert factor.value == 0.001