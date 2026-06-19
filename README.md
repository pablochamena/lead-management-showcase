# Lead & Customer Management System

*Showcase de Arquitectura Python: Backend con FastAPI, Interfaz Administrativa con NiceGUI y Persistencia con PostgreSQL*

---

## 1. Visión General

Este proyecto consiste en un sistema de gestión de leads y clientes potenciales (*CRM - Lead Management*), diseñado con fines demostrativos para servir como showcase de competencias profesionales en ingeniería de software backend e integración de sistemas.

La aplicación permite registrar, almacenar, clasificar y consultar información comercial de clientes potenciales de manera estructurada, exponiendo estas capacidades a través de una interfaz de programación de aplicaciones (API RESTful) limpia y autodocumentada, complementada por una interfaz de usuario administrativa desarrollada 100% en Python mediante NiceGUI.

### Habilidades y Tecnologías Demostradas

Este proyecto está concebido para reflejar la aplicación práctica de estándares de la industria en:

*   **Desarrollo Backend**: Python y FastAPI para la construcción de una API asíncrona, robusta y de alto rendimiento.
*   **Persistencia de Datos**: PostgreSQL como motor de base de datos relacional para garantizar la integridad y consistencia de los datos.
*   **Contenerización**: Docker y Docker Compose para asegurar entornos consistentes y portables.
*   **Arquitectura de Software**: Estructuración modular del código con una clara delimitación de responsabilidades.
*   **Diseño de APIs**: Definición de contratos claros basados en estándares abiertos (OpenAPI).
*   **Calidad y Pruebas**: Estrategia de testing integral y automatizable.
*   **Buenas Prácticas de Ingeniería**: Adopción de principios de desarrollo robustos y mantenibles en el tiempo.

---

## 2. Objetivos

### Objetivos Técnicos
*   **Baja Latencia y Rendimiento**: Diseñar una API backend asíncrona capaz de responder de forma eficiente bajo cargas típicas de un sistema comercial mediano.
*   **Arquitectura Desacoplada**: Implementar una estructura de componentes donde la lógica de negocio sea independiente de la infraestructura, el transporte (HTTP) y el mecanismo de persistencia.
*   **Consistencia de Datos**: Diseñar un esquema de base de datos relacional normalizado que maneje correctamente transacciones, restricciones y unicidad de leads.

### Objetivos de Aprendizaje y Demostración
*   **Pragmatismo frente a Sobreingeniería**: Demostrar la capacidad de construir una base de código sólida, escalable y mantenible para una aplicación pequeña/mediana, evitando patrones hiper-complejos innecesarios (como arquitecturas distribuidas complejas o microservicios prematuros) pero manteniendo la disciplina de separación de responsabilidades.
*   **Legibilidad y Mantenibilidad**: Escribir código que pueda ser leído, entendido y extendido de forma natural por otros ingenieros en un equipo de desarrollo profesional.

### Objetivos de Portfolio
*   Servir como referencia técnica para procesos de evaluación profesional, permitiendo a arquitectos de software, líderes técnicos y reclutadores auditar directamente decisiones de diseño, estilo de código, cobertura de pruebas y estructuración de sistemas.

---

## 3. Alcance Inicial

Para garantizar la entrega iterativa de valor y mantener el foco en la calidad de la base de código, se definen los siguientes límites para la primera versión de la aplicación:

### Dentro del Alcance (Fase Inicial)
*   **Operaciones CRUD de Leads**: Creación, consulta, edición básica y eliminación de leads.
*   **Métricas y Agregación (`GET /metrics`)**: Endpoint dedicado para obtener los totales agrupados por estado del lead, optimizando la carga de datos analíticos.
*   **Filtrado y Búsqueda**: Endpoints optimizados para filtrar clientes potenciales por estado y realizar búsquedas de texto parciales.
*   **Validación de Esquemas**: Validación estricta mediante Pydantic en los límites de la API.
*   **Persistencia Relacional**: Almacenamiento persistente en PostgreSQL con restricciones e índices adecuados.
*   **Entorno Contenerizado**: Configuración mediante Docker Compose para levantar base de datos, backend y frontend.
*   **Pruebas Automatizadas**: Cobertura de pruebas unitarias y de integración sobre la API y las reglas de negocio.
*   **Interfaz Visual (NiceGUI)**: Dashboard administrativo interactivo programado completamente en Python usando NiceGUI, eliminando la necesidad de JavaScript o frameworks web tradicionales en el frontend.

