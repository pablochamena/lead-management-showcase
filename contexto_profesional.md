# Presentación Profesional

Desarrollador de software especializado en el diseño e implementación de sistemas automatizados de ingesta, clasificación y estructuración de datos. Mi experiencia se centra en construir flujos de procesamiento para extraer información útil de fuentes de texto no estructurado, tales como correos electrónicos y pliegos de licitaciones públicas. A través del uso de Python, bases de datos (SQL y NoSQL) y técnicas de procesamiento de lenguaje natural y recuperación de información (RAG), automatizo la recolección de datos y la generación de registros estructurados listos para ser consumidos por herramientas de análisis o sistemas de consulta.


# Especialización

* **Desarrollo Backend y REST APIs:** Diseño e implementación de la lógica de servidor en Python, asegurando consistencia de datos, control de errores y modularidad.
* **Automatización de Pipelines de Datos:** Construcción de flujos automatizados para la ingesta, transformación, validación y almacenamiento estructurado de información.
* **Integración de Modelos de Inteligencia Artificial:** Incorporación de modelos de procesamiento de lenguaje natural para clasificación de documentos y extracción de datos en flujos tradicionales.
* **Optimización de Bases de Datos Relacionales:** Diagnóstico, reestructuración y optimización de rendimiento de esquemas de bases de datos relacionales (PostgreSQL).
* **DevOps y Contenerización:** Aislamiento de entornos y configuración de despliegues en servidores cloud utilizando Docker.

# Experiencia Profesional

* **Python Engineer - Automatización e Infraestructura Backend | Empresa de Servicios Tecnológicos (Noviembre 2024 - Presente):**
  * Desarrollo de sistemas de automatización e ingesta de datos desestructurados provenientes de correos, archivos PDF y plataformas externas.
  * Optimización lógica de consultas SQL e indexación estratégica en bases de datos PostgreSQL para reducir tiempos de respuesta y costos de servidores cloud.
  * Desarrollo e integración de REST APIs e interconexión de servicios de terceros con lógica de reintentos y tolerancia a fallos.
  * Estandarización de entornos de desarrollo y producción utilizando contenedores Docker.

# Tecnologías y Herramientas

* **Lenguajes de programación:** Python, SQL.
* **Bases de datos:** PostgreSQL, MySQL, DynamoDB.
* **Contenerización y control de versiones:** Docker, Git, GitHub.
* **Infraestructura Cloud:** AWS, Google Cloud Platform (GCP).
* **Integraciones:** REST APIs, sistemas de recuperación de información (RAG) y APIs de modelos de lenguaje.

# Proyectos Destacados

* **Automatización de Procesamiento de Notas de Prensa:** Sistema en Python y DynamoDB para ingesta continua de correos electrónicos mediante API, con clasificación automática y extracción de contactos y entidades.
* **Procesamiento Inteligente de Licitaciones Públicas:** Pipeline en Python para la descarga automática de documentos desde una API, clasificación y extracción textual de pliegos, y estructuración de los datos para sistemas RAG.


# Caso de Estudio 1 - Automatización de Procesamiento de Noticias

## Contexto
La organización recibe diariamente entre cientos y miles de notas de prensa en una cuenta de correo electrónico accesible mediante una API.

## Situación Inicial
Previo al proyecto, no existía un procesamiento automatizado de estos correos. La información permanecía en el buzón sin ser analizada ni almacenada de forma estructurada.

## Problema
Para identificar oportunidades comerciales, una persona debía revisar manualmente cada correo, copiar su contenido, enviarlo a herramientas de inteligencia artificial para su análisis y, con base en el resultado, intentar redactar una propuesta comercial de forma manual. Este proceso dependía completamente de la intervención humana, no era escalable y requería un alto tiempo de ejecución.

