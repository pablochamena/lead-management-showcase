# Guía de Agentes (GEMINI.md)

Este documento sirve como el manual de operaciones y mapa de arquitectura para los agentes de IA (como Gemini) que interactúan con esta base de código. Define los roles especializados (subagentes), las destrezas de programación requeridas (skills) y el entorno de ejecución restrictivo del proyecto.

---

## 1. Entorno de Ejecución Exclusivo: 100% Docker

> [!IMPORTANT]
> **REGLA DE INFRAESTRUCTURA OBLIGATORIA:** Todo el desarrollo, ejecución, linters y pruebas de este proyecto se realizan de manera exclusiva dentro de contenedores Docker.

*   **Sin Entornos Locales de Python**: Está terminantemente prohibido crear entornos virtuales locales (`venv`, `poetry`, `conda`, `pipenv`, etc.) o ejecutar comandos de Python/Pip directamente sobre la máquina host del desarrollador o del agente.
*   **Aislamiento Total**: Todas las dependencias de Python, herramientas de formateo y el servidor ASGI se instalan y ejecutan dentro del contenedor de la aplicación.
*   **Ejecución de Comandos**:
    *   **Levantar el entorno**: `docker compose up --build`
    *   **Ejecutar pruebas automatizadas**: `docker compose exec backend pytest`
    *   **Ejecutar formateadores/linters**: `docker compose exec backend black .` (o el comando de linter correspondiente).
    *   **Ejecutar migraciones**: `docker compose exec backend alembic upgrade head`

---

## 2. Mapa de Subagentes Especializados

En el directorio `.agents/` se encuentran definidos los perfiles de comportamiento para tareas específicas. Cada subagente está configurado para utilizar el modelo de lenguaje `gemini-3.5-flash-low`:

1.  **Code Implementer (`.agents/code-implementer.md`)**
    *   *Rol*: Desarrollador Backend Senior.
    *   *Responsabilidad*: Escribir la lógica de negocio, esquemas de API, adaptadores de base de datos y pruebas automatizadas siguiendo estrictamente las directrices de código.
2.  **Code Reviewer (`.agents/code-reviewer.md`)**
    *   *Rol*: Ingeniero de Control de Calidad / QA Senior.
    *   *Responsabilidad*: Auditar el código propuesto línea por línea, emitiendo veredictos (`APPROVED`, `APPROVED WITH SUGGESTIONS`, `REJECTED`) y categorizando los hallazgos en Bloqueantes (Critical), Sugerencias (Minor) y Aciertos (Kudos).
3.  **Spec Auditor (`.agents/spec-auditor.md`)**
    *   *Rol*: Ingeniero Principal de Producto.
    *   *Responsabilidad*: Proteger el proyecto contra el *scope creep* (expansión no planificada de requisitos) y la sobreingeniería, contrastando cualquier implementación con el alcance inicial del `README.md`.

---

## 3. Catálogo de Skills (Conocimientos Técnicos)

Las directrices técnicas detalladas de programación se encuentran bajo `.agents/skills/`. Todo agente debe consultar y validar su código contra estas guías antes de entregar resultados:

*   **[Patrón Repositorio](.agents/skills/repository_pattern.md)**: Abstracción de base de datos relacional. Restringe la lógica de negocio de usar consultas SQL o clases ORM directamente.
*   **[Capa de Servicios](.agents/skills/service_layer.md)**: Encapsulación de la lógica de negocio/casos de uso en servicios puros de Python. Mantiene las rutas de FastAPI limpias y desacopladas del negocio.
*   **[Inyección de Dependencias](.agents/skills/dependency_injection.md)**: Uso sistemático de inyección por constructores en clases y `Depends` en FastAPI para asegurar alta testabilidad y bajo acoplamiento.
*   **[Testabilidad Ante Todo](.agents/skills/testability_first.md)**: Especificaciones y patrones para escribir pruebas unitarias aisladas (con mocks) y pruebas de integración autocontenidas y transaccionales (con rollback).

---

## 4. Instrucciones para Nuevos Agentes
Si eres un nuevo agente trabajando en este repositorio:
1.  Lee el archivo `README.md` para entender qué es el proyecto y cuál es el alcance inicial.
2.  Lee este archivo (`GEMINI.md`) para entender bajo qué reglas de entorno opera el proyecto.
3.  Cuando el usuario te asigne una tarea (ej: crear un endpoint, testear un servicio, revisar código), lee el subagente correspondiente en `.agents/` y adopta su comportamiento y formato de salida.
4.  Antes de codificar, consulta la skill adecuada en `.agents/skills/` para replicar exactamente los patrones estructurales aprobados.
