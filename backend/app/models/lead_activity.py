from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class LeadActivity(Base):
    """
    LeadActivity ORM Model representing an interaction or follow-up note for a specific Lead.
    """
    __tablename__ = "lead_activities"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    lead_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("leads.id", ondelete="CASCADE"),
        nullable=False
    )
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    notes: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    
    # Relación N:1 con Lead
    lead: Mapped["Lead"] = relationship("Lead", back_populates="activities")

    __table_args__ = (
        CheckConstraint(
            "type IN ('CALL', 'EMAIL', 'NOTE')",
            name="chk_lead_activity_type"
        ),
    )
