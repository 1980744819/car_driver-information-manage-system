"""second migration

Revision ID: ae61f2765b45
Revises: 801d9e9617a8
Create Date: 2017-12-24 19:52:54.680734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ae61f2765b45'
down_revision = '801d9e9617a8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('car_info_list', 'used_time')
    op.add_column('repair_record', sa.Column('is_fixed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('repair_record', 'is_fixed')
    op.add_column('car_info_list', sa.Column('used_time', sa.VARCHAR(length=10, collation='Chinese_PRC_CI_AS'), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
