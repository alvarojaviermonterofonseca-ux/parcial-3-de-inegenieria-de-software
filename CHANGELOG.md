# Changelog

Todos los cambios importantes de este proyecto se registran en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto usa [Versionado Semántico](https://semver.org/lang/es/).

## [Sin publicar]

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

[Sin publicar]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/alvarojaviermonterofonseca-ux/parcial-3-de-inegenieria-de-software/releases/tag/v1.0.0
