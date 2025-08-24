"""add_prompts_suggestions_table

Revision ID: 723da7035dbf
Revises: 737874a7db82
Create Date: 2025-08-24 16:11:50.882714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '723da7035dbf'
down_revision: Union[str, None] = '737874a7db82'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('prompts_suggestions',
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('title')
    )
    
    op.bulk_insert(
        sa.table('prompts_suggestions',
                 sa.column('title', sa.String),
                 sa.column('content', sa.Text)),
        [
            {
                "title": "Help me study vocabulary for a college entrance exam",
                "content": "Help me study vocabulary: write a sentence for me to fill in the blank, and I'll try to pick the correct option.",
            },
            {
                "title": "Give me ideas for what to do with my kids' art",
                "content": "What are 5 creative things I could do with my kids' art? I don't want to throw them away, but it's also so much clutter.",
            },
            {
                "title": "Tell me a fun fact about the Roman Empire",
                "content": "Tell me a random fun fact about the Roman Empire",
            },
            {
                "title": "Show me a code snippet of a website's sticky header",
                "content": "Show me a code snippet of a website's sticky header in CSS and JavaScript.",
            },
            {
                "title": "Explain options trading if I'm familiar with buying and selling stocks",
                "content": "Explain options trading in simple terms if I'm familiar with buying and selling stocks.",
            },
            {
                "title": "Overcome procrastination give me tips",
                "content": "Could you start by asking me about instances when I procrastinate the most and then give me some suggestions to overcome it?",
            },
        ]
    )


def downgrade() -> None:
    op.drop_table('prompts_suggestions')