"""Arma el informe del parcial en HTML y PDF a partir de los documentos de docs/.

Uso:  python tools/generar_informe.py

Requiere el paquete `markdown` y Microsoft Edge o Chrome para imprimir a PDF.
"""

import html
import shutil
import subprocess
from pathlib import Path

import markdown

RAIZ = Path(__file__).resolve().parent.parent
DOCS = RAIZ / "docs"
HTML_SALIDA = DOCS / "informe.html"
PDF_SALIDA = RAIZ / "Informe_Parcial3_0182310065.pdf"

PARTES = [
    "01-requisitos.md",
    "02-plan-de-pruebas.md",
    "03-caja-negra.md",
    "04-caja-blanca.md",
    "05-automatizacion-y-defectos.md",
    "06-mantenimiento-y-refactorizacion.md",
    "07-gestion-de-configuracion.md",
    "08-solicitud-de-cambio.md",
]

# (título, archivo de docs/evidencias)
ANEXOS = [
    ("A.1 Pruebas contra el código heredado v1.0.0 (fallan 20)",
     "01-pruebas-v1.0.0-heredado.txt"),
    ("A.2 Pruebas de regresión sobre v2.0.0 (todas pasan)",
     "04-regresion-v2.0.0.txt"),
    ("A.3 Pruebas de la hora pico escritas primero (fallan)",
     "06-hora-pico-pruebas-primero.txt"),
    ("A.4 Pruebas sobre v2.1.0 (todas pasan)",
     "07-pruebas-v2.1.0.txt"),
    ("A.5 Historial de Git", "08-git-log.txt"),
]

NAVEGADORES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]

ESTILOS = """
@page { size: A4; margin: 16mm 14mm 16mm 14mm; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Arial, sans-serif; font-size: 10pt;
       line-height: 1.42; color: #111; margin: 0; }
h1 { font-size: 17pt; color: #0b3d6b; border-bottom: 2px solid #0b3d6b;
     padding-bottom: 4px; margin: 0 0 10px; page-break-before: always; }
h2 { font-size: 12.5pt; color: #0b3d6b; margin: 16px 0 6px; }
h3 { font-size: 10.8pt; margin: 13px 0 4px; }
h2, h3 { page-break-after: avoid; }
p { margin: 5px 0; }
table { border-collapse: collapse; width: 100%; margin: 7px 0 10px;
        font-size: 8.4pt; }
th, td { border: 1px solid #9aa4ae; padding: 3px 5px; vertical-align: top;
         text-align: left; }
th { background: #e6eef6; }
tr { page-break-inside: avoid; }
code { font-family: Consolas, "Courier New", monospace; font-size: 8.8pt;
       background: #f1f3f5; padding: 0 2px; border-radius: 2px; }
pre { background: #0f1720; color: #dde5ec; padding: 8px 10px;
      border-radius: 4px; font-size: 7.1pt; line-height: 1.3;
      white-space: pre-wrap; word-break: break-all;
      -webkit-print-color-adjust: exact; print-color-adjust: exact; }
pre code { background: none; color: inherit; font-size: inherit; padding: 0; }
blockquote { margin: 6px 0; padding: 4px 10px; border-left: 3px solid #0b3d6b;
             background: #f4f8fb; }
img { display: block; margin: 6px auto; max-width: 100%; max-height: 200mm; }
.portada { text-align: center; padding-top: 30mm; }
.portada h1 { page-break-before: avoid; border: none; font-size: 23pt; }
.portada .dato { font-size: 12pt; margin: 4px 0; }
.portada table { width: 100%; margin-top: 12mm; font-size: 9.5pt; }
.portada td, .portada th { text-align: center; }
.verde { color: #5fd38d; } .rojo { color: #ff8a80; }
"""

