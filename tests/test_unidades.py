"""Pruebas de unidad de las piezas que salieron de la refactorización.

Cada función extraída de calc y cada estrategia de zona se prueba sola
(nivel de unidad del plan de pruebas).
"""

from decimal import Decimal

import pytest

import envios
from envios import (
    EstrategiaZona,
    ZonaNacional,
    ZonaRural,
    ZonaUrbana,
    aplicar_descuentos,
    recargo_fin_de_semana,
    redondear,
    tarifa_base,
    validar_envio,
)


# --- Patrón Estrategia -----------------------------------------------------
@pytest.mark.parametrize(
    "estrategia, esperado",
    [(ZonaUrbana(), 9000), (ZonaRural(), 10800), (ZonaNacional(), 13500)],
    ids=["urbana", "rural", "nacional"],
)
def test_cada_zona_aplica_su_recargo(estrategia, esperado):
    assert estrategia.aplicar_recargo(Decimal(9000)) == esperado


def test_todas_las_zonas_registradas_son_estrategias():
    assert set(envios.ZONAS) == {"urbana", "rural", "nacional"}
    assert all(isinstance(zona, EstrategiaZona) for zona in envios.ZONAS.values())


def test_la_estrategia_abstracta_no_se_puede_instanciar():
    with pytest.raises(TypeError):
        EstrategiaZona()


# --- Funciones extraídas ---------------------------------------------------
@pytest.mark.parametrize(
    "peso, esperado",
    [(0.5, 6000), (3, 6000), (3.01, 9000), (10, 9000), (10.5, 9400), (45, 37000)],
)
def test_tarifa_base(peso, esperado):
    assert tarifa_base(peso) == esperado


@pytest.mark.parametrize("dia, esperado", [(1, 0), (5, 0), (6, 2000), (7, 2000)])
def test_recargo_fin_de_semana(dia, esperado):
    assert recargo_fin_de_semana(dia) == esperado


def test_descuentos_se_aplican_en_cadena():
    # VIP 10 % y luego cupón 10 % sobre lo que queda: 10.000 -> 9.000 -> 8.100
    assert aplicar_descuentos(Decimal(10000), "vip", "ENVIO10") == 8100


@pytest.mark.parametrize(
    "valor, esperado",
    [("8549.99", 8500), ("8550", 8600), ("8550.01", 8600), ("8649.99", 8600),
     ("4860", 5000), ("5000", 5000), ("5049.99", 5000), ("5050", 5100)],
)
def test_redondear(valor, esperado):
    assert redondear(Decimal(valor)) == esperado


@pytest.mark.parametrize(
    "peso, zona, dia, cupon, mensaje",
    [
        (0, "urbana", 1, None, "peso inválido"),
        (45.01, "urbana", 1, None, "peso inválido"),
        (5, "lunar", 1, None, "zona inválida"),
        (5, "urbana", 0, None, "día inválido"),
        (5, "urbana", 6.5, None, "día inválido"),
        (5, "urbana", 1, "NOEXISTE", "cupón inválido"),
    ],
)
def test_validar_envio_dice_que_dato_esta_mal(peso, zona, dia, cupon, mensaje):
    with pytest.raises(ValueError) as error:
        validar_envio(peso, zona, dia, cupon)
    assert str(error.value) == mensaje


def test_validar_envio_acepta_un_envio_correcto():
    assert validar_envio(45, "nacional", 7, "ENVIO10") is None
