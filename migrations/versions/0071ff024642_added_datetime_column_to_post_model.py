"""added datetime column to post model

Revision ID: 0071ff024642
Revises: 2e31b3e9274a
Create Date: 2024-01-24 23:22:41.931897

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0071ff024642'
down_revision: Union[str, None] = '2e31b3e9274a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('time_created', sa.DateTime))


def downgrade() -> None:
    op.drop_column('posts', 'time_created')
