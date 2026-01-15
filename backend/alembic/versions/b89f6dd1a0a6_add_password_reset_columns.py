"""add password reset columns

Revision ID: b89f6dd1a0a6
Revises: 6db7e0d84c40
Create Date: 2026-01-16 00:52:54.671512

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b89f6dd1a0a6'
down_revision: Union[str, None] = '6db7e0d84c40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('reset_token', sa.String(64), nullable=True))
    op.add_column('users', sa.Column('reset_token_expires_at', sa.DateTime, nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'reset_token_expires_at')
    op.drop_column('users', 'reset_token')
