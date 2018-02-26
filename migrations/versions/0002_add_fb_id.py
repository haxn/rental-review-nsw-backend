"""empty message

Revision ID: 3dbb7ec4bcd1
Revises: 0001_init_db
Create Date: 2018-02-26 19:02:39.442590

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0002_add_fb_id'
down_revision = '0001_init_db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fb_id', sa.Text(), nullable=True))
    op.create_unique_constraint(None, 'user', ['fb_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'fb_id')
    # ### end Alembic commands ###
