# Parcial 3 - Ingeniería de Software I

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

## Contenido

| Ruta | Qué es |
|------|--------|
| `envios.py` | Cálculo del costo (versión 2.1.0) |
| `tests/` | 103 pruebas con pytest: caja negra, caja blanca, unidad y hora pico |
| `docs/01` a `docs/08` | Las ocho partes del informe |
| `docs/evidencias/` y `docs/img/` | Salidas de consola, capturas y diagramas |
| `Informe_Parcial3_0182310065.pdf` | Informe completo |
| `CHANGELOG.md` | Historial de versiones |
| `tools/` | Scripts que generan los diagramas y el PDF |

Versiones: `v1.0.0` (heredado), `v1.0.1` (defectos corregidos), `v2.0.0`
(refactorización) y `v2.1.0` (hora pico).

## Cómo ejecutar

```bash
python -m pip install -r requirements-dev.txt
```

```bash
python -m pytest --cov=envios --cov-branch --cov-report=term-missing
```
