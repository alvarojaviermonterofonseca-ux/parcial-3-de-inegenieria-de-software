"""Casos de caja blanca de EnvíaYa (Parte 4 del parcial).

Un caso por cada camino independiente del grafo de flujo de calc
(V(G) = 15, ver docs/04-caja-blanca.md). El camino base es CB-03 y cada
uno de los demás cambia una decisión respecto a él.

El resultado esperado sale de la especificación, no del código.
"""

import pytest

from envios import calc


def test_CB_01_peso_cero_lanza_error():
    # Camino 1: p <= 0 verdadero
    with pytest.raises(ValueError):
        calc(0, "urbana", "normal", 1)


def test_CB_02_peso_sobre_el_tope_del_codigo_lanza_error():
    # Camino 2: p <= 0 falso, p > 50 verdadero
    with pytest.raises(ValueError):
        calc(51, "urbana", "normal", 1)


def test_CB_03_camino_base():
    # Camino 3: tramo 2, urbana, día hábil, cliente normal, sin cupón
    assert calc(5, "urbana", "normal", 1) == 9000


def test_CB_04_tramo_1():
    # Camino 4: p <= L1 verdadero
    assert calc(2, "urbana", "normal", 1) == 6000


def test_CB_05_tramo_3():
    # Camino 5: p <= L2 falso -> 9.000 + 10 x 800
    assert calc(20, "urbana", "normal", 1) == 17000


def test_CB_06_zona_rural():
    # Camino 6: z == "rural" verdadero -> 9.000 x 1,20
    assert calc(5, "rural", "normal", 1) == 10800


def test_CB_07_zona_nacional():
    # Camino 7: z == "nacional" verdadero -> 9.000 x 1,50
    assert calc(5, "nacional", "normal", 1) == 13500


def test_CB_08_zona_que_no_existe():
    # Camino 8: las tres comparaciones de zona son falsas.
    # Según R2 debe lanzar error.
    with pytest.raises(ValueError):
        calc(5, "internacional", "normal", 1)


def test_CB_09_fin_de_semana():
    # Camino 9: d > 6 verdadero -> 9.000 + 2.000
    assert calc(5, "urbana", "normal", 7) == 11000


def test_CB_10_cliente_frecuente():
    # Camino 10: c == "frecuente" verdadero -> 8.550 -> 8.600
    assert calc(5, "urbana", "frecuente", 1) == 8600


def test_CB_11_cliente_vip():
    # Camino 11: c == "vip" verdadero -> 9.000 x 0,90
    assert calc(5, "urbana", "vip", 1) == 8100


def test_CB_12_cupon_envio10():
    # Camino 12: cup != None verdadero y cup == "ENVIO10" verdadero
    assert calc(5, "urbana", "normal", 1, "ENVIO10") == 8100


def test_CB_13_cupon_que_no_existe():
    # Camino 13: cup != None verdadero y cup == "ENVIO10" falso.
    # Según R7 (F impar) debe lanzar error.
    with pytest.raises(ValueError):
        calc(5, "urbana", "normal", 1, "OTRO")


def test_CB_14_costo_minimo():
    # Camino 14: t < 5000 verdadero -> 6.000 x 0,90 x 0,90 = 4.860 -> 5.000
    assert calc(2, "urbana", "vip", 1, "ENVIO10") == 5000


def test_CB_15_flag_ya_no_existe():
    # Camino 15 de la versión 1.0.0. En la 2.0.0 se eliminó el parámetro
    # flag: pasar un sexto argumento posicional ahora es un error de uso.
    with pytest.raises(TypeError):
        calc(5, "urbana", "normal", 1, None, True)
