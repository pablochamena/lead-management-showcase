from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.models.lead import Lead
from app.models.lead_activity import LeadActivity

class AbstractLeadRepository(ABC):
    """
    Abstract interface for Lead entity persistence operations.
    Fully decoupled from SQLAlchemy or any other infrastructure framework.
    """
    @abstractmethod
    def create(self, lead: Lead) -> Lead:
        """
        Persist a new Lead entity in the database.
        """
        pass

    @abstractmethod
    def get_by_id(self, lead_id: int) -> Optional[Lead]:
        """
        Retrieve a Lead entity by its primary key ID.
        Returns None if the lead does not exist.
        """
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Lead]:
        """
        Retrieve a Lead entity by its unique email address.
        Used to enforce uniqueness constraints.
        Returns None if not found.
        """
        pass

    @abstractmethod
    def list(
        self,
        status: Optional[str] = None,
        query: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Lead]:
        """
        Retrieve a paginated list of leads, optionally filtered by status or name/company/email query.
        Results must be ordered by created_at DESC.
        """
        pass

    @abstractmethod
    def update(self, lead: Lead) -> Lead:
        """
        Update an existing Lead entity in persistence and return the updated entity.
        """
        pass

    @abstractmethod
    def delete(self, lead_id: int) -> None:
        """
        Physically delete a Lead entity from the database by its ID.
        """
        pass

    @abstractmethod
    def get_metrics(self) -> Dict[str, int]:
        """
        Retrieve count metrics of leads grouped by their commercial status.
        """
        pass


class AbstractLeadActivityRepository(ABC):
    """
    Abstract interface for LeadActivity entity persistence operations.
    """
    @abstractmethod
    def create(self, activity: LeadActivity) -> LeadActivity:
        """
        Persist a new LeadActivity entity in the database.
        """
        pass

    @abstractmethod
    def list_by_lead_id(self, lead_id: int) -> List[LeadActivity]:
        """
        Retrieve all activities related to a specific lead ID.
        Results must be ordered by created_at DESC.
        """
        pass
