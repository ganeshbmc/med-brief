"""fix_prod_add_fullname

Revision ID: ab29e3a05762
Revises: 15b0d85587dc
Create Date: 2025-12-31 03:35:49.496823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab29e3a05762'
down_revision: Union[str, None] = '15b0d85587dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Safe migration: Only add the column if it doesn't exist
    # This handles the discrepancy between Local (created via create_all) and Prod (older schema)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    if 'full_name' not in columns:
        op.add_column('users', sa.Column('full_name', sa.String(), nullable=True))


def downgrade() -> None:
    # Downgrade logic (optional, but good practice)
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    if 'full_name' in columns:
        op.drop_column('users', 'full_name')
