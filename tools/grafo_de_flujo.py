"""Genera el grafo de flujo de calc (v1.0.0) como SVG en docs/img/.

Uso:  python tools/grafo_de_flujo.py
"""

from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "docs" / "img"

# ---------------------------------------------------------------------------
# Grafo de flujo de calc (versión 1.0.0)
# ---------------------------------------------------------------------------
# nodo: (columna, fila, es_predicado)
NODOS = {
    1: (0, 0, True), 2: (0, 1, True), 3: (2, 0.5, False),
    4: (0, 2, True), 5: (-1, 3, False), 6: (1, 3, True),
    7: (0, 4, False), 8: (2, 4, False),
    9: (0, 5, True), 10: (-1, 6, False), 11: (1, 6, True),
    12: (0, 7, False), 13: (2, 7, True), 14: (1, 8, False),
    15: (0, 9, True), 16: (-1, 10, False),
    17: (0, 11, True), 18: (-1, 12, False),
    19: (0, 13, True), 20: (-1, 14, False),
    21: (0, 15, True), 22: (1, 16, True), 23: (1, 17, False),
    24: (0, 18, True), 25: (-1, 19, False),
    26: (0, 20, True), 27: (-1, 21, False),
    28: (0, 22, False), 29: (0, 23, False),
}

# (origen, destino, etiqueta, puntos intermedios en columna/fila)
ARISTAS = [
    (1, 3, "V", []), (1, 2, "F", []),
    (2, 3, "V", []), (2, 4, "F", []),
    (3, 29, "", [(3, 0.5), (3, 23)]),
    (4, 5, "V", []), (4, 6, "F", []),
    (5, 9, "", []),
    (6, 7, "V", []), (6, 8, "F", []),
    (7, 9, "", []), (8, 9, "", []),
    (9, 10, "V", []), (9, 11, "F", []),
    (10, 15, "", []),
    (11, 12, "V", []), (11, 13, "F", []),
    (12, 15, "", []),
    (13, 14, "V", []), (13, 15, "F", [(2, 9)]),
    (14, 15, "", []),
    (15, 16, "V", []), (15, 17, "F", []),
    (16, 17, "", []),
    (17, 18, "V", []), (17, 19, "F", []),
    (18, 19, "", []),
    (19, 20, "V", []), (19, 21, "F", []),
    (20, 21, "", []),
    (21, 22, "V", []), (21, 24, "F", []),
    (22, 23, "V", []), (22, 24, "F", []),
    (23, 24, "", []),
    (24, 25, "V", []), (24, 26, "F", []),
    (25, 26, "", []),
    (26, 27, "V", []), (26, 28, "F", []),
    (27, 28, "", []),
    (28, 29, "", []),
]

# región: (columna, fila) donde se escribe la etiqueta
REGIONES = {
    "R1": (0.75, 0.5), "R2": (2.55, 12), "R3": (-0.3, 3.45), "R4": (1, 4.25),
    "R5": (-0.3, 7.4), "R6": (0.7, 7.3), "R7": (1.55, 8.6),
    "R8": (-0.38, 10), "R9": (-0.38, 12), "R10": (-0.38, 14),
    "R11": (0.3, 16.4), "R12": (0.72, 17), "R13": (-0.38, 19),
    "R14": (-0.38, 21), "R15": (-1.75, 12),
}

ANCHO_COL, ALTO_FILA, RADIO = 120, 44, 14
ORIGEN_X, ORIGEN_Y = 290, 30


def _xy(col, fila):
    return ORIGEN_X + col * ANCHO_COL, ORIGEN_Y + fila * ALTO_FILA


def _recortar(x1, y1, x2, y2, distancia):
    """Devuelve el punto que queda a `distancia` de (x1, y1) hacia (x2, y2)."""
    largo = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return x1 + (x2 - x1) * distancia / largo, y1 + (y2 - y1) * distancia / largo


def grafo_de_flujo():
    ancho, alto = 700, ORIGEN_Y * 2 + 23 * ALTO_FILA
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" '
        f'width="{ancho}" height="{alto}" font-family="Arial, sans-serif">',
        f'<rect width="{ancho}" height="{alto}" fill="#ffffff"/>',
        '<defs><marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker></defs>',
    ]
    for origen, destino, etiqueta, intermedios in ARISTAS:
        puntos = [_xy(*NODOS[origen][:2])]
        puntos += [_xy(c, f) for c, f in intermedios]
        puntos.append(_xy(*NODOS[destino][:2]))
        puntos[0] = _recortar(*puntos[0], *puntos[1], RADIO)
        puntos[-1] = _recortar(*puntos[-1], *puntos[-2], RADIO + 1)
        camino = " ".join(f"{x:.1f},{y:.1f}" for x, y in puntos)
        partes.append(
            f'<polyline points="{camino}" fill="none" stroke="#222" '
            'stroke-width="1.2" marker-end="url(#flecha)"/>'
        )
        if etiqueta:
            # la etiqueta va a un lado de la arista, no encima de ella
            (x1, y1), (x2, y2) = puntos[0], puntos[1]
            largo = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            px, py = (y2 - y1) / largo, -(x2 - x1) / largo  # perpendicular
            if py > 0 or (py == 0 and px < 0):
                px, py = -px, -py
            ex, ey = _recortar(x1, y1, x2, y2, min(20, largo / 2))
            color = "#0a6b2d" if etiqueta == "V" else "#b3261e"
            partes.append(
                f'<text x="{ex + px * 9:.1f}" y="{ey + py * 9 + 3.5:.1f}" '
                f'font-size="10" font-weight="bold" text-anchor="middle" '
                f'fill="{color}">{etiqueta}</text>'
            )
    for numero, (col, fila, predicado) in NODOS.items():
        x, y = _xy(col, fila)
        relleno = "#ffe08a" if predicado else "#ffffff"
        partes.append(
            f'<circle cx="{x}" cy="{y}" r="{RADIO}" fill="{relleno}" '
            'stroke="#222" stroke-width="1.3"/>'
        )
        partes.append(
            f'<text x="{x}" y="{y + 4}" font-size="11" text-anchor="middle" '
            f'fill="#111">{numero}</text>'
        )
    for nombre, (col, fila) in REGIONES.items():
        x, y = _xy(col, fila)
        partes.append(
            f'<text x="{x}" y="{y + 4}" font-size="10" font-style="italic" '
            f'text-anchor="middle" fill="#1d4ed8">{nombre}</text>'
        )
    # leyenda
    partes.append(
        '<circle cx="530" cy="930" r="9" fill="#ffe08a" stroke="#222"/>'
        '<text x="545" y="934" font-size="10" fill="#111">nodo predicado</text>'
        '<circle cx="530" cy="955" r="9" fill="#fff" stroke="#222"/>'
        '<text x="545" y="959" font-size="10" fill="#111">nodo de proceso</text>'
        '<text x="521" y="981" font-size="10" font-style="italic" '
        'fill="#1d4ed8">R1..R15</text>'
        '<text x="568" y="981" font-size="10" fill="#111">regiones</text>'
    )
    partes.append("</svg>")
    return "\n".join(partes)


def contar_grafo():
    """Aristas, nodos y nodos predicado, para verificar V(G)."""
    return len(ARISTAS), len(NODOS), sum(1 for n in NODOS.values() if n[2])


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "grafo-flujo.svg").write_text(grafo_de_flujo(), encoding="utf-8")
    aristas, nodos, predicados = contar_grafo()
    print(f"grafo-flujo.svg: E={aristas} N={nodos} P={predicados} "
          f"V(G)={aristas - nodos + 2}")
