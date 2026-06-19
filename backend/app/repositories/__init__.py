from app.repositories.base import AbstractLeadRepository, AbstractLeadActivityRepository
from app.repositories.sqlalchemy_lead_repository import SQLAlchemyLeadRepository
from app.repositories.sqlalchemy_lead_activity_repository import SQLAlchemyLeadActivityRepository

__all__ = [
    "AbstractLeadRepository",
    "AbstractLeadActivityRepository",
    "SQLAlchemyLeadRepository",
    "SQLAlchemyLeadActivityRepository",
]
