"""add_usage_count_to_prompts_suggestions_table

Revision ID: 7c3060fffb89
Revises: 723da7035dbf
Create Date: 2025-08-24 16:28:30.693492

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '7c3060fffb89'
down_revision: Union[str, None] = '723da7035dbf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.add_column('prompts_suggestions', sa.Column('usage_count', sa.Integer(), nullable=True, server_default='0'))
    op.execute("UPDATE prompts_suggestions SET usage_count = 0 WHERE usage_count IS NULL")
    
    with op.batch_alter_table('prompts_suggestions') as batch_op:
        batch_op.alter_column('usage_count', nullable=False, server_default='0')


def downgrade() -> None:
    with op.batch_alter_table('prompts_suggestions') as batch_op:
        batch_op.drop_column('usage_count')