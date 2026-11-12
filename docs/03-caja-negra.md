# Parte 3 - Diseño de casos de caja negra

Todos los resultados esperados salen de la especificación (Parte 1) con mis
valores: PMAX = 45, L1 = 3 (incluido), L2 = 10, rural +20 %, nacional +50 %,
VIP 10 %, fin de semana +$2.000 antes de los descuentos, ambos descuentos y
cupón inexistente = error.

## 3.1 Particiones de equivalencia

### Peso (kg)

| Clase | Tipo | Rango | Representante | Resultado |
|-------|------|-------|---------------|-----------|
| P1 | Inválida | peso ≤ 0 | −1 | Error "peso inválido" |
| P2 | Válida | 0 < peso ≤ 3 (tramo 1) | 2 | Base $6.000 |
| P3 | Válida | 3 < peso ≤ 10 (tramo 2) | 5 | Base $9.000 |
| P4 | Válida | 10 < peso ≤ 45 (tramo 3) | 20 | Base $9.000 + $800 × (peso − 10) |
| P5 | Inválida | peso > 45 | 50 | Error "peso inválido" |

### Zona

| Clase | Tipo | Valor | Resultado |
|-------|------|-------|-----------|
| Z1 | Válida | `urbana` | Sin recargo |
| Z2 | Válida | `rural` | +20 % |
| Z3 | Válida | `nacional` | +50 % |
| Z4 | Inválida | cualquier otro texto (`internacional`) | Error |

### Cliente

| Clase | Tipo | Valor | Resultado |
|-------|------|-------|-----------|
| C1 | Válida | `normal` | Sin descuento |
| C2 | Válida | `frecuente` | −5 % |
| C3 | Válida | `vip` | −10 % |
| C4 | No definida | otro texto | La especificación no lo define (ver supuesto de la Parte 1); no se diseñó caso con resultado esperado. |

### Día

| Clase | Tipo | Rango | Representante | Resultado |
|-------|------|-------|---------------|-----------|
| D1 | Inválida | día < 1 | 0 | Error |
| D2 | Válida | 1 a 5 (día hábil) | 1 y 5 | Sin recargo |
| D3 | Válida | 6 y 7 (fin de semana) | 6 y 7 | +$2.000 |
| D4 | Inválida | día > 7 | 8 | Error |

### Cupón

| Clase | Tipo | Valor | Resultado |
|-------|------|-------|-----------|
| K1 | Válida | sin cupón | Sin descuento de cupón |
| K2 | Válida | `ENVIO10` | −10 % |
| K3 | Inválida | cupón que no existe (`NOEXISTE`, `envio10`) | Error (F = 5 es impar) |

## 3.2 Valores límite del peso

Con zona urbana, cliente normal, lunes y sin cupón, para que el costo dependa
solo del peso. Se usa un paso de 0,01 kg.

| Frontera | Valor | Clase | Esperado | Caso |
|----------|-------|-------|----------|------|
| 0 | 0 | P1 (inválida) | Error | CN-02 |
| 0 | 0,01 | P2 | $6.000 | CN-03 |
| L1 = 3 | 2,99 | P2 | $6.000 | CN-04 |
| L1 = 3 | **3** | P2 - **el límite está incluido porque D = 0 es par** | $6.000 | CN-05 |
| L1 = 3 | 3,01 | P3 | $9.000 | CN-06 |
| L2 = 10 | 9,99 | P3 | $9.000 | CN-07 |
| L2 = 10 | 10 | P3 (incluido) | $9.000 | CN-08 |
| L2 = 10 | 10,01 | P4 | $9.008 → $9.000 | CN-09 |
| PMAX = 45 | 44,99 | P4 | $36.992 → $37.000 | CN-11 |
| PMAX = 45 | 45 | P4 (incluido) | $37.000 | CN-12 |
| PMAX = 45 | 45,01 | P5 (inválida) | Error | CN-13 |

También se prueban los límites del día: 0 (error), 1, 5, 6, 7 y 8 (error) en
los casos CN-18 a CN-23.

## 3.3 Tabla de decisión: cliente × cupón × fin de semana

Base de todos los casos: 5 kg, zona urbana → **$9.000**. "Fin de semana = sí"
usa el domingo (día 7).