## Solución Implementada
Desarrollé un sistema en Python que descarga los correos de forma continua mediante la API, clasifica el texto de las notas de prensa según su contenido y extrae datos específicos (nombres de contactos y entidades mencionadas). Los datos resultantes se normalizan y se almacenan de forma estructurada en DynamoDB, lo que permite realizar consultas directas y alimentar otros flujos automáticos o herramientas de análisis.

## Mi Participación
Lideré y ejecuté el desarrollo completo del proyecto. Diseñé la arquitectura del flujo de procesamiento de datos, implementé los procesos de ingesta y extracción en Python, y definí el modelo de datos para su almacenamiento en DynamoDB.

## Qué ganó la organización
La organización eliminó el trabajo manual de lectura preliminar de correos. Obtuvo una base de datos estructurada con información histórica de notas de prensa procesadas, evitando que los datos se perdieran en el buzón.

## Capacidades nuevas que obtuvo la organización
* Clasificación automática y continua de altos volúmenes de correos electrónicos de notas de prensa.
* Extracción desatendida de contactos y entidades a partir del texto de los correos.
* Disponibilidad de una base de datos estructurada para alimentar futuras herramientas de análisis y procesos comerciales.

## Tecnologías principales
* Python
* DynamoDB

## Aprendizajes técnicos
* Implementación de flujos de ingesta y procesamiento continuo en Python para el tratamiento de volúmenes variables de correos electrónicos mediante API.
* Modelado y almacenamiento de datos no relacionales en DynamoDB para persistir de manera eficiente la información clasificada y las entidades extraídas.


# Caso de Estudio 2 - Procesamiento Inteligente de Licitaciones

## Contexto
La organización mantiene una hemeroteca de licitaciones públicas.

## Situación Inicial
Antes del proyecto, únicamente se almacenaban referencias básicas sobre las licitaciones y enlaces a los documentos adjuntos. El contenido de los documentos no se procesaba ni se estructuraba.

## Problema
Al permanecer la información de los pliegos en documentos sin procesar, no podía ser explotada de forma eficiente por productos de inteligencia artificial ni para análisis avanzados.

## Solución Implementada
Desarrollé un flujo automatizado en Python que obtiene licitaciones públicas a través de una API, extrae el texto de los documentos adjuntos, lo clasifica mediante inteligencia artificial y genera registros organizados. El sistema procesa los documentos de valor para la organización y prepara los datos en un formato apto para sistemas de recuperación de información (RAG).

## Mi Participación
Diseñé y desarrollé el flujo completo de procesamiento, abarcando la extracción de texto de los documentos, la clasificación mediante modelos de lenguaje, la estructuración de la información y la preparación de los datos para sistemas de recuperación de información.

## Qué ganó la organización
La organización pasó de almacenar únicamente referencias documentales a disponer de conocimiento estructurado listo para alimentar productos basados en inteligencia artificial.

## Capacidades nuevas que obtuvo la organización
* Procesamiento, extracción y clasificación automática del contenido de pliegos de licitaciones públicas.
* Disponibilidad de datos estructurados para su uso en sistemas RAG.

## Tecnologías principales
* Python

## Aprendizajes técnicos
* Desarrollo en Python de arquitecturas de procesamiento documental orientadas a la preparación de datos para sistemas RAG.

## Productos habilitados por la solución
* Herramientas de generación asistida de pliegos administrativos.
* Herramientas de generación asistida de pliegos técnicos.
* Soluciones operativas para empresas que participan en licitaciones públicas.
* Sistemas de alertas basados en contenido documental.
* Productos de análisis y recuperación de información documental.

## Impacto estratégico
El procesamiento del contenido de los documentos de licitaciones públicas habilitó la creación de nuevos servicios y herramientas internas basadas en datos estructurados y recuperación de información.


# Arquitectura e Infraestructura

