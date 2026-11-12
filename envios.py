"""Cálculo del costo de un envío de EnvíaYa.

Especificación del código estudiantil 0182310065 (A=3 B=1 C=0 D=0 E=6 F=5).
Las reglas R1 a R8 están en docs/01-requisitos.md.

Orden del cálculo:
    validar -> tarifa base -> recargo de zona -> recargo de hora pico
    -> recargo de fin de semana -> descuento de cliente -> descuento de cupón
    -> costo mínimo -> redondeo
"""

from abc import ABC, abstractmethod
from decimal import ROUND_HALF_UP, Decimal

# --- Parámetros de mi especificación ---------------------------------------
PESO_MAXIMO_KG = 45             # PMAX = 30 + 5*A
LIMITE_TRAMO_1_KG = 3           # L1 = 2 + (B mod 3); incluido porque D es par
LIMITE_TRAMO_2_KG = 10          # L2 = 10 + C; incluido

TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_ADICIONAL = 800       # por cada kg sobre LIMITE_TRAMO_2_KG

RECARGO_RURAL_PCT = 20          # RR = 10 + 5*(E mod 4)
RECARGO_NACIONAL_PCT = 50       # RN = 40 + 5*(F mod 3)
RECARGO_FIN_DE_SEMANA = 2000    # S = 2000 + 500*(C mod 4)
DIAS_VALIDOS = range(1, 8)      # 1 = lunes ... 7 = domingo
DIAS_FIN_DE_SEMANA = (6, 7)     # sábado y domingo

HORAS_VALIDAS = range(0, 24)
HORA_PICO_INICIO = 17           # incluida
HORA_PICO_FIN = 19              # incluida
RECARGO_HORA_PICO_PCT = 8

DESCUENTO_FRECUENTE_PCT = 5
DESCUENTO_VIP_PCT = 10          # V = 10 + 5*(A mod 3)
DESCUENTOS_CLIENTE_PCT = {
    "normal": 0,
    "frecuente": DESCUENTO_FRECUENTE_PCT,
    "vip": DESCUENTO_VIP_PCT,
}
DESCUENTOS_CUPON_PCT = {"ENVIO10": 10}

COSTO_MINIMO = 5000
MULTIPLO_REDONDEO = 100


def sumar_porcentaje(valor, porcentaje):
    return valor + valor * porcentaje / 100


def restar_porcentaje(valor, porcentaje):
    return valor - valor * porcentaje / 100


# --- Patrón Estrategia: recargo por zona (R4) ------------------------------
class EstrategiaZona(ABC):
    """Interfaz común: cada zona sabe cómo recargar el valor del envío."""

    @abstractmethod
    def aplicar_recargo(self, valor):
        """Devuelve el valor con el recargo de la zona."""


class ZonaUrbana(EstrategiaZona):
    def aplicar_recargo(self, valor):
        return valor


class ZonaRural(EstrategiaZona):
    def aplicar_recargo(self, valor):
        return sumar_porcentaje(valor, RECARGO_RURAL_PCT)


class ZonaNacional(EstrategiaZona):
    def aplicar_recargo(self, valor):
        return sumar_porcentaje(valor, RECARGO_NACIONAL_PCT)


ZONAS = {
    "urbana": ZonaUrbana(),
    "rural": ZonaRural(),
    "nacional": ZonaNacional(),
}


# --- Pasos del cálculo ------------------------------------------------------
def validar_envio(peso, zona, dia, cupon, hora=None):
    """R1, R2, R7 y R9: lanza ValueError si un dato del envío no es válido."""
    if not 0 < peso <= PESO_MAXIMO_KG:
        raise ValueError("peso inválido")
    if zona not in ZONAS:
        raise ValueError("zona inválida")
    if dia not in DIAS_VALIDOS:
        raise ValueError("día inválido")
    if cupon is not None and cupon not in DESCUENTOS_CUPON_PCT:
        raise ValueError("cupón inválido")
    if hora is not None and hora not in HORAS_VALIDAS:
        raise ValueError("hora inválida")


def tarifa_base(peso):
    """R3: tarifa según el tramo de peso."""
    if peso <= LIMITE_TRAMO_1_KG:
        return Decimal(TARIFA_TRAMO_1)
    if peso <= LIMITE_TRAMO_2_KG:
        return Decimal(TARIFA_TRAMO_2)
    kilos_adicionales = Decimal(str(peso)) - LIMITE_TRAMO_2_KG
    return TARIFA_TRAMO_2 + kilos_adicionales * TARIFA_KG_ADICIONAL


def aplicar_hora_pico(valor, hora):
    """R9: +8 % entre las 17 y las 19, sobre el valor que ya trae la zona."""
    if hora is not None and HORA_PICO_INICIO <= hora <= HORA_PICO_FIN:
        return sumar_porcentaje(valor, RECARGO_HORA_PICO_PCT)
    return valor


def recargo_fin_de_semana(dia):
    """R5: recargo fijo los sábados y domingos."""
    return RECARGO_FIN_DE_SEMANA if dia in DIAS_FIN_DE_SEMANA else 0


def aplicar_descuentos(valor, cliente, cupon):
    """R6: se aplican ambos, primero el del cliente y luego el del cupón."""
    descuento_cliente = DESCUENTOS_CLIENTE_PCT.get(cliente, 0)
    descuento_cupon = DESCUENTOS_CUPON_PCT.get(cupon, 0)
    valor = restar_porcentaje(valor, descuento_cliente)
    return restar_porcentaje(valor, descuento_cupon)


def redondear(valor):
    """R8: costo mínimo y redondeo al múltiplo de $100; los $50 suben."""
    valor = max(valor, Decimal(COSTO_MINIMO))
    multiplos = (valor / MULTIPLO_REDONDEO).quantize(Decimal(1), ROUND_HALF_UP)
    return int(multiplos) * MULTIPLO_REDONDEO


def calcular_costo(peso, zona, cliente, dia, cupon=None, *, hora=None):
    """Devuelve el costo del envío en pesos, como entero múltiplo de 100.

    `hora` (0 a 23) es opcional y solo se acepta por nombre. Si no se indica,
    no se cobra recargo de hora pico.
    """
    validar_envio(peso, zona, dia, cupon, hora)
    valor = tarifa_base(peso)
    valor = ZONAS[zona].aplicar_recargo(valor)
    valor = aplicar_hora_pico(valor, hora)        # después de la zona
    valor = valor + recargo_fin_de_semana(dia)    # antes de los descuentos
    valor = aplicar_descuentos(valor, cliente, cupon)
    return redondear(valor)


# Nombre original de la función: se conserva para quien ya la usa.
calc = calcular_costo
