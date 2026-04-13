"""Create SCP Table

Revision ID: cdaa37230cd7
Revises: 37f7a8d2d513
Create Date: 2026-04-13 19:07:31.987125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdaa37230cd7'
down_revision: Union[str, Sequence[str], None] = '37f7a8d2d513'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("scp_subjects",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("object_class", sa.VARCHAR(15), nullable=False),
                    sa.Column("containment_procedures", sa.VARCHAR(1024)),
                    sa.Column("description", sa.VARCHAR(4096))
                    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("scp_subjects")
