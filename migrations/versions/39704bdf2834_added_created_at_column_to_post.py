"""added created at column to post

Revision ID: 39704bdf2834
Revises: 0071ff024642
Create Date: 2024-01-25 20:37:36.717563

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '39704bdf2834'
down_revision: Union[str, None] = '0071ff024642'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('created_at', sa.Date))


def downgrade() -> None:
    op.drop_column('posts', 'created_at')
