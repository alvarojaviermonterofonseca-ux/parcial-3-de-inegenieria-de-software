# Changelog

Todos los cambios importantes de este proyecto se registran en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Sin publicar]

## [2.0.0] - 2026-11-11

### Cambiado

- La función principal ahora se llama `calcular_costo(peso, zona, cliente,
  dia, cupon=None)`. `calc` se conserva como alias.
- El cálculo se dividió en funciones pequeñas: `validar_envio`, `tarifa_base`,
  `recargo_fin_de_semana`, `aplicar_descuentos` y `redondear`.
- El recargo por zona usa el patrón Estrategia (`EstrategiaZona`,
  `ZonaUrbana`, `ZonaRural`, `ZonaNacional`).
- Los números mágicos se reemplazaron por constantes con nombre.
- El dinero se calcula con `Decimal` en lugar de `float`.
- El día debe ser un entero de 1 a 7 (antes se aceptaba, por ejemplo, 6,5).

### Eliminado

- **Incompatible:** el parámetro `flag` de `calc` y la impresión por consola.
  Las llamadas que lo usaban (`calc(..., flag=True)`) ahora producen
  `TypeError`.
- **Incompatible:** el diccionario `CONFIG`. Los valores ahora son constantes
  del módulo (`PESO_MAXIMO_KG`, `LIMITE_TRAMO_1_KG`, ...).
- La asignación sin efecto `t = t`.

### Añadido

- Pruebas de unidad de las funciones extraídas y de las estrategias
  (`tests/test_unidades.py`).

## [1.0.1] - 2026-11-11

### Corregido

- **DEF-04:** el sábado no cobraba el recargo de fin de semana.
- **DEF-06:** el costo se truncaba en vez de redondearse al múltiplo de $100
  más cercano.
- **DEF-01:** se aceptaban envíos de más de 45 kg (el tope estaba en 50).
- **DEF-02:** una zona inexistente se cobraba como urbana; ahora es error.
- **DEF-03:** no se validaba que el día estuviera entre 1 y 7.
- **DEF-05:** un cupón inexistente se ignoraba; ahora es error.
- **DEF-07:** el mensaje de error decía "peso invalido" en vez de
  "peso inválido".

### Añadido

- Suite de pruebas automatizadas con pytest: 42 casos de caja negra y 15 de
  caja blanca.

## [1.0.0] - 2026-11-11

### Añadido

- Código heredado de EnvíaYa: función `calc` con `CONFIG` lleno según el
  código estudiantil 0182310065.

[Sin publicar]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/compare/v1.0.1...v2.0.0
[1.0.1]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/releases/tag/v1.0.0
