"""Add staff and roles tables

Revision ID: 6a27b4b7e2a1
Revises: cdaa37230cd7
Create Date: 2026-04-15 09:54:43.084590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a27b4b7e2a1'
down_revision: Union[str, Sequence[str], None] = 'cdaa37230cd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table("roles",
                    sa.Column("id", sa.INTEGER, primary_key=True, autoincrement=True),
                    sa.Column("role_name", sa.VARCHAR(45), nullable=False),
                    sa.Column("role_description", sa.VARCHAR(64), nullable=False))

    op.create_table("staff",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("first_name", sa.VARCHAR(45), nullable=False),
                    sa.Column("last_name", sa.VARCHAR(45)),
                    sa.Column("clearence_level", sa.SMALLINT, nullable=False),
                    sa.Column("user_id", sa.INTEGER, sa.ForeignKey("users.id"), nullable=False),
                    sa.Column("role_id", sa.INTEGER), sa.ForeignKey("roles.id"))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("staff")
    op.drop_table("roles")
