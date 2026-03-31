===
title: Add Portugal national holidays support
status: done
priority: P2
last_activity: 2026-03-31
labels: [feature, portugal, holidays, api, tests, docs]
===
## Objetivo
Implementar soporte para festivos nacionales de Portugal por anio con una clase `HolidayPortugal`, manteniendo compatibilidad con la API actual del paquete.

## Plan de ejecucion para completar
1. Crear `holidays_es/holidays_portugal.py` con la clase `HolidayPortugal`.
2. Implementar validacion de anio (`min_year`, `max_year`) alineada con el patron de `HolidaySpain`.
3. Integrar cliente HTTP con `requests` contra `https://date.nager.at/api/v3/PublicHolidays/{year}/PT` con `timeout` y manejo de errores.
4. Mapear la respuesta a `models.Holiday` usando:
   - `scope=enums.Scope.NATIONAL`
   - `date` desde string ISO
   - `description=localName` (fallback a `name` si no existe)
5. Agregar excepcion especifica en `holidays_es/exceptions.py`: `HolidayPortugalError`.
6. Exportar `HolidayPortugal` en `holidays_es/__init__.py`.
7. Crear pruebas en `tests/test_holidays_portugal.py` para:
   - carga de festivos
   - scopes nacionales
   - validacion de anio fuera de rango
   - `find(date)` con una fecha conocida
8. Actualizar `README.rst` con ejemplo de uso de `HolidayPortugal`.
9. Ejecutar `pytest` y ajustar cualquier fallo de estilo/tipos.

## Criterios de aceptacion
- Existe clase publica `HolidayPortugal` importable desde `holidays_es`.
- Se obtienen festivos nacionales de Portugal para un anio valido.
- Ante error de red/API se lanza `HolidayPortugalError`.
- Todas las pruebas nuevas y existentes pasan.
- README incluye ejemplo funcional de Portugal.
