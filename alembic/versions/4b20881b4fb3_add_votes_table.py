"""add Votes table

Revision ID: 4b20881b4fb3
Revises: 1dc6b11c7156
Create Date: 2025-03-07 15:59:28.191639

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b20881b4fb3'
down_revision: Union[str, None] = '1dc6b11c7156'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'Votes',
        sa.Column('post_id', sa.Integer, sa.ForeignKey('Post.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('Users.id', ondelete='CASCADE'), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Votes')
