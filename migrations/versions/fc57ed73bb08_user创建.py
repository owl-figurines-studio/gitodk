"""user创建

Revision ID: fc57ed73bb08
Revises: 
Create Date: 2019-12-02 17:52:19.177918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc57ed73bb08'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('is_deleted', sa.Boolean(), nullable=True),
    sa.Column('createtime', sa.DateTime(), nullable=True),
    sa.Column('updatetime', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_phone', sa.String(length=11), nullable=True),
    sa.Column('gender', sa.String(length=11), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_phone')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
