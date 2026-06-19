# SKILL: Patrón Repositorio (Repository Pattern)

Este documento define la regla de diseño y el estándar de codificación para la capa de persistencia en este proyecto. Todo agente de desarrollo que modifique o cree accesos a la base de datos debe adherirse a esta especificación.

---

## 1. Propósito y Contexto
El **Patrón Repositorio** actúa como un mediador entre el dominio (lógica de negocio) y la infraestructura de persistencia (PostgreSQL mediante SQLAlchemy). Su objetivo principal es abstraer el acceso a datos de forma que la lógica de negocio no conozca los detalles de cómo se guardan o consultan los objetos.

### Cuándo usar esta Skill
*   Al crear nuevos dominios o entidades (ej: `Lead`, `Customer`).
*   Al añadir nuevos métodos de consulta, filtrado o persistencia.
*   Al refactorizar consultas directas de base de datos fuera de la capa de API o de Servicios.

---

## 2. Reglas Arquitectónicas
1.  **Depender de Abstracciones**: La capa de negocio (servicios) solo debe interactuar con las interfaces abstractas de los repositorios (`abc.ABC` o `typing.Protocol`), nunca directamente con las implementaciones de SQLAlchemy.
2.  **No Filtración de Tipos de ORM**: Las firmas de los métodos del repositorio abstracto no deben retornar ni recibir objetos específicos del ORM de SQLAlchemy si esto genera acoplamiento fuerte en la lógica de negocio. Se prefiere el uso de esquemas de dominio o entidades puras.
3.  **Transaccionalidad Externa**: El repositorio no debe realizar `commit` o `rollback` internamente. **Evita implementar un patrón `UnitOfWork` abstracto y complejo**; para un CRUD simple, confía en la inyección de dependencias de FastAPI (`Depends(get_db)`) para manejar la transacción básica por petición, manteniendo la simplicidad.
4.  **Evitar Abstracciones Genéricas**: Evita la creación de un `BaseRepository` dinámico o hiper-genérico. Es preferible mantener repositorios explícitos por entidad para preservar la legibilidad y evitar sobreingeniería.
5.  **Control de Boilerplate**: El mapeo manual entre Entidad, ORM y Esquema API puede volverse tedioso. Se recomienda considerar el uso de Data Classes o modelos Pydantic puros para las Entidades de Dominio, siempre y cuando NO dependan de los esquemas de entrada/salida específicos de FastAPI.

---

## 3. Ejemplo de Código de Referencia

### A. Interfaz Abstracta (Capa de Dominio/Puerto)
Ubicación sugerida: `src/domain/repositories/lead_repository.py`

```python
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities import Lead

class LeadRepository(ABC):
    @abstractmethod
    def save(self, lead: Lead) -> Lead:
        """Guarda un lead nuevo o actualiza uno existente."""
        pass

    @abstractmethod
    def get_by_id(self, lead_id: int) -> Optional[Lead]:
        """Obtiene un lead por su identificador único."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Lead]:
        """Obtiene un lead por su dirección de correo electrónico."""
        pass

    @abstractmethod
    def list_leads(self, skip: int = 0, limit: int = 100) -> List[Lead]:
        """Obtiene una lista paginada de leads."""
        pass
```

### B. Implementación Concreta (Capa de Infraestructura/Adaptador)
Ubicación sugerida: `src/infrastructure/repositories/sqlalchemy_lead_repository.py`

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.entities import Lead
from src.domain.repositories.lead_repository import LeadRepository
from src.infrastructure.database.models import LeadORM

class SQLAlchemyLeadRepository(LeadRepository):
    def __init__(self, db_session: Session):
        self.session = db_session

    def save(self, lead: Lead) -> Lead:
        # Mapeo de Entidad Dominio -> Modelo ORM
        orm_lead = LeadORM(
            id=lead.id,
            name=lead.name,
            email=lead.email,
            status=lead.status
        )
        self.session.add(orm_lead)
        self.session.flush()  # Obtener ID autogenerado sin hacer commit aún
        lead.id = orm_lead.id
        return lead

    def get_by_id(self, lead_id: int) -> Optional[Lead]:
        orm_lead = self.session.query(LeadORM).filter(LeadORM.id == lead_id).first()
        if not orm_lead:
            return None
        return Lead(id=orm_lead.id, name=orm_lead.name, email=orm_lead.email, status=orm_lead.status)

    def get_by_email(self, email: str) -> Optional[Lead]:
        orm_lead = self.session.query(LeadORM).filter(LeadORM.email == email).first()
        if not orm_lead:
            return None
        return Lead(id=orm_lead.id, name=orm_lead.name, email=orm_lead.email, status=orm_lead.status)

    def list_leads(self, skip: int = 0, limit: int = 100) -> List[Lead]:
        orm_leads = self.session.query(LeadORM).offset(skip).limit(limit).all()
        return [
            Lead(id=o.id, name=o.name, email=o.email, status=o.status)
            for o in orm_leads
        ]
```

---

## 4. Checklist de Validación para el Agente
Antes de dar por concluida una tarea de persistencia, comprueba que:
- [ ] ¿Has definido la interfaz del repositorio en una carpeta que no dependa de librerías de persistencia (como `sqlalchemy`)?
- [ ] ¿La lógica de negocio (servicios) solo importa y utiliza la clase abstracta (interfaz)?
- [ ] ¿El repositorio concreto recibe la sesión de base de datos a través de su constructor (Inyección de Dependencias)?
- [ ] ¿Se han cubierto los métodos del repositorio con pruebas utilizando una base de datos de pruebas o de memoria?
- [ ] ¿Has evitado poner lógica de negocio o validaciones comerciales complejas dentro de las consultas del repositorio? (El repositorio solo consulta y persiste datos).
- [ ] ¿Has evitado la creación de abstracciones genéricas excesivas (como `BaseRepository`) y patrones de transaccionalidad complejos (`UnitOfWork`) si no son estrictamente necesarios?
