from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Integer, DateTime, CheckConstraint, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import LeadStatus

class Lead(Base):
    """
    Lead ORM Model representing a prospective client in the CRM system.
    """
    __tablename__ = "leads"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    company: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    status: Mapped[LeadStatus] = mapped_column(String(20), nullable=False, default=LeadStatus.NEW)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relación 1:N con LeadActivity.
    # El borrado en cascada a nivel de SQLAlchemy se complementa con ON DELETE CASCADE en BD.
    activities: Mapped[List["LeadActivity"]] = relationship(
        "LeadActivity",
        back_populates="lead",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "status IN ('NEW', 'CONTACTED', 'QUALIFIED', 'LOST')",
            name="chk_lead_status"
        ),
        UniqueConstraint("email", name="uq_lead_email"),
        Index("idx_leads_status_created_at", "status", "created_at"),
    )
