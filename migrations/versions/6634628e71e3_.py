"""empty message

Revision ID: 6634628e71e3
Revises: 5b5d3f1fa57d
Create Date: 2023-07-10 12:59:41.560507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6634628e71e3'
down_revision = '5b5d3f1fa57d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('aset_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('bookkeeping_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('bookkeeping_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('bookkeeping_asets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('bookkeeping_ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('bussiness_plan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('money_bookkeeping', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('owner_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_deleted', sa.Integer(), nullable=True))
        batch_op.drop_column('deleted_at')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('owner_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('money_bookkeeping', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('bussiness_plan', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('bookkeeping_ticket', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('bookkeeping_asets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('bookkeeping_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('bookkeeping_account', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    with op.batch_alter_table('aset_activity', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deleted_at', sa.DATE(), nullable=True))
        batch_op.drop_column('is_deleted')

    # ### end Alembic commands ###
