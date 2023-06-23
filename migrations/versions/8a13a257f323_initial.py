"""Initial

Revision ID: 8a13a257f323
Revises: 
Create Date: 2023-07-11 23:51:51.480077

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = "8a13a257f323"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "urls",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("prefix", sa.String(), unique=True, index=True),
        sa.Column("redirect_to", sa.Text),
        sa.Column("hits", sa.Integer, default=0),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("created_at", sa.DateTime, server_default=func.now()),
    )


def downgrade() -> None:
    op.drop_table("urls")
