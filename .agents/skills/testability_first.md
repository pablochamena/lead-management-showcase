# SKILL: Testabilidad ante todo (Testability First)

Este documento establece las directrices de diseño y codificación para asegurar la verificabilidad automatizada de la aplicación mediante pruebas unitarias y de integración.

---

## 1. Propósito y Contexto
La **Testabilidad** es una característica arquitectónica de primer nivel. Un código difícil de testear suele reflejar un mal diseño (alto acoplamiento, dependencias ocultas o falta de cohesión). Esta skill guía al agente para escribir código estructurado que facilite la escritura de pruebas veloces y fiables.

### Cuándo usar esta Skill
*   Al crear cualquier nueva funcionalidad (escribir tests concurrentemente).
*   Al refactorizar código existente para asegurar que no se introducen regresiones.
*   Al configurar clientes, adaptadores o servicios externos.

---

## 2. Reglas de Testing
1.  **Doble Suite (Unit + Integration)**: El proyecto contará con dos conjuntos de pruebas diferenciados:
    *   **Pruebas Unitarias**: Rápidas y asiladas. Prueban lógica de negocio pura en la capa de servicios y entidades. Tienen prohibido realizar llamadas de red, acceder a bases de datos reales o interactuar con el sistema de archivos.
    *   **Pruebas de Integración**: Prueban la interacción de componentes. Validan endpoints HTTP contra la base de datos real (ejecutándose en aislamiento) y verifican flujos transaccionales.
2.  **Mocking de Repositorios**: En los tests unitarios, la persistencia se simula inyectando dobles de prueba (mocks) creados con `unittest.mock` o implementaciones falsas en memoria (`InMemRepository`).
3.  **Transaccionalidad en Pruebas**: Para los tests de integración que utilizan la base de datos PostgreSQL, cada caso de prueba debe ejecutarse dentro de una transacción que se revierte (`rollback`) al finalizar la prueba, garantizando que el estado de la base de datos se mantenga limpio y determinista.
4.  **Nomenclatura Semántica**: Los nombres de las funciones de prueba deben ser descriptivos del escenario y el resultado esperado:
    *   `test_[nombre_de_metodo]_[comportamiento_esperado]_cuando_[escenario]`
    *   Ejemplo: `test_create_lead_raises_already_exists_error_when_email_exists`

---

## 3. Ejemplo de Código de Referencia

### A. Prueba Unitaria (Aislada, con Mocks)
Ubicación sugerida: `tests/unit/test_lead_service.py`

```python
import pytest
from unittest.mock import Mock
from src.services.lead_service import LeadService, LeadAlreadyExistsError
from src.domain.entities import Lead

def test_create_lead_raises_error_when_email_exists():
    # 1. Arrange (Preparar)
    mock_repository = Mock()
    # Simulamos que ya existe un lead con ese email
    mock_repository.get_by_email.return_value = Lead(name="Test", email="duplicado@example.com", status="NEW")
    
    service = LeadService(lead_repository=mock_repository)

    # 2. Act & Assert (Actuar y Verificar)
    with pytest.raises(LeadAlreadyExistsError):
        service.create_new_lead(name="Otro Lead", email="duplicado@example.com")
        
    # Verificar que get_by_email se llamó correctamente
    mock_repository.get_by_email.assert_called_once_with("duplicado@example.com")
    # Verificar que NO se intentó guardar nada
    mock_repository.save.assert_not_called()
```

### B. Prueba de Integración (Interactúa con BD y API)
Ubicación sugerida: `tests/integration/test_leads_api.py`

```python
from fastapi.testclient import TestClient
from fastapi import status

def test_create_lead_api_returns_201_when_payload_is_valid(test_client: TestClient):
    # Nota: test_client es un fixture que provee FastAPI TestClient configurado
    # con una base de datos limpia y transaccional.
    
    # 1. Arrange (Preparar)
    payload = {
        "name": "Cliente Potencial",
        "email": "lead_valido@example.com"
    }

    # 2. Act (Actuar)
    response = test_client.post("/leads/", json=payload)

    # 3. Assert (Verificar)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Cliente Potencial"
    assert data["email"] == "lead_valido@example.com"
    assert "id" in data
```

---

## 4. Checklist de Validación para el Agente
Antes de entregar un desarrollo técnico, comprueba que:
- [ ] ¿Los nuevos archivos y funciones tienen pruebas asociadas?
- [ ] ¿Los tests unitarios no inician bases de datos ni realizan llamadas HTTP reales a servicios externos?
- [ ] ¿Los tests de integración limpian su estado de base de datos después de cada ejecución (rollback) de forma que puedan correr en cualquier orden de forma concurrente?
- [ ] ¿Has evitado aserciones vagas (como `assert True`) en favor de aserciones precisas sobre los datos y comportamientos del negocio?
- [ ] ¿Las dependencias externas difíciles de controlar (ej: APIs de terceros de enriquecimiento de leads) están aisladas detrás de interfaces y simuladas en los tests de integración?