PORTADA = """
<section class="portada">
  <p class="dato">UNIVERSIDAD DE LA GUAJIRA</p>
  <p class="dato">Facultad de Ingenierías - Ingeniería de Sistemas</p>
  <h1>Parcial 3 - Ingeniería de Software I</h1>
  <p class="dato">Caso EnvíaYa: pruebas, mantenimiento y evolución</p>
  <br>
  <p class="dato"><strong>Estudiante:</strong> Álvaro Javier Montero Fonseca</p>
  <p class="dato"><strong>Código estudiantil:</strong> 0182310065</p>
  <p class="dato"><strong>Grupo:</strong> B1 - VI semestre</p>
  <p class="dato"><strong>Docente:</strong> Ing. Robert Damián Quintero Laverde</p>
  <p class="dato"><strong>Fecha:</strong> 11 de noviembre de 2026</p>
  <p class="dato"><strong>Repositorio:</strong>
     github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software</p>
  <h2>Mis parámetros</h2>
  <table>
    <tr><th>A</th><th>B</th><th>C</th><th>D</th><th>E</th><th>F</th>
        <th>PMAX</th><th>L1</th><th>L2</th><th>RR</th><th>RN</th><th>V</th>
        <th>S</th><th>CAMBIO</th></tr>
    <tr><td>3</td><td>1</td><td>0</td><td>0</td><td>6</td><td>5</td>
        <td>45 kg</td><td>3 kg</td><td>10 kg</td><td>20 %</td><td>50 %</td>
        <td>10 %</td><td>$2.000</td><td>2 (hora pico)</td></tr>
  </table>
  <table>
    <tr><th>D = 0 (par)</th><th>E = 6 (par)</th><th>B = 1 (impar)</th>
        <th>F = 5 (impar)</th></tr>
    <tr><td>El tramo 1 incluye el límite: peso ≤ 3</td>
        <td>El recargo de fin de semana va antes de los descuentos</td>
        <td>Se aplican ambos descuentos: cliente y luego cupón</td>
        <td>Un cupón que no existe es error</td></tr>
  </table>
</section>
"""


def _colorear(texto):
    """Resalta PASSED y FAILED en las salidas de consola."""
    texto = html.escape(texto)
    texto = texto.replace("PASSED", '<span class="verde">PASSED</span>')
    texto = texto.replace("FAILED", '<span class="rojo">FAILED</span>')
    return texto


def construir_html():
    cuerpo = [PORTADA]
    for nombre in PARTES:
        ruta = DOCS / nombre
        if not ruta.exists():
            raise SystemExit(f"falta {nombre}: el informe quedaría incompleto")
        cuerpo.append(
            markdown.markdown(
                ruta.read_text(encoding="utf-8"),
                extensions=["tables", "fenced_code", "sane_lists"],
            )
        )
    cuerpo.append("<h1>Anexo - Evidencias de ejecución</h1>")
    cuerpo.append(
        "<p>Salidas reales de la consola, guardadas en "
        "<code>docs/evidencias/</code> del repositorio.</p>"
    )
    for titulo, archivo in ANEXOS:
        ruta = DOCS / "evidencias" / archivo
        if not ruta.exists():
            raise SystemExit(f"falta la evidencia {archivo}")
        cuerpo.append(f"<h2>{html.escape(titulo)}</h2>")
        cuerpo.append(f"<pre>{_colorear(ruta.read_text(encoding='utf-8'))}</pre>")
    return (
        '<!doctype html><html lang="es"><head><meta charset="utf-8">'
        "<title>Informe Parcial 3 - 0182310065</title>"
        f"<style>{ESTILOS}</style></head><body>{''.join(cuerpo)}</body></html>"
    )


def imprimir_pdf():
    navegador = next((n for n in NAVEGADORES if Path(n).exists()), None)
    navegador = navegador or shutil.which("msedge") or shutil.which("chrome")
    if navegador is None:
        print("No se encontró Edge ni Chrome: abre docs/informe.html e imprime a PDF.")
        return
    subprocess.run(
        [navegador, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={PDF_SALIDA}", HTML_SALIDA.as_uri()],
        check=True, capture_output=True,
    )
    print(f"PDF generado: {PDF_SALIDA.name}")


if __name__ == "__main__":
    HTML_SALIDA.write_text(construir_html(), encoding="utf-8")
    print(f"HTML generado: {HTML_SALIDA.relative_to(RAIZ)}")
    imprimir_pdf()
