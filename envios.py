"""Cálculo del costo de un envío de EnvíaYa.

Especificación del código estudiantil 0182310065 (A=3 B=1 C=0 D=0 E=6 F=5).
Las reglas R1 a R8 están en docs/01-requisitos.md.

Orden del cálculo:
    validar -> tarifa base -> recargo de zona -> recargo de fin de semana
    -> descuento de cliente -> descuento de cupón -> costo mínimo -> redondeo
"""

from decimal import ROUND_HALF_UP, Decimal

# --- Parámetros de mi especificación ---------------------------------------
PESO_MAXIMO_KG = 45             # PMAX = 30 + 5*A
LIMITE_TRAMO_1_KG = 3           # L1 = 2 + (B mod 3); incluido porque D es par
LIMITE_TRAMO_2_KG = 10          # L2 = 10 + C; incluido

TARIFA_TRAMO_1 = 6000
TARIFA_TRAMO_2 = 9000
TARIFA_KG_ADICIONAL = 800       # por cada kg sobre LIMITE_TRAMO_2_KG

ZONAS_VALIDAS = ("urbana", "rural", "nacional")
RECARGO_RURAL_PCT = 20          # RR = 10 + 5*(E mod 4)
RECARGO_NACIONAL_PCT = 50       # RN = 40 + 5*(F mod 3)
RECARGO_FIN_DE_SEMANA = 2000    # S = 2000 + 500*(C mod 4)
DIAS_VALIDOS = range(1, 8)      # 1 = lunes ... 7 = domingo
DIAS_FIN_DE_SEMANA = (6, 7)     # sábado y domingo

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


# --- Pasos del cálculo ------------------------------------------------------
def validar_envio(peso, zona, dia, cupon):
    """R1, R2 y R7: lanza ValueError si un dato del envío no es válido."""
    if not 0 < peso <= PESO_MAXIMO_KG:
        raise ValueError("peso inválido")
    if zona not in ZONAS_VALIDAS:
        raise ValueError("zona inválida")
    if dia not in DIAS_VALIDOS:
        raise ValueError("día inválido")
    if cupon is not None and cupon not in DESCUENTOS_CUPON_PCT:
        raise ValueError("cupón inválido")


def tarifa_base(peso):
    """R3: tarifa según el tramo de peso."""
    if peso <= LIMITE_TRAMO_1_KG:
        return Decimal(TARIFA_TRAMO_1)
    if peso <= LIMITE_TRAMO_2_KG:
        return Decimal(TARIFA_TRAMO_2)
    kilos_adicionales = Decimal(str(peso)) - LIMITE_TRAMO_2_KG
    return TARIFA_TRAMO_2 + kilos_adicionales * TARIFA_KG_ADICIONAL


def aplicar_recargo_zona(valor, zona):
    """R4: recargo según la zona de destino."""
    if zona == "rural":
        return sumar_porcentaje(valor, RECARGO_RURAL_PCT)
    if zona == "nacional":
        return sumar_porcentaje(valor, RECARGO_NACIONAL_PCT)
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


def calcular_costo(peso, zona, cliente, dia, cupon=None):
    """Devuelve el costo del envío en pesos, como entero múltiplo de 100."""
    validar_envio(peso, zona, dia, cupon)
    valor = tarifa_base(peso)
    valor = aplicar_recargo_zona(valor, zona)
    valor = valor + recargo_fin_de_semana(dia)    # antes de los descuentos
    valor = aplicar_descuentos(valor, cliente, cupon)
    return redondear(valor)


# Nombre original de la función: se conserva para quien ya la usa.
calc = calcular_costo
