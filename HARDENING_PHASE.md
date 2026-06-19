# Fase de Endurecimiento y Estabilización (V1)

> **Rama activa:** `fix/V1-hardening-phase`
> **Fecha de auditoría:** 2026-06-19
> **Estado:** 🔍 ANÁLISIS COMPLETADO — Pendiente de aprobación del plan de acción

---

## 1. Inventario de Componentes Auditados e Inconsistencias

### PASO A — Capa de Persistencia y Dominio

#### `backend/app/models/`

| Componente | Hallazgo | Severidad |
|---|---|---|
| `Lead.created_at` / `updated_at` | Usan `DateTime` sin `timezone=True`. Las fechas almacenadas son naive (sin tz). La API las serializa como ISO-8601 sin sufijo `Z`, lo que crea ambigüedad en el cliente. | ⚠️ Minor |
| `Lead.status` | Tipado como `Mapped[str]` en lugar de `Mapped[LeadStatus]` (el enum propio). El ORM no aplica validación a nivel de tipo; sólo confía en el `CheckConstraint` de PostgreSQL. | ⚠️ Minor |
| `LeadActivity.type` | Misma inconsistencia: `Mapped[str]` en lugar de `Mapped[ActivityType]`. | ⚠️ Minor |
| `Lead.updated_at` | Usa `default=func.now()` como valor inicial. Verificado en la migración → OK. | ✅ OK |
| `models/__init__.py` | Importa `LeadStatus` y `ActivityType` de `enums.py`. El archivo es idéntico al del frontend (duplicación de código). | ℹ️ Info |

#### `backend/app/repositories/`

| Componente | Hallazgo | Severidad |
|---|---|---|
| `SQLAlchemyLeadRepository.create()` | Usa `session.flush()` sin `commit()`. El commit lo gestiona la dependencia FastAPI. Patrón Unit of Work correcto. | ✅ OK |
| `SQLAlchemyLeadRepository.update()` | Llama a `session.flush()` pero **sin** `session.refresh(lead)`. Sin el refresh, atributos auto-generados como `updated_at` (server default) podrían no actualizarse en el objeto devuelto por la API (datos stale). | 🔴 Bug |
| `SQLAlchemyLeadRepository.delete()` | Si el `lead_id` no existe, no hace nada (silent no-op). El servicio garantiza la existencia antes, pero el repo no valida por sí solo. | ⚠️ Minor |
| `AbstractLeadActivityRepository` | No tiene método `delete_by_lead_id`. El borrado en cascada lo maneja la FK de BD. Correcto pero implícito sin documentación. | ℹ️ Info |

#### `backend/app/dependencies.py`

| Componente | Hallazgo | Severidad |
|---|---|---|
| `get_db()` | Usa `try/finally` con `db.close()`. **No hace rollback en caso de excepción.** La doc oficial de FastAPI recomienda `try/except/finally` para ejecutar rollback antes del close y evitar transacciones zombi. | 🔴 Bug |
| `get_lead_activity_service()` | Crea **dos sesiones de DB independientes**: una para `activity_repo` y otra para `lead_repo` (cada `Depends(get_db)` abre su propia sesión). Las operaciones que involucran ambos repos viajan en **transacciones distintas**, violando la atomicidad. | 🔴 Bug Crítico |
| `engine` | Creado con `pool_pre_ping=True` (correcto). No configura `pool_size` ni `max_overflow`, lo que en producción puede generar saturación del connection pool. | ⚠️ Minor |

#### `backend/alembic/versions/0001_initial_migration.py`

| Componente | Hallazgo | Severidad |
|---|---|---|
| DDL `created_at` / `updated_at` | Declarados como `sa.DateTime()` sin `timezone=True`. Inconsistencia con UTC-aware ideal en producción. | ⚠️ Minor |
| `server_default` ausente | Las columnas `created_at` y `updated_at` **no tienen `server_default`** en el DDL. Si alguien inserta un registro directamente via psql o migración manual, las columnas quedarán `NULL`, violando el constraint `nullable=False`. | 🔴 Bug |

