# Informe de Revisión Crítica del Alcance (V1)

Este documento presenta una auditoría técnica del alcance propuesto para el **Lead & Customer Management System**. Como Arquitecto de Software Senior, he evaluado las especificaciones funcionales, los riesgos de sobreingeniería, las contradicciones y los vacíos en la documentación con el objetivo de congelar los requisitos de la V1 para su entrega garantizada en pocas semanas.

---

## 1. Alcance Actual Resumido
Estamos construyendo un **CRM ultra-simplificado para gestión de prospectos comerciales (Leads)**. El sistema consta de:
*   Un **Backend API** (FastAPI) asíncrono que expone operaciones CRUD de leads, registro de notas de actividad y un endpoint analítico simple de métricas agrupadas.
*   Una **Base de Datos** (PostgreSQL) con integridad relacional y validaciones.
*   Un **Dashboard Administrativo** (NiceGUI) interactivo en Python que actúa como cliente de la API, mostrando el listado, el detalle cronológico de interacciones de cada prospecto y tarjetas KPI agregadas.
*   Todo contenerizado bajo **Docker Compose**.

---

## 2. Funcionalidades Obligatorias (Imprescindibles para V1)
Para demostrar la calidad técnica mínima esperable en un portfolio profesional, los siguientes elementos son ineludibles:

*   **API & Backend**:
    *   `POST /leads`: Creación de prospecto con validación de unicidad de email.
    *   `GET /leads`: Listado paginado (`limit`/`offset`) y filtrado por estado o búsqueda textual (`query`).
    *   `GET /leads/{id}`: Detalle de un lead específico.
    *   `PUT /leads/{id}`: Actualización de datos y estado.
    *   `DELETE /leads/{id}`: Eliminación física para mantener el CRUD limpio.
    *   `GET /metrics`: Consulta analítica rápida para el dashboard.
    *   `POST /leads/{id}/activities`: Registrar una interacción.
    *   `GET /leads/{id}/activities`: Recuperar el historial del lead.
*   **Base de Datos**:
    *   Tabla `leads` y tabla `lead_activities` (Relación FK 1:N).
    *   Restricción única (`UniqueConstraint`) de email.
    *   Restricción de verificación (`CheckConstraint`) de estados del lead.
*   **Dashboard NiceGUI**:
    *   Vista principal con KPI Cards (totales por estado).
    *   Tabla interactiva de leads con paginación visual y barra de búsqueda.
    *   Formulario modal de creación de lead.
    *   Vista de detalle del lead con su información, formulario para añadir notas y la línea de tiempo (timeline) cronológica.

---

## 3. Funcionalidades Opcionales (Descartables)
Estas funcionalidades aportan valor estético pero pueden omitirse si el tiempo apremia, sin degradar la calidad del backend:

*   **Exportación a CSV**: Permitir descargar el listado filtrado de leads (descartable para V1).
*   **Edición o Eliminación de Actividades**: Una vez creada una nota o actividad, no es necesario permitir editarla o borrarla (mantener actividades inmutables simplifica la API).
*   **Edición masiva de leads**: Cambiar el estado de varios leads a la vez desde el listado.

---

## 4. Posibles Riesgos de Sobreingeniería
He identificado dos puntos de sobreingeniería potenciales ocultos en la especificación actual:

1.  **Migraciones complejas con Alembic**: Aunque Alembic es excelente, configurar múltiples ramas o migraciones complejas retrasará la inicialización. 
    *   *Mitigación*: Mantener una única migración inicial (`initial_migration`) que configure el esquema relacional de base de datos.
2.  **Lógica de reintentos HTTP ultra-sofisticada en el Dashboard**: Diseñar un cliente HTTPX con políticas complejas de reconexión y caching.
    *   *Mitigación*: Utilizar un manejo de excepciones simple en NiceGUI que muestre un diálogo visual de error si el backend no responde, sin implementar middleware de red complejo.

---

