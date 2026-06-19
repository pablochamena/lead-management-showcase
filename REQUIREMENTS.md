# Especificación de Requerimientos (REQUIREMENTS.md)

---

## 1. Modelo de Datos

### Entidad "Lead" (Cliente Potencial)
El recurso principal del sistema se define con los siguientes campos y restricciones:

| Campo (Código) | Equivalente | Tipo | Restricciones / Reglas | Descripción |
| :--- | :--- | :--- | :--- | :--- |
| `id` | id | Entero | Autoincremental, Clave Primaria | Identificador único del lead. |
| `name` | nombre | Texto | Obligatorio, Máx. 100 caracteres | Nombre completo o razón social del cliente. |
| `company` | empresa | Texto | Opcional, Máx. 100 caracteres | Empresa u organización a la que pertenece. |
| `email` | email | Texto | Obligatorio, Formato de email válido, Único | Dirección de correo de contacto principal. |
| `phone` | telefono | Texto | Opcional, Máx. 20 caracteres | Número telefónico de contacto. |
| `status` | estado | Texto | Obligatorio, Valores restringidos | Estado comercial en el embudo de ventas. |
| `created_at` | fecha_creacion | Fecha/Hora | Automático (UTC) | Registro del momento exacto de la creación. |
| `updated_at` | fecha_actualizacion | Fecha/Hora | Automático (UTC) | Registro de la última modificación realizada. |

### Entidad "LeadActivity" (Historial de Actividad)
Representa una nota o interacción de seguimiento realizada sobre un Lead específico (Relación 1:N):

| Campo (Código) | Tipo | Restricciones / Reglas | Descripción |
| :--- | :--- | :--- | :--- |
| `id` | Entero | Autoincremental, Clave Primaria | Identificador único de la actividad. |
| `lead_id` | Entero | ForeignKey (`leads.id`), NotNull, ON DELETE CASCADE | Relación con el Lead asociado. |
| `type` | Texto | Obligatorio, Valores restringidos (Enum) | Tipo de interacción efectuada. |
| `notes` | Texto | Obligatorio | Detalle textual o notas de la interacción. |
| `created_at` | Fecha/Hora | Automático (UTC) | Fecha y hora en que se registró la actividad. |

---

## 2. Casos de Uso del Sistema

### UC-01: Crear Lead
*   **Descripción**: Permite registrar un nuevo prospecto en la base de datos.
*   **Entradas**: `name` (Texto), `email` (Texto), opcionalmente `company` (Texto) y `phone` (Texto).
*   **Comportamiento**:
    1.  El sistema valida que el email tenga un formato sintácticamente válido.
    2.  El sistema verifica que el email no exista registrado en la base de datos (Regla: Email Único).
    3.  El sistema asigna de forma automática el estado inicial: `NEW`.
    4.  El sistema registra las marcas de tiempo (`created_at` y `updated_at`).
    5.  Se persiste el registro y se retorna el Lead con su ID asignado.

### UC-02: Actualizar Lead
*   **Descripción**: Permite modificar la información de un lead existente (datos básicos o estado comercial).
*   **Entradas**: `id` (Entero, identificador), opcionalmente `name` (Texto), `company` (Texto), `phone` (Texto) y `status` (Texto).
*   **Comportamiento**:
    1.  El sistema valida que el lead con el ID provisto exista. Si no existe, lanza un error de "No encontrado".
    2.  Si se incluye el campo `status`, el sistema valida que sea un valor del listado permitido (Regla: Status Restringido).
    3.  El sistema actualiza la fecha `updated_at` al momento actual.
    4.  Se persisten los cambios y se retorna el objeto actualizado.

### UC-03: Buscar y Listar Leads
*   **Descripción**: Permite consultar el listado de leads aplicando filtros y paginación.
*   **Entradas (Opcionales)**: 
    *   `status` (Filtrar por estado exacto).
    *   `query` (Búsqueda parcial en campos `name`, `email` o `company`).
    *   `skip` / `limit` (Parámetros para paginación básica).
