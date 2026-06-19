from typing import Optional
from fastapi import APIRouter, Depends, status

from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadListResponse
from app.services.lead_service import LeadService
from app.dependencies import get_lead_service

router = APIRouter(prefix="/leads", tags=["Leads"])

@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new Lead",
    description="Registers a new prospective client and assigns status NEW."
)
def create_lead(
    payload: LeadCreate,
    service: LeadService = Depends(get_lead_service)
) -> LeadResponse:
    return service.create_lead(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        phone=payload.phone
    )

@router.get(
    "",
    response_model=LeadListResponse,
    status_code=status.HTTP_200_OK,
    summary="List and search Leads",
    description="Retrieve a paginated list of leads, optionally filtering by status and searching by text query."
)
def list_leads(
    status: Optional[str] = None,
    query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    service: LeadService = Depends(get_lead_service)
) -> LeadListResponse:
    leads = service.list_leads(status=status, query=query, skip=skip, limit=limit)
    return LeadListResponse(leads=leads, skip=skip, limit=limit)

@router.get(
    "/{lead_id}",
    response_model=LeadResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Lead by ID",
    description="Retrieves the detailed information of a specific lead by its ID."
)
def get_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service)
) -> LeadResponse:
    return service.get_lead(lead_id)

@router.put(
    "/{lead_id}",
    response_model=LeadResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Lead",
    description="Updates basic details or transition state of an existing lead."
)
def update_lead(
    lead_id: int,
    payload: LeadUpdate,
    service: LeadService = Depends(get_lead_service)
) -> LeadResponse:
    return service.update_lead(
        lead_id=lead_id,
        **payload.model_dump(exclude_unset=True)
    )

@router.delete(
    "/{lead_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Lead",
    description="Physically removes a lead and all its chronological activities."
)
def delete_lead(
    lead_id: int,
    service: LeadService = Depends(get_lead_service)
) -> None:
    service.delete_lead(lead_id)
