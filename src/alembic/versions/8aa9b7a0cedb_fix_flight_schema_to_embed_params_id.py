"""Fix flight schema to embed params id

Revision ID: 8aa9b7a0cedb
Revises: 27613065a23c
Create Date: 2023-10-22 16:06:57.523616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8aa9b7a0cedb'
down_revision: Union[str, None] = '27613065a23c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'flights', sa.Column('parameters_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None,
        'flights',
        'parameters',
        ['parameters_id'],
        ['id'],
        ondelete='CASCADE'
    )
    param_id = sa.table('flights', sa.Column('parameters_id'))
    op.execute(param_id.update().values(parameters_id=1))
    op.alter_column('flights', 'parameters_id', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'flights', type_='foreignkey')
    op.drop_column('flights', 'parameters_id')
    # ### end Alembic commands ###
