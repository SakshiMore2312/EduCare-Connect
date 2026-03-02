"""normalize user roles to ADMIN and USER only

Revision ID: 20260302_update_user_roles
Revises: 6060b65048f0
"""

from alembic import op
import sqlalchemy as sa

revision = '20260302_update_user_roles'
down_revision = '6060b65048f0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # convert any legacy roles to USER
    op.execute("UPDATE users SET role='USER' WHERE role IN ('USER','ADMIN')")

    # ensure the new USER enum value exists (PostgreSQL specific syntax)
    # `ALTER TYPE ... ADD VALUE IF NOT EXISTS` is available in PG >= 9.6
    try:
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'USER'")
    except Exception:
        # if the enum already contains USER or if DB is not Postgres, ignore
        pass

    # note: removing values from a Postgres enum is non‑trivial; the application
    # will simply stop using the legacy values moving forward.


def downgrade() -> None:
    # on downgrade, re‑add legacy values so old code can still function
    try:
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'USER'")
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'ADMIN'")
    except Exception:
        pass
