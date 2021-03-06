"""add agency properties and agent properties

Revision ID: ff57d22feeeb
Revises: 0004_country_to_countryname
Create Date: 2018-04-19 22:59:33.927050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0005_update_properties'
down_revision = '0004_country_to_countryname'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agency', sa.Column('address1', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('address2', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column(
        'agencyLogoUrl', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('domainUrl', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('email', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('fax', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('mobile', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column(
        'numberForRent', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('rentalEmail', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column(
        'rentalTelephone', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('state', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('suburb', sa.Text(), nullable=True))
    op.add_column('agency', sa.Column('telephone', sa.Text(), nullable=True))
    op.add_column('agent', sa.Column(
        'agentAvatarUrl', sa.Text(), nullable=True))
    op.add_column('agent', sa.Column('brandColour', sa.Text(), nullable=True))
    op.add_column('agent', sa.Column(
        'domainProfileUrl', sa.Text(), nullable=True))
    op.add_column('agent', sa.Column('emailAddress', sa.Text(), nullable=True))
    op.add_column('agent', sa.Column('phoneNumber', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('agent', 'phoneNumber')
    op.drop_column('agent', 'emailAddress')
    op.drop_column('agent', 'domainProfileUrl')
    op.drop_column('agent', 'brandColour')
    op.drop_column('agent', 'agentAvatarUrl')
    op.drop_column('agency', 'telephone')
    op.drop_column('agency', 'suburb')
    op.drop_column('agency', 'state')
    op.drop_column('agency', 'rentalTelephone')
    op.drop_column('agency', 'rentalEmail')
    op.drop_column('agency', 'numberForRent')
    op.drop_column('agency', 'mobile')
    op.drop_column('agency', 'fax')
    op.drop_column('agency', 'email')
    op.drop_column('agency', 'domainUrl')
    op.drop_column('agency', 'description')
    op.drop_column('agency', 'agencyLogoUrl')
    op.drop_column('agency', 'address2')
    op.drop_column('agency', 'address1')
    # ### end Alembic commands ###
