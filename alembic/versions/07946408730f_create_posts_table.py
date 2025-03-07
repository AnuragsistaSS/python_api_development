"""create posts table

Revision ID: 07946408730f
Revises: 
Create Date: 2025-03-07 13:26:00.246568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07946408730f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'Post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('content', sa.String, nullable=False),
        sa.Column('published', sa.Boolean, default=True),
        sa.Column('created_at', sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('Post')
    