---

### PASO B — Capa de Transporte Backend (API)

#### `backend/app/main.py`

| Componente | Hallazgo | Severidad |
|---|---|---|
| Exception handlers | Registrados: `LeadNotFound (404)`, `DuplicateEmail (409)`, `InvalidStatus (422)`, `InvalidActivityType (422)`. **No existe handler global para `Exception` (500) ni para `RequestValidationError` de Pydantic.** Un error inesperado devolvería un 500 sin formato JSON consistente. | 🔴 Bug |
| Handler `RequestValidationError` | Pydantic lanza `RequestValidationError` para payloads malformados. El handler por defecto devuelve `{"detail": [...]}` (lista anidada), diferente al formato de los handlers personalizados `{"detail": "string"}`. Inconsistencia de contrato de API. | ⚠️ Minor |
| `lifespan` — API style | Usa `db.query(Lead).count()` con la API Legacy de SQLAlchemy 1.x, siendo que el resto del código usa la API 2.0 (`select()`). Mezcla de estilos. | ⚠️ Minor |
| `lifespan` — logging | El bloque `except Exception` usa `print()` en lugar del módulo `logging`. En producción los logs de stdout no son capturados de forma estructurada. | ⚠️ Minor |

#### `backend/app/routers/leads.py`

| Componente | Hallazgo | Severidad |
|---|---|---|
| `list_leads` — param `status` | Recibe `status: Optional[str]` sin validación enum en el query param. Un valor `?status=INVALID` llega al repositorio y la query devuelve vacío en lugar de un 422 claro. | ⚠️ Minor |
| Return type hints | Las funciones declaran `-> LeadResponse` pero el servicio retorna `Lead` (ORM object). FastAPI serializa via `response_model`, pero el type hint es técnicamente incorrecto. | ⚠️ Minor |

#### `backend/app/routers/lead_activities.py`

| Componente | Hallazgo | Severidad |
|---|---|---|
| `list_activities` — return type | `-> List[LeadActivityResponse]` pero el servicio retorna `List[LeadActivity]`. Mismo problema de type hint que en leads. | ⚠️ Minor |

#### `backend/app/schemas/`

| Componente | Hallazgo | Severidad |
|---|---|---|
| `LeadUpdate.status` | Tipo `Optional[str]` sin validación enum en Pydantic. Un cliente puede enviar `{"status": "FOOBAR"}` y Pydantic lo acepta. La validación ocurre más tarde en `LeadService`, pero la defensa debería ser más temprana. | ⚠️ Minor |
| `LeadCreate.name` | `Field(..., max_length=100)` pero sin `min_length=1`. Un nombre de solo espacios `" "` pasa la validación de Pydantic. | ⚠️ Minor |
| `LeadActivityCreate.notes` | `Field(..., min_length=1)` — Correcto. | ✅ OK |

---

### PASO C — Frontend (Diagnóstico NoneType → ver Sección 2)

#### Hallazgos generales del frontend

| Componente | Hallazgo | Severidad |
|---|---|---|
| `client.py` — `httpx.AsyncClient` | El cliente HTTP se instancia como variable global del módulo. Con `reload=True` (dev), los módulos pueden ser reimportados sin reinicializar limpiamente el cliente. En producción con `reload=False` es inofensivo. | ℹ️ Info |
| `lead_table.py` — `table_state` | Estado global mutable compartido entre todas las sesiones de usuario. En NiceGUI multi-user, el filtro de un usuario afectaría la vista de todos los demás. | 🔴 Bug (multi-user) |
| `lead_detail.py` — `detail_state` | Mismo problema que `table_state`. El `selected_id` es global, no aislado por sesión. | 🔴 Bug (multi-user) |
| `lead_table.py` L.119 | `lambda msg: on_select_lead(msg.args)` — `msg.args` puede ser `dict` o `int` según la versión de NiceGUI/Quasar. No hay validación del tipo del argumento. | ⚠️ Minor |

