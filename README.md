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

| Archivo | Qué es |
|---------|--------|
| `envios.py` | Código heredado (v1.0.0) con mi `CONFIG` |

## Cómo ejecutar

```bash
python -m pip install -r requirements-dev.txt
```

```bash
python -m pytest
```
