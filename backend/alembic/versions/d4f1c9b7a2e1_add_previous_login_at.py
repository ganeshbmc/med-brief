"""add previous login at

Revision ID: d4f1c9b7a2e1
Revises: c3d8e1b2a9f0
Create Date: 2026-02-17 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4f1c9b7a2e1'
down_revision: Union[str, None] = 'c3d8e1b2a9f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('previous_login_at', sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'previous_login_at')
