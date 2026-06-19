from typing import List
from fastapi import APIRouter, Depends, status

from app.schemas.lead_activity import LeadActivityCreate, LeadActivityResponse
from app.services.lead_activity_service import LeadActivityService
from app.dependencies import get_lead_activity_service

router = APIRouter(prefix="/leads/{lead_id}/activities", tags=["Activities"])

@router.post(
    "",
    response_model=LeadActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new activity for a Lead",
    description="Registers an interaction (CALL, EMAIL, NOTE) and attaches it to the specified lead."
)
def register_activity(
    lead_id: int,
    payload: LeadActivityCreate,
    service: LeadActivityService = Depends(get_lead_activity_service)
) -> LeadActivityResponse:
    return service.register_activity(
        lead_id=lead_id,
        type=payload.type.value,
        notes=payload.notes
    )

@router.get(
    "",
    response_model=List[LeadActivityResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Lead activity history",
    description="Retrieves all chronological activities registered for the specified lead in descending order."
)
def list_activities(
    lead_id: int,
    service: LeadActivityService = Depends(get_lead_activity_service)
) -> List[LeadActivityResponse]:
    return service.list_activities(lead_id)