Por mis reglas, cuando es fin de semana los $2.000 se suman **antes** de los
descuentos (E par), y cuando hay descuento de cliente y cupón se aplican
**los dos**, primero cliente y luego cupón (B impar).

| Regla | Cliente | Cupón | Fin de semana | +$2.000 antes | Desc. cliente | Desc. cupón | Cálculo | Esperado | Caso |
|-------|---------|-------|---------------|---------------|---------------|-------------|---------|----------|------|
| 1 | normal | no | no | - | - | - | 9.000 | **$9.000** | CN-19 |
| 2 | normal | no | sí | X | - | - | 9.000 + 2.000 | **$11.000** | CN-22 |
| 3 | normal | ENVIO10 | no | - | - | 10 % | 9.000 × 0,90 | **$8.100** | CN-24 |
| 4 | normal | ENVIO10 | sí | X | - | 10 % | 11.000 × 0,90 | **$9.900** | CN-29 |
| 5 | frecuente | no | no | - | 5 % | - | 9.000 × 0,95 = 8.550 | **$8.600** | CN-25 |
| 6 | frecuente | no | sí | X | 5 % | - | 11.000 × 0,95 = 10.450 | **$10.500** | CN-30 |
| 7 | frecuente | ENVIO10 | no | - | 5 % | 10 % | 8.550 × 0,90 = 7.695 | **$7.700** | CN-26 |
| 8 | frecuente | ENVIO10 | sí | X | 5 % | 10 % | 10.450 × 0,90 = 9.405 | **$9.400** | CN-31 |
| 9 | vip | no | no | - | 10 % | - | 9.000 × 0,90 | **$8.100** | CN-27 |
| 10 | vip | no | sí | X | 10 % | - | 11.000 × 0,90 | **$9.900** | CN-32 |
| 11 | vip | ENVIO10 | no | - | 10 % | 10 % | 8.100 × 0,90 = 7.290 | **$7.300** | CN-28 |
| 12 | vip | ENVIO10 | sí | X | 10 % | 10 % | 9.900 × 0,90 = 8.910 | **$8.900** | CN-33 |
| 13 | cualquiera | no existe | cualquiera | - | - | - | - | **Error** | CN-34, CN-35 |

Por qué esta tabla distingue mis reglas de las de otro compañero:

- **Regla E.** En la regla 10, si el recargo fuera *después* de los
  descuentos, el resultado sería 9.000 × 0,90 + 2.000 = $10.100 y no $9.900.
- **Regla B.** En la regla 11, si solo se aplicara el *mayor* descuento, el
  resultado sería $8.100 y no $7.300.
- **Regla F.** En la regla 13, si el cupón inexistente se *ignorara*, el
  resultado sería un costo y no un error.

## 3.4 Matriz de casos de prueba

Técnicas: **PE** = partición de equivalencia, **VL** = valor límite,
**TD** = tabla de decisión, **CE** = combinación de reglas (caso de extremo
a extremo). Días: 1 = lunes, 5 = viernes, 6 = sábado, 7 = domingo.

