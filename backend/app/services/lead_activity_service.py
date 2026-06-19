from typing import List
from app.models.lead_activity import LeadActivity
from app.models.enums import ActivityType
from app.repositories.base import AbstractLeadRepository, AbstractLeadActivityRepository
from app.exceptions import LeadNotFound, InvalidActivityType

class LeadActivityService:
    """
    LeadActivityService coordinates use cases for Lead follow-up and notes (UC-06 to UC-07).
    """
    def __init__(
        self,
        activity_repository: AbstractLeadActivityRepository,
        lead_repository: AbstractLeadRepository
    ):
        self.activity_repository = activity_repository
        self.lead_repository = lead_repository

    def register_activity(self, lead_id: int, type: str, notes: str) -> LeadActivity:
        """
        Registers an interaction or follow-up note linked to a Lead (UC-06).
        Validates lead existence and allowed activity types.
        """
        # Validate Lead existence (raises LeadNotFound if not found)
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            raise LeadNotFound(f"Lead with ID {lead_id} not found.")

        # Validate Activity type
        try:
            validated_type = ActivityType(type)
        except ValueError:
            raise InvalidActivityType(
                f"Activity type '{type}' is not allowed. Must be one of: "
                f"{[t.value for t in ActivityType]}"
            )

        new_activity = LeadActivity(
            lead_id=lead_id,
            type=validated_type.value,
            notes=notes
        )
        return self.activity_repository.create(new_activity)

    def list_activities(self, lead_id: int) -> List[LeadActivity]:
        """
        Retrieves all activities registered for a specific Lead, sorted cronologically (UC-07).
        """
        # Validate Lead existence
        lead = self.lead_repository.get_by_id(lead_id)
        if not lead:
            raise LeadNotFound(f"Lead with ID {lead_id} not found.")

        return self.activity_repository.list_by_lead_id(lead_id)
