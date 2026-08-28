"""Pruebas de la entidad Vehículo.

Foco: asegurar que no se pueda crear un vehículo con datos sin sentido,
como identificadores vacíos o eficiencias de cero.
"""
import pytest

from app.domain.enums.vehicle_type import VehicleType
from app.domain.entities.vehicle import Vehicle


def _vehicle(**cambios) -> Vehicle:
    """Crea un vehículo diésel válido y aplica cambios para el test."""
    base = dict(
        id="TRK-001",
        type=VehicleType.DIESEL,
        base_efficiency_km_l=4.5,
        base_consumption_kwh_km=0.2,
    )
    base.update(cambios)
    return Vehicle(**base)


def test_vehiculo_valido_se_crea_sin_problemas():
    vehiculo = _vehicle()
    assert vehiculo.id == "TRK-001", (
        "El vehículo válido debería conservar su identificador tal como se envió, "
        "pero se perdió en la creación."
    )


def test_identificador_vacio_es_rechazado():
    with pytest.raises(ValueError):
        _vehicle(id="")
    with pytest.raises(ValueError):
        _vehicle(id="   ")


def test_identificador_de_solo_espacios_es_rechazado():
    with pytest.raises(ValueError):
        _vehicle(id="   ")


def test_eficiencia_de_combustible_cero_es_rechazada():
    with pytest.raises(ValueError):
        _vehicle(base_efficiency_km_l=0)
    with pytest.raises(ValueError):
        _vehicle(base_efficiency_km_l=-2)


def test_consumo_electrico_cero_es_rechazado():
    with pytest.raises(ValueError):
        _vehicle(base_consumption_kwh_km=0)
    with pytest.raises(ValueError):
        _vehicle(base_consumption_kwh_km=-1.5)


def test_porcentaje_electrico_fuera_de_rango_es_rechazado():
    with pytest.raises(ValueError):
        _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=-0.1)
    with pytest.raises(ValueError):
        _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=1.5)


def test_porcentaje_electrico_en_extremos_es_valido():
    hibrido_cero = _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=0.0)
    hibrido_total = _vehicle(type=VehicleType.HYBRID, electric_usage_ratio=1.0)
    assert hibrido_cero.electric_usage_ratio == 0.0
    assert hibrido_total.electric_usage_ratio == 1.0