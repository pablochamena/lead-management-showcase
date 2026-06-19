# SKILL: Inyección de Dependencias (Dependency Injection)

Este documento define las reglas de diseño para la gestión de dependencias y su inyección a lo largo del ciclo de vida de la aplicación.

---

## 1. Propósito y Contexto
La **Inyección de Dependencias (DI)** es clave para cumplir con el Principio de Inversión de Dependencias (D). En lugar de que un componente cree o instancie los servicios o bases de datos que necesita, estas le son "inyectadas" desde el exterior. Esto permite desacoplar los componentes de su infraestructura y simplifica drásticamente las pruebas automatizadas (mocking).

### Cuándo usar esta Skill
*   Al crear un nuevo servicio que requiere acceso a repositorios u otros servicios.
*   Al registrar nuevas dependencias de infraestructura en la capa HTTP.
*   Al configurar suites de pruebas y sobreescribir dependencias de producción.

---

## 2. Reglas Arquitectónicas
1.  **DI Basada en Constructor**: Las clases de negocio (servicios) e infraestructura (repositorios) deben recibir sus dependencias a través del método `__init__`. No deben instanciar dependencias de forma interna ni usar variables globales.
2.  **DI de FastAPI (Depends)**: Para el cableado de la capa web, se utiliza el sistema declarativo `Depends` de FastAPI. Esto permite resolver de manera limpia el ciclo de vida de recursos como las conexiones/sesiones a base de datos.
3.  **Abstracción en Proveedores**: Los proveedores de dependencias deben instanciar y retornar los repositorios concretos implementando las interfaces abstractas de negocio.
4.  **Soporte para Pruebas (Overrides)**: La inyección de dependencias en las rutas debe permitir la sobreescritura de dependencias mediante el diccionario `app.dependency_overrides` de FastAPI durante las pruebas de integración.

---

## 3. Ejemplo de Código de Referencia

### A. Proveedores de Dependencias (Capa de API/Infraestructura)
Ubicación sugerida: `src/api/dependencies.py`

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from src.infrastructure.database.session import get_db_session  # Generador de sesiones SQL
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.repositories.sqlalchemy_lead_repository import SQLAlchemyLeadRepository
from src.services.lead_service import LeadService

def get_lead_repository(db: Session = Depends(get_db_session)) -> LeadRepository:
    """Proveedor para el repositorio de leads. Retorna la interfaz abstracta."""
    return SQLAlchemyLeadRepository(db_session=db)

def get_lead_service(repo: LeadRepository = Depends(get_lead_repository)) -> LeadService:
    """Proveedor para el servicio de leads. Inyecta el repositorio."""
    return LeadService(lead_repository=repo)
```

### B. Consumo en Rutas FastAPI
```python
from fastapi import APIRouter, Depends
from src.services.lead_service import LeadService
from src.api.dependencies import get_lead_service

router = APIRouter()

@router.get("/{lead_id}")
def read_lead(lead_id: int, service: LeadService = Depends(get_lead_service)):
    # El servicio ya viene inicializado con su repositorio y sesión de base de datos
    return service.get_lead(lead_id)
```

### C. Sobreescritura en Entornos de Test
```python
from fastapi.testclient import TestClient
from src.main import app
from src.api.dependencies import get_lead_service

class MockLeadService:
    def get_lead(self, lead_id: int):
        return {"id": lead_id, "name": "Lead Ficticio", "email": "mock@example.com"}

client = TestClient(app)

# Sobreescribir el proveedor real por el mock antes de ejecutar los tests de integración
app.dependency_overrides[get_lead_service] = lambda: MockLeadService()

def test_read_lead_endpoint():
    response = client.get("/leads/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Lead Ficticio"
    
    # Limpiar overrides después del test
    app.dependency_overrides.clear()
```

---

## 4. Checklist de Validación para el Agente
Antes de dar por concluida una tarea que implique inyección de dependencias, comprueba que:
- [ ] ¿Los constructores de tus clases reciben interfaces/abstracciones en lugar de implementaciones rígidas?
- [ ] ¿El ciclo de vida de la conexión a la base de datos (sesión de SQLAlchemy) está gestionado mediante dependencias de FastAPI (`yield db` con cierre automático)?
- [ ] ¿Has evitado el uso de variables globales para almacenar instancias de repositorios o servicios?
- [ ] ¿Los proveedores en `src/api/dependencies.py` tienen anotaciones de tipo claras tanto en los argumentos como en el tipo de retorno?
- [ ] ¿Es posible instanciar las clases en un entorno de pruebas unitarias puras pasando stubs o mocks directamente al constructor sin inicializar FastAPI?
