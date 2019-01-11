"""empty message

Revision ID: abf6ca815a01
Revises: 42f3c49b3461
Create Date: 2019-01-11 10:36:52.775242

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "abf6ca815a01"
down_revision = "42f3c49b3461"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "tweet_link",
        "url",
        existing_type=sa.VARCHAR(length=200),
        type_=sa.String(length=400),
        existing_nullable=True,
    )


def downgrade():
    op.alter_column(
        "tweet_link",
        "url",
        existing_type=sa.String(length=400),
        type_=sa.VARCHAR(length=200),
        existing_nullable=True,
    )

