# Parte 2 - Plan de pruebas

## 2.1 Alcance

**Objeto de prueba:** la función `calc` del módulo `envios.py` de EnvíaYa,
versión heredada 1.0.0 y las versiones que salgan del mantenimiento.

**Dentro del alcance**

- Las ocho reglas de negocio R1 a R8 con los valores del código 0182310065.
- Validación de entradas: peso, zona, día y cupón.
- Cálculo completo: tarifa base, recargo de zona, recargo de fin de semana,
  descuentos, costo mínimo y redondeo.
- Pruebas de regresión después de cada corrección y de la refactorización.
- El cambio de la Parte 8 (hora pico).

**Fuera del alcance**

- Interfaz gráfica, base de datos, facturación y cualquier otro módulo del
  sistema: solo se entregó la función de cálculo.
- Pruebas de rendimiento, carga y seguridad: la función es un cálculo en
  memoria sin entrada ni salida.
- Tipos de dato no numéricos en el peso o el día (por ejemplo, texto): la
  especificación no los define.

## 2.2 Niveles de prueba aplicados al caso

| Nivel | Qué se prueba aquí | Cómo se hace | Quién |
|-------|--------------------|--------------|-------|
| **Unidad** | La función `calc` aislada y, después de refactorizar, cada función extraída: validación, tarifa base, estrategia de zona, descuentos y redondeo. | pytest con casos de caja negra (`tests/test_caja_negra.py`) y de caja blanca (`tests/test_caja_blanca.py`); cobertura con pytest-cov. | Desarrollador / tester |
| **Integración** | Que las piezas trabajen juntas en el orden correcto: tarifa → zona → fin de semana → descuentos → mínimo → redondeo. Tras la refactorización, que `calc` combine bien las estrategias de zona con las funciones de descuento. | Los casos combinados CN-38 a CN-41 recorren todas las reglas en una sola llamada. La integración es ascendente: primero las funciones pequeñas, luego `calc`. | Tester |
| **Sistema** | El módulo completo, visto como lo usaría el sistema de mostrador: se llama a `calc` con datos de envíos reales y se compara con la tarifa oficial. | Ejecución de toda la suite desde la línea de comandos (`python -m pytest`) en un ambiente limpio, sobre la versión etiquetada. | Tester |
| **Aceptación** | Que el cálculo cumple lo que el negocio pidió. | Los criterios Dado / Cuando / Entonces de las historias HU-01 a HU-03 se revisan con el dueño del producto; cada criterio tiene al menos un caso automatizado en la matriz de trazabilidad. | Dueño del producto (gerente comercial) con apoyo del tester |

## 2.3 Estrategia

1. **Pruebas basadas en la especificación (caja negra):** particiones de
   equivalencia, valores límite y tabla de decisión. Los resultados esperados
   se calculan a mano con la especificación, nunca ejecutando el código.
2. **Pruebas basadas en la estructura (caja blanca):** grafo de flujo,
   complejidad ciclomática y caminos independientes para asegurar cobertura de
   sentencias y de ramas.
3. **Automatización:** todos los casos se escriben en pytest para poder
   repetirlos sin costo.
4. **Primero contra el código heredado:** la suite se ejecuta contra la
   versión 1.0.0 sin tocarla; cada fallo se analiza y se registra como
   defecto.
5. **Regresión:** después de cada corrección (`fix/DEF-xx`) y de la
   refactorización se ejecuta de nuevo la suite completa. Ninguna rama se
   integra a `main` si rompe una prueba que antes pasaba.
6. **Pruebas primero en los cambios:** para la solicitud de cambio se escribe
   la prueba, se ve fallar y luego se implementa.

## 2.4 Ambiente

| Elemento | Valor |
|----------|-------|
| Sistema operativo | Windows 11 |
| Lenguaje | Python 3.14 |
| Marco de pruebas | pytest 9 |
| Cobertura | pytest-cov (coverage.py), con cobertura de ramas |
| Complejidad | radon |
| Control de versiones | Git y GitHub |
| Datos de prueba | Valores escritos en los propios casos; no hay base de datos |

Comando de ejecución:

```bash
python -m pytest --cov=envios --cov-branch --cov-report=term-missing
```

## 2.5 Roles

El trabajo es individual, así que una sola persona cumple todos los roles:

| Rol | Responsabilidad |
|-----|-----------------|
| Analista de pruebas | Escribe la especificación, las historias y diseña los casos. |
| Tester / automatizador | Programa los casos en pytest, los ejecuta y reporta los defectos. |
| Desarrollador de mantenimiento | Corrige los defectos y refactoriza. |
| Gestor de configuración | Maneja ramas, etiquetas, versiones y el CHANGELOG. |
| Dueño del producto (docente) | Aclara dudas de la especificación y acepta la entrega. |

## 2.6 Riesgos y mitigación

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|--------|-------|---------|------------|
| 1 | Calcular mal un resultado esperado a mano y reportar un defecto que no existe. | Media | Alto | Mostrar el cálculo paso a paso; revisar cada fallo contra la especificación antes de registrarlo. |
| 2 | Usar parámetros que no son los de mi código estudiantil. | Baja | Muy alto (nota 0) | Tabla de parámetros con el cálculo de cada fórmula al inicio; CONFIG revisado contra esa tabla. |
| 3 | Que una corrección dañe algo que funcionaba (regresión). | Media | Alto | Suite completa después de cada rama; integrar solo en verde. |
| 4 | Errores de punto flotante en el redondeo (por ejemplo 8.549,999 en lugar de 8.550). | Media | Medio | Casos que caen justo en $50; en la refactorización el dinero se maneja con `Decimal`. |
| 5 | Ambigüedades de la especificación (cliente desconocido, cupón vacío). | Media | Medio | Dejarlas escritas como supuestos y no inventar reglas. |
| 6 | Que la refactorización cambie el comportamiento sin querer. | Media | Alto | Refactorizar en pasos pequeños con las mismas pruebas como red de seguridad. |
| 7 | Poco tiempo: la entrega es el mismo día. | Alta | Alto | Priorizar por rúbrica; commits pequeños y frecuentes para no perder trabajo. |

## 2.7 Criterios de entrada

- Especificación R1 a R8 con mis valores escrita y revisada.
- Código heredado en el repositorio con la etiqueta `v1.0.0` y `CONFIG` lleno.
- Ambiente instalado: Python, pytest y pytest-cov funcionando.
- Casos de prueba diseñados con su resultado esperado calculado a mano.

## 2.8 Criterios de salida

- El 100 % de los casos diseñados está automatizado y ejecutado.
- El 100 % de los casos pasa sobre la versión corregida.
- Cobertura de sentencias y de ramas del 100 % en `envios.py`.
- Ningún defecto de severidad alta o media abierto.
- Cada defecto encontrado tiene su reporte, su rama `fix/DEF-xx` y una prueba
  que lo reproduce.
- Versión publicada con etiqueta, CHANGELOG y notas de versión.

## 2.9 Entregables

Plan de pruebas (este documento), diseño de casos (Partes 3 y 4), código de
las pruebas en `tests/`, reporte de defectos y métricas (Parte 5), evidencias
de ejecución en `docs/evidencias/` y el informe final en PDF.
