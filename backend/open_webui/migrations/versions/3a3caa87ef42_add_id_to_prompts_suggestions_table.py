"""add_id_to_prompts_suggestions_table

Revision ID: 3a3caa87ef42
Revises: 61ae994534bb
Create Date: 2025-08-24 17:05:45.488002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision: str = '3a3caa87ef42'
down_revision: Union[str, None] = '61ae994534bb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'prompts_suggestions_temp',
        sa.Column('id', sa.Text(), nullable=False),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    connection = op.get_bind()
    results = connection.execute(sa.text("SELECT title, content, usage_count FROM prompts_suggestions")).fetchall()
    
    for row in results:
        connection.execute(
            sa.text("INSERT INTO prompts_suggestions_temp (id, title, content, usage_count) VALUES (:id, :title, :content, :usage_count)"),
            {
                "id": str(uuid.uuid4()),
                "title": row.title,
                "content": row.content,
                "usage_count": row.usage_count
            }
        )
    
    op.drop_table('prompts_suggestions')
    
    op.rename_table('prompts_suggestions_temp', 'prompts_suggestions')


def downgrade() -> None:
    op.create_table(
        'prompts_suggestions_temp',
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('usage_count', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('title')
    )
    
    connection = op.get_bind()
    results = connection.execute(sa.text("SELECT title, content, usage_count FROM prompts_suggestions")).fetchall()
    
    for row in results:
        connection.execute(
            sa.text("INSERT INTO prompts_suggestions_temp (title, content, usage_count) VALUES (:title, :content, :usage_count)"),
            {
                "title": row.title,
                "content": row.content,
                "usage_count": row.usage_count
            }
        )
    
    op.drop_table('prompts_suggestions')
    
    op.rename_table('prompts_suggestions_temp', 'prompts_suggestions')
