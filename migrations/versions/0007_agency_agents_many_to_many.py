"""agent agency many to many

Revision ID: e2c6517495f9
Revises: cda43a18d9ca
Create Date: 2018-04-22 19:15:34.009439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0007_agency_agents_many_to_many'
down_revision = 'cda43a18d9ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('agent_identifier',
                    sa.Column('agentId', sa.Integer(), nullable=True),
                    sa.Column('agencyId', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['agencyId'], ['agency.id'], ),
                    sa.ForeignKeyConstraint(['agentId'], ['agent.id'], )
                    )
    op.create_unique_constraint(None, 'agent', ['domainId'])
    op.drop_constraint('agent_agencyId_fkey', 'agent', type_='foreignkey')
    op.drop_column('agent', 'agencyId')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('agent', sa.Column('agencyId', sa.INTEGER(),
                                     autoincrement=False, nullable=False))
    op.create_foreign_key('agent_agencyId_fkey', 'agent', 'agency', ['agencyId'], [
                          'id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_constraint(None, 'agent', type_='unique')
    op.drop_table('agent_identifier')
    # ### end Alembic commands ###
