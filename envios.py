# envios.py

CONFIG = {
    "PMAX": 45,                # 30 + 5*A = 30 + 5*3, en kg
    "L1": 3,                   # 2 + (B mod 3) = 2 + (1 mod 3)
    "L2": 10,                  # 10 + C = 10 + 0
    "RECARGO_RURAL": 0.20,     # 10 + 5*(E mod 4) = 20 %
    "RECARGO_NACIONAL": 0.50,  # 40 + 5*(F mod 3) = 50 %
    "DESC_VIP": 0.10,          # 10 + 5*(A mod 3) = 10 %
    "RECARGO_FINDE": 2000,     # 2000 + 500*(C mod 4), en pesos
}


def calc(p, z, c, d, cup=None, flag=False):
    if p <= 0 or p > CONFIG["PMAX"]:
        raise ValueError("peso invalido")
    if p <= CONFIG["L1"]:
        t = 6000
    elif p <= CONFIG["L2"]:
        t = 9000
    else:
        t = 9000 + (p - CONFIG["L2"]) * 800
    if z == "urbana":
        t = t
    elif z == "rural":
        t = t + t * CONFIG["RECARGO_RURAL"]
    elif z == "nacional":
        t = t + t * CONFIG["RECARGO_NACIONAL"]
    else:
        raise ValueError("zona inválida")
    # fin de semana
    if d >= 6:
        t = t + CONFIG["RECARGO_FINDE"]
    if c == "frecuente":
        t = t - t * 0.05
    if c == "vip":
        t = t - t * CONFIG["DESC_VIP"]
    if cup != None:
        if cup == "ENVIO10":
            t = t - t * 0.10
    if t < 5000:
        t = 5000
    if flag:
        print("costo:", t)
    return int(round(t, 2) / 100 + 0.5) * 100
