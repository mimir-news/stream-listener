"""empty message

Revision ID: 8fa168decf74
Revises:
Create Date: 2018-09-02 23:00:20.045335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fa168decf74'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('stock',
    sa.Column('symbol', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('total_count', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('symbol')
    )
    op.create_table('tweet',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('text', sa.String(length=500), nullable=True),
    sa.Column('language', sa.String(length=10), nullable=True),
    sa.Column('author_id', sa.String(length=50), nullable=True),
    sa.Column('author_followers', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tweet_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=200), nullable=True),
    sa.Column('tweet_id', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ),
    )
    op.create_table('tweet_symbol',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symbol', sa.String(length=20), nullable=False),
    sa.Column('tweet_id', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.ForeignKeyConstraint(['symbol'], ['stock.symbol'], ),
    sa.ForeignKeyConstraint(['tweet_id'], ['tweet.id'], ),
    )


def downgrade():
    op.drop_table('tweet_link')
    op.drop_table('tweet_url')
    op.drop_table('tweet')
    op.drop_table('stock')
