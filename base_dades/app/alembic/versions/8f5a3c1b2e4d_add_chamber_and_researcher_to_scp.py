"""Add chamber and researcher fields to SCP table

Revision ID: 8f5a3c1b2e4d
Revises: cdaa37230cd7
Create Date: 2026-04-13 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f5a3c1b2e4d'
down_revision: Union[str, Sequence[str], None] = 'cdaa37230cd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("scp_subjects", sa.Column("chamber_id", sa.Integer, nullable=True))
    op.add_column("scp_subjects", sa.Column("assigned_researcher_id", sa.Integer, nullable=True))
    op.create_foreign_key("fk_chamber_id", "scp_subjects", "chambers", ["chamber_id"], ["id"])
    op.create_foreign_key("fk_researcher_id", "scp_subjects", "staff", ["assigned_researcher_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_researcher_id", "scp_subjects", type_="foreignkey")
    op.drop_constraint("fk_chamber_id", "scp_subjects", type_="foreignkey")
    op.drop_column("scp_subjects", "assigned_researcher_id")
    op.drop_column("scp_subjects", "chamber_id")
