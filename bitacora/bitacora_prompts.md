# Bitácora de Prompts

Este documento recopila los prompts que dieron origen al proyecto, en orden cronológico.

---

## Prompt 1 — Planificación del microservicio

> Actúa como desarrollador senior de software con gran experiencia en Python y FastAPI, con estándares de limpieza de código y principios SOLID. Para ello, vamos a planificar paso a paso para la construcción de un microservicio de cálculo de huella de carbono para una empresa de logística.
>
> Para este servicio es necesario que se calcule las emisiones de CO2 basado en varias variables como el tipo de vehículo (eléctrico, Diesel, Híbrido), el peso de la carga (en toneladas), la distancia recorrida en kilómetros y el factor de eficiencia del combustible/energía.
>
> Para todo lo anterior, primero debes prometer la lógica del cálculo para cada uno de los posibles escenarios.

**Decisiones tomadas a partir de este prompt:**
- Utilizar factores de emisión IPCC como fuente de datos.
- Para vehículos eléctricos, modelar emisiones indirectas mediante un factor de red eléctrica configurable.
- Arquitectura limpia (Clean Architecture) organizada en dominio, aplicación, infraestructura y presentación.

---

## Prompt 2 — Función principal y modularización

> Teniendo el plan en cuenta, procede a crear la función principal del cálculo; para ello es necesario que manejes modularización, es decir, que separes la lógica de negocio de los controladores de la API.

**Resultado:**
- Implementación de la capa de cálculo (strategy por tipo de vehículo).
- Separación estricta entre lógica de negocio (dominio + aplicación) y controladores de la API (presentación).
- Inyección de dependencias vía composición en infraestructura.

---

## Prompt 3 — Formato exacto de los datos

> Dame un ejemplo de formato que estás usando para las peticiones

**Resultado:**
- Documentación de los formatos exactos (JSON) de peticiones, respuestas, factores y errores de la API.

---

## Prompt 4 — Pruebas unitarias con cobertura

> Genera pruebas unitarias usando Pytest que cubran al menos el 90% de la lógica del código incluyendo casos borde o inesperados como distancias 0 o neutrales, tipo de vehículos no soportados, etc, de manera amigable para el usuario de forma que puedan entender cuál es el problema exacto sin tanto lenguaje "técnico".

**Resultado:**
- Suite de 58 pruebas con 100% de cobertura.
- Mensajes de aserción en lenguaje claro y no técnico.
- Cobertura de casos borde: distancia 0, peso neutro/negativo, tipos no soportados, identificadores vacíos, etc.

---

## Prompt 5 — Revisión integral de código (seguridad y rendimiento)

> Actúa como desarrollador senior de software con gran experiencia en Python y FastAPI, con estándares de limpieza de código y principios SOLID. Haz una revisión integral del código fuente del proyecto de cálculo de huella de carbono y haz una crítica enfocada en el rendimiento y la seguridad, teniendo en cuenta estándares actuales de código y seguridad en software.

**Resultado:**

Revisión exhaustiva de lo  archivos fuente del proyecto que identificó **17 problemas** clasificados por severidad:

### Seguridad (5 hallazgos)
- **CRÍTICO**: Sin autenticación/autorización en la API.
- **CRÍTICO**: Sin rate limiting para prevenir abuso.
- **CRÍTICO**: Sin configuración de CORS (`CORSMiddleware`).
- **ALTO**: Sin limitación de tamaño de payload.
- **ALTO**: El handler de `ValueError` devuelve `str(exc)` directamente, posiblemente filtrando información interna.

### Rendimiento (4 hallazgos)
- **ALTO**: `get_calculator_factory()` reconstruye toda la cadena de dependencias (catalog + 4 calculadoras) en cada request. Solución propuesta: cachear con `@lru_cache`.
- **ALTO**: Triple validación redundante (Pydantic → DTO `validate()` → Value Object `__post_init__`).
- **MEDIO**: `IpccFactorCatalog.get_factor()` recrea un diccionario en cada llamada.
- **MEDIO**: `weight_adjustment_factor()` usa `abs()` innecesariamente, enmascarando bugs potenciales.

### Arquitectura / SOLID (5 hallazgos)
- `EmissionCalculator.calculate()` no tiene tipado en parámetros (viola explicit interface contracts).
- `EmissionCalculatorFactory` es clase concreta, no interfaz ABC (viola Dependency Inversion).
- Duplicación de enums `FuelType` y `VehicleType` con mapeo implícito frágil.
- `Vehicle` tiene campos `make` y `model` sin uso real (dead code, monkey-patching en el use case).
- `WEIGHT_PENALTY_PER_TON` está hardcodeada ignorando `Settings.weight_penalty_per_ton`.

### Infraestructura (3 hallazgos)
- Sin `Dockerfile` ni `.dockerignore`.
- Dependencias de testing mezcladas con producción en `requirements.txt`.
- Sin linter (`ruff`/`flake8`) ni type checker (`mypy`/`pyright`) configurados.

### Plan de mejoras priorizado (17 items)
Se generó una tabla de 17 mejoras ordenadas de CRÍTICO a BAJO, con esfuerzo estimado, desde agregar autenticación y rate limiting (críticos) hasta reemplazar `abs()` y migrar a `Decimal` (bajos).