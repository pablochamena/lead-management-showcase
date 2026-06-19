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

---

## 5. Directorios Ignorados y Acceso a Documentación

Para mantener el historial de Git limpio de metadatos y documentación interna, existen directorios que están ignorados en el control de versiones (`.gitignore`):

*   **/docs/**: Contiene la documentación del proyecto (como el PRD, requerimientos, arquitectura, roadmap, etc.), exceptuando `README.md` y `GEMINI.md` que permanecen en la raíz.
*   **.agents/**: Contiene las configuraciones de subagentes y catálogo de skills del proyecto.

> [!IMPORTANT]
> **Acceso a datos locales:** Aunque estas carpetas no se suben al repositorio de Git, **existen localmente en el entorno de desarrollo**. Si necesitas consultar o leer su contenido para obtener contexto sobre la arquitectura, decisiones de diseño o el roadmap, debes hacerlo leyendo directamente los archivos del disco (por ejemplo, ejecutando comandos de visualización como `cat` o usando las herramientas de lectura del sistema).

## 6. Estrategia de Git y Control de Versiones Obligatorio

> [!IMPORTANT]
> **REGLA DE RAMIFICACIÓN:** Está terminantemente prohibido realizar commits directos sobre la rama `main`. El desarrollo debe avanzar estrictamente de forma secuencial mediante ramas asociadas a los Milestones del `ROADMAP.md`.

* **Nomenclatura de Ramas**: `feature/M<Número>-<nombre-corto>` (Ejemplo: `feature/M2-base-structure`).
* **Flujo de Trabajo por Milestone**:
    1. Al iniciar un Milestone, el agente debe verificar que está parado en la rama del Milestone anterior (o `main` si es el M1) y crear la nueva rama.
    2. Al finalizar el desarrollo y cumplir el 100% del Definition of Done (DoD) del Milestone, el agente debe realizar el commit con un mensaje descriptivo y profesional (siguiendoConventional Commits si es posible, ej: `feat(infra): complete docker setup and verify connections`).
    3. El agente debe realizar el `git push origin feature/M...` hacia el repositorio remoto.
    4. **Simulación de PR / Fusión**: Una vez que el usuario apruebe el resultado en el chat, el agente cambiará a `main`, fusionará la rama del hito (`git merge --no-ff`) y subirá `main` al remoto. Jamás se borran las ramas de los Milestones anteriores para mantener el historial como showcase.

