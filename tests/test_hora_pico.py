"""Pruebas de la solicitud de cambio CR-02: hora pico (Parte 8).

Regla nueva R9: se agrega el parámetro hora (0 a 23). Entre las 17 y las 19,
inclusive, hay un recargo del 8 % que se calcula después del recargo por zona
(y, con mis reglas, antes del recargo de fin de semana y de los descuentos).

Estas pruebas se escribieron ANTES de implementar el cambio.
"""

import pytest

from envios import calc

LUNES, SABADO, DOMINGO = 1, 6, 7

# (id, peso, zona, cliente, día, cupón, hora, costo esperado)
CASOS_HORA_PICO = [
    # --- Valores límite de la franja 17-19 (5 kg urbano = $9.000) ---
    ("HP-01", 5, "urbana", "normal", LUNES, None, 16, 9000),
    ("HP-02", 5, "urbana", "normal", LUNES, None, 17, 9700),   # 9.720
    ("HP-03", 5, "urbana", "normal", LUNES, None, 18, 9700),
    ("HP-04", 5, "urbana", "normal", LUNES, None, 19, 9700),
    ("HP-05", 5, "urbana", "normal", LUNES, None, 20, 9000),
    # --- Límites del rango válido 0-23 ---
    ("HP-06", 5, "urbana", "normal", LUNES, None, 0, 9000),
    ("HP-07", 5, "urbana", "normal", LUNES, None, 23, 9000),
    # --- El 8 % se calcula sobre el valor que ya trae el recargo de zona ---
    ("HP-10", 5, "rural", "normal", LUNES, None, 18, 11700),   # 11.664
    # --- Va antes del recargo de fin de semana y de los descuentos ---
    ("HP-11", 5, "urbana", "vip", DOMINGO, None, 17, 10500),   # 10.548
    # --- Caso completo ---
    ("HP-12", 12.5, "nacional", "vip", SABADO, "ENVIO10", 19, 16100),  # 16.054,2
    # --- Con costo cercano al mínimo ---
    ("HP-13", 2, "urbana", "vip", LUNES, "ENVIO10", 18, 5200),  # 5.248,8
]


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, hora, esperado",
    [caso[1:] for caso in CASOS_HORA_PICO],
    ids=[caso[0] for caso in CASOS_HORA_PICO],
)
def test_costo_con_hora(peso, zona, cliente, dia, cupon, hora, esperado):
    assert calc(peso, zona, cliente, dia, cupon, hora=hora) == esperado


@pytest.mark.parametrize("hora", [-1, 24, 18.5], ids=["HP-08", "HP-09", "HP-14"])
def test_hora_invalida_lanza_error(hora):
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", LUNES, hora=hora)


def test_HP_15_sin_hora_no_cambia_el_costo():
    """Compatibilidad: quien no envía la hora obtiene el costo de siempre."""
    assert calc(5, "urbana", "normal", LUNES) == 9000
    assert calc(4, "rural", "vip", SABADO, "ENVIO10") == 10400
