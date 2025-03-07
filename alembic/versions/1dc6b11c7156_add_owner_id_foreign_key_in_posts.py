"""add owner id foreign key in posts

Revision ID: 1dc6b11c7156
Revises: 33420c77f90b
Create Date: 2025-03-07 15:58:14.484502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1dc6b11c7156'
down_revision: Union[str, None] = '33420c77f90b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('Post', sa.Column('owner_id', sa.Integer, sa.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('Post', 'owner_id')
