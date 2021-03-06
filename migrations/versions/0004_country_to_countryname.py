"""change country to countryName

Revision ID: f69d4f251a27
Revises: 0003_rent_to_weekly
Create Date: 2018-04-14 12:52:11.062849

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0004_country_to_countryname'
down_revision = '0003_rent_to_weekly'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agency', sa.Column('countryName', sa.Text(), nullable=True))
    op.drop_column('agency', 'country')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agency', sa.Column('country', sa.TEXT(),
                                      autoincrement=False, nullable=True))
    op.drop_column('agency', 'countryName')
    # ### end Alembic commands ###
