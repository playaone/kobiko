"""Bed column added

Revision ID: 557c66fd5575
Revises: 25cde4c67cae
Create Date: 2024-08-11 18:11:10.309543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '557c66fd5575'
down_revision = '25cde4c67cae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bed', sa.String(length=50), server_default='1 queen size bed', nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('room', schema=None) as batch_op:
        batch_op.drop_column('bed')

    # ### end Alembic commands ###
