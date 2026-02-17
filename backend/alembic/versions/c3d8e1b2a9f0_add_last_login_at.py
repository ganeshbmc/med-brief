"""add last login at

Revision ID: c3d8e1b2a9f0
Revises: b89f6dd1a0a6
Create Date: 2026-02-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d8e1b2a9f0'
down_revision: Union[str, None] = 'b89f6dd1a0a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('last_login_at', sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'last_login_at')
