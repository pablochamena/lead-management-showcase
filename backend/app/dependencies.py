from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.repositories.base import AbstractLeadRepository, AbstractLeadActivityRepository
from app.repositories.sqlalchemy_lead_repository import SQLAlchemyLeadRepository
from app.repositories.sqlalchemy_lead_activity_repository import SQLAlchemyLeadActivityRepository
from app.services.lead_service import LeadService
from app.services.lead_activity_service import LeadActivityService

# Initialize the database engine with explicit connection pool limits for production (A-04).
# pool_size: max persistent connections kept open in the pool.
# max_overflow: additional connections allowed beyond pool_size under peak load.
# pool_pre_ping: validates connections before use, discarding stale/dead ones.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db():
    """
    FastAPI dependency that yields a database session.
    Guarantees rollback on any unhandled exception before closing the session,
    preventing zombie transactions in PostgreSQL (B-01).
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def get_lead_repository(db: Session = Depends(get_db)) -> AbstractLeadRepository:
    """
    FastAPI provider that returns an initialized SQLAlchemyLeadRepository.
    """
    return SQLAlchemyLeadRepository(db_session=db)

def get_lead_service(repo: AbstractLeadRepository = Depends(get_lead_repository)) -> LeadService:
    """
    FastAPI provider that injects the repository into LeadService.
    """
    return LeadService(lead_repository=repo)

def get_lead_activity_service(db: Session = Depends(get_db)) -> LeadActivityService:
    """
    FastAPI provider that injects LeadActivityService using a SINGLE shared database
    session for both repositories, guaranteeing transactional atomicity (B-02).
    Previously, two separate Depends(get_lead_repository) and Depends(get_lead_activity_repository)
    each opened their own session, breaking atomicity across UC-06 and UC-07.
    """
    lead_repo = SQLAlchemyLeadRepository(db_session=db)
    activity_repo = SQLAlchemyLeadActivityRepository(db_session=db)
    return LeadActivityService(
        activity_repository=activity_repo,
        lead_repository=lead_repo
    )
