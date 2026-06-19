from enum import Enum

class LeadStatus(str, Enum):
    """
    Lead commercial status values.
    """
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    QUALIFIED = "QUALIFIED"
    LOST = "LOST"

class ActivityType(str, Enum):
    """
    Lead interaction type values.
    """
    CALL = "CALL"
    EMAIL = "EMAIL"
    NOTE = "NOTE"
