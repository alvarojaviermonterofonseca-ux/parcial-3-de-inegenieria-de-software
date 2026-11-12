# Parte 7 - Gestión de configuración

Repositorio:
<https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software>

## 7.1 Línea base: etiqueta v1.0.0

El primer commit de trabajo contiene el código heredado tal como se recibió,
con un único cambio: `CONFIG` lleno con mis valores. Ese commit lleva la
etiqueta anotada **`v1.0.0`** y es la línea base contra la que se ejecutaron
las pruebas de la Parte 5.

```bash
git tag -a v1.0.0 -m "v1.0.0 - código heredado sin modificar"
```

## 7.2 Ramas e integración

`main` siempre queda en un estado que se puede entregar. Cada trabajo se hizo
en su propia rama y se integró con `git merge --no-ff`, para que en el
historial quede visible qué commits pertenecen a cada rama.

| Rama | Para qué | Se integró en |
|------|----------|---------------|
| `test/suite` | Casos de caja negra y de caja blanca automatizados | `main` |
| `fix/DEF-04` | El sábado no cobraba recargo | `main` |
| `fix/DEF-06` | Truncaba en vez de redondear | `main` |
| `fix/DEF-01` | Aceptaba más de 45 kg | `main` |
| `fix/DEF-02` | Zona inexistente | `main` |
| `fix/DEF-03` | Día sin validar | `main` |
| `fix/DEF-05` | Cupón inexistente | `main` |
| `fix/DEF-07` | Mensaje de error | `main` |
| `refactor/estrategia` | Extracción de funciones, constantes y patrón Estrategia | `main` |
| `feature/hora-pico` | Solicitud de cambio CR-02 | `main` |

Reglas que seguí:

- Una rama por defecto, creada desde `main` actualizado. Las ramas `fix/` se
  hicieron en orden de **prioridad** del defecto, no en orden de número.
- Antes de integrar una rama se ejecutó toda la suite; solo se integró si no
  rompía ninguna prueba que ya pasaba.
- Mensajes de commit con prefijo según el tipo de cambio: `feat`, `fix`,
  `test`, `refactor`, `docs`, `chore`.

## 7.3 Versiones y justificación (versionado semántico)

En versionado semántico la versión es `MAJOR.MINOR.PATCH`: PATCH para
correcciones compatibles, MINOR para funcionalidad nueva compatible y MAJOR
cuando se rompe la interfaz pública.

| Etiqueta | Qué contiene | Tipo | Justificación |
|----------|--------------|------|---------------|
| `v1.0.0` | Código heredado | - | Línea base. |
| `v1.0.1` | Los 7 defectos corregidos | **PATCH** | Solo son correcciones para que el código cumpla la especificación. La firma `calc(p, z, c, d, cup=None, flag=False)` es exactamente la misma. |
| `v2.0.0` | Refactorización y patrón Estrategia | **MAJOR** | Se rompe la interfaz pública (ver abajo). |
| `v2.1.0` | Hora pico | **MINOR** | Funcionalidad nueva y compatible: `hora` es opcional. |

**¿Quitar `flag` hace que la versión sea major? Sí.**

La interfaz pública de este módulo es la firma de `calc` y lo que se puede
importar de `envios`. En la versión 2.0.0:

1. Se eliminó el parámetro `flag`. Un programa que llamaba
   `calc(5, "urbana", "normal", 1, None, True)` o `calc(..., flag=True)`
   funcionaba en 1.x y en 2.0.0 falla con `TypeError`. Eso es un cambio
   **incompatible hacia atrás**, y la regla 8 de SemVer dice que cualquier
   cambio incompatible en la API pública obliga a subir MAJOR, aunque el
   cambio sea pequeño o el parámetro casi no se usara.
2. Se cambiaron los nombres de los parámetros (`p` → `peso`, `z` → `zona`…):
   quien llamara con nombres (`calc(p=5, z="urbana", …)`) también se rompe.
3. Se eliminó el diccionario `CONFIG`: quien lo importara o lo modificara
   también se rompe.

Lo que **no** obliga a major: las llamadas posicionales normales
(`calc(5, "urbana", "normal", 1)`) siguen funcionando, porque `calc` se dejó
como alias de `calcular_costo`.

