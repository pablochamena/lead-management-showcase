from fastapi import APIRouter, Depends

from app.schemas.lead import LeadMetricsResponse
from app.services.lead_service import LeadService
from app.dependencies import get_lead_service

router = APIRouter(prefix="/metrics", tags=["Metrics"])

@router.get(
    "",
    response_model=LeadMetricsResponse,
    summary="Get Sales Funnel Metrics",
    description="Returns the total count of leads grouped by their commercial status."
)
def get_metrics(
    service: LeadService = Depends(get_lead_service)
) -> LeadMetricsResponse:
    raw_metrics = service.get_metrics()
    return LeadMetricsResponse(
        new=raw_metrics.get("NEW", 0),
        contacted=raw_metrics.get("CONTACTED", 0),
        qualified=raw_metrics.get("QUALIFIED", 0),
        lost=raw_metrics.get("LOST", 0)
    )
