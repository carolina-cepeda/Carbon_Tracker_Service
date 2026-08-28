"""Pruebas de los manejadores globales de error.

Foco: que los errores internos lleguen al usuario final convertidos en
respuestas HTTP claras, sin filtraciones técnicas.
"""
import asyncio

from app.main import unhandled_error_handler, value_error_handler


def test_error_de_negocio_se_responde_como_422():
    response = asyncio.run(
        value_error_handler(None, ValueError("la carga no puede ser negativa"))
    )
    assert response.status_code == 422, (
        "Un error de regla de negocio debería llegar al usuario como un 422 "
        "(petición no entendida), con su explicación."
    )
    assert b"la carga no puede ser negativa" not in response.body, (
        "El handler global no debería devolver el texto del ValueError directamente, "
        "ya que podría contener detalles técnicos internos."
    )


def test_error_inesperado_se_responde_como_500_sin_detalles():
    response = asyncio.run(
        unhandled_error_handler(None, RuntimeError("detalle interno"))
    )
    assert response.status_code == 500, (
        "Un fallo imprevisto del servidor debería devolverse como 500."
    )
    assert b"Internal server error" in response.body
    assert b"detalle interno" not in response.body, (
        "Los detalles técnicos internos no deberían filtrarse al usuario."
    )