"""add_id_to_prompts_suggestions_table

Revision ID: 61ae994534bb
Revises: 7c3060fffb89
Create Date: 2025-08-24 16:51:06.266645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '61ae994534bb'
down_revision: Union[str, None] = '7c3060fffb89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('prompts_suggestions_new',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('usage_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    
    op.bulk_insert(
        sa.table('prompts_suggestions_new',
                 sa.column('title', sa.String),
                 sa.column('content', sa.Text),
                 sa.column('usage_count', sa.Integer)),
        [
            {
                "title": "Help me study vocabulary for a college entrance exam",
                "content": "Help me study vocabulary: write a sentence for me to fill in the blank, and I'll try to pick the correct option.",
                "usage_count": 0
            },
            {
                "title": "Give me ideas for what to do with my kids' art",
                "content": "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.",
                "usage_count": 0
            },
            {
                "title": "Tell me a fun fact about the Roman Empire",
                "content": "Tell me a random fun fact about the Roman Empire",
                "usage_count": 0
            },
            {
                "title": "Show me a code snippet of a website's sticky header",
                "content": "Show me a code snippet of a website's sticky header in CSS and JavaScript.",
                "usage_count": 0
            },
            {
                "title": "Explain options trading if I'm familiar with buying and selling stocks",
                "content": "Explain options trading in simple terms if I'm familiar with buying and selling stocks.",
                "usage_count": 0
            },
            {
                "title": "Overcome procrastination give me tips",
                "content": "Could you start by asking me about instances when I procrastinate the most and then give me some suggestions to overcome it?",
                "usage_count": 0
            },
        ]
    )
    
    op.drop_table('prompts_suggestions')
    op.rename_table('prompts_suggestions_new', 'prompts_suggestions')


def downgrade() -> None:
    op.create_table('prompts_suggestions_old',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('usage_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('title')
    )
    op.execute('INSERT INTO prompts_suggestions_old (title, content, usage_count) SELECT title, content, usage_count FROM prompts_suggestions')
    op.drop_table('prompts_suggestions')
    op.rename_table('prompts_suggestions_old', 'prompts_suggestions')
