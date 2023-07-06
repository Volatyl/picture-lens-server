"""Edited commetn table

Revision ID: 483c8c2cb687
Revises: e7779d3412a9
Create Date: 2023-07-06 09:08:30.477795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '483c8c2cb687'
down_revision = 'e7779d3412a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('commentText', sa.String(), nullable=True))
    op.drop_column('comments', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('comment', sa.VARCHAR(), nullable=True))
    op.drop_column('comments', 'commentText')
    # ### end Alembic commands ###