---

## 2. Diagnóstico del Error NoneType (Frontend <-> Backend)

### 🔴 Causa Raíz Identificada — Cadena de Fallos

El error `'NoneType' object ...` al cargar `http://localhost:8080/` es consecuencia de una **cadena de fallos** y no de un único punto de falla:

#### Flujo de ejecución al cargar `/`

```
index_page()
  ├─ await kpi_cards()
  │       └─ api_request("GET", "/metrics")
  │               └─ httpx.ConnectError → returns None
  │                       ✅ Manejado: fallback a {new:0, contacted:0, ...}
  │
  ├─ await lead_table(on_select_lead=select_lead)
  │       └─ api_request("GET", "/leads?...")
  │               └─ httpx.ConnectError → returns None
  │                       ✅ Manejado: leads = []
  │
  └─ await lead_detail(detail_state["selected_id"], on_update=refresh_all)
                        ↑
                        None  ←── ESTADO INICIAL
```

#### Vector de crash #1 — Stale Closure en `lead_detail.py:57`

La función `lead_detail()` recibe `lead_id=None` en la carga inicial. El guard en **L.17** lo intercepta correctamente:

```python
# lead_detail.py L.17
if not lead_id:
    # Renderiza placeholder card
    return  # ← OK en la primera carga
```

**El crash ocurre en un segundo render**, cuando `update_status()` (closure definido dentro del render de `lead_detail`) llama a:

```python
# lead_detail.py L.57
lead_detail.refresh(lead_id)
```

`lead_id` es una variable libre capturada por el closure de `update_status()`. Si entre el momento del render original y la ejecución de `update_status()` NiceGUI ha rehidratado el componente (ej: `refresh_all()` ejecutado), el closure puede tener una referencia al `lead_id` del render anterior o incluso a `None`.

Esto causa que `api_request("GET", f"/leads/{lead_id}")` construya la URL `/leads/None`, el backend responde 404, `api_request` retorna `None`, y el flujo llega a:

```python
# lead_detail.py L.41 — CRASH PRINCIPAL
ui.label(lead["name"])  # TypeError: 'NoneType' object is not subscriptable
```

El guard `if not lead: return` en **L.27-31** existe para interceptar esto. La hipótesis es que bajo condiciones de **race condition async** (dos re-renders concurrentes por `refresh_all()` + `lead_detail.refresh()`), el guard se evalúa antes de que la coroutine de la request HTTP haya resuelto `lead`, y el flujo sigue ejecutando en un contexto donde `lead = None`.

#### Vector de crash #2 — Guard débil en `lead_table.py:28`

```python
# lead_table.py L.28
leads = data["leads"] if data else []
```

El guard `if data else []` protege solo contra `None`. Si el backend devuelve un JSON no-dict (ej: error de proxy devuelve HTML o un string), `data["leads"]` lanzaría `TypeError`. La protección debe cubrir también respuestas con estructura inesperada.

### 🛡️ Guards propuestos (diseño, sin implementación en esta fase)

**`lead_detail.py` — Guard endurecido:**
```python
# Reemplazar la verificación actual de L.27
if not lead or not isinstance(lead, dict) or "name" not in lead:
    # Renderizar error card y return
```

**`lead_table.py:28` — Guard endurecido:**
```python
leads = data.get("leads", []) if isinstance(data, dict) else []
```

**Stale closure en `update_status` y `add_activity`:**
```python
# Capturar lead_id como argumento default para evitar stale closure
async def update_status(captured_lead_id: int = lead_id):
    ...
    lead_detail.refresh(captured_lead_id)
```

**`detail_state` / `table_state` — Aislamiento por sesión:**
```python
# En lugar de dicts globales, usar app.storage.user de NiceGUI
from nicegui import app as nicegui_app
# nicegui_app.storage.user["selected_id"] en lugar de detail_state["selected_id"]
```

---

## 3. Actualizaciones Tecnológicas y Seguridad (Vía MCP)

