from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from app.models.enums import ActivityType

class LeadActivityCreate(BaseModel):
    """Schema for registering a new LeadActivity."""
    type: ActivityType = Field(..., description="Type of interaction (CALL, EMAIL, NOTE)")
    notes: str = Field(..., min_length=1, description="Detail text or note of the interaction (cannot be empty)")

class LeadActivityResponse(BaseModel):
    """Schema for LeadActivity details in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    lead_id: int
    type: str
    notes: str
    created_at: datetime
