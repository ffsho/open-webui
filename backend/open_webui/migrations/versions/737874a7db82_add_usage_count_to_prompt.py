"""add_usage_count_to_prompt

Revision ID: 737874a7db82
Revises: d31026856c01
Create Date: 2025-08-24 12:54:35.582195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '737874a7db82'
down_revision: Union[str, None] = 'd31026856c01'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('prompt', sa.Column('usage_count', sa.Integer(), nullable=True, server_default='0'))


def downgrade() -> None:
    op.drop_column('prompt', 'usage_count')