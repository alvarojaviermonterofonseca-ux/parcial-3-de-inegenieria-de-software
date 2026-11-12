"""Genera el diagrama de clases UML del patrón Estrategia como SVG.

Uso:  python tools/diagrama_clases.py
"""

from pathlib import Path

SALIDA = Path(__file__).resolve().parent.parent / "docs" / "img"

ANCHO, ALTO = 900, 350
ALTO_TITULO, ALTO_LINEA = 44, 18


def _clase(x, y, ancho, estereotipo, nombre, atributos, metodos, abstracta=False):
    """Dibuja una caja de clase con tres compartimentos."""
    alto_atributos = max(len(atributos), 1) * ALTO_LINEA + 8
    alto_metodos = max(len(metodos), 1) * ALTO_LINEA + 8
    alto = ALTO_TITULO + alto_atributos + alto_metodos
    centro = x + ancho / 2
    estilo_nombre = ' font-style="italic"' if abstracta else ""
    partes = [
        f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" fill="#fffbe6" '
        'stroke="#222" stroke-width="1.3"/>',
        f'<text x="{centro}" y="{y + 16}" font-size="11" text-anchor="middle" '
        f'fill="#444">{estereotipo}</text>',
        f'<text x="{centro}" y="{y + 34}" font-size="13" font-weight="bold" '
        f'text-anchor="middle" fill="#111"{estilo_nombre}>{nombre}</text>',
        f'<line x1="{x}" y1="{y + ALTO_TITULO}" x2="{x + ancho}" '
        f'y2="{y + ALTO_TITULO}" stroke="#222"/>',
    ]
    for i, texto in enumerate(atributos):
        partes.append(
            f'<text x="{x + 8}" y="{y + ALTO_TITULO + 18 + i * ALTO_LINEA}" '
            f'font-size="11" fill="#111">{texto}</text>'
        )
    y_metodos = y + ALTO_TITULO + alto_atributos
    partes.append(
        f'<line x1="{x}" y1="{y_metodos}" x2="{x + ancho}" y2="{y_metodos}" '
        'stroke="#222"/>'
    )
    for i, texto in enumerate(metodos):
        partes.append(
            f'<text x="{x + 8}" y="{y_metodos + 18 + i * ALTO_LINEA}" '
            f'font-size="11" fill="#111"{estilo_nombre}>{texto}</text>'
        )
    return "\n".join(partes), alto


def diagrama_de_clases():
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" '
        f'width="{ANCHO}" height="{ALTO}" font-family="Arial, sans-serif">',
        f'<rect width="{ANCHO}" height="{ALTO}" fill="#ffffff"/>',
        '<defs>'
        '<marker id="herencia" viewBox="0 0 14 14" refX="13" refY="7" '
        'markerWidth="14" markerHeight="14" orient="auto">'
        '<path d="M1,1 L13,7 L1,13 z" fill="#fff" stroke="#222"/></marker>'
        '<marker id="usa" viewBox="0 0 12 12" refX="11" refY="6" '
        'markerWidth="11" markerHeight="11" orient="auto">'
        '<path d="M1,1 L11,6 L1,11" fill="none" stroke="#222"/></marker>'
        '</defs>',
    ]

    # Contexto: el módulo que usa la estrategia
    caja, _ = _clase(
        20, 30, 330, "«contexto» módulo envios", "calcular_costo",
        ["ZONAS: dict[str, EstrategiaZona]"],
        ["+ calcular_costo(peso, zona, cliente, dia, cupon): int",
         "+ validar_envio(peso, zona, dia, cupon)"],
    )
    partes.append(caja)

    # Estrategia abstracta
    caja, alto_abstracta = _clase(
        470, 30, 300, "«abstracta»", "EstrategiaZona", [],
        ["+ aplicar_recargo(valor): Decimal"], abstracta=True,
    )
    partes.append(caja)
    base_abstracta = 30 + alto_abstracta

    # Estrategias concretas
    concretas = [
        ("ZonaUrbana", "sin recargo"),
        ("ZonaRural", "+20 %  (RECARGO_RURAL_PCT)"),
        ("ZonaNacional", "+50 %  (RECARGO_NACIONAL_PCT)"),
    ]
    y_concretas, ancho_concreta = 230, 220
    x_inicial = 110
    separacion = 240
    y_bus = 185
    centro_abstracta = 470 + 150
    for i, (nombre, nota) in enumerate(concretas):
        x = x_inicial + i * separacion
        caja, _ = _clase(
            x, y_concretas, ancho_concreta, "«estrategia concreta»", nombre,
            [nota], ["+ aplicar_recargo(valor): Decimal"],
        )
        partes.append(caja)
        centro = x + ancho_concreta / 2
        partes.append(
            f'<polyline points="{centro},{y_concretas} {centro},{y_bus} '
            f'{centro_abstracta},{y_bus}" fill="none" stroke="#222" '
            'stroke-width="1.2"/>'
        )
    partes.append(
        f'<line x1="{centro_abstracta}" y1="{y_bus}" x2="{centro_abstracta}" '
        f'y2="{base_abstracta}" stroke="#222" stroke-width="1.2" '
        'marker-end="url(#herencia)"/>'
    )

    # Asociación contexto -> estrategia
    partes.append(
        '<line x1="350" y1="75" x2="470" y2="75" stroke="#222" '
        'stroke-width="1.2" marker-end="url(#usa)"/>'
        '<text x="410" y="67" font-size="11" text-anchor="middle" '
        'fill="#111">usa</text>'
        '<text x="410" y="92" font-size="10" text-anchor="middle" '
        'fill="#444">ZONAS[zona]</text>'
    )
    partes.append("</svg>")
    return "\n".join(partes)


if __name__ == "__main__":
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "uml-estrategia.svg").write_text(diagrama_de_clases(), encoding="utf-8")
    print("uml-estrategia.svg generado")
