"""0003_add_timezone_to_timestamps

Adds timezone=True (TIMESTAMP WITH TIME ZONE) to the created_at and updated_at
columns on the leads and lead_activities tables (T-03).

Revision ID: d7a5b3c1e2f4
Revises: 9f2c1a4e88db
Create Date: 2026-06-19 12:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7a5b3c1e2f4'
down_revision: Union[str, None] = '9f2c1a4e88db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Alter datetime columns to declare timezone=True (TIMESTAMP WITH TIME ZONE).
    """
    # --- leads table ---
    op.alter_column(
        'leads',
        'created_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        existing_server_default=sa.text('NOW()')
    )
    op.alter_column(
        'leads',
        'updated_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        existing_server_default=sa.text('NOW()')
    )

    # --- lead_activities table ---
    op.alter_column(
        'lead_activities',
        'created_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(),
        existing_nullable=False,
        existing_server_default=sa.text('NOW()')
    )


def downgrade() -> None:
    """
    Revert timezone-aware datetime columns back to naive datetime.
    """
    # --- lead_activities table ---
    op.alter_column(
        'lead_activities',
        'created_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text('NOW()')
    )

    # --- leads table ---
    op.alter_column(
        'leads',
        'updated_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text('NOW()')
    )
    op.alter_column(
        'leads',
        'created_at',
        type_=sa.DateTime(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
        existing_server_default=sa.text('NOW()')
    )