* **Bases de datos:** Optimización del rendimiento de esquemas de bases de datos PostgreSQL mediante optimización lógica de consultas SQL e indexación estratégica.
* **Integración de APIs:** Diseño e implementación de REST APIs e intercomunicación de servicios con mecanismos de tolerancia a fallos y lógicas de reintento.
* **Contenerización y Despliegues:** Uso de Docker para asegurar la portabilidad de aplicaciones backend en entornos cloud (AWS y Google Cloud Platform).

# Automatización e Inteligencia Artificial

* **Procesamiento documental y de texto:** Desarrollo de flujos para extraer, clasificar y estructurar contenido de correos y documentos PDF.
* **Integración de Modelos de Lenguaje:** Conexión de flujos de código estructurados con modelos de procesamiento de lenguaje natural y preparación de datos para sistemas RAG (Generación Aumentada por Recuperación).
* **Extracción de datos (Web Scraping):** Diseño de scripts autónomos para recolectar información estructurada desde plataformas externas mediante API y técnicas de extracción de datos.

# Principales Logros

* **Automatización integral de ingesta de notas de prensa:** Diseño y desarrollo completo de un sistema en Python que procesa miles de correos diarios y almacena los datos estructurados en DynamoDB.
* **Pipeline de extracción para licitaciones públicas:** Implementación de un flujo automático para procesar, clasificar y estructurar contenido de pliegos de licitaciones orientándolo a sistemas RAG.
* **Optimización de base de datos productiva:** Reducción de tiempos de respuesta en PostgreSQL y costos asociados a servidores mediante reindexación estratégica y optimización lógica de consultas en entornos de producción.
* **Certificación técnica:** Aprobación del examen de certificación en patrones de diseño y arquitectura limpia con una puntuación del 86% en 2026.

# Problemas que Sé Resolver

* **Pérdida de valor de información no estructurada:** Migración de procesos manuales basados en lectura o copiado de archivos (PDFs, correos) hacia bases de datos estructuradas y automatizadas.
* **Cuellos de botella en bases de datos:** Diagnóstico y resolución de problemas de lentitud de consultas y consumo excesivo de recursos en PostgreSQL.
* **Dependencia de procesos manuales repetitivos:** Sustitución de flujos manuales lentos por scripts e integraciones en Python autónomas y libres de intervención humana constante.
* **Inconsistencias en despliegues:** Estandarización del software y su entorno utilizando contenedores Docker para asegurar que se comporte de manera consistente en desarrollo y producción.

# Servicios que Puedo Ofrecer

* **Automatización de flujos de procesamiento de datos (End-to-End):** Diseño y desarrollo de sistemas para automatizar procesos manuales de ingesta y estructuración de datos. Construcción de soluciones listas para producción a partir de especificaciones iniciales, gestionando la arquitectura, la lógica de negocio y la persistencia de forma independiente sin requerir supervisión constante.


# Diferenciadores Profesionales

* **Sólida base en patrones de diseño y modularidad:** Dominio y aplicación verificable de patrones de arquitectura y principios SOLID (respaldado por certificación técnica con 86% de calificación).
* **Autonomía total en el desarrollo:** Capacidad para liderar todo el ciclo del proyecto (diseño, base de datos, backend y despliegue) sin requerir supervisión o micro-gestión por parte del cliente.
* **Enfoque en la eficiencia operativa:** Priorización de soluciones que disminuyan costos de servidores y reduzcan los tiempos de procesamiento manual, impactando directamente en la operatividad del negocio.

# Evidencias y Material para Portfolio

* **Código fuente del pipeline de notas de prensa:** Repositorio público con la implementación del flujo de ingesta, clasificación y persistencia en Python y DynamoDB.
* **Código fuente del pipeline de licitaciones públicas:** Repositorio demostrativo del procesamiento documental de pliegos y la preparación de índices para sistemas RAG.
* **Certificado digital de patrones de diseño:** Enlace a la acreditación de la calificación del 86% obtenida en 2026.
* **Diagramas de arquitectura técnica:** Modelos y flujogramas de datos de los pipelines de ingesta implementados.

