"""Inital Stock Data

Revision ID: 42f3c49b3461
Revises: 8fa168decf74
Create Date: 2018-09-03 09:53:04.391375

"""
from datetime import datetime
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision = '42f3c49b3461'
down_revision = '8fa168decf74'
branch_labels = None
depends_on = None


def upgrade():
    stock_table = table('stock',
                        column('symbol', sa.String),
                        column('name', sa.String),
                        column('is_active', sa.Boolean),
                        column('total_count', sa.Integer),
                        column('updated_at', sa.DateTime))
    op.bulk_insert(stock_table, [
        {'symbol': 'T', 'name': 'AT&T, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'WMT', 'name': 'Wal-Mart Stores Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'PYPL', 'name': 'PayPal Holdings, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'TWTR', 'name': 'Twitter, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'NFLX', 'name': 'Netflix, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'FB', 'name': 'Facebook Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'NKE', 'name': 'Nike, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'GOOG', 'name': 'Alphabet Inc', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'SNAP', 'name': 'Snap Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'F', 'name': 'Ford Motor Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'V', 'name': 'Visa Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'AMD', 'name': 'Advanced Micro Devices, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'BIDU', 'name': 'Baidu, Inc', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'MON', 'name': 'Monsanto Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'S', 'name': 'Sprint Corporation', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'M', 'name': "Macy's Inc", 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'C', 'name': 'Citigroup, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'JPM', 'name': 'JP Morgan Chase & Co.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'GM', 'name': 'General Motors Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'HPQ', 'name': 'HP Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'PG', 'name': 'Procter & Gamble Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'SQ', 'name': 'Square, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'NEWR', 'name': 'New Relic, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'OKTA', 'name': 'Okta, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'SPLK', 'name': 'Splunk Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'EBAY', 'name': 'eBay Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'TSLA', 'name': 'Tesla, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'ACN', 'name': 'Accenture plc', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'AMZN', 'name': 'Amazon.com, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'INTC', 'name': 'Intel Corporation', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'CSCO', 'name': 'Cisco Systems, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'FIT', 'name': 'Fitbit, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'BABA', 'name': 'Alibaba Group Holding Limited', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'ORCL', 'name': 'Oracle Corporation', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'UA', 'name': 'Under Armour, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'GE', 'name': 'General Electric Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'DIS', 'name': 'Walt Disney Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'VZ', 'name': 'Verizon Communications Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'BA', 'name': 'Boeing Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'CRM', 'name': 'Salesforce.com Inc', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'KO', 'name': 'Coca-Cola Company', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()},
        {'symbol': 'GPRO', 'name': 'GoPro, Inc.', 'is_active': True, 'total_count': 0, 'updated_at': datetime.utcnow()}
    ])


def downgrade():
    pass
