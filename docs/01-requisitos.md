# Parte 1 - Requisitos y criterios de aceptación

## 1.1 Mis parámetros

Código estudiantil **0182310065**. Últimos seis dígitos: **3 1 0 0 6 5**.

| A | B | C | D | E | F | PMAX | L1 | L2 | RR | RN | V | S | CAMBIO |
|---|---|---|---|---|---|------|----|----|----|----|---|---|--------|
| 3 | 1 | 0 | 0 | 6 | 5 | 45 kg | 3 kg | 10 kg | 20 % | 50 % | 10 % | $2.000 | 2 |

Cómo sale cada valor:

| Parámetro | Fórmula | Cálculo | Valor |
|-----------|---------|---------|-------|
| PMAX | 30 + 5·A | 30 + 5·3 | **45 kg** |
| L1 | 2 + (B mod 3) | 2 + (1 mod 3) = 2 + 1 | **3 kg** |
| L2 | 10 + C | 10 + 0 | **10 kg** |
| RR | 10 + 5·(E mod 4) | 10 + 5·(6 mod 4) = 10 + 5·2 | **20 %** |
| RN | 40 + 5·(F mod 3) | 40 + 5·(5 mod 3) = 40 + 5·2 | **50 %** |
| V | 10 + 5·(A mod 3) | 10 + 5·(3 mod 3) = 10 + 0 | **10 %** |
| S | 2000 + 500·(C mod 4) | 2000 + 500·0 | **$2.000** |
| CAMBIO | (A + F) mod 3 | (3 + 5) mod 3 = 8 mod 3 | **2 - hora pico** |

Reglas que dependen de la paridad:

| Dígito | Valor | Paridad | Regla que me corresponde |
|--------|-------|---------|--------------------------|
| D - tramo 1 | 0 | par | El tramo 1 **incluye** el límite: peso ≤ 3 kg |
| E - recargo de fin de semana | 6 | par | Se suma **antes** de los descuentos |
| B - cliente y cupón | 1 | impar | Se aplican **ambos**: primero el del cliente y luego el cupón |
| F - cupón que no existe | 5 | impar | **Es error** |

## 1.2 Especificación completa (R1 a R8 con mis valores)

La función recibe: `peso` en kg (puede tener decimales); `zona` (urbana, rural
o nacional); `cliente` (normal, frecuente o vip); `dia` de 1 a 7, donde 6 es
sábado y 7 es domingo; y `cupon`, que es opcional.

| ID | Regla |
|----|-------|
| **R1** | El peso debe cumplir **0 < peso ≤ 45**. Si no, se lanza el error `"peso inválido"`. |
| **R2** | Si la zona no es `urbana`, `rural` o `nacional`, o el día no está entre 1 y 7, se lanza un error. |
| **R3** | Tarifa base. Tramo 1 (**peso ≤ 3 kg**): $6.000. Tramo 2 (3 < peso ≤ 10 kg): $9.000. Más de 10 kg: $9.000 + $800 por cada kg sobre 10, de forma proporcional. |
| **R4** | Recargo por zona. Rural: **+20 %**. Nacional: **+50 %**. Urbana: sin recargo. |
| **R5** | Fin de semana (día 6 o 7): **+$2.000**, que se suma **antes** de aplicar los descuentos. |
| **R6** | Descuento de cliente. Frecuente: 5 %. VIP: **10 %**. Cupón `ENVIO10`: 10 %. Si hay los dos, **se aplican ambos**: primero el del cliente y luego el cupón, cada uno sobre el valor que deja el anterior. |
| **R7** | Un cupón que no existe **es error**. |
| **R8** | El costo nunca es menor que $5.000. El resultado se redondea al múltiplo de $100 más cercano; los $50 redondean hacia arriba. |

Orden del cálculo que resulta de mis reglas:

1. Validar peso, zona, día y cupón (R1, R2, R7).
2. Tarifa base según el tramo (R3).
3. Recargo por zona (R4).
4. Recargo de fin de semana (R5).
5. Descuento del cliente y después el del cupón (R6).
6. Costo mínimo y redondeo a $100 (R8).

Supuesto: la especificación no dice qué pasa si el tipo de cliente no es uno
de los tres válidos. No lo traté como error porque ninguna regla lo pide; un
cliente desconocido se cobra sin descuento, igual que en el código heredado.
Queda como pregunta abierta para el dueño del producto.

## 1.3 Historias de usuario

### HU-01 - Validar los datos del envío (R1, R2)

> **Como** operador de mostrador de EnvíaYa, **quiero** que el sistema rechace
> los envíos con peso, zona o día que no son válidos, **para** no cobrar ni
> despachar envíos que la empresa no puede atender.

Criterios de aceptación:

- **CA-01.1** **Dado** un envío de 45 kg a zona urbana un lunes, **cuando**
  calculo el costo, **entonces** el sistema lo acepta y devuelve $37.000.
- **CA-01.2** **Dado** un envío de 45,01 kg, **cuando** calculo el costo,
  **entonces** el sistema lanza el error "peso inválido".
- **CA-01.3** **Dado** un envío de 0 kg o de peso negativo, **cuando** calculo
  el costo, **entonces** el sistema lanza el error "peso inválido".
