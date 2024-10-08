"""added prices for different types

Revision ID: 585fe54493b9
Revises: 6df11f250118
Create Date: 2024-08-23 09:30:52.875408

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '585fe54493b9'
down_revision = '6df11f250118'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price_regular', sa.Float(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('price_vip', sa.Float(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('price_lounge', sa.Float(), server_default='0', nullable=False))
        batch_op.drop_column('price')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.FLOAT(), nullable=False))
        batch_op.drop_column('price_lounge')
        batch_op.drop_column('price_vip')
        batch_op.drop_column('price_regular')

    # ### end Alembic commands ###
