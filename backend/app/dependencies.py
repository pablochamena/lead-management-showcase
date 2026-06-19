from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.repositories.base import AbstractLeadRepository, AbstractLeadActivityRepository
from app.repositories.sqlalchemy_lead_repository import SQLAlchemyLeadRepository
from app.repositories.sqlalchemy_lead_activity_repository import SQLAlchemyLeadActivityRepository
from app.services.lead_service import LeadService
from app.services.lead_activity_service import LeadActivityService

# Initialize the database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    FastAPI dependency that yields a database session and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_lead_repository(db: Session = Depends(get_db)) -> AbstractLeadRepository:
    """
    FastAPI provider that returns an initialized SQLAlchemyLeadRepository.
    """
    return SQLAlchemyLeadRepository(db_session=db)

def get_lead_activity_repository(db: Session = Depends(get_db)) -> AbstractLeadActivityRepository:
    """
    FastAPI provider that returns an initialized SQLAlchemyLeadActivityRepository.
    """
    return SQLAlchemyLeadActivityRepository(db_session=db)

def get_lead_service(repo: AbstractLeadRepository = Depends(get_lead_repository)) -> LeadService:
    """
    FastAPI provider that injects the repository into LeadService.
    """
    return LeadService(lead_repository=repo)

def get_lead_activity_service(
    activity_repo: AbstractLeadActivityRepository = Depends(get_lead_activity_repository),
    lead_repo: AbstractLeadRepository = Depends(get_lead_repository)
) -> LeadActivityService:
    """
    FastAPI provider that injects required repositories into LeadActivityService.
    """
    return LeadActivityService(
        activity_repository=activity_repo,
        lead_repository=lead_repo
    )