## 5. Vacíos Funcionales Detectados
Durante la revisión he detectado dos vacíos técnicos críticos que deben ser resueltos en el alcance:

1.  **Semilla de Datos (Data Seeding)**:
    *   *Problema*: Al levantar el entorno Docker por primera vez, el Dashboard estará vacío. Un evaluador no sabrá cómo interactuar de inmediato.
    *   *Solución*: Implementar un script de carga inicial o un botón discreto en el Dashboard "Generar Datos de Prueba" que inserte automáticamente 10 leads ficticios con 15 actividades realistas en la línea de tiempo.
2.  **Inconsistencia en REQUIREMENTS.md (Casos de Uso de Actividades)**:
    *   *Problema*: El documento de requerimientos definía la entidad `Lead` y sus CRUDs, pero omitió detallar formalmente los casos de uso para `LeadActivity` (`UC-06: Registrar Actividad` y `UC-07: Listar Actividades`).
    *   *Solución*: Se subsanará esta omisión agregando estos casos de uso explícitos en el documento final.
3.  **Tipo de Eliminación**:
    *   *Problema*: En el README se insinuaba borrado lógico, pero en REQUIREMENTS se definía borrado físico.
    *   *Solución*: Se congela en **Eliminación Física (Physical Delete)** para la V1. Es más rápido de testear y simplifica las consultas del repositorio.

---

## 6. Recomendaciones Finales
1.  **Adoptar Eliminación Física**: Ahorra la complejidad de manejar banderas `is_deleted` en todas las consultas y repositorios.
2.  **Añadir Semilla de Datos automática**: Al levantar el backend en Docker Compose, verificar si la base de datos está vacía e inyectar datos de prueba automáticamente en el inicio de la app.
3.  **Mantener actividades inmutables**: No desarrollar endpoints `PUT` o `DELETE` para `LeadActivity`.

---

# Alcance V1 Congelado

El alcance final para el desarrollo queda delimitado y cerrado estrictamente de la siguiente forma:

### En el Alcance (Dentro de la V1)
*   **Backend (FastAPI)**:
    *   CRUD completo de `Leads` (Físico en base de datos).
    *   Endpoints para crear y listar cronológicamente `LeadActivities`.
    *   Endpoint analítico `GET /metrics`.
    *   Inyección de dependencias y patrones Repository/Service Layer puros.
*   **Base de Datos (PostgreSQL)**:
    *   2 Tablas: `leads` y `lead_activities` con FK e integridad referencial (`ON DELETE CASCADE`).
    *   Índices compuesto `(status, created_at)` y único en `email`.
    *   Alembic para control de esquema (un único archivo inicial).
*   **Dashboard (NiceGUI)**:
    *   Página única con visualización por componentes dinámicos (Listado, Creación, Vista de Detalle).
    *   Tarjetas de KPI del embudo conectadas asíncronamente a `GET /metrics`.
    *   Línea de tiempo en el Detalle del Lead para registrar notas de seguimiento.
    *   Manejo visual elegante ante fallos de conexión HTTP con la API.
    *   Semillero (seeding) automático de leads de prueba en la primera inicialización.
*   **Testing**:
    *   Suite de tests unitarios (con mocks) para `LeadService`.
    *   Suite de tests de integración reales ejecutándose en Docker contra PostgreSQL temporal con rollback transaccional automático.

### Fuera del Alcance (Excluido de la V1)
*   **Autenticación y Autorización**: Sin inicio de sesión, roles ni políticas complejas de acceso.
*   **Edición/Borrado de Actividades**: Las actividades del lead son registros de auditoría inmutables.
*   **Eliminación Lógica**: No se manejan marcas de borrado lógico; el borrado es físico.
*   **Infraestructura Compleja**: Sin CQRS, sin arquitectura hexagonal estricta, sin colas de mensajería (Celery/Redis/RabbitMQ), sin base de datos en memoria y sin despliegue cloud.
