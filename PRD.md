# Product Requirements Document (PRD)

---

## 1. Introducción
Este documento define la justificación de negocio, los objetivos de producto y las necesidades del usuario final que motivan el desarrollo del **Lead & Customer Management System**. El enfoque aquí es puramente comercial y de valor de producto, sin entrar en detalles tecnológicos.

---

## 2. El Problema
Las pequeñas empresas, consultores independientes y equipos comerciales emergentes suelen gestionar su captación de clientes de forma descentralizada e ineficiente (hojas de cálculo compartidas, notas adhesivas, bandejas de entrada de correo sin clasificar). 

Este desorden operativo genera tres problemas principales:
*   **Pérdida de Información**: Olvido de datos clave de contacto y de los requerimientos iniciales de los prospectos.
*   **Falta de Seguimiento**: Incapacidad para saber con precisión cuándo fue el último contacto o en qué estado de negociación se encuentra el prospecto.
*   **Fricción de Entrada**: Los CRMs tradicionales del mercado son complejos de configurar, costosos y con interfaces sobrecargadas, lo que desincentiva su uso diario en equipos pequeños.

---

## 3. El Usuario (User Persona)
El sistema está diseñado para dos perfiles de usuario clave:

### A. El Ejecutivo Comercial (Usuario de Negocio)
*   **Perfil**: Un profesional enfocado en el cierre de ventas que necesita agilidad.
*   **Necesidades**: 
    *   Registrar un cliente potencial en menos de 10 segundos.
    *   Visualizar rápidamente sus contactos activos sin navegar por menús complejos.
    *   Actualizar el estado del cliente de forma rápida para mantener su cartera comercial al día.

### B. El Evaluador Técnico (Usuario del Showcase)
*   **Perfil**: Un líder técnico o reclutador que audita este proyecto como portfolio.
*   **Necesidades**:
    *   Ver cómo se traduce una necesidad de negocio simple en una arquitectura de software limpia y desacoplada.
    *   Confirmar que el alcance comercial esté estrictamente cubierto por el código implementado, sin añadir funcionalidades o complejidades artificiales.

---

## 4. La Solución
Un sistema centralizado de gestión de leads (*CRM simplificado*) que proporciona una interfaz de programación de aplicaciones (API) estable y una interfaz administrativa en Python de alta velocidad. La solución se enfoca exclusivamente en resolver el registro, la clasificación y el seguimiento inicial del embudo de ventas del lead de forma estructurada y limpia.

---

## 5. Beneficio Comercial
*   **Centralización y Consistencia**: Una única fuente de verdad para los leads, evitando correos duplicados y bases de datos dispersas.
*   **Optimización del Tiempo de Respuesta**: Al reducir la fricción en la carga y búsqueda de datos, el equipo puede responder y atender prospectos de forma más rápida.
*   **Visión Clara del Embudo**: Facilita a los tomadores de decisiones saber de un vistazo cuántos prospectos se encuentran activos y cuántos se han perdido o calificado.

---

## 6. Alcance del Producto (Fase Inicial)
Para garantizar la entrega ágil de valor, el producto se limita a:

*   **Captura de Leads**: Registro con nombre, empresa, teléfono y correo electrónico validado.
*   **Gestión del Estado del Lead**: Permitir la transición del lead por un flujo lógico simple (`Nuevo` -> `Contactado` -> `Calificado` o `Perdido`).
*   **Métricas del Embudo**: Consulta agregada de la salud del embudo (KPI Cards) a través del backend.
*   **Búsqueda Rápida**: Un filtro por texto y por estado para ubicar clientes en segundos desde el dashboard.
*   **Dashboard Visual (NiceGUI)**: Interfaz de usuario interactiva desarrollada en Python mediante NiceGUI que consume el API en tiempo real para visualizar, monitorear y gestionar los prospectos.
