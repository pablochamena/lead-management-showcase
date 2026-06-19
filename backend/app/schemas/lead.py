from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class LeadCreate(BaseModel):
    """Schema for creating a new Lead."""
    name: str = Field(..., max_length=100, description="Full name or business name")
    email: EmailStr = Field(..., description="Primary contact email address (must be unique)")
    company: Optional[str] = Field(None, max_length=100, description="Associated company/organization")
    phone: Optional[str] = Field(None, max_length=20, description="Contact phone number")

class LeadUpdate(BaseModel):
    """Schema for updating an existing Lead's information or status."""
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None)
    company: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, description="Commercial status in sales funnel")

class LeadResponse(BaseModel):
    """Schema for Lead details in API responses."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    company: Optional[str]
    email: str
    phone: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class LeadListResponse(BaseModel):
    """Wrapper schema for a paginated list of Leads."""
    leads: List[LeadResponse]
    skip: int
    limit: int
