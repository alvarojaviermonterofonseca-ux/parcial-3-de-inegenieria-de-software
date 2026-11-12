# Parcial 3 - Ingeniería de Software I

[![pruebas](https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/actions/workflows/pruebas.yml/badge.svg)](https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/actions/workflows/pruebas.yml)

Universidad de La Guajira - Ingeniería de Sistemas - Grupo B1 - 2026-2

- **Estudiante:** Álvaro Javier Montero Fonseca
- **Código estudiantil:** 0182310065
- **Docente:** Ing. Robert Damián Quintero Laverde

Caso EnvíaYa: pruebas, mantenimiento y evolución de la función que calcula
el costo de un envío.

## Mis parámetros

Últimos 6 dígitos del código: **3 1 0 0 6 5**

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 3 | 1 | 0 | 0 | 6 | 5 | 45 kg | 3 kg | 10 kg | 20 % | 50 % | 10 % | $2.000 | 2 (hora pico) |

Reglas según la paridad:

| Dígito | Valor | Regla que me toca |
|--------|-------|-------------------|
| D - tramo 1 | 0 (par) | Incluye el límite: `peso <= 3` |
| E - recargo de fin de semana | 6 (par) | Se suma **antes** de los descuentos |
| B - cliente y cupón | 1 (impar) | Se aplican **ambos**: primero cliente, luego cupón |
| F - cupón que no existe | 5 (impar) | **Es error** |

## Informe

El informe completo está en
[`Informe_Parcial3_0182310065.pdf`](Informe_Parcial3_0182310065.pdf). Cada
parte también se puede leer aquí:

| Parte | Documento |
|-------|-----------|
| 1. Requisitos y criterios de aceptación | [docs/01-requisitos.md](docs/01-requisitos.md) |
| 2. Plan de pruebas | [docs/02-plan-de-pruebas.md](docs/02-plan-de-pruebas.md) |
| 3. Caja negra | [docs/03-caja-negra.md](docs/03-caja-negra.md) |
| 4. Caja blanca | [docs/04-caja-blanca.md](docs/04-caja-blanca.md) |
| 5. Automatización, ejecución y defectos | [docs/05-automatizacion-y-defectos.md](docs/05-automatizacion-y-defectos.md) |
| 6. Mantenimiento y refactorización | [docs/06-mantenimiento-y-refactorizacion.md](docs/06-mantenimiento-y-refactorizacion.md) |
| 7. Gestión de configuración | [docs/07-gestion-de-configuracion.md](docs/07-gestion-de-configuracion.md) |
| 8. Solicitud de cambio (hora pico) | [docs/08-solicitud-de-cambio.md](docs/08-solicitud-de-cambio.md) |

## Versiones

| Etiqueta | Qué contiene | Pruebas |
|----------|--------------|---------|
| `v1.0.0` | Código heredado, solo con `CONFIG` lleno | 37 de 57 pasan (7 defectos) |
| `v1.0.1` | Defectos DEF-01 a DEF-07 corregidos | 57 de 57 |
| `v2.0.0` | Refactorización y patrón Estrategia; se elimina `flag` | 88 de 88 |
| `v2.1.0` | Recargo de hora pico (CR-02) | 103 de 103 |

El detalle de cada versión está en [CHANGELOG.md](CHANGELOG.md).

## Estructura

| Ruta | Qué es |
|------|--------|
| `envios.py` | Cálculo del costo del envío |
| `tests/test_caja_negra.py` | 42 casos: particiones, valores límite y tabla de decisión |
| `tests/test_caja_blanca.py` | 15 casos: un camino independiente cada uno |
| `tests/test_unidades.py` | 31 pruebas de las funciones extraídas y las estrategias |
| `tests/test_hora_pico.py` | 15 pruebas de la solicitud de cambio |
| `docs/evidencias/` | Salidas de consola de pytest, cobertura, radon y Git |
| `docs/img/` | Capturas, grafo de flujo y diagrama UML |
| `tools/` | Scripts que dibujan los diagramas y arman el PDF |
| `.github/workflows/pruebas.yml` | Ejecuta la suite en cada push |

## Uso

```python
from envios import calcular_costo

calcular_costo(4, "rural", "vip", 6, "ENVIO10")       # 10400
calcular_costo(5, "rural", "normal", 1, hora=18)      # 11700 (hora pico)
```

## Cómo ejecutar

Instalar las herramientas:

```bash
python -m pip install -r requirements-dev.txt
```

Ejecutar las pruebas con cobertura de sentencias y de ramas:

```bash
python -m pytest --cov=envios --cov-branch --cov-report=term-missing
```

Medir la complejidad ciclomática:

```bash
python -m radon cc -s -a envios.py
```

Volver a generar el informe en PDF (requiere Edge o Chrome):

```bash
python tools/generar_informe.py
```
