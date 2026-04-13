"""Create users table

Revision ID: 37f7a8d2d513
Revises: 
Create Date: 2026-04-13 19:01:29.281281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37f7a8d2d513'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("users",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("username", sa.VARCHAR(45), nullable=False),
                    sa.Column("password", sa.VARCHAR(64), nullable=False)
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
