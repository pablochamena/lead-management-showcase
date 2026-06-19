import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.dependencies import get_db
from app.config import settings

@pytest.fixture(scope="session")
def db_engine():
    """
    Creates a database engine for the test suite.
    """
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True
    )
    return engine

@pytest.fixture
def db_session(db_engine):
    """
    Fixture that runs each test inside a transaction and rolls it back at the end.
    Ensures tests remain isolated and do not pollute the database.
    """
    connection = db_engine.connect()
    # Begin the outer transaction
    transaction = connection.begin()
    
    # Session factory bound to the active connection
    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=connection
    )
    session = TestSessionLocal()
    
    yield session
    
    session.close()
    # Rollback all database modifications made during the test
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """
    FastAPI TestClient that overrides get_db to inject the transactional session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    # Clear overrides after the test is completed
    app.dependency_overrides.clear()
