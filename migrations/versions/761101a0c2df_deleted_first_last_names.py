"""Deleted first last names

Revision ID: 761101a0c2df
Revises: e16d9d0a6255
Create Date: 2023-07-05 21:07:15.903271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '761101a0c2df'
down_revision = 'e16d9d0a6255'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(), nullable=True))
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(), nullable=True))
    op.add_column('users', sa.Column('first_name', sa.VARCHAR(), nullable=True))
    op.drop_column('users', 'email')
    # ### end Alembic commands ###