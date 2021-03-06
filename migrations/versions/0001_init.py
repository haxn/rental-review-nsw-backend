"""empty message

Revision ID: ae09596f1249
Revises:
Create Date: 2018-04-08 00:03:57.929448

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('email', sa.Text(), nullable=True),
    sa.Column('fbId', sa.Text(), nullable=True),
    sa.Column('profilePicture', sa.Text(), nullable=True),
    sa.Column('createdDate', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('fbId')
    )
    op.create_table('agent',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('agencyId', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['agencyId'], ['agency.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agentRating',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('agentId', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['agentId'], ['agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('property',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('addressString', sa.Text(), nullable=True),
    sa.Column('lat', sa.Float(), nullable=True),
    sa.Column('lng', sa.Float(), nullable=True),
    sa.Column('googlePlacesId', sa.Text(), nullable=True),
    sa.Column('currentAgent', sa.Integer(), nullable=True),
    sa.Column('currentAgency', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['currentAgency'], ['agency.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['currentAgent'], ['agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('propertyId', sa.Integer(), nullable=False),
    sa.Column('userId', sa.Integer(), nullable=False),
    sa.Column('startDate', sa.DateTime(), nullable=True),
    sa.Column('endDate', sa.DateTime(), nullable=True),
    sa.Column('monthlyRent', sa.Float(), nullable=True),
    sa.Column('bond', sa.Float(), nullable=True),
    sa.Column('bondReturned', sa.Boolean(), nullable=True),
    sa.Column('propertyRating', sa.Float(), nullable=True),
    sa.Column('neighbourRating', sa.Float(), nullable=True),
    sa.Column('phoneReception', sa.Float(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['propertyId'], ['property.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['userId'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('property')
    op.drop_table('agentRating')
    op.drop_table('agent')
    op.drop_table('user')
    op.drop_table('agency')
    # ### end Alembic commands ###