*   **Comportamiento**:
    1.  El sistema aplica los filtros indicados de forma acumulativa.
    2.  Si se proporciona `query`, se realiza una búsqueda insensible a mayúsculas/minúsculas (LIKE / ILIKE) sobre el nombre, correo o empresa del lead.
    3.  Retorna un listado de leads ordenados por fecha de creación descendente (`created_at` DESC) junto con sus estados actuales.

### UC-04: Eliminar Lead
*   **Descripción**: Remueve permanentemente a un lead y todas sus actividades asociadas de la base de datos (borrado físico).
*   **Entradas**: `id` (Entero).
*   **Comportamiento**:
    1.  El sistema valida que el ID exista en la base de datos. Si no existe, lanza un error de "No encontrado".
    2.  Remueve físicamente el registro de la base de datos (la cascada en BD eliminará automáticamente las actividades asociadas).

### UC-05: Obtener Métricas de Leads
*   **Descripción**: Retorna la cantidad total de leads agrupados de manera analítica por su estado comercial actual para alimentar los indicadores del Dashboard.
*   **Entradas**: Ninguna.
*   **Comportamiento**:
    1.  El sistema realiza una consulta de agregación (GROUP BY) en la base de datos contando la cantidad de registros por cada valor de `status`.
    2.  Retorna una estructura JSON con el mapeo de totales por estado (ej: `{"new": 25, "contacted": 10, "qualified": 5, "lost": 3}`).

### UC-06: Registrar Actividad en Lead
*   **Descripción**: Registra una nueva interacción o nota de seguimiento vinculada a un prospecto.
*   **Entradas**: `lead_id` (Entero), `type` (Texto) y `notes` (Texto).
*   **Comportamiento**:
    1.  El sistema valida que el lead con el `lead_id` provisto exista. Si no, lanza un error de "No encontrado".
    2.  El sistema valida que `type` corresponda a un tipo de actividad permitido (Regla: Tipo de Actividad Restringido).
    3.  Registra la fecha y hora de creación automática (`created_at`).
    4.  Persiste el registro de actividad y lo retorna.

### UC-07: Obtener Historial de Actividades
*   **Descripción**: Recupera la cronología completa de notas e interacciones de un lead específico.
*   **Entradas**: `lead_id` (Entero).
*   **Comportamiento**:
    1.  El sistema valida que el lead con el `lead_id` exista. Si no, lanza un error de "No encontrado".
    2.  Consulta las actividades asociadas al lead, ordenadas cronológicamente de forma descendente (`created_at` DESC).
    3.  Retorna la lista de actividades.

---

## 3. Reglas de Negocio Críticas
1.  **Email Único**: No se permite la coexistencia de dos leads registrados con la misma dirección de correo electrónico.
2.  **Ciclo de Vida / Estados Permisibles**: El campo `status` solo puede contener uno de los siguientes valores exactos:
    *   `NEW`: Prospecto recién registrado sin contacto previo.
    *   `CONTACTED`: Se ha iniciado comunicación con el prospecto.
    *   `QUALIFIED`: Se confirma que el prospecto cumple con el perfil de cliente potencial.
    *   `LOST`: El proceso de venta finaliza sin éxito.
3.  **Tipo de Actividad Restringido**: El campo `type` en `LeadActivity` solo puede contener uno de los siguientes valores exactos:
    *   `CALL`: Llamada telefónica.
    *   `EMAIL`: Envío o recepción de correo electrónico.
    *   `NOTE`: Nota general de seguimiento o reunión.
4.  **Inmutabilidad de Actividades**: Una vez persistida una actividad, no puede ser modificada ni eliminada de manera individual (registro histórico inmutable).
5.  **Inmutabilidad de Tiempos**: El campo `created_at` es inmutable una vez generado. El campo `updated_at` en Leads debe ser actualizado de forma automática por la persistencia en cualquier evento de modificación.