### Versiones actuales vs. últimas disponibles

| Librería | Versión Fijada | Última Estable | Riesgo |
|---|---|---|---|
| `fastapi` | `0.111.0` | `0.128.0` | ⚠️ 17 versiones minor atrás. Fixes de seguridad y lifespan. |
| `uvicorn` | `0.30.1` | `0.34.x` | ⚠️ Performance y compatibilidad con Starlette. |
| `sqlalchemy` | `2.0.30` | `2.0.41` | ⚠️ 11 patches atrás. Fixes en typed ORM y session management. |
| `alembic` | `1.13.1` | `1.16.x` | ⚠️ Mejoras en autogenerate y compatibilidad SA 2.0. |
| `psycopg2-binary` | `2.9.9` | `2.9.10` | ℹ️ Patch menor. |
| `pydantic-settings` | `2.3.3` | `2.9.x` | ⚠️ Validation y performance. |
| `httpx` | `0.27.0` | `0.28.x` | ⚠️ Fixes en async client lifecycle. |
| `pytest` | `8.2.2` | `8.4.x` | ℹ️ Patch menor. |
| `pytest-asyncio` | `0.23.7` | `0.25.x` | ⚠️ Cambios en configuración de modo async. |
| `nicegui` | `1.4.25` | `2.x` | 🔴 **BREAKING CHANGE**: NiceGUI v2.x tiene nueva API. Migración requiere análisis dedicado. |

### Hallazgos MCP — FastAPI (via context7)

1. **`get_db()` sin rollback**: La documentación oficial de FastAPI (*Dependencies with yield*) establece explícitamente que las dependencias deben capturar excepciones para hacer rollback antes del `finally`. La implementación actual **solo tiene `finally`**, dejando transacciones zombi ante fallos.

2. **Lifespan correcto en forma, inconsistente en contenido**: El uso de `@asynccontextmanager` es el patrón moderno y correcto. Sin embargo, el lifespan usa `db.query(Lead).count()` (API SQLAlchemy 1.x Legacy) siendo que el resto del código usa la API 2.0 (`select()`).

3. **Override de `RequestValidationError` recomendado**: Se debe registrar un handler para `RequestValidationError` (importado de `fastapi.exceptions`) para homogeneizar el formato de errores de validación Pydantic con el de los handlers de dominio.

### Hallazgos MCP — NiceGUI (via context7)

1. **Estado global vs. por sesión**: La documentación de NiceGUI advierte que las variables globales son compartidas entre todas las sesiones. El patrón recomendado es `app.storage.user` (persistido por usuario) o `app.storage.tab` (por pestaña del navegador).

2. **Stale closures en `@ui.refreshable`**: El decorator `@ui.refreshable` recrea los widgets pero los closures de Python capturan referencias al momento de creación. La recomendación es siempre pasar el estado como argumento default al `def`, nunca depender de captura implícita del scope externo.

3. **NiceGUI 1.x → 2.x**: Major release con breaking changes en arquitectura de `pages` y `storage`. La actualización debe evaluarse en un spike dedicado, fuera del scope de esta fase de hardening.

---

## 4. Plan de Acción Propuesto (Pendiente de Aprobación)

> [!IMPORTANT]
> Cada ítem debe implementarse en un commit independiente sobre la rama `fix/V1-hardening-phase`. **Ningún commit directo sobre `main`.**

---

### [Solución de Bugs] — Prioridad CRÍTICA 🔴

