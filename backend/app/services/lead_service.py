from typing import List, Optional, Dict
from app.models.lead import Lead
from app.models.enums import LeadStatus
from app.repositories.base import AbstractLeadRepository
from app.exceptions import LeadNotFound, DuplicateEmail, InvalidStatus

class LeadService:
    """
    LeadService coordinates use cases for Lead management (UC-01 to UC-05).
    """
    def __init__(self, lead_repository: AbstractLeadRepository):
        self.repository = lead_repository

    def create_lead(
        self,
        name: str,
        email: str,
        company: Optional[str] = None,
        phone: Optional[str] = None
    ) -> Lead:
        """
        Creates a new prospective client (UC-01).
        Validates email uniqueness and assigns status NEW.
        """
        existing = self.repository.get_by_email(email)
        if existing:
            raise DuplicateEmail(f"A lead with email '{email}' is already registered.")

        new_lead = Lead(
            name=name,
            email=email,
            company=company,
            phone=phone,
            status=LeadStatus.NEW.value
        )
        return self.repository.create(new_lead)

    def get_lead(self, lead_id: int) -> Lead:
        """
        Retrieves a lead by its ID (UC-02 verification / generic query).
        Raises LeadNotFound if it does not exist.
        """
        lead = self.repository.get_by_id(lead_id)
        if not lead:
            raise LeadNotFound(f"Lead with ID {lead_id} not found.")
        return lead

    def update_lead(
        self,
        lead_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        company: Optional[str] = None,
        phone: Optional[str] = None,
        status: Optional[str] = None
    ) -> Lead:
        """
        Updates basic info or status of an existing lead (UC-02).
        Validates email uniqueness if modified, and enforces allowed status values.
        """
        lead = self.get_lead(lead_id)

        if email is not None and email != lead.email:
            existing = self.repository.get_by_email(email)
            if existing:
                raise DuplicateEmail(f"A lead with email '{email}' is already registered.")
            lead.email = email

        if status is not None:
            # Enforce status constraints
            try:
                allowed_status = LeadStatus(status)
                lead.status = allowed_status.value
            except ValueError:
                raise InvalidStatus(
                    f"Status '{status}' is not allowed. Must be one of: "
                    f"{[s.value for s in LeadStatus]}"
                )

        if name is not None:
            lead.name = name
        if company is not None:
            lead.company = company
        if phone is not None:
            lead.phone = phone

        return self.repository.update(lead)

    def list_leads(
        self,
        status: Optional[str] = None,
        query: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Lead]:
        """
        Retrieves a paginated list of leads based on status and search query (UC-03).
        """
        return self.repository.list(
            status=status,
            query=query,
            skip=skip,
            limit=limit
        )

    def delete_lead(self, lead_id: int) -> None:
        """
        Physically deletes a lead and all associated activities (UC-04).
        """
        # Ensure lead exists first
        self.get_lead(lead_id)
        self.repository.delete(lead_id)

    def get_metrics(self) -> Dict[str, int]:
        """
        Calculates analytical metrics of leads grouped by commercial status (UC-05).
        Guarantees that all 4 commercial status categories are returned, default to 0.
        """
        db_metrics = self.repository.get_metrics()
        
        # Ensure all states exist in the resulting metrics dict
        final_metrics = {status.value: 0 for status in LeadStatus}
        
        # Merge metrics retrieved from repository
        for status_key, count in db_metrics.items():
            if status_key in final_metrics:
                final_metrics[status_key] = count
                
        return final_metrics
