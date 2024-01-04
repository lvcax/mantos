"""eu quero tudo de novo

Revision ID: b37aff1c9c89
Revises: 
Create Date: 2024-01-03 21:03:52.172767

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'b37aff1c9c89'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clubs',
    sa.Column('id', sa.Uuid(), server_default=sa.text('(gen_random_uuid())'), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('country', sa.String(length=20), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clubs')
    # ### end Alembic commands ###