- **CA-01.4** **Dado** un envío a la zona "internacional", **cuando** calculo
  el costo, **entonces** el sistema lanza un error y no devuelve ningún valor.
- **CA-01.5** **Dado** un envío con día 0 o día 8, **cuando** calculo el costo,
  **entonces** el sistema lanza un error.

### HU-02 - Cobrar según el peso y la zona (R3, R4, R8)

> **Como** cliente de EnvíaYa, **quiero** que el costo dependa del peso del
> paquete y de la zona de destino, **para** pagar un valor justo y saber de
> antemano cuánto cuesta mi envío.

Criterios de aceptación:

- **CA-02.1** **Dado** un paquete de 3 kg a zona urbana un lunes, **cuando**
  calculo el costo, **entonces** se cobra el tramo 1: $6.000.
- **CA-02.2** **Dado** un paquete de 3,01 kg a zona urbana un lunes,
  **cuando** calculo el costo, **entonces** se cobra el tramo 2: $9.000.
- **CA-02.3** **Dado** un paquete de 20 kg a zona urbana un lunes, **cuando**
  calculo el costo, **entonces** se cobra $9.000 + 10 × $800 = $17.000.
- **CA-02.4** **Dado** un paquete de 5 kg, **cuando** va a zona rural,
  **entonces** cuesta $10.800 (+20 %); y **cuando** va a zona nacional,
  **entonces** cuesta $13.500 (+50 %).
- **CA-02.5** **Dado** un envío cuyo cálculo da $4.860, **cuando** se entrega
  el resultado, **entonces** se cobra el mínimo de $5.000.
- **CA-02.6** **Dado** un envío cuyo cálculo da $8.550, **cuando** se entrega
  el resultado, **entonces** se redondea hacia arriba a $8.600.

### HU-03 - Aplicar el recargo de fin de semana y los descuentos (R5, R6, R7)

> **Como** gerente comercial de EnvíaYa, **quiero** que se cobre el recargo de
> fin de semana y que se apliquen los descuentos de cliente y de cupón,
> **para** cubrir el costo de operar sábados y domingos y premiar a los
> clientes fieles sin regalar descuentos que no existen.

Criterios de aceptación:

- **CA-03.1** **Dado** un envío de 5 kg urbano de un cliente normal,
  **cuando** se hace un sábado o un domingo, **entonces** cuesta $11.000
  ($9.000 + $2.000).
- **CA-03.2** **Dado** un envío de 5 kg urbano de un cliente VIP un domingo,
  **cuando** calculo el costo, **entonces** el recargo se suma antes del
  descuento: ($9.000 + $2.000) × 0,90 = $9.900.
- **CA-03.3** **Dado** un cliente VIP con el cupón ENVIO10 y un envío de 5 kg
  urbano un lunes, **cuando** calculo el costo, **entonces** se aplican los
  dos descuentos: $9.000 × 0,90 × 0,90 = $7.290, que se redondea a $7.300.
- **CA-03.4** **Dado** un cliente frecuente sin cupón y un envío de 5 kg
  urbano un lunes, **cuando** calculo el costo, **entonces** se descuenta el
  5 %: $8.550, que se redondea a $8.600.
- **CA-03.5** **Dado** un envío con el cupón "NOEXISTE", **cuando** calculo el
  costo, **entonces** el sistema lanza un error.

## 1.4 Matriz de trazabilidad

Los casos `CN-xx` son de caja negra (Parte 3) y los `CB-xx` de caja blanca
(Parte 4). La última fila (R9, casos `HP-xx`) se agregó con la solicitud de
cambio de la Parte 8.

| Requisito | Historia | Criterios | Casos de prueba |
|-----------|----------|-----------|-----------------|
| R1 peso válido | HU-01 | CA-01.1, CA-01.2, CA-01.3 | CN-01, CN-02, CN-03, CN-12, CN-13, CN-14, CN-42, CB-01, CB-02 |
| R2 zona y día válidos | HU-01 | CA-01.4, CA-01.5 | CN-17, CN-18, CN-19, CN-23, CB-08 |
| R3 tarifa base | HU-02 | CA-02.1, CA-02.2, CA-02.3 | CN-03 a CN-12, CB-03, CB-04, CB-05 |
| R4 recargo por zona | HU-02 | CA-02.4 | CN-15, CN-16, CN-38, CN-39, CN-40, CN-41, CB-06, CB-07 |
| R5 fin de semana | HU-03 | CA-03.1, CA-03.2 | CN-20, CN-21, CN-22, CN-29 a CN-33, CN-38, CN-39, CN-41, CB-09 |
| R6 descuentos | HU-03 | CA-03.3, CA-03.4 | CN-24 a CN-33, CN-37, CN-38, CN-40, CB-10, CB-11, CB-12 |
| R7 cupón inexistente | HU-03 | CA-03.5 | CN-34, CN-35, CB-13 |
| R8 mínimo y redondeo | HU-02 | CA-02.5, CA-02.6 | CN-09, CN-11, CN-25, CN-26, CN-28, CN-30, CN-31, CN-36, CN-37, CB-14 |
| R9 hora pico (Parte 8) | HU-04 | CA-04.1 a CA-04.5 | HP-01 a HP-15 |
