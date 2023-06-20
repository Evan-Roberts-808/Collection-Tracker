"""add set_img column

Revision ID: a02b1c2133d8
Revises: fddd2199fe8c
Create Date: 2023-06-19 23:59:03.257955

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a02b1c2133d8'
down_revision = 'fddd2199fe8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('set_img', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('sets', schema=None) as batch_op:
        batch_op.drop_column('set_img')

    # ### end Alembic commands ###
