from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers.leads import router as leads_router
from app.exceptions import LeadNotFound, DuplicateEmail, InvalidStatus, InvalidActivityType

app = FastAPI(
    title="Lead & Customer Management System API",
    version="1.0.0",
    description="Backend API for managing leads and activity logs."
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

@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint."""
    return {"status": "ok", "message": "Lead & Customer Management API is active"}
