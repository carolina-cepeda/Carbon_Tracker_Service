# Microservicio de Cálculo de Huella de Carbono

Microservicio para empresas de logística que calcula las emisiones de CO2 de un viaje basándose en el tipo de vehículo, el peso de la carga, la distancia recorrida y los factores de eficiencia del combustible/energía.

Este proyecto fue desarrollado con la asistencia de Inteligencia Artificial (IA) en todas sus fases: planificación, diseño de la lógica de cálculo, implementación y pruebas. Para conocer el detalle de cómo se construyó, consulta la [Bitácora de Prompts](bitacora/bitacora_prompts.md).

## Tipos de vehículo soportados

| Tipo | Lógica de cálculo |
|------|-------------------|
| Diésel (`diesel`) | Consumo = distancia / eficiencia (ajustado por peso); CO2 = litros × 2.68 kg CO2/l |
| Gasolina (`gasoline`) | Igual que diésel con factor de 2.31 kg CO2/l |
| Eléctrico (`electric`) | Energía = distancia × consumo kWh/km (ajustado por peso); CO2 = kWh × factor de red |
| Híbrido (`hybrid`) | Suma ponderada de la parte de combustión y la parte eléctrica según `electric_usage_ratio` |

El peso añade una penalización del 2% de consumo por tonelada de carga.

## Estructura del proyecto

```
.
├── app/                          # Código fuente (Clean Architecture)
│   ├── main.py                   # Punto de entrada de FastAPI
│   ├── domain/                   # Reglas de negocio puras (sin dependencias externas)
│   │   ├── entities/             # Entidades: Vehicle, EmissionCalculation
│   │   ├── enums/                # Tipos de vehículo y de combustible
│   │   ├── value_objects/        # Objetos validados: Distance, Weight, EmissionFactor
│   │   ├── interfaces/           # Contratos: FactorCatalog, EmissionCalculator
│   │   └── services/emission/    # Lógica de cálculo por tipo de vehículo (Strategy)
│   ├── application/              # Casos de uso y DTOs (orquesta el dominio)
│   │   ├── use_cases/            # CalculateEmissionUseCase
│   │   ├── dto/                  # Peticiones/respuestas de aplicación
│   │   └── interfaces/           # Fabrica de calculadores
│   ├── infrastructure/           # Detalles técnicos: configuración, factores IPCC, DI
│   │   ├── config/               # Settings (variables de entorno CFS_*)
│   │   ├── factors/              # Catálogo de factores IPCC
│   │   └── composition.py        # Montaje de dependencias
│   └── presentation/             # Capa HTTP: routers y schemas (sin lógica de negocio)
│       ├── api/v1/               # Endpoints REST
│       ├── schemas/              # Modelos Pydantic
│       └── dependencies/         # Inyección de dependencias
├── tests/                        # Suite de pruebas (unitarias e integración)
│   ├── unit/                     # Tests de dominio, aplicación e infraestructura
│   └── integration/              # Tests de la API y manejadores de error
├── bitacora/
│   └── bitacora_prompts.md       # Bitácora con los prompts que dieron origen al proyecto
├── requirements.txt              # Dependencias del proyecto
└── pyproject.toml                # Configuración del proyecto y de pytest
```

## Principios de diseño

- **Clean Architecture**: separación en dominio, aplicación, infraestructura y presentación.
- **Modularización**: la lógica de negocio está completamente separada de los controladores de la API.
- **SOLID**: cálculo abierto a nuevos tipos de vehículo (patrón Strategy + Factory), interfaces segregadas e inversión de dependencias.
- **Validación defensiva**: los datos sin sentido (distancias 0, cargas negativas, vehículos sin identificación, tipos no soportados) se rechazan con mensajes claros.

## API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/v1/emissions/calculate` | Calcula las emisiones de CO2 de un viaje |
| `GET`  | `/v1/emissions/factors` | Consulta los factores de emisión configurados |
| `GET`  | `/health` | Verifica el estado del servicio |

### Ejemplo de petición

```json
{
  "vehicle_id": "TRK-001",
  "vehicle_type": "diesel",
  "distance_km": 250.0,
  "weight_tons": 12.0,
  "base_efficiency_km_l": 4.5,
  "base_consumption_kwh_km": 0.2,
  "electric_usage_ratio": 0.0
}
```

### Ejemplo de respuesta

```json
{
  "vehicle_id": "TRK-001",
  "vehicle_type": "diesel",
  "distance_km": 250.0,
  "weight_tons": 12.0,
  "total_co2_kg": 218.813,
  "breakdown": {
    "fuel_consumed_liters": 81.65,
    "emissions_kg": 218.822
  },
  "formula_used": "combustion: CO2 = (distance * 1/eff) * weight_factor * fuel_factor"
}
```

## Instalación y ejecución

```bash
# Crear entorno virtual e instalar dependencias
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# Ejecutar el servidor
.venv/bin/uvicorn app.main:app --reload
```

Documentación interactiva automática (OpenAPI): `http://localhost:8000/docs`

### Variables de entorno

| Variable | Predeterminado | Descripción |
|----------|---------------|-------------|
| `CFS_GRID_FACTOR_KG_KWH` | `0.4` | Factor de emisión de la red eléctrica (kg CO2/kWh) |
| `CFS_WEIGHT_PENALTY_PER_TON` | `0.02` | Penalización de consumo por tonelada de carga |

## Pruebas

La suite consta de 58 pruebas con 100% de cobertura, incluyendo casos borde (distancias 0, cargas neutras/negativas, tipos de vehículo no soportados, identificadores vacíos, etc.), con mensajes de error amigables y no técnicos.

```bash
# Ejecutar todas las pruebas con reporte de cobertura
.venv/bin/python -m pytest --cov=app --cov-report=term-missing
```

## 
## Nota sobre la autoría del proyecto

El presente proyecto fue realizado íntegramente con la asistencia de Inteligencia Artificial, desde el análisis y la planificación inicial hasta la implementación del código y la generación de pruebas. El detalle de la conversación (prompts) queda registrado en [bitacora/bitacora_prompts.md](bitacora/bitacora_prompts.md).