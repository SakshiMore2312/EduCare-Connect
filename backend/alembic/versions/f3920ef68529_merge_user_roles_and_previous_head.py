"""merge user roles and previous head

Revision ID: f3920ef68529
Revises: 20260302_update_user_roles, fd21b7514670
Create Date: 2026-03-02 19:07:18.208133

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3920ef68529'
down_revision: Union[str, Sequence[str], None] = ('20260302_update_user_roles', 'fd21b7514670')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
