import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers.leads import router as leads_router
from app.routers.lead_activities import router as activities_router
from app.routers.metrics import router as metrics_router
from app.exceptions import LeadNotFound, DuplicateEmail, InvalidStatus, InvalidActivityType

from app.dependencies import SessionLocal
from app.models.lead import Lead
from scripts.seed import seed_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager.
    Idempotently seeds the database on startup if it contains 0 leads (only outside test environments).
    """
    is_testing = "pytest" in sys.modules or any("pytest" in arg for arg in sys.argv)
    if not is_testing:
        db = SessionLocal()
        try:
            lead_count = db.query(Lead).count()
            if lead_count == 0:
                print("Database is empty. Triggering automated startup data seeding...")
                seed_db(db)
            else:
                print(f"Database contains {lead_count} existing leads. Skipping automated seeding.")
        except Exception as e:
            print(f"Warning: Failed to verify or seed database on startup: {str(e)}")
        finally:
            db.close()
    yield

app = FastAPI(
    title="Lead & Customer Management System API",
    version="1.0.0",
    description="Backend API for managing leads and activity logs.",
    lifespan=lifespan
)

# Exception Handlers
@app.exception_handler(LeadNotFound)
def lead_not_found_handler(request: Request, exc: LeadNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

@app.exception_handler(DuplicateEmail)
def duplicate_email_handler(request: Request, exc: DuplicateEmail):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )

@app.exception_handler(InvalidStatus)
def invalid_status_handler(request: Request, exc: InvalidStatus):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

@app.exception_handler(InvalidActivityType)
def invalid_activity_type_handler(request: Request, exc: InvalidActivityType):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

# Register Routers
app.include_router(leads_router)
app.include_router(activities_router)
app.include_router(metrics_router)

@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Lead & Customer Management API is active"}
