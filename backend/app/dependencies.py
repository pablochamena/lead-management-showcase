# Dependencies Injection Providers

def get_db():
    """
    Database session generator provider.
    Will yield a SQLAlchemy session once the engine is configured (Milestone 6).
    """
    yield None
