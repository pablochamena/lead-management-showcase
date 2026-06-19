"""0002_add_server_defaults

Adds server_default=NOW() to the created_at and updated_at columns on the
leads and lead_activities tables.

Without server_default, rows inserted directly via SQL (psql, manual scripts,
or other tools bypassing the ORM) would leave these columns NULL, violating
the nullable=False constraint. The ORM relies on Python-side defaults which
are not applied in raw SQL contexts.

This migration makes the schema self-sufficient at the database level (A-05).

Revision ID: 9f2c1a4e88db
Revises: 7d4ba69b71aa
Create Date: 2026-06-19 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f2c1a4e88db'
down_revision: Union[str, None] = '7d4ba69b71aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Inject server_default=NOW() into timestamp columns for both tables.
    This ensures that direct SQL inserts without specifying these columns
    receive a valid timestamp from the DB engine rather than failing with
    a NOT NULL constraint violation.
    """
    # --- leads table ---
    op.alter_column(
        'leads',
        'created_at',
        existing_type=sa.DateTime(),
        server_default=sa.text('NOW()'),
        existing_nullable=False
    )
    op.alter_column(
        'leads',
        'updated_at',
        existing_type=sa.DateTime(),
        server_default=sa.text('NOW()'),
        existing_nullable=False
    )

    # --- lead_activities table ---
    op.alter_column(
        'lead_activities',
        'created_at',
        existing_type=sa.DateTime(),
        server_default=sa.text('NOW()'),
        existing_nullable=False
    )


def downgrade() -> None:
    """
    Remove server_default from all timestamp columns, reverting to ORM-only
    default assignment.
    """
    # --- lead_activities table ---
    op.alter_column(
        'lead_activities',
        'created_at',
        existing_type=sa.DateTime(),
        server_default=None,
        existing_nullable=False
    )

    # --- leads table ---
    op.alter_column(
        'leads',
        'updated_at',
        existing_type=sa.DateTime(),
        server_default=None,
        existing_nullable=False
    )
    op.alter_column(
        'leads',
        'created_at',
        existing_type=sa.DateTime(),
        server_default=None,
        existing_nullable=False
    )
