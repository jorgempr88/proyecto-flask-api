"""empty message

Revision ID: a963dd2913d4
Revises: 805bad3cecaa
Create Date: 2023-02-14 21:27:25.597240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a963dd2913d4'
down_revision = '805bad3cecaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ventas', sa.Column('ventas_productos', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ventas', 'ventas_productos')
    # ### end Alembic commands ###
