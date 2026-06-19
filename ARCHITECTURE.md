# Arquitectura del Sistema (ARCHITECTURE.md)

---

## 1. Topología del Sistema
El proyecto sigue una arquitectura monolítica clásica de tres capas, diseñada para entornos contenerizados. Se prioriza la simplicidad y el desacoplamiento físico de los componentes principales.

```text
[ Capa de Usuario ]        [ Capa de Aplicación ]        [ Capa de Persistencia ]
┌─────────────────┐        ┌────────────────────┐        ┌──────────────────────┐
│    Dashboard    │ ─────> │    FastAPI API     │ ─────> │  Base de Datos (SQL) │
│ (NiceGUI en Py) │ <───── │ (Backend Service)  │ <───── │     PostgreSQL       │
└─────────────────┘        └────────────────────┘        └──────────────────────┘
```

---

## 2. Responsabilidades por Capa

### A. Capa de Visualización (Dashboard)
*   **Tecnologías**: Python, NiceGUI, HTTPX (Cliente HTTP).
*   **Responsabilidad**: Renderizar e interactuar con la interfaz del dashboard administrativo completamente programada en Python. Consume los endpoints del backend (incluyendo el nuevo endpoint `/metrics` y los CRUD de leads) de manera asíncrona usando la librería cliente `httpx` en Python, eliminando la necesidad de programar en JavaScript o escribir CSS complejo.

### B. Capa de Transporte y Entrada (FastAPI API)
*   **Responsabilidad**: Exponer la API REST del sistema. Maneja la validación de payloads de entrada y esquemas de salida mediante **Pydantic**. Genera de forma automática la documentación interactiva OpenAPI (`/docs`). Es la encargada de resolver las dependencias HTTP y gestionar excepciones en el límite de la red.

### C. Capa de Negocio (Servicios / Caso de Uso)
*   **Responsabilidad**: Ejecutar las reglas de negocio descritas en los requerimientos. Actúa como el orquestador del flujo, controlando las transiciones de estado, verificando la unicidad del email y abstrayendo la persistencia. Es código Python puro libre de acoplamiento con frameworks web o librerías de persistencia.

### D. Capa de Persistencia (Repositorio / SQLAlchemy)
*   **Responsabilidad**: Mapear los objetos de negocio a tablas relacionales y viceversa. Ejecuta las consultas y persistencias físicas sobre PostgreSQL utilizando SQLAlchemy ORM.

---

## 3. Mapa de Dependencias
Para asegurar un diseño limpio y mantenible, las dependencias de código fluyen estrictamente en una dirección:

```text
Capa API (FastAPI) ──> Capa de Servicio ──> Interfaz Repositorio 
                                                    ▲
                                                    │ (Implementa)
                                           SQLAlchemy Repository ──> PostgreSQL
```

*   **Inversión de Control**: La capa de negocio (Servicios) **no** depende del repositorio concreto de SQLAlchemy. Depende de una clase abstracta (interfaz). La implementación concreta se inyecta en tiempo de ejecución.
*   **Aislamiento de Infraestructura**: Si la base de datos cambia de PostgreSQL a otro motor, o el framework web se migra de FastAPI a otro, la lógica comercial en la capa de servicios se mantiene intacta.

---

## 4. Flujo de Datos (Creación de un Lead)
A continuación se ilustra cómo viajan los datos a lo largo de las capas cuando se registra un cliente potencial:

```text
[Dashboard]              [FastAPI Route]             [LeadService]          [Repository / BD]
    │                           │                           │                       │
    │─── 1. POST /leads/ ──────>│                           │                       │
    │    (JSON payload)         │─── 2. Validar payload ───>│                       │
    │                           │    y llamar servicio      │                       │
    │                           │                           │─── 3. Solicitar ─────>│
    │                           │                           │    email existente    │
    │                           │                           │<── 4. Retorna None ───│
    │                           │                           │                       │
    │                           │                           │─── 5. Guardar Lead ──>│
    │                           │                           │    (Persistir ORM)    │
    │                           │                           │<── 6. Retorna Lead ───│
    │                           │                           │    (con ID de BD)     │
    │                           │<── 7. Retorna Entidad ────│                       │
    │<── 8. Respuesta 201 ──────│                           │                       │
    │    (JSON con ID)          │                           │                       │
```

1.  **Dashboard (NiceGUI)**: Captura la entrada del usuario en la interfaz interactiva Python, e inicia una llamada asíncrona HTTP POST usando `httpx` con el payload en formato JSON hacia el backend.
2.  **FastAPI Route**: Recibe el JSON, lo valida contra el esquema de entrada de Pydantic, e invoca el caso de uso del servicio.
3.  **LeadService**: Valida las reglas comerciales críticas (ej: verifica que el correo electrónico no esté duplicado realizando una llamada de consulta al repositorio).
4.  **SQLAlchemyRepository / PostgreSQL**: Procesa la consulta de verificación de email y la responde.
5.  **LeadService**: Si la regla comercial pasa, inicializa el Lead, le asigna el estado `NEW` y solicita al repositorio guardar la información.
6.  **SQLAlchemyRepository / PostgreSQL**: Realiza la inserción en base de datos, autogenera el ID de base de datos y la marca temporal de creación, confirmando la persistencia.
7.  **FastAPI Route**: Recibe el Lead guardado y lo serializa automáticamente utilizando el esquema de respuesta de Pydantic.
8.  **Dashboard (NiceGUI)**: Recibe la respuesta HTTP, actualiza el estado de las variables reactivas en Python y refresca los elementos de la interfaz en tiempo real sin recargar la página.
