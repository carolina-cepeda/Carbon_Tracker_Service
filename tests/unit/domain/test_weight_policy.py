"""Pruebas del ajuste por peso de la carga.

Foco: que la penalización de consumo crezca con las toneladas y se
comporte de forma predecible en los extremos (0 y cargas grandes).
"""
import pytest

from app.domain.services.emission.weight_policy import (
    WEIGHT_PENALTY_PER_TON,
    weight_adjustment_factor,
)


def test_sin_carga_el_factor_es_neutro():
    assert weight_adjustment_factor(0) == 1.0, (
        "Un viaje sin carga (0 toneladas) no debería penalizar el consumo: "
        "el factor debe ser 1 (neutro)."
    )


def test_cada_tonelada_penaliza_el_dos_por_ciento():
    assert weight_adjustment_factor(10) == pytest.approx(1 + 10 * WEIGHT_PENALTY_PER_TON)


def test_carga_grande_nunca_hace_factor_cero():
    assert weight_adjustment_factor(100) > weight_adjustment_factor(10)


def test_peso_negativo_no_se_enmascara_como_magnitud():
    assert weight_adjustment_factor(-5) == pytest.approx(1 - 5 * WEIGHT_PENALTY_PER_TON), (
        "La función no debe ignorar el signo de un peso negativo: "
        "Weight ya rechaza los negativos en el dominio, así que un valor negativo "
        "aquí es una señal de bug y no debe enmascararse con abs()."
    )