| # | Archivo | Descripción del Fix | Impacto |
|---|---|---|---|
| **B-01** | `backend/app/dependencies.py` | Agregar `except Exception: db.rollback(); raise` al generador `get_db()`. | Evita transacciones zombi en PostgreSQL |
| **B-02** | `backend/app/dependencies.py` | Refactorizar `get_lead_activity_service()` para reutilizar **la misma sesión** para `lead_repo` y `activity_repo`, eliminando el doble `Depends(get_db)`. | Garantiza atomicidad en UC-06 y UC-07 |
| **B-03** | `backend/app/repositories/sqlalchemy_lead_repository.py` | Agregar `self.session.refresh(lead)` después de `session.flush()` en `update()`. | Evita respuestas con `updated_at` stale |
| **B-04** | `frontend/app/components/lead_detail.py` | Endurecer el guard de `lead` con `isinstance(lead, dict)` y capturar `lead_id` como argumento default en los closures de `update_status` y `add_activity`. | Soluciona el crash NoneType reportado |
| **B-05** | `frontend/app/components/lead_table.py` | Cambiar `data["leads"] if data else []` por `data.get("leads", []) if isinstance(data, dict) else []`. | Protege contra respuestas con estructura inesperada |
| **B-06** | `backend/app/main.py` | Agregar handler global para `Exception` → respuesta 500 con `{"detail": "Internal server error"}`. | Evita respuestas 500 sin body JSON |

---

### [Mejoras de Arquitectura] — Prioridad ALTA ⚠️

| # | Archivo | Descripción | Impacto |
|---|---|---|---|
| **A-01** | `frontend/app/components/lead_table.py` + `lead_detail.py` | Migrar `table_state` y `detail_state` a `app.storage.user` de NiceGUI. | Hace el sistema correcto para multi-usuario |
| **A-02** | `backend/app/main.py` | Reemplazar `db.query(Lead).count()` por `db.execute(select(func.count()).select_from(Lead)).scalar()` (API SA 2.0 pura). | Consistencia de estilo en todo el backend |
| **A-03** | `backend/app/main.py` | Agregar handler para `RequestValidationError` con formato `{"detail": str}` consistente con los handlers de dominio. | Unifica el contrato de errores de la API |
| **A-04** | `backend/app/dependencies.py` | Configurar `pool_size=5` y `max_overflow=10` en `create_engine()`. | Previene saturación de conexiones en producción |
| **A-05** | `backend/alembic/` | Crear nueva migración que agregue `server_default=sa.text("NOW()")` a `created_at` y `updated_at`. | Garantiza valores válidos ante inserciones directas a BD |

---

### [Pulido de Tipos] — Prioridad BAJA ℹ️

| # | Archivo | Descripción | Impacto |
|---|---|---|---|
| **T-01** | `backend/app/models/lead.py` | Cambiar `Mapped[str]` → `Mapped[LeadStatus]` en campo `status`. | Type safety en ORM |
| **T-02** | `backend/app/models/lead_activity.py` | Cambiar `Mapped[str]` → `Mapped[ActivityType]` en campo `type`. | Type safety en ORM |
| **T-03** | `backend/app/models/` | Cambiar `DateTime` → `DateTime(timezone=True)` + nueva migración Alembic. | Timestamps UTC-aware en producción |
| **T-04** | `backend/app/schemas/lead.py` | Cambiar `LeadUpdate.status: Optional[str]` → `Optional[LeadStatus]`. | Validación temprana en Pydantic |
| **T-05** | `backend/app/schemas/lead.py` | Agregar `min_length=1` y `strip_whitespace=True` a `LeadCreate.name`. | Evita nombres vacíos o con solo espacios |
| **T-06** | `backend/app/routers/leads.py` | Cambiar `status: Optional[str]` del query param → `Optional[LeadStatus]`. | Devuelve 422 automático para valores de status inválidos |
| **T-07** | `backend/app/routers/leads.py` + `lead_activities.py` | Corregir return type hints de funciones router (actualmente `-> LeadResponse`, correcto sería `-> Lead`). | Honestidad de type hints |

---

### Resumen Ejecutivo

```
🔴 CRÍTICO  — 6 tareas  (B-01 a B-06) — Bloqueantes para producción
⚠️ ALTO     — 5 tareas  (A-01 a A-05) — Robustez y arquitectura
ℹ️ BAJO     — 7 tareas  (T-01 a T-07) — Deuda técnica de tipos y pulido
────────────────────────────────────────
Total: 18 tareas de refactorización identificadas
```
