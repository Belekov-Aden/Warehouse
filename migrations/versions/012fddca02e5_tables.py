"""tables

Revision ID: 012fddca02e5
Revises: f25bbbd7a03f
Create Date: 2024-09-27 19:16:10.825973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '012fddca02e5'
down_revision: Union[str, None] = 'f25bbbd7a03f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('status', sa.Enum('IN_PROCESS', 'SENT', 'DELIVERED', name='statusenum'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_orders_id'), 'orders', ['id'], unique=False)
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('count_in_storage', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_product_id'), 'product', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_product_id'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_orders_id'), table_name='orders')
    op.drop_table('orders')
    # ### end Alembic commands ###