| ID | Requisito | Peso | Zona | Cliente | Día | Cupón | Resultado esperado | Técnica |
|----|-----------|------|------|---------|-----|-------|--------------------|---------|
| CN-01 | R1 | −1 | urbana | normal | 1 | - | Error | PE (P1) |
| CN-02 | R1 | 0 | urbana | normal | 1 | - | Error | VL (0) |
| CN-03 | R1, R3 | 0,01 | urbana | normal | 1 | - | $6.000 | VL (0) |
| CN-04 | R3 | 2,99 | urbana | normal | 1 | - | $6.000 | VL (L1) |
| CN-05 | R3 | 3 | urbana | normal | 1 | - | $6.000 | VL (L1 incluido) |
| CN-06 | R3 | 3,01 | urbana | normal | 1 | - | $9.000 | VL (L1) |
| CN-07 | R3 | 9,99 | urbana | normal | 1 | - | $9.000 | VL (L2) |
| CN-08 | R3 | 10 | urbana | normal | 1 | - | $9.000 | VL (L2) |
| CN-09 | R3, R8 | 10,01 | urbana | normal | 1 | - | $9.000 | VL (L2) |
| CN-10 | R3 | 20 | urbana | normal | 1 | - | $17.000 | PE (P4) |
| CN-11 | R3, R8 | 44,99 | urbana | normal | 1 | - | $37.000 | VL (PMAX) |
| CN-12 | R1, R3 | 45 | urbana | normal | 1 | - | $37.000 | VL (PMAX) |
| CN-13 | R1 | 45,01 | urbana | normal | 1 | - | Error | VL (PMAX) |
| CN-14 | R1 | 50 | urbana | normal | 1 | - | Error | PE (P5) |
| CN-15 | R4 | 5 | rural | normal | 1 | - | $10.800 | PE (Z2) |
| CN-16 | R4 | 5 | nacional | normal | 1 | - | $13.500 | PE (Z3) |
| CN-17 | R2 | 5 | internacional | normal | 1 | - | Error | PE (Z4) |
| CN-18 | R2 | 5 | urbana | normal | 0 | - | Error | VL (día) |
| CN-19 | R2, R5 | 5 | urbana | normal | 1 | - | $9.000 | VL (día), TD-1 |
| CN-20 | R5 | 5 | urbana | normal | 5 | - | $9.000 | VL (día) |
| CN-21 | R5 | 5 | urbana | normal | 6 | - | $11.000 | VL (día) |
| CN-22 | R5 | 5 | urbana | normal | 7 | - | $11.000 | VL (día), TD-2 |
| CN-23 | R2 | 5 | urbana | normal | 8 | - | Error | VL (día) |
| CN-24 | R6 | 5 | urbana | normal | 1 | ENVIO10 | $8.100 | TD-3 |
| CN-25 | R6, R8 | 5 | urbana | frecuente | 1 | - | $8.600 | TD-5 |
| CN-26 | R6, R8 | 5 | urbana | frecuente | 1 | ENVIO10 | $7.700 | TD-7 |
| CN-27 | R6 | 5 | urbana | vip | 1 | - | $8.100 | TD-9 |
| CN-28 | R6, R8 | 5 | urbana | vip | 1 | ENVIO10 | $7.300 | TD-11 |
| CN-29 | R5, R6 | 5 | urbana | normal | 7 | ENVIO10 | $9.900 | TD-4 |
| CN-30 | R5, R6, R8 | 5 | urbana | frecuente | 7 | - | $10.500 | TD-6 |
| CN-31 | R5, R6, R8 | 5 | urbana | frecuente | 7 | ENVIO10 | $9.400 | TD-8 |
| CN-32 | R5, R6 | 5 | urbana | vip | 7 | - | $9.900 | TD-10 |
| CN-33 | R5, R6, R8 | 5 | urbana | vip | 7 | ENVIO10 | $8.900 | TD-12 |
| CN-34 | R7 | 5 | urbana | normal | 1 | NOEXISTE | Error | TD-13, PE (K3) |
| CN-35 | R7 | 5 | urbana | vip | 7 | envio10 | Error | TD-13, PE (K3) |
| CN-36 | R8 | 2 | urbana | vip | 1 | ENVIO10 | $5.000 | VL (costo mínimo) |
| CN-37 | R6, R8 | 2 | urbana | frecuente | 1 | ENVIO10 | $5.100 | VL (costo mínimo) |
| CN-38 | R3 a R8 | 4 | rural | vip | 6 | ENVIO10 | $10.400 | CE |
| CN-39 | R3 a R8 | 12,5 | nacional | vip | 6 | ENVIO10 | $15.000 | CE |
| CN-40 | R3 a R8 | 45 | nacional | frecuente | 7 | - | $54.600 | CE |
| CN-41 | R3 a R8 | 3 | rural | frecuente | 6 | - | $8.700 | CE |
| CN-42 | R1 | 0 | urbana | normal | 1 | - | Mensaje exacto "peso inválido" | PE (P1) |

Son **42 casos**. Están automatizados en `tests/test_caja_negra.py` con el
mismo ID.

## 3.5 Cálculo paso a paso

### CN-38 - el ejemplo del enunciado con mis valores

Entradas: peso = 4 kg · zona = rural · cliente = vip · día = 6 (sábado) ·
cupón = ENVIO10

1. Tramo: D = 0 es par, el tramo 1 es peso ≤ 3. Como 4 no es ≤ 3 y sí es
   ≤ 10, va al tramo 2 → **$9.000**
