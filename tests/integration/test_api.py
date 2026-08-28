"""Pruebas de la API (capa de presentación).

Foco: que las peticiones HTTP entren por el puerto correcto y que las
respuestas sean claras: 200 cuando todo está bien y 422 cuando algo se
entendió mal en la petición.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _payload(**cambios) -> dict:
    base = {
        "vehicle_id": "TRK-001",
        "vehicle_type": "diesel",
        "distance_km": 100,
        "weight_tons": 0,
        "base_efficiency_km_l": 4.5,
        "base_consumption_kwh_km": 0.2,
    }
    base.update(cambios)
    return base


def test_calcular_diesel_sin_carga():
    response = client.post("/v1/emissions/calculate", json=_payload())
    assert response.status_code == 200, (
        "Un vehículo diésel con datos válidos debería responder 200 OK, "
        f"pero recibimos {response.status_code}: {response.text}"
    )
    body = response.json()
    assert body["total_co2_kg"] == pytest.approx((100 / 4.5) * 2.68, abs=1e-3)


def test_calcular_electrico_sin_carga():
    response = client.post(
        "/v1/emissions/calculate",
        json=_payload(vehicle_id="EV-001", vehicle_type="electric", base_consumption_kwh_km=0.2),
    )
    assert response.status_code == 200
    assert response.json()["total_co2_kg"] == pytest.approx(100 * 0.2 * 0.4, rel=1e-6)


def test_calcular_gasolina_sin_carga():
    response = client.post(
        "/v1/emissions/calculate",
        json=_payload(vehicle_id="G-001", vehicle_type="gasoline"),
    )
    assert response.status_code == 200
    assert response.json()["total_co2_kg"] == pytest.approx(100 / 4.5 * 2.31, abs=1e-3)


def test_calcular_hibrido_con_carga():
    response = client.post(
        "/v1/emissions/calculate",
        json=_payload(
            vehicle_id="HYB-001",
            vehicle_type="hybrid",
            distance_km=250,
            weight_tons=12,
            base_efficiency_km_l=5.0,
            base_consumption_kwh_km=0.15,
            electric_usage_ratio=0.4,
        ),
    )
    assert response.status_code == 200
    body = response.json()
    assert "fuel_emissions_kg" in body["breakdown"] and "grid_emissions_kg" in body["breakdown"], (
        "Un vehículo híbrido debería desglosar sus emisiones entre la parte de "
        "combustible y la parte eléctrica."
    )
    assert body["total_co2_kg"] > 0


def test_hibrido_sin_porcentaje_electrico_se_rechaza():
    response = client.post(
        "/v1/emissions/calculate",
        json=_payload(
            vehicle_id="HYB-001",
            vehicle_type="hybrid",
            base_efficiency_km_l=5.0,
            base_consumption_kwh_km=0.15,
        ),
    )
    assert response.status_code == 422, (
        "Si dices que el vehículo es híbrido, debes indicar qué porcentaje usa "
        "el motor eléctrico (electric_usage_ratio). Sin ese dato la petición "
        "carece de sentido y debería devolverse 422."
    )


def test_distancia_cero_se_rechaza():
    response = client.post("/v1/emissions/calculate", json=_payload(distance_km=0))
    assert response.status_code == 422, (
        "Un viaje no puede tener distancia 0 o negativa; la petición debería "
        "rechazarse con 422."
    )


def test_peso_neutral_cero_es_aceptado():
    response = client.post("/v1/emissions/calculate", json=_payload(weight_tons=0))
    assert response.status_code == 200, (
        "Cargar 0 toneladas (viaje vacío) es válido y debería responder 200 OK."
    )


def test_peso_negativo_se_rechaza():
    response = client.post("/v1/emissions/calculate", json=_payload(weight_tons=-3))
    assert response.status_code == 422, (
        "Una carga no puede pesar menos de 0; la petición debería rechazarse."
    )


def test_identificador_vacio_se_rechaza():
    response = client.post("/v1/emissions/calculate", json=_payload(vehicle_id="   "))
    assert response.status_code == 422, (
        "Un vehículo sin identificador válido no se puede procesar y debería "
        "devolverse un 422 con la explicación del problema."
    )
    assert "error" in response.json()["detail"].lower() or "vehicle_id" in response.json()["detail"].lower()


def test_tipo_de_vehiculo_no_soportado_se_rechaza():
    response = client.post("/v1/emissions/calculate", json=_payload(vehicle_type="tractor"))
    assert response.status_code == 422, (
        "El tipo de vehículo 'tractor' no es uno de los soportados; la API "
        "debería rechazarlo en lugar de guardarlo silenciosamente."
    )


def test_eficiencia_cero_se_rechaza():
    response = client.post("/v1/emissions/calculate", json=_payload(base_efficiency_km_l=0))
    assert response.status_code == 422, (
        "Una eficiencia de 0 km/litro es imposible y debería rechazarse."
    )


def test_consultar_factores():
    response = client.get("/v1/emissions/factors")
    assert response.status_code == 200
    body = response.json()
    assert body["diesel"]["value"] == pytest.approx(2.68, rel=1e-6)
    assert body["gasoline"]["value"] == pytest.approx(2.31, rel=1e-6)
    assert body["grid_electricity"]["value"] == pytest.approx(0.4, rel=1e-6)


def test_salud_del_servicio():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}