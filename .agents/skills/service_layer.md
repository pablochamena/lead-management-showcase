# SKILL: Capa de Servicios (Service Layer)

Este documento define la regla de diseño y el estándar de codificación para la orquestación de la lógica de negocio (casos de uso) en este proyecto.

---

## 1. Propósito y Contexto
La **Capa de Servicios** actúa como el núcleo de la aplicación, encapsulando las reglas de negocio y coordinando el flujo de datos entre la capa de entrada/transporte (FastAPI) y la capa de datos (Repositorios). Asegura que la API HTTP sea solo una interfaz de comunicación intercambiable.

### Cuándo usar esta Skill
*   Al añadir nuevos endpoints que ejecutan alguna regla de negocio.
*   Al validar reglas comerciales (ej: "no se puede duplicar un lead activo con el mismo email").
*   Al estructurar nuevos flujos transaccionales.

---

## 2. Reglas Arquitectónicas
1.  **Endpoints Delgados (Thin Controllers)**: Las rutas de FastAPI (`@app.get`, `@app.post`, etc.) solo deben ocuparse de:
    *   Extraer parámetros de la URL, query o cuerpo (validación Pydantic de entrada).
    *   Llamar a un método de la Capa de Servicios.
    *   Retornar la respuesta en el formato adecuado con su código de estado HTTP (validación Pydantic de salida).
    *   No debe haber lógica de base de datos ni validación de negocio dentro de las funciones de ruta.
2.  **Independencia de Framework**: La capa de servicio no debe importar nada procedente del framework web (`fastapi`, `starlette`). Debe ser código Python puro para garantizar portabilidad.
3.  **Excepciones de Dominio**: Los servicios deben lanzar excepciones de negocio personalizadas (ej: `LeadAlreadyExistsError`, `LeadNotFoundError`) en lugar de excepciones HTTP directas (`HTTPException`). La conversión a códigos de estado HTTP se realiza en la capa de API o mediante manejadores de excepciones globales.

---

## 3. Ejemplo de Código de Referencia

### A. Definición de Excepciones y Caso de Uso (Capa de Servicio)
Ubicación sugerida: `src/services/lead_service.py`

```python
from src.domain.entities import Lead
from src.domain.repositories.lead_repository import LeadRepository

# Excepciones de negocio personalizadas (Heredan de Exception, no de HTTPException)
class LeadDomainError(Exception):
    pass

class LeadNotFoundError(LeadDomainError):
    pass

class LeadAlreadyExistsError(LeadDomainError):
    pass


class LeadService:
    def __init__(self, lead_repository: LeadRepository):
        self.repository = lead_repository

    def create_new_lead(self, name: str, email: str) -> Lead:
        # 1. Regla de negocio: Validar duplicidad
        existing = self.repository.get_by_email(email)
        if existing:
            raise LeadAlreadyExistsError(f"El lead con email '{email}' ya se encuentra registrado.")
        
        # 2. Crear entidad de dominio
        new_lead = Lead(name=name, email=email, status="NEW")
        
        # 3. Persistir usando el repositorio abstracto
        saved_lead = self.repository.save(new_lead)
        return saved_lead

    def get_lead(self, lead_id: int) -> Lead:
        lead = self.repository.get_by_id(lead_id)
        if not lead:
            raise LeadNotFoundError(f"Lead con ID {lead_id} no fue encontrado.")
        return lead
```

### B. Consumo en la Capa API (Controlador Delgado)
Ubicación sugerida: `src/api/routes/leads.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from src.api.schemas.leads import LeadCreateSchema, LeadResponseSchema
from src.services.lead_service import LeadService, LeadNotFoundError, LeadAlreadyExistsError
from src.api.dependencies import get_lead_service  # Ver Skill de Inyección de Dependencias

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post("/", response_model=LeadResponseSchema, status_code=status.HTTP_201_CREATED)
def create_lead(payload: LeadCreateSchema, service: LeadService = Depends(get_lead_service)):
    try:
        lead = service.create_new_lead(name=payload.name, email=payload.email)
        return lead
    except LeadAlreadyExistsError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
```

---

## 4. Checklist de Validación para el Agente
Antes de dar por concluida una tarea de servicio, comprueba que:
- [ ] ¿Los archivos en la capa de servicios están libres de importaciones de `fastapi` u otros frameworks de transporte?
- [ ] ¿Los endpoints de la API delegan toda la lógica en un servicio en lugar de procesar los datos directamente?
- [ ] ¿Las validaciones de negocio están ubicadas dentro de la capa de servicio y lanzan excepciones de dominio propias?
- [ ] ¿El servicio recibe todas sus dependencias (como repositorios o clientes externos) a través de su constructor?
- [ ] ¿La capa de servicio es completamente testable de forma unitaria reemplazando los repositorios abstractos con mocks?
