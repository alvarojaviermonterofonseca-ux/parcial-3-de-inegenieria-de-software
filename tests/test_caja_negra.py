"""Casos de caja negra de EnvíaYa (Parte 3 del parcial).

Código estudiantil 0182310065 -> A=3 B=1 C=0 D=0 E=6 F=5
PMAX=45 kg, L1=3 kg (incluido), L2=10 kg, rural +20 %, nacional +50 %,
VIP 10 %, fin de semana +$2.000 antes de los descuentos, se aplican ambos
descuentos y un cupón que no existe es error.

Los resultados esperados están calculados a mano a partir de la
especificación (ver docs/03-caja-negra.md), no a partir del código.
"""

import pytest

from envios import calc

LUNES, VIERNES, SABADO, DOMINGO = 1, 5, 6, 7

# (id, peso, zona, cliente, día, cupón, costo esperado)
CASOS_CON_COSTO = [
    # --- Valores límite y particiones del peso (R1, R3) ---
    ("CN-03", 0.01, "urbana", "normal", LUNES, None, 6000),
    ("CN-04", 2.99, "urbana", "normal", LUNES, None, 6000),
    ("CN-05", 3, "urbana", "normal", LUNES, None, 6000),      # L1 incluido (D par)
    ("CN-06", 3.01, "urbana", "normal", LUNES, None, 9000),
    ("CN-07", 9.99, "urbana", "normal", LUNES, None, 9000),
    ("CN-08", 10, "urbana", "normal", LUNES, None, 9000),     # L2 incluido
    ("CN-09", 10.01, "urbana", "normal", LUNES, None, 9000),  # 9.008 -> 9.000
    ("CN-10", 20, "urbana", "normal", LUNES, None, 17000),
    ("CN-11", 44.99, "urbana", "normal", LUNES, None, 37000), # 36.992 -> 37.000
    ("CN-12", 45, "urbana", "normal", LUNES, None, 37000),    # PMAX incluido
    # --- Zona (R4) ---
    ("CN-15", 5, "rural", "normal", LUNES, None, 10800),
    ("CN-16", 5, "nacional", "normal", LUNES, None, 13500),
    # --- Día (R2, R5) ---
    ("CN-19", 5, "urbana", "normal", LUNES, None, 9000),
    ("CN-20", 5, "urbana", "normal", VIERNES, None, 9000),
    ("CN-21", 5, "urbana", "normal", SABADO, None, 11000),
    ("CN-22", 5, "urbana", "normal", DOMINGO, None, 11000),
    # --- Tabla de decisión cliente x cupón x fin de semana (R5, R6) ---
    ("CN-24", 5, "urbana", "normal", LUNES, "ENVIO10", 8100),
    ("CN-25", 5, "urbana", "frecuente", LUNES, None, 8600),       # 8.550 -> 8.600
    ("CN-26", 5, "urbana", "frecuente", LUNES, "ENVIO10", 7700),  # 7.695
    ("CN-27", 5, "urbana", "vip", LUNES, None, 8100),
    ("CN-28", 5, "urbana", "vip", LUNES, "ENVIO10", 7300),        # 7.290
    ("CN-29", 5, "urbana", "normal", DOMINGO, "ENVIO10", 9900),
    ("CN-30", 5, "urbana", "frecuente", DOMINGO, None, 10500),    # 10.450
    ("CN-31", 5, "urbana", "frecuente", DOMINGO, "ENVIO10", 9400),  # 9.405
    ("CN-32", 5, "urbana", "vip", DOMINGO, None, 9900),
    ("CN-33", 5, "urbana", "vip", DOMINGO, "ENVIO10", 8900),      # 8.910
    # --- Costo mínimo y redondeo (R8) ---
    ("CN-36", 2, "urbana", "vip", LUNES, "ENVIO10", 5000),        # 4.860 -> piso
    ("CN-37", 2, "urbana", "frecuente", LUNES, "ENVIO10", 5100),  # 5.130
    # --- Casos combinados ---
    ("CN-38", 4, "rural", "vip", SABADO, "ENVIO10", 10400),       # 10.368
    ("CN-39", 12.5, "nacional", "vip", SABADO, "ENVIO10", 15000), # 14.985
    ("CN-40", 45, "nacional", "frecuente", DOMINGO, None, 54600), # 54.625
    ("CN-41", 3, "rural", "frecuente", SABADO, None, 8700),       # 8.740
]

# (id, peso, zona, cliente, día, cupón) -> debe lanzar un error
CASOS_CON_ERROR = [
    ("CN-01", -1, "urbana", "normal", LUNES, None),            # R1 peso negativo
    ("CN-02", 0, "urbana", "normal", LUNES, None),             # R1 límite 0
    ("CN-13", 45.01, "urbana", "normal", LUNES, None),         # R1 justo sobre PMAX
    ("CN-14", 50, "urbana", "normal", LUNES, None),            # R1 sobre PMAX
    ("CN-17", 5, "internacional", "normal", LUNES, None),      # R2 zona inválida
    ("CN-18", 5, "urbana", "normal", 0, None),                 # R2 día 0
    ("CN-23", 5, "urbana", "normal", 8, None),                 # R2 día 8
    ("CN-34", 5, "urbana", "normal", LUNES, "NOEXISTE"),       # R7 cupón inexistente
    ("CN-35", 5, "urbana", "vip", DOMINGO, "envio10"),         # R7 cupón mal escrito
]


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon, esperado",
    [caso[1:] for caso in CASOS_CON_COSTO],
    ids=[caso[0] for caso in CASOS_CON_COSTO],
)
def test_costo_esperado(peso, zona, cliente, dia, cupon, esperado):
    assert calc(peso, zona, cliente, dia, cupon) == esperado


@pytest.mark.parametrize(
    "peso, zona, cliente, dia, cupon",
    [caso[1:] for caso in CASOS_CON_ERROR],
    ids=[caso[0] for caso in CASOS_CON_ERROR],
)
def test_entrada_invalida_lanza_error(peso, zona, cliente, dia, cupon):
    with pytest.raises(ValueError):
        calc(peso, zona, cliente, dia, cupon)


def test_CN_42_mensaje_de_peso_invalido():
    """R1: el error debe decir exactamente "peso inválido"."""
    with pytest.raises(ValueError) as error:
        calc(0, "urbana", "normal", LUNES)
    assert str(error.value) == "peso inválido"
