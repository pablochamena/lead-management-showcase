class LeadDomainError(Exception):
    """Base exception for all domain-specific errors in the CRM application."""
    pass

class LeadNotFound(LeadDomainError):
    """Raised when a requested Lead is not found in the persistence layer."""
    pass

class DuplicateEmail(LeadDomainError):
    """Raised when trying to create/update a Lead with an email that is already registered."""
    pass

class InvalidStatus(LeadDomainError):
    """Raised when a lead transition or status value is commercialy invalid."""
    pass

class InvalidActivityType(LeadDomainError):
    """Raised when registering an activity with an invalid interaction type."""
    pass