### Fuera del Alcance (Fases Posteriores)
*   **Autenticación y Autorización Compleja**: No se implementarán sistemas de control de acceso basados en roles (RBAC) complejos ni integraciones con proveedores de identidad externos (OAuth/OpenID) en la primera versión.
*   **Pipeline de Ventas y Automatizaciones**: Funcionalidades como tableros Kanban interactivos avanzados, envío automático de correos electrónicos de seguimiento o integraciones con herramientas de mensajería externa quedan excluidas temporalmente.
*   **Arquitectura de Microservicios o Mensajería Asíncrona**: No se incorporarán colas de tareas en segundo plano pesadas (como Celery) ni mensajería por eventos de manera inicial, resolviendo todos los flujos de forma síncrona/asíncrona directa dentro del propio proceso backend.

---

## 4. Principios y Patrones de Desarrollo

El desarrollo de este proyecto se rige por principios y patrones de ingeniería enfocados en mantenibilidad, desacoplamiento y consistencia:

*   **Clean Code & SOLID**: Código autodocumentado, fuertemente tipado y modular.
*   **Separation of Concerns (SoC)**: Capas bien definidas: Transporte (FastAPI), Negocio (Servicios) y Persistencia (Repositorios).
*   **Explicit is Better than Implicit**: Uso explícito de Type Hinting e Inyección de Dependencias.
*   **Testability First**: Estructuración pensada para facilitar la verificabilidad.
*   **Containerized Development**: Entorno reproducible basado en Docker, sin dependencias en el host.

> [!NOTE]
> Las especificaciones técnicas detalladas y los ejemplos de código para la implementación de estos patrones se encuentran en el catálogo de [Skills para Agentes](.agents/skills/).

---

## 5. Estrategia de Calidad y Pruebas

La calidad del software se garantiza de forma automatizada y continua mediante:

*   **Pruebas Unitarias**: Validación de reglas de negocio en total aislamiento (utilizando mocks).
*   **Pruebas de Integración**: Pruebas de extremo a extremo que interactúan con una base de datos PostgreSQL real ejecutada en entornos aislados.
*   **Validación Estricta**: Esquemas de datos estructurados e inmutables definidos en los límites del sistema.
*   **Manejo Global de Excepciones**: Respuestas de error estandarizadas que evitan la exposición de detalles internos de infraestructura.
*   **Entorno Reproducible**: Reglas estrictas de ejecución contenerizada para linters, formateadores y ejecución del sistema.

> [!IMPORTANT]
> Todo el desarrollo, herramientas de calidad (linters) y pruebas automatizadas corren exclusivamente bajo Docker, tal como se especifica en la [Guía de Agentes (GEMINI.md)](GEMINI.md).

---

## 6. Evolución Esperada

La arquitectura inicial de este showcase se concibe bajo el concepto de **arquitectura evolutiva**. Aunque la primera versión implementa un conjunto de funciones y un alcance delimitado, el diseño estructural e infraestructura del proyecto se realiza de modo que la introducción de nuevas funcionalidades sea ágil:

1.  **Extensibilidad en Persistencia**: El desacoplamiento de la base de datos mediante el patrón repositorio permitirá, si es necesario en el futuro, migrar el almacenamiento o introducir mecanismos de caché (ej: Redis) con un impacto mínimo en las capas de negocio.
2.  **Preparación para la Asincronía**: La naturaleza asíncrona nativa elegida para el backend facilita la futura migración de operaciones bloqueantes (como envío de reportes o procesamiento de leads) hacia colas de trabajo asíncronas en segundo plano.
3.  **Modularidad de Negocio**: La organización de dominios permitirá agregar nuevos módulos funcionales (como cotizaciones, notas o reuniones) de manera aditiva, reduciendo el riesgo de efectos colaterales en la lógica existente.

---

## 7. Estado Actual

El proyecto se encuentra formalmente en **Fase de Diseño Conceptual y Definición Arquitectónica**. 

Este documento de visión rectora representa la fase inicial ("Documentation-First") y sirve como el contrato de requerimientos y guías de calidad que regirán la posterior creación de la estructura del repositorio, el modelo de datos, la API y los tests asociados.

## Directorios Ignorados y Acceso a Documentación

Para mantener el historial de Git limpio de metadatos y documentación interna, existen directorios que están ignorados en el control de versiones (`.gitignore`):

*   **/docs/**: Contiene la documentación del proyecto (como el PRD, requerimientos, arquitectura, roadmap, etc.), exceptuando `README.md` y `GEMINI.md` que permanecen en la raíz.
*   **.agents/**: Contiene las configuraciones de subagentes y catálogo de skills del proyecto.

> [!IMPORTANT]
> **Acceso a datos locales:** Aunque estas carpetas no se suben al repositorio de Git, **existen localmente en el entorno de desarrollo**. Si necesitas consultar o leer su contenido para obtener contexto sobre la arquitectura, decisiones de diseño o el roadmap, debes hacerlo leyendo directamente los archivos del disco (por ejemplo, ejecutando comandos de visualización como `cat` o usando las herramientas de lectura del sistema).