¿Y los defectos corregidos? Ahora se lanza error con entradas que antes
devolvían un valor (zona inexistente, día 8, cupón inexistente, peso de 46 a
50 kg). No lo conté como cambio incompatible porque la interfaz documentada
(la especificación R1 a R8) siempre dijo que eso era error: corregir el código
para que cumpla su contrato es PATCH.

## 7.4 CHANGELOG y notas de versión

El archivo [`CHANGELOG.md`](../CHANGELOG.md) sigue el formato *Keep a
Changelog*: una sección por versión, de la más nueva a la más vieja, con los
cambios agrupados en **Añadido**, **Cambiado**, **Eliminado** y
**Corregido**, y los enlaces de comparación al final.

### Notas de la versión 2.0.0

> **EnvíaYa - cálculo de costo de envíos 2.0.0** (11 de noviembre de 2026)
>
> Esta versión corrige el cobro y reorganiza el código por dentro.
>
> **Qué cambia para el negocio** (viene de 1.0.1)
>
> - Los sábados ya se cobra el recargo de fin de semana de $2.000.
> - El costo se redondea a los $100 más cercanos; antes siempre se redondeaba
>   hacia abajo.
> - Ya no se aceptan envíos de más de 45 kg, zonas que no existen, días fuera
>   de 1 a 7 ni cupones que no existen: el sistema avisa con un error.
>
> **Qué cambia para quien usa la función**
>
> - **Cambio incompatible:** desapareció el parámetro `flag`. Si necesita ver
>   el costo, imprima el valor que devuelve la función.
> - **Cambio incompatible:** desapareció `CONFIG`; use las constantes del
>   módulo.
> - La función se llama ahora `calcular_costo`; `calc` sigue funcionando.
>
> **Cómo actualizar**
>
> 1. Busque en su código `flag=` y llamadas a `calc` con seis argumentos, y
>    quite ese argumento.
> 2. Si usaba nombres de parámetro (`p=`, `z=`, `c=`, `d=`, `cup=`),
>    cámbielos por `peso=`, `zona=`, `cliente=`, `dia=`, `cupon=`.
>
> **Calidad:** 88 pruebas automatizadas, todas pasan; cobertura de sentencias
> y de ramas del 100 %.

### Notas de la versión 2.1.0

> **EnvíaYa - cálculo de costo de envíos 2.1.0** (11 de noviembre de 2026)
>
> **Novedad: recargo de hora pico.** Los envíos que se hacen entre las 17 y
> las 19 (inclusive) tienen un recargo del 8 %, calculado sobre el valor con
> recargo de zona.
>
> - Para usarlo, envíe la hora por nombre: `calcular_costo(5, "rural",
>   "normal", 1, hora=18)`.
> - Si no envía la hora, todo funciona igual que en la 2.0.0: **no hay que
>   cambiar nada para actualizar.**
> - Una hora fuera de 0 a 23 produce el error "hora inválida".
>
> **Calidad:** 103 pruebas automatizadas, todas pasan; cobertura del 100 %.

## 7.5 Salida de `git log --oneline --graph --all`

