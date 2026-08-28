"""Pruebas del resultado de cálculo.

Verifica que el formato en el que se entrega el resultado al exterior
(por ejemplo, a la API) sea claro y redondeado a 3 decimales.
"""
from app.domain.entities.emission_calculation import EmissionCalculation
from app.domain.value_objects.distance import Distance
from app.domain.value_objects.weight import Weight


def test_resultado_se_convierte_a_formato_legible():
    resultado = EmissionCalculation(
        distance=Distance(100),
        weight=Weight(7.5),
        total_co2_kg=123.456789,
        breakdown={"emissions_kg": 123.457},
        formula_used="combustion",
    )
    datos = resultado.to_dict()

    assert datos == {
        "distance_km": 100,
        "weight_tons": 7.5,
        "total_co2_kg": 123.457,
        "breakdown": {"emissions_kg": 123.457},
        "formula_used": "combustion",
    }, (
        "El resultado exportado debería incluir todas las claves con el total "
        "redondeado a 3 decimales, tal como lo consumirá la API."
    )


def test_redondeo_de_total_a_tres_decimales():
    resultado = EmissionCalculation(
        distance=Distance(1),
        weight=Weight(0),
        total_co2_kg=2.675,
        breakdown={},
        formula_used="x",
    )
    assert resultado.to_dict()["total_co2_kg"] == 2.675