2. Zona rural +20 % → 9.000 × 1,20 = **$10.800**
3. Sábado, y E = 6 es par: el recargo va antes de los descuentos →
   10.800 + 2.000 = **$12.800**
4. B = 1 es impar: se aplican ambos. Primero VIP 10 % → 12.800 × 0,90 =
   **$11.520**; luego cupón 10 % → 11.520 × 0,90 = **$10.368**
5. Es mayor que $5.000. Se redondea a $100: 10.368 está más cerca de 10.400
   → resultado esperado: **$10.400**

### CN-39 - tramo 3 con decimales, zona nacional

Entradas: peso = 12,5 kg · zona = nacional · cliente = vip · día = 6 ·
cupón = ENVIO10

1. Tramo 3 (12,5 > 10): 9.000 + (12,5 − 10) × 800 = 9.000 + 2.000 =
   **$11.000**
2. Zona nacional +50 % → 11.000 × 1,50 = **$16.500**
3. Sábado, antes de los descuentos → 16.500 + 2.000 = **$18.500**
4. VIP 10 % → 18.500 × 0,90 = **$16.650**; cupón 10 % → 16.650 × 0,90 =
   **$14.985**
5. Mayor que $5.000. Redondeo: 14.985 → resultado esperado: **$15.000**

### CN-40 - peso máximo, cliente frecuente, domingo

Entradas: peso = 45 kg · zona = nacional · cliente = frecuente · día = 7 ·
sin cupón

1. Peso válido (45 ≤ 45). Tramo 3: 9.000 + (45 − 10) × 800 = 9.000 + 28.000
   = **$37.000**
2. Zona nacional +50 % → 37.000 × 1,50 = **$55.500**
3. Domingo, antes de los descuentos → 55.500 + 2.000 = **$57.500**
4. Frecuente 5 % → 57.500 × 0,95 = **$54.625**. No hay cupón.
5. Redondeo: 54.625 está más cerca de 54.600 que de 54.700 → resultado
   esperado: **$54.600**

### CN-41 - justo en el límite L1, sábado

Entradas: peso = 3 kg · zona = rural · cliente = frecuente · día = 6 ·
sin cupón

1. Tramo: 3 ≤ 3, y el límite está incluido (D par) → tramo 1: **$6.000**
2. Zona rural +20 % → 6.000 × 1,20 = **$7.200**
3. Sábado, antes de los descuentos → 7.200 + 2.000 = **$9.200**
4. Frecuente 5 % → 9.200 × 0,95 = **$8.740**
5. Redondeo: 8.740 → resultado esperado: **$8.700**

### CN-36 - costo mínimo

Entradas: peso = 2 kg · zona = urbana · cliente = vip · día = 1 (lunes) ·
cupón = ENVIO10

1. Tramo 1 (2 ≤ 3) → **$6.000**
2. Zona urbana: sin recargo → **$6.000**
3. Lunes: sin recargo de fin de semana.
4. VIP 10 % → 6.000 × 0,90 = **$5.400**; cupón 10 % → 5.400 × 0,90 =
   **$4.860**
5. 4.860 es menor que el mínimo → resultado esperado: **$5.000**

### CN-30 - redondeo de los $50 hacia arriba

Entradas: peso = 5 kg · zona = urbana · cliente = frecuente · día = 7
(domingo) · sin cupón

1. Tramo 2 → **$9.000**
2. Urbana: sin recargo.
3. Domingo, antes del descuento → 9.000 + 2.000 = **$11.000**
4. Frecuente 5 % → 11.000 × 0,95 = **$10.450**
5. Queda justo en $50: redondea hacia arriba → resultado esperado:
   **$10.500**

### CN-11 - justo debajo del peso máximo

Entradas: peso = 44,99 kg · zona = urbana · cliente = normal · día = 1 ·
sin cupón

1. Peso válido (44,99 ≤ 45). Tramo 3: 9.000 + (44,99 − 10) × 800 =
   9.000 + 34,99 × 800 = 9.000 + 27.992 = **$36.992**
2. Urbana, lunes, cliente normal, sin cupón: no cambia.
3. Redondeo: 36.992 está más cerca de 37.000 → resultado esperado:
   **$37.000**