```text
*   8f2d3d1 merge: integra feature/hora-pico (CR-02)
|\  
| * 021fee4 feat: recargo de hora pico del 8 % entre las 17 y las 19 (CR-02)
| * eb1d526 test: pruebas de hora pico escritas primero (CR-02, fallan)
|/  
* 2091e45 docs: Parte 6, CHANGELOG y evidencias de la versión 2.0.0
*   b345a69 merge: integra refactor/estrategia
|\  
| * 9eaa0b6 refactor: patrón Estrategia para el recargo por zona
| * f044c12 refactor: extrae funciones, nombra las constantes y elimina flag
* | fd2e4bc docs: CHANGELOG y evidencias de regresión de la versión 1.0.1
* | 1c48d51 merge: integra fix/DEF-07
|\| 
| * 059f836 fix(DEF-07): el mensaje de error dice "peso inválido"
* | 98f7092 merge: integra fix/DEF-05
|\| 
| * 23cbbf9 fix(DEF-05): un cupón que no existe lanza error
* | 26e24b7 merge: integra fix/DEF-03
|\| 
| * bfc34e9 fix(DEF-03): valida que el día esté entre 1 y 7
* | e6413ae merge: integra fix/DEF-02
|\| 
| * 91e9476 fix(DEF-02): una zona que no existe lanza error
|/  
* 73744a4 docs: captura del reporte de pytest fallando contra v1.0.0 (Parte 5)
*   5f89973 merge: integra fix/DEF-01
|\  
| * 3da56cb fix(DEF-01): rechaza envíos de más de 45 kg
|/  
* a9de32d docs: capturas del reporte HTML de cobertura sobre v1.0.0 (Parte 5)
*   9f738b1 merge: integra fix/DEF-06
|\  
| * 99de1d2 fix(DEF-06): redondea al múltiplo de $100 más cercano
|/  
*   bc7f806 merge: integra fix/DEF-04
|\  
| * 7182ef7 fix(DEF-04): el sábado cobra el recargo de fin de semana
|/  
* 5dd9bec docs: reporte de 7 defectos, cobertura y métricas contra v1.0.0 (Parte 5)
*   0b41a3d merge: integra test/suite (casos de caja negra y caja blanca)
|\  
| * 2573229 test: 15 caminos independientes de caja blanca y grafo de flujo (Parte 4)
| * b9760bb test: 42 casos de caja negra con pytest (Parte 3)
|/  
* 3399948 docs: plan de pruebas con niveles, estrategia, riesgos y criterios (Parte 2)
* e7ef91e docs: especificación R1-R8, historias de usuario y trazabilidad (Parte 1)
* 05a7957 feat: código heredado de EnvíaYa con mi CONFIG (v1.0.0)
* 5293245 Initial commit
```

## 7.6 Distribución de los commits en el tiempo

Fecha y hora de cada commit (`git log --date=format:'%H:%M' --format='%ad %s'`):

```text
18:59 Initial commit
19:44 feat: código heredado de EnvíaYa con mi CONFIG (v1.0.0)
19:47 docs: especificación R1-R8, historias de usuario y trazabilidad (Parte 1)
19:56 docs: plan de pruebas con niveles, estrategia, riesgos y criterios (Parte 2)
20:07 test: 42 casos de caja negra con pytest (Parte 3)
20:17 test: 15 caminos independientes de caja blanca y grafo de flujo (Parte 4)
20:26 merge: integra test/suite (casos de caja negra y caja blanca)
20:36 docs: reporte de 7 defectos, cobertura y métricas contra v1.0.0 (Parte 5)
20:46 fix(DEF-04): el sábado cobra el recargo de fin de semana
20:46 merge: integra fix/DEF-04
20:56 fix(DEF-06): redondea al múltiplo de $100 más cercano
20:56 merge: integra fix/DEF-06
21:01 docs: capturas del reporte HTML de cobertura sobre v1.0.0 (Parte 5)
21:06 fix(DEF-01): rechaza envíos de más de 45 kg
21:06 merge: integra fix/DEF-01
21:08 docs: captura del reporte de pytest fallando contra v1.0.0 (Parte 5)
21:17 fix(DEF-02): una zona que no existe lanza error
21:27 fix(DEF-03): valida que el día esté entre 1 y 7
21:36 fix(DEF-05): un cupón que no existe lanza error
21:44 fix(DEF-07): el mensaje de error dice "peso inválido"
21:57 refactor: extrae funciones, nombra las constantes y elimina flag
22:09 merge: integra fix/DEF-02
22:09 merge: integra fix/DEF-03
22:09 refactor: patrón Estrategia para el recargo por zona
22:09 merge: integra fix/DEF-05
22:09 merge: integra fix/DEF-07
22:09 docs: CHANGELOG y evidencias de regresión de la versión 1.0.1
22:09 merge: integra refactor/estrategia
22:09 docs: Parte 6, CHANGELOG y evidencias de la versión 2.0.0
22:09 test: pruebas de hora pico escritas primero (CR-02, fallan)
22:09 feat: recargo de hora pico del 8 % entre las 17 y las 19 (CR-02)
22:09 merge: integra feature/hora-pico (CR-02)
```
