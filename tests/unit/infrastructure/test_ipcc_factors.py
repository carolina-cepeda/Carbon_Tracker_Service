"""Pruebas del catálogo de factores de emisión IPCC.

Verifica que los factores configurados sean los esperados y que se
informe con claridad cuando alguien pida un combustible desconocido.
"""
import pytest

from app.domain.enums.vehicle_type import VehicleType
from app.infrastructure.factors.ipcc_factors import IpccFactorCatalog


def test_factores_conocidos_estan_disponibles():
    catalogo = IpccFactorCatalog(grid_factor_kg_kwh=0.4)

    assert catalogo.get_factor(VehicleType.DIESEL).value == 2.68
    assert catalogo.get_factor(VehicleType.GASOLINE).value == 2.31
    assert catalogo.get_grid_factor().value == 0.4


def test_combustible_desconocido_explica_el_problema():
    catalogo = IpccFactorCatalog(grid_factor_kg_kwh=0.4)
    with pytest.raises(ValueError) as error:
        catalogo.get_factor(VehicleType.HYBRID)
    assert "Unknown fuel type" in str(error.value), (
        "El mensaje debería indicar que el tipo de combustible no está soportado."
    )


def test_factor_de_red_customizable():
    catalogo = IpccFactorCatalog(grid_factor_kg_kwh=0.9)
    assert catalogo.get_grid_factor().value == 0.9