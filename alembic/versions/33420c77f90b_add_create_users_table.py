"""add create users table

Revision ID: 33420c77f90b
Revises: 07946408730f
Create Date: 2025-03-07 15:55:21.817535

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '33420c77f90b'
down_revision: Union[str, None] = '07946408730f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'Users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Users')
